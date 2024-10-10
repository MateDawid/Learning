# Deployment

> Source: https://testdriven.io/courses/django-celery/deployment/

## Compose file

Start by creating a new compose file called docker-compose.prod.yml for the production infrastructure:

```yaml
version: '3.8'

services:

  nginx:
    build: ./compose/production/nginx
    volumes:
      - staticfiles:/app/staticfiles
      - mediafiles:/app/mediafiles
    ports:
      - 80:80
      - 5555:5555
      - 15672:15672
    depends_on:
      - web
      - flower

  web:
    build:
      context: .
      dockerfile: ./compose/production/django/Dockerfile
    command: /start
    volumes:
      - staticfiles:/app/staticfiles
      - mediafiles:/app/mediafiles
    env_file:
      - ./.env/.prod-sample
    depends_on:
      - redis
      - db

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=hello_django
      - POSTGRES_USER=hello_django
      - POSTGRES_PASSWORD=hello_django

  redis:
    image: redis:7-alpine

  rabbitmq:
    image: rabbitmq:3-management
    env_file:
      - ./.env/.prod-sample

  celery_worker:
    build:
      context: .
      dockerfile: ./compose/production/django/Dockerfile
    image: django_celery_example_celery_worker
    command: /start-celeryworker
    volumes:
      - staticfiles:/app/staticfiles
      - mediafiles:/app/mediafiles
    env_file:
      - ./.env/.prod-sample
    depends_on:
      - redis
      - db

  celery_beat:
    build:
      context: .
      dockerfile: ./compose/production/django/Dockerfile
    image: django_celery_example_celery_beat
    command: /start-celerybeat
    volumes:
      - staticfiles:/app/staticfiles
      - mediafiles:/app/mediafiles
    env_file:
      - ./.env/.prod-sample
    depends_on:
      - redis
      - db

  flower:
    build:
      context: .
      dockerfile: ./compose/production/django/Dockerfile
    image: django_celery_example_celery_flower
    command: /start-flower
    volumes:
      - staticfiles:/app/staticfiles
      - mediafiles:/app/mediafiles
    env_file:
      - ./.env/.prod-sample
    depends_on:
      - redis
      - db

volumes:
  postgres_data:
  staticfiles:
  mediafiles:
```

1. The production app uses Nginx as a reverse proxy.
2. For the message broker, we're using RabbitMQ instead of Redis.
3. Environment variables are stored in ./.env/.prod-sample.
4. Both static and media files are stored in Docker volumes.

![flow](_images/018_flow.png)

## Nginx

```yaml
nginx:
  build: ./compose/production/nginx
  volumes:
    - staticfiles:/app/staticfiles
    - mediafiles:/app/mediafiles
  ports:
    - 80:80
    - 5555:5555
    - 15672:15672
  depends_on:
    - web
    - flower
```

1. As you can see, we used a custom Dockerfile (compose/production/nginx/Dockerfile) to build the nginx service image.
2. Nginx will listen on three ports:
   1. 80 for Django
   2. 5555 for Flower
   3. 15672 for the RabbitMQ dashboard
 
Next, create a "production" folder inside the "compose folder and add the following files and folders it:

```
production
├── django
└── nginx
    ├── Dockerfile
    └── nginx.conf
```

compose/production/nginx/Dockerfile:

```dockerfile
FROM nginx:1.25.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

compose/production/nginx/nginx.conf:

```
upstream hello_django {
    server web:8000;
}

upstream celery_flower {
    server flower:5555;
}

upstream rabbitmq {
    server rabbitmq:15672;
}

server {
    listen 80;
    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        client_max_body_size 20M;
    }
    location /static/ {
        alias /app/staticfiles/;
    }
    location /media/ {
        alias /app/mediafiles/;
    }

    location /ws {
        proxy_pass http://hello_django;
        proxy_http_version  1.1;
        proxy_set_header    Upgrade $http_upgrade;
        proxy_set_header    Connection "upgrade";
        proxy_set_header    Host $http_host;
        proxy_set_header    X-Real-IP $remote_addr;
    }
}

