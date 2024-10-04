# Testing with Pytest

> Source: https://testdriven.io/courses/django-celery/pytest/

## Sample View and Task

Assume you have a Django view that accepts a username and email via a POST request. In the view, the user info is added to the database and a Celery task is enqueued that subscribes the user to a mailing list via a third-party API.

Add the view to polls/views.py:

```python
@transaction.atomic
def user_subscribe(request):
    """
    This Django view saves user info to the db and sends task to Celery worker
    to subscribe the user to the database
    """
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            instance, flag = User.objects.get_or_create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            transaction.on_commit(
                lambda: task_add_subscribe.delay(instance.pk)
            )
            return HttpResponseRedirect('')
    else:
        form = YourForm()

    return render(request, 'user_subscribe.html', {'form': form})
```
Notes:

1. As mentioned, it's recommended to use transaction.atomic or ATOMIC_REQUESTS=True, so atomicity on the database is guaranteed.
2. Since we wrapped our Django view with transaction.atomic, transaction.on_commit is used to register the callback function to call the Celery task. Review the Database Transactions chapter for more on this.

Next, add the task to polls/tasks.py:

```python
@shared_task(bind=True)
def task_add_subscribe(self, user_pk):
    try:
        user = User.objects.get(pk=user_pk)
        requests.post(
            'https://httpbin.org/delay/5',
            data={'email': user.email},
        )
    except Exception as exc:
        raise self.retry(exc=exc)
```

Notes:

1. requests.post mimics the behavior of calling a third-party API.
2. If an exception is raised, the Celery task will retry via raise self.retry(exc=exc).

Wire up the path in polls/urls.py:

```python
from django.urls import path

from polls.views import (
    subscribe,
    task_status,
    webhook_test,
    webhook_test_async,
    subscribe_ws,
    transaction_celery,
    user_subscribe
)

urlpatterns = [
    path('form/', subscribe, name='form'),
    path('task_status/', task_status, name='task_status'),
    path('webhook_test/', webhook_test, name='webhook_test'),
    path('webhook_test_async/', webhook_test_async, name='webhook_test_async'),
    path('form_ws/', subscribe_ws, name='form_ws'),
    path('transaction_celery/', transaction_celery, name='transaction_celery'),
    path('user_subscribe/', user_subscribe, name='user_subscribe'),
]
```

Create polls/templates/user_subscribe.html

```html
<form class="your-form" method="post">
  {% csrf_token %}

  {{ form.as_p }}

  <button type="submit">Submit</button>

</form>
```

## pytest Setup

Start by adding pytest and pytest-django, a pytest plugin that provides a set of tools made specifically for testing Django applications, to your requirements file:

```
pytest==7.4.4
pytest-django==4.7.0
```

Next, create a pytest.ini file for configuring pytest in the root of your project directory:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = tests.settings
```

The `DJANGO_SETTINGS_MODULE` setting tells pytest where to find the Django settings.

Next, create a "tests" directory, again, in the root directory and add the following files and folders to it:

```
tests
├── __init__.py
├── polls
│   ├── test_task.py
│   └── test_view.py
└── settings.py
```

settings.py is a Django settings file, which will be used by pytest. We can add custom settings to it as necessary. Update it like so, to pull in the all settings from your project:

```python
from django_celery_example.settings import *
```

## Fixtures

With regard to testing, fixtures are used to create a known state or a baseline before tests run.

> With the built-in Django testing framework, the term fixture is usually used to reference a file that contains test data generated from the dumpdata management command. Just keep it mind that a test fixture is much more than that.

In pytest land, fixtures are used to manage test dependencies and data as well as mocking and patching.

To see all the default plugins that pytest and pytest-django ship with, run the following command:

```commandline
$ docker compose exec web python -m pytest --fixtures
```

In the above output, you should see a fixture for the Django test client called client:

```
client
    A Django test client instance.
```

Let's take a quick look at the source code:

```python
@pytest.fixture()
def client() -> "django.test.client.Client":
    """A Django test client instance."""
    skip_if_no_django()

    from django.test.client import Client

    return Client()
```

This is just a pytest fixture -- @pytest.fixture() is used to mark the function as a pytest fixture -- that returns the Django test client. Let's look at how to use it.

```python
def test_client(client):
    response = client.get('/')
    assert response.status_code == 200
```

This is a very simple test that just asserts that a 200 response is returned when a GET request is sent to '/'. Take note ot the test arg: client. This relates back to the client fixture. When the tests are run, pytest searches for a fixture called client, executes it, and passes the return value to the test function.

So, fixtures can be used to abstract out setup code for our tests. It helps keep our test code DRY as well.

## Custom Fixture

Custom fixtures are generally added to a conftest.py file. Add this file to "tests".

Next, let's look at how to add some dummy data to our test with factory_boy.

Why dummy data? Sometimes you need to create some basic test data in order to ensure that the code behaves in a specific way given different types of data.

With factory_boy we can create test data during the test.

Add the following fixture to tests/conftest.py:

```python
import pytest
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from factory import Faker

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = LazyAttribute(lambda o: '%s@example.com' % o.username)
    password = LazyAttribute(lambda o: make_password(o.username))
    first_name = Faker("first_name")
    last_name = Faker("last_name")



