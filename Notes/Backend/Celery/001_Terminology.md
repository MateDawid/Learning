# Terminology

> Source: https://testdriven.io/courses/django-celery/intro

Celery (along with similar tools like RQ and Huey) uses the **producer/consumer model**.

**Message broker** is an intermediary program used as the transport for producing or consuming tasks.

**Result backend** is used to store the result of a Celery task.

The **Celery client** is the producer which adds a new task to the queue via the **message broker**. **Celery workers** then consume new tasks from the queue, again, via the **message broker**. Once processed, results are then stored in the **result backend**.

In terms of tools, RabbitMQ is arguably the better choice for a message broker since it supports AMQP (Advanced Message Queuing Protocol) while Redis is fine as your result backend.