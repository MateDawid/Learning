# User-level Permissions

Source: https://testdriven.io/blog/django-permissions/

## User permissions to model

When django.contrib.auth is added to the INSTALLED_APPS setting in the settings.py file, Django automatically creates add, change, delete and view permissions for each Django model that's created.

Permissions in Django follow the following naming sequence:

```{app}.{action}_{model_name}```
```python
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
```

By default, Django will create the following permissions:
* blog.add_post
* blog.change_post
* blog.delete_post
* blog.view_post

## Checking User permission

You can then check if a user (via a Django user object) has permissions with the has_perm() method:
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from blog.models import Post

content_type = ContentType.objects.get_for_model(Post)
post_permission = Permission.objects.filter(content_type=content_type)
print([perm.codename for perm in post_permission])
# => ['add_post', 'change_post', 'delete_post', 'view_post']

user = User.objects.create_user(username="test", password="test", email="test@user.com")

# Check if the user has permissions already
print(user.has_perm("blog.view_post"))
# => False

# To add permissions
for perm in post_permission:
    user.user_permissions.add(perm)

print(user.has_perm("blog.view_post"))
# => False
# Why? This is because Django's permissions do not take
# effect until you allocate a new instance of the user.

user = get_user_model().objects.get(email="test@user.com")
print(user.has_perm("blog.view_post"))
# => True
```

Superusers will always have permission set to True even if the permission does not exist:
```python
from django.contrib.auth.models import User

superuser = User.objects.create_superuser(
    username="super", password="test", email="super@test.com"
)

# Output will be true
print(superuser.has_perm("blog.view_post"))

# Output will be true even if the permission does not exists
print(superuser.has_perm("foo.add_bar"))
```