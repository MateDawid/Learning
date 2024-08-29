# Poetry
Dependency management tool for Python. Works well with pyenv.

## New project
```commandline
$ poetry new sample-project
$ cd sample-project
```
This will create the following files and folders:

```
sample-project
├── README.rst
├── pyproject.toml
├── sample_project
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_sample_project.py
```

## pyproject.toml
Dependencies are managed inside the pyproject.toml file:
```toml
[tool.poetry]
name = "sample-project"
version = "0.1.0"
description = ""
authors = ["John Doe <john@doe.com>"]

[tool.poetry.dependencies]
python = "^3.10"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```
## Add new dependency
To add new a dependency, simply run:
```commandline
$ poetry add [--dev] <package name>
```

The --dev flag indicates that the dependency is meant to be used in development mode only. Development dependencies are not installed by default.

For example:

```commandline
$ poetry add flask
```
This downloads and installs Flask from PyPI inside the virtual environment managed by Poetry, adds it along with all sub-dependencies to the poetry.lock file, and automatically adds it (a top-level dependency) to pyproject.toml:

```toml
[tool.poetry.dependencies]
python = "^3.10"
Flask = "^2.0.3"
```
## Running command in virtual environment
To run a command inside the virtual environment, prefix the command with poetry run. For example, to run tests with pytest:
```commandline
$ poetry run python -m pytest
```
poetry run <command> will run commands inside the virtual environment. It doesn't activate the virtual environment, though.
