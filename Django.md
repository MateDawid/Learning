
# **DJANGO**
## 1. PRZYGOTOWANIE PROJEKTU
### 1.1. Virtual Environment
Przed rozpoczęciem nowego projektu konieczne jest założenie wirtualnego środowiska.
```commandline
python -m virtualenv {nazwa-venv}
```

Aby uruchomić wirtualne środowisko należy użyć komendy:
```commandline
{nazwa-venv}/Scripts/activate
```

### 1.2. Instalacja Django
Aby zainstalować Django należy użyć komendy:
```commandline
python -m pip install Django
```
### 1.3. Tworzenie projektu Django
Do utworzenia nowego projektu w Django należy użyć komendy:
```commandline
django-admin startproject {nazwa-projektu}
```
### 1.4. Dodanie nowego modułu
Do dodania nowego modułu projektu służy komenda:
```commandline
django-admin startapp {nazwa-modulu}
```
Po dodaniu nowego modułu w pliku settings.py należy dodać moduł do INSTALLED_APPS
```python
# settings.py
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<nowy moduł>' 
]
```

### 1.5. Uruchamianie aplikacji
Aby uruchomić aplikację na serwerze lokalnym należy będąc w folderze projektu użyć komendy:
```commandline
python manage.py runserver
```

### 1.6. Pierwsza migracja
Po utworzeniu projektu konieczne jest wykonanie pierwszej migracji, w celu przygotowania bazy danych. Służy do tego komenda:
```commandline
python manage.py migrate
```
### 1.7. Tworzenie superusera
Warto również założyć konto superusera, aby uzyskać możliwość logowania się w panelu administracyjnym.
```commandline
python manage.py createsuperuser
```
## 2. DODAWANIE NOWEGO WIDOKU (VIEW)
W celu dodania nowego widoku konieczne jest utworzenie jego definicji w views.py oraz określenie w urls.py endpointu pod jakim ten widok będzie dostępny. Konieczne jest dodanie zawartości pliku urls.py zawartego w danym module do url.py projektu.
```python
# module/views.py
 from django.shortcuts import render
 from django.http import HttpResponse

 def index(request):
     return HttpResponse("Hello, world!")
```
```python
# module/urls.py
 from django.urls import path
 from . import views

 urlpatterns = [
     path("", views.index, name="index")
 ]
```
```python
# project.urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('module/', include("module.urls"))
]
```

## 3. FORMULARZE
### 3.1. Podstawowe formularze
```python
# module/forms.py
from django import forms

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
```
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
## 4. SESJA
```python
# module/views.py
def index(request):
    # Check if there already exists a "tasks" key in our session
    if "tasks" not in request.session:
        # If not, create a new list in session
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })
```
## 5. LOGIN / LOGOUT
```python
# module.urls.py
...

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
```
### 5.1. Login
```python
# module/views.py
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "module/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "module/login.html")
```
### 5.2. Logout
```python
# module/views.py
def logout_view(request):
    logout(request)
    return render(request, "module/login.html", {
                "message": "Logged Out"
            })
```
## 6. TESTY
### 6.1. Testowanie modeli
```python
from django.test import TestCase
from .models import Flight, Airport, Passenger


class FlightTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

	def test_departures_count(self):
	    a = Airport.objects.get(code="AAA")
	    self.assertEqual(a.departures.count(), 3)

	def test_arrivals_count(self):
	    a = Airport.objects.get(code="AAA")
	    self.assertEqual(a.arrivals.count(), 1)
```
### 6.2. Testowanie przy użyciu Client
```python
...
class FlightTestCase(TestCase):
	...
	def test_valid_flight_page(self):
	    a1 = Airport.objects.get(code="AAA")
	    f = Flight.objects.get(origin=a1, destination=a1)

	    c = Client()
	    response = c.get(f"/flights/{f.id}")
	    self.assertEqual(response.status_code, 200)

	def test_invalid_flight_page(self):
	    max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

	    c = Client()
	    response = c.get(f"/flights/{max_id + 1}")
	    self.assertEqual(response.status_code, 404)
```
## 7. Django REST Framework
### 7.1. Przygotowanie projektu
Przykładowa zawartość pliku requirements.txt, którą należy zainstalować.
```
Django==4.1.3  
django-extensions==3.2.1  
django-filter==22.1  
djangorestframework==3.14.0  
djangorestframework-jsonapi==6.0.0
```
Następnie w pliku settings.py dodać zainstalowane pakiety.

```python
# settings.py

INSTALLED_APPS = [  
    'django.contrib.admin',  
  'django.contrib.auth',  
  'django.contrib.contenttypes',  
  'django.contrib.sessions',  
  'django.contrib.messages',  
  'django.contrib.staticfiles',  
  'django_extensions', #Great packaged to access abstract models  
  'django_filters', #Used with DRF  
  'rest_framework', #DRF package  
]
```
W tym samym pliku dodać słownik REST_FRAMEWORK. Poniżej przykład z bazowymi wartościami z dokumentacji.
 ```python
#settings.py

REST_FRAMEWORK = {  
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',  
  'DEFAULT_PARSER_CLASSES': (  
        'rest_framework_json_api.parsers.JSONParser',  
  ),  
  'DEFAULT_RENDERER_CLASSES': (  
        'rest_framework_json_api.renderers.JSONRenderer',  
  'rest_framework.renderers.BrowsableAPIRenderer'  
  ),  
  'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',  
  'DEFAULT_FILTER_BACKENDS': (  
        'rest_framework_json_api.filters.QueryParameterValidationFilter',  
  'rest_framework_json_api.filters.OrderingFilter',  
  'rest_framework_json_api.django_filters.DjangoFilterBackend',  
  'rest_framework.filters.SearchFilter',  
  ),  
  'SEARCH_PARAM': 'filter[search]',  
  'TEST_REQUEST_RENDERER_CLASSES': (  
        'rest_framework_json_api.renderers.JSONRenderer',  
  ),  
  'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'  
}
```
W głównym pliku urls.py dodać router i jego adresy.
```python
#urls.py

from django.urls import path  
from django.contrib import admin  
from rest_framework import routers  
  
router = routers.DefaultRouter()  
  
urlpatterns = router.urls  
  
urlpatterns += [  
    path('admin/', admin.site.urls),  
]
```
Utworzyć i wykonać migracje
```
python manage.py makemigrations
python manage.py migrate
```
