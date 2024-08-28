# Handlers

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

Handlers basically determine what happens to each message in a logger. It has log levels the same as Loggers. But, we can essentially define what way we want to handle each log level.

For example: ERROR log level messages can be sent in real-time to the developer, while INFO log levels can just be stored in a system file.

It essentially tells the system what to do with the message like writing it on the screen, a file, or to a network socket