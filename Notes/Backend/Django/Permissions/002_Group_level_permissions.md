# Group-level permissions

Source: https://testdriven.io/blog/django-permissions/

## Intro

Group models are a generic way of categorizing users so you can apply permissions, or some other label, to those users. A user can belong to any number of groups.

With Django, you can create groups to class users and assign permissions to each group so when creating users, you can just assign the user to a group and, in turn, the user has all the permissions from that group.

To create a group, you need the Group model from django.contrib.auth.models.

## Example

Let's create groups for the following roles:
* Author: Can view and add posts
* Editor: Can view, add, and edit posts
* Publisher: Can view, add, edit, and delete posts

```python
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from blog.models import Post

author_group, created = Group.objects.get_or_create(name="Author")
editor_group, created = Group.objects.get_or_create(name="Editor")
publisher_group, created = Group.objects.get_or_create(name="Publisher")

content_type = ContentType.objects.get_for_model(Post)
post_permission = Permission.objects.filter(content_type=content_type)
print([perm.codename for perm in post_permission])
# => ['add_post', 'change_post', 'delete_post', 'view_post']

for perm in post_permission:
    if perm.codename == "delete_post":
        publisher_group.permissions.add(perm)

    elif perm.codename == "change_post":
        editor_group.permissions.add(perm)
        publisher_group.permissions.add(perm)
    else:
        author_group.permissions.add(perm)
        editor_group.permissions.add(perm)
        publisher_group.permissions.add(perm)

user = User.objects.get(username="test")
user.groups.add(author_group)  # Add the user to the Author group

user = get_object_or_404(User, pk=user.id)

print(user.has_perm("blog.delete_post")) # => False
print(user.has_perm("blog.change_post")) # => False
print(user.has_perm("blog.view_post")) # => True
print(user.has_perm("blog.add_post")) # => True
```