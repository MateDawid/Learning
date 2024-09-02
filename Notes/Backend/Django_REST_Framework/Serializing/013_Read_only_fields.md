# Read-only Fields

Source: https://testdriven.io/blog/drf-serializers/

Serializer fields come with the read_only option. By setting it to True, DRF includes the field in the API output, but ignores it during create and update operations:
```python
from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = IntegerField(label='ID', read_only=True)
    username = CharField(max_length=32, required=True)
```
Setting fields like id, create_date, etc. to read only will give you a performance boost during write operations.

If you want to set multiple fields to read_only, you can specify them using read_only_fields in Meta like so:
```python
from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = IntegerField(label='ID')
    username = CharField(max_length=32, required=True)

    class Meta:
        read_only_fields = ['id', 'username']
```