# Serializer
Wymaga zdefiniowania wszystkich pól, jakie mają być serializowane. Odpowiednik modelu Form z bazowego Django.

Przykładowy model:
```python
# models.py

from django.db import models  
from pygments.lexers import get_all_lexers  
from pygments.styles import get_all_styles  
  
LEXERS = [item for item in get_all_lexers() if item[1]]  
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])  
  
  
class Snippet(models.Model):  
    created = models.DateTimeField(auto_now_add=True)  
    title = models.CharField(max_length=100, blank=True, default='')  
    code = models.TextField()  
    linenos = models.BooleanField(default=False)  
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)  
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)  
  
    class Meta:  
        ordering = ['created']
```
Serializer dla modelu:
```python
# serializers.py

from rest_framework import serializers  
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES  
  
  
class SnippetSerializer(serializers.Serializer):  
    id = serializers.IntegerField(read_only=True)  
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)  
    code = serializers.CharField(style={'base_template': 'textarea.html'})  
    linenos = serializers.BooleanField(required=False)  
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')  
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')  
  
    def create(self, validated_data):  
		"""  
		Create and return a new `Snippet` instance, given the validated data. 
		"""  
		return Snippet.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
		"""  
		Update and return an existing `Snippet` instance, given the validated data. 
		"""  
		instance.title = validated_data.get('title', instance.title)  
		instance.code = validated_data.get('code', instance.code)  
		instance.linenos = validated_data.get('linenos', instance.linenos)  
		instance.language = validated_data.get('language', instance.language)  
		instance.style = validated_data.get('style', instance.style)  
		instance.save()  
		return instance
```