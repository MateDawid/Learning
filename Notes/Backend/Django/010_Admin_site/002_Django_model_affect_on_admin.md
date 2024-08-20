# Django Model and Admin

Source: https://testdriven.io/blog/customize-django-admin/#django-model-and-admin

Some Django model attributes directly affect the Django admin site. Most importantly:

* __str__() is used to define object's display name
* Meta class is used to set various metadata options (e.g., ordering and verbose_name)

Here's an example of how these attributes are used in practice:
```python
# tickets/models.py

class ConcertCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "concert category"
        verbose_name_plural = "concert categories"
        ordering = ["-name"]

    def __str__(self):
        return f"{self.name}"
```
We provided the plural form since the plural of "concert category" isn't "concert categorys".
By providing the ordering attribute the categories are now ordered by name.