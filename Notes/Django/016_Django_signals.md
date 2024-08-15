# Django Signals

Source: https://testdriven.io/courses/django-rest-framework/validation-ordering-pagination/#H-6-django-signals

Django provides several built-in signals that are set by default. Some examples:

* `pre_save` and `post_save` - triggered before/after a model's save() is called
* `pre_delete` and `post_delete` - triggered before/after a model's delete() or a QuerySets' delete() are called
* `request_started` and `request_finished` - triggered when Django starts or finishes an HTTP request
* `m2m_changed` - triggered when a ManyToManyField on a model is changed

There're two key elements of the signal: The sender and the receiver.

The sender (a Python object) dispatches a signal, and the receiver (a function or an instance method) receives the signal and then does something.

```python
# shopping_list/receivers.py


from django.db.models.signals import post_save
from django.dispatch import receiver

from shopping_list.models import ShoppingItem, ShoppingList


@receiver(post_save, sender=ShoppingItem)
def interaction_with_shopping_list(sender, instance, **kwargs):
    ShoppingList.objects.get(id=instance.shopping_list.id).save(update_fields=["last_interaction"])
```

With @receiver, we made the interaction_with_shopping_list function a receiver. The sender is ShoppingItem, and the signal is post_save.

So, when a ShoppingItem instance is saved, interaction_with_shopping_list updates the ShoppingList's last_interaction field.

We just need to register the receiver in shopping_list/apps.py:

```python
# shopping_list/apps.py


from django.apps.config import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shopping_list"

    def ready(self):
        import shopping_list.receivers
```

Now all receivers inside the shopping_list/receivers.py will be imported when the app is ready after it's initialized.

To ensure Django's uses this configuration, update shopping_list/__init__.py like so:

```python
default_app_config = "shopping_list.apps.ApiConfig"
```

This sets the app's default configuration to the one defined in shopping_list/apps.py.

