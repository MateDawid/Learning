# Querysets
Sources:
1. https://docs.djangoproject.com/en/5.0/ref/models/querysets/#when-querysets-are-evaluated
2. https://docs.djangoproject.com/en/5.0/topics/db/queries/#caching-and-querysets

## When QuerySets are evaluated
### Iteration
 A QuerySet is iterable, and it executes its database query the first time you iterate over it.
```python
for e in Entry.objects.all():
    print(e.headline)
```
Note: Don’t use this if all you want to do is determine if at least one result exists. It’s more efficient to use exists().

### Slicing with step paramether
Generally, slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query. An exception is if you use the “step” parameter of Python slice syntax. For example, this would actually execute the query in order to return a list of every second object of the first 10:
```python
Entry.objects.all()[:10:2]
```

### Pickling/Caching

If you pickle a QuerySet, this will force all the results to be loaded into memory prior to pickling. Pickling is usually used as a precursor to caching and when the cached queryset is reloaded, you want the results to already be present and ready for use (reading from the database can take some time, defeating the purpose of caching). This means that when you unpickle a QuerySet, it contains the results at the moment it was pickled, rather than the results that are currently in the database.

### repr()

A QuerySet is evaluated when you call repr() on it. This is for convenience in the Python interactive interpreter, so you can immediately see your results when using the API interactively.

### len()

A QuerySet is evaluated when you call len() on it. This, as you might expect, returns the length of the result list.

Note: If you only need to determine the number of records in the set (and don’t need the actual objects), it’s much more efficient to handle a count at the database level using SQL’s SELECT COUNT(*). Django provides a count() method for precisely this reason.

### list()

Force evaluation of a QuerySet by calling list() on it. For example:
```python
entry_list = list(Entry.objects.all())
```

### bool()

Testing a QuerySet in a boolean context, such as using bool(), or, and or an if statement, will cause the query to be executed. If there is at least one result, the QuerySet is True, otherwise False. For example:
```python
if Entry.objects.filter(headline="Test"):
    print("There is at least one Entry with the headline Test")
```
Note: If you only want to determine if at least one result exists (and don’t need the actual objects), it’s more efficient to use exists().

## Caching
### When QuerySets are cached
In a newly created QuerySet, the cache is empty. The first time a QuerySet is evaluated – and, hence, a database query happens – Django saves the query results in the QuerySet’s cache and returns the results that have been explicitly requested (e.g., the next element, if the QuerySet is being iterated over). Subsequent evaluations of the QuerySet reuse the cached results.

The following will create two QuerySets, evaluate them, and throw them away:

```python
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])
```
The same database query will be executed twice, effectively doubling your database load. Also, there’s a possibility the two lists may not include the same database records, because an Entry may have been added or deleted in the split second between the two requests.

To avoid this problem, save the QuerySet and reuse it:

```python
queryset = Entry.objects.all()
print([p.headline for p in queryset])  # Evaluate the query set.
print([p.pub_date for p in queryset])  # Reuse the cache from the evaluation.
```

### When QuerySets are not cached

Repeatedly getting a certain index in a queryset object will query the database each time:

```python
queryset = Entry.objects.all()
print(queryset[5])  # Queries the database
print(queryset[5])  # Queries the database again
```

However, if the entire queryset has already been evaluated, the cache will be checked instead:

```python
queryset = Entry.objects.all()
[entry for entry in queryset]  # Queries the database
print(queryset[5])  # Uses cache
print(queryset[5])  # Uses cache
```
Here are some examples of other actions that will result in the entire queryset being evaluated and therefore populate the cache:
```python
[entry for entry in queryset]
bool(queryset)
entry in queryset
list(queryset)
```