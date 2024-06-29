# Filter Model Objects

Source: https://testdriven.io/blog/customize-django-admin/#filter-model-objects

```python
# tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    # ...
    list_filter = ["venue"]
```

To filter by a related object's fields, use the __ operator.

or more advanced filtering functionality, you can also define custom filters. To define a custom filter, you must specify the options or so-called lookups and a queryset for each lookup.

```python
# tickets/admin.py

from django.contrib.admin import SimpleListFilter


class SoldOutFilter(SimpleListFilter):
    title = "Sold out"
    parameter_name = "sold_out"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Yes"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(tickets_left=0)
        else:
            return queryset.exclude(tickets_left=0)


class ConcertAdmin(admin.ModelAdmin):
    # ...
    list_filter = ["venue", SoldOutFilter]
```
