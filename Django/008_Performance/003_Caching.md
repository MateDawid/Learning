# Caching in Django

Source: https://testdriven.io/blog/django-caching
Repo: https://github.com/MateDawid/course_Caching_in_Django

## Caching types

**Memcached**: Memcached is a memory-based, key-value store for small chunks of data. It supports distributed caching across multiple servers.

**Database**: Here, the cache fragments are stored in a database. A table for that purpose can be created with one of the Django's admin commands. This isn't the most performant caching type, but it can be useful for storing complex database queries.

**File** system: The cache is saved on the file system, in separate files for each cache value. This is the slowest of all the caching types, but it's the easiest to set up in a production environment.

**Local** memory: Local memory cache, which is best-suited for your local development or testing environments. While it's almost as fast as Memcached, it cannot scale beyond a single server, so it's not appropriate to use as a data cache for any app that uses more than one web server.

**Dummy**: A "dummy" cache that doesn't actually cache anything but still implements the cache interface. It's meant to be used in development or testing when you don't want caching, but do not wish to change your code.

## Caching levels
### Per-site cache
This is the easiest way to implement caching in Django. To do this, all you'll have to do is add two middleware classes to your settings.py file:
```python
# settings.py

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',     # NEW
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # NEW
]
...

CACHE_MIDDLEWARE_ALIAS = 'default'  # which cache alias to use
CACHE_MIDDLEWARE_SECONDS = '600'    # number of seconds to cache a page for (TTL)
CACHE_MIDDLEWARE_KEY_PREFIX = ''    # should be used if the cache is shared across multiple sites that use the same Django instance
```
Although caching the entire site could be a good option if your site has little or no dynamic content, it may not be appropriate to use for large sites with a memory-based cache backend since RAM is, well, expensive.
### Per-view cache
**It's the caching level that you should almost always start with when looking to implement caching in your Django app.**

You can implement this type of cache with the cache_page decorator either on the view function directly or in the path within URLConf:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def your_view(request):
    ...

# or

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('object/<int:object_id>/', cache_page(60 * 15)(your_view)),
]
```

The cache itself is based on the URL, so requests to, say, object/1 and object/2 will be cached separately.

It's worth noting that implementing the cache directly on the view makes it more difficult to disable the cache in certain situations. For example, what if you wanted to allow certain users access to the view without the cache? Enabling the cache via the URLConf provides the opportunity to associate a different URL to the view that doesn't use the cache:
```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('object/<int:object_id>/', your_view),
    path('object/cache/<int:object_id>/', cache_page(60 * 15)(your_view)),
]
```
### Template fragment cache

If your templates contain parts that change often based on the data you'll probably want to leave them out of the cache.

For example, perhaps you use the authenticated user's email in the navigation bar in an area of the template. Well, If you have thousands of users then that fragment will be duplicated thousands of times in RAM, one for each user. This is where template fragment caching comes into play, which allows you to specify the specific areas of a template to cache.

To cache a list of objects:
```html
{% load cache %}

{% cache 500 object_list %}
  <ul>
    {% for object in objects %}
      <li>{{ object.title }}</li>
    {% endfor %}
  </ul>
{% endcache %}
```
Here, ```{% load cache %}``` gives us access to the cache template tag, which expects a cache timeout in seconds (500) along with the name of the cache fragment (object_list).

### Low-level cache API

For cases where the previous options don't provide enough granularity, you can use the low-level API to manage individual objects in the cache by cache key.

For example:
```python
from django.core.cache import cache


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    objects = cache.get('objects')

    if objects is None:
        objects = Objects.all()
        cache.set('objects', objects)

    context['objects'] = objects

    return context
```

In this example, you'll want to invalidate (or remove) the cache when objects are added, changed, or removed from the database. One way to manage this is via database signals:
```python
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_delete, sender=Object)
def object_post_delete_handler(sender, **kwargs):
     cache.delete('objects')


@receiver(post_save, sender=Object)
def object_post_save_handler(sender, **kwargs):
    cache.delete('objects')
```