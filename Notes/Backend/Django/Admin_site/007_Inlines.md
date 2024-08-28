# Handle Model Inlines

Source: https://testdriven.io/blog/customize-django-admin/#handle-model-inlines

The admin interface allows you to edit models on the same page as the parent model via inlines. Django provides two types of inlines StackedInline and TabularInline. The main difference between them is how they look.

```python
# tickets/admin.py

class ConcertInline(admin.TabularInline):
    model = Concert
    fields = ["name", "starts_at", "price", "tickets_left"]

    # optional: make the inline read-only
    readonly_fields = ["name", "starts_at", "price", "tickets_left"]
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = True


class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "capacity"]
    inlines = [ConcertInline]
```