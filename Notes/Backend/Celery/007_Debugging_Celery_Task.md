# Debugging a Celery Task
> Source: https://testdriven.io/courses/django-celery/debugging-celery/

## Method 1: Eager Mode

By setting task_always_eager to True, tasks will be executed immediately (synchronously) instead of being sent to the queue (asynchronously), allowing you to debug the code within the task as you normally would (with breakpoints and print statements and what not) with any other code in your Django app.

It's worth noting that task_always_eager is False by default to help prevent inadvertently activating it in production.

So, you can add `CELERY_TASK_ALWAYS_EAGER=True` to the settings of Django project to activate it.

## Method 2: PyCharm

If you're not using Docker to run your application locally, then you can follow these steps to help with debugging a Celery task:

1. Make sure the message broker and result backend settings have been configured and that the relevant services are running.
2. Launch the debugger for your Django server.
3. Launch the debugger for your Celery worker (you'll need to configure this with a Python run config instead of a Django run config).

## Methods 3: rdb

rdb is a powerful tool that allows you to debug your Celery task directly in your terminal.

You must have Telnet installed in order for this to work.

You'll need to install telnet like so in compose/local/django/Dockerfile:

```Dockerfile
...

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git procps telnet \              # new
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

...
```
Next, add rdb to the Celery task in django_celery_example/celery.py:

```python
@app.task
def divide(x, y):
    from celery.contrib import rdb
    rdb.set_trace()

    # this is for test purposes
    import time
    time.sleep(10)
    return x / y
```

`rdb.set_trace()` works like a breakpoint.

Update:

```commandline
$ docker compose up -d --build
$ docker compose logs -f
```

Next, in a new terminal window navigate to the project directory, and then send a task to the Celery worker via the Django shell:

```commandline
$ docker compose exec web bash
(container)$ ./manage.py shell
```

Within the shell, run the Celery task:

```commandline
>>> from django_celery_example.celery import divide
>>> divide.delay(1, 2)
```

Back in the first window where the logs are running, you should see something similar to:

```commandline
django-celery-project-celery_worker-1  | [2024-01-02 03:08:33,224: INFO/MainProcess] Task django_celery_example.celery.divide[73e0876f-7a55-4917-8f71-3972e2e2bfa1] received
django-celery-project-celery_worker-1  | [2024-01-02 03:08:33,262: WARNING/ForkPoolWorker-16] Remote Debugger:6915: Ready to connect: telnet 127.0.0.1 6915
django-celery-project-celery_worker-1  |
django-celery-project-celery_worker-1  | Type `exit` in session to continue.
django-celery-project-celery_worker-1  |
django-celery-project-celery_worker-1  | Remote Debugger:6915: Waiting for client...
```

Take note of the port: `Remote Debugger:6915: Waiting for client..`

Open another terminal window, navigate to the project directory, and connect to the debugger via Telnet:

```commandline
$ docker compose exec celery_worker bash
(container)$ telnet 127.0.0.1 6915

Connected to 127.0.0.1.
Escape character is '^]'.
> /app/django_celery_example/celery.py(31)divide()
-> import time
(Pdb)
```

> Make sure to change `6915` to the port the debugger is running on your machine.

Now you can start debugging:

```commandline
(Pdb) args
x = 1
y = 2

(Pdb) help

Documented commands (type help <topic>):
========================================
EOF    cl         display   j         next     run     unalias    where
a      clear      down      jump      p        rv      undisplay
alias  commands   enable    l         pp       s       unt
args   condition  h         list      r        source  until
b      d          help      ll        restart  step    up
break  debug      ignore    longlist  return   tbreak  w
bt     disable    interact  n         retval   u       whatis

Miscellaneous help topics:
==========================
exec  pdb

Undocumented commands:
======================
c  cont  continue  exit  q  quit
```

You can exit the debug shell by typing c (which means continue). The Celery worker will finish executing the task:

```commandline
django-celery-project-celery_worker-1  | [2024-01-02 03:10:08,206: WARNING/ForkPoolWorker-16] Remote Debugger:6915: Session with 127.0.0.1:34462 ended.
django-celery-project-celery_worker-1  | [2024-01-02 03:10:18,211: INFO/ForkPoolWorker-16] Task django_celery_example.celery.divide[73e0876f-7a55-4917-8f71-3972e2e2bfa1] succeeded in 105.04715652900632s: 0.5
```

Make sure to comment our or remove rdb from the task once done:

```python
@app.task
def divide(x, y):
    # from celery.contrib import rdb
    # rdb.set_trace()

    # this is for test purposes
    import time
    time.sleep(10)
    return x / y
```