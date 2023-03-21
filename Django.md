
# **DJANGO**
## PRZYGOTOWANIE PROJEKTU
### Virtual Environment
Przed rozpoczęciem nowego projektu konieczne jest założenie wirtualnego środowiska.
```commandline
python -m virtualenv {nazwa-venv}
```

Aby uruchomić wirtualne środowisko należy użyć komendy:
```commandline
{nazwa-venv}/Scripts/activate
```

### Instalacja Django
Aby zainstalować Django należy użyć komendy:
```commandline
python -m pip install Django
```
### Tworzenie projektu Django
Do utworzenia nowego projektu w Django należy użyć komendy:
```commandline
django-admin startproject {nazwa-projektu}
```
### Dodanie nowego modułu
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

### Uruchamianie aplikacji
Aby uruchomić aplikację na serwerze lokalnym należy będąc w folderze projektu użyć komendy:
```commandline
python manage.py runserver
```

### Pierwsza migracja
Po utworzeniu projektu konieczne jest wykonanie pierwszej migracji, w celu przygotowania bazy danych. Służy do tego komenda:
```commandline
python manage.py migrate
```
### Tworzenie superusera
Warto również założyć konto superusera, aby uzyskać możliwość logowania się w panelu administracyjnym.
```commandline
python manage.py createsuperuser
```
## DODAWANIE NOWEGO WIDOKU (VIEW)
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

## FORMULARZE
### Podstawowe formularze
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
## SESJA
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
## LOGIN / LOGOUT
```python
# module.urls.py
...

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
```
### Login
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
### Logout
```python
# module/views.py
def logout_view(request):
    logout(request)
    return render(request, "module/login.html", {
                "message": "Logged Out"
            })
```
## TESTY
### Testowanie modeli
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
### Testowanie przy użyciu Client
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
