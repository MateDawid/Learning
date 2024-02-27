# extra_kwargs
Aby nadpisać niektóre właściwości dla poszczególnych pól można utworzyć zmienną extra_kwargs w klasie Meta serializera:
```python
class UserSerializer(serializers.ModelSerializer):
  class Meta:
      ...
      extra_kwargs = {'password': {
          'write_only': True,  # password will be able to save in POST request, but won't be returned in response
          'min_length': 5
      }}
```