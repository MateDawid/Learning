# Validation

Source: https://testdriven.io/blog/drf-serializers/

## Custom field validation
Custom field validation allows us to validate a specific field. We can use it by adding the validate_<field_name> method to our serializer like so:
```python
from rest_framework import serializers
from examples.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating has to be between 1 and 10.')
        return value
```
## Object-level validation
Sometimes you'll have to compare fields with one another in order to validate them. This is when you should use the object-level validation approach.

Example:
```python
from rest_framework import serializers
from examples.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('US gross cannot be greater than worldwide gross.')
        return data
```
The validate method will make sure us_gross is never bigger than worldwide_gross.

You should avoid accessing additional fields in the custom field validator via self.initial_data. This dictionary contains raw data, which means that your data types won't necessarily match the required data types. DRF will also append validation errors to the wrong field.

## Functional validators
If we use the same validator in multiple serializers, we can create a function validator instead of writing the same code over and over again. Let's write a validator that checks if the number is between 1 and 10:
```python
def is_rating(value):
    if value < 1:
        raise serializers.ValidationError('Value cannot be lower than 1.')
    elif value > 10:
        raise serializers.ValidationError('Value cannot be higher than 10')
```
We can now append it to our MovieSerializer like so:
```python
from rest_framework import serializers
from examples.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    rating = IntegerField(validators=[is_rating])
    ...
```