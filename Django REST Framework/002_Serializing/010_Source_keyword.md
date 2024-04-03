# Source keyword

Source: https://testdriven.io/blog/drf-serializers/

The DRF serializer comes with the source keyword, which is extremely powerful and can be used in multiple case scenarios. We can use it to:

* Rename serializer output fields
* Attach serializer function response to data
* Fetch data from one-to-one models

Let's say you're building a social network and every user has their own UserProfile, which has a one-to-one relationship with the User model:
```python
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} profile'
```
We're using a ModelSerializer for serializing our users:
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active']
```

## Rename serializer output fields

To rename a serializer output field we need to add a new field to our serializer and pass it to fields property.
```python
class UserSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source='is_active')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'active']
Our active field is now going to be named active instead of is_active.
```
## Attach serializer function response to data
We can use source to add a field which equals to function's return.
```python
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'is_staff', 'active']
```
```get_full_name()``` is a method from the Django user model that concatenates user.first_name and user.last_name.

## Append data from one-to-one models
Now let's suppose we also wanted to include our user's bio and birth_date in UserSerializer. We can do that by adding extra fields to our serializer with the source keyword.

Let's modify our serializer class:
```python
class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='userprofile.bio')
    birth_date = serializers.DateField(source='userprofile.birth_date')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_staff',
            'is_active', 'bio', 'birth_date'
        ]  # note we also added the new fields here
```
We can access userprofile.<field_name>, because it is a one-to-one relationship with our user.