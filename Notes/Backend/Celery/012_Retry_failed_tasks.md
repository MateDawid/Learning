# Retry failed tasks

> Source: https://testdriven.io/courses/django-celery/retrying-failed-tasks/

## Celery Task

```python
@shared_task(bind=True)
def task_process_notification(self):
    try:
        if not random.choice([0, 1]):
            # mimic random error
            raise Exception()

        # this would block the I/O
        requests.post('https://httpbin.org/delay/5')
    except Exception as e:
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)
```

In the real world this may call an internal or external third-party service. Regardless of the service, assume it's very unreliable, especially at peak periods. How can we handle failures?

## Solution 1: Use a Try/Except Block

We've already implemented this solution, but let's quickly review:

1. Since we set bind to True, this is a bound task, so the first argument to the task will always be the current task instance (self). Because of this, we can call self.retry to retry the failed task.
2. Please remember to raise the exception returned by the self.retry method to make it work.
3. By setting the countdown argument to 5, the task will retry after a 5 second delay.

## Solution 2: Task Retry Decorator

Celery 4.0 added built-in support for retrying, so you can let the exception bubble up and specify in the decorator how to handle it:

```python
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 5})
def task_process_notification(self):
    if not random.choice([0, 1]):
        # mimic random error
        raise Exception()

    requests.post('https://httpbin.org/delay/5')
```
Notes:

1. `autoretry_for` takes a list/tuple of exception types that you'd like to retry for.
2. `retry_kwargs` takes a dictionary of additional options for specifying how autoretries are executed. In the above example, the task will retry after a 5 second delay (via countdown) and it allows for a maximum of 7 retry attempts (via `max_retries`). Celery will stop retrying after 7 failed attempts and raise an exception.

## Exponential Backoff

If your Celery task needs to send a request to a third-party service, it's a good idea to use [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff) to avoid overwhelming the service.

```python
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def task_process_notification(self):
    if not random.choice([0, 1]):
        # mimic random error
        raise Exception()

    requests.post('https://httpbin.org/delay/5')
```

In this example, the first retry should run after 1s, the following after 2s, the third one after 0s

```commandline
Task polls.tasks.task_process_notification[fbe041b6-e6c1-453d-9cc9-cb99236df6ff] retry: Retry in 1s: Exception()
Task polls.tasks.task_process_notification[fbe041b6-e6c1-453d-9cc9-cb99236df6ff] retry: Retry in 2s: Exception()
Task polls.tasks.task_process_notification[fbe041b6-e6c1-453d-9cc9-cb99236df6ff] retry: Retry in 0s: Exception()
```

You can also set retry_backoff to a number for use as a delay factor:

```python
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 5})
def task_process_notification(self):
    if not random.choice([0, 1]):
        # mimic random error
        raise Exception()

    requests.post('https://httpbin.org/delay/5')
```

```commandline
Task polls.tasks.task_process_notification[6a0b2682-74f5-410b-af1e-352069238f3d] retry: Retry in 2s: Exception()
Task polls.tasks.task_process_notification[6a0b2682-74f5-410b-af1e-352069238f3d] retry: Retry in 0s: Exception()
Task polls.tasks.task_process_notification[6a0b2682-74f5-410b-af1e-352069238f3d] retry: Retry in 12s: Exception()
```

## Randomness

When you build a custom retry strategy for your Celery task (which needs to send a request to another service), you should add some randomness to the delay calculation to prevent all tasks from being executed simultaneously resulting in a thundering herd.

Celery has you covered here as well with retry_jitter:

```python
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True, retry_kwargs={'max_retries': 5})
def task_process_notification(self):
    if not random.choice([0, 1]):
        # mimic random error
        raise Exception()

    requests.post('https://httpbin.org/delay/5')
```

This option is set to True by default, which helps prevent the thundering herd problem when you use Celery's built-in retry_backoff.

## Task Base Class

If you find yourself writing the same retry arguments in your Celery task decorators, you can (as of Celery 4.4) define retry arguments in a base class, which you can then use as a base class in your Celery tasks:

```python
class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    raise Exception()
```