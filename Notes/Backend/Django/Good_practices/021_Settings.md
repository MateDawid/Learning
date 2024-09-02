# Settings

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#settings

## Organization

When it comes to Django settings, we tend to follow the folder structure from cookiecutter-django, with few adjustments:

* We separate Django specific settings from other settings.
* Everything should be included in base.py.
    * There should be nothing that's only included in production.py.
    * Things that need to only work in production are controlled via environment variables.

Here's the folder structure of our Styleguide-Example project:

```
config
├── __init__.py
├── django
│   ├── __init__.py
│   ├── base.py
│   ├── local.py
│   ├── production.py
│   └── test.py
├── settings
│   ├── __init__.py
│   ├── celery.py
│   ├── cors.py
│   ├── sentry.py
│   └── sessions.py
├── urls.py
├── env.py
└── wsgi.py
├── asgi.py
```
In config/django, we put everything that's Django related:
* base.py contains most of the settings & imports everything else from config/settings
* production.py imports from base.py and then overwrites some specific settings for production.
* test.py imports from base.py and then overwrites some specific settings for running tests.
  * This should be used as the settings module in pytest.ini.
* local.py imports from base.py and can overwrite some specific settings for local development.
  * If you want to use that, point to local in manage.py. Otherwise stick with base.py

In config/settings, we put everything else:
* Celery configuration.
* 3rd party configurations.
* etc.

This gives you a nice separation of modules.

Additionally, we usually have config/env.py with the following code:

```python
import environ

env = environ.Env()
```

And then, whenever we need to read something from the environment, we import like that:

```python
from config.env import env
```

Usually, at the end of the base.py module, we import everything from config/settings:

```python
from config.settings.cors import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.sentry import *  # noqa
```

## Prefixing environment variables with DJANGO_

In a lot of examples, you'll see that environment variables are usually prefixed with DJANGO_. This is very helpful when there are other applications alongside your Django app that run on the same environment. In that case, prefixing the environment variables with DJANGO_ helps you to differ which are the environment variables specific to your Django app.

In HackSoft we do not ususally have several apps running on the same environment. So, we tend to prefix with DJANGO_ only the Django specific environments & anything else.

For example, we would have DJANGO_SETTINGS_MODULE, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS, DJANGO_CORS_ORIGIN_WHITELIST prefixed. We would have AWS_SECRET_KEY, CELERY_BROKER_URL, EMAILS_ENABLED not prefixed.

This is mostly up to personal preference. Just make sure you are consistent with that.

## Integrations

Since everything should be imported in base.py, but sometimes we don't want to configure a certain integration for local development, we derived the following approach:

* Integration-specific settings are placed in config/settings/some_integration.py
* There's always a boolean setting called USE_SOME_INTEGRATION, which reads from the environment & defaults to False.
* If the value is True, then proceed reading other settings & failing if things are not present in the environment.

For example, lets take a look at config/settings/sentry.py:
```python
from config.env import env

SENTRY_DSN = env('SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    # ... we proceed with sentry settings here ...
    # View the full file here - https://github.com/HackSoftware/Styleguide-Example/blob/master/config/settings/sentry.py
```

## Reading from .env

Having a local .env is a nice way of providing values for your settings.

And the good thing is, django-environ provides you with a way to do that:
```python
# That's in the beginning of base.py

import os

from config.env import env, environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env.read_env(os.path.join(BASE_DIR, ".env"))
```
Now you can have a .env (but it's not required) file in your project root & place values for your settings there.

There are 2 things worth mentioning here:

* Don't put .env in your source control, since this will leak credentials.
* Rather put an .env.example with empty values for everything, so new developers can figure out what's being used.