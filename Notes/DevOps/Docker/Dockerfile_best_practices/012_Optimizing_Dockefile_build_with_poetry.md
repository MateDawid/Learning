# Optimizing Dockerfile build with poetry

Source: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

## Project structure

``` 
.
├── Dockerfile
├── README.md
├── annapurna
│   ├── __init__.py
│   └── main.py
├── poetry.lock
└── pyproject.toml
```

pyproject.toml
```toml
[tool.poetry]
name = "annapurna"
version = "1.0.0"
description = ""
authors = ["Riccardo Albertazzi <my@email.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"

fastapi = "^0.95.1"


[tool.poetry.group.dev.dependencies]
black = "^23.3.0"
mypy = "^1.2.0"
ruff = "^0.0.263"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Naive approach

```dockerfile
FROM python:3.11-buster

RUN pip install poetry

COPY .. .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

## First improvements

```dockerfile
FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY annapurna ./annapurna
RUN touch README.md

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

* Pin the `poetry` version, as Poetry can contain breaking changes from one minor version to other, and you don’t want your builds to suddenly break when a new version is released. 
* Just `COPY` the data that you need, and nothing else. 
* Poetry will complain if a README.md is not found (I don’t really share this choice) and as such I create an empty one. 
* Avoid installing development dependencies with `poetry install --without dev` , as you won’t need linters and tests suites in your production environment.

## Cleaning Poetry cache

```dockerfile
FROM python:3.11-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY annapurna ./annapurna
RUN touch README.md

RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

* By default, Poetry caches downloaded packages so that they can be re-used for future installation commands. We clearly don’t care about this in a Docker build (do we?) and as such we can remove this duplicate storage.
* When removing the cache folder make sure this is done in the same RUN command. If it’s done in a separate RUN command the cache will still be part of the previous Docker layer (the one containing poetry install ), effectively rendering your optimization useless.
* While doing this I’m also setting a few Poetry environment variables to further strengthen the determinism of my build. The most controversial one is POETRY_VIRTUALENVS_CREATE=1. What’s the point why would I want to create a virtual environment inside a Docker container? I honestly prefer this solution over who disables this flag, as it makes sure that my environment will be as isolated as possible and above all that my installation will not mess up with the system Python or, even worse, with Poetry itself.

## Installing dependencies before copying code 

```dockerfile
FROM python:3.11-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY annapurna ./annapurna

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

* The solution here is to provide Poetry with the minimal information needed to build the virtual environment and only later COPY our codebase. We can achieve this with the --no-root option, which instructs Poetry to avoid installing the current project into the virtual environment.
* The additional RUN poetry install --without dev instruction is needed to install your project in the virtual environment. This can be useful for example for installing any custom script. Depending on your project you may not even need this step. Anyways, this layer execution will be super fast since the project dependencies have already been installed.

## Using Docker multi-stage builds

```dockerfile
# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY annapurna ./annapurna

ENTRYPOINT ["python", "-m", "annapurna.main"]
```
* Python `buster` is a big image that comes with development dependencies, and we will use it to install a virtual environment. Python `slim-buster` is a smaller image that comes with the minimal dependencies to just run Python, and we will use it to run our application.
* Poetry isn’t even installed in the runtime stage. Poetry is in fact an unnecessary dependency for running your Python application once your virtual environment is built. We just need to play with environment variables (such as the VIRTUAL_ENV variable) to let Python recognize the right virtual environment.
* For simplicity I removed the second installation step (`RUN poetry install --without dev `) as I don’t need it for my toy project, although one could still add it in the runtime image in a single instruction: `RUN pip install poetry && poetry install --without dev && pip uninstall poetry` .

## Buildkit Cache Mounts

```dockerfile
FROM python:3.11-buster as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY annapurna ./annapurna

ENTRYPOINT ["python", "-m", "annapurna.main"]
```

* Once Dockerfiles get more complex I also suggest using Buildkit, the new build backend plugged into the Docker CLI. If you are looking for fast and secure builds, that’s the tool to use.
```
DOCKER_BUILDKIT=1 docker build --target=runtime .
```
* This final trick is not known to many as it’s rather newer compared to the other features I presented. It leverages Buildkit cache mounts, which basically instruct Buildkit to mount and manage a folder for caching reasons. The interesting thing is that such cache will persist across builds!
* By plugging this feature with Poetry cache (now you understand why I did want to keep caching?) we basically get a dependency cache that is re-used every time we build our project. The result we obtain is a fast dependency build phase when building the same image multiple times on the same environment.
* Note how the Poetry cache is not cleared after installation, as this would prevent to store and re-use the cache across builds. This is fine, as Buildkit will not persist the managed cache in the built image (plus, it’s not even our runtime image).