server {
    listen 5555;
    location / {
        proxy_pass http://celery_flower;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}


server {
    listen 15672;
    location / {
        proxy_pass http://rabbitmq;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

> A reverse proxy handles requests from the Internet and forwards them along to the services in an internal network.

## Django service

### Dockerfile
To simplify the config, the web and celery services use the same Dockerfile and entrypoint.

compose/production/django/Dockerfile:

```dockerfile
FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential netcat \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

RUN mkdir /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles
WORKDIR /app

# copy project code
COPY . .

RUN chown -R django:django /app

USER django

ENTRYPOINT ["/entrypoint"]
```

1. For security purposes, we added a django user and used it to run the entrypoint command.
2. When the image is built, the source code is copied over to the image and the appropriate permissions are set.
3. We also created folders for the static and media files -- "staticfiles" and "mediafiles", respectively -- to prevent any permission issues. (You can ignore this if you use a third-party service like AWS S3 for static and mediafiles.)

### Entrypoint

Next, add compose/production/django/entrypoint:

```bash
#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'


rabbitmq_ready() {
    echo "Waiting for rabbitmq..."

    while ! nc -z rabbitmq 5672; do
      sleep 1
    done

    echo "rabbitmq started"
}

rabbitmq_ready

exec "$@"
```

1. In the entrypoint, we added a rabbitmq_ready function to check if RabbitMQ is up and running.
2. exec "$@" is used to make the entrypoint a "pass through" to ensure that Docker runs the command the user passes in (command: /start, in our case). For more, review this Stack Overflow answer.

### Start Scripts

Start by updating the files and folders in the "compose/production/django" folder so it looks like this:

```
└── django
    ├── Dockerfile
    ├── celery
    │   ├── beat
    │   │   └── start
    │   ├── flower
    │   │   └── start
    │   └── worker
    │       └── start
    ├── entrypoint
    └── start
```

compose/production/django/start:

```bash
#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py collectstatic --noinput
python /app/manage.py migrate

/usr/local/bin/gunicorn django_celery_example.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --chdir=/app
```

After running the collectstatic command to collect static files in the "app/staticfiles" folder, we used Gunicorn and Uvicorn to run the Django app instead of the Django development server.

> Uvicorn, an ASGI server, is required by Django Channels.

compose/production/django/celery/worker/start:

```bash
#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

exec celery -A django_celery_example worker -l INFO
```

> For the production app, we added exec before the command. This helps to make sure that the Celery worker shuts down gracefully. For more, check out [What are the uses of the exec command in shell scripts](https://stackoverflow.com/questions/18351198/what-are-the-uses-of-the-exec-command-in-shell-scripts) and [Fix ungraceful Celery workers shutdown in container](https://github.com/cookiecutter/cookiecutter-django/pull/3405https://github.com/cookiecutter/cookiecutter-django/pull/3405).

compose/production/django/celery/beat/start:

```bash
#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


exec celery -A django_celery_example beat -l INFO
```

compose/production/django/celery/flower/start:

```bash
#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A django_celery_example inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

exec celery -A django_celery_example \
    --broker="${CELERY_BROKER}" \
    flower \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
```

In this final script, we used the same logic from our entrypoint to ensure that Flower doesn't start until the workers are ready.

### Environment Variables

Create a new file to store production environment variables called .prod-sample in the ".env" folder:

```
DEBUG=0
SECRET_KEY=dbaa1_i7%*3r9-=z-+_mz4r-!qeed@(-a_r(g@k8jo8y3r27%m
DJANGO_ALLOWED_HOSTS=*

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432

RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=admin

CELERY_BROKER=amqp://admin:admin@rabbitmq:5672/
CELERY_BACKEND=redis://redis:6379/0

CELERY_FLOWER_USER=admin
CELERY_FLOWER_PASSWORD=admin

CHANNELS_REDIS=redis://redis:6379/0
```

> In real projects, DO NOT put sensitive info in the source code.

Let's update django_celery_example/settings.py to read theSECRET_KEY, DEBUG and ALLOWED_HOSTS environment variables:

```python
SECRET_KEY = os.environ.get("SECRET_KEY", "&nl8s430j^j8l*je+m&ys5dv#zoy)0a2+x1!m8hx290_sx&0gh")

DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(" ")
```

### Simple Test 

Add Gunicorn and uvicorn to the requirements file:

```
gunicorn==21.2.0
uvicorn[standard]==0.25.0
```

Update the static and media file config in django_celery_example/settings.py:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
```

Let's test the production config locally:

```
$ docker compose stop

$ docker compose -f docker-compose.prod.yml -p django-celery-prod up -d --build

$ docker compose -f docker-compose.prod.yml -p django-celery-prod logs -f
```

1. -f docker-compose.prod.yml tells Docker to use the production config file instead of the default docker-compose.yml file.
2. -p django-celery-prod changes the project name from <directory_name>-<service_name> to django-celery-prod-<service_name> -- i.e., django-celery-prod-web -- to prevent a clash with the development services. For more on this, check our the Docker docs.
3. The following services should be available via your web browser:
   1. Gunicorn/Django: http://localhost:80/form
   2. Flower: http://localhost:5555 (use `admin` for the username and password)
   3. RabbitMQ dashboard: http://localhost:15672 (use `admin` for the username and password)

Bring the services (and volumes) down once done:

```
# cleanup
$ docker compose -f docker-compose.prod.yml -p django-celery-prod stop

# delete containers and volumes
$ docker compose -f docker-compose.prod.yml -p django-celery-prod down -v

# verify
$ docker compose -f docker-compose.prod.yml -p django-celery-prod ps

Name   Command   State   Ports
------------------------------
```

### Deploy to DigitalOcean

Process described [here](https://testdriven.io/courses/django-celery/deployment/#H-9-deploy-to-digitalocean).