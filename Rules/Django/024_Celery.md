# Celery

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#celery

We use Celery for the following general cases:

* Communicating with 3rd party services (sending emails, notifications, etc.)
* Offloading heavier computational tasks outside the HTTP cycle.
* Periodic tasks (using Celery beat)

## Basics
We try to treat Celery as if it's just another interface to our core logic - meaning - don't put business logic there.

```python
from django.db import transaction
from django.core.mail import EmailMultiAlternatives

from styleguide_example.core.exceptions import ApplicationError
from styleguide_example.common.services import model_update
from styleguide_example.emails.models import Email


@transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email.status}")

    subject = email.subject
    from_email = "styleguide-example@hacksoft.io"
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={
            "status": Email.Status.SENT,
            "sent_at": timezone.now()
        }
    )
    return email
```
Email sending has business logic around it, but we still want to trigger this particular service from a task.

Our task looks like that:
```python
from celery import shared_task

from styleguide_example.emails.models import Email


@shared_task
def email_send(email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send
    email_send(email)
```
As you can see, we treat the task as an API:

1. Fetch the required data. 
2. Call the appropriate service.

Now, imagine we have a different service, that triggers the email sending.

It may look like that:
```python
from django.db import transaction

# ... more imports here ...

from styleguide_example.emails.tasks import email_send as email_send_task


@transaction.atomic
def user_complete_onboarding(user: User) -> User:
    # ... some code here

    email = email_get_onboarding_template(user=user)

    transaction.on_commit(lambda: email_send_task.delay(email.id))

    return user
```
2 important things to point out here:

* We are importing the task (which has the same name as the service), but we are giving it a _task suffix.
* And when the transaction commits, we'll call the task.

So, in general, the way we use Celery can be described as:

* Tasks call services.
* We import the service in the function body of the task.
* When we want to trigger a task, we import the task, at module level, giving the _task suffix.
* We execute tasks, as a side effect, whenever our transaction commits.

## Error handling

Sometimes, our service can fail and we might want to handle the error on the task level. For example - we might want to retry the task.

This error handling code needs to live in the task.

Lets expand the email_send task example from above, by adding error handling:
```python
from celery import shared_task
from celery.utils.log import get_task_logger

from styleguide_example.emails.models import Email


logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_failed

    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send

    try:
        email_send(email)
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
```
As you can see, we do a bunch of retries and if all of them fail, we handle this in the on_failure callback.

The callback follows the naming pattern of _{task_name}_failure and it calls the service layer, just like an ordinary task.

## Structure
Tasks are located in tasks.py modules in different apps.

We follow the same rules as with everything else (APIs, services, selectors): if the tasks for a given app grow too big, split them by domain.

Meaning, you can end up with tasks/domain_a.py and tasks/domain_b.py. All you need to do is import them in tasks/__init__.py for Celery to autodiscover them.

The general rule of thumb is - split your tasks in a way that'll make sense to you.

## Periodic tasks
Managing periodic tasks is quite important, especially when you have tens or hundreds of them.

We use Celery Beat + django_celery_beat.schedulers:DatabaseScheduler + django-celery-beat for our periodic tasks.

The extra thing that we do is to have a management command, called setup_periodic_tasks, which holds the definition of all periodic tasks within the system. This command is located in the tasks app, discussed above.

Here's how project.tasks.management.commands.setup_periodic_tasks.py looks like:
```python
from django.core.management.base import BaseCommand
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from project.app.tasks import some_periodic_task


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {some_periodic_task.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Deleting all periodic tasks and schedules...\n')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                'task': some_periodic_task
                'name': 'Do some peridoic stuff',
                # https://crontab.guru/#15_*_*_*_*
                'cron': {
                    'minute': '15',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **periodic_task['cron']
            )

            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled']
            )
```
Few key things:

* We use this task as part of a deploy procedure.
* We always put a link to crontab.guru to explain the cron. Otherwise it's unreadable.
* Everything is in one place.
* ⚠️ We use, almost exclusively, a cron schedule. If you plan on using the other schedule objects, provided by Celery, please read thru their documentation & the important notes - https://django-celery-beat.readthedocs.io/en/latest/#example-creating-interval-based-periodic-task - about pointing to the same schedule object. ⚠️