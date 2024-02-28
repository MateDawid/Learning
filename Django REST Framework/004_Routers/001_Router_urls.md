# Router urls

Router służy do mapowania ViewSetów na adresy url. Chcąc wykorzystać adresy url zarejestrowane w routerze trzeba rozszerzyć urlpatterns w globalnym pliku urls.py o parametr url routera.

```python
# project/urls.py

from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()), # NEW URL
]
```