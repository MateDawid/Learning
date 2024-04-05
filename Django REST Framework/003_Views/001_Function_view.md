# Function-based Views

Source: https://testdriven.io/blog/drf-views-part-1/

## Intro
If you're writing a view in the form of a function, you'll need to use the @api_view decorator.

@api_view is a decorator that converts a function-based view into an APIView subclass (thus providing the Response and Request classes). It takes a list of allowed methods for the view as an argument.

## Example
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['DELETE'])
def delete_all_items(request):
    Item.objects.all().delete()
    return Response(status=status.HTTP_200_OK)
```

## Policy Decorators

* @renderer_classes
* @parser_classes
* @authentication_classes
* @throttle_classes
* @permission_classes

Those decorators correspond to APIView subclasses. Because the @api_view decorator checks if any of the following decorators are used, they need to be added below the api_view decorator

```python
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # policy decorator
@renderer_classes([JSONRenderer])       # policy decorator
def items_not_done(request):
    user_count = Item.objects.filter(done=False).count()
    content = {'not_done': user_count}

    return Response(content)
```