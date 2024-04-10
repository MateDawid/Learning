# Global permissions

Source: https://testdriven.io/blog/built-in-permission-classes-drf/#global-permissions

You can easily set global permission in your settings.py file, using built-in permission classes. For example:
```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```
DEFAULT_PERMISSION_CLASSES will only work for the views or objects that don't have permissions explicitly set.