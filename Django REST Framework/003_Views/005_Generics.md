# Generyczne klasowe widoki
Widoki można uprościć jeszcze bardziej poprzez pominięcie użycia mixinów i wykorzystanie predefiniowanych generycznych widoków. W takiej sytuacji widoki zdefiniowane w punkcie 7.3.3. prezentują się następująco:
```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```