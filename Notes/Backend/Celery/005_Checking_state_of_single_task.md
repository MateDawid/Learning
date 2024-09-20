# Checking state of single task

> Source: https://testdriven.io/courses/django-celery/getting-started/#H-8-monitoring-celery-with-flower

![004_flower.png](_images%2F004_flower.png)

Take note of the UUID column. This is the id of AsyncResult. Copy the UUID for the failed task and open the terminal window where the Django shell is running to view the details:

```commandline
>>> from celery.result import AsyncResult
>>> task = AsyncResult('6104b10e-cffe-4703-997d-bc085068d517')  # replace with your UUID
>>>
>>> task.state
'FAILURE'
>>>
>>> task.result
ZeroDivisionError('division by zero')
```