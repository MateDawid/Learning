# Database transactions

> Source: https://testdriven.io/courses/django-celery/database-transactions/

## What is a Database Transaction?

A database transaction is a unit of work that is either committed (applied to the database) or rolled back (undone from the database) as a unit.

Most databases use the following pattern:

1. Begin the transaction.
2. Execute a set of data manipulations and/or queries.
3. If no error occurs, then commit the transaction.
4. If an error occurs, then roll back the transaction.

As you can see, a transaction is a very useful way to keep your data far away from chaos.

## Database Transactions in Django

Assume you have the following view:

```python
def test_view(request):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    logger.info(f'create user {user.pk}')
    raise Exception('test')
```

### Default behavior
Django's default behavior is to autocommit: Each query is directly committed to the database unless a transaction is active. In other words, with autocommit, each query starts a transaction and either commits or rolls back the transaction as well. If you have a view with three queries, then each will run one-by-one. If one fails, the other two will be committed.

So, in the above view, the exception is raised after the transaction is committed, creating the user john.

### Explicit control
If you'd prefer to have more control over database transactions, you can override the default behavior with transaction.atomic. In this mode, before calling a view function, Django starts a transaction. If the response is produced without problems, Django commits the transaction. On the other hand, if the view produces an exception, Django rolls back the transaction. If you have three queries and one fails, then none of the queries will be committed.

Here's how the same example view would look with transaction.atomic:

```python
def transaction_test(request):
    with transaction.atomic():
        user = User.objects.create_user('john1', 'lennon@thebeatles.com', 'johnpassword')
        logger.info(f'create user {user.pk}')
        raise Exception('force transaction to rollback')
```

Now the user create operation will roll back when the exception is raised, so the user will not be created in the end.

transaction.atomic is a very useful tool which can keep your data organized, especially when you need to manipulate data in models.

It can also be used as a decorator like so:

```python
@transaction.atomic
def transaction_test2(request):
    user = User.objects.create_user('john1', 'lennon@thebeatles.com', 'johnpassword')
    logger.info(f'create user {user.pk}')
    raise Exception('force transaction to rollback')
```

So if some error gets raised in the view, and we do not catch it, then the transaction would roll back.

If you want to use transaction.atomic for all view functions, you can set ATOMIC_REQUESTS to True in your Django settings file:

```python
ATOMIC_REQUESTS=True

# or

DATABASES["default"]["ATOMIC_REQUESTS"] = True
```

You can then override the behavior so that the view runs in autocommit mode:

```python
@transaction.non_atomic_requests
```

## DoesNotExist exception

If you don't have a solid understanding of how Django manages database transactions, it can be quite confusing when you come across random database-related errors in a Celery worker.

Add the following view to polls/views.py:

```python
def random_username():
    username = ''.join([random.choice(ascii_lowercase) for i in range(5)])
    return username

@transaction.atomic
def transaction_celery(request):
    username = random_username()
    user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
    logger.info(f'create user {user.pk}')
    task_send_welcome_email.delay(user.pk)

    time.sleep(1)
    return HttpResponse('test')
```

Then, add the task to polls/tasks.py:

```python
@shared_task()
def task_send_welcome_email(user_pk):
    user = User.objects.get(pk=user_pk)
    logger.info(f'send email to {user.email} {user.pk}')
```

1. Since the view uses the transaction.atomic decorator, all database operations are only committed if an error isn't raised in the view, including the Celery task.
2. The task is fairly simple: We create a user and then pass the primary key to the task to send a welcome email.
3. time.sleep(1) is used to introduce a race condition.

Update the URLs in polls/urls.py:

```python
from django.urls import path

from polls.views import subscribe, task_status, webhook_test, webhook_test_async, subscribe_ws, transaction_celery


urlpatterns = [
    path('form/', subscribe, name='form'),
    path('task_status/', task_status, name='task_status'),
    path('webhook_test/', webhook_test, name='webhook_test'),
    path('webhook_test_async/', webhook_test_async, name='webhook_test_async'),
    path('form_ws/', subscribe_ws, name='form_ws'),
    path('transaction_celery/', transaction_celery, name='transaction_celery'),               # new
]
```

Navigate to http://localhost:8010/transaction_celery/ in your browser. You should see the following error in the terminal:

```commandline
django.contrib.auth.models.User.DoesNotExist: User matching query does not exist.
```

Why?

1. In the Django view, we pause for 1 second after enqueueing the task.
2. Since the task executes immediately, user = User.objects.get(pk=user_pk) fails as the user is not in the database because the transaction in Django has not yet been committed.

**Solution 1**
Disable the database transaction, so Django would use the autocommit feature. To do so, you can simply remove the transaction.atomic decorator. However, this isn't recommended since the atomic database transaction is a powerful tool.

**Solution 2**
Force the Celery task to run after a period of time.

For example, to pause for 10 seconds:
```python
task_send_welcome_email.apply_async(args=[user.pk], countdown=10)
```

**Solution 3**
Django has a callback function called transaction.on_commit that executes after a transaction successfully commits. To use this, update the view like so:
```python
from functools import partial


@transaction.atomic
def transaction_celery(request):
    username = random_username()
    user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
    logger.info(f'create user {user.pk}')
    # the task does not get called until after the transaction is committed
    transaction.on_commit(partial(task_send_welcome_email.delay, user.pk))

    time.sleep(1)
    return HttpResponse('test')
```
Notes:

1. Now, the task doesn't get called until after the database transaction commit. So, when the Celery worker finds the user, it can be found because the code in the worker always runs after the Django database transaction commits successfully.
2. Here we use partial to bind the user.pk to the task_send_welcome_email.delay function, this can help avoid the late binding bug brought with lambda in some cases. You can check Performing actions after commit from the Django docs and Use partial() With Django’s transaction.on_commit() to Avoid Late-Binding Bugs to learn more about this.

This is the recommended solution.

> It's worth noting that you may not want your transaction to commit right away, especially if you're running in a high-scale environment. If either the database or instance are at high-utilization, forcing a commit will only add to the existing usage. In this case, you may want to use the second solution and wait for a sufficient amount of time (20 seconds, perhaps) to ensure that the changes are made to the database before the task executes.

## Testing

Django's TestCase wraps each test in a transaction which is then rolled back after each test. Since no transactions are ever committed, on_commit() never runs either. So, if you need to test code fired in an on_commit callback, you can use either TransactionTestCase or TestCase.captureOnCommitCallbacks() in your test code.

## Database Transaction in a Celery Task

If your Celery task needs to update a database record, it makes sense to use a database transaction in the Celery task.

One simple way is with transaction.atomic():

```python
@shared_task()
def task_transaction_test():
    with transaction.atomic():
        from .views import random_username
        username = random_username()
        user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        logger.info(f'send email to {user.pk}')
        raise Exception('test')
```

A better approach is to write a custom decorator which has transaction support:

```python
class custom_celery_task:
    """
    This is a decorator we can use to add custom logic to our Celery task
    such as retry or database transaction
    """
    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                with transaction.atomic():
                    return func(*args, **kwargs)
            except Exception as e:
                # task_func.request.retries
                raise task_func.retry(exc=e, countdown=5)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func

...

@custom_celery_task(max_retries=5)
def task_transaction_test():
    # do something
```