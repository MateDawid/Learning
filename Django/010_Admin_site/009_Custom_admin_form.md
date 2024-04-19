# Override Django Admin Forms

Source: https://testdriven.io/blog/customize-django-admin/#override-django-admin-forms

By default, Django automatically generates a ModelForm for your model. That form is then used on the add and change page. If you want to customize the form or implement unique data validation, you'll have to override the form.

Go ahead and create a forms.py file in the tickets app:
```python
# tickets/forms.py

from django import forms
from django.forms import ModelForm, RadioSelect

from tickets.models import Ticket


class TicketAdminForm(ModelForm):
    first_name = forms.CharField(label="First name", max_length=32)
    last_name = forms.CharField(label="Last name", max_length=32)

    class Meta:
        model = Ticket
        fields = [
            "concert",
            "first_name",
            "last_name",
            "payment_method",
            "is_active"
        ]
        widgets = {
            "payment_method": RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = {}

        if instance:
            customer_full_name_split = instance.customer_full_name.split(" ", maxsplit=1)
            initial = {
                "first_name": customer_full_name_split[0],
                "last_name": customer_full_name_split[1],
            }

        super().__init__(*args, **kwargs, initial=initial)

    def save(self, commit=True):
        self.instance.customer_full_name = self.cleaned_data["first_name"] + " " \
                                            + self.cleaned_data["last_name"]
        return super().save(commit)
```
Here:

We added the first_name and last_name form fields.
We used the Meta class to specify what model this form relates to and what fields to include.
On form __init__(), we populated the form using model instance data.
On save(), we merged first_name and last_name and saved it as customer_full_name.
Next, set TicketAdmin's form like so:
```python
# tickets/admin.py

class TicketAdmin(admin.ModelAdmin):
    # ...
    form = TicketAdminForm
```