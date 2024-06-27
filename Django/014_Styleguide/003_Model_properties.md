# Model properties

Sources:
* https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#properties

Model properties are great way to quickly access a derived value from a model's instance.

For example, lets look at the has_started and has_finished properties of our Course model:

```python
from django.utils import timezone
from django.core.exceptions import ValidationError


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()
```

Those properties are handy, because we can now refer to them in serializers or use them in templates.

We have few general rules of thumb, for when to add properties to the model:

* If we need a simple derived value, based on non-relational model fields, add a @property for that.
* If the calculation of the derived value is simple enough.

Properties should be something else (service, selector, utility) in the following cases:

* If we need to span multiple relations or fetch additional data.
* If the calculation is more complex.

Keep in mind that those rules are vague, because context is quite often important. Use your best judgement!