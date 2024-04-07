# GenericViewSet

Source: https://testdriven.io/blog/drf-views-part-3/

While ViewSet extends APIView, GenericViewSet extends GenericAPIView.
```python
# https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/viewsets.py#L210
class ViewSet(ViewSetMixin, views.APIView):
   pass


# https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/viewsets.py#L217
class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
   pass
```

## Using GenericViewSet with Mixins
```python
from rest_framework import mixins, viewsets

class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
```

## Using GenericViewSet with Explicit Action Implementations

```python
from rest_framework import status
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

class ItemViewSet(GenericViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [DjangoObjectPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

