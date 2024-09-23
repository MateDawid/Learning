# Auto reload

>Source: https://testdriven.io/courses/django-celery/auto-reload/

## Solution 1: Custom Django Command

You can write a Django management command to restart the Celery workers and then hook that command into Django's autoreload utility.

```python
# management/commands/celery_worker.py
import shlex
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    celery_worker_cmd = "celery -A django_celery_example worker"
    cmd = f'pkill -f "{celery_worker_cmd}"'
    if sys.platform == "win32":
        cmd = "taskkill /f /t /im celery.exe"

    subprocess.call(shlex.split(cmd))
    subprocess.call(shlex.split(f"{celery_worker_cmd} --loglevel=info"))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting celery worker with autoreload...")
        autoreload.run_with_reloader(restart_celery)
```

Update compose/local/django/celery/worker/start:

```commandline
#!/bin/bash

set -o errexit
set -o nounset

python manage.py celery_worker
```

Next, you'll need to install the procps package to use the pkill command, so install the package in compose/local/django/Dockerfile:

```Dockerfile
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git procps \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
```

Now after code change worker automatically restarts.

## Solution 2: Watchfiles

Watchfiles (previously called Watchgod), a helpful tool for monitoring file system events, can help us restart Celery worker after code change.

```commandline
pip install watchfiles
```

Assuming you run your Celery worker like so

```commandline
celery -A django_celery_example worker --loglevel=info
```

To incorporate Watchdog, you'd now run it like this:
```commandline
watchfiles --filter python 'celery -A django_celery_example worker --loglevel=info'
```
* `--filter python` tells `watchfiles` to only watch `py` files.
* `celery -A django_celery_example worker --loglevel=info` is the command we want `watchfiles` to run
* By default, watchfiles will watch the current directory and all subdirectories

```commandline
# requirements.txt
watchfiles==0.21.0
```

compose/local/django/celery/worker/start:
```commandline
#!/bin/bash

set -o errexit
set -o nounset

watchfiles \
  --filter python \
  'celery -A django_celery_example worker --loglevel=info'
```
