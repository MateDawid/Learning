# Log handlers

Source: https://www.samyakinfo.tech/blog/logging-in-python#log-handlers

Log handlers in Python's logging module determine where log messages should go once they are created. Handlers are responsible for routing log messages to specific destinations, such as the console, files, email, or external services. In this part, we'll explore the concept of log handlers and how to use them effectively.

## StreamHandler
Directs log messages to the console(stream):

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a StreamHandler and set its log level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handler
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
In this example, we create a StreamHandler, set its log level to DEBUG, create a formatter to customize the log message format, and attach the formatter to the handler. Finally, we add the handler to the logger.

## FileHandler
Directs log messages to a file:
```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a FileHandler and set its log level to DEBUG
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Create a logger and add the file handler
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```
In this example, we create a FileHandler, set its log level, create a formatter, and attach it to the handler. The log messages will be written to a file named app.log.

## RotatingFileHandler
Similar to FileHandler, but it rotates log files based on size and keeps a specified number of backup files.

```python
rotating_file_handler = logging.RotatingFileHandler("logfile.log", maxBytes=1024, backupCount=3)
logging.getLogger().addHandler(rotating_file_handler)
```
## SMTPHandler

Sends log messages via email.
```python
smtp_handler = logging.handlers.SMTPHandler(mailhost=("smtp.example.com", 587),
                                            fromaddr="sender@example.com",
                                            toaddrs=["recipient@example.com"],
                                            subject="Error in your application")
logging.getLogger().addHandler(smtp_handler)
```