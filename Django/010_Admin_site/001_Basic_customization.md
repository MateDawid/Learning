# Basic Admin Site Customization

Source: https://testdriven.io/blog/customize-django-admin/#basic-admin-site-customization

## Site header
```python
# core/urls.py

admin.site.site_title = "TicketsPlus site admin (DEV)"
admin.site.site_header = "TicketsPlus administration"
admin.site.index_title = "Site administration"
```

## URL

Another thing you should do is change the default /admin URL. This'll make it more difficult for malicious actors to find your admin panel.

Change your core/urls.py like so:
```python
# core/urls.py

urlpatterns = [
    path("secretadmin/", admin.site.urls),
]
```
Your admin site should now be accessible at http://localhost:8000/secretadmin.