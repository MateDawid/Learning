# Indexes

Source: https://medium.com/@sandesh.thakar18/types-of-database-indexing-in-django-5d31581fec67

## Unique Index
A unique index ensures that no two rows in a table have the same values for the indexed columns. In Django, this can be achieved by adding the unique=True attribute to a field in the model. For example:

```python
class MyModel(models.Model):
  email = models.EmailField(unique=True)
```

## Primary Key Index
Every Django model has a primary key field, which is automatically created and added to the model by default. This field is used to uniquely identify each row in the table and is indexed for fast lookups. The primary key index is created automatically and cannot be removed.

## Regular Index
A regular index is used to improve the performance of queries that use the indexed columns. In Django, this can be achieved by adding the db_index=True attribute to a field in the model. For example:
```python
class MyModel(models.Model):
    name = models.CharField(max_length=100, db_index=True)
```

## Multi-column index
A multi-column index is used when you want to index multiple fields in your model. This is useful when you often query your data based on multiple fields at the same time. In Django, this can be achieved by creating an index on multiple fields using the Index class. For example:
```python
from django.db import models

class MyModel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]
```
## Partial Index
A partial index is a type of index that is created on a subset of a table’s rows, rather than the entire table. This can be useful when you want to improve the performance of queries that filter on specific values in a column.

In Django, partial indexes can be created using the Index class and the condition parameter. The condition parameter is used to specify a condition that must be met in order for a row to be included in the index.

For example, let’s say you have a model with a published field that is a boolean indicating whether an article has been published or not. If you often query for published articles and rarely for unpublished articles, you could create a partial index on the published field like this:
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    published = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['published'], name='published_idx', condition=Q(published=True))
        ]
```

This will create an index on the published field, but only for rows where the published field is True. This can improve the performance of queries that filter on published articles without affecting write performance or consuming unnecessary resources.

It’s worth noting that creating partial indexes can be beneficial when you have a specific use case, but it’s important to consider the trade-offs of each type of index in order to achieve the best performance for your application.

It’s worth noting that indexes are not always necessary and can sometimes slow down write operations. It’s important to consider the balance between read and write performance when deciding which fields to index. Additionally, it’s important to keep in mind that each index consumes disk space and memory and can slow down your database.

In conclusion, indexes are an important tool for optimizing the performance of Django’s database operations. The different types of indexes allow you to index fields in different ways, depending on the use case. It’s important to use them judiciously and consider the trade-offs of each type of index in order to achieve the best performance for your application.