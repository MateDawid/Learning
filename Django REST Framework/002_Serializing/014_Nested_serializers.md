# Nested serializers

Source: https://testdriven.io/blog/drf-serializers/

## Explicit definition

The explicit definition works by passing an external Serializer as a field to our main serializer.

Let's take a look at an example. We have a Comment which is defined like so:
```python
from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
```
Say you then have the following serializer:
```python
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
```
If we serialize a Comment, you'll get the following output:
```json
{
    "id": 1,
    "datetime": "2021-03-19T21:51:44.775609Z",
    "content": "This is an interesting message.",
    "author": 1
}
```
If we also wanted to serialize the user (instead of only showing their ID), we can add an author serializer field to our Comment:
```python
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
```
Serialize again and you'll get this:
```json
{
    "id": 1,
    "author": {
        "id": 1,
        "username": "admin"
    },
    "datetime": "2021-03-19T21:51:44.775609Z",
    "content": "This is an interesting message."
}
```
## Using the depth field

When it comes to nested serialization, the depth field is one of the most powerful featuress. Let's suppose we have three models -- ModelA, ModelB, and ModelC. ModelA depends on ModelB while ModelB depends on ModelC. They are defined like so:
```python
from django.db import models


class ModelC(models.Model):
    content = models.CharField(max_length=128)


class ModelB(models.Model):
    model_c = models.ForeignKey(to=ModelC, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)


class ModelA(models.Model):
    model_b = models.ForeignKey(to=ModelB, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
```
Our ModelA serializer, which is the top-level object, looks like this:
```python
from rest_framework import serializers


class ModelASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelA
        fields = '__all__'
```
If we serialize an example object we'll get the following output:
```json
{
    "id": 1,
    "content": "A content",
    "model_b": 1
}
```
Now let's say we also want to include ModelB's content when serializing ModelA. We could add the explicit definition to our ModelASerializer or use the depth field.

When we change depth to 1 in our serializer like so:
```python
from rest_framework import serializers


class ModelASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelA
        fields = '__all__'
        depth = 1
```
The output changes to the following:
```json
{
    "id": 1,
    "content": "A content",
    "model_b": {
        "id": 1,
        "content": "B content",
        "model_c": 1
    }
}
```
If we change it to 2 our serializer will serialize a level deeper:
```json
{
    "id": 1,
    "content": "A content",
    "model_b": {
        "id": 1,
        "content": "B content",
        "model_c": {
            "id": 1,
            "content": "C content"
        }
    }
}
```
The downside is that you have no control over a child's serialization. Using depth will include all fields on the children, in other words.