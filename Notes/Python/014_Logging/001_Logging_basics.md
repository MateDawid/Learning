# Logging basics

Sources: 
* https://www.samyakinfo.tech/blog/logging-in-python
* https://realpython.com/python-logging/

Logging is the process of recording information about the execution of a program. This information, known as log messages, includes details about the application's state, error messages, warnings, and other relevant data.

Logging is essential for several reasons:

`Debugging`: Logs help developers identify and fix issues by providing a trail of execution flow and variable values.

`Monitoring`: Logs enable monitoring of application behavior in real-time, helping detect performance bottlenecks and unexpected behavior.

`Auditing and compliance`: For applications handling sensitive information, logging can be essential for auditing user actions and ensuring compliance with regulations.

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```