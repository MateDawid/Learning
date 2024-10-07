# Custom task decorator

> Source: https://testdriven.io/courses/django-celery/celery-task-decorator/

Start by adding the following class-based decorator to a new file called base_task.py in the "polls" folder:

## Task decorator

```python
import functools

from celery import shared_task


class custom_celery_task:

    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            # you can add custom code here
            return func(*args, **kwargs)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func
```

Next, we'll add code to the wrapper function for supporting database transactions and handling retries.

Add the following to the wrapper function to enable database transactions:

```python
with transaction.atomic():
    # add Django db transaction support
    return func(*args, **kwargs)
```

As for the retry strategy, let's first look at how Celery handles this:

```python
if autoretry_for and not hasattr(task, '_orig_run'):

    @wraps(task.run)
    def run(*args, **kwargs):
        try:
            return task._orig_run(*args, **kwargs)
        except Ignore:
            # If Ignore signal occurs task shouldn't be retried,
            # even if it suits autoretry_for list
            raise
        except Retry:
            raise
        except dont_autoretry_for:
            raise
        except autoretry_for as exc:
            if retry_backoff:
                retry_kwargs['countdown'] = \
                    get_exponential_backoff_interval(
                        factor=int(max(1.0, retry_backoff)),
                        retries=task.request.retries,
                        maximum=retry_backoff_max,
                        full_jitter=retry_jitter)
            # Override max_retries
            if hasattr(task, 'override_max_retries'):
                retry_kwargs['max_retries'] = getattr(task,
                                                      'override_max_retries',
                                                      task.max_retries)
            ret = task.retry(exc=exc, **retry_kwargs)
            # Stop propagation
            if hasattr(task, 'override_max_retries'):
                delattr(task, 'override_max_retries')
            raise ret

    task._orig_run, task.run = task.run, run
```

The logic here is fairly simple:

1. Celery replaces a Task's run method with the above run function.
2. Within the function, a try/except block is used to run the task code. If an exception is raised, the Celery task will retry via task.retry(exc=exc, **retry_kwargs).
3. get_exponential_backoff_interval is used to calculate the countdown.

Edit polls/base_task.py

```python
import functools
from django.db import transaction
from celery import shared_task
from celery.utils.time import get_exponential_backoff_interval


class custom_celery_task:
    EXCEPTION_BLOCK_LIST = (
        IndexError,
        KeyError,
        TypeError,
        UnicodeDecodeError,
        ValueError,
    )

    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                with transaction.atomic():
                    # add Django db transaction support
                    return func(*args, **kwargs)
            except self.EXCEPTION_BLOCK_LIST:
                # do not retry for those exceptions
                raise
            except Exception as e:
                # here we add Exponential Backoff just like Celery
                countdown = self._get_retry_countdown(task_func)
                raise task_func.retry(exc=e, countdown=countdown)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func

    def _get_retry_countdown(self, task_func):
        retry_backoff = int(
            max(1.0, float(self.task_kwargs.get('retry_backoff', True)))
        )
        retry_backoff_max = int(
            self.task_kwargs.get('retry_backoff_max', 600)
        )
        retry_jitter = self.task_kwargs.get(
            'retry_jitter', True
        )

        countdown = get_exponential_backoff_interval(
            factor=retry_backoff,
            retries=task_func.request.retries,
            maximum=retry_backoff_max,
            full_jitter=retry_jitter
        )

        return countdown
```

Notes:

1. We used a try/except block to only retry specific exceptions found in EXCEPTION_BLOCK_LIST. You can modify the exception list based on your needs.
2. We used _get_retry_countdown to calculate the countdown.

## Using a Custom Task Decorator

Add the following task to polls/tasks.py:

```python
from polls.base_task import custom_celery_task

@custom_celery_task(max_retries=3)
def task_transaction_test():
    from .views import random_username
    username = random_username()
    user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
    user.save()
    logger.info(f'send email to {user.pk}')
    # this cause db rollback because of transaction.atomic
    raise Exception('test')
```

## Testing a Custom Task Decorator

Add the following task and test to a new file called test_base_task.py in "tests/polls":

```python
# tasks

@custom_celery_task()
def successful_task(user_pk):
    user = User.objects.get(pk=user_pk)
    user.username = 'test'
    user.save()


# tests

@pytest.mark.django_db()
def test_custom_celery_task(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True

    instance = UserFactory.create()
    successful_task.delay(instance.pk)

    assert User.objects.get(pk=instance.pk).username == 'test'
```

This test just tests the happy path. In other words, it ensures that when we use the decorator, the code in the task function executes as expected.

What else should be tested?

1. If an exception is raised, the database transaction is rolled back.
2. If an exception in EXCEPTION_BLOCK_LIST is raised, the task does not retry.
3. If an exception which is not in EXCEPTION_BLOCK_LIST is raised, the task retries.

Add the following task and test for ensuring that the database transaction is properly rolled back:

```python
@custom_celery_task()
def throwing_task(user_pk):
    user = User.objects.get(pk=user_pk)
    user.username = 'test'
    user.save()
    # no retry in this task
    raise TypeError


@pytest.mark.django_db()
def test_db_transaction(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    instance = UserFactory.create()

    with pytest.raises(TypeError):
        throwing_task.delay(instance.pk)

    assert User.objects.get(pk=instance.pk).username != 'test'
```

Notes:

1. The exception in the task causes the transaction rollback, so the username is not changed. (Even if it runs before the exception.)
2. By default, Celery's eager mode does not raise exceptions, so we need to set settings.CELERY_TASK_EAGER_PROPAGATES to True to make it work.

Next, add the tasks and tests for testing the EXCEPTION_BLOCK_LIST and the retry logic:

```python
from unittest import mock


@custom_celery_task()
def throwing_no_retry_task():
    raise TypeError


@custom_celery_task()
def throwing_retry_task():
    raise Exception


@pytest.mark.django_db()
def test_throwing_no_retry_task(settings):
    """
    If the exception is in EXCEPTION_BLOCK_LIST, should not retry the task
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(TypeError):
            throwing_no_retry_task.delay()

        mock_retry.assert_not_called()


@pytest.mark.django_db()
def test_throwing_retry_task(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(Exception):
            throwing_retry_task.delay()

        mock_retry.assert_called()
        assert 'countdown' in mock_retry.call_args.kwargs
```