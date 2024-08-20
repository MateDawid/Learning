# Custom Admin Actions

Source: https://testdriven.io/blog/customize-django-admin/#custom-admin-actions

Django admin actions allow you to perform an "action" on an object or a group of objects. An action can be used to modify an object's attributes, delete the object, copy it, and so forth. Actions are primarily utilized for frequently performed "actions" or bulk changes.

```python
# tickets/admin.py

@admin.action(description="Activate selected tickets")
def activate_tickets(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate selected tickets")
def deactivate_tickets(modeladmin, request, queryset):
    queryset.update(is_active=False)


class TicketAdmin(admin.ModelAdmin):
    # ...
    actions = [activate_tickets, deactivate_tickets]
```