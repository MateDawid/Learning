# Routers

Source: https://testdriven.io/blog/drf-views-part-3/

Instead of using Django's urlpatterns, ViewSets come with a router class that automatically generates the URL configurations.

DRF comes with two routers out-of-the-box:

* SimpleRouter
* DefaultRouter

The main difference between them is that DefaultRouter includes a default API root view.

Routers can also be combined with urlpatterns:
```python
# urls.py

from django.urls import path, include
from rest_framework import routers

from .views import ChangeUserInfo, ItemsViewSet

router = routers.DefaultRouter()
router.register(r'custom-viewset', ItemsViewSet)

urlpatterns = [
    path('change-user-info', ChangeUserInfo.as_view()),
    path('', include(router.urls)),
]
```

Here's how the router maps methods to actions:
```python
# https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/routers.py#L83

routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
```