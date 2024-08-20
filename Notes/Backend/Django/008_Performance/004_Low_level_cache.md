# Low level caching

Source: https://testdriven.io/blog/django-low-level-cache

## Setup Redis

[Download](https://redis.io/download/) and install Redis.

Once installed, in a new terminal window start the Redis server and make sure that it's running on its default port, 6379. The port number will be important when we tell Django how to communicate with Redis.

```commandline
redis-server
```

For Django to use Redis as a cache backend, the django-redis dependency is required. It's already been installed, so you just need to add the custom backend to the settings.py file:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## Reading and setting cache

You may want to use the low-level cache API if you need to cache different:

* Model objects that change at different intervals
* Logged-in users' data separate from each other
* External resources with heavy computing load
* External API calls

Example:

The HomePageView view in products/views.py simply lists all products in the database:
```python
class HomePageView(View):
    template_name = 'products/home.html'

    def get(self, request):
        product_objects = Product.objects.all()

        context = {
            'products': product_objects
        }

        return render(request, self.template_name, context)

```

Let's add support for the low-level cache API to the product objects.

```python
from django.core.cache import cache


class HomePageView(View):
    template_name = 'products/home.html'

    def get(self, request):
        product_objects = cache.get('product_objects')      # NEW

        if product_objects is None:                         # NEW
            product_objects = Product.objects.all()
            cache.set('product_objects', product_objects)   # NEW

        context = {
            'products': product_objects
        }

        return render(request, self.template_name, context)
```

Here, we first checked to see if there's a cache object with the name product_objects in our default cache:

* If so, we just returned it to the template without doing a database query.
* If it's not found in our cache, we queried the database and added the result to the cache with the key product_objects.

## Invalidating the Cache
### TTL
Cache may be invalidated after period of time by using ```TTL``` param in settings like:

```python
# Cache time to live is 5 minutes
CACHE_TTL = 60 * 5
```

Example for view caching:

```python
import datetime

import requests
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

BASE_URL = 'https://httpbin.org/'
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ApiCalls(TemplateView):
    template_name = 'apicalls/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{BASE_URL}/delay/2')
        response.raise_for_status()
        context['content'] = 'Results received!'
        context['current_time'] = datetime.datetime.now()
        return context
```
### Signals
Cache may be also invalidated after changes in database by Django Signals.

Firstly, update ```module/apps.py``` file.

```python
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'

    def ready(self):                # NEW
        import products.signals     # NEW
```

Create file ```module/signals.py```.

```python
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product


@receiver(post_delete, sender=Product, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
     cache.delete('product_objects')


@receiver(post_save, sender=Product, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete('product_objects')
```

Here, we used the receiver decorator from django.dispatch to decorate two functions that get called when a product is added or deleted, respectively. Let's look at the arguments:

* The first argument is the signal event in which to tie the decorated function to, either a save or delete.
* We also specified a sender, the Product model in which to receive signals from.
* Finally, we passed a string as the dispatch_uid to prevent duplicate signals.

So, when either a save or delete occurs against the Product model, the delete method on the cache object is called to remove the contents of the product_objects cache.

### Django Lifecycle

Rather than using database signals, you could use a third-party package called [Django Lifecycle](https://rsinger86.github.io/django-lifecycle/), which helps make invalidation of cache easier and more readable.

Install ``django-lifecycle`` and modify ``module/apps.py`` to base form, without any Django signals settings.
```python
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'
```

Update model with django_lifecycle hooks like:

```python
from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Manager
from django_lifecycle import LifecycleModel, hook, AFTER_DELETE, AFTER_SAVE   # NEW
from django.utils import timezone


class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('product_objects')
        super(CustomQuerySet, self).update(updated=timezone.now(), **kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)


class Product(LifecycleModel):              # NEW
    title = models.CharField(max_length=200, blank=False)
    price = models.CharField(max_length=20, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    class Meta:
        ordering = ['-created']

    @hook(AFTER_SAVE)                       # NEW
    @hook(AFTER_DELETE)                     # NEW
    def invalidate_cache(self):             # NEW
       cache.delete('product_objects')      # NEW
```

In the code above, we:

* First imported the necessary objects from Django Lifecycle
* Then inherited from LifecycleModel rather than django.db.models
* Created an invalidate_cache method that deletes the product_object cache key
* Used the @hook decorators to specify the events that we want to "hook" into

As with django signals the hooks won't trigger if we do update via a QuerySet:
```python
Product.objects.filter(id=1).update(title="A new title")
```
In this case, we still need to create a custom Manager and QuerySet.