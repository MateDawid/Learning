# Serializer context

Source: https://testdriven.io/blog/drf-serializers/

There are some cases when you need to pass additional data to your serializers. You can do that by using the serializer context property. You can then use this data inside the serializer such as to_representation or when validating data.

You pass the data as a dictionary via the context keyword:
```python
from rest_framework import serializers
from examples.models import Resource

resource = Resource.objects.get(id=1)
serializer = ResourceSerializer(resource, context={'key': 'value'})
```
Then you can fetch it inside the serializer class from the self.context dictionary like so:
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['key'] = self.context['key']

        return representation
```
Our serializer output will now contain key with value.