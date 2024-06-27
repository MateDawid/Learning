# Model testing

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#testing

Models need to be tested only if there's something additional to them - like validation, properties or methods.

Here's an example:

```python
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from project.some_app.models import Course


class CourseTests(TestCase):
    def test_course_end_date_cannot_be_before_start_date(self):
        start_date = timezone.now()
        end_date = timezone.now() - timedelta(days=1)

        course = Course(start_date=start_date, end_date=end_date)

        with self.assertRaises(ValidationError):
            course.full_clean()
```

A few things to note here:

* We assert that a validation error is going to be raised if we call full_clean.
* We are not hitting the database at all, since there's no need for that. This can speed up certain tests.