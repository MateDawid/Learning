# Static and media files

Source: https://testdriven.io/blog/django-static-files/

## Django project files types:
**Source code**: These are your core Python modules and HTML files that make up every Django project, where you define your models, views, and templates.

**Static files**: These are your CSS stylesheets, JavaScript files, fonts, and images. Since there's no processing involved, these files are very energy efficient since they can just be served up as is. They are also much easier to cache. Static files are kept in version control and shipped with your source code files during deployment.

**Media file**: These are files that a user uploads. Media files are files that your end-users (internally and externally) upload or are dynamically created by your application (often as a side effect of some user action).

## Why should you treat static and media files differently?

You can't trust files uploaded by end-users, so media files need to be treated differently.

You may need to perform processing on user uploaded, media files to be better served -- e.g., you could optimize uploaded images to support different devices.

You don't want a user uploaded file to replace a static file accidentally.

## Static files
### Settings
**STATIC_URL**: URL where the user can access your static files from in the browser. The default is /static/, which means your files will be available at http://127.0.0.1:8000/static/ in development mode -- e.g., http://127.0.0.1:8000/static/css/main.css.

**STATIC_ROOT**: The absolute path to the directory where your Django application will serve your static files from. When you run the collectstatic management command (more on this shortly), it will find all static files and copy them into this directory.

**STATICFILES_DIRS**: By default, static files are stored at the app-level at <APP_NAME>/static/. The collectstatic command will look for static files in those directories. You can also tell Django to look for static files in additional locations with STATICFILES_DIRS.

**STORAGES**: It specifies a way to configure different storage backends for managing files. Each storage backend can be given an alias, and there are two special aliases: default for managing files (with FileSystemStorage as the default storage engine) and staticfiles for managing static files (using StaticFilesStorage by default).

**STATICFILES_FINDERS**: This setting defines the file finder backends to be used to automatically find static files. By default, the FileSystemFinder and AppDirectoriesFinder finders are used:
* FileSystemFinder - uses the STATICFILES_DIRS setting to find files.
* AppDirectoriesFinder - looks for files in a "static" folder in each Django app within the project.

### Management commands
```collectstatic``` is a management command that collects static files from the various locations -- i.e., <APP_NAME>/static/ and the directories found in the STATICFILES_DIRS setting -- and copies them to the STATIC_ROOT directory.

```findstatic``` is a really helpful command to use when debugging so you can see exactly where a specific file comes from.

```runserver``` starts a lightweight, development server to run your Django application in development.

Don't put any static files in the STATIC_ROOT directory. That's where the static files get copied to automatically after you run collectstatic. Instead, always put them in the directories associated with the STATICFILES_DIRS setting or <APP_NAME>/static/.

### Development mode
Typical development config:

```python
# settings.py

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
```
![static_files_develop.png](static_files_develop.png)

### Production mode
* Use a web server like Nginx to route traffic destined for your static files directly to the static root (configured via STATIC_ROOT)
* Use WhiteNoise to serve up static files directly from the WSGI or ASGI web application server

Sample Nginx config:

```
upstream hello_django {
    server web:8000;
}

server {

    listen 80;

    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /home/app/web/staticfiles/;
    }

}
```
In short, when a request is sent to /static/ -- e.g, /static/base.css -- Nginx will attempt to serve the file from the "/home/app/web/staticfiles/" folder.

## Media files
### Settings
**MEDIA_URL**: Similar to the STATIC_URL, this is the URL where users can access media files.

**MEDIA_ROOT**: The absolute path to the directory where your Django application will serve your media files from.

### Development mode
Typical development config:
```python
# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'
```

Unfortunately, the Django development server doesn't serve media files by default. Fortunately, there's a very simple workaround: You can add the media root as a static path to the ROOT_URLCONF in your project-level URLs. Example:

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # ... the rest of your URLconf goes here ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Production mode

Sample Nginx config:
```
upstream hello_django {
    server web:8000;
}

server {

    listen 80;

    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /media/ {
        alias /home/app/web/mediafiles/;
    }

}
```
So, when a request is sent to /media/ -- e.g, /media/upload.png -- Nginx will attempt to serve the file from the "/home/app/web/mediafiles/" folder.
