# Other options

Source: https://realpython.com/python-logging

## Date format

```python
>>> import logging
>>> logging.basicConfig(
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> logging.error("Something went wrong!")
2024-07-22 09:26 - ERROR - Something went wrong!
```

## Logging to file

```python
>>> import logging
>>> logging.basicConfig(
...     filename="app.log",
...     encoding="utf-8",
...     filemode="a",
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> logging.warning("Save me!")
```

## Displaying Variable Data

```python
>>> import logging
>>> logging.basicConfig(
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
...     level=logging.DEBUG,
... )

>>> name = "Samara"
>>> logging.debug(f"{name=}")
2024-07-22 14:49 - DEBUG - name='Samara'
```

F-strings are eagerly evaluated. That means that they are interpolated even if the log message is never handled. If you’re interpolating a lot of lower level log messages, you should consider using the modulo operator (%) for interpolation instead of f-strings. This style is supported by logging natively, such that you can write code like the following:

```python
>>> import logging
>>> logging.basicConfig(
...     format="%(asctime)s - %(levelname)s - %(message)s",
...     style="%",
...     datefmt="%Y-%m-%d %H:%M",
...     level=logging.DEBUG,
... )

>>> name = "Samara"
>>> logging.debug("name=%s", name)
2024-07-22 14:51 - DEBUG - name=Samara
```

## Capturing Stack Traces

```python
>>> import logging
>>> logging.basicConfig(
...     filename="app.log",
...     encoding="utf-8",
...     filemode="a",
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> donuts = 5
>>> guests = 0
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.error("DonutCalculationError", exc_info=True)
...
```

```text
2024-07-22 15:04 - ERROR - DonutCalculationError
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

```python
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.exception("DonutCalculationError")
...
```
Calling logging.exception() is like calling logging.error(exc_info=True). Since the logging.exception() function always dumps exception information, you should only call logging.exception() from an exception handler.

## Filtering Logs

There are three approaches to creating filters for logging. You can create a:

* Subclass of logging.Filter() and overwrite the .filter() method
* Class that contains a .filter() method
* Callable that resembles a .filter() method

```python
>>> import logging
>>> def show_only_debug(record):
...     return record.levelname == "DEBUG"
...

>>> logger = logging.getLogger(__name__)
>>> logger.setLevel("DEBUG")
>>> formatter = logging.Formatter("{levelname} - {message}", style="{")

>>> console_handler = logging.StreamHandler()
>>> console_handler.setLevel("DEBUG")
>>> console_handler.setFormatter(formatter)
>>> console_handler.addFilter(show_only_debug)
>>> logger.addHandler(console_handler)

>>> file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
>>> file_handler.setLevel("WARNING")
>>> file_handler.setFormatter(formatter)
>>> logger.addHandler(file_handler)

>>> logger.debug("Just checking in!")
DEBUG - Just checking in!

>>> logger.warning("Stay curious!")
>>> logger.error("Stay put!")
```