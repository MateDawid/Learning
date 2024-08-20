# List Display

Source: https://testdriven.io/blog/customize-django-admin/#customize-admin-site-with-modeladmin-class

## Control List Display

The list_display attribute allows you to control which model fields are displayed on the model list page. Another great thing about it is that it can display related model fields using the __ operator.
```python
# tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", "venue", "starts_at", "price", "tickets_left"]
    readonly_fields = ["tickets_left"]
```

By adding the venue to the list_display, we introduced the N + 1 problem. Since Django needs to fetch the venue name for each concert separately, many more queries get executed.

To avoid the N + 1 problem, we can use the list_select_related attribute, which works similarly to the select_related method:

```python
# tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", "venue", "starts_at", "price", "tickets_left"]
    list_select_related = ["venue"]
    readonly_fields = ["tickets_left"]
```

## List Display Custom Fields

The list_display setting can also be used to add custom fields. To add a custom field, you must define a new method within the ModelAdmin class.

Add a "Sold Out" field, which is True if no tickets are available:
```python
# tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", "venue", "starts_at", "tickets_left", "display_sold_out"]
    list_select_related = ["venue"]

    def display_sold_out(self, obj):
        return obj.tickets_left == 0

    display_sold_out.short_description = "Sold out"
    display_sold_out.boolean = True
```
We used short_description to set the column name and boolean to tell Django that this column has a boolean value. This way, Django displays the tick/cross icon instead of True and False. We also had to add our display_sold_out method to list_display.
```python
# tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = [
        "name", "venue", "starts_at", "tickets_left", "display_sold_out",  "display_price"
    ]
    # ...

    def display_price(self, obj):
        return f"${obj.price}"

    display_price.short_description = "Price"
    display_price.admin_order_field = "price"
```
We used admin_order_field to tell Django by what field this column is orderable.