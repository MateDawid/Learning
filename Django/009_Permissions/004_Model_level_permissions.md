# Model-level Permissions

Source: https://testdriven.io/blog/django-permissions/

You can also add custom permissions to a Django model via the model Meta options.

Let's add an is_published flag to the Post model:
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
    is_published = models.Boolean(default=False)
```
Next, we'll set a custom permission called set_published_status:
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
    is_published = models.Boolean(default=False)

    class Meta:
        permissions = [
            (
                "set_published_status",
                "Can set the status of the post to either publish or not"
            )
        ]
```
In order to enforce this permission, we can use the UserPassesTestMixin Django provided mixin in our view, giving us the flexibility to explicitly check whether a user has the required permission or not.

Here's what a class-based view might look like that checks whether a user has permission to set the published status of a post:
```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import View

from blog.models import Post

class PostListView(UserPassesTestMixin, View):
    template_name = "post_details.html"

    def test_func(self):
        return self.request.user.has_perm("blog.set_published_status")

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        published_status = request.POST.get('published_status')

        if post_id:
            post = Post.objects.get(pk=post_id)
            post.is_published = bool(published_status)
            post.save()

        return render(request, self.template_name)
```
So, with UserPassesTestMixin, you need to override the test_func method of the class and add your own test. Do note that the return value of this method must always be a boolean.