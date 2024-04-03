# SerializerMethodField

Source: https://testdriven.io/blog/drf-serializers/

SerializerMethodField is a read-only field, which gets its value by calling a method on the serializer class that it is attached to. It can be used to attach any kind of data to the serialized presentation of the object.

SerializerMethodField gets its data by calling get_<field_name>.

If we wanted to add a full_name attribute to our User serializer we could achieve that like this:

from django.contrib.auth.models import User
from rest_framework import serializers

```python
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
```
This piece of code creates a user serializer that also contains full_name which is the result of the get_full_name() function.