# Different Read and Write Serializers

Source: https://testdriven.io/blog/drf-serializers/

If your serializers contain a lot of nested data, which is not required for write operations, you can boost your API performance by creating separate read and write serializers.

You do that by overriding the ```get_serializer_class()``` method in your ViewSet like so:
```python
from rest_framework import viewsets

from .models import MyModel
from .serializers import MyModelWriteSerializer, MyModelReadSerializer


class MyViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return MyModelWriteSerializer

        return MyModelReadSerializer
```
This code checks what REST operation has been used and returns MyModelWriteSerializer for write operations and MyModelReadSerializer for read operations.