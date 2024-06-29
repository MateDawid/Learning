# Multitable inheritance

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0

This type of inheritance is used when each model in the hierarchy is considered a full entity on its own, potentially linked to a physical database table.

Example:
```python
class Place(models.Model):
    name = models.CharField(max_length=50)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)
```



Here, Restaurant is a type of Place and has its own table with a link to Place.