@pytest.fixture()
def user():
    return UserFactory()
```

Here, we created a UserFactory and user fixture, which can help us quickly create user instances with fake data for use in our tests.

Add factory_boy to the requirements.txt file:

```
factory-boy==3.3.0
```

## Monkeypatching

pytest comes with a default fixture called monkeypatch that can be used for mocking and patching:

```
monkeypatch
    The returned ``monkeypatch`` fixture provides these
    helper methods to modify objects, dictionaries or os.environ::

        monkeypatch.setattr(obj, name, value, raising=True)
        monkeypatch.delattr(obj, name, raising=True)
        monkeypatch.setitem(mapping, name, value)
        monkeypatch.delitem(obj, name, raising=True)
        monkeypatch.setenv(name, value, prepend=False)
        monkeypatch.delenv(name, raising=True)
        monkeypatch.syspath_prepend(path)
        monkeypatch.chdir(path)

    All modifications will be undone after the requesting
    test function or fixture has finished. The ``raising``
    parameter determines if a KeyError or AttributeError
    will be raised if the set/deletion operation has no target.
```

> If you prefer the mock.patch style, you can still use it in pytest.

## Test Django View

Add the following test to tests/polls/test_view.py:

```python
from unittest import mock

from django.contrib.auth.models import User
from django.urls import reverse

from polls import tasks


def test_subscribe_post_succeed(transactional_db, monkeypatch, client, user):
    mock_task_add_subscribe_delay = mock.MagicMock(name="task_add_subscribe_delay")
    monkeypatch.setattr(tasks.task_add_subscribe, 'delay', mock_task_add_subscribe_delay)

    response = client.post(
        reverse('user_subscribe'),
        {
            'username': user.username,
            'email': user.email,
        }
    )

    assert response.status_code == 302
    assert User.objects.filter(username=user.username).exists() is True

    user = User.objects.filter(username=user.username).first()
    mock_task_add_subscribe_delay.assert_called_with(
        user.pk
    )
```

Notes:

1. `transactional_db` is a fixture from pytest-django that adds transaction support to the test. Without it, each test is wrapped in a transaction, which is then rolled back after each test. Since no transactions are ever committed, on_commit() never runs either. So, if you need to test code fired in an on_commit callback within pytest, you can use the transactional_db fixture. It's akin to using Django's TransactionTestCase.
2. The `monkeypatch` fixture is used to patch the task_add_subscribe.delay method in the Django view.
3. The `client` fixture is used to send requests to our Django view.

Everything works fine thus far, but there is one small issue: transactional_db slows the test down. Although speed is not an issue with this one test, it can become an issue for larger test suites. Fortunately, we can use the django_capture_on_commit_callbacks fixture to call on_commit without having to use the transactional_db fixture.

```python
from unittest import mock

from django.contrib.auth.models import User
from django.urls import reverse

from polls import tasks


def test_subscribe_post_succeed(db, monkeypatch, client, user, django_capture_on_commit_callbacks):
    mock_task_add_subscribe_delay = mock.MagicMock(name="task_add_subscribe_delay")
    monkeypatch.setattr(tasks.task_add_subscribe, 'delay', mock_task_add_subscribe_delay)

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        response = client.post(
            reverse('user_subscribe'),
            {
                'username': user.username,
                'email': user.email,
            }
        )

    assert response.status_code == 302
    assert User.objects.filter(username=user.username).exists() is True

    user = User.objects.filter(username=user.username).first()
    mock_task_add_subscribe_delay.assert_called_with(
        user.pk
    )
```

Notes:

1. For the database fixture, we used db instead of transactional_db.
2. We wrapped the call with with django_capture_on_commit_callbacks(execute=True).

## pytest-factoryboy

Before moving on, let's take a quick look at another pytest extension called pytest-factoryboy, which, as the name suggests, integrates factory_boy with pytest.

It can become tedious creating pytest fixtures for each factory model instance (UserFactory). We can use pytest-factoryboy to simplify this.

Add it to the requirements file:

```
pytest-factoryboy==2.6.0
```

Update tests/conftest.py:

```python
from pytest_factoryboy import register
from polls.factories import UserFactory


register(UserFactory)
```

We removed the user fixture that we just created, and then "registered" the factory, as a Model Fixture. This will implement an instance of the model created by the factory with the model's lowercase-underscore class name. In other words, in our tests, we'll have access to a variable called user created by UserFactory automatically.

