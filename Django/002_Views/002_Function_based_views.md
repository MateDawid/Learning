# Function-based views

Source: https://testdriven.io/blog/django-class-based-vs-function-based-views/#function-based-views-fbvs

## Pros

* Explicit code flow (you have full control over what happens)
* Simple to implement
* Easy to understand
* Great for unique view logic
* Easy to integrate with decorators

## Cons

* A lot of repeated (boilerplate) code
* Handling of HTTP methods via conditional branching
* Don't take advantage of OOP
* Harder to maintain

## Example

```python
from django.shortcuts import render, redirect
from django.views import View


def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task-list'))

    return render(request, 'todo/task_create.html', {
        'form': TaskForm(),
    })
```
In order to use FBVs, we have to register them inside urls.py like so:
```python
urlpatterns = [
    path('create/', task_create_view, name='task-create'),
]
```
## Usage

You should opt for FBVs when you're working on highly customized view logic. In other words, FBVs are a great use case for a view that doesn't share much code with other views. A few real-world examples for using FBVs would be: a statistics view, a chart view, and a password reset view.