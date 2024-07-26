# Multi-stage Builds

Source: https://testdriven.io/blog/docker-best-practices/#use-multi-stage-builds

Multi-stage Docker builds allow you to break up your Dockerfiles into several stages. For example, you can have a stage for compiling and building your application, which can then be copied to subsequent stages. Since only the final stage is used to create the image, the dependencies and tools associated with building your application are discarded, leaving a lean and modular production-ready image.

```dockerfile
# temp stage
FROM python:3.12.2-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.12.2-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*
```

In this example, the GCC compiler is required for installing certain Python packages, so we added a temp, build-time stage to handle the build phase. Since the final run-time image does not contain GCC, it's much lighter and more secure.

Size comparison:
```commandline
REPOSITORY                 TAG                    IMAGE ID       CREATED          SIZE
docker-single              latest                 8d6b6a4d7fb6   16 seconds ago   259MB
docker-multi               latest                 813c2fa9b114   3 minutes ago    156MB
```