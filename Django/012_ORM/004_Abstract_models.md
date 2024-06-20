# Abstract models

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0


Abstract models are a fantastic way to encapsulate common information and behavior. An abstract model isn’t represented by any database table; instead, its fields and methods are inherited by subclasses.

Example:

```python
class BaseProfile(models.Model):
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')
    
    class Meta:
        abstract = True

class StudentProfile(BaseProfile):
    graduation_year = models.IntegerField()
    

class TeacherProfile(BaseProfile):
    office = models.CharField(max_length=100)
```
Here, BaseProfile serves as a template. StudentProfile and TeacherProfile will both have bio and avatar fields, but they are stored in separate database tables with their specific fields.