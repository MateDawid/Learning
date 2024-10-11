# Config and Best Practices

> Source: https://testdriven.io/courses/django-celery/best-practices/

## SSL Connection

SSL is more secure so it's highly recommended.

```python
CELERY_BROKER_USE_SSL = True
CELERY_REDIS_BACKEND_USE_SSL = True

REDIS_URL = "rediss://{username}:{password}@{host}:{port}?ssl_cert_reqs=CERT_NONE"
CELERY_BROKER_URL = REDIS_URL
```

`rediss` means `redis` + `s`, where the extra `s` means `SSL`. If you set `rediss` in the URL (which, again, causes it to use SSL), you can skip the `CELERY_BROKER_USE_SSL` config. That said, it's always good to be explicit, so it doesn't hurt to do both.

## Celery Task Queue and Routing Config

As mentioned, it's recommended to change the default queue name from `celery` to `default` and to set `CELERY_TASK_CREATE_MISSING_QUEUES` to `False` to prevent typos in your code.

```python
CELERY_TASK_DEFAULT_QUEUE = 'default'

# Force all queues to be explicitly listed in `CELERY_TASK_QUEUES` to help prevent typos
CELERY_TASK_CREATE_MISSING_QUEUES = False

CELERY_TASK_QUEUES = (
    # need to define default queue here or exception would be raised
    Queue('default'),

    Queue('high_priority'),
    Queue('low_priority'),
)

CELERY_TASK_ROUTES = {
    'django_celery_example.celery.*': {
        'queue': 'high_priority',
    },
}
```

## Prefetch Multiplier

Celery's method for prefetching is not very efficient, both dynamically and globally. It can actually cause problems quite often. We recommend limiting prefetching to one so that each worker gets only one message at a time:

```python
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
```

## Acknowledgements

Celery workers send an acknowledgement back to the message broker after a task is picked up from the queue. The broker will usually respond by removing the task from the queue. This can cause problems if the worker dies while running the task and the task has been removed from the queue.

To address this, you can configure the message broker to only acknowledge tasks (and subsequently remove the task from the queue) after the tasks have completed (succeeded or failed):
```python
CELERY_TASK_ACKS_LATE = True
```

## Time Limit

To prevent tasks from hanging, you can set a soft or hard time limit globally or per task when you define or call the task:

```python
# global example
CELERY_TASK_SOFT_TIME_LIMIT = 15 * 60
CELERY_TASK_TIME_LIMIT = CELERY_TASK_SOFT_TIME_LIMIT + 30


# per task when defined
@celery.task(time_limit=30, soft_time_limit=10)
def your_task():
    try:
        return do_something()
    except SoftTimeLimitExceeded:
        cleanup_in_a_hurry()

# per task when called

your_task.apply_async(args=[], kwargs={}, time_limit=30, soft_time_limit=10)
```

If the task exceeds the soft limit, SoftTimeLimitExceeded will be raised.

If the task running time exceeds the hard limit, the worker process will be killed and replaced with a new one.

It's a good idea to set the hard limit greater than the soft limit to let the error reporting code finish.

## Serializer

Everything passed into Celery is serialized and everything that comes out is deserialized. Because of this, it's recommended to force developers into good practices for task arguments by setting task_serializer to json:
```python
CELERY_TASK_SERIALIZER = json
```

> If you're using Celery 4 or greater json is the default.

## Recommended services

Below are some recommended SaaS and PaaS offerings to simplify infrastructure, error handling, and monitoring:

* AWS, Heroku, Fly.io, and Render can save a lot of time and money since they handle nearly all your infrastructure requirements. Plus, they make it very easy to scale based on your app's requirements.
* Sentry aggregates exception info, which can help you with troubleshooting.
* New Relic is a monitoring solution that can help with finding performance bottlenecks.
* Papertrail is logging solution that makes it easy to find and analyze logs.

## Enqueue Reference

If possible, always enqueue a reference to the data rather than the data itself. For example, rather than adding an email address, which could change before the task runs, add the user's primary database key.

From the Celery docs:

Another gotcha is Django model objects. They shouldn’t be passed on as arguments to tasks. It’s almost always better to re-fetch the object from the database when the task is running instead, as using old data may lead to race conditions.

## Specify Task Name

It's a good practice to specify explicit task names instead of letting Celery generate a name based on the module and function name.

```python
name=users.tasks.subscribe
```

This can help prevent naming issues when using relative imports. For more on this, review the [Automatic naming and relative imports guide](https://docs.celeryq.dev/en/stable/userguide/tasks.html#automatic-naming-and-relative-imports) from the docs.

## Avoid Long Running Tasks

You should avoid long running Celery tasks by splitting them up into small tasks. Tasks should also be idempotent, which means that a task won't cause unintended effects even if called multiple times with the same arguments.

For help with building workflows of tasks, check out the [Canvas](https://docs.celeryq.dev/en/stable/userguide/canvas.html) module.