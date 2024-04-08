# Enforcing Permissions

Source: https://testdriven.io/blog/django-permissions/

Aside for the Django Admin, permissions are typically enforced at the view layer since the user is obtained from the request object.

To enforce permissions in class-based views, you can use the PermissionRequiredMixin from django.contrib.auth.mixins like so:
```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from blog.models import Post

class PostListView(PermissionRequiredMixin, ListView):
    permission_required = "blog.view_post"
    template_name = "post.html"
    model = Post
```
permission_required can either be a single permission or an iterable of permissions. If using an iterable, a user must have ALL the permissions before they can access the view:
```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from blog.models import Post

class PostListView(PermissionRequiredMixin, ListView):
    permission_required = ("blog.view_post", "blog.add_post")
    template_name = "post.html"
    model = Post
```
For function-based views, use the permission_required decorator:
```python
from django.contrib.auth.decorators import permission_required

@permission_required("blog.view_post")
def post_list_view(request):
    return HttpResponse()
```
You can also check for permissions in your Django templates. With Django's auth context processors, a perms variable is available by default when you render your template. The perms variable actually contains all permissions in your Django application.

For example:
```
{% if perms.blog.view_post %}
  {# Your content here #}
{% endif %}
```