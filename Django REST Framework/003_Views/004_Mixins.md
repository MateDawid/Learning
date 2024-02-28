# Mixins
W celu uproszczenia kodu możliwe jest wykorzystanie wbudowanych mixinów zapewniających typowe dla API funkcjonalności, którymi obudować można podstawowy widok bazujący na klasach. 

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```
Oba widoki bazują na GenericAPIView, który zapewnia podstawowe funkcjonalności widoku. 
SnippetList wykorzystuje mixiny zapewniające funkcjonalności listy obiektów (ListModelMixin) oraz tworzenia nowego obiektu (CreateModelMixin).
Za to SnippetDetail rozszerzony jest o pobieranie (RetrieveModelMixin), aktualizowanie (UpdateModelMixin) oraz usuwanie obiektów (DestroyModelMixin).
