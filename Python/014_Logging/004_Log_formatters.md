# Log Formatters

Source: https://www.samyakinfo.tech/blog/logging-in-python#log-formatters

A log formatter is an object responsible for specifying the layout of log records. It determines how the information within a log message should be presented. Python's logging module provides a Formatter class that allows developers to create custom formatting rules.

## Base Formatter

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a StreamHandler and set its log level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter with a custom format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Create a logger and add the console handler
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

In this example, the Formatter class is used to create a formatter with a specific format string. The format string contains placeholders enclosed in %() that represent various attributes such as asctime, name, levelname, and message.

## Custom Formatter

```python
import logging

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_message = f"{record.levelname} - {record.name} - {record.message}"
        if record.exc_info:
            log_message += '\n' + self.formatException(record.exc_info)
        return log_message

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a StreamHandler and set its log level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create an instance of the custom formatter
custom_formatter = CustomFormatter()

# Set the formatter for the console handler
console_handler.setFormatter(custom_formatter)

# Create a logger and add the console handler
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

# Log messages
logger.debug("This is a debug message")
logger.error("An error occurred", exc_info=True)

```