# Proxy models

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0

Proxy models are used to change the behavior of a model, like the default ordering or the default manager, without creating a new database table.

Example:
```python
class OrderedProfile(Profile):
    class Meta:
        proxy = True
        ordering = ['name']

# Usage:
ordered_profiles = OrderedProfile.objects.all()

```

This proxy model will show all profiles ordered by name.