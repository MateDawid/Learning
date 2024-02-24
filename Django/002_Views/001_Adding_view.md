# Dodawanie widoku
W celu dodania nowego widoku konieczne jest utworzenie jego definicji w views.py oraz określenie w urls.py endpointu pod jakim ten widok będzie dostępny.
```python
# project/module/views.py
 from django.shortcuts import render
 from django.http import HttpResponse

 def index(request):
     return HttpResponse("Hello, world!")
```
```python
# project/module/urls.py
 from django.urls import path
 from . import views

 urlpatterns = [
     path("", views.index, name="index")
 ]
```

Konieczne jest dodanie zawartości pliku urls.py zawartego w danym module do urls.py projektu.

```python
# project/project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('module/', include("module.urls"))
]
```