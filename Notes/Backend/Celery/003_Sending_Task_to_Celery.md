# Sending a Task to Celery

>Source: https://testdriven.io/courses/django-celery/getting-started/#H-7-sending-a-task-to-celery

```python
# django_celery_example/celery.py
"""
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery

from django.conf import settings

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_example.settings')

# you can change the name here
app = Celery("django_celery_example")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
```

Having config like above in celery.py - with Celery app named `django_celery_example` - and Broker (like Redis) running we can run Celery worker like:

```commandline
celery -A django_celery_example worker --loglevel=info
```

To run task manually use:
```commandline
(venv)$ python manage.py migrate
(venv)$ python manage.py shell
>>> from django_celery_example.celery import divide
>>> task = divide.delay(1, 2)
```

What's happening?

1. We used the `delay` method to send a new message to the message broker. The worker process then picked up and executed the task from the queue.
2. After releasing from the Enter key, the code finished executing while the `divide` task ran in the background.

Picture the workflow in your head:

1. The Celery client (the producer) adds a new task to the queue via the message broker.
2. The Celery worker (the consumer) grabs the tasks from the queue, again, via the message broker.
3. Once processed, results are stored in the result backend.

```commandline
>>> task = divide.delay(1, 2)

>>> type(task)
<class 'celery.result.AsyncResult'>
```

After we called the delay method, we get an AsyncResult instance, which can be used to check the task state along with the return value or exception details.

```commandline
>>> print(task.state, task.result)
PENDING None

>>> print(task.state, task.result)
PENDING None

>>> print(task.state, task.result)
PENDING None

>>> print(task.state, task.result)
SUCCESS 0.5

>>> print(task.state, task.result)
SUCCESS 0.5
```

What happens if there's an error?

```commandline
>>> task = divide.delay(1, 0)

# wait a few seconds before checking the state and result

>>> task.state
'FAILURE'

>>> task.result
ZeroDivisionError('division by zero')
```
