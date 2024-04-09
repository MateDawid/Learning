# Built-in permission classes

Source: https://testdriven.io/blog/built-in-permission-classes-drf/

![003_built_in_permissions.png](003_built_in_permissions.png)

All of those classes, except the last one, DjangoObjectPermissions, override just the has_permission method and inherits the has_object_permission from the BasePermission class. has_object_permission in the BasePermission class always returns True, so it has no impact on object-level access restriction.

## AllowAny

The most open permission of all is AllowAny. The has_permission and has_object_permission methods on AllowAny always return True without checking anything. Using it isn't necessary (by not setting the permission class, you implicitly set this one), but you still should since it makes the intent explicit and helps to maintain consistency throughout the app.
```python
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny] # built-in permission class used

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
```
## IsAuthenticated

IsAuthenticated checks if the request has a user and if that user is authenticated. Setting permission_classes to IsAuthenticated means that only authenticated users will be able to access the API endpoint with any of the request methods.

## IsAuthenticatedOrReadOnly

When permissions are set to IsAuthenticatedOrReadOnly, the request must either have an authenticated user or use one of the safe/read-only HTTP request methods (GET, HEAD, OPTIONS). This means that every user will be able to see all the objects, but only logged-in users will be able to add, change, or delete objects.

## IsAdminUser

