# ModelAdmin Class

Source: https://testdriven.io/blog/customize-django-admin/#link-related-model-objects

## Link Related Model Objects

Django admin site URL structure:

| Page	   | URL                               | 	Description                                   |
|---------|-----------------------------------|------------------------------------------------|
| List    | 	admin:\<app>_\<model>_changelist | 	Displays the list of objects                  |
| Add     | 	admin:\<app>_\<model>_add        | 	Object add form                               |
| Change  | 	admin:\<app>_\<model>_change     | 	Object change form (requires objectId)        |
| Delete  | 	admin:\<app>_\<model>_delete     | 	Object delete form (requires objectId)        |
| History | 	admin:\<app>_\<model>_history    | 	Displays object's history (requires objectId) |

Add the display_venue method to ConcertAdmin like so:
```python
# tickets/admin.py

class ConcertAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = [
        "name", "venue", "starts_at", "tickets_left",
        "display_sold_out",  "display_price", "display_venue",
    ]
    list_select_related = ["venue"]

    # ...

    def display_venue(self, obj):
        link = reverse("admin:tickets_venue_change", args=[obj.venue.id])
        return format_html('<a href="{}">{}</a>', link, obj.venue)

    display_venue.short_description = "Venue"
```