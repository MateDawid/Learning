# DRF Renderers

Source: https://testdriven.io/courses/django-rest-framework/manual-testing/#H-6-default-renderer

To render data in JSON, you need to change DEFAULT_RENDERER_CLASSES inside your settings.py file:

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}
```

If you, for some reason, want only one view to be rendered as JSON, you can set it in renderer_classes inside the view.

```python
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from shopping_list.api.serializers import ShoppingItemSerializer
from shopping_list.models import ShoppingItem


class ShoppingItemViewSet(ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    renderer_classes = [JSONRenderer]
```