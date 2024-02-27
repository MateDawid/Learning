# ViewSet
## Co to jest?
W celu jeszcze większego uproszczenia kodu możliwe jest zastosowanie ViewSetu. Automatyzuje on mapowanie endpoitów na poszczególne adresy URL. Nie ma również potrzeby tworzyć osobnych widoków listy i pojedynczego elementu - oba warianty można obsłużyć viewsetem.
```python 
# views.py

from .serializers import ItemSerializer
from .models import Item 
from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets 
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

class ItemViewSet(  
		ListModelMixin,  
		RetrieveModelMixin,  
		viewsets.GenericViewSet  
	):  
	"""  
	A simple ViewSet for listing or retrieving items. 
	"""  
	permission_classes = (IsAuthenticated,)  
	queryset = Item.objects.all()  
	serializer_class = ItemSerializer
```
## Rodzaje ViewSetów

### Bazowy ViewSet
  ```python
from rest_framework import views 
from rest_framework import mixins

class ViewSet(mixins.ViewSetMixin, views.APIView):
    """
    The base ViewSet class does not provide any actions by default.
    """
    pass
  ```
### GenericViewSet:
  ```python
from rest_framework import mixins
from rest_framework import generics

class GenericViewSet(mixins.ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass
  ```
### ReadOnlyViewSet
Pozwala jedynie na pobieranie danych, nie daje możliwości zmiany lub usunięcia.
  ```python
from rest_framework import mixins
from rest_framework import generics


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    generics.GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass
  ```
### ModelViewSet
Pozwala na wszystkie możliwe operacje z zakresu CRUD.
```python
from rest_framework import mixins
from rest_framework import generics

class ModelViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
```

## Własna akcja w ViewSecie
Aby utworzyć własny endpoint wewnątrz viewsetu, trzeba użyć dekoratora @action.
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    ...
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```