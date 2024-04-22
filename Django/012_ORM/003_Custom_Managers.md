# Custom Managers

Source: https://pogromcykodu.pl/masz-dosc-powtarzajacych-sie-warunkow-zapytan-django-manager-rozwiaze-twoj-problem/

## CustomManager

```python
from django.db import models

    
class ArticleManager(models.Manager): 
    def get_published(self): 
        return self.filter(published=True) 
    
    def get_archived(self): 
        return self.filter(archived=True) 

class Article(models.Model): 
    title = models.CharField(max_length=30) 
    published = models.BooleanField(default=False) 
    archived = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True) 

    objects = ArticleManager()  
```

From now on, calling `Article.objects.get_published()` will return only published Articles. Other QuerySet operations like `.exclude` can be performed.
```python
Article.objects.get_published().exclude(title__startswith='H') 
```

## Custom Manager with custom QuerySet

```python
from django.db import models

# Filtering objects directly on QuerySet
class ArticleQuerySet(models.QuerySet):
    def get_published(self):
        return self.filter(published=True)
    def get_archived(self):
        return self.filter(archived=True)

# Using custom Queryset in Custom manager.
class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)
    def get_published(self):
        return self.get_queryset().get_published()
    def get_archived(self):
        return self.get_queryset().get_archived()
    
class Article(models.Model):
    title = models.CharField(max_length=30)
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = ArticleManager()
```

Such composition enables to chain custom commands on QuerySets returned by Manager, like `Article.objects.get_published().get_archived()`
