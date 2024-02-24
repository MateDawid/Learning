# Podstawowe formularze

Definicja podstawowego formularza.

```python
# project/module/forms.py
from django import forms

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
```
Widok wykorzystujący formularz.

```python
# module/views.py
from django.urls import reverse
from django.http import HttpResponseRedirect

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
			# some logic for collected task
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            # Rendering invalid form with adnotations about errors
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
```
Wyświetlenie formularza w HTML.

```html
{% extends "module/layout.html" %}

{% block body %}
    <h1>Add Task:</h1>
    <form action="{% url 'module:add' %}" method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>
    <a href="{% url 'module:index' %}">View Tasks</a>
{% endblock %}
```