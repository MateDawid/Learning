# ModelViewSets

Source: https://testdriven.io/blog/drf-views-part-3/

## ModelViewSet

ModelViewSet provides default create, retrieve, update, partial_update, destroy and list actions since it uses GenericViewSet and all of the available mixins.

ModelViewSet is the easiest of all the views to use. You only need three lines:
```python
class ItemModelViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
```
## ReadOnlyModelViewSet

ReadOnlyModelViewSet is a ViewSet that provides only list and retrieve actions by combining GenericViewSet with the RetrieveModelMixin and ListModelMixin mixins.

Like ModelViewSet, ReadOnlyModelViewSet only needs the queryset and serializer_class attributes to work:
```python
from rest_framework.viewsets import ReadOnlyModelViewSet

class ItemReadOnlyViewSet(ReadOnlyModelViewSet):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
```