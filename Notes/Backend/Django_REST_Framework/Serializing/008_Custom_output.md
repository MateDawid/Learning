# Custom output

Source: https://testdriven.io/blog/drf-serializers/

Two of the most useful functions inside the BaseSerializer class that we can override are ```to_representation()``` and ```to_internal_value()```. By overriding them, we can change the serialization and deserialization behavior, respectively, to append additional data, extract data, and handle relationships.

* to_representation() allows us to change the serialization output
* to_internal_value() allows us to change the deserialization output
```python
from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(to=User)

    def __str__(self):
        return f'{self.title}'
```
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
```
If we serialize a resource and access its data property, we'll get the following output:
```json
{
   "id": 1,
   "title": "C++ with examples",
   "content": "This is the resource's content.",
   "liked_by": [
      2,
      3
   ]
}
```
## to_representation()
Now, let's say we want to add a total likes count to the serialized data. The easiest way to achieve this is by implementing the to_representation method in our serializer class:
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()

        return representation
```
This piece of code fetches the current representation, appends likes to it, and returns it.

If we serialize another resource, we'll get the following result:
```json
{
   "id": 1,
   "title": "C++ with examples",
   "content": "This is the resource's content.",
   "liked_by": [
      2,
      3
   ],
   "likes": 2
}
```
## to_internal_value()
Suppose the services that use our API appends unnecessary data to the endpoint when creating resources:
```json
{
   "info": {
       "extra": "data",
       ...
   },
   "resource": {
      "id": 1,
      "title": "C++ with examples",
      "content": "This is the resource's content.",
      "liked_by": [
         2,
         3
      ],
      "likes": 2
   }
}
```
If we try to serialize this data, our serializer will fail because it will be unable to extract the resource.

We can override to_internal_value() to extract the resource data:
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_internal_value(self, data):
        resource_data = data['resource']

        return super().to_internal_value(resource_data)
```