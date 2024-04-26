# Loggers

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

Loggers are basically the entry point of the logging system. This is what you'll actually work with as a developers.

When a message is received by the logger, the log level is compared to the log level of the logger. If it is the same or exceeds the log level of the logger, the message is sent to the handler for further processing. The log levels are:

* DEBUG: Low-level system information
* INFO: General system information
* WARNING: Minor problems related information
* ERROR: Major problems related information
* CRITICAL: Critical problems related information
