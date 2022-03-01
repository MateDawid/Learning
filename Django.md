# **DJANGO**
## SPIS TREŚCI
* [PRZYGOTOWANIE PROJEKTU](#PRZYGOTOWANIE-PROJEKTU)
	* [Virtual Environment](#Virtual-Environment)
	* [Instalacja Django](#Instalacja-Django)
	* [Tworzenie projektu Django](#Tworzenie-projektu-Django)
	* [Dodanie nowego modułu](#Dodanie-nowego-modułu)
	* [Uruchamianie aplikacji](#Uruchamianie-aplikacji)
	* [Pierwsza migracja](#Pierwsza-migracja)
	* [Tworzenie superusera](#Tworzenie-superusera)
##PRZYGOTOWANIE PROJEKTU
###Virtual Environment
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