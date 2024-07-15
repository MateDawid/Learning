# Querysets
Sources:
1. https://docs.djangoproject.com/en/5.0/ref/models/querysets/#when-querysets-are-evaluated
2. https://docs.djangoproject.com/en/5.0/topics/db/queries/#caching-and-querysets
3. https://www.hacksoft.io/blog/django-orm-under-the-hood-iterables

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

## QuerySet as a generator vs QuerySet as an iterable

* The QuerySet is immutable - chaining methods to our queryset doesn't modify the original queryset - it creates a new one.
* The QuerySet is a generator when you iterate over it for the first time - when you start iterating over the queryset, internally it executes a SELECT query and yields the DB rows shaped into the desired Python data structure.
* The QuerySet is an iterable - once we've iterated over the queryset once, the queryset puts the DB result into a cache. On every subsequent iteration, we'll use the cached objects. This prevents us from unwanted queries duplication.

```python
users = User.objects.all()  # Creates a queryset

hacksoft_users = users.filter(email__icontains='@hacksoft.io') # Creates a new queryset

for user in hacksoft_users:  # Makes SELECT query and yields the result
    pass

for user in hacksoft_users:  # Just yields the cached result
    pass
```

Based on the unique querysets first iterations, the code above makes 1 SELECT query.

## Cache implementation
```python
class QuerySet:
    ...
    def _fetch_all(self):
        if self._result_cache is None:
            self._result_cache = list(self._iterable_class(self))
        # ... more code to handle prefetched relations

    def __iter__(self):
        self._fetch_all()
        return iter(self._result_cache)
```

## Iterable classes
Let's focus on the QuerySet._iterable_class and see what it does with the SELECT query's data.

The _iterable_class has two functions:

* calls the SQL compiler to execute SELECT query
* puts the raw database data (a list of tuples) into ORM objects(.all), dictionaries(.values) or tuples(.values_list) and return it

We have the following types of "iterable classes" that comes from the Django ORM:

* ModelIterable - used by .all and yields ORM objects
* ValuesIterable - set when .values is called and yields dictionaries
* ValuesListIterable, NamedValuesListIterable and FlatValuesListIterable - set when .values_list is called (we have 3 iterable classes here since values_list returns different formats depending on the named and flat arguments)

```python
class ValuesIterable(BaseIterable):
    def __iter__(self):
        queryset = self.queryset
        query = queryset.query
        compiler = query.get_compiler(queryset.db)

        names = [
            *query.extra_select,
            *query.values_select,
            *query.annotation_select,
        ]
        indexes = range(len(names))
        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size):
            yield {names[i]: row[i] for i in indexes}
```

## Methods chaining and order of execution
The order of the method chaining is not always the same as the order of execution.
We could categorize the QuerySet methods into 2 categories:

* Methods that modify the SQL query - filter/ exclude/ annotate/ only / etc. They are "executed" into the database when it runs the SQL query.
* Methods that define the data structure - all/ values / values_list/etc. They're executed in our Django app (by iterating over the iterable class and modifying the data)

The ORM allows us to chain the same methods in almost any order. But, no matter the order of chaining, the order of execution will always be:

1. Execute the methods that are modifying the SQL query
2. Run the query in the database
3. Execute the methods that define the data structure