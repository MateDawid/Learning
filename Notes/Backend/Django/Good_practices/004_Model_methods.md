# Model methods

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#methods

Model methods are also very powerful tool, that can build on top of properties.

Lets see an example with the is_within(self, x) method:

```python
from django.core.exceptions import ValidationError
from django.utils import timezone


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

    def is_within(self, x: date) -> bool:
        return self.start_date <= x <= self.end_date
```

is_within cannot be a property, because it requires an argument. So it's a method instead.

Another great way for using methods in models is using them for attribute setting, when setting one attribute must always be followed by setting another attribute with a derived value.

An example:

```python
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone


class Token(BaseModel):
    secret = models.CharField(max_length=255, unique=True)
    expiry = models.DateTimeField(blank=True, null=True)

    def set_new_secret(self):
        now = timezone.now()

        self.secret = get_random_string(255)
        self.expiry = now + settings.TOKEN_EXPIRY_TIMEDELTA

        return self
```

Now, we can safely call set_new_secret, that'll produce correct values for both secret and expiry.

We have few general rules of thumb, for when to add methods to the model:

* If we need a simple derived value, that requires arguments, based on non-relational model fields, add a method for that.
* If the calculation of the derived value is simple enough.
* If setting one attribute always requires setting values to other attributes, use a method for that.

Models should be something else (service, selector, utility) in the following cases:

* If we need to span multiple relations or fetch additional data.
* If the calculation is more complex.

Keep in mind that those rules are vague, because context is quite often important. Use your best judgement!