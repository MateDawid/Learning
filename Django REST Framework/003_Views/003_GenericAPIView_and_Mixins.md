# GenericAPIView and mixins

Source: https://testdriven.io/blog/drf-views-part-1/

## GenericAPIView

GenericAPIView is a base class for all other generic views. It provides methods like get_object/get_queryset and get_serializer. Although it's designed to be combined with mixins (as it's used within generic views), it's possible to use it on its own:
```python
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class RetrieveDeleteItem(GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 ```       
When extending GenericAPIView, queryset and serializer_class must be set. Alternatively, you can overwrite get_queryset()/get_serializer_class().

## Mixins

|Mixin |	Usage|
|-|-|
|CreateModelMixin |	Create a model instance|
|ListModelMixin |	List a queryset|
|RetrieveModelMixin |	Retrieve a model instance|
|UpdateModelMixin |	Update a model instance|
|DestroyModelMixin |	Delete a model instance|

Here's an example of what a mixin looks like:
```python
class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

Example usage of mixins:
```python
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class CreateListItems(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 ```       
In CreateListItems we used the serializer_class and queryset provided by GenericAPIView.

We defined get and post methods on our own, which used list and create actions provided by the mixins:

* CreateModelMixin provides a create action
* ListModelMixin provides a list action

**You're responsible for binding actions to the methods.**

Theoretically, that means that you could bind POST methods with list actions and GET methods with create actions, and things would "kind" of work.

**It's a good idea to have a single view for handling all instances -- listing all instances and adding a new instance -- and another view for handling a single instance -- retrieving, updating, and deleting single instances.**