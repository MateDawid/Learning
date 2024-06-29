# Search Model Objects

Source: https://testdriven.io/blog/customize-django-admin/#search-model-objects

Django admin provides basic search functionality. It can be enabled by specifying which model fields should be searchable via the search_fields attribute. Keep in mind that Django doesn't support fuzzy queries by default.

```python
# tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    # ...
    search_fields = ["name", "venue__name", "venue__address"]
```

