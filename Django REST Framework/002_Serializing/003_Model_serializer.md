# ModelSerializer
Korzysta ze wskazanych pól modelu zdefiniowanego w klasie Meta, możliwe jest jednak dodanie własnych danych. Odpowiednik modelu ModelForm z bazowego Django.

Przykładowy model:
```python
# models.py

from django.db import models  
from utils.model_abstracts import Model  
from django_extensions.db.models import (  
    TimeStampedModel,  
  ActivatorModel,  
  TitleDescriptionModel  
)  
  
  
class Contact(  
    TimeStampedModel,  
  ActivatorModel,  
  TitleDescriptionModel,  
  Model  
):  
    class Meta:  
        verbose_name_plural = "Contacts"  
  
  email = models.EmailField(verbose_name="Email")  
  
    def __str__(self):  
        return f'{self.title}'
```
Serializer dla modelu:
```python
# serializers.py

from . import models  
from rest_framework import serializers  
from rest_framework.fields import CharField, EmailField  
  
  
class ContactSerializer(serializers.ModelSerializer):  
    name = CharField(source="title", required=True)  
    message = CharField(source="description", required=True)  
    email = EmailField(required=True)  
  
    class Meta:  
        model = models.Contact  
        fields = (  
			'name',  
			'email',  
			'message'  
		)
```