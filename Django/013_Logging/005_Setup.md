# Logging setup

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

## settings.py

```python
# settings.py

LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'warning.log',
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
       # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['file'], # notice how file variable is called in handler which has been defined above
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

When `propagate` is set as True, a child will propagate all their logging calls to the parent. This means that we can define a handler at the root (parent) of the logger tree and all logging calls in the subtree (child) go to the handler defined in the parent.

## Using logger

```python

from django.http import HttpResponse
import datetime
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def hello_reader(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Hello FreeCodeCamp.org Reader :)</h1>")

```
