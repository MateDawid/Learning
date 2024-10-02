# Logging

> Source: https://testdriven.io/courses/django-celery/logging/

By default, Celery "hijacks" and modifies the root logger:

```python
root = logging.getLogger()

if self.app.conf.worker_hijack_root_logger:
    root.handlers = []
    get_logger('celery').handlers = []
    get_logger('celery.task').handlers = []
    get_logger('celery.redirected').handlers = []

# Configure root logger
self._configure_logger(
    root, logfile, loglevel, format, colorize, **kwargs
)
```

`worker_hijack_root_logger` defaults to True. So, you can see in the above code that Celery clears the root handlers and resets the root log level. Be aware of this since it can cause some strange problems that are difficult to debug.

## Logging in Celery task

Add the following task to polls/tasks.py:

```python
from celery.utils.log import get_task_logger
...
logger = get_task_logger(__name__)


@shared_task()
def task_test_logger():
    logger.info('test')
```

Notes:
1. With `get_task_logger(__name__)` the logger name will be the module name.
2. `get_task_logger` also adds the `task_name` and `task_id` to the log, which helps us troubleshoot in some cases.
3. Finally, `get_task_logger` sets up one logger called `celery.task`, which is the parent of all task loggers. `get_task_logger(__name__)` builds the relationship for us so we do not need to set up a handler or formatter in the Django logging config.

Test:
```commandline
$ docker compose up -d --build

$ docker compose logs -f
```

Open the shell in a new terminal window:

```commandline
$ docker compose exec web bash
(container)$ ./manage.py shell
>>> from polls.tasks import task_test_logger
>>> task_test_logger.delay()
```

In the logs you should see:

```commandline
django-celery-project-celery_worker-1  | [2024-01-03 01:30:03,253: INFO/ForkPoolWorker-14] polls.tasks.task_test_logger[a6c0506f-53ad-4136-94ff-6e34d6711252]: test
django-celery-project-celery_worker-1  | [2024-01-03 01:30:03,258: INFO/ForkPoolWorker-14] Task polls.tasks.task_test_logger[a6c0506f-53ad-4136-94ff-6e34d6711252] succeeded in 0.005411332997027785s: None
```

To customize the log format, you can modify the worker_log_format and worker_task_log_format config options in the settings file. Just make sure to use CELERY_WORKER_LOG_FORMAT and CELERY_WORKER_TASK_LOG_FORMAT since we set the namespace in django_celery_example/celery.py:
```python
# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')
```

## Custom Celery Task Logging

### (1) Override
You can use the Celery setup_logging signal to completely override Celery's logging configuration.

> Celery won’t configure the loggers if this signal is connected, so you can use it to completely override the logging configuration with your own.

```python
@setup_logging.connect()
def on_setup_logging(**kwargs):
    logging_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file_log': {
                'class': 'logging.FileHandler',
                'filename': 'celery.log',
            },
            'default': {
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'celery': {
                'handlers': ['default', 'file_log'],
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    }

    logging.config.dictConfig(logging_dict)

    # display task_id and task_name in task log
    from celery.app.log import TaskFormatter
    celery_logger = logging.getLogger('celery')
    for handler in celery_logger.handlers:
        handler.setFormatter(
            TaskFormatter(
                '[%(asctime)s: %(levelname)s/%(processName)s/%(thread)d] [%(task_name)s(%(task_id)s)] %(message)s'
            )
        )
```

1. You'll have full control over the root logger and you can use Python's standard logger for logging.
2. As you can see, in the above code, we used TaskFormatter to make the task_id and task_name available in the log format.
3. We can also log concurrency info, like processName and threadName. Review the source code for logging for more info.

### (2) Disable

You can change `worker_hijack_root_logger` to False to prevent Celery from clearing the root handlers and resetting the root log level.

This is the most invasive method, so it should only be used in rare cases.

To use, add the following to the Django settings:

```python
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_log': {
            'class': 'logging.FileHandler',
            'filename': 'celery.log',
        },
        'default': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'celery': {
            'handlers': ['default', 'file_log'],
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['default'],
        'level': 'INFO',
    },
}
```
Here, we used CELERY_WORKER_HIJACK_ROOT_LOGGER to change worker_hijack_root_logger to False, so Celery does not clear the logging handlers when it sets up logging.

### (3) Augment Celery's Logger

You can use the Celery after_setup_logger and after_setup_task_logger signals, which are sent after Celery sets up the logger, to modify the logger.

This is recommended method in most cases since it's the least invasive.

Add the following after_setup_logger handler to django_celery_example/celery.py:

```python
import logging
from celery.signals import after_setup_logger

...

@after_setup_logger.connect()
def on_after_setup_logger(logger, **kwargs):
    formatter = logger.handlers[0].formatter
    file_handler = logging.FileHandler('celery.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
```

You should now be able to see all Celery task logs in celery.log.
