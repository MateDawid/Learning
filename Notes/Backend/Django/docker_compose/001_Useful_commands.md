# Useful commands

> Source: https://testdriven.io/courses/tdd-django/workflow/

## Common Commands
Build the images:
```
$ docker compose build
```
Run the containers:
```
$ docker compose up -d
```
Create migrations:
```
$ docker compose exec {service_name} python manage.py makemigrations
```
Apply migrations:
```
$ docker compose exec {service_name} python manage.py migrate
```
Seed the database:
```
$ docker compose exec {service_name} python manage.py loaddata data.json
```
Run the tests:
```
$ docker compose exec {service_name} pytest -p no:warnings
```
Run the tests with coverage:
```
$ docker compose exec {service_name} pytest -p no:warnings --cov=.
```
Lint:
```
$ docker compose exec {service_name} flake8 .
```
Run Black and isort with check options:
```
$ docker compose exec {service_name} black --exclude=migrations --check .
$ docker compose exec {service_name} isort . --check-only
```
Make code changes with Black and isort:
```
$ docker compose exec {service_name} black --exclude=migrations .
$ docker compose exec {service_name} isort .
```

## Other Commands
To stop the containers:
```
$ docker compose stop
```
To bring down the containers:
```
$ docker compose down
```
Want to force a build?
```
$ docker compose build --no-cache
```
Remove images:
```
$ docker rmi $(docker images -q)
```

## Postgres
Want to access the database via psql?

```
$ docker compose exec {db_service_name} psql -d {POSTGRES_DB} -U {POSTGRES_USER}
```
Then, you can connect to the database and run SQL queries. For example:
```
# select * from {table_name};
```
