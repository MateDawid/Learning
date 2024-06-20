# Indexes

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0

Indexes are essential for improving the performance of database operations, particularly for large datasets.

Example:
```python
class User(models.Model):
    username = models.CharField(max_length=100, db_index=True)
    email = models.CharField(max_length=100)

    class Meta:
            indexes = [
                models.Index(fields=['username'], name='username_idx'),
                models.Index(fields=['email'], name='email_idx')
            ]
```
