Backend
=======

# Backend\Authentication\001_Basic_authentication.md

## HTTP Basic Authentication

Source: https://testdriven.io/blog/web-authentication-methods/#http-basic-authentication

### Intro

Basic authentication, which is built into the HTTP protocol, is the most basic form of authentication. With it, login credentials are sent in the request headers with each request:
```
"Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=" your-website.com
```

Usernames and passwords are not encrypted. Instead, the username and password are concatenated together using a : symbol to form a single string: username:password. This string is then encoded using base64.
```
>>> import base64
>>>
>>> auth = "username:password"
>>> auth_bytes = auth.encode('ascii') # convert to bytes
>>> auth_bytes
b'username:password'
>>>
>>> encoded = base64.b64encode(auth_bytes) # base64 encode
>>> encoded
b'dXNlcm5hbWU6cGFzc3dvcmQ='
>>> base64.b64decode(encoded) # base64 decode
b'username:password'
```
This method is stateless, so the client must supply the credentials with each and every request. It's suitable for API calls along with simple auth workflows that do not require persistent sessions.

### Flow
![001_Flow.png](_images/001_Flow.png)
### Pros
* Since there aren't many operations going on, authentication can be faster with this method.
* Easy to implement.
* Supported by all major browsers.
### Cons
* Base64 is not the same as encryption. It's just another way to represent data. The base64 encoded string can easily be decoded since it's sent in plain text. This poor security feature calls for many types of attacks. Because of this, HTTPS/SSL is absolutely essential.
* Credentials must be sent with every request.
* Users can only be logged out by rewriting the credentials with an invalid one.
# Backend\Authentication\002_Digest_authentication.md

## HTTP Digest Authentication

Source: https://testdriven.io/blog/web-authentication-methods/#http-digest-authentication

### Intro

HTTP Digest Authentication (or Digest Access Authentication) is a more secure form of HTTP Basic Auth. The main difference is that the password is sent in MD5 hashed form rather than in plain text, so it's more secure than Basic Auth.

### Flow

![002_Flow.png](_images/002_Flow.png)

### Pros

* More secure than Basic auth since the password is not sent in plain text.
* Easy to implement.
* Supported by all major browsers.

### Cons

* Credentials must be sent with every request.
* User can only be logged out by rewriting the credentials with an invalid one.
* Compared to Basic auth, passwords are less secure on the server since bcrypt can't be used.
* Vulnerable to man-in-the-middle attacks.
# Backend\Authentication\003_Session-based_Auth.md

## Session-based Auth

Source: https://testdriven.io/blog/web-authentication-methods/#session-based-auth

### Intro

With session-based auth (or session cookie auth or cookie-based auth), the user's state is stored on the server. It does not require the user to provide a username or a password with each request. Instead, after logging in, the server validates the credentials. If valid, it generates a session, stores it in a session store, and then sends the session ID back to the browser. The browser stores the session ID as a cookie, which gets sent anytime a request is made to the server.

Session-based auth is stateful. Each time a client requests the server, the server must locate the session in memory in order to tie the session ID back to the associated user.

### Flow

![003_Flow.png](_images/003_Flow.png)

### Pros
* Faster subsequent logins, as the credentials are not required.
* Improved user experience.
* Fairly easy to implement. Many frameworks (like Django) provide this feature out-of-the-box.
### Cons
* It's stateful. The server keeps track of each session on the server-side. The session store, used for storing user session information, needs to be shared across multiple services to enable authentication. Because of this, it doesn't work well for RESTful services, since REST is a stateless protocol.
* Cookies are sent with every request, even if it does not require authentication.
* Vulnerable to CSRF attacks. Read more about CSRF and how to prevent it in Flask here.
# Backend\Authentication\004_Token-based_Auth.md

## Token-Based Authentication

Source: https://testdriven.io/blog/web-authentication-methods/#token-based-authentication

### Intro

This method uses tokens to authenticate users instead of cookies. The user authenticates using valid credentials and the server returns a signed token. This token can be used for subsequent requests.

Tokens don't need not be saved on the server-side. They can just be validated using their signature. In recent times, token adoption has increased due to the rise of RESTful APIs and Single Page Applications (SPAs).

### JSON Web Token

The most commonly used token is a JSON Web Token (JWT). A JWT consists of three parts:

* Header (includes the token type and the hashing algorithm used)
* Payload (includes the claims, which are statements about the subject)
* Signature (used to verify that the message wasn't changed along the way)

All three are base64 encoded and concatenated using a . and hashed. Since they are encoded, anyone can decode and read the message. But only authentic users can produce valid signed tokens. The token is authenticated using the Signature, which is signed with a private key.

JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties. The claims in a JWT are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) structure or as the plaintext of a JSON Web Encryption (JWE) structure, enabling the claims to be digitally signed or integrity protected with a Message Authentication Code (MAC) and/or encrypted. - IETF

### Flow

![004_Flow.png](_images/004_Flow.png)

## Pros
* It's stateless. The server doesn't need to store the token as it can be validated using the signature. This makes the request faster as a database lookup is not required.
* Suited for a microservices architecture, where multiple services require authentication. All we need to configure at each end is how to handle the token and the token secret. 
## Cons
* Depending on how the token is saved on the client, it can lead to XSS (via localStorage) or CSRF (via cookies) attacks.
* Tokens cannot be deleted. They can only expire. This means that if the token gets leaked, an attacker can misuse it until expiry. Thus, it's important to set token expiry to something very small, like 15 minutes.
* Refresh tokens need to be set up to automatically issue tokens at expiry.
* One way to delete tokens is to create a database for blacklisting tokens. This adds extra overhead to the microservice architecture and introduces state.
# Backend\Authentication\005_One_Time_Passwords.md

## One Time Passwords

Source: https://testdriven.io/blog/web-authentication-methods/#one-time-passwords

### Intro
One time passwords (OTPs) are commonly used as confirmation for authentication. OTPs are randomly generated codes that can be used to verify if the user is who they claim to be. Its often used after user credentials are verified for apps that leverage two-factor authentication.

To use OTP, a trusted system must be present. This trusted system could be a verified email or mobile number.

Modern OTPs are stateless. They can be verified using multiple methods. While there are a few different types of OTPs, Time-based OTPs (TOTPs) is arguably the most common type. Once generated, they expire after a period of time.

Since you get an added layer of security, OTPs are recommended for apps that involve highly sensitive data, like online banking and other financial services.

### Flow
The traditional way of implementing OTPs:

* Client sends username and password
* After credential verification, the server generates a random code, stores it on the server-side, and sends the code to the trusted system
* The user gets the code on the trusted system and enters it back on the web app
* The server verifies the code against the one stored and grants access accordingly

How TOTPs work:

* Client sends username and password
* After credential verification, the server generates a random code using a randomly generated seed, stores the seed on the server-side, and sends the code to the trusted system
* The user gets the code on the trusted system and enters it back on the web app
* The server verifies the code against the stored seed, ensures that it has not expired, and grants access accordingly

How OTP agents like Google Authenticator, Microsoft Authenticator, and FreeOTP work:

* Upon registering for Two Factor Authentication (2FA), the server generates a random seed value and sends the seed to the user in the form of unique QR code
* The user scans the QR code using their 2FA application to validate the trusted device
* Whenever the OTP is required, the user checks for the code on their device and enters it on the web app
* The server verifies the code and grants access accordingly

### Pros
* Adds an extra layer of protection.
* No danger that a stolen password can be used for multiple sites or services that also implement OTPs.
### Cons
* You need to store the seed used for generating OTPs.
* OTP agents like Google Authenticator are difficult to set up again if you lose the recovery code.
* Problems arise when the trusted device is not available (dead battery, network error, etc.). Because of this, a backup device is typically required which adds an additional attack vector.
# Backend\Authentication\006_OAuth_and_OpenID.md

## OAuth and OpenID

Source 1: https://testdriven.io/blog/web-authentication-methods/#oauth-and-openid
Source 2: https://developer.okta.com/blog/2019/10/21/illustrated-guide-to-oauth-and-oidc

### Intro

OpenID - used for authentication
OAuth - used for authorization

OAuth 2.0 is designed only for authorization, for granting access to data and features from one application to another. OpenID Connect (OIDC) is a thin layer that sits on top of OAuth 2.0 that adds login and profile information about the person who is logged in. Establishing a login session is often referred to as authentication, and information about the person logged in (i.e. the Resource Owner) is called identity. When an Authorization Server supports OIDC, it is sometimes called an identity provider, since it provides information about the Resource Owner back to the Client.

OpenID Connect enables scenarios where one login can be used across multiple applications, also known as single sign-on (SSO). For example, an application could support SSO with social networking services such as Facebook or Twitter so that users can choose to leverage a login they already have and are comfortable using.

OAuth/OAuth2 and OpenID are popular forms of authorization and authentication, respectively. They are used to implement social login, which is a form of single sign-on (SSO) using existing information from a social networking service such as Facebook, Twitter, or Google, to sign in to a third-party website instead of creating a new login account specifically for that website.

This type of authentication and authorization can be used when you need to have highly-secure authentication. Some of these providers have more than enough resources to invest in the authentication itself. Leveraging such battle-tested authentication systems can ultimately make your application more secure.

This method is often coupled with session-based auth.

### Flow

You visit a website that requires you to log in. You navigate to the login page and see a button called "Sign in with Google". You click the button and it takes you to the Google login page. Once authenticated, you're then redirected back to the website that logs you in automatically. This is an example of using OpenID for authentication. It lets you authenticate using an existing account (via an OpenID provider) without the need to create a new account.

The most famous OpenID providers are Google, Facebook, Twitter, and GitHub.

After logging in, you navigate to the download service within the website that lets you download large files directly to Google Drive. How does the website get access to your Google Drive? This is where OAuth comes into play. You can grant permissions to access resources on another website. In this case, write access to Google Drive.

### Pros

* Improved security.
* Easier and faster log in flows since there's no need to create and remember a username or password.
* In case of a security breach, no third-party damage will occur, as the authentication is passwordless.

### Cons

* Your application now depends on another app, outside of your control. If the OpenID system is down, users won't be able to log in.
* People often tend to ignore the permissions requested by OAuth applications.
* Users that don't have accounts on the OpenID providers that you have configured won't be able to access your application. The best approach is to implement both -- i.e., username and password and OpenID -- and let the user choose.


# Backend\Django\Admin_site\001_Basic_customization.md

### Basic Admin Site Customization

Source: https://testdriven.io/blog/customize-django-admin/#basic-admin-site-customization

#### Site header
```python
### core/urls.py

admin.site.site_title = "TicketsPlus site admin (DEV)"
admin.site.site_header = "TicketsPlus administration"
admin.site.index_title = "Site administration"
```

#### URL

Another thing you should do is change the default /admin URL. This'll make it more difficult for malicious actors to find your admin panel.

Change your core/urls.py like so:
```python
### core/urls.py

urlpatterns = [
    path("secretadmin/", admin.site.urls),
]
```
Your admin site should now be accessible at http://localhost:8000/secretadmin.
# Backend\Django\Admin_site\002_Django_model_affect_on_admin.md

### Django Model and Admin

Source: https://testdriven.io/blog/customize-django-admin/#django-model-and-admin

Some Django model attributes directly affect the Django admin site. Most importantly:

* __str__() is used to define object's display name
* Meta class is used to set various metadata options (e.g., ordering and verbose_name)

Here's an example of how these attributes are used in practice:
```python
### tickets/models.py

class ConcertCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "concert category"
        verbose_name_plural = "concert categories"
        ordering = ["-name"]

    def __str__(self):
        return f"{self.name}"
```
We provided the plural form since the plural of "concert category" isn't "concert categorys".
By providing the ordering attribute the categories are now ordered by name.
# Backend\Django\Admin_site\003_List_display.md

### List Display

Source: https://testdriven.io/blog/customize-django-admin/#customize-admin-site-with-modeladmin-class

#### Control List Display

The list_display attribute allows you to control which model fields are displayed on the model list page. Another great thing about it is that it can display related model fields using the __ operator.
```python
### tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", "venue", "starts_at", "price", "tickets_left"]
    readonly_fields = ["tickets_left"]
```

By adding the venue to the list_display, we introduced the N + 1 problem. Since Django needs to fetch the venue name for each concert separately, many more queries get executed.

To avoid the N + 1 problem, we can use the list_select_related attribute, which works similarly to the select_related method:

```python
### tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", "venue", "starts_at", "price", "tickets_left"]
    list_select_related = ["venue"]
    readonly_fields = ["tickets_left"]
```

#### List Display Custom Fields

The list_display setting can also be used to add custom fields. To add a custom field, you must define a new method within the ModelAdmin class.

Add a "Sold Out" field, which is True if no tickets are available:
```python
### tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", "venue", "starts_at", "tickets_left", "display_sold_out"]
    list_select_related = ["venue"]

    def display_sold_out(self, obj):
        return obj.tickets_left == 0

    display_sold_out.short_description = "Sold out"
    display_sold_out.boolean = True
```
We used short_description to set the column name and boolean to tell Django that this column has a boolean value. This way, Django displays the tick/cross icon instead of True and False. We also had to add our display_sold_out method to list_display.
```python
### tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    list_display = [
        "name", "venue", "starts_at", "tickets_left", "display_sold_out",  "display_price"
    ]
    # ...

    def display_price(self, obj):
        return f"${obj.price}"

    display_price.short_description = "Price"
    display_price.admin_order_field = "price"
```
We used admin_order_field to tell Django by what field this column is orderable.
# Backend\Django\Admin_site\004_Linking_related_model_objects.md

### ModelAdmin Class

Source: https://testdriven.io/blog/customize-django-admin/#link-related-model-objects

#### Link Related Model Objects

Django admin site URL structure:

| Page	   | URL                               | 	Description                                   |
|---------|-----------------------------------|------------------------------------------------|
| List    | 	admin:\<app>_\<model>_changelist | 	Displays the list of objects                  |
| Add     | 	admin:\<app>_\<model>_add        | 	Object add form                               |
| Change  | 	admin:\<app>_\<model>_change     | 	Object change form (requires objectId)        |
| Delete  | 	admin:\<app>_\<model>_delete     | 	Object delete form (requires objectId)        |
| History | 	admin:\<app>_\<model>_history    | 	Displays object's history (requires objectId) |

Add the display_venue method to ConcertAdmin like so:
```python
### tickets/admin.py

class ConcertAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = [
        "name", "venue", "starts_at", "tickets_left",
        "display_sold_out",  "display_price", "display_venue",
    ]
    list_select_related = ["venue"]

    # ...

    def display_venue(self, obj):
        link = reverse("admin:tickets_venue_change", args=[obj.venue.id])
        return format_html('<a href="{}">{}</a>', link, obj.venue)

    display_venue.short_description = "Venue"
```
# Backend\Django\Admin_site\005_Filtering.md

### Filter Model Objects

Source: https://testdriven.io/blog/customize-django-admin/#filter-model-objects

```python
### tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    # ...
    list_filter = ["venue"]
```

To filter by a related object's fields, use the __ operator.

or more advanced filtering functionality, you can also define custom filters. To define a custom filter, you must specify the options or so-called lookups and a queryset for each lookup.

```python
### tickets/admin.py

from django.contrib.admin import SimpleListFilter


class SoldOutFilter(SimpleListFilter):
    title = "Sold out"
    parameter_name = "sold_out"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Yes"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(tickets_left=0)
        else:
            return queryset.exclude(tickets_left=0)


class ConcertAdmin(admin.ModelAdmin):
    # ...
    list_filter = ["venue", SoldOutFilter]
```

# Backend\Django\Admin_site\006_Searching.md

### Search Model Objects

Source: https://testdriven.io/blog/customize-django-admin/#search-model-objects

Django admin provides basic search functionality. It can be enabled by specifying which model fields should be searchable via the search_fields attribute. Keep in mind that Django doesn't support fuzzy queries by default.

```python
### tickets/admin.py

class ConcertAdmin(admin.ModelAdmin):
    # ...
    search_fields = ["name", "venue__name", "venue__address"]
```


# Backend\Django\Admin_site\007_Inlines.md

### Handle Model Inlines

Source: https://testdriven.io/blog/customize-django-admin/#handle-model-inlines

The admin interface allows you to edit models on the same page as the parent model via inlines. Django provides two types of inlines StackedInline and TabularInline. The main difference between them is how they look.

```python
### tickets/admin.py

class ConcertInline(admin.TabularInline):
    model = Concert
    fields = ["name", "starts_at", "price", "tickets_left"]

    # optional: make the inline read-only
    readonly_fields = ["name", "starts_at", "price", "tickets_left"]
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = True


class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "capacity"]
    inlines = [ConcertInline]
```
# Backend\Django\Admin_site\008_Custom_actions.md

### Custom Admin Actions

Source: https://testdriven.io/blog/customize-django-admin/#custom-admin-actions

Django admin actions allow you to perform an "action" on an object or a group of objects. An action can be used to modify an object's attributes, delete the object, copy it, and so forth. Actions are primarily utilized for frequently performed "actions" or bulk changes.

```python
### tickets/admin.py

@admin.action(description="Activate selected tickets")
def activate_tickets(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate selected tickets")
def deactivate_tickets(modeladmin, request, queryset):
    queryset.update(is_active=False)


class TicketAdmin(admin.ModelAdmin):
    # ...
    actions = [activate_tickets, deactivate_tickets]
```
# Backend\Django\Admin_site\009_Custom_admin_form.md

### Override Django Admin Forms

Source: https://testdriven.io/blog/customize-django-admin/#override-django-admin-forms

By default, Django automatically generates a ModelForm for your model. That form is then used on the add and change page. If you want to customize the form or implement unique data validation, you'll have to override the form.

Go ahead and create a forms.py file in the tickets app:
```python
### tickets/forms.py

from django import forms
from django.forms import ModelForm, RadioSelect

from tickets.models import Ticket


class TicketAdminForm(ModelForm):
    first_name = forms.CharField(label="First name", max_length=32)
    last_name = forms.CharField(label="Last name", max_length=32)

    class Meta:
        model = Ticket
        fields = [
            "concert",
            "first_name",
            "last_name",
            "payment_method",
            "is_active"
        ]
        widgets = {
            "payment_method": RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = {}

        if instance:
            customer_full_name_split = instance.customer_full_name.split(" ", maxsplit=1)
            initial = {
                "first_name": customer_full_name_split[0],
                "last_name": customer_full_name_split[1],
            }

        super().__init__(*args, **kwargs, initial=initial)

    def save(self, commit=True):
        self.instance.customer_full_name = self.cleaned_data["first_name"] + " " \
                                            + self.cleaned_data["last_name"]
        return super().save(commit)
```
Here:

We added the first_name and last_name form fields.
We used the Meta class to specify what model this form relates to and what fields to include.
On form __init__(), we populated the form using model instance data.
On save(), we merged first_name and last_name and saved it as customer_full_name.
Next, set TicketAdmin's form like so:
```python
### tickets/admin.py

class TicketAdmin(admin.ModelAdmin):
    # ...
    form = TicketAdminForm
```
# Backend\Django\Config\001_venv.md

### Virtual Environment
Przed rozpoczęciem nowego projektu konieczne jest założenie wirtualnego środowiska.
```commandline
python -m virtualenv {nazwa-venv}
```

Aby uruchomić wirtualne środowisko należy użyć komendy:
```commandline
{nazwa-venv}/Scripts/activate
```

# Backend\Django\Config\002_Django_installation.md

### Instalacja Django
Aby zainstalować Django należy użyć komendy:
```commandline
python -m pip install Django
```
# Backend\Django\Config\003_Creating_new_project.md

### Tworzenie projektu Django
Do utworzenia nowego projektu w Django należy użyć komendy:
```commandline
django-admin startproject {nazwa-projektu}
```
# Backend\Django\Config\004_Creating_new_module.md

### Dodanie nowego modułu
Do dodania nowego modułu projektu służy komenda:
```commandline
django-admin startapp {nazwa-modulu}
```
Po dodaniu nowego modułu w pliku settings.py należy dodać moduł do INSTALLED_APPS
```python
### settings.py
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
# Backend\Django\Config\005_Running_project.md

### Uruchamianie aplikacji
Aby uruchomić aplikację na serwerze lokalnym należy będąc w folderze projektu użyć komendy:
```commandline
python manage.py runserver
```
# Backend\Django\Config\006_First_migrations.md

### Pierwsze migracje
Po utworzeniu projektu konieczne jest wykonanie pierwszych migracji, w celu przygotowania bazy danych. Służy do tego komenda:
```commandline
python manage.py migrate
```
# Backend\Django\Config\007_Static_and_media_files.md

### Static and media files

Source: https://testdriven.io/blog/django-static-files/

#### Django project files types:
**Source code**: These are your core Python modules and HTML files that make up every Django project, where you define your models, views, and templates.

**Static files**: These are your CSS stylesheets, JavaScript files, fonts, and images. Since there's no processing involved, these files are very energy efficient since they can just be served up as is. They are also much easier to cache. Static files are kept in version control and shipped with your source code files during deployment.

**Media file**: These are files that a user uploads. Media files are files that your end-users (internally and externally) upload or are dynamically created by your application (often as a side effect of some user action).

#### Why should you treat static and media files differently?

You can't trust files uploaded by end-users, so media files need to be treated differently.

You may need to perform processing on user uploaded, media files to be better served -- e.g., you could optimize uploaded images to support different devices.

You don't want a user uploaded file to replace a static file accidentally.

#### Static files
##### Settings
**STATIC_URL**: URL where the user can access your static files from in the browser. The default is /static/, which means your files will be available at http://127.0.0.1:8000/static/ in development mode -- e.g., http://127.0.0.1:8000/static/css/main.css.

**STATIC_ROOT**: The absolute path to the directory where your Django application will serve your static files from. When you run the collectstatic management command (more on this shortly), it will find all static files and copy them into this directory.

**STATICFILES_DIRS**: By default, static files are stored at the app-level at <APP_NAME>/static/. The collectstatic command will look for static files in those directories. You can also tell Django to look for static files in additional locations with STATICFILES_DIRS.

**STORAGES**: It specifies a way to configure different storage backends for managing files. Each storage backend can be given an alias, and there are two special aliases: default for managing files (with FileSystemStorage as the default storage engine) and staticfiles for managing static files (using StaticFilesStorage by default).

**STATICFILES_FINDERS**: This setting defines the file finder backends to be used to automatically find static files. By default, the FileSystemFinder and AppDirectoriesFinder finders are used:
* FileSystemFinder - uses the STATICFILES_DIRS setting to find files.
* AppDirectoriesFinder - looks for files in a "static" folder in each Django app within the project.

##### Management commands
```collectstatic``` is a management command that collects static files from the various locations -- i.e., <APP_NAME>/static/ and the directories found in the STATICFILES_DIRS setting -- and copies them to the STATIC_ROOT directory.

```findstatic``` is a really helpful command to use when debugging so you can see exactly where a specific file comes from.

```runserver``` starts a lightweight, development server to run your Django application in development.

Don't put any static files in the STATIC_ROOT directory. That's where the static files get copied to automatically after you run collectstatic. Instead, always put them in the directories associated with the STATICFILES_DIRS setting or <APP_NAME>/static/.

##### Development mode
Typical development config:

```python
### settings.py

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
```
![static_files_develop.png](_images/static_files_develop.png)

##### Production mode
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

#### Media files
##### Settings
**MEDIA_URL**: Similar to the STATIC_URL, this is the URL where users can access media files.

**MEDIA_ROOT**: The absolute path to the directory where your Django application will serve your media files from.

##### Development mode
Typical development config:
```python
### settings.py

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

##### Production mode

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

# Backend\Django\Forms\001_Base_forms.md

### Podstawowe formularze

Definicja podstawowego formularza.

```python
### project/module/forms.py
from django import forms

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
```
Widok wykorzystujący formularz.

```python
### module/views.py
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
# Backend\Django\Good practices\001_Separating_business_logic.md

### Separating business logic

Sources: 
* https://emcarrio.medium.com/business-logic-in-a-django-project-a25abc64718c
* https://github.com/HackSoftware/Django-Styleguide

#### Shortly

In Django, business logic should live in:

* Services - functions, that mostly take care of writing things to the database.
* Selectors - functions, that mostly take care of fetching things from the database.
* Model properties (with some exceptions).
* Model clean method for additional validations (with some exceptions).

In Django, business logic should not live in:

* APIs and Views.
* Serializers and Forms.
* Form tags.
* Model save method.
* Custom managers or querysets.
* Signals.

Model properties vs selectors:

* If the property spans multiple relations, it should better be a selector.
* If the property is non-trivial & can easily cause N + 1 queries problem, when serialized, it should better be a selector.

The general idea is to "separate concerns" so those concerns can be maintainable / testable.

#### In detail

>As a rule-of-thumb, your application logic should live in modules that aren’t Django-specific modules (eg not in views.py, models.py or forms.py). If I had my way, Django would create an empty business_logic.py in each new app to encourage this.

Just be careful of not taking too much away from your models or you will be left with anemic domain models. Only business logic is meant to leave, the domain logic like validations, calculations, etc are already at home.

The answer is treating it like a data repository. A really not used pattern to a big part of the Django developers I used to know (highly influenced by using the Django ORM everywhere).

In reality, this solution is the recommended way of doing things, although it is not advertised as a data repository at all. In every Django tutorial, you are suggested to write your queries inside custom managers to avoid repetition and writing the same query every time. But you are gaining a lot more than that, implementing the queries there decouples the ORM implementation from its use in the application, a win-win situation.

Following this principle, you can then use your Model.objects as it was your data repository in the business logic, reducing the coupling to the ORM and allowing you to do integration tests for the database interactions only. In the next example, we’ll see how to use it.

#### Example

The example is very simple: we have an Address model that has an is_default field that indicates if that address is the default one of its user.

And then we have an action that makes an address instance the default one, setting its is_default to True and setting it to False to the other user’s addresses. After setting the default address, we publish the changes to anyone interested.

Here first we have the example done using fat models (high coupling and low cohesion):

```python
### models.py
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    is_default = models.BooleanField()

    @property
    def full_address(self):
        return f'{self.street}, {self.number}'

    # Business logic inside the model
    def set_default(self):
        # Dependencies with other models (in this case the same one)
        Address.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True
        self.save()

        # Side-effects of the action inside the model, SRP ko
        events.publish(events.DEFAULT_ADDRESS_CHANGED, address=self)


### tests.py
class TestSetDefault:

    @pytest.fixture
    def address(self, user):
        return Address(user=user, street='Fake', number=1, is_default=False)

    def test_sets_address_as_default_and_publishes_changes(self, mocker, address):
        mock_filter = mocker.patch.object(Address.objects, 'filter')
        mock_update = mocker.patch.object(mock_filter.return_value, 'update')
        mock_save = mocker.patch.object(address, 'save')
        mock_publish = mocker.patch.object(events, 'publish')

        address.set_default()

        # We lose the integration tests of the database flows
        mock_filter.assert_called_with(user=address.user)
        mock_update.assert_called_with(is_default=False)
        assert address.is_default == True
        mock_save.assert_called()
        mock_publish.assert_called_with(events.DEFAULT_ADDRESS_CHANGED, address=address)
```

Some important things to notice are:

* The model indeed contains the business action set_default.
* It has dependencies with other models (in this case itself).
* There are side-effects in the action inside the model, breaking the SRP.
* To achieve unit tests for our business logic we need to mock up all the dependencies. 

In the last point, we have something important to discuss. You can follow 2 approaches: do an integration test where you validate the business flow with all its dependencies or do a unit test mocking all the external calls.

The problem with the integration test is that you have to test the behaviour using a real database as all the dependencies will end using the ORM, slowing down your tests and not validating the logic flow independently of the dependencies. The problem with the unit test is that you lose the integration validation of database behaviours and you have to mock everything.

So let’s look to the same example but applying a business logic layer and abstracting the database interactions to a manager (low coupling and high cohesion):

```python
### managers.py
class AddressManager(models.Manager):

    # We use the manager as a data repository
    def set_default(self, address):
        self.filter(user=address.user).update(is_default=False)
        address.is_default = True
        address.save()


### models.py
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    is_default = models.BooleanField()

    @property
    def full_address(self):
        return f'{self.street}, {self.number}'

    objects = AddressManager()


### business_logic.py
### The business rule is simple and easily testeable
def set_default(address):
    Address.objects.set_default(address)
    events.publish(events.DEFAULT_ADDRESS_CHANGED, address=address)


### tests.py
@pytest.mark.django_db
class TestAddressManagerSetDefault:

    # We make integration tests for the manager to validate database behaviours
    def test_sets_address_as_default(self, saved_user):
        old_default_address = Address.objects.create(
            user=saved_user, street='Fake', number=1, is_default=True)
        address = Address.objects.create(
            user=saved_user, street='Fake', number=2, is_default=False)

        Address.objects.set_default(address)

        old_default_address.refresh_from_db()
        address.refresh_from_db()
        assert not old_default_address.is_default
        assert address.is_default


class TestSetDefault:

    @pytest.fixture
    def address(self, user):
        return Address(user=user, street='Fake', number=1, is_default=False)

    def test_sets_address_as_default_and_publishes_changes(self, mocker, address):
        # In this case a lot less dependencies
        mock_set_default = mocker.patch.object(Address.objects, 'set_default')
        mock_publish = mocker.patch.object(events, 'publish')

        set_default(address)

        # We test only the logic and forget about ORM interactions
        mock_set_default.assert_called_with(address)
        mock_publish.assert_called_with(events.DEFAULT_ADDRESS_CHANGED, address=address)
```

As you can see we have easier tests and more maintainable code. In this case, we implement unit tests for our business logic that are fast and validate its flow. And then integration tests for the manager that validate the data operations and its dependencies with the database.

The key in this structure is that our business logic is not aware of data integrity or how it is stored, that is the job of the managers. This way we can unit test every flow and leave the integrity checks for the integration tests of the data layer.
# Backend\Django\Good practices\002_Model_validation.md

### Model validation

Sources:
* https://github.com/HackSoftware/Django-Styleguide

#### clean and full_clean
Lets take a look at an example model:

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")
```

We are defining the model's clean method, because we want to make sure we get good data in our database.

Now, in order for the clean method to be called, someone must call full_clean on an instance of our model, before saving.

Our recommendation is to do that in the service, right before calling save:

```python
def course_create(*, name: str, start_date: date, end_date: date) -> Course:
    obj = Course(name=name, start_date=start_date, end_date=end_date)

    obj.full_clean()
    obj.save()

    return obj
```

This also plays well with Django admin, because the forms used there will trigger full_clean on the instance.

We have few general rules of thumb for when to add validation in the model's clean method:

* If we are validating based on multiple, non-relational fields, of the model.
* If the validation itself is simple enough. 

Validation should be moved to the service layer if:

* The validation logic is more complex.
* Spanning relations & fetching additional data is required.

It's OK to have validation both in clean and in the service, but we tend to move things in the service, if that's the case.

#### constraints

As proposed in this issue, if you can do validation using Django's constraints, then you should aim for that.

Less code to write, less to code to maintain, the database will take care of the data even if it's being inserted from a different place.

Lets look at an example!

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```

# Backend\Django\Good practices\003_Model_properties.md

### Model properties

Sources:
* https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#properties

Model properties are great way to quickly access a derived value from a model's instance.

For example, lets look at the has_started and has_finished properties of our Course model:

```python
from django.utils import timezone
from django.core.exceptions import ValidationError


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()
```

Those properties are handy, because we can now refer to them in serializers or use them in templates.

We have few general rules of thumb, for when to add properties to the model:

* If we need a simple derived value, based on non-relational model fields, add a @property for that.
* If the calculation of the derived value is simple enough.

Properties should be something else (service, selector, utility) in the following cases:

* If we need to span multiple relations or fetch additional data.
* If the calculation is more complex.

Keep in mind that those rules are vague, because context is quite often important. Use your best judgement!
# Backend\Django\Good practices\004_Model_methods.md

### Model methods

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#methods

Model methods are also very powerful tool, that can build on top of properties.

Lets see an example with the is_within(self, x) method:

```python
from django.core.exceptions import ValidationError
from django.utils import timezone


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()

    def is_within(self, x: date) -> bool:
        return self.start_date <= x <= self.end_date
```

is_within cannot be a property, because it requires an argument. So it's a method instead.

Another great way for using methods in models is using them for attribute setting, when setting one attribute must always be followed by setting another attribute with a derived value.

An example:

```python
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone


class Token(BaseModel):
    secret = models.CharField(max_length=255, unique=True)
    expiry = models.DateTimeField(blank=True, null=True)

    def set_new_secret(self):
        now = timezone.now()

        self.secret = get_random_string(255)
        self.expiry = now + settings.TOKEN_EXPIRY_TIMEDELTA

        return self
```

Now, we can safely call set_new_secret, that'll produce correct values for both secret and expiry.

We have few general rules of thumb, for when to add methods to the model:

* If we need a simple derived value, that requires arguments, based on non-relational model fields, add a method for that.
* If the calculation of the derived value is simple enough.
* If setting one attribute always requires setting values to other attributes, use a method for that.

Models should be something else (service, selector, utility) in the following cases:

* If we need to span multiple relations or fetch additional data.
* If the calculation is more complex.

Keep in mind that those rules are vague, because context is quite often important. Use your best judgement!
# Backend\Django\Good practices\005_Model_testing.md

### Model testing

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#testing

Models need to be tested only if there's something additional to them - like validation, properties or methods.

Here's an example:

```python
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from project.some_app.models import Course


class CourseTests(TestCase):
    def test_course_end_date_cannot_be_before_start_date(self):
        start_date = timezone.now()
        end_date = timezone.now() - timedelta(days=1)

        course = Course(start_date=start_date, end_date=end_date)

        with self.assertRaises(ValidationError):
            course.full_clean()
```

A few things to note here:

* We assert that a validation error is going to be raised if we call full_clean.
* We are not hitting the database at all, since there's no need for that. This can speed up certain tests.
# Backend\Django\Good practices\006_Service.md

### Service

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#services

#### What is Service?

Services are where business logic lives.

The service layer speaks the specific domain language of the software, can access the database & other resources & can interact with other parts of your system.

Here's a very simple diagram, positioning the service layer in our Django apps:

![](_images/006_Service.png)

A service can be:

* A simple function.
* A class.
* An entire module.
* Whatever makes sense in your case.

In most cases, a service can be simple function that:

* Lives in <your_app>/services.py module.
* Takes keyword-only arguments, unless it requires no or one argument.
* Is type-annotated (even if you are not using mypy at the moment).
* Interacts with the database, other resources & other parts of your system.
* Does business logic - from simple model creation to complex cross-cutting concerns, to calling external services & tasks.


# Backend\Django\Good practices\007_Service_examples.md

### Service examples

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#example---function-based-service


#### Example - function-based service

An example service that creates a user:

```python
def user_create(
    *,
    email: str,
    name: str
) -> User:
    user = User(email=email)
    user.full_clean()
    user.save()

    profile_create(user=user, name=name)
    confirmation_email_send(user=user)

    return user
```

As you can see, this service calls 2 other services - profile_create and confirmation_email_send.

In this example, everything related to the user creation is in one place and can be traced.

#### Example - class-based service

Additionally, we can have "class-based" services, which is a fancy way of saying - wrap the logic in a class.

Here's an example, taken straight from the Django Styleguide Example, related to file upload:

```python
### https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/services.py


class FileStandardUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates 2 different behaviors (create & update) under a namespace.

    Meaning, we use the class here for:

    1. The namespace
    2. The ability to reuse `_infer_file_name_and_type` (which can also be an util)
    """
    def __init__(self, user: BaseUser, file_obj):
        self.user = user
        self.file_obj = file_obj

    def _infer_file_name_and_type(self, file_name: str = "", file_type: str = "") -> Tuple[str, str]:
        file_name = file_name or self.file_obj.name

        if not file_type:
            guessed_file_type, encoding = mimetypes.guess_type(file_name)
            file_type = guessed_file_type or ""

        return file_name, file_type

    @transaction.atomic
    def create(self, file_name: str = "", file_type: str = "") -> File:
        _validate_file_size(self.file_obj)

        file_name, file_type = self._infer_file_name_and_type(file_name, file_type)

        obj = File(
            file=self.file_obj,
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            upload_finished_at=timezone.now()
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def update(self, file: File, file_name: str = "", file_type: str = "") -> File:
        _validate_file_size(self.file_obj)

        file_name, file_type = self._infer_file_name_and_type(file_name, file_type)

        file.file = self.file_obj
        file.original_file_name = file_name
        file.file_name = file_generate_name(file_name)
        file.file_type = file_type
        file.uploaded_by = self.user
        file.upload_finished_at = timezone.now()

        file.full_clean()
        file.save()

        return file
```

As stated in the comment, we are using this approach for 2 main reasons:

* Namespace. We have a single namespace for our create & update.
* Reuse of the _infer_file_name_and_type logic.

Here's how this service is used:
```python
### https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/apis.py

class FileDirectUploadApi(ApiAuthMixin, APIView):
    def post(self, request):
        service = FileDirectUploadService(
            user=request.user,
            file_obj=request.FILES["file"]
        )
        file = service.create()

        return Response(data={"id": file.id}, status=status.HTTP_201_CREATED)
```
And
```python
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    # ... other code here ...
    # https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/admin.py

    def save_model(self, request, obj, form, change):
        try:
            cleaned_data = form.cleaned_data

            service = FileDirectUploadService(
                file_obj=cleaned_data["file"],
                user=cleaned_data["uploaded_by"]
            )

            if change:
                service.update(file=obj)
            else:
                service.create()
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
```
# Backend\Django\Good practices\008_Service_naming_convention.md

### Service naming conventions

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#naming-convention

Naming convention depends on your taste. It pays off to have something consistent throughout a project.

If we take the example above, our service is named user_create. The pattern is - <entity>_<action>.

This is what we prefer in HackSoft's projects. This seems odd at first, but it has few nice features:

* Namespacing. It's easy to spot all services starting with user_ and it's a good idea to put them in a users.py module.
* Greppability. Or in other words, if you want to see all actions for a specific entity, just grep for user_.
# Backend\Django\Good practices\009_Service_modules.md

### Service naming conventions

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#modules

If you have a simple-enough Django app with a bunch of services, they can all live happily in the service.py module.

But when things get big, you might want to split services.py into a folder with sub-modules, depending on the different sub-domains that you are dealing with in your app.

For example, lets say we have an authentication app, where we have 1 sub-module in our services module, that deals with jwt, and one sub-module that deals with oauth.

The structure may look like this:

```
services
├── __init__.py
├── jwt.py
└── oauth.py
```
There are lots of flavors here:

* You can do the import-export dance in services/__init__.py, so you can import from project.authentication.services everywhere else
* You can create a folder-module, jwt/__init__.py, and put the code there.
* Basically, the structure is up to you. If you feel it's time to restructure and refactor - do so.

# Backend\Django\Good practices\010_Service_selectors.md

### Service - selectors

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#selectors

In most of our projects, we distinguish between "Pushing data to the database" and "Pulling data from the database":

* Services take care of the push.
* Selectors take care of the pull.
* Selectors can be viewed as a "sub-layer" to services, that's specialized in fetching data.

A selector follows the same rules as a service.

For example, in a module <your_app>/selectors.py, we can have the following:
```python
def user_list(*, fetched_by: User) -> Iterable[User]:
    user_ids = user_get_visible_for(user=fetched_by)

    query = Q(id__in=user_ids)

    return User.objects.filter(query)
```
As you can see, user_get_visible_for is another selector.

You can return querysets, or lists or whatever makes sense to your specific case.


# Backend\Django\Good practices\011_Service_testing.md

### Service - testing

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#testing-1

Since services hold our business logic, they are an ideal candidate for tests.

If you decide to cover the service layer with tests, we have few general rules of thumb to follow:

* The tests should cover the business logic in an exhaustive manner.
* The tests should hit the database - creating & reading from it.
* The tests should mock async task calls & everything that goes outside the project.

When creating the required state for a given test, one can use a combination of:

* Fakes (We recommend using faker)
* Other services, to create the required objects.
* Special test utility & helper methods.
* Factories (We recommend using factory_boy)
* Plain Model.objects.create() calls, if factories are not yet introduced in the project.
* Usually, whatever suits you better.

Let's take a look at our service from the example:
```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from project.payments.selectors import items_get_for_user
from project.payments.models import Item, Payment
from project.payments.tasks import payment_charge


@transaction.atomic
def item_buy(
    *,
    item: Item,
    user: User,
) -> Payment:
    if item in items_get_for_user(user=user):
        raise ValidationError(f'Item {item} already in {user} items.')

    payment = Payment(
        item=item,
        user=user,
        successful=False
    )
    payment.full_clean()
    payment.save()

    # Run the task once the transaction has commited,
    # guaranteeing the object has been created.
    transaction.on_commit(
        lambda: payment_charge.delay(payment_id=payment.id)
    )

    return payment
```
The service:

* Calls a selector for validation.
* Creates an object.
* Delays a task.

Those are our tests:
```python
from unittest.mock import patch, Mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.services import item_buy
from django_styleguide.payments.models import Payment, Item


class ItemBuyTests(TestCase):
    @patch('project.payments.services.items_get_for_user')
    def test_buying_item_that_is_already_bought_fails(
        self, items_get_for_user_mock: Mock
    ):
        """
        Since we already have tests for `items_get_for_user`,
        we can safely mock it here and give it a proper return value.
        """
        user = User(username='Test User')
        item = Item(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        items_get_for_user_mock.return_value = [item]

        with self.assertRaises(ValidationError):
            item_buy(user=user, item=item)

    @patch('project.payments.services.payment_charge.delay')
    def test_buying_item_creates_a_payment_and_calls_charge_task(
        self,
        payment_charge_mock: Mock
    ):
        # How we prepare our tests is a topic for a different discussion
        user = given_a_user(username="Test user")
        item = given_a_item(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        self.assertEqual(0, Payment.objects.count())

        payment = item_buy(user=user, item=item)

        self.assertEqual(1, Payment.objects.count())
        self.assertEqual(payment, Payment.objects.first())

        self.assertFalse(payment.successful)

        payment_charge_mock.assert_called_once()
```
# Backend\Django\Good practices\012_API_and_Serializers.md

### API and Serializers

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#apis--serializers

#### API

When using services & selectors, all of your APIs should look simple & identical.

When we are creating new APIs, we follow those general rules:

* Have 1 API per operation. This means, for CRUD on a model, having 4 APIs.
* Inherit from the most simple APIView or GenericAPIView.
* Avoid the more abstract classes, since they tend to manage things via serializers & we want to do that via services & selectors.
* Don't do business logic in your API.
* You can do object fetching / data manipulation in your APIs (potentially, you can extract that to somewhere else).
* If you are calling some_service in your API, you can extract object fetching / data manipulation to some_service_parse.
* Basically, keep the APIs as simple as possible. They are an interface towards your core business logic.

#### Serialization

When we are talking about APIs, we need a way to deal with data serialization - both incoming & outgoing data.

Here are our rules for API serialization:

* There should be a dedicated input serializer & a dedicated output serializer.
* Input serializer takes care of the data coming in.
* Output serializer takes care of the data coming out.
* In terms of serialization, Use whatever abstraction works for you.

In case you are using DRF's serializers, here are our rules:

* Serializer should be nested in the API and be named either InputSerializer or OutputSerializer.
* Our preference is for both serializers to inherit from the simpler Serializer and avoid using ModelSerializer
  * This is a matter of preference and choice. If ModelSerializer is working fine for you, use it.
* If you need a nested serializer, use the inline_serializer util.
* Reuse serializers as little as possible.
  * Reusing serializers may expose you to unexpected behavior, when something changes in the base serializers.

#### Naming convention

For our APIs we use the following naming convention: <Entity><Action>Api.

Here are few examples: UserCreateApi, UserSendResetPasswordApi, UserDeactivateApi, etc.
# Backend\Django\Good practices\013_API_List.md

### List API

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#list-apis

#### Plain

A dead-simple list API should look like that:

```python
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from styleguide_example.users.selectors import user_list
from styleguide_example.users.models import BaseUser


class UserListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        email = serializers.CharField()

    def get(self, request):
        users = user_list()

        data = self.OutputSerializer(users, many=True).data

        return Response(data)
```

#### Filters and pagination

At first glance, this is tricky, since our APIs are inheriting the plain APIView from DRF, while filtering and pagination are baked into the generic ones:

* DRF Filtering
* DRF Pagination

That's why, we take the following approach:

* Selectors take care of the actual filtering.
* APIs take care of filter parameter serialization.
* If you need some of the generic paginations, provided by DRF, the API should take care of that.
* If you need a different pagination, or you are implementing it yourself, either add a new layer to handle pagination or let the selector do that for you.

Let's look at the example, where we rely on pagination, provided by DRF:

```python
from rest_framework.views import APIView
from rest_framework import serializers

from styleguide_example.api.mixins import ApiErrorsMixin
from styleguide_example.api.pagination import get_paginated_response, LimitOffsetPagination

from styleguide_example.users.selectors import user_list
from styleguide_example.users.models import BaseUser


class UserListApi(ApiErrorsMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        # Important: If we use BooleanField, it will default to False
        is_admin = serializers.NullBooleanField(required=False)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        email = serializers.CharField()
        is_admin = serializers.BooleanField()

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self
        )
```

When we look at the API, we can identify few things:

* There's a FilterSerializer, which will take care of the query parameters. If we don't do this here, we'll have to do it elsewhere & DRF serializers are great at this job.
* We pass the filters to the user_list selector
* We use the get_paginated_response utility, to return a .. paginated response.

Now, let's look at the selector:

```python
import django_filters

from styleguide_example.users.models import BaseUser


class BaseUserFilter(django_filters.FilterSet):
    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'is_admin')


def user_list(*, filters=None):
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs
```

As you can see, we are leveraging the powerful django-filter library.

> 👀 The key thing here is that the selector is responsible for the filtering. You can always use something else, as a filtering abstraction. For most of the cases, django-filter is more than enough.

Finally, let's look at get_paginated_response:
```python
from rest_framework.response import Response


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)
```
This is basically a code, extracted from within DRF.

Same goes for the LimitOffsetPagination:

```python
from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data):
        return OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
```
What we basically did is reverse-engineered the generic APIs.

> 👀 Again, if you need something else for pagination, you can always implement it & use it in the same manner. There are cases, where the selector needs to take care of the pagination. We approach those cases the same way we approach filtering.
# Backend\Django\Good practices\014_API_Detail.md

### Detail API

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#detail-api

```python
class CourseDetailApi(SomeAuthenticationMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def get(self, request, course_id):
        course = course_get(id=course_id)

        serializer = self.OutputSerializer(course)

        return Response(serializer.data)
```
# Backend\Django\Good practices\015_API_Create.md

### Create API

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#create-api

```python
class CourseCreateApi(SomeAuthenticationMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
```
# Backend\Django\Good practices\016_API_Update.md

### Update API

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#update-api

```python
class CourseUpdateApi(SomeAuthenticationMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)

    def post(self, request, course_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_update(course_id=course_id, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
```
# Backend\Django\Good practices\017_Fetching_objects.md

### Fetching objects

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#update-api

When our APIs receive an object_id, the question that arises is: Where should we fetch that object?

We have several options:

* We can pass that object to a serializer, which has a PrimaryKeyRelatedField (or a SlugRelatedField for that matter)
* We can do some kind of object fetching in the API & pass the object to a service or a selector.
* We can pass the id to the service / selector and do the object fetching there.

What approach we take is a matter of project context & preference.

What we usually do is to fetch objects on the API level, using a special get_object util:

```python
def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
```
This is a very basic utility, that handles the exception and returns None instead.

Whatever you do, make sure to keep it consistent.

# Backend\Django\Good practices\018_Nested_serializers.md

### Nested serializers

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#nested-serializers

In case you need to use a nested serializer, you can do the following thing:

```python
class Serializer(serializers.Serializer):
    weeks = inline_serializer(many=True, fields={
        'id': serializers.IntegerField(),
        'number': serializers.IntegerField(),
    })
```

The implementation of inline_serializer can be found [here](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/api/utils.py), in the Styleguide-Example repo.

```python
from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    # Important note if you are using `drf-spectacular`
    # Please refer to the following issue:
    # https://github.com/HackSoftware/Django-Styleguide/issues/105#issuecomment-1669468898
    # Since you might need to use unique names (uuids) for each inline serializer
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
```
# Backend\Django\Good practices\019_Advanced_serialization.md

### Advanced serialization

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#advanced-serialization

Sometimes, the end result of an API can be quite complex. Sometimes, we want to optimize the queries that we do and the optimization itself can be quite complex.

Trying to stick with just an OutputSerializer in that case might limit our options.

In those cases, we can implement our output serialization as a function, and have the optimizations we need there, instead of having all the optimizations in the selector.

Lets take this API as an example:
```python
class SomeGenericFeedApi(BaseApi):
    def get(self, request):
        feed = some_feed_get(
            user=request.user,
        )

        data = some_feed_serialize(feed)

        return Response(data)
```
In this scenario, some_feed_get has the responsibility of returning a list of feed items (can be ORM objects, can be just IDs, can be whatever works for you).

And we want to push the complexity of serializing this feed, in an optimal manner, to the serializer function - some_feed_serialize.

This means we don't have to do any unnecessary prefetches & optimizations in some_feed_get.

Here's an example of some_feed_serialize:
```python
class FeedItemSerializer(serializers.Serializer):
    ... some fields here ...
    calculated_field = serializers.IntegerField(source="_calculated_field")


def some_feed_serialize(feed: List[FeedItem]):
    feed_ids = [feed_item.id for feed_item in feed]

    # Refetch items with more optimizations
    # Based on the relations that are going in
    objects = FeedItem.objects.select_related(
      # ... as complex as you want ...
    ).prefetch_related(
      # ... as complex as you want ...
    ).filter(
      id__in=feed_ids
    ).order_by(
      "-some_timestamp"
    )

    some_cache = get_some_cache(feed_ids)

    result = []

    for feed_item in objects:
        # An example, adding additional fields for the serializer
        # That are based on values outside of our current object
        # This may be some optimization to save queries
        feed_item._calculated_field = some_cache.get(feed_item.id)

        result.append(FeedItemSerializer(feed_item).data)

    return result
```
As you can see, this is a pretty generic example, but the idea is simple:

* Refetch your data, with the needed joins & prefetches.
* Fetch or build in-memory caches, that will save you queries for specific computed values.
* Return a result, that's ready to be an API response.

Even though this is labeled as "advanced serialization", the pattern is really powerful and can be used for all serializations.

Such serializer functions usually live in a serializers.py module, in the corresponding Django app.
# Backend\Django\Good practices\020_Urls.md

### Urls

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#urls

We usually organize our urls the same way we organize our APIs - 1 url per API, meaning 1 url per action.

A general rule of thumb is to split urls from different domains in their own domain_patterns list & include from urlpatterns.

Here's an example with the APIs from above:
```python
from django.urls import path, include

from project.education.apis import (
    CourseCreateApi,
    CourseUpdateApi,
    CourseListApi,
    CourseDetailApi,
    CourseSpecificActionApi,
)


course_patterns = [
    path('', CourseListApi.as_view(), name='list'),
    path('<int:course_id>/', CourseDetailApi.as_view(), name='detail'),
    path('create/', CourseCreateApi.as_view(), name='create'),
    path('<int:course_id>/update/', CourseUpdateApi.as_view(), name='update'),
    path(
        '<int:course_id>/specific-action/',
        CourseSpecificActionApi.as_view(),
        name='specific-action'
    ),
]

urlpatterns = [
    path('courses/', include((course_patterns, 'courses'))),
]
```
Splitting urls like that can give you the extra flexibility to move separate domain patterns to separate modules, especially for really big projects, where you'll often have merge conflicts in urls.py.

Now, if you like to see the entire url tree structure, you can do just that, by not extracting specific variables for the urls that you include.

Here's an example from our Django Styleguide Example:

```python
from django.urls import path, include

from styleguide_example.files.apis import (
    FileDirectUploadApi,

    FilePassThruUploadStartApi,
    FilePassThruUploadFinishApi,
    FilePassThruUploadLocalApi,
)


urlpatterns = [
    path(
        "upload/",
        include(([
            path(
                "direct/",
                FileDirectUploadApi.as_view(),
                name="direct"
            ),
            path(
                "pass-thru/",
                include(([
                    path(
                        "start/",
                        FilePassThruUploadStartApi.as_view(),
                        name="start"
                    ),
                    path(
                        "finish/",
                        FilePassThruUploadFinishApi.as_view(),
                        name="finish"
                    ),
                    path(
                        "local/<str:file_id>/",
                        FilePassThruUploadLocalApi.as_view(),
                        name="local"
                    )
                ], "pass-thru"))
            )
        ], "upload"))
    )
]
```
Some people prefer the first way of doing it, others prefer the visible tree-like structure. This is up to you & your team.


# Backend\Django\Good practices\021_Settings.md

### Settings

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#settings

#### Organization

When it comes to Django settings, we tend to follow the folder structure from cookiecutter-django, with few adjustments:

* We separate Django specific settings from other settings.
* Everything should be included in base.py.
    * There should be nothing that's only included in production.py.
    * Things that need to only work in production are controlled via environment variables.

Here's the folder structure of our Styleguide-Example project:

```
config
├── __init__.py
├── django
│   ├── __init__.py
│   ├── base.py
│   ├── local.py
│   ├── production.py
│   └── test.py
├── settings
│   ├── __init__.py
│   ├── celery.py
│   ├── cors.py
│   ├── sentry.py
│   └── sessions.py
├── urls.py
├── env.py
└── wsgi.py
├── asgi.py
```
In config/django, we put everything that's Django related:
* base.py contains most of the settings & imports everything else from config/settings
* production.py imports from base.py and then overwrites some specific settings for production.
* test.py imports from base.py and then overwrites some specific settings for running tests.
  * This should be used as the settings module in pytest.ini.
* local.py imports from base.py and can overwrite some specific settings for local development.
  * If you want to use that, point to local in manage.py. Otherwise stick with base.py

In config/settings, we put everything else:
* Celery configuration.
* 3rd party configurations.
* etc.

This gives you a nice separation of modules.

Additionally, we usually have config/env.py with the following code:

```python
import environ

env = environ.Env()
```

And then, whenever we need to read something from the environment, we import like that:

```python
from config.env import env
```

Usually, at the end of the base.py module, we import everything from config/settings:

```python
from config.settings.cors import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.sentry import *  # noqa
```

#### Prefixing environment variables with DJANGO_

In a lot of examples, you'll see that environment variables are usually prefixed with DJANGO_. This is very helpful when there are other applications alongside your Django app that run on the same environment. In that case, prefixing the environment variables with DJANGO_ helps you to differ which are the environment variables specific to your Django app.

In HackSoft we do not ususally have several apps running on the same environment. So, we tend to prefix with DJANGO_ only the Django specific environments & anything else.

For example, we would have DJANGO_SETTINGS_MODULE, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS, DJANGO_CORS_ORIGIN_WHITELIST prefixed. We would have AWS_SECRET_KEY, CELERY_BROKER_URL, EMAILS_ENABLED not prefixed.

This is mostly up to personal preference. Just make sure you are consistent with that.

#### Integrations

Since everything should be imported in base.py, but sometimes we don't want to configure a certain integration for local development, we derived the following approach:

* Integration-specific settings are placed in config/settings/some_integration.py
* There's always a boolean setting called USE_SOME_INTEGRATION, which reads from the environment & defaults to False.
* If the value is True, then proceed reading other settings & failing if things are not present in the environment.

For example, lets take a look at config/settings/sentry.py:
```python
from config.env import env

SENTRY_DSN = env('SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    # ... we proceed with sentry settings here ...
    # View the full file here - https://github.com/HackSoftware/Styleguide-Example/blob/master/config/settings/sentry.py
```

#### Reading from .env

Having a local .env is a nice way of providing values for your settings.

And the good thing is, django-environ provides you with a way to do that:
```python
### That's in the beginning of base.py

import os

from config.env import env, environ

### Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env.read_env(os.path.join(BASE_DIR, ".env"))
```
Now you can have a .env (but it's not required) file in your project root & place values for your settings there.

There are 2 things worth mentioning here:

* Don't put .env in your source control, since this will leak credentials.
* Rather put an .env.example with empty values for everything, so new developers can figure out what's being used.
# Backend\Django\Good practices\022_Error_and_exceptions.md

### Errors & Exception Handling

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#errors--exception-handling

> 👀 If you want the code, hop to the Styleguide-Example project - https://github.com/HackSoftware/Styleguide-Example/blob/master/styleguide_example/api/exception_handlers.py

Errors & exception handling is a big topic & quite often - the details are specific for a given project.

That's why we'll split things into two - general guidelines, followed by some specific approaches for error handling.

Our general guidelines are:

* Know how exception handling works (we'll give context for Django Rest Framework).
* Describe how your API errors are going to look like.
* Know how to change the default exception handling behavior.

Followed by some specific approaches:

* Use DRF's default exceptions, with very little modifications.
* HackSoft's proposed approach.

If you are looking for a standard way to structure your error responses, check RFC7807 - https://datatracker.ietf.org/doc/html/rfc7807

#### How exception handling works (in the context of DRF)

DRF has an excellent guide on how exceptions are being handled, so make sure to read it first - https://www.django-rest-framework.org/api-guide/exceptions/

![](_images/022_Error_and_exceptions.png)

Basically, if the exception handler cannot handle the given exception & returns None, this will result in an unhandled exception & a 500 Server Error. This is often good, because you won't be silencing errors, that you need to pay attention to.

##### DRF's ValidationError

For example, if we simply raise a rest_framework.exceptions.ValidationError like that:

```python
from rest_framework import exceptions


def some_service():
    raise ValidationError("Error message here.")
```

The response payload is going to look like this:

```python
["Some message"]
```

This looks strange, because if we do it like this:

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.ValidationError({"error": "Some message"})
```

The response payload is going to look like this:

```python
{
  "error": "Some message"
}
```

That's basically what we passed as the detail of the ValidationError. But it's a different data structure from the initial array.

Now, if we decide to raise another of the DRF's built-in exceptions:
```python
from rest_framework import exceptions


def some_service():
    raise exceptions.NotFound()
```
The response payload is going to look like this:

```python
{
  "detail": "Not found."
}
```
That's entirely different from what we saw as behavior from the ValidationError and this might cause problems.

So far, the default DRF behavior can get us:

* An array.
* A dictionary.
* A specific {"detail": "something"} result.

So if we need to use the default DRF behavior, we need to take care of this inconsistency.

##### Django's ValidationError

Now, DRF's default exception handling is not playing nice with Django's ValidationError.

This piece of code:
```python
from django.core.exceptions import ValidationError as DjangoValidationError


def some_service():
    raise DjangoValidationError("Some error message")
```
Will result in an unhandled exception, causing 500 Server Error.

This will also happen if this ValidationError comes from model validation, for example:

```python
def some_service():
    user = BaseUser()
    user.full_clean()  # Throws ValidationError
    user.save()
```
This will also result in 500 Server Error.

If we want to start handling this, as if it was rest_framework.exceptions.ValidationError, we need to roll-out our own custom exception handler:
```python
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework.serializers import as_serializer_error
from rest_framework import exceptions


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    return response
```
This is basically the default implementation, with the addition of this piece of code:

```python
if isinstance(exc, DjangoValidationError):
    exc = exceptions.ValidationError(as_serializer_error(exc))
```

Since we need to map between django.core.exceptions.ValidationError and rest_framework.exceptions.ValidationError, we are using DRF's as_serializer_error, which is used internally in the serializers, just for that.

With that, we can now have Django's ValidationError playing nice with DRF's exception handler.

#### Describe how your API errors are going to look like.

This is very important and should be done as early as possible in any given project.

This is basically agreeing upon what the interface of your API errors - How an error is going to look like as an API response?

This is very project specific, you can use some of the popular APIs for inspiration:

* Stripe - https://stripe.com/docs/api/errors

As an example, we might decide that our errors are going to look like this:
* 4** and 5** status codes for different types of errors.
* Each error will be a dictionary with a single message key, containing the error message.

```python
{
  "message": "Some error message here"
}
```
That's simple enough:

* 400 will be used for validation errors.
* 401 for auth errors.
* 403 for permission errors.
* 404 for not found errors.
* 429 for throttling errors.
* 500 for server errors (we need to be careful not to silence an exception causing 500 and always report that in services like Sentry)

Again, this is up to you & it's specific to the project.\

#### Know how to change the default exception handling behavior.
This is also important, because when you decide how your errors are going to look like, you need to implement this as custom exception handling.

We've already provided an example for that in the paragraph above, talking about Django's ValidationError.

We'll also provide additional examples in the sections below.

#### Approach 1 - Use DRF's default exceptions, with very little modifications.

DRF's error handling is good. It'd be great, if the end result was always consistent. Those are the little modifications that we are going to do.

We want to end up with errors, always looking like that:
```python
{
  "detail": "Some error"
}
```
```python
{
  "detail": ["Some error", "Another error"]
}
```
```python
{
  "detail": { "key": "... some arbitrary nested structure ..." }
}
```
Basically, make sure we always have a dictionary with a detail key.

Additonally, we want to handle Django's ValidationError as well.

In order to achieve that, this is how our custom exception handler is going to look like:
```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error


def drf_default_with_modifications_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    return response
```
We kind-of replicate the original exception handler, so we can deal with an APIException after that (looking for detail).

Now, lets run a set of tests:

Code:
```python
def some_service():
    raise DjangoValidationError("Some error message")
```
Response:
```python
{
  "detail": {
    "non_field_errors": ["Some error message"]
  }
}
```
---
Code:
```python
from django.core.exceptions import PermissionDenied

def some_service():
    raise PermissionDenied()
```
Response:
```python
{
  "detail": "You do not have permission to perform this action."
}
```
---
Code:
```python
from django.http import Http404

def some_service():
    raise Http404()
```
Response:
```python
{
  "detail": "Not found."
}
```
---
Code:
```python
def some_service():
    raise RestValidationError("Some error message")
```
Response:
```python
{
  "detail": ["Some error message"]
}
```
---
Code:
```python
def some_service():
    raise RestValidationError(detail={"error": "Some error message"})
```
Response:
```python
{
  "detail": {
    "error": "Some error message"
  }
}
```
---
Code:
```python
class NestedSerializer(serializers.Serializer):
    bar = serializers.CharField()


class PlainSerializer(serializers.Serializer):
    foo = serializers.CharField()
    email = serializers.EmailField(min_length=200)

    nested = NestedSerializer()


def some_service():
    serializer = PlainSerializer(data={
        "email": "foo",
        "nested": {}
    })
    serializer.is_valid(raise_exception=True)
```
Response:
```python
{
  "detail": {
    "foo": ["This field is required."],
    "email": [
      "Ensure this field has at least 200 characters.",
      "Enter a valid email address."
    ],
    "nested": {
      "bar": ["This field is required."]
    }
  }
}
```
---
Code:
```python
from rest_framework import exceptions


def some_service():
    raise exceptions.Throttled()
```
Response:
```python
{
  "detail": "Request was throttled."
}
```
#### Approach 2 - HackSoft's proposed way
We are going to propose an approach, that can be easily extended into something that works well for you.

Here are the key ideas:

* Your application will have its own hierarchy of exceptions, that are going to be thrown by the business logic.
* Lets say, for simplicity, that we are going to have only 1 error - ApplicationError.
  * This is going to be defined in a special core app, within exceptions module. Basically, having project.core.exceptions.ApplicationError.
* We want to let DRF handle everything else, by default.
* ValidationError is now special and it's going to be handled differently.
  * ValidationError should only come from either serializer or a model validation.
---
We are going to define the following structure for our errors:

```python
{
  "message": "The error message here",
  "extra": {}
}
```
The extra key can hold arbitrary data, for the purposes of passing information to the frontend.

For example, whenever we have a ValidationError (usually coming from a Serializer or a Model), we are going to present the error like that:
```python
{
  "message": "Validation error.",
  "extra": {
    "fields": {
      "password": ["This field cannot be blank."],
      "email": ["This field cannot be blank."]
    }
  }
}
```
This can be communicated with the frontend, so they can look for extra.fields, to present those specific errors to the user.

In order to achieve that, the custom exception handler is going to look like this:
```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response

from styleguide_example.core.exceptions import ApplicationError


def hacksoft_proposed_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=400)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
```
Take a look at that code & try to understand what's going on. The strategy is - reuse as much as possible from DRF & then adjust.

Now, we are going to have the following behavior:

Code:
```python
from styleguide_example.core.exceptions import ApplicationError


def trigger_application_error():
    raise ApplicationError(message="Something is not correct", extra={"type": "RANDOM"})
```
Response:
```python
{
  "message": "Something is not correct",
  "extra": {
    "type": "RANDOM"
  }
}
```
Now, this can be extended & made to better suit your needs:

* You can have ApplicationValidationError and ApplicationPermissionError, as an additional hierarchy.
* You can reimplement DRF's default exception handler, instead of reusing it (copy-paste it & adjust to your needs).

The general idea is - figure out what kind of error handling you need and then implement it accordingly.

As you can see, we can mold exception handling to our needs.

You can start handling more stuff - for example - translating django.core.exceptions.ObjectDoesNotExist to rest_framework.exceptions.NotFound.

You can even handle all exceptions, but then, you should be sure those exceptions are being logged properly, otherwise you might silence something that's important.
# Backend\Django\Good practices\023_Testing.md

### Testing

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#testing-2

#### Organization

In our Django projects, we split our tests depending on the type of code they represent.

Meaning, we generally have tests for models, services, selectors & APIs / views.

The file structure usually looks like this:
```
project_name
├── app_name
│   ├── __init__.py
│   └── tests
│       ├── __init__.py
│       ├── factories.py
│       ├── models
│       │   └── __init__.py
│       │   └── test_some_model_name.py
│       ├── selectors
│       │   └── __init__.py
│       │   └── test_some_selector_name.py
│       └── services
│           ├── __init__.py
│           └── test_some_service_name.py
└── __init__.py
```

#### Naming conventions
We follow 2 general naming conventions:

* The test file names should be ```test_the_name_of_the_thing_that_is_tested.py```
* The test case should be `class TheNameOfTheThingThatIsTestedTests(TestCase):`

For example, if we have:
```python
def a_very_neat_service(*args, **kwargs):
    pass
```
We are going to have the following for file name:
```python
project_name/app_name/tests/services/test_a_very_neat_service.py
```
And the following for test case:
```python
class AVeryNeatServiceTests(TestCase):
    pass
```
For tests of utility functions, we follow a similar pattern.

For example, if we have `project_name/common/utils.py`, then we are going to have `project_name/common/tests/test_utils.py` and place different test cases in that file.

If we are to split the utils.py module into submodules, the same will happen for the tests:
* project_name/common/utils/files.py
* project_name/common/tests/utils/test_files.py
We try to match the structure of our modules with the structure of their respective tests.
# Backend\Django\Good practices\024_Celery.md

### Celery

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#celery

We use Celery for the following general cases:

* Communicating with 3rd party services (sending emails, notifications, etc.)
* Offloading heavier computational tasks outside the HTTP cycle.
* Periodic tasks (using Celery beat)

#### Basics
We try to treat Celery as if it's just another interface to our core logic - meaning - don't put business logic there.

```python
from django.db import transaction
from django.core.mail import EmailMultiAlternatives

from styleguide_example.core.exceptions import ApplicationError
from styleguide_example.common.services import model_update
from styleguide_example.emails.models import Email


@transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email.status}")

    subject = email.subject
    from_email = "styleguide-example@hacksoft.io"
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={
            "status": Email.Status.SENT,
            "sent_at": timezone.now()
        }
    )
    return email
```
Email sending has business logic around it, but we still want to trigger this particular service from a task.

Our task looks like that:
```python
from celery import shared_task

from styleguide_example.emails.models import Email


@shared_task
def email_send(email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send
    email_send(email)
```
As you can see, we treat the task as an API:

1. Fetch the required data. 
2. Call the appropriate service.

Now, imagine we have a different service, that triggers the email sending.

It may look like that:
```python
from django.db import transaction

### ... more imports here ...

from styleguide_example.emails.tasks import email_send as email_send_task


@transaction.atomic
def user_complete_onboarding(user: User) -> User:
    # ... some code here

    email = email_get_onboarding_template(user=user)

    transaction.on_commit(lambda: email_send_task.delay(email.id))

    return user
```
2 important things to point out here:

* We are importing the task (which has the same name as the service), but we are giving it a _task suffix.
* And when the transaction commits, we'll call the task.

So, in general, the way we use Celery can be described as:

* Tasks call services.
* We import the service in the function body of the task.
* When we want to trigger a task, we import the task, at module level, giving the _task suffix.
* We execute tasks, as a side effect, whenever our transaction commits.

#### Error handling

Sometimes, our service can fail and we might want to handle the error on the task level. For example - we might want to retry the task.

This error handling code needs to live in the task.

Lets expand the email_send task example from above, by adding error handling:
```python
from celery import shared_task
from celery.utils.log import get_task_logger

from styleguide_example.emails.models import Email


logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_failed

    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send

    try:
        email_send(email)
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
```
As you can see, we do a bunch of retries and if all of them fail, we handle this in the on_failure callback.

The callback follows the naming pattern of _{task_name}_failure and it calls the service layer, just like an ordinary task.

#### Structure
Tasks are located in tasks.py modules in different apps.

We follow the same rules as with everything else (APIs, services, selectors): if the tasks for a given app grow too big, split them by domain.

Meaning, you can end up with tasks/domain_a.py and tasks/domain_b.py. All you need to do is import them in tasks/__init__.py for Celery to autodiscover them.

The general rule of thumb is - split your tasks in a way that'll make sense to you.

#### Periodic tasks
Managing periodic tasks is quite important, especially when you have tens or hundreds of them.

We use Celery Beat + django_celery_beat.schedulers:DatabaseScheduler + django-celery-beat for our periodic tasks.

The extra thing that we do is to have a management command, called setup_periodic_tasks, which holds the definition of all periodic tasks within the system. This command is located in the tasks app, discussed above.

Here's how project.tasks.management.commands.setup_periodic_tasks.py looks like:
```python
from django.core.management.base import BaseCommand
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from project.app.tasks import some_periodic_task


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {some_periodic_task.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Deleting all periodic tasks and schedules...\n')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                'task': some_periodic_task
                'name': 'Do some peridoic stuff',
                # https://crontab.guru/#15_*_*_*_*
                'cron': {
                    'minute': '15',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **periodic_task['cron']
            )

            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled']
            )
```
Few key things:

* We use this task as part of a deploy procedure.
* We always put a link to crontab.guru to explain the cron. Otherwise it's unreadable.
* Everything is in one place.
* ⚠️ We use, almost exclusively, a cron schedule. If you plan on using the other schedule objects, provided by Celery, please read thru their documentation & the important notes - https://django-celery-beat.readthedocs.io/en/latest/#example-creating-interval-based-periodic-task - about pointing to the same schedule object. ⚠️
# Backend\Django\Good practices\025_Model_update_cookbook.md

### Model update cookbook

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#cookbook

As for updating, we have a generic update service that we use inside of the actual update services. Here's what a sample user_update service would look like:
```python
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ['first_name', 'last_name']

    user, has_updated = model_update(
        instance=user,
        fields=non_side_effect_fields,
        data=data
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
```
* We're calling the generic model_update service for the fields that have no side-effects related to them (meaning that they're just set to the value that we provide).
* This pattern allows us to extract the repetitive field setting in a generic service and perform only the specific tasks inside of the update service (side-effects).
* We can be smart & provide the update_fields kwarg, when saving the instance. This way, in the UPDATE query, we'll only send values that are actually updated.

The full implementations of these services can be found in our example project:
* [model_update](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/services.py)
* [user_update](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/users/services.py)

If you are going to include model_update in your project, make sure to read the [tests](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/tests/services/test_model_update.py) & include them too!


# Backend\Django\Logging\001_Loggers.md

### Loggers

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

Loggers are basically the entry point of the logging system. This is what you'll actually work with as a developers.

When a message is received by the logger, the log level is compared to the log level of the logger. If it is the same or exceeds the log level of the logger, the message is sent to the handler for further processing. The log levels are:

* DEBUG: Low-level system information
* INFO: General system information
* WARNING: Minor problems related information
* ERROR: Major problems related information
* CRITICAL: Critical problems related information

# Backend\Django\Logging\002_Handlers.md

### Handlers

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

Handlers basically determine what happens to each message in a logger. It has log levels the same as Loggers. But, we can essentially define what way we want to handle each log level.

For example: ERROR log level messages can be sent in real-time to the developer, while INFO log levels can just be stored in a system file.

It essentially tells the system what to do with the message like writing it on the screen, a file, or to a network socket
# Backend\Django\Logging\003_Filters.md

### Filters

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

A filter can sit between a Logger and a Handler. It can be used to filter the log record.

For example: in CRITICAL messages, you can set a filter which only allows a particular source to be processed.
# Backend\Django\Logging\004_Formatters.md

### Formatters

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

As the name suggests, formatters describe the format of the text which will be rendered.


# Backend\Django\Logging\005_Setup.md

### Logging setup

Source: https://www.freecodecamp.org/news/logging-in-python-debug-your-django-projects/

#### settings.py

```python
### settings.py

LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'warning.log',
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
       # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['file'], # notice how file variable is called in handler which has been defined above
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

When `propagate` is set as True, a child will propagate all their logging calls to the parent. This means that we can define a handler at the root (parent) of the logger tree and all logging calls in the subtree (child) go to the handler defined in the parent.

#### Using logger

```python

from django.http import HttpResponse
import datetime
### import the logging library
import logging
### Get an instance of a logger
logger = logging.getLogger(__name__)

def hello_reader(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Hello FreeCodeCamp.org Reader :)</h1>")

```

# Backend\Django\ORM\001_F.md

### F()

Source: https://pogromcykodu.pl/django-orm-w-akcji-wyrazenie-f/

F() enables to access database field of given model and perform additional operations on numbers.

#### Where to use it?

* update(), 
* create(), 
* filter(), 
* order_by(), 
* annotate(),
* aggregate()

F() enables to perform arithmetic operations on database objects, like:

```python
increase_value = 1.15
Employee.objects.update(salary=F("salary") * increase_value) 
```

```python
Employee.objects.annotate(earnings=F("salary") + F("bonus")) 
```

#### Example - increasing every Employee salary by 100 PLN
```python
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    bonus = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    employment_date = models.DateField()
    position = models.CharField(max_length=50) 
```
* Method 1 - **NOT EFFICIENT**

```python
from employees.models import Employee

employees = Employee.objects.all()
for employee in employees:
    employee.salary += 100
    employee.save() 
```

This will make single database query for every single employee.

* Method 2 - **MORE EFFICIENT**

```python
from django.db.models import F
from employees.models import Employee

Employee.objects.update(salary = F("salary") + 100) 
```

This will make single query do database to update all Employees.
# Backend\Django\ORM\002_Concat.md

### Concat()

Source: https://pogromcykodu.pl/django-orm-w-akcji-wyrazenie-f/

#### Joining same Field types

```python
from django.db.models import F, Value
from django.db.models.functions import Concat
from employees.models import Employee

employees = Employee.objects.annotate(position_extra=Concat(Value("Senior "), F("position"))).all()

print(employees[0].position) # Developer
print(employees[0].position_extra) # Senior Developer 
```

> String values have to be "packed" with Value() to properly perform database operations.

#### Joining CharField and TextField with Concat()

To join CharField and TextField it's needed to provide **output_field**, to specify which type of field we need to return.

```python
### first_name -> CharField, 
### last_name -> TextField

employees = Employee.objects.annotate(full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())).all()
print(employees[0].first_name) # Jan
print(employees[0].last_name) # Kowalski
print(employees[0].full_name) # Jan Kowalski 
```

# Backend\Django\ORM\003_Custom_Managers.md

### Custom Managers

Source: https://pogromcykodu.pl/masz-dosc-powtarzajacych-sie-warunkow-zapytan-django-manager-rozwiaze-twoj-problem/

#### CustomManager

```python
from django.db import models

    
class ArticleManager(models.Manager): 
    def get_published(self): 
        return self.filter(published=True) 
    
    def get_archived(self): 
        return self.filter(archived=True) 

class Article(models.Model): 
    title = models.CharField(max_length=30) 
    published = models.BooleanField(default=False) 
    archived = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True) 

    objects = ArticleManager()  
```

From now on, calling `Article.objects.get_published()` will return only published Articles. Other QuerySet operations like `.exclude` can be performed.
```python
Article.objects.get_published().exclude(title__startswith='H') 
```

#### Custom Manager with custom QuerySet

```python
from django.db import models

### Filtering objects directly on QuerySet
class ArticleQuerySet(models.QuerySet):
    def get_published(self):
        return self.filter(published=True)
    def get_archived(self):
        return self.filter(archived=True)

### Using custom Queryset in Custom manager.
class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)
    def get_published(self):
        return self.get_queryset().get_published()
    def get_archived(self):
        return self.get_queryset().get_archived()
    
class Article(models.Model):
    title = models.CharField(max_length=30)
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = ArticleManager()
```

Such composition enables to chain custom commands on QuerySets returned by Manager, like `Article.objects.get_published().get_archived()`

# Backend\Django\ORM\004_Abstract_models.md

### Abstract models

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0


Abstract models are a fantastic way to encapsulate common information and behavior. An abstract model isn’t represented by any database table; instead, its fields and methods are inherited by subclasses.

Example:

```python
class BaseProfile(models.Model):
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')
    
    class Meta:
        abstract = True

class StudentProfile(BaseProfile):
    graduation_year = models.IntegerField()
    

class TeacherProfile(BaseProfile):
    office = models.CharField(max_length=100)
```
Here, BaseProfile serves as a template. StudentProfile and TeacherProfile will both have bio and avatar fields, but they are stored in separate database tables with their specific fields.
# Backend\Django\ORM\005_Proxy_models.md

### Proxy models

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0

Proxy models are used to change the behavior of a model, like the default ordering or the default manager, without creating a new database table.

Example:
```python
class OrderedProfile(Profile):
    class Meta:
        proxy = True
        ordering = ['name']

### Usage:
ordered_profiles = OrderedProfile.objects.all()

```

This proxy model will show all profiles ordered by name.
# Backend\Django\ORM\006_Multitable_inheritance.md

### Multitable inheritance

Source: https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0

This type of inheritance is used when each model in the hierarchy is considered a full entity on its own, potentially linked to a physical database table.

Example:
```python
class Place(models.Model):
    name = models.CharField(max_length=50)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)
```



Here, Restaurant is a type of Place and has its own table with a link to Place.
# Backend\Django\ORM\007_Indexes.md

### Indexes

Source: https://medium.com/@sandesh.thakar18/types-of-database-indexing-in-django-5d31581fec67

#### Unique Index
A unique index ensures that no two rows in a table have the same values for the indexed columns. In Django, this can be achieved by adding the unique=True attribute to a field in the model. For example:

```python
class MyModel(models.Model):
  email = models.EmailField(unique=True)
```

#### Primary Key Index
Every Django model has a primary key field, which is automatically created and added to the model by default. This field is used to uniquely identify each row in the table and is indexed for fast lookups. The primary key index is created automatically and cannot be removed.

#### Regular Index
A regular index is used to improve the performance of queries that use the indexed columns. In Django, this can be achieved by adding the db_index=True attribute to a field in the model. For example:
```python
class MyModel(models.Model):
    name = models.CharField(max_length=100, db_index=True)
```

#### Multi-column index
A multi-column index is used when you want to index multiple fields in your model. This is useful when you often query your data based on multiple fields at the same time. In Django, this can be achieved by creating an index on multiple fields using the Index class. For example:
```python
from django.db import models

class MyModel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]
```
#### Partial Index
A partial index is a type of index that is created on a subset of a table’s rows, rather than the entire table. This can be useful when you want to improve the performance of queries that filter on specific values in a column.

In Django, partial indexes can be created using the Index class and the condition parameter. The condition parameter is used to specify a condition that must be met in order for a row to be included in the index.

For example, let’s say you have a model with a published field that is a boolean indicating whether an article has been published or not. If you often query for published articles and rarely for unpublished articles, you could create a partial index on the published field like this:
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    published = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['published'], name='published_idx', condition=Q(published=True))
        ]
```

This will create an index on the published field, but only for rows where the published field is True. This can improve the performance of queries that filter on published articles without affecting write performance or consuming unnecessary resources.

It’s worth noting that creating partial indexes can be beneficial when you have a specific use case, but it’s important to consider the trade-offs of each type of index in order to achieve the best performance for your application.

It’s worth noting that indexes are not always necessary and can sometimes slow down write operations. It’s important to consider the balance between read and write performance when deciding which fields to index. Additionally, it’s important to keep in mind that each index consumes disk space and memory and can slow down your database.

In conclusion, indexes are an important tool for optimizing the performance of Django’s database operations. The different types of indexes allow you to index fields in different ways, depending on the use case. It’s important to use them judiciously and consider the trade-offs of each type of index in order to achieve the best performance for your application.
# Backend\Django\ORM\008_Atomic_transactions.md

### Atomic transactions

Sources: 
* https://www.reddit.com/r/django/comments/ypw0mg/can_somebody_explain_when_to_use_transaction/
* https://plainenglish.io/blog/understanding-djangos-transaction-atomic

#### transaction.atomic

Before diving into transaction atomic, let’s understand the concept of transactions. In a database context, a transaction represents a logical unit of work that either succeeds as a whole or fails completely, ensuring data consistency. A transaction typically consists of multiple database operations, such as inserts, updates, and deletions.

Atomic transactions are about ensuring data consistency in your database.

So say you had 2 models, and a view that populated a record in both
```python
Model1.objects.create(...)
Model2.objects.create(...)
```

Say Model1 finished saving, then your application crashed. If the fact that the Model2 record is missing will lead to inconsistent/wrong results in your db then you want to save both record in 1 transaction
```python
with transaction.atomic():
  Model1.objects.create(...)
  Model2.objects.create(...)
```

With this, you are guaranteed to have either both, or no records saved.

"Inconsistent" is up to you to define. Relational schemas can only model your data to a certain extent, at some point you need guarantees about the data in your columns. When that data is "off" is a good definition of inconsistent.

During the execution of a transaction, two critical concepts come into play: commit and rollback. A commit operation signifies that the transaction is successful, and all changes made within the transaction are permanently saved to the database. On the other hand, a rollback operation discards any changes made within the transaction and reverts the database to its state before the transaction begins.

#### select_for_update

Django’s transaction atomic already provides a basic level of concurrency control by using the transaction.atomic block. However, it doesn't handle concurrent updates outside of the transaction scope.

To implement more advanced locking mechanisms, you can use the select_for_update() method in Django's querysets.

```python
from django.db import transaction, models

def transfer(self, request):
    try:
        user_a = request.POST.get("user_a")
        user_b = request.POST.get("user_b")
        amount = request.POST.get("amount")

        with transaction.atomic():
            user_a_obj = Account.objects.select_for_update().get(user=user_a)
            user_a_obj.balance -= int(amount)
            user_a_obj.save()

            user_b_obj = Account.objects.select_for_update().get(user=user_b)
            user_b_obj.balance += int(amount)
            user_b_obj.save()

            return Response(
                {"status": "success", "message": "Your amount is transfered."}
            )

    except Exception as e:
        print(e)
        return Response({"status": "failed", "message": "Something went wrong."})
```

The select_for_update() method is called on the querysets for user_one_obj and user_two_obj. This method locks the selected rows in the database, preventing other transactions from modifying them until the current transaction is completed.

#### Bulk inserting

Here’s an example of how to perform a bulk insert using Django’s transaction atomic feature with the Product model:

```python
from django.db import transaction

### Assume you have a list of products to insert
products_data = [
    {'name': 'Product 1', 'sku': 'SKU1', 'price': 10.99},
    {'name': 'Product 2', 'sku': 'SKU2', 'price': 19.99},
    {'name': 'Product 3', 'sku': 'SKU3', 'price': 14.99},
    # Add more products as needed
]

@transaction.atomic
def create_products(products_data):
    # Create a list to hold the Product objects
    products = []

    try:
        # Iterate over the products_data list
        for data in products_data:
            product = Product(name=data['name'], sku=data['sku'], price=data['price'])
            products.append(product)

        # Use the bulk_create method to insert the products in a single query
        Product.objects.bulk_create(products)

        # Transaction will be committed automatically if no exceptions occur
    except Exception as e:
        # Handle any exceptions that occur during the bulk creation process
        print(f"Error occurred: {e}")
        # Raise an exception to trigger a rollback
```

Here, we decorate the function with the transaction.atomic decorator to ensure the entire bulk insert operation is treated as an atomic transaction.

After iterating over all the data, we use the bulk_create method of the Product.objects manager to insert all the Product objects in a single query, improving performance compared to individual save() calls.

If any exception occurs during the bulk creation process, we catch it and handle it accordingly. By raising an exception, the transaction will be rolled back, and no changes will persist in the database. If no exceptions occur, the transaction will be committed automatically, and all the products will be inserted into the database.
# Backend\Django\ORM\009_Proxy_models.md

### Proxy models

Source: https://medium.com/django-unleashed/proxy-models-in-django-a-powerful-tool-for-efficient-entity-management-cf9f4fe18bbc

#### Usage example

```python
from django.db import models

class BaseUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Admin(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        kwargs['is_admin'] = True
        return super().save(*args, **kwargs)

    objects = models.Manager().filter(is_admin=True)  # Default manager for regular queries

class Customer(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        kwargs['is_customer'] = True
        return super().save(*args, **kwargs)

    objects = models.Manager().filter(is_customer=True)  # Default manager
    recent_customers = models.Manager().filter(is_customer=True).order_by('-date_joined')[:5]  # Custom queryset for recent customers


admin = Admin(
  username='admin', first_name='Hardik', last_name='Patel', email='hnmpatel@live.com'
)
admin.save() # Overridden save function will add admin related attributes to object
customer = Customer(
  username='customer', first_name='Test', last_name='Last', email='test@last.com'
)
customer.save() # Overridden save function will add customer related attributes to object
```
# Backend\Django\ORM\010_Contraints.md

### Constraints

Sources:
* https://adamj.eu/tech/2020/03/10/django-check-constraints-sum-percentage-fields/
* https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/
* https://adamj.eu/tech/2020/03/25/django-check-constraints-one-field-set/
* https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/

#### Fields calculation constraint

```python
from django.db import models


class Book(models.Model):
    percent_read = models.PositiveIntegerField()
    percent_unread = models.PositiveIntegerField()
    percent_ignored = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} - {self.percent_read}% read"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    percent_read=(
                        100 - models.F("percent_unread") - models.F("percent_ignored")
                    )
                ),
                name="%(app_label)s_%(class)s_percentages_sum_100",
            )
        ]
```
#### Choice field constraint

Django’s model validation is designed mostly for forms. It trusts that other code paths in your application “know what they’re doing.”

```python
from django.db import models


class Status(models.TextChoices):
    UNPUBLISHED = "UN", "Unpublished"
    PUBLISHED = "PB", "Published"


class Book(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.UNPUBLISHED,
    )

    def __str__(self):
        return f"{self.id} - {Status(self.status).label}"
```

For Book class above we can save item in database with status other than declared in choices:
```python
book = Book.objects.get(id=1)
book.status = 'republished'
book.save()
```
or
```python
Book.objects.update(status="republished")
```

To prevent that, use contraints:
```python
class Book(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.UNPUBLISHED,
    )

    def __str__(self):
        return f"{self.id} - {Status(self.status).label}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=Status.values),
            )
        ]
```

#### One of fields filled constraint

To make sure that only one field has a value, when other one is Null use constraint as below.

```python
from django.db import models


class ScoreType(models.IntegerChoices):
    POINTS = 1, "Points"
    DURATION = 2, "Duration"


class Score(models.Model):
    type = models.IntegerField(choices=ScoreType.choices)
    value_points = models.IntegerField(null=True)
    value_duration = models.DurationField(null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_value_matches_type",
                check=(
                    models.Q(
                        type=ScoreType.POINTS,
                        value_points__isnull=False,
                        value_duration__isnull=True,
                    )
                    | models.Q(
                        type=ScoreType.DURATION,
                        value_points__isnull=True,
                        value_duration__isnull=False,
                    )
                ),
            )
        ]
```
You can also combine this with proxy models to split Scores based on type. 
```python
class PointsScoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=ScoreType.POINTS)


class PointsScore(Score):
    objects = PointsScoreManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ScoreType.POINTS

    class Meta:
        proxy = True
```

#### Many-to-many field constraint

##### Follow mechanism

Imagine we have a user model that we’d like to introduce a social media “following” pattern to. Users can follow other users to receive updates on our site. We’d like to ensure that users do not follow themselves, since that would need special care in all our code.

To add the followers relationship, we’ll be using ManyToManyField. By default, ManyToManyField creates a hidden model class to hold the relationships. Because we want to customize our model with add an extra constraint, we’ll need to use the through argument to define our own visible model class instead.

```python
from django.db import models


class User(models.Model):
    ...
    followers = models.ManyToManyField(
        to="self",
        through="Follow",
        related_name="following",
        symmetrical=False,
    )


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["from_user", "to_user"],
            ),
        ]
```
Note:

* We use to="self" to define that the relationship is from User to itself. Django calls this a recursive relationship.
* We use the string format of through, because we’re defining User before Follow. We could define Follow first, but then we’d need to use strings to specify User in its definition.
* We declare the relationship as asymmetrical with symmetrical=False. If Alice follows Bob, it does not mean Bob follows Alice. If our relationship was a mutual “friend request” style, we would instead make the relationship symmetrical.
* The Follow class uses two foreign keys to link up the related users. ManyToManyField will automatically use the first foreign key as the “source” of the relationship and the other as the destination. It’s possible Follow could have a third foreign key to User, for example to track another user who suggested the follow. In this case, we’d need to use ManyToManyField.through_fields to specify which foreign keys actually form the relationship.

* We have already added a constraint to the model - a UniqueConstraint to ensure that exactly one relationship exists between users. Without this, multiple follows could exist between e.g. Alice and Bob, and it would be confusing what that means. This is copying what Django’s default hidden through model.

* We use string interpolation in our constraint’s name to namespace it to our model. This prevents naming collisions with constraints on other models. Databases have only one namespace for constraints across all tables, so we need to be careful.

##### Preventing self follow

```python
class Follow(models.Model):
    ...

    class Meta:
        constraints = [
            ...,
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        ]
```
# Backend\Django\ORM\011_Custom_migrations.md

### Custom migrations

Source: https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/

```python
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Follow = apps.get_model("core", "Follow")
    db_alias = schema_editor.connection.alias
    Follow.objects.using(db_alias).filter(from_user=models.F("to_user")).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_auto_20210225_0320"),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_func,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.CheckConstraint(
                check=models.Q(_negated=True, from_user=models.F("to_user")),
                name="core_follow_prevent_self_follow",
            ),
        ),
    ]
```

* We use the same template for `forwards_func` as in the RunPython [documentation](https://docs.djangoproject.com/en/stable/ref/migration-operations/#django.db.migrations.operations.RunPython).
* We fetch the point-in-history version of the `Follow` model through `apps.get_model()`, rather than importing the latest version. Using the latest version would fail since it could reference fields that haven’t been added to the database yet.
* We also use the current database alias. It’s best to this even if our project only uses a single database, in case it gains multiple in the future.
* We declare `reverse_code` as a no-op, so that this migration is reversible. Reversing the migration won’t be able to restore deleted self-follow relationships because we aren’t backing them up anywhere.
* We declare the operation as elidable. This means Django can drop the operation when squashing the migration history. This is always worth considering when writing a `RunPython` or `RunSQL` operation, as it helps you make smaller, faster squashes.
# Backend\Django\ORM\012_Full_clean.md

### Full clean

Source: https://jamescooke.info/djangos-model-save-vs-full_clean.html

* Creating an instance of a Model and calling `save` on that instance does not call `full_clean`. Therefore it’s possible for invalid data to enter your database if you don’t manually call the `full_clean` function before saving.

* Object managers’ default `create` function also doesn’t call `full_clean`.
# Backend\Django\ORM\013_Dumping_and_loading_data.md

### Dumping and loading data

Source: https://testdriven.io/courses/django-rest-framework/multiple-lists/#H-1-populating-the-new-database

Dumping data to file:
```commandline
// python manage.py dumpdata app_name.model app_name.model > file_path
python manage.py dumpdata shopping_list.shoppinglist shopping_list.shoppingitem > shopping_list/fixtures/initial_shopping_lists_with_items.json
```


Loading data from file:
```commandline
// python manage.py loaddata file_path
python manage.py loaddata initial_shopping_lists_with_items.json
```
# Backend\Django\Performance\001_Benchark_and_profiling.md

### Benchmarking and Profiling

Source: https://testdriven.io/blog/django-performance-optimization-tips/

* Django Debug Toolbar - https://github.com/jazzband/django-debug-toolbar
* Silk - https://github.com/jazzband/django-silk
* line_profiler - https://github.com/pyutils/line_profiler
* Locust - https://locust.io/
# Backend\Django\Performance\002_QuerySets.md

### Querysets
Sources:
1. https://docs.djangoproject.com/en/5.0/ref/models/querysets/#when-querysets-are-evaluated
2. https://docs.djangoproject.com/en/5.0/topics/db/queries/#caching-and-querysets
3. https://www.hacksoft.io/blog/django-orm-under-the-hood-iterables

#### When QuerySets are evaluated
##### Iteration
 A QuerySet is iterable, and it executes its database query the first time you iterate over it.
```python
for e in Entry.objects.all():
    print(e.headline)
```
Note: Don’t use this if all you want to do is determine if at least one result exists. It’s more efficient to use exists().

##### Slicing with step paramether
Generally, slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query. An exception is if you use the “step” parameter of Python slice syntax. For example, this would actually execute the query in order to return a list of every second object of the first 10:
```python
Entry.objects.all()[:10:2]
```

##### Pickling/Caching

If you pickle a QuerySet, this will force all the results to be loaded into memory prior to pickling. Pickling is usually used as a precursor to caching and when the cached queryset is reloaded, you want the results to already be present and ready for use (reading from the database can take some time, defeating the purpose of caching). This means that when you unpickle a QuerySet, it contains the results at the moment it was pickled, rather than the results that are currently in the database.

##### repr()

A QuerySet is evaluated when you call repr() on it. This is for convenience in the Python interactive interpreter, so you can immediately see your results when using the API interactively.

##### len()

A QuerySet is evaluated when you call len() on it. This, as you might expect, returns the length of the result list.

Note: If you only need to determine the number of records in the set (and don’t need the actual objects), it’s much more efficient to handle a count at the database level using SQL’s SELECT COUNT(*). Django provides a count() method for precisely this reason.

##### list()

Force evaluation of a QuerySet by calling list() on it. For example:
```python
entry_list = list(Entry.objects.all())
```

##### bool()

Testing a QuerySet in a boolean context, such as using bool(), or, and or an if statement, will cause the query to be executed. If there is at least one result, the QuerySet is True, otherwise False. For example:
```python
if Entry.objects.filter(headline="Test"):
    print("There is at least one Entry with the headline Test")
```
Note: If you only want to determine if at least one result exists (and don’t need the actual objects), it’s more efficient to use exists().

#### Caching
##### When QuerySets are cached
In a newly created QuerySet, the cache is empty. The first time a QuerySet is evaluated – and, hence, a database query happens – Django saves the query results in the QuerySet’s cache and returns the results that have been explicitly requested (e.g., the next element, if the QuerySet is being iterated over). Subsequent evaluations of the QuerySet reuse the cached results.

The following will create two QuerySets, evaluate them, and throw them away:

```python
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])
```
The same database query will be executed twice, effectively doubling your database load. Also, there’s a possibility the two lists may not include the same database records, because an Entry may have been added or deleted in the split second between the two requests.

To avoid this problem, save the QuerySet and reuse it:

```python
queryset = Entry.objects.all()
print([p.headline for p in queryset])  # Evaluate the query set.
print([p.pub_date for p in queryset])  # Reuse the cache from the evaluation.
```

##### When QuerySets are not cached

Repeatedly getting a certain index in a queryset object will query the database each time:

```python
queryset = Entry.objects.all()
print(queryset[5])  # Queries the database
print(queryset[5])  # Queries the database again
```

However, if the entire queryset has already been evaluated, the cache will be checked instead:

```python
queryset = Entry.objects.all()
[entry for entry in queryset]  # Queries the database
print(queryset[5])  # Uses cache
print(queryset[5])  # Uses cache
```
Here are some examples of other actions that will result in the entire queryset being evaluated and therefore populate the cache:
```python
[entry for entry in queryset]
bool(queryset)
entry in queryset
list(queryset)
```

#### QuerySet as a generator vs QuerySet as an iterable

* The QuerySet is immutable - chaining methods to our queryset doesn't modify the original queryset - it creates a new one.
* The QuerySet is a generator when you iterate over it for the first time - when you start iterating over the queryset, internally it executes a SELECT query and yields the DB rows shaped into the desired Python data structure.
* The QuerySet is an iterable - once we've iterated over the queryset once, the queryset puts the DB result into a cache. On every subsequent iteration, we'll use the cached objects. This prevents us from unwanted queries duplication.

```python
users = User.objects.all()  # Creates a queryset

hacksoft_users = users.filter(email__icontains='@hacksoft.io') # Creates a new queryset

for user in hacksoft_users:  # Makes SELECT query and yields the result
    pass

for user in hacksoft_users:  # Just yields the cached result
    pass
```

Based on the unique querysets first iterations, the code above makes 1 SELECT query.

#### Cache implementation
```python
class QuerySet:
    ...
    def _fetch_all(self):
        if self._result_cache is None:
            self._result_cache = list(self._iterable_class(self))
        # ... more code to handle prefetched relations

    def __iter__(self):
        self._fetch_all()
        return iter(self._result_cache)
```

#### Iterable classes
Let's focus on the QuerySet._iterable_class and see what it does with the SELECT query's data.

The _iterable_class has two functions:

* calls the SQL compiler to execute SELECT query
* puts the raw database data (a list of tuples) into ORM objects(.all), dictionaries(.values) or tuples(.values_list) and return it

We have the following types of "iterable classes" that comes from the Django ORM:

* ModelIterable - used by .all and yields ORM objects
* ValuesIterable - set when .values is called and yields dictionaries
* ValuesListIterable, NamedValuesListIterable and FlatValuesListIterable - set when .values_list is called (we have 3 iterable classes here since values_list returns different formats depending on the named and flat arguments)

```python
class ValuesIterable(BaseIterable):
    def __iter__(self):
        queryset = self.queryset
        query = queryset.query
        compiler = query.get_compiler(queryset.db)

        names = [
            *query.extra_select,
            *query.values_select,
            *query.annotation_select,
        ]
        indexes = range(len(names))
        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size):
            yield {names[i]: row[i] for i in indexes}
```

#### Methods chaining and order of execution
The order of the method chaining is not always the same as the order of execution.
We could categorize the QuerySet methods into 2 categories:

* Methods that modify the SQL query - filter/ exclude/ annotate/ only / etc. They are "executed" into the database when it runs the SQL query.
* Methods that define the data structure - all/ values / values_list/etc. They're executed in our Django app (by iterating over the iterable class and modifying the data)

The ORM allows us to chain the same methods in almost any order. But, no matter the order of chaining, the order of execution will always be:

1. Execute the methods that are modifying the SQL query
2. Run the query in the database
3. Execute the methods that define the data structure
# Backend\Django\Performance\003_Caching.md

### Caching in Django

Source: https://testdriven.io/blog/django-caching

#### Caching types

**Memcached**: Memcached is a memory-based, key-value store for small chunks of data. It supports distributed caching across multiple servers.

**Database**: Here, the cache fragments are stored in a database. A table for that purpose can be created with one of the Django's admin commands. This isn't the most performant caching type, but it can be useful for storing complex database queries.

**File** system: The cache is saved on the file system, in separate files for each cache value. This is the slowest of all the caching types, but it's the easiest to set up in a production environment.

**Local** memory: Local memory cache, which is best-suited for your local development or testing environments. While it's almost as fast as Memcached, it cannot scale beyond a single server, so it's not appropriate to use as a data cache for any app that uses more than one web server.

**Dummy**: A "dummy" cache that doesn't actually cache anything but still implements the cache interface. It's meant to be used in development or testing when you don't want caching, but do not wish to change your code.

#### Caching levels
##### Per-site cache
This is the easiest way to implement caching in Django. To do this, all you'll have to do is add two middleware classes to your settings.py file:
```python
### settings.py

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',     # NEW
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # NEW
]
...

CACHE_MIDDLEWARE_ALIAS = 'default'  # which cache alias to use
CACHE_MIDDLEWARE_SECONDS = '600'    # number of seconds to cache a page for (TTL)
CACHE_MIDDLEWARE_KEY_PREFIX = ''    # should be used if the cache is shared across multiple sites that use the same Django instance
```
Although caching the entire site could be a good option if your site has little or no dynamic content, it may not be appropriate to use for large sites with a memory-based cache backend since RAM is, well, expensive.
##### Per-view cache
**It's the caching level that you should almost always start with when looking to implement caching in your Django app.**

You can implement this type of cache with the cache_page decorator either on the view function directly or in the path within URLConf:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def your_view(request):
    ...

### or

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('object/<int:object_id>/', cache_page(60 * 15)(your_view)),
]
```

The cache itself is based on the URL, so requests to, say, object/1 and object/2 will be cached separately.

It's worth noting that implementing the cache directly on the view makes it more difficult to disable the cache in certain situations. For example, what if you wanted to allow certain users access to the view without the cache? Enabling the cache via the URLConf provides the opportunity to associate a different URL to the view that doesn't use the cache:
```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('object/<int:object_id>/', your_view),
    path('object/cache/<int:object_id>/', cache_page(60 * 15)(your_view)),
]
```
##### Template fragment cache

If your templates contain parts that change often based on the data you'll probably want to leave them out of the cache.

For example, perhaps you use the authenticated user's email in the navigation bar in an area of the template. Well, If you have thousands of users then that fragment will be duplicated thousands of times in RAM, one for each user. This is where template fragment caching comes into play, which allows you to specify the specific areas of a template to cache.

To cache a list of objects:
```html
{% load cache %}

{% cache 500 object_list %}
  <ul>
    {% for object in objects %}
      <li>{{ object.title }}</li>
    {% endfor %}
  </ul>
{% endcache %}
```
Here, ```{% load cache %}``` gives us access to the cache template tag, which expects a cache timeout in seconds (500) along with the name of the cache fragment (object_list).

##### Low-level cache API

For cases where the previous options don't provide enough granularity, you can use the low-level API to manage individual objects in the cache by cache key.

For example:
```python
from django.core.cache import cache


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    objects = cache.get('objects')

    if objects is None:
        objects = Objects.all()
        cache.set('objects', objects)

    context['objects'] = objects

    return context
```

In this example, you'll want to invalidate (or remove) the cache when objects are added, changed, or removed from the database. One way to manage this is via database signals:
```python
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_delete, sender=Object)
def object_post_delete_handler(sender, **kwargs):
     cache.delete('objects')


@receiver(post_save, sender=Object)
def object_post_save_handler(sender, **kwargs):
    cache.delete('objects')
```

#### Redis

[Download](https://redis.io/download/) and install Redis.

Once installed, in a new terminal window start the Redis server and make sure that it's running on its default port, 6379. The port number will be important when we tell Django how to communicate with Redis.

```commandline
redis-server
```

For Django to use Redis as a cache backend, the django-redis dependency is required. It's already been installed, so you just need to add the custom backend to the settings.py file:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```
# Backend\Django\Performance\004_Low_level_cache.md

### Low level caching

Source: https://testdriven.io/blog/django-low-level-cache

#### Setup Redis

[Download](https://redis.io/download/) and install Redis.

Once installed, in a new terminal window start the Redis server and make sure that it's running on its default port, 6379. The port number will be important when we tell Django how to communicate with Redis.

```commandline
redis-server
```

For Django to use Redis as a cache backend, the django-redis dependency is required. It's already been installed, so you just need to add the custom backend to the settings.py file:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

#### Reading and setting cache

You may want to use the low-level cache API if you need to cache different:

* Model objects that change at different intervals
* Logged-in users' data separate from each other
* External resources with heavy computing load
* External API calls

Example:

The HomePageView view in products/views.py simply lists all products in the database:
```python
class HomePageView(View):
    template_name = 'products/home.html'

    def get(self, request):
        product_objects = Product.objects.all()

        context = {
            'products': product_objects
        }

        return render(request, self.template_name, context)

```

Let's add support for the low-level cache API to the product objects.

```python
from django.core.cache import cache


class HomePageView(View):
    template_name = 'products/home.html'

    def get(self, request):
        product_objects = cache.get('product_objects')      # NEW

        if product_objects is None:                         # NEW
            product_objects = Product.objects.all()
            cache.set('product_objects', product_objects)   # NEW

        context = {
            'products': product_objects
        }

        return render(request, self.template_name, context)
```

Here, we first checked to see if there's a cache object with the name product_objects in our default cache:

* If so, we just returned it to the template without doing a database query.
* If it's not found in our cache, we queried the database and added the result to the cache with the key product_objects.

#### Invalidating the Cache
##### TTL
Cache may be invalidated after period of time by using ```TTL``` param in settings like:

```python
### Cache time to live is 5 minutes
CACHE_TTL = 60 * 5
```

Example for view caching:

```python
import datetime

import requests
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

BASE_URL = 'https://httpbin.org/'
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ApiCalls(TemplateView):
    template_name = 'apicalls/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{BASE_URL}/delay/2')
        response.raise_for_status()
        context['content'] = 'Results received!'
        context['current_time'] = datetime.datetime.now()
        return context
```
##### Signals
Cache may be also invalidated after changes in database by Django Signals.

Firstly, update ```module/apps.py``` file.

```python
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'

    def ready(self):                # NEW
        import products.signals     # NEW
```

Create file ```module/signals.py```.

```python
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product


@receiver(post_delete, sender=Product, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
     cache.delete('product_objects')


@receiver(post_save, sender=Product, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete('product_objects')
```

Here, we used the receiver decorator from django.dispatch to decorate two functions that get called when a product is added or deleted, respectively. Let's look at the arguments:

* The first argument is the signal event in which to tie the decorated function to, either a save or delete.
* We also specified a sender, the Product model in which to receive signals from.
* Finally, we passed a string as the dispatch_uid to prevent duplicate signals.

So, when either a save or delete occurs against the Product model, the delete method on the cache object is called to remove the contents of the product_objects cache.

##### Django Lifecycle

Rather than using database signals, you could use a third-party package called [Django Lifecycle](https://rsinger86.github.io/django-lifecycle/), which helps make invalidation of cache easier and more readable.

Install ``django-lifecycle`` and modify ``module/apps.py`` to base form, without any Django signals settings.
```python
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'
```

Update model with django_lifecycle hooks like:

```python
from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Manager
from django_lifecycle import LifecycleModel, hook, AFTER_DELETE, AFTER_SAVE   # NEW
from django.utils import timezone


class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('product_objects')
        super(CustomQuerySet, self).update(updated=timezone.now(), **kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)


class Product(LifecycleModel):              # NEW
    title = models.CharField(max_length=200, blank=False)
    price = models.CharField(max_length=20, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    class Meta:
        ordering = ['-created']

    @hook(AFTER_SAVE)                       # NEW
    @hook(AFTER_DELETE)                     # NEW
    def invalidate_cache(self):             # NEW
       cache.delete('product_objects')      # NEW
```

In the code above, we:

* First imported the necessary objects from Django Lifecycle
* Then inherited from LifecycleModel rather than django.db.models
* Created an invalidate_cache method that deletes the product_object cache key
* Used the @hook decorators to specify the events that we want to "hook" into

As with django signals the hooks won't trigger if we do update via a QuerySet:
```python
Product.objects.filter(id=1).update(title="A new title")
```
In this case, we still need to create a custom Manager and QuerySet.
# Backend\Django\Performance\005_Request_response_cycle.md

### Request/response cycle

Source: https://medium.com/@ksarthak4ever/django-request-response-cycle-2626e9e8606e

![005_request_path.png](_images/005_request_path.png)

#### WSGI
As we know a Web server is a program that uses HTTP (Hypertext Transfer Protocol) to serve the files that form Web pages to users, in response to their requests, which are forwarded by their computers’ HTTPclients.

WSGI is a tool created to solve a basic problem: connecting a web server to a web framework. WSGI has two sides: the ‘server’ side and the ‘application’ side. To handle a WSGI response, the server executes the application and provides a callback function to the application side. The application processes the request and returns the response to the server using the provided callback. Essentially, the WSGI handler acts as the gatekeeper between your web server (Apache, NGINX, etc) and your Django project.

Between the server and the application lie the middlewares. You can think of middlewares as a series of bidirectional filters: they can alter (or short-circuit) the data flowing back and forth between the network and your Django application.

#### Single request flow

When the user makes a request of your application, a WSGI handler is instantiated, which:

1. imports your settings.py file and Django’s exception classes.
2. loads all the middleware classes it finds in the MIDDLEWARE_CLASSES or MIDDLEWARES(depending on Django version) tuple located in settings.py
3. builds four lists of methods which handle processing of request, view, response, and exception.
4. loops through the request methods, running them in order
5. resolves the requested URL
6. loops through each of the view processing methods
7. calls the view function (usually rendering a template)
8. processes any exception methods
9. loops through each of the response methods, (from the inside out, reverse order from request middlewares)
10. finally builds a return value and calls the callback function to the web server

#### Layers of Django Application
1. Request Middlewares
2. URL Router(URL Dispatcher)
3. Views
4. Context Processors
5. Template Renderers
6. Response Middlewares

#### Middlewares

There are four key points you can hook into the request/response cycle through your own custom middleware: ```process_request```, ```process_response```, ```process_view```, and ```process_exception```. Think of an onion: request middlewares are executed from the outside-in, hit the view at the center, and return through response middlewares back to the surface.
# Backend\Django\Permissions\001_User_level_permissions.md

### User-level Permissions

Source: https://testdriven.io/blog/django-permissions/

#### User permissions to model

When django.contrib.auth is added to the INSTALLED_APPS setting in the settings.py file, Django automatically creates add, change, delete and view permissions for each Django model that's created.

Permissions in Django follow the following naming sequence:

```{app}.{action}_{model_name}```
```python
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
```

By default, Django will create the following permissions:
* blog.add_post
* blog.change_post
* blog.delete_post
* blog.view_post

#### Checking User permission

You can then check if a user (via a Django user object) has permissions with the has_perm() method:
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from blog.models import Post

content_type = ContentType.objects.get_for_model(Post)
post_permission = Permission.objects.filter(content_type=content_type)
print([perm.codename for perm in post_permission])
### => ['add_post', 'change_post', 'delete_post', 'view_post']

user = User.objects.create_user(username="test", password="test", email="test@user.com")

### Check if the user has permissions already
print(user.has_perm("blog.view_post"))
### => False

### To add permissions
for perm in post_permission:
    user.user_permissions.add(perm)

print(user.has_perm("blog.view_post"))
### => False
### Why? This is because Django's permissions do not take
### effect until you allocate a new instance of the user.

user = get_user_model().objects.get(email="test@user.com")
print(user.has_perm("blog.view_post"))
### => True
```

Superusers will always have permission set to True even if the permission does not exist:
```python
from django.contrib.auth.models import User

superuser = User.objects.create_superuser(
    username="super", password="test", email="super@test.com"
)

### Output will be true
print(superuser.has_perm("blog.view_post"))

### Output will be true even if the permission does not exists
print(superuser.has_perm("foo.add_bar"))
```
# Backend\Django\Permissions\002_Group_level_permissions.md

### Group-level permissions

Source: https://testdriven.io/blog/django-permissions/

#### Intro

Group models are a generic way of categorizing users so you can apply permissions, or some other label, to those users. A user can belong to any number of groups.

With Django, you can create groups to class users and assign permissions to each group so when creating users, you can just assign the user to a group and, in turn, the user has all the permissions from that group.

To create a group, you need the Group model from django.contrib.auth.models.

#### Example

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
### => ['add_post', 'change_post', 'delete_post', 'view_post']

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
# Backend\Django\Permissions\003_Enforcing_permission.md

### Enforcing Permissions

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
# Backend\Django\Permissions\004_Model_level_permissions.md

### Model-level Permissions

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
# Backend\Django\Session\001_Storing_data_in_session.md

### Przechowywanie danych w sesji
```python
### module/views.py
def index(request):
    # Check if there already exists a "tasks" key in our session
    if "tasks" not in request.session:
        # If not, create a new list in session
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })
```
# Backend\Django\Signals\001_Django_signals.md

### Django Signals

Source: https://testdriven.io/courses/django-rest-framework/validation-ordering-pagination/#H-6-django-signals

Django provides several built-in signals that are set by default. Some examples:

* `pre_save` and `post_save` - triggered before/after a model's save() is called
* `pre_delete` and `post_delete` - triggered before/after a model's delete() or a QuerySets' delete() are called
* `request_started` and `request_finished` - triggered when Django starts or finishes an HTTP request
* `m2m_changed` - triggered when a ManyToManyField on a model is changed

There're two key elements of the signal: The sender and the receiver.

The sender (a Python object) dispatches a signal, and the receiver (a function or an instance method) receives the signal and then does something.

```python
### shopping_list/receivers.py


from django.db.models.signals import post_save
from django.dispatch import receiver

from shopping_list.models import ShoppingItem, ShoppingList


@receiver(post_save, sender=ShoppingItem)
def interaction_with_shopping_list(sender, instance, **kwargs):
    ShoppingList.objects.get(id=instance.shopping_list.id).save(update_fields=["last_interaction"])
```

With @receiver, we made the interaction_with_shopping_list function a receiver. The sender is ShoppingItem, and the signal is post_save.

So, when a ShoppingItem instance is saved, interaction_with_shopping_list updates the ShoppingList's last_interaction field.

We just need to register the receiver in shopping_list/apps.py:

```python
### shopping_list/apps.py


from django.apps.config import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shopping_list"

    def ready(self):
        import shopping_list.receivers
```

Now all receivers inside the shopping_list/receivers.py will be imported when the app is ready after it's initialized.

To ensure Django's uses this configuration, update shopping_list/__init__.py like so:

```python
default_app_config = "shopping_list.apps.ApiConfig"
```

This sets the app's default configuration to the one defined in shopping_list/apps.py.


# Backend\Django\Templates\001_Variables.md

### Variables in templates

Source: https://pogromcykodu.pl/html-na-sterydach/

#### Example view
```python
class StudentsView(View):
    def get(self, request):
        student_1 = {'name': 'John', 'surname': 'Black', 'grade':5.0}
        student_2 = {'name': 'Mary', 'surname': 'White', 'grade': 3.5}
        context = {
            'student_1': student_1,
            'student_2': student_2
        }
        return render(request, 'students.html', context=context)
```
#### Variables
Template:
```html
Student 1 : {{ student_1 }}
Student 2 : {{ student_2 }} 
```
Display:
```
Student 1: {'name': 'John', 'surname': 'Black', 'grade': 5.0}
Student 2: {'name': 'Mary', 'surname': 'White', 'grade': 3.5}
```
#### Dict values
Template:
```html
Student 1:
Imię: {{ student_1.name }}, Nazwisko: {{ student_1.surname }}
```
Output:
```
Student 1:
Imię: John, Nazwisko: Black
```
#### Class objects
```python
class Student:
    def __init__(self, name, surname, grade):
        self.name = name
        self.surname = surname
        self.grade = grade 

...

student_3 = Student(name='Mike', surname='Doe', grade=4.5)
context = {
            ...
            'student_3': student_3
}    
```
Template:
```html
Student 3:
Imię: {{ student_3.name}}, Nazwisko: {{ student_3.surname }} 
```
Output:
```
Student 3:
Imię: Mike, Nazwisko: Doe
```

#### Lists

```python
students_list = [student_1, student_2, student_3]
context = {
            ...
            'students_list': students_list
} 
```
Template:
```html
Pierwszy student z listy: {{ students_list.0 }}
Drugi student z listy: {{ students_list.1 }} 
```
Output:
```
Pierwszy student z listy: {'name': 'John', 'surname': 'Black', 'grade': 5.0}
Drugi student z listy: {'name': 'Mary', 'surname': 'White', 'grade': 3.5}
```


# Backend\Django\Templates\002_Tags.md

### Tags

Source: https://pogromcykodu.pl/html-na-sterydach/

#### List iteration

`{% for ... in ... %}`

Template:
```html
<ul>
    {% for student in students_list %}
        <li>{{ student.name }} {{ student.surname }}</li>
    {% endfor %}
</ul> 
```

#### Reversed list iteration

```html
{% for pizza in pizza_menu reversed %}
    <div>{{ pizza }}</div>
{% endfor %} 
```

#### Item index during iteration

* `{{ forloop.counter0 }}`

Returns loop counter starting from 0.

```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.counter0 }} - {{ pizza }}
    </div>
{% endfor %}
```
* `{{ forloop.counter }}`
Returns loop counter starting from 1.
```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.counter }} - {{ pizza }}
    </div>
{% endfor %} 
```
* `{{ forloop.revcounter0 }}`
Returns reverted loop counter ending on 0.
```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.revcounter0 }} - {{ pizza }}
    </div>
{% endfor %} 
```
* `{{ forloop.revcounter }}`
Returns reverted loop counter ending on 1.
```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.revcounter }} - {{ pizza }}
    </div>
{% endfor %} 
```

#### Detecting first/last element during iteration

* `{{ forloop.first }}`
```html
{% for pizza in pizza_menu %}
<div>
    {{ pizza }}
    {% if forloop.first %} - MNIAM
    {% endif %}
</div>
{% endfor %}
```
* `{{ forloop.last }}`
```html
{% for pizza in pizza_menu %}
<div>
    {{ pizza }}
    {% if forloop.last %} - MNIAM
    {% endif %}
</div>
{% endfor %}
```

#### Detecting empty list
`{% empty %}`
```html
<ul>
{% for pizza in pizza_menu %}
    <li>{{ pizza.name }}</li>
{% empty %}
    <li>Wszystko zjedzone :( </li>
{% endfor %} 
</ul> 
```
#### If/else
`{% if ... elif ... else %}`
Template:
```html
<ul>
    {% for student in students_list %}
        <li>
        {{ student.name }} {{ student.surname }}
        {% if student.grade == 5.0 %} - Kujon
        {% elif student.grade > 4 %} - Tak trzymaj!
        {% else %} - Pora na naukę!
        {% endif %}
        </li>
     {% endfor %}
</ul> 
```

#### Inheritance and templates extending

* `{% block ... %} {% endblock %}` – defining block to override in different template
* `{% extends ... %}` – indicating template to extend
* `{% include %}` – input other template
* `{% load %}` – loading additional tags

# Backend\Django\Templates\003_Filters.md

### Filters

Source: https://pogromcykodu.pl/html-na-sterydach/

#### Pattern

`{{ variable | filter_name }} `

#### Example data
```python
student_1 = {
    'name': 'John', 
    'surname': 'Black', 
    'grade': 5.0,
    'birth_date': datetime(2000, 10, 27, 16, 25),  
    'has_graduated': True, 
    'bio': 'Very smart n and intelligent.', 
    'scholarship': ''
}
```
#### String operations
* `lower` – lowercasing string. Example: `{{ student_1.name | lower }}`  ➜  john.
* `upper` – uppercasing string. Example: `{{ student_1.name | upper }}`   ➜  JOHN 
* `title` – changing first letter of single word to upper case.  Example:  `{{ student_1.bio | title }}`   ➜  Very Smart And Intelligent.
* `slice` – slicing string. Example:  `{{ student_1.bio | slice:"5:16" }}`   ➜  smart and
* `truncatechars` – cutting string to given length, including '...'. Example:  `{{ student_1.bio | truncatechars:7 }}`   ➜  Very s…
* `truncatewords` – cutting string to given words count, adding '...'. Example:  `{{ student_1.bio | truncatewords:2 }}`   ➜  Very smart …
* `linebreaksbr` – replacing '\n' with <br>.

#### Date/hour formatting
`date` – date in given format. Example: `{{ student_1.birth_date | date:"d/m/Y" }}`   ➜  27/10/2000
`time` – time in given format. Example: `{{ student_1.birth_date | time:"H:i" }}`   ➜  16:25
#### Empty/default values
`default` – replacing empty string or none with default. Example: `{{ student_1.scholarship | default:"Brak" }}`   ➜  Brak 
`yesno` – custom string for boolean values.. Example: `{{ student_1.has_graduated | yesno:"Tak,Nie" }}`   ➜  Tak

# Backend\Django\Testing\001_Models_testing.md

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
# Backend\Django\Testing\002_Endpoints_testing.md

### Testowanie endpointów
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

# Backend\Django\Testing\003_Factories.md

### Factories

Source: 
* https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories#fakes
* https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories-advanced-usage
* https://youtu.be/-C-XNHAJF-c?si=5viLbeVKRLgn8zXD

#### Creating Factories

```python
### models.py

from django.db import models
from django.utils import timezone

class VehiclePurchase(models.Model):
    price = models.DecimalField(max_digits=19, decimal_places=2)
    color = models.ForeignKey(
        VehicleColor, null=True, blank=True, on_delete=models.SET_NULL
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        BaseUser, null=True, blank=True, on_delete=models.SET_NULL
    )
    sales_member = models.ForeignKey(
        BaseUser, null=True, blank=True, on_delete=models.SET_NULL
    )
    requested_at = models.DateTimeField(db_index=True, default=timezone.now)
    cancelled_at = models.DateTimeField(null=True, blank=True)
```

```python
### factories.py

import factory

from my_project.utils.tests import faker

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.LazyAttribute(lambda _: faker.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())

class VehiclePurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehiclePurchase

    price = factory.LazyAttribute(lambda _: faker.pyfloat(positive=True))
    color = factory.SubFactory(ColorFactory)
    vehicle = factory.SubFactory(VehicleFactory)
    plan = factory.SubFactory(PlanFactory)
    customer = factory.SubFactory(UserFactory)
    sales_member = factory.SubFactory(UserFactory)
```

#### DjangoModelFactory

DjangoModelFactory is a basic interface from factory_boy that gives "ORM powers" to your factories.

It's main feature here is that it provides you with a common "create" and "build" strategies that you can use to generate objects in your tests.

* SomeFactory.create() / SomeFactory() - saves the generated object to the database. The related sub factories are also created in the database.
* SomeFactory.build() - generates a model instance without saving it to the database. The related sub factories are also not stored in the database.

#### Faker

As you may have noticed, we don't create a Faker instance in the factories file. We import it from another file in the application. This is intentional!

We highly recommend "proxying" the Faker instance and using it in your app that way.

You'd most likely want to have the same configuration when you use fakes around your app. Same goes if you want to customize the providers and use them in different places.
```python
### my_project/utils/tests/base.py

from faker import Faker

faker = Faker()
```

#### LazyAttribute
It's an extremely simple but yet powerful abstraction that represents the symbiosis between the factories and the fakes.

It accepts a method which is invoked when a Factory instance is being generated. The return value of the method is used for the value of the desired attribute.

If you don't use it, you're actually setting a class attribute to your Factory. This means that this attribute will be generated when you define your Factory class, not when you instantiate it.
```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = faker.unique.email()
```
Defining your Factory this way will produce the following result:

```python
for _ in range(5):
    print(UserFactory.build().email)
 
erobinson@example.org
erobinson@example.org
erobinson@example.org
erobinson@example.org
erobinson@example.org
```
For most of the cases, you would want your objects to be generated with different values every time:
```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.unique.email())
```
This is the output when you use LazyAttribute:

```python
for _ in range(5):
    print(UserFactory.build().email)
    
woodtammy@example.net
justin56@example.com
rachel10@example.com
michaelthompson@example.com
mkennedy@example.com
```

#### Factory.build() vs Factory.create()
Factory.build() will return you a new object that's not yet saved in the database.

This might be helpful in situations, where you need the object, but don't need it to be saved in the database, thus, improving the speed of the test.

Possible use cases where you can apply this:

* A method that receives an object and performs some validation over its fields. If this is not related to any database queries, use Factory.build() in your tests
* A service that performs some small validation at the beginning of its definition. This service receives some model instances as arguments. When you test the validation, you can build() the passed objects if you don't need them in the database
* A selector that is grouping some passed data. If this selector does not perform any database queries, build() the passed data instead of creating it

### LazyAttribute for field constraints

```python
class SchoolCourse(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="school_course_start_before_end",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```

Here is how you can define Factory and make sure that the end_date will be after the start_date:
```python
class SchoolCourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolCourse

    start_date = factory.LazyAttribute(lambda _: faker.past_date())
    end_date = factory.LazyAttribute(lambda _self: _self.start_date + timedelta(days=365))
```
As you can see, the _self attribute of the lamba function is key here.

#### SelfAttribute

```python
class Student(models.Model):
    email = models.EmailField(max_length=255)
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email', 'school', )

class Roster(models.Model):
    student = models.ForeignKey(Student, related_name='rosters', on_delete=models.CASCADE)
    school_course = models.ForeignKey(SchoolCourse, related_name='rosters', on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
```
> NOTE: The Roster model represents that a Student is taking part in a School Course

```python
class RosterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Roster

    student = factory.SubFactory(StudentFactory)
    school_course = factory.SubFactory(
        SchoolCourseFactory,
        school=factory.SelfAttribute('..student.school')
    )
    start_date = factory.SelfAttribute('school_course.start_date')
    end_date = factory.SelfAttribute('school_course.end_date')
```
This implementation says: "I want my roster period to be the same as the course period" which should be a valid statement for most of the use cases. It also says -  "I want my roster's course to be in the school of the generated student by default".

#### The double-dot notation
The double-dot notation refers to the parent factory (in our case RosterFactory) where current sub factory (in our case SchoolCourseFactory) is being called. This is well described in the docs [here](https://factoryboy.readthedocs.io/en/stable/reference.html?#parents).

If the double-dot notation is not up to your taste, you can achieve the same behavior by using the LazyAttribute, making the code a bit more explicit:

```python
class RosterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Roster

    student = factory.SubFactory(StudentFactory)
    school_course = factory.SubFactory(
        SchoolCourseFactory,
        school=factory.LazyAttribute(lambda course: course.factory_parent.student.school)
    )
    start_date = factory.LazyAttribute(lambda _self: _self.school_course.start_date)
    end_date = factory.LazyAttribute(lambda _self: _self.school_course.end_date)
```
> NOTE: Take a look at the factory_parent here. It's actually a reference to the RosterFactory in our case.

#### Helper Factories

For example, if we observe that a lot of tests are dealing with Rosters that need to be in some chronological order, one after the other, we might want to do something like this:

```python
def get_future_roster_start_date(roster_obj):
    if not roster_obj.start_after:
        return faker.future_date()

    return roster_obj.start_after + timedelta(days=faker.pyint(2, 100))

class FutureRosterFactory(RosterFactory):
    class Params:
        start_after = None

    start_date = factory.LazyAttribute(get_future_roster_start_date)
```
```python
In [1]: roster = RosterFactory.build()

In [2]: future_roster1 = FutureRosterFactory.build(start_after=roster.start_date)

In [3]: future_roster2 = FutureRosterFactory.build(start_after=future_roster1.start_date)

In [4]: roster.start_date, future_roster1.start_date, future_roster2.start_date
Out [4]: (datetime.date(2021, 11, 25),
 datetime.date(2022, 3, 1),
 datetime.date(2022, 5, 13))
```
> NOTE: In the Params class you can list all arguments that are factory class specific. They won't be passed to the generated instance.

```python
In [13]: future_roster1.start_after
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-13-9299608b2d13> in <module>
----> 1 future_roster1.start_after

AttributeError: 'Roster' object has no attribute 'start_after'
```

#### Parent with children factory

If we observe that a lot of tests always require a specific parent object, to come hand-in-hand with created children objects, we might want to make our lives a bit easier.

Let's take our SchoolCourse model.  You'd most likely have services and/or selectors that work with school courses that have rosters in them.

Here's a helper factory dealing with this:

```python
class SchoolCourseWithRostersFactory(SchoolCourseFactory):
    @factory.post_generation
    def rosters(obj, create, extracted, **kwargs):
        if create:
            rosters = extracted or RosterFactory.create_batch(
                kwargs.pop('count', 5),
                **kwargs,
                student__school=obj.school  # NOTE!
            )

            obj.rosters.set(rosters)

            return rosters
```

```python
In [1]: course1 = SchoolCourseWithRostersFactory()

In [2]: course1.rosters.count()
Out[2]: 5

In [3]: roster = RosterFactory()

In [4]: course2 = SchoolCourseWithRostersFactory(rosters=[roster])

In [5]: course2.rosters.all()
Out[5]: <QuerySet [<Roster: Roster object (6)>]>

In [6]: course3 = SchoolCourseWithRostersFactory(rosters__count=10)

In [7]: course3.rosters.count()
Out[7]: 10
```

There are several important points here:

* @factory.post_generation is a post-generation hook from factory_boy. It's invoked after the model object is created
* The obj argument is the model object that's just been generated
* The create argument is a boolean which is True if the create() strategy is being used. False otherwise (.build() strategy)
* extracted is the value of the defined attribute if one is passed when the Factory is being called. SchoolCourseWithRostersFactory(students=some_generated_students) →  extracted == some_generated_students
* kwargs are the passed optional arguments via the double underscores of the defined attribute. SchoolCourseWithRostersFactory(students__count=10) → kwargs == {'count': 10}
* As you may have noticed, this example is going to work only with the create() strategy. This is a limitation that comes from the fact that the students set comes as a reversed relation from the ORM.

The moral of the story is - whenever you see a pattern emerging, create additional helpers, to make your tests clearer.

#### Other topics

![](_images/003_Factories.png)

#### Traits

![](_images/003_Factories_traits.png)

#### SubFactory vs RelatedFactory

![](_images/003_Factories_sub_vs_related.png)
![](_images/003_Factories_4.png)
# Backend\Django\Urls\001_All_url_patterns.md

### Listing all url patterns in project

```python
from django.urls import get_resolver

patterns = get_resolver().url_patterns
```
Example output:
![img.png](_images/img.png)
# Backend\Django\Urls\002_Defining_URL_params.md

### Defining URL params

Source: https://pogromcykodu.pl/stworz-wlasny-walidator-url/

```python
urlpatterns = {
    path('article/<int:pk>', ArticleDetailsView.as_view()),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', ArticlesListView.as_view()), 
}

```

#### URL variables types:
* int – integer -> `<int:pk>`
* str – non-empty string without '/' sign -> `<str:name>`
* slug – string containint letters, numbers, '-' and '_' -> `<slug:slug>`
* uuid – string containing groups of letters divided by '=' -> `<uuid:id>`
* path – non-empty string with '/' sign as path separator -> `<path:file_path>`
# Backend\Django\Urls\003_PathConverters.md

### PathConverters

Source: https://pogromcykodu.pl/stworz-wlasny-walidator-url/

#### Default URL converters:

```python
path('article/<int:pk>', ArticleDetailsView.as_view()),
```

* int – IntConverter
* str – StringConverter
* slug – SlugConverter
* uuid – UUIDConverter 
* path – PathConverter

#### Example Converter

```python
class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
```

#### Exceptions

* ValueError - on invalid value in `to_python` method
* NoReverseMatch - on invalid value in `to_url` method

#### Custom Converter

```python
class YearConverter(IntConverter):

    def to_python(self, value):
        value = int(value)
        if value >= 1996 and value <= 2020:
            return value
        raise ValueError 
```

```python
### urls.py

register_converter(YearConverter, 'yyyy')

...

urlpatterns = {
    path('articles/<yyyy:year>', ArticlesListView.as_view()) 
}
```
# Backend\Django\Users\001_Login_and_logout.md

### Login i logout
```python
### project/module/urls.py
...

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
```
#### Login
```python
### project/module/views.py
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
##### 5.2. Logout
```python
### module/views.py
def logout_view(request):
    logout(request)
    return render(request, "module/login.html", {
                "message": "Logged Out"
            })
```
# Backend\Django\Users\002_Superuser.md

### Tworzenie superusera
Warto również założyć konto superusera, aby uzyskać możliwość logowania się w panelu administracyjnym.
```commandline
python manage.py createsuperuser
```
# Backend\Django\Users\003_Custom_user_model.md

### Custom user model

Source: https://testdriven.io/blog/django-custom-user-model

#### Start project with custom User!
Do this on project init to omit problems in the future. In case you want to migrate to custom User model in existing project check [this link](https://testdriven.io/blog/django-custom-user-model-migration/).

#### Base classes for custom User
Options:

**AbstractUser**: Use this option if you are happy with the existing fields on the user model and just want to remove the username field.

**AbstractBaseUser**: Use this option if you want to start from scratch by creating your own, completely new user model. 

#### Custom User manager

Custom manager subclassing BaseUserManager, that uses email as the unique identifier instead of a username.

```python
### users/managers.py

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
```

#### Custom User model

##### AbstractUser - use predefined fields
* Set *username* field to None. 
* Add *email* field, make it unique and required, and mark it as *USERNAME_FIELD*. 
* Specify that all objects for the class come from the CustomUserManager

```python
### users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
```
##### AbstractBaseUser - add all fields manually
* Add fields *email*, *is_staff*, *is_active*, and *date_joined*.
* Mark *email* field as *USERNAME_FIELD*. 
* Specify that all objects for the class come from the CustomUserManager

#### Settings
Add the following line to the settings.py file so that Django knows to use the new custom user class:

```python
### settings.py

AUTH_USER_MODEL = "users.CustomUser"
```

After that, make migrations and migrate changes to database.

#### Forms
```python
### users/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
```

#### Admin
```python
### users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
```
# Backend\Django\Views\001_Adding_view.md

### Dodawanie widoku
W celu dodania nowego widoku konieczne jest utworzenie jego definicji w views.py oraz określenie w urls.py endpointu pod jakim ten widok będzie dostępny.
```python
### project/module/views.py
 from django.shortcuts import render
 from django.http import HttpResponse

 def index(request):
     return HttpResponse("Hello, world!")
```
```python
### project/module/urls.py
 from django.urls import path
 from . import views

 urlpatterns = [
     path("", views.index, name="index")
 ]
```

Konieczne jest dodanie zawartości pliku urls.py zawartego w danym module do urls.py projektu.

```python
### project/project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('module/', include("module.urls"))
]
```
# Backend\Django\Views\002_Function_based_views.md

### Function-based views

Source: https://testdriven.io/blog/django-class-based-vs-function-based-views/#function-based-views-fbvs

#### Pros

* Explicit code flow (you have full control over what happens)
* Simple to implement
* Easy to understand
* Great for unique view logic
* Easy to integrate with decorators

#### Cons

* A lot of repeated (boilerplate) code
* Handling of HTTP methods via conditional branching
* Don't take advantage of OOP
* Harder to maintain

#### Example

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
#### Usage

You should opt for FBVs when you're working on highly customized view logic. In other words, FBVs are a great use case for a view that doesn't share much code with other views. A few real-world examples for using FBVs would be: a statistics view, a chart view, and a password reset view.
# Backend\Django\Views\003_Class_based_views.md

### Class-based views

Source: https://testdriven.io/blog/django-class-based-vs-function-based-views/#class-based-views-cbvs

#### Pros

* Are extensible
* They take advantage of OOP concepts (most importantly inheritance)
* Great for writing CRUD views
* Cleaner and reusable code
* Django's built-in generic CBVs
* They're similar to Django REST framework views

#### Cons

* Implicit code flow (a lot of stuff happens in the background)
* Use many mixins, which can be confusing
* More complex and harder to master
* Decorators require an extra import or code override

#### Flow

1. An HttpRequest is routed to MyView by the Django URL dispatcher.
2. The Django URL dispatcher calls as_view() on MyView.
3. as_view() invokes setup() and dispatch().
4. dispatch() triggers a method for a specific HTTP method or http_method_not_allowed().
5. An HttpResponse is returned.

![](_images/003_CBV_Flow.png)
# Backend\Django\Views\004_Generic_class_based_views.md

### Generic Class-based views

Source: https://testdriven.io/blog/django-class-based-vs-function-based-views/#djangos-generic-class-based-views

#### Generic Display Views

Designed to display data.

* DetailView
* ListView

#### Generic Editing Views

Provide a foundation for editing content.

* FormView
* CreateView
* UpdateView
* DeleteView

#### Generic Date-based Views

Allow in-depth displaying of date-based data.

* ArchiveIndexView
* YearArchiveView
* MonthArchiveView
* WeekArchiveView
* DayArchiveView
* TodayArchiveView
* DateDetailView
# Backend\Django REST Framework\Authentication\001_Credentials_based_authentication.md

### Credentials-based Authentication

Source: https://testdriven.io/blog/django-rest-auth

#### Settings
```python
### core/settings.py

INSTALLED_APPS = [
    # ...
    "rest_framework",
    "rest_framework.authtoken",
]
```

The authtoken app is required since we'll use TokenAuthentication instead of Django's default SessionAuthentication. Token authentication is a simple token-based HTTP authentication scheme that is appropriate for client-server setups.
```python
### settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}
```

#### django-allauth

```python
### core/settings.py

INSTALLED_APPS = [
    "django.contrib.sites",  # make sure 'django.contrib.sites' is installed
    # ...
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # add if you want social authentication
]
```

django-allauth depends on Django's "sites" framework so make sure you have it installed. On top of that, make sure that you have the SITE_ID set:
```python
### core/settings.py

SITE_ID = 1  # make sure SITE_ID is set
```
#### dj-rest-auth
```commandline
pip install "dj-rest-auth[with_social]==4.0.0"
```
We need to use the with_social specifier since we want to enable the standard registration process. Additionally, we'll utilize this package later when we enable social authentication.
```python
### core/settings.py

INSTALLED_APPS = [
    # ...
    "dj_rest_auth",
    "dj_rest_auth.registration",
]
```
Update authentication/urls.py like so:
```python
### authentication/urls.py

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path


urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
]
```
#### Testing

##### #Register
Then, to create an account run the following in a new terminal window:
```commandline
$ curl -XPOST -H "Content-type: application/json" -d '{
      "username": "user1",
      "password1": "complexpassword123",
      "password2": "complexpassword123"
  }' 'http://localhost:8000/api/auth/register/' | jq
```
By default, you'll get an empty response.

##### Login
You can now use the created account to obtain an authentication token:
```commandline
$ curl -XPOST -H "Content-type: application/json" -d '{
      "username": "user1",
      "password": "complexpassword123"
  }' 'http://localhost:8000/api/auth/login/' | jq
```
The response will be similar to this one:

```commandline
{
    "key": "<your_token>"
}
```
##### User Details
Now pass the token in the Authorization header to fetch the user details:
```commandline
$ curl -XGET -H 'Authorization: Token <your_token>' \
    -H "Content-type: application/json" 'http://localhost:8000/api/auth/user/' | jq
```
Response:
```
{
    "pk": 1,
    "username": "user1",
    "email": "user1@example.com",
    "first_name": "",
    "last_name": ""
}
```
##### Logout
As you might have guessed, sending a POST request to the logout endpoint destroys the token:
```commandline
$ curl -XPOST -H 'Authorization: Token <your_token>' \
    -H "Content-type: application/json" 'http://localhost:8000/api/auth/logout/' | jq
```
Response:
```
{
    "detail": "Successfully logged out."
}
```

# Backend\Django REST Framework\Authentication\002_Email_verification_and_password_reset.md

### Email Verification and Password Reset

Source: https://testdriven.io/blog/django-rest-auth/#email-verification-and-password-reset

#### SMTP Settings

You can use your own SMTP server or utilize Brevo (formerly SendInBlue), Mailgun, SendGrid, or a similar service. I suggest you go with Brevo since they're relatively cheap and allow you to send a decent amount of emails daily (for free).

To configure SMTP, add the following to core/settings.py:
```python
### core/settings.py

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "<your email host>"                    # smtp-relay.sendinblue.com
EMAIL_USE_TLS = False                               # False
EMAIL_PORT = "<your email port>"                    # 587
EMAIL_HOST_USER = "<your email user>"               # your email address
EMAIL_HOST_PASSWORD = "<your email password>"       # your password
DEFAULT_FROM_EMAIL = "<your default from email>"    # email ending with @sendinblue.com
```

#### Email verification and password reset

Add the following django-allauth settings to core/settings.py:
```python
### core/settings.py

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
```

Next, let's take care of the URLs found in the confirmation and password reset email templates. The {{ password_reset_url }} and {{ activate_url }} get replaced with the following values:
```
http://localhost:8000/api/auth/register/account-confirm-email/<str:key>/
http://localhost:8000/api/auth/password/reset/confirm/<str:uidb64>/<str:token>/
```
By default, django-allauth takes care of these URLs. It renders a form and submits a request back to the backend. Since we're building a REST-based API we don't want that to happen; instead, we want to redirect these two URLs to our frontend from where we can POST the keys back to the backend.

To set up the redirects, first define the following two settings in core/settings.py:
```python
### core/settings.py

### <EMAIL_CONFIRM_REDIRECT_BASE_URL>/<key>
EMAIL_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/email/confirm/"

### <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uidb64>/<token>/
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/password-reset/confirm/"
```
Make sure to include the trailing slash / at the end of the URLs.

Next, add the following two views to authentication/views.py:
```python
### authentication/views.py

from django.conf import settings
from django.http import HttpResponseRedirect


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

```
Lastly, register the newly created views in authentication/urls.py:
```python
### authentication/urls.py

from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)
from authentication.views import email_confirm_redirect, password_reset_confirm_redirect
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path


urlpatterns = [
    # ...
    path("register/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("register/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),
    path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
```
#### Testing
##### Register
Creating a new user now requires you to provide a valid email address:
```commandline
$ curl -XPOST -H "Content-type: application/json" -d '{
      "username": "user2",
      "email": "<your email address>",
      "password1": "complexpassword123",
      "password2": "complexpassword123"
  }' 'http://localhost:8000/api/auth/register/' | jq
```
Make sure to replace <your email address> with your actual email address.

Response:
```
{
    "detail": "Verification e-mail sent."
}
```
As you register a verification email will be sent to your email.
##### Verify Email
From the frontend you can then POST the key back to the backend to verify the email address:
```commandline
$ curl -XPOST -H "Content-type: application/json" -d '{
      "key": "OQ:1ptSAe:gh_07-gQ_1ak6muKCAly..."
  }' 'http://localhost:8000/api/auth/register/verify-email/' | jq
```
Response:
```
{
    "detail": "ok"
}
```
Once you've successfully verified your email address you'll be able to log in.

##### Password Reset
To request a new password, you need to POST to /api/auth/password/reset/ like so:
```
$ curl -XPOST -H "Content-type: application/json" -d '{
      "email": "<your email address>"
  }' 'http://localhost:8000/api/auth/password/reset/' | jq
```
After you send the request you'll receive aa email.
# Backend\Django REST Framework\Authentication\003_Authentication_types.md

### Authentication types
#### BasicAuthentication

Username + password (base64 encoded)

```python
### settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ]
}
```

| Pros   | Cons                                 |
|--------|--------------------------------------|
| Simple | Every request look up Session Object |
| &nbsp; | Credentials passed in clear text     |
| &nbsp; | Only suitable for testing            |
| &nbsp; | Must use HTTPS                       |

#### SessionAuthentication

Cookie files stored in browser session after first authentication.

```python
### settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}
```

| Pros                    | Cons                            |
|-------------------------|---------------------------------|
| Secure                  | Not good for multiple frontends |
| Only validate user once | Hard to keep up-to-date         |

#### TokenAuthentication

Using token generated with single username & password authentication.

```python
### settings/core.py
INSTALLED_APPS = {
    "rest_framework.authtoken"
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}
```

| Pros                    | Cons                          |
|-------------------------|-------------------------------|
| Easy to scale           | Large tokens hurt performance |
| Only validate user once | Tokens never expire           |

#### RemoteUserAuthentication

Rarely used, mostly for intranet sites.

```python
### settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.RemoteUserAuthentication",
    ]
}
```

#### JWTAuthentication

JSON Web Token generated with djangorestframework-simplejwt package.

jwt.io - site to destructuring  JWT token

```python
### settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ]
}
```

| Pros              | Cons              |
|-------------------|-------------------|
| Store more data   | Large size        |
| Signed            | Complicated setup |
| Can be encrypted  | &nbsp;            |
| Can set to expire | &nbsp;            |
# Backend\Django REST Framework\Basics\001_DRF_Basics.md

### DRF Basics

Source: https://testdriven.io/courses/django-rest-framework/intro

#### REST
An API, which stands for Application Programming Interface, is an interface for computers instead of people. It's a method of communication between two machines.

REST, which stands for Representational State Transfer, is an architectural style for providing standards between computer systems on the web. Its purpose is to make it easier for systems to communicate with each other.

For a system to be "RESTful" -- i.e., compliant with REST -- it needs to abide by some rules:

1. **Separation of Concerns**: The client and server are separated
2. **Stateless**: Each request from the client to the server is stateless. In other words, both the client and server can understand any request independently, without seeing any of the previous requests.
3. **Uniformed Interface**: All API endpoints should be accessible by the same approach.

#### Methods

| HTTP   | Method  | 	CRUD Action	Scope | 	Purpose	                                | Structure of URL          |
|--------|---------|--------------------|------------------------------------------|---------------------------|
| GET    | 	Read   | 	collection        | 	Retrieve all resources in a collection	 | api/shopping-items/       |
| GET    | 	Read   | 	single resource   | 	Retrieve a single resource	             | api/shopping-items/<uuid> |
| POST   | 	Create | 	collection        | 	Create a new resource in a collection	  | api/shopping-items/       |
| PUT    | 	Update | 	single resource   | 	Update a single resource	               | api/shopping-items/<uuid> |
| PATCH  | 	Update | 	single resource   | 	Update a single resource	               | api/shopping-items/<uuid> |
| DELETE | 	Delete | 	single resource	  | Delete a single resource	                | api/shopping-items/<uuid> |
# Backend\Django REST Framework\Permissions\001_View_permissions.md

### View Permissions

Source: https://testdriven.io/blog/drf-permissions/

APIView has two methods that check for permissions:

* check_permissions - checks if the request should be permitted based on request data
* check_object_permissions - checks if the request should be permitted based on the combination of the request and object data

```python
### rest_framework/views.py

class APIView(View):
    # other methods
    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )
```
# Backend\Django REST Framework\Permissions\002_Permission_classes.md

### Permission classes

Source: https://testdriven.io/blog/drf-permissions/

#### BasePermission
All permission classes, either custom or built-in, extend from the BasePermission class:
```python
class BasePermission(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
```
As you can see, BasePermission has two methods, has_permission and has_object_permission, that both return True. The permission classes override one or both of the methods to conditionally return True.

#### has_permission

has_permission is used to decide whether a request and a user are allowed to access a specific view

For example:
* Is the request method allowed?
* Is the user authenticated?
* Is the user an admin or super user?

has_permission possesses knowledge about the request, but not about the object of the request.

has_permission (called by check_permissions) gets executed before the view handler is executed, without explicitly calling it.

#### has_object_permission

has_object_permission is used to decide whether a specific user is allowed to interact with a specific object

For example:
* Who created the object?
* When was it created?
* In which group does the object belong to?

Besides the knowledge of the request, has_object_permission also possesses data about the object of the request. The method executes after the object is retrieved from the database.

Unlike has_permission, has_object_permission isn't always executed by default:
* With an APIView, you must explicitly call check_object_permission to execute has_object_permission for all permission classes.
* With ViewSets (like ModelViewSet) or Generic Views (like RetrieveAPIView), has_object_permission is executed via check_object_permission inside a get_object method out of the box.
* has_object_permission is never executed for list views (regardless of the view you're extending from) or when the request method is POST (since the object doesn't exist yet).
* When any has_permission returns False, the has_object_permission doesn't get checked. The request is immediately rejected.

#### Difference between has_permission and has_object_permission

![002_has_permissions_differences.png](_images/002_has_permissions_differences.png)

List views, only has_permission is executed and the request is either granted or refused access. If access is refused, the objects never get retrieved.

Detail views, has_permission is executed and then only if permission is granted, has_object_permission is executed after the object is retrieved.

# Backend\Django REST Framework\Permissions\003_Built_in_permission_classes.md

### Built-in permission classes

Source: https://testdriven.io/blog/built-in-permission-classes-drf/

![003_built_in_permissions.png](_images/003_built_in_permissions.png)

All of those classes, except the last one, DjangoObjectPermissions, override just the has_permission method and inherits the has_object_permission from the BasePermission class. has_object_permission in the BasePermission class always returns True, so it has no impact on object-level access restriction.

#### AllowAny

The most open permission of all is AllowAny. The has_permission and has_object_permission methods on AllowAny always return True without checking anything. Using it isn't necessary (by not setting the permission class, you implicitly set this one), but you still should since it makes the intent explicit and helps to maintain consistency throughout the app.
```python
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny] # built-in permission class used

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
```
#### IsAuthenticated

IsAuthenticated checks if the request has a user and if that user is authenticated. Setting permission_classes to IsAuthenticated means that only authenticated users will be able to access the API endpoint with any of the request methods.

#### IsAuthenticatedOrReadOnly

When permissions are set to IsAuthenticatedOrReadOnly, the request must either have an authenticated user or use one of the safe/read-only HTTP request methods (GET, HEAD, OPTIONS). This means that every user will be able to see all the objects, but only logged-in users will be able to add, change, or delete objects.

#### IsAdminUser

Permissions set to IsAdminUser means that the request needs to have a user and that user must have is_staff set to True. This means that only admin users can see, add, change, or delete objects.

#### DjangoModelPermissions

DjangoModelPermissions allows us to set any combination of permissions to each of the users separately. The permission then checks if the user is authenticated and if they have add, change, or delete user permissions on the model.
```python
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):

    permission_classes = [DjangoModelPermissions]

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
```
You need to set the permissions for the specific user or group:

![003_DjangoModelPermissions.png](_images/003_DjangoModelPermissions.png)

#### DjangoModelPermissionsOrAnonReadOnly

DjangoModelPermissionsOrAnonReadOnly extends the DjangoModelPermissions and only changes one thing: It sets authenticated_users_only to False. 

Anonymous users can see the objects but can't interact with them.

#### DjangoObjectPermissions

While DjangoModelPermissions limits the user's permission for interacting with a model (all the instances), DjangoObjectPermissions limits the interaction to a single instance of the model (an object). To use DjangoObjectPermissions you'll need a permission backend that supports object-level permissions, like django-guardian.

# Backend\Django REST Framework\Permissions\004_Custom_permission_classes.md

### Custom permission classes

Source: https://testdriven.io/blog/custom-permission-classes-drf/

#### BasePermission

All permission classes, either custom or built-in, extend from the BasePermission class:
```python
class BasePermission(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
```

Permission classes override one or both of those methods to conditionally return True. If you don't override the methods, they will always return True, granting unlimited access.

#### Permission based on User properties
```python
### permissions.py

from rest_framework import permissions


class AuthorAllStaffAllButEditOrReadOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
```

#### Permission based on object properties

Let's say you want to restrict access to objects older than 10 minutes for everyone except superusers:

```python
### permissions.py

from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import permissions

class ExpiredObjectSuperuserOnly(permissions.BasePermission):

    def object_expired(self, obj):
        expired_on = timezone.make_aware(datetime.now() - timedelta(minutes=10))
        return obj.created < expired_on

    def has_object_permission(self, request, view, obj):

        if self.object_expired(obj) and not request.user.is_superuser:
            return False
        else:
            return True
```

#### Custom error message

![004_Error_message.png](_images/004_Error_message.png)

Take note of the error message. It's not very informative. The user has no idea why their access was denied. We can create a custom error message by adding a message attribute to our permission class:
```python
class ExpiredObjectSuperuserOnly(permissions.BasePermission):

    message = "This object is expired." # custom error message

    def object_expired(self, obj):
        expired_on = timezone.make_aware(datetime.now() - timedelta(minutes=10))
        return obj.created < expired_on

    def has_object_permission(self, request, view, obj):

        if self.object_expired(obj) and not request.user.is_superuser:
            return False
        else:
            return True
```
# Backend\Django REST Framework\Permissions\005_Global_permissions.md

### Global permissions

Source: https://testdriven.io/blog/built-in-permission-classes-drf/#global-permissions

You can easily set global permission in your settings.py file, using built-in permission classes. For example:
```python
### settings.py

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```
DEFAULT_PERMISSION_CLASSES will only work for the views or objects that don't have permissions explicitly set.
# Backend\Django REST Framework\Permissions\006_Combining_and_Excluding_Permission_Classes.md

### Combining and Excluding Permission Classes

Source: https://testdriven.io/blog/custom-permission-classes-drf/#combining-and-excluding-permission-classes

#### AND operator

AND is the default behavior of permission classes, achieved by using ,:
```python
permission_classes = [IsAuthenticated, IsStaff, SomeCustomPermissionClass]
```

It can also be written with &:
```python
permission_classes = [IsAuthenticated & IsStaff & SomeCustomPermissionClass]
```

#### OR operator

With the OR (|), when any of the permission classes return True, the permission is granted. You can use the OR operator to offer multiple possibilities in which the user gets granted permission.
```python
permission_classes = [IsStaff | IsOwner]
```

#### NOT operator

The NOT operator results in the exact opposite to the defined permission class. In other words, permission is granted to all users except the ones from the permission class.

```python
permission_classes = [~IsFinancesMember] 
```

Be careful! If you only use the NOT operator, everybody else will be allowed access, including unauthenticated users! If that's not what you meant to do, you can fix that by adding another class like so:
```python
permission_classes = [~IsFinancesMember & IsAuthenticated]
```

#### Parentheses

Inside permission_classes you can also use parentheses (()) to control which expression gets resolved first.
```python
permission_classes = [(IsFinancesMember | IsTechMember) & IsOwner]
```
In this example, (IsFinancesMember | IsTechMember) will be resolved first. Then, the result of that will be used with & IsOwner.
# Backend\Django REST Framework\Project_init\001_Installation.md

### Installation
Przykładowa zawartość pliku requirements.txt, którą należy zainstalować.
```
Django==4.1.3  
django-extensions==3.2.1  
django-filter==22.1  
djangorestframework==3.14.0  
djangorestframework-jsonapi==6.0.0
```
# Backend\Django REST Framework\Project_init\002_Settings.md

### Settings

W pliku settings.py dodać zainstalowane pakiety.

```python
### settings.py

INSTALLED_APPS = [  
    'django.contrib.admin',  
  'django.contrib.auth',  
  'django.contrib.contenttypes',  
  'django.contrib.sessions',  
  'django.contrib.messages',  
  'django.contrib.staticfiles',  
  'django_extensions', # Great package to access abstract models  
  'django_filters', # Used with DRF  
  'rest_framework', # DRF package  
]
```
W tym samym pliku dodać słownik REST_FRAMEWORK. Poniżej przykład z bazowymi wartościami z dokumentacji.
 ```python
###settings.py

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
###urls.py

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
# Backend\Django REST Framework\Routers\001_Router_urls.md

### Router urls

Router służy do mapowania ViewSetów na adresy url. Chcąc wykorzystać adresy url zarejestrowane w routerze trzeba rozszerzyć urlpatterns w globalnym pliku urls.py o parametr url routera.

```python
### project/urls.py

from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()), # NEW URL
]
```
# Backend\Django REST Framework\Routers\002_Default_router.md

### DefaultRouter

Jeżeli chcemy dodać url dla obiektu ViewSet (np. dziedziczącego z GenericViewSet) należy go zarejestrować bezpośrednio w routerze.

```python
from ecommerce import views as ecommerce_views  
from rest_framework import routers    
  
router = routers.DefaultRouter()  
router.register(r'item', ecommerce_views.ItemViewSet, basename='item')  
router.register(r'order', ecommerce_views.OrderViewSet, basename='order')
```
# Backend\Django REST Framework\Serializing\001_Serializing_definition.md

### Serializing

Source: https://testdriven.io/courses/django-rest-framework/getting-started/#H-2-serializers

While working with Django, you tend to use complex data types and structures, like model instances. Since those are specific to Django, a client wouldn't know what to do with it. So, complex, Django-specific data structures need to be converted into something less complex that a client knows how to work with. That's what serializers are for. They convert complex data structures to native Python data types. Native data types can then be easily converted to content types, like JSON and XML, that other computers or systems can read and understand:

Django QuerySets -> Python dictionaries -> JSON

This also happens vice versa: Parsed data is deserialized into complex data types:

JSON -> Python dictionaries -> Django QuerySets

While deserializing the data, serializers also perform validation.

Generally, you write your serializers in a serializers.py file. If it becomes too big, you can restructure it into a separate Python package.


# Backend\Django REST Framework\Serializing\002_Base_serializer.md

### Serializer
Wymaga zdefiniowania wszystkich pól, jakie mają być serializowane. Odpowiednik modelu Form z bazowego Django.

Przykładowy model:
```python
### models.py

from django.db import models  
from pygments.lexers import get_all_lexers  
from pygments.styles import get_all_styles  
  
LEXERS = [item for item in get_all_lexers() if item[1]]  
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])  
  
  
class Snippet(models.Model):  
    created = models.DateTimeField(auto_now_add=True)  
    title = models.CharField(max_length=100, blank=True, default='')  
    code = models.TextField()  
    linenos = models.BooleanField(default=False)  
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)  
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)  
  
    class Meta:  
        ordering = ['created']
```
Serializer dla modelu:
```python
### serializers.py

from rest_framework import serializers  
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES  
  
  
class SnippetSerializer(serializers.Serializer):  
    id = serializers.IntegerField(read_only=True)  
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)  
    code = serializers.CharField(style={'base_template': 'textarea.html'})  
    linenos = serializers.BooleanField(required=False)  
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')  
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')  
  
    def create(self, validated_data):  
		"""  
		Create and return a new `Snippet` instance, given the validated data. 
		"""  
		return Snippet.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
		"""  
		Update and return an existing `Snippet` instance, given the validated data. 
		"""  
		instance.title = validated_data.get('title', instance.title)  
		instance.code = validated_data.get('code', instance.code)  
		instance.linenos = validated_data.get('linenos', instance.linenos)  
		instance.language = validated_data.get('language', instance.language)  
		instance.style = validated_data.get('style', instance.style)  
		instance.save()  
		return instance
```
# Backend\Django REST Framework\Serializing\003_Model_serializer.md

### ModelSerializer
Korzysta ze wskazanych pól modelu zdefiniowanego w klasie Meta, możliwe jest jednak dodanie własnych danych. Odpowiednik modelu ModelForm z bazowego Django.

Przykładowy model:
```python
### models.py

from django.db import models  
from utils.model_abstracts import Model  
from django_extensions.db.models import (  
    TimeStampedModel,  
  ActivatorModel,  
  TitleDescriptionModel  
)  
  
  
class Contact(  
    TimeStampedModel,  
  ActivatorModel,  
  TitleDescriptionModel,  
  Model  
):  
    class Meta:  
        verbose_name_plural = "Contacts"  
  
  email = models.EmailField(verbose_name="Email")  
  
    def __str__(self):  
        return f'{self.title}'
```
Serializer dla modelu:
```python
### serializers.py

from . import models  
from rest_framework import serializers  
from rest_framework.fields import CharField, EmailField  
  
  
class ContactSerializer(serializers.ModelSerializer):  
    name = CharField(source="title", required=True)  
    message = CharField(source="description", required=True)  
    email = EmailField(required=True)  
  
    class Meta:  
        model = models.Contact  
        fields = (  
			'name',  
			'email',  
			'message'  
		)
```
# Backend\Django REST Framework\Serializing\004_Serializing_and_deserializing.md

### Proces serializacji i deserializacji
Model:
```python
### models.py

from django.db import models  
from pygments.lexers import get_all_lexers  
from pygments.styles import get_all_styles  
  
LEXERS = [item for item in get_all_lexers() if item[1]]  
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])  
  
  
class Snippet(models.Model):  
    created = models.DateTimeField(auto_now_add=True)  
    title = models.CharField(max_length=100, blank=True, default='')  
    code = models.TextField()  
    linenos = models.BooleanField(default=False)  
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)  
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)  
  
    class Meta:  
        ordering = ['created']
```
Serializer:
```python
### serializers.py

from rest_framework import serializers  
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES  
  
  
class SnippetSerializer(serializers.Serializer):  
    id = serializers.IntegerField(read_only=True)  
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)  
    code = serializers.CharField(style={'base_template': 'textarea.html'})  
    linenos = serializers.BooleanField(required=False)  
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')  
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')  
  
    def create(self, validated_data):  
		"""  
		Create and return a new `Snippet` instance, given the validated data. 
		"""  
		return Snippet.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
		"""  
		Update and return an existing `Snippet` instance, given the validated data. 
		"""  
		instance.title = validated_data.get('title', instance.title)  
		instance.code = validated_data.get('code', instance.code)  
		instance.linenos = validated_data.get('linenos', instance.linenos)  
		instance.language = validated_data.get('language', instance.language)  
		instance.style = validated_data.get('style', instance.style)  
		instance.save()  
		return instance
```

Przy użyciu serializera dla modelu Snippet tworzymy instancję obiektu.

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='print("hello, world")\n')
snippet.save()
```
Serializujemy instancję obiektu przekazując ją do obiektu serializera.
```python
serializer = SnippetSerializer(snippet)
serializer.data
### {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```
Słownik zawarty w zmiennej serializer.data serializujemy przy użyciu klasy JSONRenderer. Uzyskujemy obiekt w postaci bajtowej.
```python
content = JSONRenderer().render(serializer.data)
content
### b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
```
Taki obiekt można również zdeserializować z powrotem do postaci instancji obiektu modelu Django.
```python
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = SnippetSerializer(data=data)
serializer.is_valid()
### True
serializer.validated_data
### OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
### <Snippet: Snippet object>
```
# Backend\Django REST Framework\Serializing\005_Queryset_serializing.md

### Serializowanie querysetów

Do obiektu serializera możliwe jest też przekazanie całego querysetu. W tym celu konieczne jest podanie parametru **many** z wartością **True**.
```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
### [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```
# Backend\Django REST Framework\Serializing\006_extra_kwargs.md

### extra_kwargs
Aby nadpisać niektóre właściwości dla poszczególnych pól można utworzyć zmienną extra_kwargs w klasie Meta serializera:
```python
class UserSerializer(serializers.ModelSerializer):
  class Meta:
      ...
      extra_kwargs = {'password': {
          'write_only': True,  # password will be able to save in POST request, but won't be returned in response
          'min_length': 5
      }}
```
# Backend\Django REST Framework\Serializing\007_Validation.md

### Validation

Source: https://testdriven.io/blog/drf-serializers/

#### Custom field validation
Custom field validation allows us to validate a specific field. We can use it by adding the validate_<field_name> method to our serializer like so:
```python
from rest_framework import serializers
from examples.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating has to be between 1 and 10.')
        return value
```
#### Object-level validation
Sometimes you'll have to compare fields with one another in order to validate them. This is when you should use the object-level validation approach.

Example:
```python
from rest_framework import serializers
from examples.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('US gross cannot be greater than worldwide gross.')
        return data
```
The validate method will make sure us_gross is never bigger than worldwide_gross.

You should avoid accessing additional fields in the custom field validator via self.initial_data. This dictionary contains raw data, which means that your data types won't necessarily match the required data types. DRF will also append validation errors to the wrong field.

#### Functional validators
If we use the same validator in multiple serializers, we can create a function validator instead of writing the same code over and over again. Let's write a validator that checks if the number is between 1 and 10:
```python
def is_rating(value):
    if value < 1:
        raise serializers.ValidationError('Value cannot be lower than 1.')
    elif value > 10:
        raise serializers.ValidationError('Value cannot be higher than 10')
```
We can now append it to our MovieSerializer like so:
```python
from rest_framework import serializers
from examples.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    rating = IntegerField(validators=[is_rating])
    ...
```
# Backend\Django REST Framework\Serializing\008_Custom_output.md

### Custom output

Source: https://testdriven.io/blog/drf-serializers/

Two of the most useful functions inside the BaseSerializer class that we can override are ```to_representation()``` and ```to_internal_value()```. By overriding them, we can change the serialization and deserialization behavior, respectively, to append additional data, extract data, and handle relationships.

* to_representation() allows us to change the serialization output
* to_internal_value() allows us to change the deserialization output
```python
from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(to=User)

    def __str__(self):
        return f'{self.title}'
```
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
```
If we serialize a resource and access its data property, we'll get the following output:
```json
{
   "id": 1,
   "title": "C++ with examples",
   "content": "This is the resource's content.",
   "liked_by": [
      2,
      3
   ]
}
```
#### to_representation()
Now, let's say we want to add a total likes count to the serialized data. The easiest way to achieve this is by implementing the to_representation method in our serializer class:
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()

        return representation
```
This piece of code fetches the current representation, appends likes to it, and returns it.

If we serialize another resource, we'll get the following result:
```json
{
   "id": 1,
   "title": "C++ with examples",
   "content": "This is the resource's content.",
   "liked_by": [
      2,
      3
   ],
   "likes": 2
}
```
#### to_internal_value()
Suppose the services that use our API appends unnecessary data to the endpoint when creating resources:
```json
{
   "info": {
       "extra": "data",
       ...
   },
   "resource": {
      "id": 1,
      "title": "C++ with examples",
      "content": "This is the resource's content.",
      "liked_by": [
         2,
         3
      ],
      "likes": 2
   }
}
```
If we try to serialize this data, our serializer will fail because it will be unable to extract the resource.

We can override to_internal_value() to extract the resource data:
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_internal_value(self, data):
        resource_data = data['resource']

        return super().to_internal_value(resource_data)
```
# Backend\Django REST Framework\Serializing\009_Serializer_context.md

### Serializer context

Source: https://testdriven.io/blog/drf-serializers/

There are some cases when you need to pass additional data to your serializers. You can do that by using the serializer context property. You can then use this data inside the serializer such as to_representation or when validating data.

You pass the data as a dictionary via the context keyword:
```python
from rest_framework import serializers
from examples.models import Resource

resource = Resource.objects.get(id=1)
serializer = ResourceSerializer(resource, context={'key': 'value'})
```
Then you can fetch it inside the serializer class from the self.context dictionary like so:
```python
from rest_framework import serializers
from examples.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['key'] = self.context['key']

        return representation
```
Our serializer output will now contain key with value.
# Backend\Django REST Framework\Serializing\010_Source_keyword.md

### Source keyword

Source: https://testdriven.io/blog/drf-serializers/

The DRF serializer comes with the source keyword, which is extremely powerful and can be used in multiple case scenarios. We can use it to:

* Rename serializer output fields
* Attach serializer function response to data
* Fetch data from one-to-one models

Let's say you're building a social network and every user has their own UserProfile, which has a one-to-one relationship with the User model:
```python
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} profile'
```
We're using a ModelSerializer for serializing our users:
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active']
```

#### Rename serializer output fields

To rename a serializer output field we need to add a new field to our serializer and pass it to fields property.
```python
class UserSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source='is_active')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'active']
Our active field is now going to be named active instead of is_active.
```
#### Attach serializer function response to data
We can use source to add a field which equals to function's return.
```python
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'is_staff', 'active']
```
```get_full_name()``` is a method from the Django user model that concatenates user.first_name and user.last_name.

#### Append data from one-to-one models
Now let's suppose we also wanted to include our user's bio and birth_date in UserSerializer. We can do that by adding extra fields to our serializer with the source keyword.

Let's modify our serializer class:
```python
class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='userprofile.bio')
    birth_date = serializers.DateField(source='userprofile.birth_date')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_staff',
            'is_active', 'bio', 'birth_date'
        ]  # note we also added the new fields here
```
We can access userprofile.<field_name>, because it is a one-to-one relationship with our user.
# Backend\Django REST Framework\Serializing\011_SerializerMethodField.md

### SerializerMethodField

Source: https://testdriven.io/blog/drf-serializers/

SerializerMethodField is a read-only field, which gets its value by calling a method on the serializer class that it is attached to. It can be used to attach any kind of data to the serialized presentation of the object.

SerializerMethodField gets its data by calling get_<field_name>.

If we wanted to add a full_name attribute to our User serializer we could achieve that like this:

from django.contrib.auth.models import User
from rest_framework import serializers

```python
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
```
This piece of code creates a user serializer that also contains full_name which is the result of the get_full_name() function.
# Backend\Django REST Framework\Serializing\012_Different_serializers_for_read_and_write.md

### Different Read and Write Serializers

Source: https://testdriven.io/blog/drf-serializers/

If your serializers contain a lot of nested data, which is not required for write operations, you can boost your API performance by creating separate read and write serializers.

You do that by overriding the ```get_serializer_class()``` method in your ViewSet like so:
```python
from rest_framework import viewsets

from .models import MyModel
from .serializers import MyModelWriteSerializer, MyModelReadSerializer


class MyViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return MyModelWriteSerializer

        return MyModelReadSerializer
```
This code checks what REST operation has been used and returns MyModelWriteSerializer for write operations and MyModelReadSerializer for read operations.
# Backend\Django REST Framework\Serializing\013_Read_only_fields.md

### Read-only Fields

Source: https://testdriven.io/blog/drf-serializers/

Serializer fields come with the read_only option. By setting it to True, DRF includes the field in the API output, but ignores it during create and update operations:
```python
from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = IntegerField(label='ID', read_only=True)
    username = CharField(max_length=32, required=True)
```
Setting fields like id, create_date, etc. to read only will give you a performance boost during write operations.

If you want to set multiple fields to read_only, you can specify them using read_only_fields in Meta like so:
```python
from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = IntegerField(label='ID')
    username = CharField(max_length=32, required=True)

    class Meta:
        read_only_fields = ['id', 'username']
```
# Backend\Django REST Framework\Serializing\014_Nested_serializers.md

### Nested serializers

Source: https://testdriven.io/blog/drf-serializers/

#### Explicit definition

The explicit definition works by passing an external Serializer as a field to our main serializer.

Let's take a look at an example. We have a Comment which is defined like so:
```python
from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
```
Say you then have the following serializer:
```python
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
```
If we serialize a Comment, you'll get the following output:
```json
{
    "id": 1,
    "datetime": "2021-03-19T21:51:44.775609Z",
    "content": "This is an interesting message.",
    "author": 1
}
```
If we also wanted to serialize the user (instead of only showing their ID), we can add an author serializer field to our Comment:
```python
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
```
Serialize again and you'll get this:
```json
{
    "id": 1,
    "author": {
        "id": 1,
        "username": "admin"
    },
    "datetime": "2021-03-19T21:51:44.775609Z",
    "content": "This is an interesting message."
}
```
#### Using the depth field

When it comes to nested serialization, the depth field is one of the most powerful featuress. Let's suppose we have three models -- ModelA, ModelB, and ModelC. ModelA depends on ModelB while ModelB depends on ModelC. They are defined like so:
```python
from django.db import models


class ModelC(models.Model):
    content = models.CharField(max_length=128)


class ModelB(models.Model):
    model_c = models.ForeignKey(to=ModelC, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)


class ModelA(models.Model):
    model_b = models.ForeignKey(to=ModelB, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
```
Our ModelA serializer, which is the top-level object, looks like this:
```python
from rest_framework import serializers


class ModelASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelA
        fields = '__all__'
```
If we serialize an example object we'll get the following output:
```json
{
    "id": 1,
    "content": "A content",
    "model_b": 1
}
```
Now let's say we also want to include ModelB's content when serializing ModelA. We could add the explicit definition to our ModelASerializer or use the depth field.

When we change depth to 1 in our serializer like so:
```python
from rest_framework import serializers


class ModelASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelA
        fields = '__all__'
        depth = 1
```
The output changes to the following:
```json
{
    "id": 1,
    "content": "A content",
    "model_b": {
        "id": 1,
        "content": "B content",
        "model_c": 1
    }
}
```
If we change it to 2 our serializer will serialize a level deeper:
```json
{
    "id": 1,
    "content": "A content",
    "model_b": {
        "id": 1,
        "content": "B content",
        "model_c": {
            "id": 1,
            "content": "C content"
        }
    }
}
```
The downside is that you have no control over a child's serialization. Using depth will include all fields on the children, in other words.

The authors of Two Scoops of Django argue that you should remove any POST or PUT methods for nested resources and create separate GET/POST/PUT API views for them. From my own experience, they're right: Trying to use a writable nested serializer can quickly become irritating.
# Backend\Django REST Framework\Serializing\015_Eager_loading.md

### Eager loading

Source: https://rex-chiang.medium.com/django-rest-framework-eager-loading-a67e6be15b3

#### Implementation example

```python
class EagerLoadingMixin:
  @classmethod
  def setup_eager_loading(cls, queryset):
    if hasattr(cls, "SELECT"):
      queryset = queryset.select_related(*cls.SELECT)

    if hasattr(cls, "PREFETCH"):
      queryset = queryset.prefetch_related(*cls.PREFETCH)

    return queryset
```

```python
class OrderSerializer(ModelSerializer, EagerLoadingMixin):
  account = AccountSerializer()
  product = productSerializer()
  coupon = couponSerializer()

  SELECT = ["account", "coupon"]
  PREFETCH = ["product"]
```

```python
orders = Order.objects.all()
queryset = OrderSerializer.setup_eager_loading(orders)
data = OrderSerializer(queryset, many=True).data
```
# Backend\Django REST Framework\Testing\001_APITestCase.md

### APITestCase
DRF zapewnia moduł wspierający testowanie napisanego API. W tym celu należy zaimportować klasę APITestCase z modułu rest_framework.test
```python
### tests.py

from rest_framework.test import APITestCase  
  
class ContactTestCase(APITestCase):  
    """  
    Test suite for Contact 
    """
    pass
```
# Backend\Django REST Framework\Testing\002_setUp.md

### setUp
Zdefiniowanie metody setUp() w klasie dziedziczącej po klasie APITestCase pozwala sprawia, że kod, napisany w tej metodzie wykona się przed wykonaniem zestawu testów zdefiniowanym w klasie.

```python
### tests.py

from rest_framework.test import APIClient  
from rest_framework.test import APITestCase   


class ContactTestCase(APITestCase):  
    """  
 Test suite for Contact """  
  def setUp(self):  
        self.client = APIClient()  
        self.data = {  
			"name": "Billy Smith",  
			"message": "This is a test message",  
			"email": "billysmith@test.com"  
		}  
        self.url = "/contact/"
```
# Backend\Django REST Framework\Testing\003_Creating_unit_tests.md

### Tworzenie unit testów
Testy tworzone są jako metody dla klasy dziedziczącej po APITestCase. Przykładowy unit test:
```python
from .models import Contact  
from rest_framework.test import APIClient  
from rest_framework.test import APITestCase  
from rest_framework import status  
  
  
class ContactTestCase(APITestCase):  
	...    
	def test_create_contact(self):  
		'''  
		test ContactViewSet create method 
		'''  
		data = self.data  
		response = self.client.post(self.url, data)  
		self.assertEqual(response.status_code, status.HTTP_200_OK)  
		self.assertEqual(Contact.objects.count(), 1)  
		self.assertEqual(Contact.objects.get().title, "Billy Smith")
```
# Backend\Django REST Framework\Testing\004_Running_tests.md

### Uruchomienie testów
Uruchomienie wszystkich istniejących w projekcie testów odbywa się poprzez uruchomienie komendy:
```
python manage.py test
```
# Backend\Django REST Framework\Throttling\001_Throttling.md

### Throttling

Source: https://testdriven.io/courses/django-rest-framework/user-management/#H-4-throttling

As with permissions, throttling is used to determine if the request should be authorized. The difference is that throttling is a temporary state while user permissions are more or less permanent. In essence, throttling controls the rate of requests that clients can make to an API. When the throttling rate is exceeded, DRF returns a 429 Too Many Requests status.

Throttling can help improve the user experience and protect against slow performance or DoS (denial-of-service) attacks.

DRF provides two types of throttle classes:
1. `UserRateThrottle` - used to throttle authenticated users
2. `AnonRateThrottle` - used to throttle unauthenticated users

You can also create your own throttle class.

#### Default

As with the other default DRF settings, you can configure the default settings in the REST_FRAMEWORK dict in the settings.py file.

For the throttling to work, you need to add two settings:

1. `DEFAULT_THROTTLE_CLASSES` - determines how the throttle works (e.g., authenticated/unauthenticated users, scope)
2. `DEFAULT_THROTTLE_RATES` - determines how many requests are allowed (e.g., n/hour, n/second).

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/hour",
        "user": "2/hour"
    },
}
```

#### Custom

Let's create a throttle limitation per day and minute separately. That way, you avoid slow performance of your API and at the same time ensure the client has enough requests available throughout the day.

We need to create multiple UserRateThrottles to achieve that, one for a daily rate and one for a rate per minute.

```python
### shopping_list/api/throttling.py


from rest_framework.throttling import UserRateThrottle


class MinuteRateThrottle(UserRateThrottle):
    scope = "user_minute"


class DailyRateThrottle(UserRateThrottle):
    scope = "user_day"
```

Here, we simply set a unique scope, so we can then set the rate numbers in settings.

Back in core/settings.py, update `DEFAULT_THROTTLE_CLASSES` and `DEFAULT_THROTTLE_RATES` like so:

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "shopping_list.api.throttling.MinuteRateThrottle",
        "shopping_list.api.throttling.DailyRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/hour",
        "user_day": "10000/day",
        "user_minute": "200/minute",
    },
}
```
# Backend\Django REST Framework\Versioning\001_Versioning.md

### Versioning

Source: https://testdriven.io/courses/django-rest-framework/api-versioning/

When maintaining a real-life RESTful API, you'll sooner or later need to make some breaking changes. Changes need to be introduced incrementally and transparently -- both of which you can achieve via versioning.

DRF supports multiple versioning schemes:

1. AcceptHeaderVersioning
2. URLPathVersioning
3. NamespaceVersioning
4. HostNameVersioning
5. QueryParameterVersioning

#### Setup

For example, you could update the ShoppingListDetail view to choose the serializer based on the version parameter:
```python
### shopping_list/api/views.py


from shopping_list.api.serializers import ShoppingListSerializer,ShoppingListSerializerV2

class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    permission_classes = [ShoppingListMembersOnly]

    def get_serializer_class(self):
        if self.request.version == "v2":
            return ShoppingListSerializerV2
        return ShoppingListSerializer
```
The second version of the serializer would look something like this:

```python
### shopping_list/api/serializers.py


### original serializer:
class ShoppingListSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    unpurchased_items = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = ["id", "name", "unpurchased_items", "members", "last_interaction"]

    def get_unpurchased_items(self, obj) -> List[UnpurchasedItem]:
        return [{"name": shopping_item.name} for shopping_item in obj.shopping_items.filter(purchased=False)][:3]

### new serializer:
class ShoppingListSerializerV2(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    unpurchased_items = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = ["id", "name", "unpurchased_items", "members"]  # last_interaction removed

    def get_unpurchased_items(self, obj) -> List[UnpurchasedItem]:
        return [{"name": shopping_item.name} for shopping_item in obj.shopping_items.filter(purchased=False)][:3]
```
Now let's see how to get DRF to use different serializers based on the incoming request for different types of versioning.

#### AcceptHeaderVersioning

According to the DRF docs, versioning based on accept headers is considered the best practice.

In short, DRF gets info about the version from the HTTP request Accept header.

To use AcceptHeaderVersioning, inside REST_FRAMEWORK settings within the settings.py file, set DEFAULT_VERSIONING_CLASS to AcceptHeaderVersioning:

```python
### core/settings.py


REST_FRAMEWORK = {
 # ...
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
}
```

![versioning.png](_images/versioning_01.png)

#### URLPathVersioning

With URLPathVersioning, the URL pattern includes a version key argument -- e.g., v1/api/ or v2/api.

```python
### core/settings.py


REST_FRAMEWORK = {
    # other DRF settings
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
}
```

Add a second version URL pattern to the urls.py file:

```python
### core/urls.py


from django.urls import path, re_path

urlpatterns = [
    # ...
    path("api/shopping-lists/<uuid:pk>/", ShoppingListDetail.as_view(), name="shopping-list-detail"), # removing this url would be a breaking change
    re_path(r"(?P<version>(v2))/api/shopping-lists/(?P<pk>\S+)/$", ShoppingListDetail.as_view(), name="shopping-list-detail-v2"), # adding url for the same view with versioning
]
```
#### NamespaceVersioning

NamespaceVersioning is the same as the URLPathVersioning for the client. The only difference is that it uses namespaces instead of URL keyword arguments.

In the core urls.py file, you just need to add a namespace like so:

```python
### core/urls.py


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shopping_list.urls", namespace="v1")),
    path("v2/", include("shopping_list.urls", namespace="v2")),
]
```
Now, the namespace will be passed to all the included URLs.

Without any additional change, now if you navigate to http://127.0.0.1:8000/v2/api/shopping-lists/<SHOPPING-LIST-UUID>/, you'll see that the second serializer is used. The result is the same as with URLPathVersioning.

#### HostNameVersioning

HostNameVersioning gets the requested version based on the hostname.

To use it, DEFAULT_VERSIONING_CLASS must be set to HostNameVersioning:

```python
### core/settings.py


REST_FRAMEWORK = {
    # other DRF settings
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.HostNameVersioning",
}
```

Now a subdomain can serve a different version of the app.

Main domain:
![versioning_02.png](_images/versioning_02.png)
Subdomain:
![versioning_03.png](_images/versioning_03.png)

#### QueryParameterVersioning

QueryParameterVersioning allows a client to include the version as a query parameter -- e.g., api?version=v1 or api?version=v2.

Change the DEFAULT_VERSIONING_CLASS to URLPathVersioning:

```python
### core/settings.py


REST_FRAMEWORK = {
    # other DRF settings
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning",
}
```

You can test this option directly in the browser by adding a query parameter to the URL: http://127.0.0.1:8000/v2/api/shopping-lists/<SHOPPING-LIST-UUID>/?version=v2.


# Backend\Django REST Framework\Views\001_APIView.md

### API View

Source: https://testdriven.io/blog/drf-views-part-1/

#### Intro
APIView class is a base for all the views that you might choose to use in your DRF application.

![001_APIView.png](_images/001_APIView.png)

#### Example
```python
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    done = models.BooleanField()
```
Here's a view that allows users to delete all the items at once:

```python
from rest_framework.response import Response
from rest_framework.views import APIView

class DeleteAllItems(APIView):

    def delete(self, request):

        Item.objects.all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
```
And here's a view that lists all the items:
```python
from rest_framework.response import Response
from rest_framework.views import APIView

class ListItems(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
```
The call to the database is done inside the handler functions. They're selected according to the request's HTTP method (e.g., GET -> get, DELETE -> delete).

#### Policy attributes

| Attribute                 | 	Usage	                                                                                                                         | Examples                                    |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| renderer_classes          | determines which media types the response returns	                                                                              | JSONRenderer, BrowsableAPIRenderer          |
| parser_classes            | determines which data parsers for different media types are allowed	                                                            | JSONParser, FileUploadParser                |
| authentication_classes    | determines which authentication schemas are allowed for identifying the user                                                    | 	TokenAuthentication, SessionAuthentication |
| throttle_classes          | determines if a request should be authorized based on the rate of requests	                                                     | AnonRateThrottle, UserRateThrottle          |
| permission_classes        | determines if a request should be authorized based on user credentials	                                                         | IsAuthenticated, DjangoModelPermissions     |
| content_negotiation_class | selects one of the multiple possible representations of the resource to return to a client (unlikely you'll want to set it up)	 | only custom content negotiation classes     |
# Backend\Django REST Framework\Views\002_Function_view.md

### Function-based Views

Source: https://testdriven.io/blog/drf-views-part-1/

#### Intro
If you're writing a view in the form of a function, you'll need to use the @api_view decorator.

@api_view is a decorator that converts a function-based view into an APIView subclass (thus providing the Response and Request classes). It takes a list of allowed methods for the view as an argument.

#### Example
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['DELETE'])
def delete_all_items(request):
    Item.objects.all().delete()
    return Response(status=status.HTTP_200_OK)
```

#### Policy Decorators

* @renderer_classes
* @parser_classes
* @authentication_classes
* @throttle_classes
* @permission_classes

Those decorators correspond to APIView subclasses. Because the @api_view decorator checks if any of the following decorators are used, they need to be added below the api_view decorator

```python
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # policy decorator
@renderer_classes([JSONRenderer])       # policy decorator
def items_not_done(request):
    user_count = Item.objects.filter(done=False).count()
    content = {'not_done': user_count}

    return Response(content)
```
# Backend\Django REST Framework\Views\003_GenericAPIView_and_Mixins.md

### GenericAPIView and mixins

Source: https://testdriven.io/blog/drf-views-part-1/

#### GenericAPIView

GenericAPIView is a base class for all other generic views. It provides methods like get_object/get_queryset and get_serializer. Although it's designed to be combined with mixins (as it's used within generic views), it's possible to use it on its own:
```python
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class RetrieveDeleteItem(GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 ```       
When extending GenericAPIView, queryset and serializer_class must be set. Alternatively, you can overwrite get_queryset()/get_serializer_class().

#### Mixins

|Mixin |	Usage|
|-|-|
|CreateModelMixin |	Create a model instance|
|ListModelMixin |	List a queryset|
|RetrieveModelMixin |	Retrieve a model instance|
|UpdateModelMixin |	Update a model instance|
|DestroyModelMixin |	Delete a model instance|

Here's an example of what a mixin looks like:
```python
class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

Example usage of mixins:
```python
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

class CreateListItems(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 ```       
In CreateListItems we used the serializer_class and queryset provided by GenericAPIView.

We defined get and post methods on our own, which used list and create actions provided by the mixins:

* CreateModelMixin provides a create action
* ListModelMixin provides a list action

**You're responsible for binding actions to the methods.**

Theoretically, that means that you could bind POST methods with list actions and GET methods with create actions, and things would "kind" of work.

**It's a good idea to have a single view for handling all instances -- listing all instances and adding a new instance -- and another view for handling a single instance -- retrieving, updating, and deleting single instances.**
# Backend\Django REST Framework\Views\004_Concrete_views.md

### Concrete Views

Concrete views do most of the work that we need to do on our own when using APIView. They use mixins as their basic building blocks, combine the building blocks with GenericAPIView, and bind actions to the methods.

Example:
```python
class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```        

|Class|	Usage|	Method handler	|Extends mixin|
|-|-|-|-|
|CreateAPIView|	create-only|	post|	CreateModelMixin|
|ListAPIView|	read-only for multiple instances|	get|	ListModelMixin|
|RetrieveAPIView|	read-only for single instance	|get	|RetrieveModelMixin|
|DestroyAPIView|	delete-only for single instance	|delete	|DestroyModelMixin|
|UpdateAPIView|	update-only for single instance	put, |patch|	UpdateModelMixin|
|ListCreateAPIView|	read-write for multiple instances	|get, post|	CreateModelMixin, ListModelMixin|
|RetrieveUpdateAPIView|	read-update for single instance	|get, put, patch	|RetrieveModelMixin, UpdateModelMixin|
|RetrieveDestroyAPIView|	read-delete for single instance	|get, delete	|RetrieveModelMixin, DestroyModelMixin|
|RetrieveUpdateDestroyAPIView|	read-update-delete for single instance|	get, put, patch, delete	|RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin|

![003_Concrete_views.png](003_Concrete_views.png)

All classes that extend from a concrete view need:

* queryset
* serializer class
# Backend\Django REST Framework\Views\005_ViewSet.md

### ViewSets

Source: https://testdriven.io/blog/drf-views-part-3/

ViewSet is a type of class-based view.

Instead of method handlers, like .get() and .post(), it provides actions, like .list() and .create().

The most significant advantage of ViewSets is that the URL construction is handled automatically (with a router class). This helps with the consistency of the URL conventions across your API and minimizes the amount of code you need to write.

There are four types of ViewSets, from the most basic to the most powerful:

* ViewSet
* GenericViewSet
* ReadOnlyModelViewSet
* ModelViewSet

![005_ViewSet.png](_images/005_ViewSet.png)

#### Base ViewSet

The ViewSet class takes advantage of the APIView class. It doesn't provide any actions by default, but you can use it to create your own set of views:
```python
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class ItemViewSet(ViewSet):
    queryset = Item.objects.all()

    def list(self, request):
        serializer = ItemSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
```

#### Actions

Possible actions:
* list
* create
* retrieve (pk needed)
* update (pk needed)
* partial_update (pk needed)
* destroy (pk needed)

You can also create custom actions with the @action decorator.

For example:

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
```python
class ItemsViewSet(ViewSet):

    queryset = Item.objects.all()

    def list(self, request):
        serializer = ItemSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def items_not_done(self, request):
        user_count = Item.objects.filter(done=False).count()

        return Response(user_count)
```

The detail parameter should be set as True if the action is meant for a single object or False if it's meant for all objects.
# Backend\Django REST Framework\Views\006_Routers.md

### Routers

Source: https://testdriven.io/blog/drf-views-part-3/

Instead of using Django's urlpatterns, ViewSets come with a router class that automatically generates the URL configurations.

DRF comes with two routers out-of-the-box:

* SimpleRouter
* DefaultRouter

The main difference between them is that DefaultRouter includes a default API root view.

Routers can also be combined with urlpatterns:
```python
### urls.py

from django.urls import path, include
from rest_framework import routers

from .views import ChangeUserInfo, ItemsViewSet

router = routers.DefaultRouter()
router.register(r'custom-viewset', ItemsViewSet)

urlpatterns = [
    path('change-user-info', ChangeUserInfo.as_view()),
    path('', include(router.urls)),
]
```

Here's how the router maps methods to actions:
```python
### https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/routers.py#L83

routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
```
# Backend\Django REST Framework\Views\007_GenericViewSet.md

### GenericViewSet

Source: https://testdriven.io/blog/drf-views-part-3/

While ViewSet extends APIView, GenericViewSet extends GenericAPIView.
```python
### https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/viewsets.py#L210
class ViewSet(ViewSetMixin, views.APIView):
   pass


### https://github.com/encode/django-rest-framework/blob/3.12.4/rest_framework/viewsets.py#L217
class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
   pass
```

#### Using GenericViewSet with Mixins
```python
from rest_framework import mixins, viewsets

class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
```

#### Using GenericViewSet with Explicit Action Implementations

```python
from rest_framework import status
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

class ItemViewSet(GenericViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [DjangoObjectPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```


# Backend\Django REST Framework\Views\008_ModelViewSet.md

### ModelViewSets

Source: https://testdriven.io/blog/drf-views-part-3/

#### ModelViewSet

ModelViewSet provides default create, retrieve, update, partial_update, destroy and list actions since it uses GenericViewSet and all of the available mixins.

ModelViewSet is the easiest of all the views to use. You only need three lines:
```python
class ItemModelViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
```
#### ReadOnlyModelViewSet

ReadOnlyModelViewSet is a ViewSet that provides only list and retrieve actions by combining GenericViewSet with the RetrieveModelMixin and ListModelMixin mixins.

Like ModelViewSet, ReadOnlyModelViewSet only needs the queryset and serializer_class attributes to work:
```python
from rest_framework.viewsets import ReadOnlyModelViewSet

class ItemReadOnlyViewSet(ReadOnlyModelViewSet):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()
```
# Backend\Django REST Framework\Views\009_Renderers.md

### DRF Renderers

Source: https://testdriven.io/courses/django-rest-framework/manual-testing/#H-6-default-renderer

To render data in JSON, you need to change DEFAULT_RENDERER_CLASSES inside your settings.py file:

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}
```

If you, for some reason, want only one view to be rendered as JSON, you can set it in renderer_classes inside the view.

```python
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from shopping_list.api.serializers import ShoppingItemSerializer
from shopping_list.models import ShoppingItem


class ShoppingItemViewSet(ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    renderer_classes = [JSONRenderer]
```
# Backend\Django REST Framework\Views\010_Custom_view_actions.md

### Custom actions

Source: https://testdriven.io/courses/django-rest-framework/custom-actions/

```python
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shopping_list.api.serializers import ShoppingItemSerializer
from shopping_list.models import ShoppingItem


class ShoppingItemViewSet(ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer

    @action(detail=False, methods=['DELETE'], url_path='delete-all-purchased', url_name='delete-all-purchased')
    def delete_purchased(self, request):
        ShoppingItem.objects.filter(purchased=True).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
```

Here, we added a delete_purchased method that deletes all purchased items, decorated with the @action decorator.

Parameters for the @action decorator:

1. `detail` is the only required parameter. It determines whether this action applies to detail requests or list requests.
2. `methods` is a list of HTTP methods that this action responds to. If it's not set, it defaults to the GET method.
3. `url_path` defines the URL segment for this action. If it's not set, it defaults to the name of the method.
4. `url_name` defines the reverse URL name for this action. If it's not set, it's the name of the method; underscores are replaced with dashes.

Although not strictly needed, we've set the url_path and url_name so our naming remains consistent.
# Backend\Luigi\001_Task.md

## Luigi task

Sources: 
* https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-2-creating-a-luigi-task
* https://medium.com/big-data-processing/getting-started-with-luigi-what-why-how-f8e639a1f2a5

A Luigi task is where the execution of your pipeline and the definition of each task’s input and output dependencies take place. Tasks are the building blocks that you will create your pipeline from. You define them in a class, which contains:
* A `run()` method that holds the logic for executing the task.
* An `output()` method that returns the artifacts generated by the task. The run() method populates these artifacts.
* An optional `input()` method that returns any additional tasks in your pipeline that are required to execute the current task. The `run()` method uses these to carry out the task.

```python
## hello-world.py

import luigi
from luigi import Task

class HelloWorld(Task):

    def output(self):
        return luigi.LocalTarget('result.txt')

    def run(self):
        print("hello")
        with self.output().open('w') as f:
            f.write('Hello world')

if __name__ == '__main__':
    luigi.run(['HelloWorld', '--local-scheduler'])
```

You define that HelloLuigi() is a Luigi task by adding the luigi.Task mixin to it.

The output() method defines one or more Target outputs that your task produces. In the case of this example, you define a luigi.LocalTarget, which is a local file.

To execute the task you created, run the following command:

```commandline
python -m luigi --module hello-world HelloWorld --local-scheduler
```

Here, you run the task using python -m instead of executing the luigi command directly; this is because Luigi can only execute code that is within the current PYTHONPATH. You can alternatively add PYTHONPATH='.' to the front of your Luigi command, like so:

```commandline
PYTHONPATH='.' luigi --module hello-world HelloLuigi --local-scheduler
```

With the `--module hello-world HelloLuigi` flag, you tell Luigi which Python module and Luigi task to execute.

The `--local-scheduler` flag tells Luigi to not connect to a Luigi scheduler and, instead, execute this task locally. Running tasks using the local-scheduler flag is only recommended for development work.

# Backend\Luigi\002_Scheduler.md

## Luigi Scheduler

Source: https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-4-running-the-luigi-scheduler

So far, you have been running Luigi using the --local-scheduler tag to run your jobs locally without allocating work to a central scheduler. This is useful for development, but for production usage it is recommended to use the Luigi scheduler. The Luigi scheduler provides:

* A central point to execute your tasks.
* Visualization of the execution of your tasks.

To access the Luigi scheduler interface, you need to enable access to port 8082.

To run the scheduler execute the following command:
```commandline
luigid --port 8082 --background
```

Open a browser to access the Luigi interface. This will either be at http://localhost:8082/

By default, Luigi tasks run using the Luigi scheduler. To run one of your previous tasks using the Luigi scheduler omit the --local-scheduler argument from the command.

```commandline
python -m luigi --module word-frequency GetTopBooks
```
# Backend\Luigi\003_Parameters.md

## Luigi parameters

Sources: 
* https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-5-downloading-the-books
* https://medium.com/big-data-processing/getting-started-with-luigi-setting-up-pipelines-9547edefe782

Luigi has few different type of parameters which is self describing by their names. These parameters are

* IntParameter for integers values
* BoolParameter for boolean values
* Parameter for strings and other values
* DateParameter for date data types
* ListParameter for passing the list
* DictParameter for a dictionary of items

```python
## word-frequency.py

class DownloadBooks(luigi.Task):
    """
    Download a specified list of books
    """
    FileID = luigi.IntParameter()

    REPLACE_LIST = """.,"';_[]:*-"""

    def requires(self):
        return GetTopBooks()

    def output(self):
        return luigi.LocalTarget("data/downloads/{}.txt".format(self.FileID))

    def run(self):
        with self.input().open("r") as i:
            URL = i.read().splitlines()[self.FileID]

            with self.output().open("w") as outfile:
                book_downloads = requests.get(URL)
                book_text = book_downloads.text

                for char in self.REPLACE_LIST:
                    book_text = book_text.replace(char, " ")

                book_text = book_text.lower()
                outfile.write(book_text)
```

In this task you introduce a Parameter; in this case, an integer parameter. Luigi parameters are inputs to your tasks that affect the execution of the pipeline. Here you introduce a parameter FileID to specify a line in your list of URLs to fetch.

```commandline
python -m luigi --module word-frequency DownloadBooks --FileID 2
```
# Backend\Luigi\004_Config.md

## Luigi config

Source: https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-7-defining-configuration-parameters

When you want to set parameters that are shared among tasks, you can create a Config() class. Other pipeline stages can reference the parameters defined in the Config() class; these are set by the pipeline when executing a job.

```python
class GlobalParams(luigi.Config):
    NumberBooks = luigi.IntParameter(default=10)
    NumberTopWords = luigi.IntParameter(default=500)

    
class TopWords(luigi.Task):
    """
    Aggregate the count results from the different files
    """

    def requires(self):
        requiredInputs = []
        for i in range(GlobalParams().NumberBooks):
            requiredInputs.append(CountWords(FileID=i))
        return requiredInputs

    def output(self):
        return luigi.LocalTarget("data/summary.txt")

    def run(self):
        total_count = Counter()
        for input in self.input():
            with input.open("rb") as infile:
                nextCounter = pickle.load(infile)
                total_count += nextCounter

        with self.output().open("w") as f:
            for item in total_count.most_common(GlobalParams().NumberTopWords):
                f.write("{0: <15}{1}\n".format(*item))
```

Config values may be overridden in command.

```commandline
python -m luigi --module word-frequency TopWords --GlobalParams-NumberBooks 15 --GlobalParams-NumberTopWords 750
```
# Backend\pytest\001_Installation.md

## Instalacja
Instalacja biblioteki pytest oraz pluginu do sprawdzenia pokrycia kodu testami.
```commandline
pip install pytest
pip install pytest-cov
```
# Backend\pytest\002_Base_operations.md

## Podstawowe operacje
Żeby zdefiniować test konieczne jest utworzenie funkcji rozpoczynającej się od słowa "test". Przykład:
```python
def test_sum() -> None:  
    a = 1
    b = 2  
    assert a + b == 3
```
Uruchomienie testów w bieżącym katalogu:
```commandline
pytest
```
Uruchomienie sprawdzenia pokrycia kodu testami:
```commandline
pytest --cov
```
Raport o pokryciu testami i ze wskazaniem nieprzetestowanych fragmentów kodu:
```commandline
coverage html
```
## Uruchomienie testów
W celu uruchomienia napisanych testów w konsoli należy wpisać następującą komendę:
```
py.test
```
# Backend\pytest\003_Exceptions_testing.md

## Testowanie wyjątków
Jeżeli dany test ma sprawdzić wystąpienie wyjątku, należy użyć konstrukcji **with pytest.raises([nazwa_wyjątku])**.
```python
from pay.processor import PaymentProcessor  
import pytest  
  
API_KEY = "6cfb67f3-6281-4031-b893-ea85db0dce20"  

def test_api_key_invalid() -> None:  
    with pytest.raises(ValueError):  
        processor = PaymentProcessor("")  
        processor.charge("1249190007575069", 12, 2024, 100)
```
# Backend\pytest\004_Parametrize.md

## Parametryzacja testów
Żeby uniknąć konieczności kopiowania i wykonywania testów dla różnych danych możliwe jest parametryzowanie testów.
Testujemy metodę find_hashtags() klasy Twitter, która wyszukuje słów oznaczonych hashtagiem w podanej wiadomości.
```python
class Twitter:  
	...  
    def find_hashtags(self, message):  
        return [m.lower() for m in re.findall("#(\w+)", message)]
```
Żeby przetestować różne przypadki test dla takiej metody można sparametryzować używając dekoratora @pytest.mark.parametrize.
```python
@pytest.mark.parametrize("message, expected", (  
	("Test #first message", ["first"]),  
	("#first Test message", ["first"]),  
	("#FIRST Test message", ["first"]),  
	("Test message #first", ["first"]),  
	("Test message #first #second", ["first", "second"]),  
))  
def test_tweet_with_hashtag(message, expected):  
    twitter = Twitter()  
    assert twitter.find_hashtags(message) == expected
```

Jako pierwszy argument dekoratora podane są nazwy zmiennych, które chcemy przekazać do testu (w tym przypadku "message" oraz "expected"). Jako drugi argument przekazana jest tupla, zawierające poszczególne zestawy wartości do testowania.

# Backend\pytest\005_Fixture.md

## Fixtures
### Podstawowy fixture
W celu przygotowania parametrów wejściowych do testów, które można wielokrotnie wykorzystać używa się tzw. fixtures. 
Mamy dwa testy testujące klasę Twitter. W obu tych testach inicjalizowany jest obiekt klasy Twitter.
```python
def test_twitter_initialization():
	twitter = Twitter()
    assert twitter

def test_tweet_single_message():  
    twitter = Twitter()  
    twitter.tweet('Test message')  
    assert twitter.tweets == ['Test message']
```
Żeby uniknąć takiej redundancji można utworzyć fixture przy użyciu dekoratora @pytest.fixture.
```python
@pytest.fixture  
def twitter():  
    twitter = Twitter()  
    return twitter
```
Tak zdefiniowany dekorator można przekazać do testu jako argument o takiej samej nazwie, jak nazwa fixture'a.
```python
def test_twitter_initialization(twitter):  
    assert twitter  
  
def test_tweet_single_message(twitter):  
    twitter.tweet('Test message')  
    assert twitter.tweets == ['Test message']
```
### Fixture jako generator
Fixture z punktu 7.1. można również napisać w formie generatora.
```python
@pytest.fixture  
def twitter():  
    twitter = Twitter()  
    yield twitter  
    twitter.delete()
```
W takiej sytuacji w momencie wykonywania testu na fixturze będącym generatorem wykonywana jest po raz pierwszy metoda \_\_next\_\_(), która zwraca obiekt klasy Twitter. W momencie zakończenia testu na fixturze wykonywana jest po raz drugi metoda \_\_next\_\_, co zgodnie z działaniem generatorów prowadzi do wykonania metody twitter.delete() i zwrócenia wyjątku StopIteration. Mechanizm ten jest często wykorzystywany w testach do wykonania dodatkowych operacji przy zakończeniu testu.
### Request jako argument fixture'a
Do fixture'a można również przekazać argument request, który zawiera dodatkowe dane związane z kontekstem wykonywanego testu.
```python
@pytest.fixture  
def twitter(request):  
    twitter = Twitter()  
    yield twitter  
    twitter.delete()
```
### Parametryzacja fixture'ów
Request można również wykorzystać do parametryzowania fixture'ów. W fixturze twitter chcemy zainicjować klasę Twitter z dwoma różnymi parametrami. W tym celu do dekoratora przekazujemy żądane parametry w zmiennej param.
```python
@pytest.fixture(params=[None, 'test.txt'])  
def twitter(request):  
    twitter = Twitter(backend=request.param)  
    yield twitter  
    twitter.delete()
```
W takiej sytuacji wszystkie testy wykorzystujące ten fixture zostaną wykonane dwukrotnie - raz z wartością parametru None, a raz z wartością 'test.txt'.
### Tymczasowe pliki
Aby utworzyć tymczasowe pliki w ramach fixture'a możliwe jest skorzystanie z tymczasowej ścieżki tmpdir. Po wykonaniu testu plik taki zostanie natychmiastowo usunięty.
```python
@pytest.fixture  
def backend(tmpdir):  
    temp_file = tmpdir.join('test.txt')  
    temp_file.write('')  
    return temp_file
```
### getfixturevalue
Istnieje możliwość niepodawania fixture'a jako argumentu testu, ale wyciągnięcie go przy użyciu jego nazwy. Jest to przydatne w sytuacji, gdzie ten sam test chcemy wykonać dla różnych fixture'ów. Nie działa to jednak dobrze w przypadku sparametryzowanych fixture'ów.
```python
@pytest.mark.parametrize('file_type', ('zip_file', 'tar_file'))
def test_file(self, file_type: str, request):
	file = request.getfixturevalue(file_type)
	...
```
### yield in fixture

You can run part of a fixture before and part after a test using yield instead of return. For example:
```python
@pytest.fixture
def some_fixture():
    # do something before your test
    yield # test runs here
    # do something after your test
```

```python
@pytest.fixture(autouse=True)
def database():
    _, file_name = tempfile.mkstemp()
    os.environ["DATABASE_NAME"] = file_name
    Article.create_table(database_name=file_name)
    yield
    os.unlink(file_name)
```

# Backend\pytest\006_Monkey_patching.md

## Monkey patching
Monkey patching "nadpisuje" elementy programu np. funkcje innymi mechanizmami. Poniżej przyklad zastąpienia funkcji input.

```python
from pay.order import LineItem, Order  
from pay.payment import pay_order  
from pytest import MonkeyPatch  
  

## klasa MonkeyPatch musi być przekazana jako argument funkcji
def test_pay_order(monkeypatch: MonkeyPatch) -> None:
	# Przygotowanie inputów  
    inputs = ["1249190007575069", "12", "2024"]  
    # Zastąpienie domyślnego wywołania funkcji input przez zwrócenie pierwszego elementu listy inputs
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))  
    order = Order()  
    order.line_items.append(LineItem("Test", 100))  
    pay_order(order)
```
Do monkey patchingu można wykorzystać też funkcjonalność fixture'ów. Poniżej przykład zablokowania możliwości wykorzystania metody request. Parametr autouse wskazuje, że fixture ten będzie wykonany przed każdym testem.
```python
@pytest.fixture(autouse=True)  
def no_requests(monkeypatch):  
    monkeypatch.delattr('requests.sessions.Session.request')
```
# Backend\pytest\007_Mocking.md

## Mockowanie
W celu zastąpienia pewnych obiektów / systemów w ramach testowania wykorzystywane jest tzw. mockowanie. Proces ten polega na umieszczeniu "atrapy" domyślnie używanego obiektu, która przejmie jego funkcje w czasie testowania. Jest to bardziej zaawansowana forma monkey patchingu.
### unittest
Możliwe jest użycie metody context managera patch z biblioteki unittest, który dla wskazanej funkcji zwraca określoną w zmiennej return_value wartość.
```python
from unittest.mock import patch

def test_tweet_single_message(twitter):  
    with patch('twitter.Twitter.get_user_avatar', return_value='test'):  
        twitter.tweet('Test message')  
        assert twitter.tweet_messages == ['Test message']
```
Podobnie można mockować metody klasy:
```python
def test_tweet_single_message(twitter):  
    with patch.object(Twitter, 'get_user_avatar', return_value='test'):  
        twitter.tweet('Test message')  
        assert twitter.tweet_messages == ['Test message']
```
Do użycia patch, jak i patch.object można też użyć dekoratora. W takim przypadku mockowania klasy w ten sposób, zostanie ona przekazana do testu jako pierwszy argument (w tym przypadku avatar_mock):
```python
@patch.object(Twitter, 'get_user_avatar', return_value='test')  
def test_tweet_single_message(avatar_mock, twitter):  
    twitter.tweet('Test message')  
    assert twitter.tweet_messages == ['Test message']
```
Możliwe jest również utworzenie mocka wewnątrz samego testu. Poniżej przykład nadpisania metody find_hashtags i ustawienie zwracanej przez nią wartości.
```python
from unittest.mock import Mock
  
def test_tweet_with_hashtag_mock(avatar_mock, twitter):  
    twitter.find_hashtags = Mock()  
    twitter.find_hashtags.return_value = ['first']  
    twitter.tweet('Test #second')  
    assert twitter.tweets[0]['hashtags'] == ['first']
```
Jeżeli chcemy zamockować metody magiczne Pythona to zamiast klasy Mock() konieczne jest użycie klasy MagicMock().
```python
from unittest.mock import MagicMock

def test_twitter_version(twitter):  
    twitter.version = MagicMock()  
    twitter.version.__eq__.return_value = '2.0'  
  assert twitter.version == '2.0'
```
**Specyfikacja dla Mocka**

Żeby uniknąć zdefiniowania niechcianego parametru do obiektu Mock można przekazać listę dopuszczalnych parametrów.
```python
>>> from unittest.mock import Mock
>>> calendar = Mock(spec=['is_weekday', 'get_holidays'])

>>> calendar.is_weekday()
<Mock name='mock.is_weekday()' id='4569015856'>
>>> calendar.create_event()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 582, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'create_event'
```
Można również przekazać cały imitowany obiekt:
```python
>>> import my_calendar
>>> from unittest.mock import create_autospec

>>> calendar = create_autospec(my_calendar)
>>> calendar.is_weekday()
<MagicMock name='mock.is_weekday()' id='4579049424'>
>>> calendar.create_event()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 582, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'create_event'
```
Aby wykorzystać ten mechanizm w patchu wystarczy określić parametr **autospec** jako True.
```python
>>> import my_calendar
>>> from unittest.mock import patch

>>> with patch('__main__.my_calendar', autospec=True) as calendar:
...     calendar.is_weekday()
...     calendar.create_event()
...
<MagicMock name='my_calendar.is_weekday()' id='4579094312'>
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 582, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'create_event'
```
### pytest

#### monkeypatch
To use mocking in pytest pass ```monkeypatch``` argument in test arguments.

```python
import requests


def get_my_ip():
    response = requests.get(
        'http://ipinfo.io/json'
    )
    return response.json()['ip']


def test_get_my_ip(monkeypatch):
    my_ip = '123.123.123.123'

    class MockResponse:

        def __init__(self, json_body):
            self.json_body = json_body

        def json(self):
            return self.json_body

    monkeypatch.setattr(
        requests,
        'get',
        lambda *args, **kwargs: MockResponse({'ip': my_ip})
    )

    assert get_my_ip() == my_ip
```
What's happening here?

We used pytest's monkeypatch fixture to replace all calls to the get method from the requests module with the lambda callback that always returns an instance of MockedResponse.

We used an object because requests returns a Response object.

#### unittest.mock.create_autospec
We can simplify the tests with the create_autospec method from the unittest.mock module. This method creates a mock object with the same properties and methods as the object passed as a parameter:

```python
from unittest import mock

import requests
from requests import Response


def get_my_ip():
    response = requests.get(
        'http://ipinfo.io/json'
    )
    return response.json()['ip']


def test_get_my_ip(monkeypatch):
    my_ip = '123.123.123.123'
    response = mock.create_autospec(Response)
    response.json.return_value = {'ip': my_ip}

    monkeypatch.setattr(
        requests,
        'get',
        lambda *args, **kwargs: response
    )

    assert get_my_ip() == my_ip
    ```
# Backend\pytest\008_Skipping_test.md

## Pominięcie testu
Istnieje możliwość pominięcia testu w przypadku, gdy dla danych parametrów nie chcemy go wykonywać.
```python
def test_tweet_with_username(twitter):  
    if twitter.username:  
        pytest.skip()  
    twitter.tweet('Test message')  
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test'}]
```
# Backend\pytest\009_conftest.md

## Plik conftest.py
Plik conftest.py to plik konfiguracyjny dla testów pytestowych, gdzie można np:
*  Składować wielokrotnie używane fixtury, które będą automatycznie wykryte przez testy zdefiniowane w innych plikach.
* Ustalić czynności, które mają zostać wykonane przed wszystkimi testami, np:
```python
def pytest_runtest_setup():  
	# Funkcja wykonana przed każdym testem  
	print('Start test')
```

# Backend\pytest\010_Coverage.md

## Coverage

Source: https://testdriven.io/courses/django-rest-framework/full-test-coverage/#H-11-test-coverage

Install the pytest-cov plugin:

```commandline
(venv)$ pip install pytest-cov==5.0.0
```

To use, you can simply run the following command:
```commandline
(venv)$ python -m pytest --cov=shopping_list shopping_list/tests/
```

Notes:
* --cov tells pytest-cov which module you want to test.
* The second argument tells pytest-cov which test suite you want to run (it needs to be a full path).

```commandline
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
shopping_list/__init__.py                      0      0   100%
shopping_list/admin.py                         4      0   100%
shopping_list/api/__init__.py                  0      0   100%
shopping_list/api/serializers.py              15      0   100%
shopping_list/api/views.py                    16      0   100%
shopping_list/apps.py                          4      0   100%
shopping_list/migrations/0001_initial.py       7      0   100%
shopping_list/migrations/__init__.py           0      0   100%
shopping_list/models.py                       14      2    86%
shopping_list/tests/__init__.py                0      0   100%
shopping_list/tests/conftest.py                9      0   100%
shopping_list/tests/tests.py                 149      0   100%
shopping_list/urls.py                          3      0   100%
--------------------------------------------------------------
TOTAL                                        221      2    99%
```

There's a command that adds the line numbers that don't have code coverage to the report:

```commandline
(venv)$ python -m pytest --cov-report term-missing --cov=shopping_list
```
# Backend\Python\Concurrent_programming\001_Threading.md

### Obsługa wątków
Do obsługi wątków w Pythonie służy zapożyczony z Javy moduł threading.
```python
import threading
import time

class Task(threading.Thread):
	def run(self):
		time.sleep(1)
		print('task done')

Task().start()
print('program finished')

### program finished
### task done
```
Ostatnia linia powyższego kodu wykonała się w trakcie trwania programu. Jeżeli program ma czekać na wykonanie taska, konieczne jest zastosowanie metody .join() na tym tasku, lub określenie go jako daemon
```python
import threading
import time

class Task(threading.Thread):
	def run(self):
		time.sleep(1)
		print('task done')

task = Task()
### task.daemon = True
task.start()
task.join()
print('program finished')

### task done
### program finished
```
Tworzenie wątków jako klas jest niezalecane ze względu na konieczność dziedziczenia z modułu threading. Zamiast tego pisze się je funkcyjnie.

```python
import threading
import time

def task(name):
	time.sleep(1)
	print(f'{name} done')

threading.Thread(targer=task, args=('foo',)).start()
```
W sytuacji, gdy chcemy, aby kilka wątków rozpoczęło się równolegle można posłużyć się Barrier. Poniżej przykład wyścigu koni.
```python
import threading
import time
import random

def sleep(name, message):
	time.sleep(random.random())
	print(name, message)

def horse(name):
	sleep(name, 'ready...')
	barrier.wait()
	sleep(name, 'started')
	sleep(name, 'finished')

def on_start():
	print('--- RACE STARTED ---') 

horse_names = ('Alfie', 'Daisy', 'Unity')
### Barrier jako pierwszy argument przyjmuje liczbę wątków, które ma zatrzymać. Po zatrzymaniu podanej liczby uruchamia je ponownie.
barrier = threading.Barrier(len(horse_names), action=on_start)

### Inicjalizacja osobnego wątku dla każdego konia
horses = [
	threading.Thread(target=horse, args=(name,))
	for name in horse_names
]

for horse in horses:
	horse.start()

### Użycie drugiej pętli jest konieczne, ponieważ gdyby zastosować join() zaraz po użyciu start() dla jednego wątku, pozostałe wątki nie mogłyby się rozpocząć dopóki pierwszy by się nie zakończył
for horse in horses:
	horse.join()
```
W celu obsługi zdarzeń niezwiązanych z działaniem samych wątków wykorzystuje się klasę Event.
```python
import threading

key_pressed = threading.Event()
finished = threading.Event()

key on_key_press():
	while not finished.is_set():
		if key_pressed.wait(0.1):
			print('key pressed')
			key_pressed.clear()
	print('done')

for _ in range(3):
	input()
	key_pressed.set()

threading.Thread(target=on_key_press).start()

finished.set()
```
# Backend\Python\Concurrent_programming\002_Queues.md

### Kolejki

```python
import queue
import threading
import time

def downloader(q):
	while True:
		seconds, filename = q.get()
		time.sleep(seconds)
		print(f'downloaded {filename}')
		q,task_done()

files = [
	(1.5, 'data.xml'),
	(0.1, 'style.css'),
	(3, 'movie.avi'),
	(0.9, 'script.js'),
	(0.25, 'image.jpg'),
]

q = queue.PriorityQueue()

for file in files:
	q.put(file)

for _ in range(5):
	threading.Thread(target=downloader, args=(q,), daemon=True).start()

q.join()
```
# Backend\Python\Concurrent_programming\003_Processes.md

### Procesy
```python
from multiprocessing import Process

def reverse(text):
	return text[::-1]

if __name__ == '__main__':
	p = Process(target=reverse, args=('foobar',))
	p.start()
	p.join()
```
# Backend\Python\Concurrent_programming\004_asyncio.md

### asyncio
Bilbioteka asyncio wykorzystywana jest do przetwarzania asynchronicznego. Poniżej przykład jej zastosowaniu w ciągu Fibonacciego.

```python
import asyncio

### Zdefiniowanie korutyny
async def fib(n):
	if n < 2:
		return n
	
	a = await fib(n - 2)
	b = await fib(n - 1)
	
	return a + b

loop = asyncio.get_event_loop()
loop.set_debug(True)

try:
	result = loop.run_until_complete(fib(10))
	print(result)
finally:
	loop.close()
```

# Backend\Python\Dataclasses\001_Base_dataclasses.md

### Dataclasses

Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

#### Intro

Instead of usual class definitions, dataclasses enables to get rid of boilerplate code and define object oriented mainly on data instead of behaviour.

```python
from dataclasses import dataclass
from enum import Enum, auto


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()

@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    license_plate: str
    fuel_type: FuelType = FuelType.ELECTRIC
```
# Backend\Python\Dataclasses\002_Default_values.md

### Default values

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

Initially dataclasses do not allow to specify mutable values (like lists) as defaults for fields.
```python
@dataclass
class Vehicle:
    brand: str
    model: str
    color: str = 'white'
    license_plate: str
    fuel_type: FuelType = FuelType.ELECTRIC
    accessories: list[Accessory] = []  # It won't work
```

Instead we can use `field` method to specify it with `lambda` statement or function (like `list`).

```python
from dataclasses import dataclass, field
from enum import Enum, auto

class Accessory(Enum):
    AIRCO = auto()
    CRUISECONTROL = auto()
    NAVIGATION = auto()
    OPENROOF = auto()
    BATHTUB = auto()
    MINIBAR = auto()


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    license_plate: str
    fuel_type: FuelType = FuelType.ELECTRIC
    accessories: list[Accessory] = field(default_factory=lambda: [Accessory.AIRCO])
```

# Backend\Python\Dataclasses\003_Protected_values.md

### Protected values

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

To prevent from overriding dataclass field during initialization you can use `init=False` statement on class value.

```python
@dataclass
class Vehicle:
    ...
    accessories: list[Accessory] = field(default_factory=lambda: [Accessory.AIRCO], init=False)
```

It will end up with error if during initialization field `accessories` will be provided.

# Backend\Python\Dataclasses\004_Post_init.md

### __post_init__

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

To perform some actions just before initialization of dataclass objects they have to be specified in `.__post__init__` method.

```python
@dataclass
class Vehicle:
    ...
    def __post_init__(self):
        self.license_plate = generate_vehicle_license()
```
# Backend\Python\Dataclasses\005_Read-only_instances.md

### Read-only dataclass instance

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

If we want to prevent from changing dataclass object after its initialization we have to use `frozen=True` param on `@dataclass` decorator.

```python
@dataclass(frozen=True)
class Vehicle:
    ...
```

>It will also disable all operations performed in `__post_init__` method! You can use `field(default_factory=)` as workaround.
# Backend\Python\Data_containers\001_Array.md

### Array
Struktura danych przypominająca działaniem array stosowany np. w C i służy między innymi do komunikacji z softem pisanym w tym języku. 
```python
import array

### Konieczne zadeklarowanie typu zmiennych.
example = array.array('b')
```
# Backend\Python\Data_containers\002_ChainMap.md

### ChainMap
Struktura umożliwiająca połączenie dwóch słowników. W przypadku, gdy w którymś ze składowych słowników zajdzie jakaś zmiana, będzie ona uwzględniona w obiekcie ChainMap.
```python
from collections import ChainMap

d1 = {'color': 'red'}
d2 = {'pet': 'cat'}

d = dict(ChainMap(d1, d2))  # {'color': 'red', 'pet': 'cat'}

maps = d,maps # lista słowników w kolejności, w jakiej zostały dodane[{'color': 'red'}, {'pet': 'cat'}]
```
Przy próbie podania wartości dla już istniejącego klucza w ChainMap pozostanie pierwotna wartość.

# Backend\Python\Data_containers\003_Counter.md

### Counter
Zlicza ilość wystąpień elementów w sekwencji.
```python
from collections import Counter

c = Counter('abbac') 
### Counter({'a': 2, 'b': 2, 'c': 1})

c['x'] 
### Zwraca 0 zamiast wyjątku

c.most_common() 
### Zwraca posortowaną listę od najczęściej występującego elementu
### [('a', 2), ('b', 2), ('c', 1)]
```
# Backend\Python\Data_containers\004_defaultdict.md

### defaultdict
Pozwala na uproszczenie i przyspieszenie kodu, którego celem jest np. budowa słownika. Przykładowo - poniżej kod, którego celem jest zbudowanie słownika, gdzie kluczem jest długość imienia, a wartością - lista podanych w sekwencji imion.
```python
names_by_length = {}
for name in ('bob', 'alice', 'max', 'adam', 'eve'):
	key = len(name)
	if key not in names_by_length:
		names_by_length[key] = []
	names_by_length[key].append(name)
	
### names_by_length = {3: ['bob', 'max', 'eve'], 4: ['adam'], 5: ['alice']}
```
Ten sam efekt można uzyskać używając defaultdict. W przypadku, gdy kod sięga do słownika przy użyciu nieistniejącego klucza wykonywana jest funkcja podana jako argument przy inicjalizacji defaultdicta (w tym przypadku funkcja list()).

```python
from collections import defaultdict

names_by_length = defaultdict(list)
### argument "list" oznacza, że przy próbie wyciągnięcia danych dla nieistniejącego klucza zostanie utworzona pusta lista

for name in ('bob', 'alice', 'max', 'adam', 'eve'):
	names_by_length[len(name)].append(name)
	
### names_by_length = {3: ['bob', 'max', 'eve'], 4: ['adam'], 5: ['alice']}
```
# Backend\Python\Data_containers\005_OrderedDict.md

### OrderedDict
Słownik zachowujący porządek wstawianych kluczy. Wykorzystuje wewnętrznie listę dwukierunkową.
```python
from collections import OrderedDict

row = OrderedDict()
row['id'] = '123'
row['firstName'] = 'Jan'
row['lastName'] = 'Kowalski'

list(row.items())
### Poszczególne elementy słownika są zachowana w kolejności, w jakiej zostały dodane
### [('id', '123'), ('firstName', 'Jan'), ('lastName', 'Kowalski')]
```
# Backend\Python\Data_containers\006_deque.md

### deque
Nazwa to skrót od "double ended queue". Wykorzystuje wewnętrznie listę dwukierunkową. Deque może służyć np. do składowania historii operacji. 
Dla określonej liczby elementów deque zachowuje ich kolejność przy użyciu wskaźnika początkowego i końcowego. Przy dodaniu nowego elementu wskaźnik końcowy wskazuje na nowy element, za to wskaźnik początkowy przenosi się na następujący po dotychczasowym elemencie początkowym.
```python
from collections import deque

history = deque(maxlen=3)
### maxlen określa maksymalną długość kolejki

text = "Houston we have a problem"
for word in text.split():
	history.append(word)

### W czasie iteracji zmienna history będzie zawierać zawsze 3 elementy, gdzie dodanie nowego elementu będzie usuwać pierwszy element z listy, jeżeli będzie ona miała długość równą maxlen

history.popleft()
### Usuwa element z lewej (początkowej) strony kolejki
history.appendleft('not')
### Dodaje element na początku kolejki
```
# Backend\Python\Data_containers\007_namedtuple.md

### namedtuple
Namedtuple to po prostu tuple z nazwanymi polami
```python
import collections import namedtuple

p = 1, 2
Point = namedtuple('Point', ['x', 'y'])
Point(*p)
### Point(x=1, x=2)
d = {'x': 3, 'y': 4}
Point(**d)
### Point(x=3, x=4)
Point(x=5, y=6)
### Point(x=5, x=6)
```
# Backend\Python\Data_containers\008_enum.md

### enum

Moduł pozwalający na tworzenie typów wyliczeniowych.
```python
from enum import Enum

class Season(Enum):
	SPRING = 1
	SUMMER = 2
	AUTUMN = 3
	WINTER = 4

### printing enum member as string
Season.SPRING
### Season.SPRING

### printing name of enum member using "name" keyword
print(Season.SPRING.name)
### SPRING

### printing value of enum member using "value" keyword
print(Season.SPRING.value)
### 1

### printing the type of enum member using type()
print(type(Season.SPRING))
### <enum 'Season'>

### printing enum member as repr
print(repr(Season.SPRING))
### <Season.SPRING: 1>

### printing all enum member using "list" keyword
print(list(Season))
### [<Season.SPRING: 1>, <Season.SUMMER: 2>, <Season.AUTUMN: 3>, <Season.WINTER: 4>]
```
# Backend\Python\Functional_programming\001_Higher_order_functions.md

### Higher order functions

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150904384/posts/2160071945
Functions that may take other function as an argument and/or return function as a return value.

```python
### This is higher-order function
def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")


def is_eligible_for_promotion(customer: Customer) -> bool:
    return customer.age >= 50


def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    send_email_promotion(customers, is_eligible_for_promotion)
    # We can use lambda function also
    # send_email_promotion(customers, lambda customer: customer.age >= 50)
```

#### map
Wykonuje wskazaną funkcję na każdym elemencie podanej sekwencji i zwraca listę wyników tej funkcji
```python 
### Zwraca iterator pozycji poszczególnych elementów stringa w Unicode
map(ord, 'zażółć gęślą jaźń') 
```
#### filter
Filtruje sekwencje bazując podanej funkcji.
```python 
filter(str.isupper, 'Hello World') 
```
#### functools.reduce
Iteruje po elementach sekwencji i redukuje ją do pojedynczej wartości.
**Przykład 1: Sumowanie liczb**
```python
import operator
from functools import reduce

numbers = [42, 15, 2, 33]

### Pierwsza wartość funkcji to tzw. akumulator, na którym wykonywane są operacje bazujące na drugim argumencie
def f(subtotal, number):
	return subtotal + number

###reduce(f, numbers)
reduce(operator.add, numbers)
```
**Przykład 2: Grupowanie liczb parzystych i nieparzystych**
```python
import operator
from functools import reduce

numbers = [42, 15, 2, 33]

def f(grouped, number):
	key = 'even' if number % 2 == 0 else 'odd'
	grouped[key].append(number)
	return grouped

reduce(f, numbers, {'even': [], 'odd': []})
```
# Backend\Python\Functional_programming\002_Nested_functions.md

### Funkcje zagnieżdżone
Jako, że funkcje to typ pierwszoklasowy, można je bez ograniczeń zagnieżdżać. Stosowanie funkcji zagnieżdżonych umożliwia ukrywanie implementacji. Funkcja zagnieżdżona ma zasięg lokalny, przez co ma bezpośredni dostęp do argumentów przekazanych do funkcji nadrzędnej.  
```python
def selection_sort(items):

	def recursive(items, i):
		
		def min_index(i):
			return items.index(items[i:], i)
		
		def swap(i, j):
			items[i], items[j] = items[j], items[i]
		
		if i < len(items):
			j = min_index(i)
			swap(i, j)
			selection_sort(items, i + 1)
	
	recursive(items, 0)

items = ['bob', 'alice', 'max']
selection_sort(items) 
```
# Backend\Python\Functional_programming\003_Variables_scope.md

### Zasięg zmiennych
Wartości zmiennych wyszukiwane są w kolejności LEGB - local, enclosed, global, built-in.
```python
%reset -f

x = 'global'

def outer():
	x = 'enclosed'
	def inner():
		x = 'local'
		print(x)
	inner()
	print(x)

outer()
print(x)

### local
### enclosed
### global
```
# Backend\Python\Functional_programming\004_Closures.md

### Closures

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150904384/posts/2160071962

Functions defined within the function. It enables to pass variables to Callable types of arguments

#### Manual closure

```python

def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")

def is_eligible_closure(cutoff_age: int) -> Callable[[Customer], bool]:
    def is_eligible(customer: Customer) -> bool:
        return customer.age > cutoff_age

    return is_eligible

def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    # Using closure enables to pass argument to is_eligible_closure function
    send_email_promotion(customers, is_eligible_closure(50))
```

#### functools.partial

Same effect may be achieved by using partial function from functools package.

```python
from functools import partial

def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")

def is_eligible_for_promotion(customer: Customer, cutoff_age: int) -> bool:
    return customer.age > cutoff_age

def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    is_eligible = partial(is_eligible_for_promotion, cutoff_age=25)
    send_email_promotion(customers, is_eligible(50))
```
# Backend\Python\Functional_programming\005_Partial_functions.md

### Funkcje cząstkowe
Funkcje wykonujące działanie innej funkcji, ale z mniejszą wymaganą do podania liczbą argumentów.

```python
from functools import partial

def quadratic(x, a, b, c):
	return a*x**2 + b*x + c

### Funkcja cząstkowa - zapis 1
def y(x):
	return quadratic(x, 3, 1, -4)

### Funkcja cząstkowa - zapis 2
y = partial(quadratic, a=3, b=1, c=-4)
```
# Backend\Python\Good practices\7_principles_of_modern_software_design\001_Favor_composition_over_inheritance.md

#### Composition over inheritance

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150529699/posts/2153184357

##### Example of calculating salary for employees

```python
from dataclasses import dataclass


@dataclass
class HourlyEmployee:
    name: str
    id: int
    commission: int = 10000
    contracts_landed: float = 0
    pay_rate: int = 0
    hours_worked: float = 0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(
            self.pay_rate * self.hours_worked
            + self.employer_cost
            + self.commission * self.contracts_landed
        )


@dataclass
class SalariedEmployee:

    name: str
    id: int
    commission: int = 10000
    contracts_landed: float = 0
    monthly_salary: int = 0
    percentage: float = 1

    def compute_pay(self) -> int:
        return int(
            self.monthly_salary * self.percentage
            + self.commission * self.contracts_landed
        )


@dataclass
class Freelancer:

    name: str
    id: int
    commission: int = 10000
    contracts_landed: float = 0
    pay_rate: int = 0
    hours_worked: float = 0
    vat_number: str = ""

    def compute_pay(self) -> int:
        return int(
            self.pay_rate * self.hours_worked + self.commission * self.contracts_landed
        )


def main() -> None:

    henry = HourlyEmployee(name="Henry", id=12346, pay_rate=5000, hours_worked=100)
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah = SalariedEmployee(
        name="Sarah", id=47832, monthly_salary=500000, contracts_landed=10
    )
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()
```

In this case we have three separate classes for three types of employees - `HourlyEmployee`, `SalariedEmployee` and `Freelancer`.

All of them has `compute_pay()` method defined and demands specific fields for pay calculation.

##### Usual refactoring using inheritance

```python
from dataclasses import dataclass


@dataclass
class HourlyEmployee:
    name: str
    id: int
    pay_rate: int
    hours_worked: float = 0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(self.pay_rate * self.hours_worked + self.employer_cost)


@dataclass
class SalariedEmployee:
    name: str
    id: int
    monthly_salary: int
    percentage: float = 1

    def compute_pay(self) -> int:
        return int(self.monthly_salary * self.percentage)


@dataclass
class Freelancer:
    name: str
    id: int
    pay_rate: int
    hours_worked: float = 0
    vat_number: str = ""

    def compute_pay(self) -> int:
        return int(self.pay_rate * self.hours_worked)


@dataclass
class SalariedEmployeeWithCommission(SalariedEmployee):
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return super().compute_pay() + int(self.commission * self.contracts_landed)


@dataclass
class HourlyEmployeeWithCommission(HourlyEmployee):
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return super().compute_pay() + int(self.commission * self.contracts_landed)


@dataclass
class FreelancerWithCommission(Freelancer):
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return super().compute_pay() + int(self.commission * self.contracts_landed)


def main() -> None:

    henry = HourlyEmployee(name="Henry", id=12346, pay_rate=5000, hours_worked=100)
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah = SalariedEmployeeWithCommission(
        name="Sarah", id=47832, monthly_salary=500000, contracts_landed=10
    )
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()
```

In this way of refactoring initial code calculation of commission (that was common for all employees classes) was moved to separate classes that inherit from "base" class respectively:
* HourlyEmployee -> HourlyEmployeeWithCommission
* SalariedEmployee -> SalariedEmployeeWithCommission
* Freelancer -> FreelancerWithCommission

All `WithCommision` child classes do their job, but they provide exactly the same functionality, so it ends up with code duplication.

##### Refactoring using composition

```python
from dataclasses import dataclass, field
from typing import Protocol


class PaymentSource(Protocol):
    def compute_pay(self) -> int:
        ...


@dataclass
class DealBasedCommission:
    commission: int = 10000
    deals_landed: int = 0

    def compute_pay(self) -> int:
        return self.commission * self.deals_landed


@dataclass
class HourlyContract:
    hourly_rate: int
    hours_worked: float = 0.0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(self.hourly_rate * self.hours_worked + self.employer_cost)


@dataclass
class SalariedContract:
    monthly_salary: int
    percentage: float = 1

    def compute_pay(self) -> int:
        return int(self.monthly_salary * self.percentage)


@dataclass
class FreelanceContract:
    pay_rate: int
    hours_worked: float = 0
    vat_number: str = ""

    def compute_pay(self) -> int:
        return int(self.pay_rate * self.hours_worked)


@dataclass
class Employee:
    name: str
    id: int
    payment_sources: list[PaymentSource] = field(default_factory=list)

    def add_payment_source(self, payment_source: PaymentSource):
        self.payment_sources.append(payment_source)

    def compute_pay(self) -> int:
        return sum(source.compute_pay() for source in self.payment_sources)


def main() -> None:
    henry_contract = HourlyContract(hourly_rate=5000, hours_worked=100)
    henry = Employee(name="Henry", id=12346, payment_sources=[henry_contract])
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah_contract = SalariedContract(monthly_salary=500000)
    sarah_commission = DealBasedCommission(deals_landed=10)
    sarah = Employee(
        name="Sarah", id=47832, payment_sources=[sarah_contract, sarah_commission]
    )
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()
```

In that case payment source is provided as separate object that is a part of employee object. It enables more flexibility as every single employee may have custom combination of payment sources.

Protocol `PaymentSource` defines, how payment source should look like for typing system. `DealBasedCommission`, `HourlyContract`, `SalariedContract`, `FreelanceContract` meet the requirements of protocol and handle commission case.

`Employee` object represents all employees, that may have many payment sources.

Computing pay in `compute_pay()` method works for all payment sources as according to defined protocol they share the same interface.
# Backend\Python\Good practices\7_principles_of_modern_software_design\002_High_cohesion.md

#### High cohesion

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150528069/posts/2153184358

We can say that function has high cohesion, when it has single responsibility and uses other classes and functions to do other things.

##### Order class with low cohesion

```python
class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: str = "open"

    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def pay(self, payment_type: str, security_code: str) -> None:
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")


def main() -> None:
    order = Order()
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    order.pay("debit", "0372846")


if __name__ == "__main__":
    main()
```

`Order` class has many responsibilities - it handles adding new items to order and paying for order with many payment types.

##### Order with high cohesion

```python
from enum import Enum, auto


class PaymentStatus(Enum):
    """Payment status"""

    OPEN = auto()
    PAID = auto()


class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: PaymentStatus = PaymentStatus.OPEN

    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)


class PaymentProcessor:
    def pay_debit(self, order: Order, security_code: str) -> None:
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = PaymentStatus.PAID

    def pay_credit(self, order: Order, security_code: str) -> None:
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = PaymentStatus.PAID


def main():
    order = Order()
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    processor = PaymentProcessor()
    processor.pay_debit(order, "0372846")


if __name__ == "__main__":
    main()

```

After minor refactoring `Order` class has only responsibility to add items and store order data.
Payment processes were moved to separate `PaymentProcessor` class, where all payment types have separate method for handling payment.
Statuses were changed to Enum instead of raw string.
# Backend\Python\Good practices\7_principles_of_modern_software_design\003_Low_coupling.md

#### Low coupling

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150527399/posts/2153184359

##### Coupling

Coupling is degree in which all parts of code need each other to work. The lower coupling is the more modular your program becomes. 
When coupling is low it's easy to reuse modules in many applications.

##### Types of coupling
* Content coupling - when one class/method/function changes data in another class

```python
def add_item(order: Order, name: str, quantity: int, price: int) -> None:
    order.items.append(name)
    order.quantities.append(quantity)
    order.prices.append(price)
```

* Global coupling - when class/method/functions relies on global data shared by many parts of code, like global constant variables

```python
VEHICLE_DATA = {
    "vw": VehicleData(brand="vw", price_per_km=30, price_per_day=6000),
    "bmw": VehicleData(brand="bmw", price_per_km=35, price_per_day=8500),
    "ford": VehicleData(brand="ford", price_per_km=25, price_per_day=12000),
}
```

* External coupling - when application communicates with external sources, like API.
* Control coupling - when one part of your code controls flow of another part of code.
* Stamp coupling - when data structures are coupled in some way
* Data coupling - when many functions/classes uses the same data/objects
* Import coupling - when your application needs some third party libraries

##### Principle of Least Knowledge / Law of Demeter

It says that you have to try to create units that only have knowledge and talk to closely related units.

Example:

`add_item` function operates on params of `Order` class, so it has to "know" that they exists.

```python
def add_item(order: Order, name: str, quantity: int, price: int) -> None:
    order.items.append(name)
    order.quantities.append(quantity)
    order.prices.append(price)
```

To make it work according to Law of Demeter it would be better to make `add_item` function `Order` class method - 
then it will be operating closely on `Order` class.

```python
class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: str = "open"

    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)
```

# Backend\Python\Good practices\7_principles_of_modern_software_design\004_Start_with_the_data.md

#### Start with the data

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150523714/posts/2153274137

You need to put the behaviour as closely as possible to the data, that it needs. It will reduce number of data, 
that you will need to pass along as parameters.

##### Before

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from reader import read_kms_to_drive, read_rent_days, read_vehicle_type

FREE_KMS = 100


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    price_per_km: int
    price_per_day: int
    reserved: bool

    def total_price(self, days: int, additional_km: int) -> int:
        return days * self.price_per_day + additional_km * self.price_per_km


class ContractStatus(Enum):
    ORDERED = auto()
    PAID = auto()
    PICKED_UP = auto()
    DROPPED_OFF = auto()
    CANCELLED = auto()


@dataclass
class RentalContract:
    vehicle: Vehicle
    customer_id: int
    customer_name: str
    customer_address: str
    customer_postal_code: str
    customer_city: str
    customer_email: str
    contract_status: ContractStatus
    pickup_date: datetime
    days: int = 1
    additional_km: int = 0


VEHICLES = {
    "vw": Vehicle(
        "Volkswagen", "Golf", "black", FuelType.PETROL, "ABC123", 30, 6000, False
    ),
    "bmw": Vehicle("BMW", "X5", "green", FuelType.PETROL, "ABC123", 30, 8500, False),
    "ford": Vehicle(
        "Ford", "Fiesta", "white", FuelType.PETROL, "ABC123", 30, 12000, False
    ),
}


def main():

    vehicle_type = read_vehicle_type(list(VEHICLES.keys()))

    days = read_rent_days()

    additional_km = read_kms_to_drive()

    # setup the rental contract
    rental = RentalContract(
        VEHICLES[vehicle_type],
        12345,
        "Arjan",
        "Sesame street 104",
        "1234",
        "Amsterdam",
        "hi@arjancodes.com",
        ContractStatus.ORDERED,
        datetime.now(),
        days,
        max(additional_km - FREE_KMS, 0),
    )

    # log the rental information
    print(rental)

    # calculate the total price
    total_price = rental.vehicle.total_price(rental.days, rental.additional_km)
    print(f"Total price: ${total_price/100:.2f}")


if __name__ == "__main__":
    main()
```

##### After

Data about customer was moved from `RentalContract` dataclass to separate `Customer` dataclass.

`total_price` property moved to `RentalContract` as in fact it is property of contract, not vehicle. Thanks to that change, 
in main function user won't need to know about implementation details (`total_price = rental.vehicle.total_price(rental.days, rental.additional_km)`) to make things working.

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from reader import read_kms_to_drive, read_rent_days, read_vehicle_type

FREE_KMS = 100


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    price_per_km: int
    price_per_day: int
    reserved: bool


@dataclass
class Customer:
    id: int
    name: str
    address: str
    postal_code: str
    city: str
    email: str


class ContractStatus(Enum):
    ORDERED = auto()
    PAID = auto()
    PICKED_UP = auto()
    DROPPED_OFF = auto()
    CANCELLED = auto()


@dataclass
class RentalContract:
    vehicle: Vehicle
    customer: Customer
    contract_status: ContractStatus
    pickup_date: datetime
    days: int = 1
    additional_km: int = 0

    def total_price(self):
        return (
            self.days * self.vehicle.price_per_day
            + self.additional_km * self.vehicle.price_per_km
        )


VEHICLES = {
    "vw": Vehicle(
        "Volkswagen", "Golf", "black", FuelType.PETROL, "ABC123", 30, 6000, False
    ),
    "bmw": Vehicle("BMW", "X5", "green", FuelType.PETROL, "ABC123", 30, 8500, False),
    "ford": Vehicle(
        "Ford", "Fiesta", "white", FuelType.PETROL, "ABC123", 30, 12000, False
    ),
}


def main():
    customer = Customer(
        12345, "Arjan", "Sesame street 104", "1234", "Amsterdam", "hi@arjancodes.com"
    )

    vehicle_type = read_vehicle_type(list(VEHICLES.keys()))

    days = read_rent_days()

    additional_km = read_kms_to_drive()

    # setup the rental contract
    rental = RentalContract(
        VEHICLES[vehicle_type],
        customer,
        ContractStatus.ORDERED,
        datetime.now(),
        days,
        max(additional_km - FREE_KMS, 0),
    )

    # log the rental information
    print(rental)

    # calculate the total price
    print(f"Total price: ${rental.total_price()/100:.2f}")


if __name__ == "__main__":
    main()
```

# Backend\Python\Good practices\7_principles_of_modern_software_design\005_Depend_on_Abstractions.md

#### Depend on Abstractions

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150479414/posts/2153274138

The goal of this rule is to keep as least coupling in code as possible and it is achievable by using abstraction layers 
like abstract classes and protocols.

You have to have one "dirty" place, where all your implementations starts to "live". If you need to change your code in 
different your code in many places after minor change - you need to use more abstractions, because coupling is too high. 

##### Using typing as abstraction
###### Before

`__init__` method of `PaymentProcessor` class needing to "know" about all authorization methods, that exists in 
separate module.

```python
from pos.authorization import authorize_google, authorize_robot, authorize_sms


class PaymentProcessor:
    def __init__(self, authorizer_type: str):
        if authorizer_type == "google":
            self.authorize = authorize_google
        elif authorizer_type == "sms":
            self.authorize = authorize_sms
        else:
            self.authorize = authorize_robot
```

###### After 
Particular authorizing functions replaced with abstraction created with Python typing system. In this case `PaymentProcessor` 
gets authorizing function as an argument instead of string. 

Another benefit is that `PaymentProcess` is no longer responsible for determining authorizing system. 
```python
from typing import Callable

AuthorizeFunction = Callable[[], bool]

class PaymentProcessor:
    def __init__(self, authorize: AuthorizeFunction):
        self.authorize = authorize
```

##### Using protocol for abstraction 

###### Before
`PaymentProcessor` dependent directly on `Order` class and changing it's params (so it needs to know about implementation details).

```python
class PaymentProcessor:
    ...
    
    def pay_debit(self, order: Order) -> None:
        if not self.authorize():
            raise Exception("Not authorized")
        print(f"Processing debit payment for amount: ${(order.total_price / 100):.2f}.")
        order.status = PaymentStatus.PAID
```
###### After
Instead of using `Order` class in `PaymentProcessor` implementation using `Payable` protocol providing methods and properties needed by `PaymentProcessor`. 

```python
class Payable(Protocol):
    @property
    def total_price(self) -> int:
        ...

    def set_payment_status(self, status: PaymentStatus) -> None:
        ...

class PaymentProcessor:
    ...
    
    def pay_debit(self, payable: Payable) -> None:
        if not self.authorize():
            raise Exception("Not authorized")
        print(f"Processing debit payment for amount: ${(payable.total_price / 100):.2f}.")
        payable.set_payment_status(PaymentStatus.PAID)
```
# Backend\Python\Good practices\7_principles_of_modern_software_design\006_Separate_creation_from_use.md

#### Separate creation from use

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150444017/posts/2153274140

As a continuation of cohesion topic, where we want to split responsibilities we can go one step ahead and split 
creating an object from using them. Factory pattern is a good way to do so.

##### Factory pattern

The main point of Factory pattern is that we have a class that is responsible for creating objects.

###### Before

`main` function is responsible for - receiving a user choice for video quality, creating Exporter objects and using selected Exporter objects,

```python
def main() -> None:

    # read the desired export quality
    export_quality = read_choice(
        "What output quality do you want", ["low", "high", "master"]
    )

    # create the video and audio exporters
    video_exporter: VideoExporter
    audio_exporter: AudioExporter
    if export_quality == "low":
        video_exporter = H264BPVideoExporter()
        audio_exporter = AACAudioExporter()
    elif export_quality == "high":
        video_exporter = H264Hi422PVideoExporter()
        audio_exporter = AACAudioExporter()
    else:
        # default: master quality
        video_exporter = LosslessVideoExporter()
        audio_exporter = WAVAudioExporter()

    # prepare the export
    video_exporter.prepare_export("placeholder_for_video_data")
    audio_exporter.prepare_export("placeholder_for_audio_data")

    # do the export
    folder = Path("/usr/tmp/video")
    video_exporter.do_export(folder)
    audio_exporter.do_export(folder)
```

###### After

Instead of creating objects in `main` functions, the one of Exporter classes (which are factories) is responsible to do so.

Factory for particular choice is stored in constant `FACTORIES` dictionary. It's picked via separate `read_factory` function.

Created objects are used in separate `do_export` function.

```python
class ExporterFactory(Protocol):
    """
    Factory that represents a combination of video and audio codecs.
    The factory doesn't maintain any of the instances it creates.
    """

    def create_video_exporter(self) -> VideoExporter:
        """Returns a new video exporter belonging to this factory."""
        ...

    def create_audio_exporter(self) -> AudioExporter:
        """Returns a new audio exporter belonging to this factory."""
        ...


class FastExporter:
    """Factory aimed at providing a high speed, lower quality export."""

    def create_video_exporter(self) -> VideoExporter:
        return H264BPVideoExporter()

    def create_audio_exporter(self) -> AudioExporter:
        return AACAudioExporter()


class HighQualityExporter:
    """Factory aimed at providing a slower speed, high quality export."""

    def create_video_exporter(self) -> VideoExporter:
        return H264Hi422PVideoExporter()

    def create_audio_exporter(self) -> AudioExporter:
        return AACAudioExporter()


class MasterQualityExporter:
    """Factory aimed at providing a low speed, master quality export."""

    def create_video_exporter(self) -> VideoExporter:
        return LosslessVideoExporter()

    def create_audio_exporter(self) -> AudioExporter:
        return WAVAudioExporter()


FACTORIES: dict[str, ExporterFactory] = {
    "low": FastExporter(),
    "high": HighQualityExporter(),
    "master": MasterQualityExporter(),
}


def read_factory() -> ExporterFactory:
    """Constructs an exporter factory based on the user's preference."""

    while True:
        export_quality = input(
            f"Enter desired output quality ({', '.join(FACTORIES)}): "
        )
        try:
            return FACTORIES[export_quality]
        except KeyError:
            print(f"Unknown output quality option: {export_quality}.")


def do_export(fac: ExporterFactory) -> None:
    """Do a test export using a video and audio exporter."""

    # retrieve the exporters
    video_exporter = fac.create_video_exporter()
    audio_exporter = fac.create_audio_exporter()

    # prepare the export
    video_exporter.prepare_export("placeholder_for_video_data")
    audio_exporter.prepare_export("placeholder_for_audio_data")

    # do the export
    folder = Path("/usr/tmp/video")
    video_exporter.do_export(folder)
    audio_exporter.do_export(folder)


def main() -> None:
    # create the factory
    factory = read_factory()

    # perform the exporting job
    do_export(factory)
```
# Backend\Python\Good practices\7_principles_of_modern_software_design\007_Keep_things_simple.md

#### Keep things simple

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150437717/posts/2153274144

##### DRY

Don't repeat yourself. Remove duplications. But it's not always needed to create too generic replacements for existing duplication,
let's keep things simple and easy to maintain.

###### Before 

```python
def read_vehicle_type() -> str:
    vehicle_types = ["vw", "bmw", "tesla"]
    vehicle_type = ""
    while vehicle_type not in vehicle_types:
        vehicle_type = input(
            f"What type of vehicle would you like to rent ({', '.join(vehicle_types)})? "
        )
    return vehicle_type


def read_vehicle_color() -> str:
    vehicle_colors = ["black", "red", "blue"]
    vehicle_color = ""
    while vehicle_color not in vehicle_colors:
        vehicle_color = input(
            f"What color vehicle would you like to rent ({', '.join(vehicle_colors)})? "
        )
    return vehicle_color

def main():

    vehicle_type = read_vehicle_type()
    vehicle_color = read_vehicle_color()
```

###### After

```python
def read_choice(question: str, choices: list[str]) -> str:
    choice = ""
    while choice not in choices:
        choice = input(f"{question} ({', '.join(choices)})? ")
    return choice

def main():

    vehicle_type = read_choice(
        "What type of vehicle would you like to rent", ["vw", "bmw", "tesla"]
    )

    vehicle_color = read_choice(
        "What color vehicle would you like to rent", ["black", "red", "blue"]
    )
```

##### KISS

Keep it simple, stupid - this rule leads to not overcomplicating your code - do not use abstraction, protocols and other stuff,
if the only thing you need to do is to add two integers.

##### YAGNI

You Ain't Gonna Need It - this rule speaks about not implementing something, that you don't need right now. Don't create extra 
features - users will ask you for them if they will be needed.  
# Backend\Python\Good practices\Basics\001_Language_properties.md

#### WŁAŚCIWOŚCI JĘZYKA
##### 1.1. Przestrzenie nazw  
W pewnym sensie powiązane z zakresami są przestrzenie nazw. Są to zakresy zapewniające nam to, że nazwa danego obiektu będzie unikalna i że można z nich będzie korzystać bez ryzyka wystąpienia jakichkolwiek konfliktów. To swojego rodzaju zbiór nazw i definicji, które mogą mieć zastosowanie lokalne (podobnie jak zakresy, w obrębie funkcji), ale także globalnie, które określają nazwy dla całego kodu, zaimportowanych paczek. W Pythonie funkcjonują także wbudowane przestrzenie nazw kluczowych funkcji w tym języku, dzięki którym możemy mieć pewność, że utworzony przez nas obiekt nie będzie w konflikcie z którąkolwiek z wbudowanych funkcji Pythona.  
##### 1.2. Różnica między modułem i paczką  
Zarówno moduły jak i paczki wykorzystywane są do modularyzacji kodu, co przekłada się na jego łatwość w utrzymaniu i ułatwia pracę z omówionymi już zakresami. Moduły są plikami zawierający zestaw zdefiniowanych instrukcji, klas i zmiennych. Można zaimportować zarówno całe moduły, jak i ich części.  
Paczka w Pythonie zazwyczaj składa się z kilku modułów. Jest ona jednak na tyle przydatna, że określa dla nich przestrzenie nazw i eliminuje konflikty pomiędzy poszczególnymi modułami.  
##### 1.3. Zakresy  
Zakresy, czy też scope’y, w Pythonie nie różnią się od tego, co znamy z innych języków programowania. Scope to blok kodu, w którym działa dany obiekt i tylko w nim jest dostępny. Na przykład lokalny zakres odnosi się do wszystkich obiektów w danej funkcji, zaś zakres globalny będzie zawierał wszystkie obiekty w całym kodzie.  
```python
x = 10             # zmienna globalna

def f():
    global x       # słowo global informuje Pythona, że poprzez zmienną x będziemy odnosić się do zmiennej globalnej
    x = 111        # zmiana wartości przypisanej do zmiennej globalnej
    y = 12         # zmienna lokalna (przestaje istnieć po zakończeniu wykonywania funkcji)
    print(x, y)

f()                # uruchomienie funkcji wydrukuje zmienną globalną x i zmienna lokalną y
print(x)           # drukuje zmienną globalną x
```
#####   1.4. Typy wbudowane  
- `str` – string, tekstowy typ danych,  
- `int` – liczba,  
- `float` – liczba zmiennoprzecinkowa,  
- `complex` – liczba zespolona,  
- `list` – lista  
- `tuple` – kortka  
- `range` – zakres, liczby naturalne stanowiące szereg arytmetyczny,  
- `dict` – słownik,  
- `set` – zbiór,  
- `frozenset` – zbiór niemutowalny,  
- `bool` – logika boolowska,  
- `bytes` – konwersja ciągu na bajty,  
- `bytearray` – mutowalny wariant bytes,  
- `memoryview` – dostęp do wewnętrznych danych obiektów obsługujących bufory protokołów.  

##### 1.5. PYTHONPATH  
`PYTHONPATH` to zmienna środowiskowa pozwalająca wskazać dodatkowe lokalizacje, z których Python będzie mógł zaciągnąć moduły i paczki.  
##### 1.6. PEP8  
PEP 8 to opracowany jeszcze w 2001 r. dokument, w którym opisane zostały najlepsze praktyki w zakresie pisania czytelnego kodu w Pythonie. Stanowi część oficjalnej dokumentacji języka. Stanowi on powszechnie respektowaną normę i w zasadzie stanowi lekturę obowiązkową dla każdego, kto chce programować w Pythonie. Z treścią dokumentu zapoznać się można na  [oficjalnej stronie Pythona](https://www.python.org/dev/peps/pep-0008/#introduction).

# Backend\Python\Good practices\Being_responsible_developer\001_Mixins.md

#### Mixins

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150391101/posts/2153184360

Mixin is a pattern that uses multiple inheritance to inject some additional behaviour to existing class.

##### Tradeoffs

1. Order of inheritance matters

Python resolves hierarchy of inheritance from right to left as stands in MRO.

```python
class Example(Mixin, A, B):
    ...
```
So all methods from class Mixin will override methods with the same names from class A. Only uniquely named methods 
from classes A and B will stay untouched.

So in that case Mixin class has to be always on the left to make sure that it's behaviour is actually executed.

2. Mixin as group of methods

It's strict that mixins should be groups of methods and should not contain any instance variables - otherwise they are 
just usual classes. 

##### Better approach

Instead of injecting additional methods to class it's better to use composition (as stands in "Favor composition over 
inheritance" principle). It makes your code better to read and understand.
# Backend\Python\Good practices\Being_responsible_developer\002_Setting_up_a_complex_software_project.md

#### Setting up a complex software project

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150391480/posts/2153274176

##### Project files

* LICENSE
* README.md
* requirements.txt / pyproject.toml / other dependencies file
* .pylintrc
* .gitignore

##### Project folders

* assets - images, json files, pdfs, other data files
* docs - documentation files for users
* wiki - documentation files for developers
* locales - translations in multilanguage apps
* src - source directory for code
* tests - unit tests
* tools - script for development purposes

##### Modules and packages

Every file in Python is considered as module and every directory is considered as package.

##### Import tips

```python
#### OK
from package_1.file_1 import function_1
from package import file
import package

#### Not OK
from package_1.file_1 import *
```

##### Code organising

Avoid generic packages names like utils, helpers, etc. It would lead to group unrelated things in single package - 
we need to avoid that. Better solution is to split it into smaller packages focused on particular goal.  

##### Architecture as structure

To make code organization easier you can translate picked architecture to directories in application. Example: if you use 
Model-View-Controller architecture pattern you can create model, view, controller directories to store logic for particular architecture part.

# Backend\Python\Good practices\Clean_code\000_Sources.md

##### Sources
[1] https://testdriven.io/blog/clean-code-python

# Backend\Python\Good practices\Clean_code\001_Code_standards.md

#### Code standards
##### PEP 8
PEP 8 naming conventions:
* class names should be CamelCase (MyClass)
* variable names should be snake_case and all lowercase (first_name)
* function names should be snake_case and all lowercase (quick_sort())
* constants should be snake_case and all uppercase (PI = 3.14159)
* modules should have short, snake_case names and all lowercase (numpy)
* single quotes and double quotes are treated the same (just pick one and be consistent)

PEP 8 line formatting:
-   indent using 4 spaces (spaces are preferred over tabs)
-   lines should not be longer than 79 characters
-   avoid multiple statements on the same line
-   top-level function and class definitions are surrounded with two blank lines
-   method definitions inside a class are surrounded by a single blank line
-   imports should be on separate lines

PEP 8 whitespace:
-   avoid extra spaces within brackets or braces
-   avoid trailing whitespace anywhere
-   always surround binary operators with a single space on either side
-   if operators with different priorities are used, consider adding whitespace around the operators with the lowest priority
-   don't use spaces around the = sign when used to indicate a keyword argument

PEP 8 comments:
-   comments should not contradict the code
-   comments should be complete sentences
-   comments should have a space after the # sign with the first word capitalized
-   multi-line comments used in functions (docstrings) should have a short single-line description followed by more text

##### Pythonic Code
There's a big difference between writing Python code and writing Pythonic code. To write Pythonic code you can't just idiomatically translate another language (like Java or C++) to Python; you need to be thinking in Python to being with.
Let's look at an example. We have to add the first 10 numbers together like so  `1 + 2 + ... + 10`.

A non-Pythonic solution would be something like this:
```python
n = 10
sum_all = 0

for i in range(1, n + 1):
    sum_all = sum_all + i

print(sum_all)  # 55
```

A more Pythonic solution might look like this:
```python
n = 10
sum_all = sum(range(1, n + 1))

print(sum_all)  # 55
```
##### The Zen of Python
```
>>> import this

The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```
# Backend\Python\Good practices\Clean_code\002_Code_principles.md

#### Code Principles
##### DRY (Don't repeat yourself)
This is one of the simplest coding principles. Its only rule is that code should not be duplicated. Instead of duplicating lines, find an algorithm that uses iteration. DRY code is easily maintainable. You can take this principle even further with model/data abstraction.

The cons of the DRY principle are that you can end up with too many abstractions, external dependency creations, and complex code. DRY can also cause complications if you try to change a bigger chunk of your codebase. This is why you should avoid DRYing your code too early. It's always better to have a few repeated code sections than wrong abstractions.
##### KISS (Keep it simple, stupid)
The KISS principle states that most systems work best if they are kept simple rather than made complicated. Simplicity should be a key goal in design, and unnecessary complexity should be avoided.
##### SoC (Separation of concerns)
SoC is a design principle for separating a computer program into distinct sections such that each section addresses a separate concern. A concern is a set of information that affects the code of a computer program.

A good example of SoC is  MVC (Model - View - Controller).

If you decide to go with this approach be careful not to split your app into too many modules. You should only create a new module when it makes sense to do so. More modules equals more problems.
##### SOLID
SOLID is extremely useful when writing OOP code. It talks about splitting your class into multiple subclasses, inheritance, abstraction, interfaces, and more.

It consists of the following five concepts:

-   The  **S**ingle-responsibility principle "A class should have one, and only one, reason to change."
-   The  **O**pen–closed principle: "Entities should be open for extension, but closed for modification."
-   The  **L**iskov substitution principle: "Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."
-   The  **I**nterface segregation principle: "A client should not be forced to implement an interface that it doesn’t use."
-   The  **D**ependency inversion principle: "Depend upon abstractions, not concretions."

# Backend\Python\Good practices\Clean_code\003_Code_formatters.md

#### Code Formatters
The most popular Python code formatters are:

-   [black](https://github.com/psf/black)
-   [flake8](https://flake8.pycqa.org/en/latest/index.html)
-   [autopep8](https://github.com/hhatto/autopep8)
-   [yapf](https://github.com/google/yapf)

The most popular Python linters are:

-   [Pylint](https://pylint.pycqa.org/)
-   [PyFlakes](https://github.com/PyCQA/pyflakes)
-   [mypy](http://mypy-lang.org/)
# Backend\Python\Good practices\Clean_code\004_Naming_conventions.md

#### Naming conventions
```python
#### This is bad
#### represents the number of active users
au = 55

#### This is good
active_user_amount = 55
```
# Backend\Python\Good practices\Clean_code\005_Variables.md

##### Variables
###### 1. Use nouns for variable names
###### 2. Use descriptive/intention-revealing names
Other developers should be able to figure out what a variable stores just by reading its name.
###### 3. Use pronounceable names
You should always use pronounceable names; otherwise, you'll have a hard time explaining your algorithms out loud.
###### 4. Avoid using ambiguous abbreviations
Don't try to come up with your own abbreviations. It's better for a variable to have a longer name than a confusing name.
###### 5. Always use the same vocabulary
Avoid using synonyms when naming variables.
```python
#### This is bad
client_first_name = 'Bob'
customer_last_name = 'Smith'

#### This is good
client_first_name = 'Bob'
client_last_name = 'Smith'
```
###### 6. Don't use "magic numbers"
Magic numbers are strange numbers that appear in code, which do not have a clear meaning. Let's take a look at an example:
```python
import random

#### This is bad
def roll():
    return random.randint(0, 36)  # what is 36 supposed to represent?

#### This is good
ROULETTE_POCKET_COUNT = 36

def roll():
    return random.randint(0, ROULETTE_POCKET_COUNT)
```
Instead of using magic numbers, we can extract them into a meaningful variable.
###### 7. Use solution domain names
If you use a lot of different data types in your algorithm or class and you can't figure them out from the variable name itself, don't be afraid to add data type suffix to your variable name. For example:
```python
#### This is good
score_list = [12, 33, 14, 24]
word_dict = {
    'a': 'apple',
    'b': 'banana',
    'c': 'cherry',
}

#### This is bad  (because you can't figure out the data type from the variable name)
names = ["Nick", "Mike", "John"]
```
###### 8. Don't add redundant context
```python
#### This is bad
class Person:
    def __init__(self, person_first_name, person_last_name, person_age):
        self.person_first_name = person_first_name
        self.person_last_name = person_last_name
        self.person_age = person_age


#### This is good
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
```
We're already inside the `Person` class, so there's no need to add a `person_` prefix to every class variable.
# Backend\Python\Good practices\Clean_code\006_Functions.md

##### Functions
###### 1. Use verbs for function names
###### 2. Do not use different words for the same concept
Pick a word for each concept and stick to it. Using different words for the same concept will cause confusion.
```python
#### This is bad
def get_name(): pass
def fetch_age(): pass

#### This is good
def get_name(): pass
def get_age(): pass
```
###### 3. Write short and simple functions
###### 4. Functions should only perform a single task
```python
#### This is bad
def fetch_and_display_personnel():
    data = # ...

    for person in data:
        print(person)


#### This is good
def fetch_personnel():
    return # ...

def display_personnel(data):
    for person in data:
        print(person)
```
###### 5. Keep your arguments at a minimum

# Backend\Python\Good practices\Design_wins\001_Avoid_type_abuse.md

#### Avoid type abuse

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129429

```python
from dataclasses import dataclass

@dataclass
class User:
    first_name: str
    last_name: str
    role: str
```

`role` field in this case is passed as `str`, so you can pass anything to this. Instead of such approach, use Enum for
controlling content of such fields.

```python
from dataclasses import dataclass
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


@dataclass
class User:
    first_name: str
    last_name: str
    role: Role
```
# Backend\Python\Good practices\Design_wins\002_Use_clear_names.md

#### Use clear names

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129452

```python
from dataclasses import dataclass

@dataclass
class Contract:
    amount: float
    hourly_rate: int = 50_00

    def compute_pay(self):
        return self.amount * self.hourly_rate
```
In that case it's not known what `amount` exactly is. Renaming it to `hours_worked` makes it more understandable.

```python
from dataclasses import dataclass

@dataclass
class Contract:
    hours_worked: float
    hourly_rate: int = 50_00

    def compute_pay(self):
        return self.hours_worked * self.hourly_rate
```
# Backend\Python\Good practices\Design_wins\003_Avoid_flags.md

#### Avoid flags

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129460

```python
from dataclasses import dataclass

@dataclass
class BitcoinWallet:
    balance: int = 0  # in satoshi

    def place_order(self, amount: int, sell: bool = False) -> None:
        if sell:
            if amount > self.balance:
                raise NotEnoughFundsError(amount, self.balance)
            print(f"Selling {amount * SATOSHI_TO_BTC_RATE} BTC.")
            self.balance -= amount
        else:
            print(f"Buying {amount * SATOSHI_TO_BTC_RATE} BTC.")
            self.balance += amount
```
Using flag like `sell` in example above indicates, that functions tries to do too many things. It's better to split it 
into many functions focused on particular action.

```python
@dataclass
class BitcoinWallet:
    balance: int = 0  # in satoshi

    def buy(self, amount: int) -> None:
        print(f"Buying {amount * SATOSHI_TO_BTC_RATE} BTC.")
        self.balance += amount

    def sell(self, amount: int) -> None:
        if amount > self.balance:
            raise NotEnoughFundsError(amount, self.balance)
        print(f"Selling {amount * SATOSHI_TO_BTC_RATE} BTC.")
        self.balance -= amount
```
# Backend\Python\Good practices\Design_wins\004_Do_not_use_too_many_args.md

#### Don't use too many arguments

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129469

```python
@dataclass
class Reservation:
    room_id: str
    customer_first_name: str
    customer_last_name: str
    customer_email_address: str
    from_date: datetime
    to_date: datetime
    price: int

@dataclass
class Hotel:
    ...
    def reserve_room(
        self,
        room_id: str,
        customer_first_name: str,
        customer_last_name: str,
        customer_email_address: str,
        from_date: datetime,
        to_date: datetime,
    ) -> None:
        ...

def main():
    hotel = Hotel()
    hotel.add_room(Room(id="1A", size=20, price=200_00))
    
    hotel.reserve_room(
        "1A",
        "Arjan",
        "Codes",
        "hi@arjancodes.com",
        datetime(2022, 7, 15),
        datetime(2022, 7, 17),
    )
```
In this case reserving a room needs plenty of arguments, that describes Customer, that may become separate class.

```python
@dataclass
class Customer:
    first_name: str
    last_name: str
    email_address: str


@dataclass
class Reservation:
    room_id: str
    customer_id: str
    from_date: datetime
    to_date: datetime
    price: int

@dataclass
class Hotel:
    ...
    def reserve_room(
        self,
        room_id: str,
        customer_id: str,
        from_date: datetime,
        to_date: datetime,
    ) -> None:
    ...

def main():
    hotel = Hotel()
    hotel.add_room(Room(id="1A", size=20, price=200_00))

    hotel.add_customer(
        Customer(
            first_name="Arjan", last_name="Codes", email_address="hi@arjancodes.com"
        )
    )
    hotel.reserve_room(
        "1A",
        "hi@arjancodes.com",
        datetime(2022, 7, 15),
        datetime(2022, 7, 17),
    )
```
# Backend\Python\Good practices\Project workflow\001_Project_workflow.md

#### Project workflow

Steps for automate project workflow with code quality ensured:
* GitHub Actions for:
  * Run tests on every repository push
  * Check code quality with linters and security scanners like black, flake8 and bandit
  * Code coverage check (f.e. with CodeCov)
* Documentation build (f.e. with Read The Docs)
* Automated package update in PyPi

https://testdriven.io/blog/python-project-workflow/
https://github.com/MateDawid/course_Python_Project_Workflow
# Backend\Python\Good practices\Pythonic_Patterns\001_Strategy.md

#### Strategy

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946547/posts/2160000087

##### Initial code

```python
@dataclass
class Order:
    price: int
    quantity: int

    def compute_total(self, discount_type: str) -> int:
        if discount_type == "percentage":
            discount = int(self.price * self.quantity * 0.20)
        elif discount_type == "fixed":
            discount = 10_00
        return self.price * self.quantity - discount

    
def main() -> None:
    order = Order(price=100_00, quantity=2)
    print(order)
    print(f"Total: ${order.compute_total('percentage')/100:.2f}")
```

* Discount calculated in Order class, that has plenty of responsibilities now
* Discount type specified by string

##### Strategy pattern

```mermaid
classDiagram
    class Context {

    }
    class Strategy {
        <<interface>>
        execute()
    }
    class ConcreteStrategyA {
        execute()
    }
    class ConcreteStrategyB {
        execute()
    }
    Strategy <|-- ConcreteStrategyA
    Strategy <|-- ConcreteStrategyB
    Context *-- Strategy
```
* Context depends only on abstract Strategy class
* Context does not know anything about implementation details of particular Strategy
* Context only knows base interface that it accepts

```mermaid
classDiagram
    class Order {

    }
    class DiscountStrategy {
        <<interface>>
        +int compute(int price)
    }
    class PercentageDiscount {
        +int compute(int price)
    }
    class FixedDiscount {
        +int compute(int price)
    }
    DiscountStrategy <|-- PercentageDiscount
    DiscountStrategy <|-- FixedDiscount
    Order *-- DiscountStrategy
```

* Separate Strategy class for particular discount type. 
* Order class does not know anything about implementation details of particular DiscountStrategy 
subclass
* Order only needs Strategy class meeting expected interface (which in that case means having "compute" method).

##### Classic approach

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class DiscountStrategy(ABC):
    @abstractmethod
    def compute(self, price: int) -> int:
        pass


class PercentageDiscount(DiscountStrategy):
    def compute(self, price: int) -> int:
        return int(price * 0.20)


class FixedDiscount(DiscountStrategy):
    def compute(self, _: int) -> int:
        return 10_00


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountStrategy

    def compute_total(self) -> int:
        discount = self.discount.compute(self.price * self.quantity)
        return self.price * self.quantity - discount


def main() -> None:
    order = Order(price=100_00, quantity=2, discount=PercentageDiscount())
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")
```

* `DiscountStrategy` abstract class with `.compute` method
* `PercentageDiscount` and `FixedDiscount` with `.compute` methods
* Discount calculated in particular `DiscountStrategy` subclass, not in `Order` class.


To reach the same goal abstract classes may be replaced with protocols.

```python
class DiscountStrategy(Protocol):
    def compute(self, price: int) -> int:
        ...


class PercentageDiscount:
    def compute(self, price: int) -> int:
        return int(price * 0.20)


class FixedDiscount:
    def compute(self, _: int) -> int:
        return 10_00
```

##### Callable approach

```python
from dataclasses import dataclass
from typing import Callable

DiscountFunction = Callable[[int], int]


@dataclass
class PercentageDiscount:
    percentage: float
    
    def __call__(self, price: int) -> int:
        return int(price * self.percentage)

@dataclass
class FixedDiscount:
    fixed: int
    
    def __call__(self, price: int) -> int:
        return self.fixed


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountFunction

    def compute_total(self) -> int:
        discount = self.discount(self.price * self.quantity)
        return self.price * self.quantity - discount

def main() -> None:
    order = Order(price=100_00, quantity=2, discount=FixedDiscount(20_00))
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")
```

* `DiscountFunction` type defined to declare it in Order class.
* `__call__` method overridden in both Discount classes
* Discount classes accepting params to remove magic numbers

##### Functional approach

```python
from dataclasses import dataclass
from typing import Callable

DiscountFunction = Callable[[int], int]


def percentage_discount(price: int) -> int:
    return int(price * 0.20)


def fixed_discount(_: int) -> int:
    return 10_00


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountFunction

    def compute_total(self) -> int:
        discount = self.discount(self.price * self.quantity)
        return self.price * self.quantity - discount

def main() -> None:
    order = Order(price=100_00, quantity=2, discount=percentage_discount)
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")
```

* `DiscountFunction` type defined to declare it in Order class.
* Functions for calculating discount declared
* In that case functions cannot deal with magic numbers


##### Functional approach with closures

```python
from dataclasses import dataclass
from typing import Callable

DiscountFunction = Callable[[int], int]


def percentage_discount(percentage: float) -> DiscountFunction:
    return lambda price: int(price * percentage)


def fixed_discount(fixed: int) -> DiscountFunction:
    return lambda _: fixed


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountFunction

    def compute_total(self) -> int:
        discount = self.discount(self.price * self.quantity)
        return self.price * self.quantity - discount


def main() -> None:
    order = Order(price=100_00, quantity=2, discount=percentage_discount(0.12))
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")
```

* Discount functions as higher order functions (functions that creates another functions)
* Discount functions can accept additional arguments to remove magic numbers
* Discount functions return functions with `DiscountFunction` type. 

##### Functional approach with partial

```python
from dataclasses import dataclass
from functools import partial
from typing import Callable

DiscountFunction = Callable[[int], int]


def percentage_discount(price: int, percentage: float) -> int:
    return int(price * percentage)


def fixed_discount(_: int, fixed: int) -> int:
    return fixed


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountFunction

    def compute_total(self) -> int:
        discount = self.discount(self.price * self.quantity)
        return self.price * self.quantity - discount


def main() -> None:
    perc_discount = partial(percentage_discount, percentage=0.12)
    order = Order(price=100_00, quantity=2, discount=perc_discount)
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")

```

* Classic functions definitions
* Partial function declared in `main()` function
# Backend\Python\Good practices\Pythonic_Patterns\002_Bridge.md

#### Bridge

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946548/posts/2160000213

##### Initial code

```python
def main() -> None:
    # symbol we trade on
    symbol = "BTC/USD"
    trade_amount = 10

    # create the exchange
    exchange = Coinbase()
    
    exchange.buy(symbol, trade_amount)
```
* Specific exchange method declared in `main()` function
* No strategy for TradingBot specified yet

##### Bridge pattern

```mermaid
classDiagram
    class Abstraction {
        <<abstract>>
    }
    RefinedAbstraction1 --|> Abstraction
    RefinedAbstraction2 --|> Abstraction
    class Implementation {
        <<abstract>>
        +implementation()
    }
    Abstraction o-- Implementation : uses
    Implementation <|-- ConcreteImplementation1
    Implementation <|-- ConcreteImplementation2
    ConcreteImplementation1: +implementation()
    ConcreteImplementation2: +implementation()
```
* `Abstraction` uses `Implementation`
* `RefinedAbstraction` classes are strategies for `Abstraction`
* `ConcreteImplementation` classes are strategies for `Implementation`
* Bridge exists between `Abstraction` and `Implementation`
* `Abstraction` strategies know nothing about `Implementation` subclasses

```mermaid
classDiagram
    class Exchange {
        <<abstract>>
        +int[] get_prices(str symbol)
        +buy(str symbol, int amount)
        +sell(str symbol, int amount)
    }
    Exchange <|-- Binance
    Exchange <|-- Coinbase
    class TradingBot {
        <<abstract>>
        +run()
    }
    TradingBot o-- Exchange : uses
    TradingBot <|-- AvgTradingBot
    TradingBot <|-- MinMaxTradingBot
```
* `TradingBot` uses `Exchange`
* `AvgTradingBot` and `MinMaxTradingBot` classes are strategies for `TradingBot`
* `Binance` and `Coinbase` classes are strategies for `Exchange`
* Bridge exists between `TradingBot` and `Exchange`
* `TradingBot` strategies know nothing about `Exchange` subclasses

##### Classic Bridge Pattern

###### Abstract classes for Exchange and TradingBot 

```python
#### exchange.py
from abc import ABC, abstractmethod


class Exchange(ABC):
    @abstractmethod
    def get_prices(self, symbol: str) -> list[int]:
        pass

    @abstractmethod
    def buy(self, symbol: str, amount: int) -> None:
        pass

    @abstractmethod
    def sell(self, symbol: str, amount: int) -> None:
        pass
```
```python
#### trading_bot.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

from exchange import Exchange


@dataclass
class TradingBot(ABC):
    exchange: Exchange

    @abstractmethod
    def should_buy(self, symbol: str) -> bool:
        pass

    @abstractmethod
    def should_sell(self, symbol: str) -> bool:
        pass
```

`TradingBot` receives `Exchange` abstract class as bridge connection between two classes.

###### Subclasses of Bridge components

```python
from exchange import Exchange

PRICE_DATA = {
    "BTC/USD": [
        35_842_00,
        34_069_00,
        33_871_00,
    ],
    "ETH/USD": [
        2_381_00,
        2_233_00,
        2_300_00,
    ],
}


class Coinbase(Exchange):
    def get_prices(self, symbol: str) -> list[int]:
        return PRICE_DATA[symbol]

    def buy(self, symbol: str, amount: int) -> None:
        print(f"[Coinbase] Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: int) -> None:
        print(f"[Coinbase] Selling amount {amount} in market {symbol}.")

```

```python
#### avg_trading_bot.py

import statistics
from dataclasses import dataclass

from trading_bot import TradingBot


@dataclass
class AverageTradingBot(TradingBot):
    window_size: int = 3

    def should_buy(self, symbol: str) -> bool:
        prices = self.exchange.get_prices(symbol)
        list_window = prices[-self.window_size :]
        return prices[-1] < statistics.mean(list_window)

    def should_sell(self, symbol: str) -> bool:
        prices = self.exchange.get_prices(symbol)
        list_window = prices[-self.window_size :]
        return prices[-1] > statistics.mean(list_window)

```
Subclasses of both abstract classes matches parent classes interfaces, so they can be connected by bridge pattern.

###### main.py file
```python
#### main.py

from avg_trading_bot import AverageTradingBot
from coinbase import Coinbase


def main() -> None:
    # symbol we trade on
    symbol = "BTC/USD"
    trade_amount = 10

    # create the exchange
    exchange = Coinbase()

    # create the trading bot
    trading_bot = AverageTradingBot(exchange)  # BRIDGE CONNECTION

    should_buy = trading_bot.should_buy(symbol)
    should_sell = trading_bot.should_sell(symbol)
    if should_buy:
        exchange.buy(symbol, trade_amount)
    elif should_sell:
        exchange.sell(symbol, trade_amount)
    else:
        print("No action needed.")


if __name__ == "__main__":
    main()
```

# Backend\Python\Good practices\Pythonic_Patterns\003_Template_Method.md

#### Template method

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946548/posts/2160000213

Template method allows you to separate the algorithm from its parts. Algorithms stays the same, components changes.

##### Initial code
```python
#### main.py
from bitcoin import BitcoinTradingBot
from ethereum import EthereumTradingBot


def main():
    bitcoin_trader = BitcoinTradingBot()
    bitcoin_trader.trade()

    ethereum_trader = EthereumTradingBot()
    ethereum_trader.trade()

```
```python
#### bitcoin.py

class BitcoinTradingBot:
    ...
    def trade(self) -> None:
    prices = self.get_price_data()
    amount = self.get_amount()

    if self.should_buy(prices):
        self.buy(amount)
    if self.should_sell(prices):
        self.sell(amount)
```
```python
#### ethereum.py

class EthereumTradingBot:
    ...
    def trade(self) -> None:
    prices = self.get_price_data()
    amount = self.get_amount()

    if self.should_buy(prices):
        self.buy(amount)
    if self.should_sell(prices):
        self.sell(amount)
```
* Two TradingBot classes with some differences, but with the same, crucial `.trade()` method.

##### Template method pattern

```mermaid
classDiagram
    class AbstractClass {
        <<abstract>>
        templateMethod()
        primitive1()*
        primitive2()*
        primitive3()*
    }
    class ConcreteClassA {
        primitive1()
        primitive2()
        primitive3()
    }
    class ConcreteClassB {
        primitive1()
        primitive2()
        primitive3()
    }
    AbstractClass <|-- ConcreteClassA
    AbstractClass <|-- ConcreteClassB
```

* AbstractClass with `templateMethod()` implementation
* Abstract `primitive` methods, that need to be implemented in subclasses.
* `ConcreteClass` subclasses of `AbstractClass` with `primitive` methods implemented

```mermaid
classDiagram
    class TradingBot {
        <<abstract>>
        trade()
        buy(amount: int)*
        sell(amount)*
        should_buy(prices: list[int])*
        should_sell(prices: list[int])*
        get_price_data()*
        get_amount()*
    }
    class BitcoinTradingBot {
        buy(amount: int)
        sell(amount)
        should_buy(prices: list[int])
        should_sell(prices: list[int])
        get_price_data()
        get_amount()
    }
    class EthereumTradingBot {
        buy(amount: int)
        sell(amount)
        should_buy(prices: list[int])
        should_sell(prices: list[int])
        get_price_data()
        get_amount()
    }
    TradingBot <|-- BitcoinTradingBot
    TradingBot <|-- EthereumTradingBot
```

* `TradingBot` with `trade()` implementation
* Abstract methods like `buy()`, `sell()`, etc., that need to be implemented in subclasses.
* `BitcoinTradingBot` and `EthereumTradingBot` subclasses of `TradingBot` with abstract methods like `buy()`, `sell()` 
methods implemented

##### Classic Template method

```python
#### trading_bot.py

from abc import ABC, abstractmethod


class TradingBot(ABC):
    @abstractmethod
    def buy(self, amount: int) -> None:
        pass

    @abstractmethod
    def sell(self, amount: int) -> None:
        pass

    @abstractmethod
    def should_buy(self, prices: list[int]) -> bool:
        pass

    @abstractmethod
    def should_sell(self, prices: list[int]) -> bool:
        pass

    @abstractmethod
    def get_price_data(self) -> list[int]:
        pass

    @abstractmethod
    def get_amount(self) -> int:
        pass

    def trade(self) -> None:
        prices = self.get_price_data()
        amount = self.get_amount()

        if self.should_buy(prices):
            self.buy(amount)
        if self.should_sell(prices):
            self.sell(amount)
```
* Abstract class `TradingBot`
* Abstract methods for subclasses declared
* `.trade()` method implementation

```python
#### bitcoin.py
from trading_bot import TradingBot


class BitcoinTradingBot(TradingBot):
    ...

```
```python
#### ethereum.py
from trading_bot import TradingBot


class EthereumTradingBot(TradingBot):
    ...
```
* `BitcoinTradingBot` and `EthereumTradingBot` as `TradingBot` subclasses
* `BitcoinTradingBot` and `EthereumTradingBot` have their own implementations of `TradingBot` abstract methods
* `BitcoinTradingBot` and `EthereumTradingBot` inherit `.trade()` method from `TradingBot` class.
# Backend\Python\Good practices\Pythonic_Patterns\004_Abstract_Factory.md

#### Abstract Factory

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946549/posts/2160000491

##### Abstract Factory pattern

```mermaid
classDiagram
    direction LR
    class AbstractFactory {
        <<abstract>>
        createProductA()*
        createProductB()*
    }
    class ConcreteFactory1 {
        createProductA()
        createProductB()
    }
    class ConcreteFactory2 {
        createProductA()
        createProductB()
    }
    ConcreteFactory1 --|> AbstractFactory
    ConcreteFactory2 --|> AbstractFactory
    class AbstractProductA {
        <<abstract>>
    }
    ProductA1 --|> AbstractProductA
    ProductA2 --|> AbstractProductA
    class AbstractProductB {
        <<abstract>>
    }
    ProductB1 --|> AbstractProductB
    ProductB2 --|> AbstractProductB
    ConcreteFactory1 ..> ProductA1
    ConcreteFactory1 ..> ProductB1
    ConcreteFactory2 ..> ProductA2
    ConcreteFactory2 ..> ProductB2
```

```mermaid
classDiagram
    direction LR
    class TaxFactory {
        <<abstract>>
        create_income_tax_calculator()*
        create_capital_tax_calculator()*
    }
    class SimpleTaxFactory {
        create_income_tax_calculator()
        create_capital_tax_calculator()
    }
    class NLTaxFactory {
        create_income_tax_calculator()
        create_capital_tax_calculator()
    }
    SimpleTaxFactory --|> TaxFactory
    NLTaxFactory --|> TaxFactory
    class IncomeTaxCalculator {
        <<abstract>>
        int calculate_tax(income, apply_floor)*
    }
    SimpleIncomeTaxCalculator --|> IncomeTaxCalculator
    NLTaxCalculator --|> IncomeTaxCalculator
    class CapitalTaxCalculator {
        <<abstract>>
        int calculate_tax(capital)*
    }
    PercentageCapitalTaxCalculator --|> CapitalTaxCalculator
    ZeroCapitalTaxCalculator --|> CapitalTaxCalculator
    SimpleTaxFactory ..> SimpleIncomeTaxCalculator
    SimpleTaxFactory ..> ZeroCapitalTaxCalculator
    NLTaxFactory ..> NLTaxCalculator
    NLTaxFactory ..> PercentageCapitalTaxCalculator
```


##### Classic Abstract Factory

```python
from abc import ABC, abstractmethod


class IncomeTaxCalculator(ABC):
    @abstractmethod
    def calculate_tax(self, income: int, apply_floor=True) -> int:
        """Calculates income tax."""


class CapitalTaxCalculator(ABC):
    @abstractmethod
    def calculate_tax(self, capital: int) -> int:
        """Calculates capital tax."""
```
* Abstract classes for TaxCalculator objects

```python
from dataclasses import dataclass


@dataclass
class SimpleIncomeTaxCalculator(IncomeTaxCalculator):
    tax_rate: float = 0.1

    def calculate_tax(self, income: int, apply_floor=True) -> int:
        return int(income * self.tax_rate)


@dataclass
class NLTaxCalculator(IncomeTaxCalculator):
    floor: int = 10_000_00

    def calculate_tax(self, income: int, apply_floor=True) -> int:
        brackets: list[tuple[int | None, float]] = [
            (69_398_00, 0.37),
            (None, 0.495),
        ]
        taxable_income = income
        if apply_floor:
            taxable_income -= self.floor

        total_tax = 0
        for max_income, percentage in brackets:
            bracket_income = min(taxable_income, max_income or taxable_income)
            total_tax += int(bracket_income * percentage)
            taxable_income -= bracket_income
            if taxable_income <= 0:
                break
        return total_tax


@dataclass
class PercentageCapitalTaxCalculator(CapitalTaxCalculator):
    tax_rate: float = 0.05

    def calculate_tax(self, capital: int) -> int:
        return int(capital * self.tax_rate)


class ZeroCapitalTaxCalculator(CapitalTaxCalculator):
    def calculate_tax(self, capital: int) -> int:
        return 0
```

* TaxCalculator objects inheriting from abstract classes

```python
from abc import ABC, abstractmethod


class TaxFactory(ABC):
    @abstractmethod
    def create_income_tax_calculator(self) -> IncomeTaxCalculator:
        """Creates an income tax calculator."""

    @abstractmethod
    def create_capital_tax_calculator(self) -> CapitalTaxCalculator:
        """Creates a capital tax calculator."""
```
* Abstract class for Factory

```python
class SimpleTaxFactory(TaxFactory):
    def create_income_tax_calculator(self) -> IncomeTaxCalculator:
        return SimpleIncomeTaxCalculator()

    def create_capital_tax_calculator(self) -> CapitalTaxCalculator:
        return ZeroCapitalTaxCalculator()


class NLTaxFactory(TaxFactory):
    def create_income_tax_calculator(self) -> IncomeTaxCalculator:
        return NLTaxCalculator()

    def create_capital_tax_calculator(self) -> CapitalTaxCalculator:
        return PercentageCapitalTaxCalculator()
```
* Subclasses of Factory abstact class for producing TaxCalculator objects.

```python
def compute_tax(
    factory: TaxFactory, income: int, capital: int, apply_floor: bool = True
) -> int:
    """Computes tax for a given income and capital."""

    # create the calculator
    income_tax_calculator = factory.create_income_tax_calculator()
    capital_tax_calculator = factory.create_capital_tax_calculator()

    # calculate the tax
    income_tax = income_tax_calculator.calculate_tax(income, apply_floor)
    capital_tax = capital_tax_calculator.calculate_tax(capital)

    # return the total tax
    return income_tax + capital_tax
```
* Function for tax computing basing on passed TaxFactory

##### Functional approach

```python
from typing import Callable, Optional

IncomeTaxCalculator = Callable[[int, Optional[bool]], int]
CapitalTaxCalculator = Callable[[int], int]
TaxFactory = tuple[IncomeTaxCalculator, CapitalTaxCalculator]


def calculate_income_tax_simple(
    income: int, apply_floor=True, tax_rate: float = 0.1
) -> int:
    return int(income * tax_rate)


def calculate_income_tax_nl(income: int, apply_floor=True) -> int:
    floor = 10_000_00
    brackets: list[tuple[int | None, float]] = [
        (69_398_00, 0.37),
        (None, 0.495),
    ]
    taxable_income = income
    if apply_floor:
        taxable_income -= floor

    total_tax = 0
    for max_income, percentage in brackets:
        bracket_income = min(taxable_income, max_income or taxable_income)
        total_tax += int(bracket_income * percentage)
        taxable_income -= bracket_income
        if taxable_income <= 0:
            break
    return total_tax


def calculate_percentage_capital_tax(capital: int, tax_rate: float = 0.05) -> int:
    return int(capital * tax_rate)


def calculate_zero_capital_tax(_: int) -> int:
    return 0


simple_tax_factory: TaxFactory = (
    calculate_income_tax_simple,
    calculate_zero_capital_tax,
)

nl_tax_factory: TaxFactory = (
    calculate_income_tax_nl,
    calculate_percentage_capital_tax,
)


def compute_tax(
    factory: TaxFactory, income: int, capital: int, apply_floor: bool = True
) -> int:
    """Computes tax for a given income and capital."""
    income_tax_calculator, capital_tax_calculator = factory

    # calculate the tax
    income_tax = income_tax_calculator(income, apply_floor)
    capital_tax = capital_tax_calculator(capital)

    # return the total tax
    return income_tax + capital_tax
```
# Backend\Python\Good practices\Pythonic_Patterns\005_Pipeline_patterns.md

#### Pipeline patterns

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946552/posts/2160000607

##### Chain of responsibility pattern

```mermaid
classDiagram
    Client ..> Handler
    class Handler {
        <<abstract>>
        setNext(handler: Handler)
        handle(request)
    }
    Handler --> Handler : next
    class ConcreteHandler1 {
        setNext(handler: Handler)
        handle(request)
    }
    class ConcreteHandler2 {
        setNext(handler: Handler)
        handle(request)
    }
    ConcreteHandler1 --|> Handler
    ConcreteHandler2 --|> Handler
```

* Client uses a Handler for some process
* Handler has setNext() method to indicate, what next Handler should process request

```mermaid
classDiagram
    Client ..> Handler
    class Handler {
        <<abstract>>
        set_next(handler: Handler)
        handle_click_event()
        bool on_click()
    }
    Handler --> Handler : next
    class Button {
        name: str
        disabled: bool
        set_next(handler: Handler)
        handle_click_event(request)
        bool on_click()
    }
    class Panel {
        name: str
        disabled: bool
        set_next(handler: Handler)
        handle_click_event(request)
        bool on_click()
    }
    class Window {
        name: str
        set_next(handler: Handler)
        handle_click_event(request)
        bool on_click()
    }
    Button --|> Handler
    Panel --|> Handler
    Window --|> Handler
```
* Client uses a Handler subclasses for processing request
* Button, Panel and Window as subclasses of Handler abstract class

##### Chain of responsibility implementation

```python
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Optional


class Handler(ABC):
    def __init__(self):
        self.next: Optional[Handler] = None

    def set_next(self, handler: Handler) -> None:
        self.next = handler

    def handle_click_event(self) -> None:
        if self.on_click() and self.next:
            self.next.handle_click_event()

    def on_click(self) -> bool:
        """Handle a click event."""
        return True


@dataclass
class Button(Handler):
    name: str = "button"
    disabled: bool = False

    def on_click(self) -> bool:
        if self.disabled:
            return True
        print(f"Button [{self.name}] handling click.")
        return False


@dataclass
class Panel(Handler):
    name: str = "panel"
    disabled: bool = False


@dataclass
class Window(Handler):
    name: str = "window"

    def on_click(self) -> bool:
        print(f"Window [{self.name}] handling click.")
        return False


def main() -> None:
    button = Button(name="my_button", disabled=False)
    panel = Panel(name="my_panel", disabled=False)
    window = Window(name="my_window")

    # setup the chain of responsibility
    button.set_next(panel)
    panel.set_next(window)

    button.handle_click_event()
```

##### Sequence of functions

```python
from functools import partial, reduce
from typing import Callable

ComposableFunction = Callable[[float], float]

#### Helper function for composing functions
def compose(*functions: ComposableFunction) -> ComposableFunction:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def add_three(x: float) -> float:
    return x + 3


def multiply_by_two(x: float) -> float:
    return x * 2


def add_n(x: float, n: float) -> float:
    return x + n


def main():
    x = 12
    # oldres = multiplyByTwo(multiplyByTwo(addThree(addThree(x))))
    myfunc = compose(
        partial(add_n, n=3), partial(add_n, n=2), multiply_by_two, multiply_by_two
    )
    result = myfunc(x)
    print(result)


if __name__ == "__main__":
    main()

```
# Backend\Python\Good practices\Pythonic_Patterns\006_Notification_patterns.md

#### Notification patterns

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946554/posts/2160000668

##### Observer pattern

```mermaid
classDiagram
    class Observer {
        <<abstract>>
        +notify()
    }
    class ConcreteObserver1 {
        +notify()
    }
    class ConcreteObserver2 {
        +notify()
    }
    ConcreteObserver1 --|> Observer
    ConcreteObserver2 --|> Observer
    Subject o-- Observer : notifies
    class Subject {
        observers: list[Observer]
        +registerObserver(observer)
        +unregisterObserver(observer)
        +notifyObservers()
    }
```
* Observer abstract class for notifier objects
* Concrete subclasses of Observer class - like email notifier, sms notifier, etc.
* Subject class for business logic handling

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Observer(ABC):
    @abstractmethod
    def notify(self) -> None:
        pass


class ConcreteObserver(Observer):
    def notify(self) -> None:
        print("ConcreteObserver.notify")


@dataclass
class Subject:
    observers: list[Observer] = field(default_factory=list)

    def register_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def unregister_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self) -> None:
        for obs in self.observers:
            obs.notify()

    def do_something(self) -> None:
        print("Subject.do_something")
        self.notify_observers()


def main() -> None:
    subject = Subject()
    observer = ConcreteObserver()
    subject.register_observer(observer)
    subject.do_something()
```

##### Mediator pattern

```mermaid
classDiagram
    class Mediator {
        <<abstract>>
        notify(sender: Component, event)*
    }
    class ConcreteMediator {
        notify(sender: Component, event)
        do_something()
    }
    class Component {
        mediator: Mediator
    }
    ConcreteMediator --|> Mediator
    ConcreteComponent1 --|> Component
    ConcreteComponent2 --|> Component
    Component --> Mediator
```
* Abstract `Mediator` class, that has `notify` method
* `Mediator` subclasses, that have `notify` method implemented
* `Component` class with mediator variable
* Subclasses of `Component` class
* Mediator is notified by Component, that something is happening

```mermaid
classDiagram
    class Mediator {
        <<abstract>>
        notify(sender: Component, event)*
    }
    class LoginPage {
        notify(sender: Component, event)
        start_login()
    }
    class Component {
        mediator: Mediator
    }
    LoginPage --|> Mediator
    Button --|> Component
    TextField --|> Component
    Component --> Mediator
```

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: Component):
        """Notify all components that a change has occurred."""


@dataclass
class Component(ABC):
    mediator: Optional[Mediator] = None


@dataclass
class Button(Component):
    name: str = "login"

    def click(self):
        if self.mediator:
            self.mediator.notify(self)


@dataclass
class TextField(Component):
    name: str = "email"
    value: str = ""
    disabled: bool = False


@dataclass
class LoginPage(Mediator):
    text_field: TextField
    button: Button

    def __post_init__(self):
        self.text_field.mediator = self
        self.button.mediator = self

    def notify(self, sender: Component):
        if sender == self.button:
            self.start_login()

    def start_login(self):
        print("Disabling text field.")
        self.text_field.disabled = True
        print(f"Starting login process with email address {self.text_field.value}.")


def main() -> None:
    text_field = TextField(name="email", disabled=False)
    button = Button(name="login")

    # create the login page
    _ = LoginPage(text_field=text_field, button=button)

    text_field.value = "hi@arjancodes.com"
    button.click()
    print(f"Text field disabled: {text_field.disabled}")
```
##### Event Aggregator / Pub-Sub

```python
#### event/core.py

from typing import Callable

from lib.db import User

EventHandler = Callable[[User], None]

subscribers: dict[str, list[EventHandler]] = {}


def subscribe(event_type: str, handler: EventHandler) -> None:
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(handler)


def post_event(event_type: str, user: User) -> None:
    if event_type not in subscribers:
        return
    for handler in subscribers[event_type]:
        handler(user)
```
* EventHandler type for function handling event for particular User
* Dictionary with events, and list of EventHandlers for single event in `subscribers`
* `subscribe` method for updating `subscribers` dict with new handler for particular event
* `post_event` method for performing all handlers for particular event for given User

```python
#### event/email.py
from lib.db import User
from lib.email import send_email

from event.core import subscribe


def handle_user_registered_event(user: User) -> None:
    # send a welcome email
    send_email(
        user.name,
        user.email,
        "Welcome",
        f"Thanks for registering, {user.name}!\nRegards, The team",
    )


def handle_user_password_forgotten_event(user: User) -> None:
    # send a password reset message
    send_email(
        user.name,
        user.email,
        "Reset your password",
        f"To reset your password, use this code: {user.reset_code}.\nRegards, The team",
    )


def handle_user_upgrade_plan_event(user: User) -> None:
    # send a thank you email
    send_email(
        user.name,
        user.email,
        "Thank you",
        f"Thanks for upgrading, {user.name}! You're gonna love it. \nRegards, The team",
    )


def setup_email_event_handlers() -> None:
    subscribe("user_registered", handle_user_registered_event)
    subscribe("user_password_forgotten", handle_user_password_forgotten_event)
    subscribe("user_upgrade_plan", handle_user_upgrade_plan_event)
```
* Three EventHandler functions subscribed for email handling

```python
####api/plan.py
from event.core import post_event
from lib.db import find_user


def upgrade_plan(email: str) -> None:
    # find the user
    user = find_user(email)

    # upgrade the plan
    user.plan = "paid"

    # post an event
    post_event("user_upgrade_plan", user)
```
* Performing business logic of upgrading plan
* `post_event()` method used to notify user with registered handlers for given event name instead of setting up
handlers in `upgrade_plan` function


```python
#### main.py
from api.plan import upgrade_plan
from api.user import password_forgotten, register_new_user
from event.email import setup_email_event_handlers
from event.log import setup_log_event_handlers
from event.slack import setup_slack_event_handlers


def main() -> None:
    # initialize the event structure
    setup_slack_event_handlers()
    setup_log_event_handlers()
    setup_email_event_handlers()

    # register a new user
    register_new_user("Arjan", "BestPasswordEva", "hi@arjancodes.com")

    # send a password reset message
    password_forgotten("hi@arjancodes.com")

    # upgrade the plan
    upgrade_plan("hi@arjancodes.com")
```
* In main function all different handlers are being set up - email, slack, and log
* Business logic performed in  `register_new_user`, `password_forgotten`, `upgrade_plan` has `post_event` method used 
inside for handling events 
# Backend\Python\Good practices\Pythonic_Patterns\007_Registry.md

#### Registry

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946555/posts/2160000778

##### Registry pattern
```mermaid
classDiagram

    class AbstractFactory {
        <<abstract>>
        Product create()*
    }
    class ConcreteFactory1 {
        Product create()
    }
    class ConcreteFactory2 {
        Product create()
    }
    class Product {
        <<abstract>>
    }
    class Registry {
        registry: dict[str, AbstractFactory]
        register(type: str, factory: AbstractFactory)
        unregister(type: str)
        Product create(type: str)
    }

    ConcreteFactory1 --|> AbstractFactory
    ConcreteFactory2 --|> AbstractFactory
    ConcreteProduct1 --|> Product
    ConcreteProduct2 --|> Product
    ConcreteFactory1 ..> ConcreteProduct1
    ConcreteFactory2 ..> ConcreteProduct2
    Registry o-- AbstractFactory
```
* Registry contains str for representing particular AbstractFactory subclass.
* ConcreteFactories as AbstractFactory subclasses
* Product as abstract class for ConcreteProducts
* ConcreteFactories only create ConcreteProducts
* Registry handles creating objects of particular type 
```mermaid
classDiagram

    class TaskFactory {
        <<abstract>>
        Task create(args)*
    }
    class PulseFactory {
        Task create(args)
    }
    class RecalibrateFactory {
        Task create(args)
    }
    class ReinforceFactory {
        Task create(args)
    }
    class Task {
        <<abstract>>
        run()*
    }
    class TaskRegistry {
        registry: dict[str, TaskFactory]
        register(type: str, factory: TaskFactory)
        unregister(type: str)
        Task create(type: str)
    }

    PulseFactory --|> TaskFactory
    RecalibrateFactory --|> TaskFactory
    ReinforceFactory --|> TaskFactory
    Pulse --|> Task
    Recalibrate --|> Task
    Reinforce --|> Task

    PulseFactory ..> Pulse
    RecalibrateFactory ..> Recalibrate
    ReinforceFactory ..> Reinforce
    TaskRegistry o-- TaskFactory
```
* TaskRegistry contains str for representing particular TaskFactory subclass.
* PulseFactory, ReinforceFactory and RecalibrateFactory as TaskFactory subclasses
* Task as abstract class for Pulse, Recalibrate and Reinforce classes
* PulseFactory, ReinforceFactory and RecalibrateFactory only create Pulse, Recalibrate and Reinforce classes
* TaskRegistry handles creating objects of particular type 

##### Implementation
```python
#### registry.py

from typing import Any, Protocol


class Task(Protocol):
    def run(self) -> None:
        """Run the task."""


class TaskFactory(Protocol):
    def create(self, args: dict[str, Any]) -> Task:
        """Creates a new task."""
```
* Protocol for Task defined
* Factory for Task class

```python
#### tasks.py
from dataclasses import dataclass
from typing import Any

from registry import Task


@dataclass
class Pulse:
    strength: int

    def run(self) -> None:
        print(
            f"Sending a subspace pulse of {self.strength} microPicards to the converter assembly."
        )


@dataclass
class Recalibrate:
    target: str

    def run(self) -> None:
        print(f"Recalibrating the {self.target}.")


@dataclass
class Reinforce:
    plating_type: str
    target: str

    def run(self) -> None:
        print(f"Reinforcing {self.plating_type} plating of {self.target}.")


class PulseFactory:
    def create(self, args: dict[str, Any]) -> Task:
        return Pulse(**args)


class RecalibrateFactory:
    def create(self, args: dict[str, Any]) -> Task:
        return Recalibrate(**args)


class ReinforceFactory:
    def create(self, args: dict[str, Any]) -> Task:
        return Reinforce(**args)
```
* Reinforce, Recalibrate and Pulse classes matching Task protocol
* Factories for Reinforce, Recalibrate and Pulse classes matching TaskFactory protocol

```python
#### registry.py

from typing import Any, Protocol

...

class TaskRegistry:
    def __init__(self):
        self.registry: dict[str, TaskFactory] = {}

    def register(self, task_type: str, factory: TaskFactory) -> None:
        self.registry[task_type] = factory

    def unregister(self, task_type: str) -> None:
        self.registry.pop(task_type, None)

    def create(self, args: dict[str, Any]) -> Task:
        args_copy = args.copy()
        task_type = args_copy.pop("type")
        try:
            factory = self.registry[task_type]
        except KeyError:
            raise ValueError(f"Unknown task type: {task_type!r}") from None
        return factory.create(args_copy)

```
* TaskRegistry class for registering/unregistering Factory for particular task type
* `.create()` method for creating object for given task

```python
#### main.py

import json

from registry import TaskRegistry
from tasks import PulseFactory, RecalibrateFactory, ReinforceFactory


def main() -> None:

    # register a couple of tasks
    task_registry = TaskRegistry()
    task_registry.register("pulse", PulseFactory())
    task_registry.register("recalibrate", RecalibrateFactory())
    task_registry.register("reinforce", ReinforceFactory())

    # read data from a JSON file
    with open("./tasks.json", encoding="utf-8") as file:
        data = json.load(file)

        # create the tasks
        tasks = [task_registry.create(item) for item in data["tasks"]]

        # run the tasks
        for task in tasks:
            task.run()
```
* TaskRegistry init
* Registering factories for particular Task type
* Creating Task objects by registered TaskFactory for all tasks in JSON file
* Running created Task object

##### Functional approach

```python
#### registry.py

from typing import Any, Callable

task_functions: dict[str, Callable[..., None]] = {}


def register(task_type: str, task_fn: Callable[..., None]) -> None:
    task_functions[task_type] = task_fn


def unregister(task_type: str) -> None:
    task_functions.pop(task_type, None)


def run(arguments: dict[str, Any]) -> None:
    args_copy = arguments.copy()
    task_type = args_copy.pop("type")
    task_functions[task_type](**args_copy)
```
* `task_functions` dictionary for storing registered functions
* Functions instead of TaskRegistry class methods

```python
#### main.py

import json

from loader import load_plugins
from registry import register, run


def send_pulse(strength: int) -> None:
    print(
        f"Sending a subspace pulse of {strength} microPicards to the converter assembly."
    )


def recalibrate(target: str) -> None:
    print(f"Recalibrating the {target}.")


def reinforce(plating_type: str, target: str) -> None:
    print(f"Reinforcing {plating_type} plating of {target}.")


def main() -> None:

    # register a couple of tasks
    register("pulse", send_pulse)
    register("recalibrate", recalibrate)
    register("reinforce", reinforce)

    # read data from a JSON file
    with open("./tasks.json", encoding="utf-8") as file:
        data = json.load(file)

        # load the plugins
        load_plugins(data["plugins"])

        # run the tasks
        for task in data["tasks"]:
            run(task)
```
* No Factories for objects creation, as it only performs operations, not storing any data
* Functions for particular Task execution defined
* Registering function for particular Task type
* Loading plugins for additional tasks from JSON file

```json
// tasks.json
        
{
  "plugins": ["inject"],
  "tasks": [
    {
      "type": "pulse",
      "strength": 190
    },
    {
      "type": "recalibrate",
      "target": "Thoron subspace transponder"
    },
    {
      "type": "reinforce",
      "plating_type": "biogenic",
      "target": "the deflector array"
    },
    {
      "type": "inject",
      "material": "tachyons",
      "target": "molecular transporter resonator"
    }
  ]
}

```
```python
#### inject.py

from registry import register


def inject(material: str, target: str) -> None:
    print(f"Injecting {material} into {target}.")


register("inject", inject)

```
* inject plugin defined in separate file
* plugin registered

```python
#### loader.py
import importlib


def load_plugins(plugins: list[str]) -> None:
    for plugin in plugins:
        importlib.import_module(plugin)

```
* Function for loading additional plugins defined.
# Backend\Python\Good practices\Pythonic_Patterns\008_Command.md

#### Command

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946559/posts/2156337466

##### Command pattern
```mermaid
classDiagram
    class Command {
        <<abstract>>
        execute()*
    }
    class ConcreteCommand {
        execute()
    }
    class Receiver {
        action()
    }
    ConcreteCommand --|> Command
    Invoker ..> Command
    Receiver --o ConcreteCommand
```
* `Command` abstract class with `execute` method
* `ConcreteCommand` class with implementation of `execute` method
* `Receiver` performing some action by `ConcreteCommand`
* `Invoker` invoking abstract `Command`
```mermaid
classDiagram
    class Command {
        <<abstract>>
        execute()*
    }
    class AppendText {
        execute()
    }
    class Clear {
        execute()
    }
    class ChangeTitle {
        execute()
    }
    class Document {
        clear()
        append(text: str)
        set_title(title: str)
    }
    AppendText --|> Command
    Clear --|> Command
    ChangeTitle --|> Command
    TextController ..> Command
    Document --o Clear
    Document --o ChangeTitle
    Document --o AppendText
```
* `Command` abstract class with `execute` method
* `AppendText`, `Clear` and `ChangeTitle` classes with implementations of `execute` method
* `Document` performing some action by `Command` subclasses.
* `TextController` invoking abstract `Command`

##### Classic Command Pattern
```python
#### text/controller.py
from dataclasses import dataclass, field

from .edit import Edit


@dataclass
class TextController:
    undo_stack: list[Edit] = field(default_factory=list)

    def execute(self, edit: Edit) -> None:
        edit.execute()
        self.undo_stack.append(edit)

    def undo(self) -> None:
        if not self.undo_stack:
            return
        edit = self.undo_stack.pop()
        edit.undo()

    def undo_all(self) -> None:
        while self.undo_stack:
            self.undo()

```
* TextController class with `execute` and `undo` methods defined
* `undo_stack` list of performed commands for ability to undo command
* `undo_all` for clearing all changes performed by commands

```python
#### text/commands.py

from dataclasses import dataclass, field

from .document import Document
from .edit import Edit


@dataclass
class AppendText:
    doc: Document
    text: str

    def execute(self) -> None:
        self.doc.append(self.text)

    def undo(self) -> None:
        self.doc.text = self.doc.text[: -len(self.text)]


@dataclass
class Clear:
    doc: Document
    _old_text: str = ""

    def execute(self) -> None:
        self._old_text = self.doc.text
        self.doc.clear()

    def undo(self) -> None:
        self.doc.append(self._old_text)


@dataclass
class ChangeTitle:
    doc: Document
    title: str
    _old_title: str = ""

    def execute(self) -> None:
        self._old_title = self.doc.title
        self.doc.set_title(self.title)

    def undo(self) -> None:
        self.doc.set_title(self._old_title)


@dataclass
class Batch:
    commands: list[Edit] = field(default_factory=list)

    def execute(self) -> None:
        for command in self.commands:
            command.execute()

    def undo(self) -> None:
        for command in reversed(self.commands):
            command.undo()

```
* Commands classes defined
* Each class has `execute` and `undo` method defined
* `Batch` command to execute multiple commands

```python
#### main.py

from text.commands import AppendText, Batch, ChangeTitle, Clear
from text.controller import TextController
from text.processor import Processor


def main() -> None:

    # create a processor
    processor = Processor()

    # create a text controller
    controller = TextController()

    # create some documents
    doc1 = processor.create_document("ArjanCodes")
    doc2 = processor.create_document("Meeting Notes")

    # append some text to the documents
    controller.execute(AppendText(doc1, "Hello World!"))
    controller.execute(AppendText(doc2, "The meeting started at 9:00."))

    # update the title of the first document
    controller.execute(ChangeTitle(doc1, "Important Meeting"))
    controller.undo()

    print(processor)

    # execute a batch of commands
    controller.execute(
        Batch(
            commands=[
                AppendText(doc1, "Hello World!"),
                ChangeTitle(doc2, "Useless Meeting."),
                Clear(doc2),
            ]
        )
    )

    print(processor)

    # undo
    controller.undo()
    print(processor)
```

##### Functional approach
```python
#### text/commands.py

from typing import Callable

from .document import Document

UndoFunction = Callable[[], None]
EditFunction = Callable[[], UndoFunction]


def append_text(doc: Document, text: str) -> UndoFunction:
    def undo():
        doc.text = doc.text[: -len(text)]

    doc.append(text)
    return undo


def clear_text(doc: Document) -> UndoFunction:
    text = doc.text

    def undo():
        doc.text += text

    doc.clear()
    return undo


def change_title(doc: Document, title: str) -> UndoFunction:
    old_title = doc.title

    def undo():
        doc.set_title(old_title)

    doc.set_title(title)
    return undo


def batch(edits: list[EditFunction]) -> UndoFunction:
    undo_fns = [edit() for edit in edits]

    def undo():
        for undo_fn in reversed(undo_fns):
            undo_fn()

    return undo
```
* Higher order functions instead of classes for particular command
* Closure for returning undo function

```python
#### main.py

from functools import partial

from text.commands import append_text, batch, change_title, clear_text
from text.processor import Processor


def main() -> None:

    # create a processor
    processor = Processor()

    # create some documents
    doc1 = processor.create_document("ArjanCodes")
    doc2 = processor.create_document("Meeting Notes")

    print(processor)

    # append some text to the documents
    undo_append = append_text(doc1, "Hello World!")
    append_text(doc2, "The meeting started at 9:00.")

    # update the title of the first document
    undo_title_change = change_title(doc1, "Important Meeting")

    print(processor)

    # undo things
    undo_append()
    undo_title_change()

    print(processor)

    # execute a batch of commands
    undo_batch = batch(
        [
            partial(append_text, doc1, "Hello World!"),
            partial(change_title, doc1, "Useless Meeting"),
            partial(clear_text, doc2),
        ]
    )

    print(processor)

    # undo
    undo_batch()

    print(processor)


if __name__ == "__main__":
    main()

```
# Backend\Python\Good practices\Pythonic_Patterns\009_Callback.md

#### Callback

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2150393709/posts/2160000927

##### Callback pattern

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Button:
    label: str
    on_click: Callable[[Button], None] = lambda _: None

    def click(self) -> None:
        print(f"Clicked on [{self.label}].")
        self.on_click(self)


def main() -> None:
    def click_handler(button: Button) -> None:
        print(f"Handling click for button [{button.label}].")

    my_button = Button(label="Do something", on_click=click_handler)
    # my_button = Button(
    #     label="Do something", on_click=lambda _: print("Handling click!")
    # )
    my_button.click()
```
* Button class having `click` method.
* `click` method performing `on_click` function defined on class setup

# Backend\Python\Good practices\Pythonic_Patterns\010_Function_wrapper.md

#### Function wrapper

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2150393709/posts/2160000931

##### Wrapper pattern

```python
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Callable


class LoyaltyProgram(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3


DiscountFunction = Callable[[int], int]


def percentage_discount(price: int, percentage: float) -> int:
    return int(price * percentage)


def fixed_discount(_: int, fixed: int) -> int:
    return fixed


def loyalty_program_discount(price: int, loyalty: LoyaltyProgram) -> int:
    loyalty_percentages = {
        LoyaltyProgram.BRONZE: 0.1,
        LoyaltyProgram.SILVER: 0.15,
        LoyaltyProgram.GOLD: 0.2,
    }
    return percentage_discount(price, loyalty_percentages[loyalty])


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountFunction

    def compute_total(self) -> int:
        discount = self.discount(self.price * self.quantity)
        return self.price * self.quantity - discount


def main() -> None:
    loyalty = LoyaltyProgram.SILVER
    loyalty_discount = partial(loyalty_program_discount, loyalty=loyalty)
    order = Order(price=100_00, quantity=2, discount=loyalty_discount)
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")
```
* `loyalty_program_discount` as wrapper for `percentage_discount` with predefined discounts per `LoyaltyProgram`
# Backend\Python\Good practices\Pythonic_Patterns\011_Function_builder.md

#### Function builder

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2150393709/posts/2160000936

##### Builder pattern

```python
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Callable


class LoyaltyProgram(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3


DiscountFunction = Callable[[int], int]


def percentage_discount(price: int, percentage: float) -> int:
    return int(price * percentage)


def fixed_discount(_: int, fixed: int) -> int:
    return fixed


def loyalty_program_convertor(program: LoyaltyProgram) -> DiscountFunction:
    loyalty_percentages = {
        LoyaltyProgram.BRONZE: 0.1,
        LoyaltyProgram.SILVER: 0.15,
        LoyaltyProgram.GOLD: 0.2,
    }
    return partial(percentage_discount, percentage=loyalty_percentages[program])


@dataclass
class Order:
    price: int
    quantity: int
    discount: DiscountFunction

    def compute_total(self) -> int:
        discount = self.discount(self.price * self.quantity)
        return self.price * self.quantity - discount


def main() -> None:
    loyalty = LoyaltyProgram.SILVER
    loyalty_discount = loyalty_program_convertor(loyalty)
    order = Order(price=100_00, quantity=2, discount=loyalty_discount)
    print(order)
    print(f"Total: ${order.compute_total()/100:.2f}")
```
* `loyalty_program_convertor` as function builder function, that returns discount function for Order class
# Backend\Python\Iterables\001_Iterable.md

### Iterable
Kompozyt zdolny do zwracania swoich elementów w pętli for. Są to np. typy sekwencyjne (listy, krotki, stringi), dict, set, file, itp.
```python
class Iterable:
	def __getitem__(self, key):
		(...)
	def __len__(self):
		return (...)

iterable[123]
iterable['foobar']
```
Dla bardziej skomplikowanej logiki iterowania definiuje się metodę **\_\_iter\_\_**
```python
class Iterable:
	(...)
	def __iter__(self):
		return Iterator(...)

### Wywołanie metody __iter__ obiektu Iterable w celu utworzenia iteratora 
iterator = iter(iterable)
```
# Backend\Python\Iterables\002_Iterator.md

### Iterator
Hermetyzuje strategię sekwencyjnego dostępu do elementów kompozytu, bez względu na rzeczywistą ich organizację. Jego zadanie polega na dostarczaniu kolejnych elementów według ustalonego wzorca.
```python
class Iterator:
	def __next__(self):
		return (...)
	def __iter__(self):
		return self # Obiekt iteratora musi mieć zdefiniowaną metodę __iter__, gdzie zwraca samego siebie

iterator = iter(iterable)

### Wywoływanie kolejnych elementów.
element_1 = next(iterator)
element_2 = next(iterator)
```
Gdy nie ma już obiektów do pobrania, przy kolejnej próbie użycia funkcji **next** wystąpi wyjątek *StopIteration*.

Iterator można utworzyć również z "wartownikiem", będącym wartością przerywającą iterację.

```python
### iterator = iter(callable, sentinel)

def function():
	return random.randrange(10)

list(iter(function, 5))
```
# Backend\Python\Iterables\003_Generators.md

### Generatory
```python
def get_next_even():                   # definicja generatora wygląda jak definicja zwykłej funkcji
    for n in range(2,20,2):            # range tworzący zakres od 2 do 20, przesuwając się o 2
        yield n                        # słowo yield informuje interpreter, że ta funkcja będzie generatorem

z = get_next_even()                    # tworzenie obiektu generatora

for i in range(10):                    # pętla for wykonująca się 10 razy
    print(next(z))                     # która za kazdym razem drukuje kolejną wartość zwróconą z obiektu genratora z

y = ('a' * n for n in range(5))        # generator expression - wyrażenie generatorowe
                                       # tworzy generator, który będzie zwracał kolejne wielokrotności stringa 'a'
                                       # zakresie od 0 do 4

for i in range(5):                     # wypisanie kolejnych wartości zwróconych przez obiekt genratora y
    print(next(y))
```

Generator to inny rodzaj iteratora. Używając kluczowego słowa **yield** wyciągamy następną wartość dostarczoną przez generator, po czym zapamiętuje on swój stan aż do kolejnego jego wywołania przez pętlę lub funkcję **next**. Jednym z benefitów generatorów może być tzw. separation of concernes, czyli oddzielenie iteracji od logiki przetwarzania pojedynczego elementu. 

```python
def create_generator(start, stop, step):
	x = start
	while x < stop:
		yield x # Słowo kluczowe przekształcające funkcję w generator
		x += step
		
generator = create_generator(0, 10, 2.5)
### Logika zawarta w funkcji generatora wykonuje się dopiero po zastosowaniu funkcji next() lub w czasie iteracji w pętli

### next(generator)
for value in generator:
	print(value)
```
Generator można również zdefiniować używając tzw. Generator Comprehensions.
```python
(x**2 for x in range(10) if x % 2 == 0)
```
Jako praktyczny przykład zastosowania generatora można podać operacje na plikach, gdzie logika przetwarzania poszczególnych wierszy, jest oddzielona od in filtrowania, za które odpowiada generator.
```python
def exclude_comments(fp):
	for line in fp:
		if not line.startswith('#'):
			yield line

with open('filename') as fp:
	for line in exclude_comments(fp):
		process(line)
```
Generatory wykorzystują tzw. leniwą ewaluację, która pozwala strumieniowo przetwarzać duże ilości danych bez konieczności wczytywania ich w całości do pamięci.
# Backend\Python\Iterables\004_Infinite_iterators.md

### Iteratory nieskończone
```python 
from itertools import *

### Kolejne wartości liczbowe
for i in count(10, 1):
	print(i)

### 10
### 11
### 12
### ...

### Kolejne wartości z listy podawane cyklicznie
for i in cycle(['spring', 'summer', 'fall', 'winter']):
	print(i)

### Powtórzenie tej samej wartości podaną ilość razy, lub w nieskończoność
for i in repeat('hello', 3):
	print(i)
```

# Backend\Python\Iterables\005_Combinatoric_iterators.md

### Iteratory kombinatoryczne
#### product
Iloczyn kartezjański dwóch lub więcej zbiorów (wszystkie możliwe kombinacje wartości).
```python 
from itertools import *


colors = {'black', 'white'}
sizes = {'S', 'M', 'L', 'XL'}
materials = {'cotton', 'polyester', 'lycra'}

for color, size, material in product(colors, sizes, materials):
	print(color, size, material)
	# black S lycra
	# black S cotton
	# ...
	# black M lycra
	# ...
	# white S lycra
	...

### Kombinacja kilku wartości z tego samego zakresu
list(product(range(10), repeat=4))
### [(0, 0, 0, 0),
### (0, 0, 0, 1),
...
### (9, 9, 9, 9)]
```
#### permutations
Możliwe permutacje dla podanego zbioru (możliwe kolejności obiektów w zbiorze).
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in permutations(horses):
	for i, horse in enumerate(outcome, 1):
		print(i, horse)
	print()

### 1 Duke
### 2 Coco
### 3 Star
### 4 Dolly
### 5 Gypsy
### 
### 1 Duke
### 2 Coco
...
```
Możliwe jest również uzyskanie n-elementowych wariacji bez powtórzeń - tutaj w celu uzyskania pierwszych trzech miejsc na podium.
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in permutations(horses, 3):
	for i, horse in enumerate(outcome, 1):
		print(i, horse)
	print()
### 1 Duke
### 2 Coco
### 3 Star
...
```
#### combinations
n-elementowe unikalne podzbiory bez względu na kolejność elementów.
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in combinations(horses, 3):
	print(outcome)
### 1 Duke
### 2 Coco
### 3 Star
...
```
# Backend\Python\Iterables\006_Other_iterators.md

### Iteratory pozostałe
#### chain
Pozwala na iterowanie po kilku sekwencjach na raz. Po wyczerpaniu elementów w sekwencji chain przechodzi do pobierania elementów z kolejnej z nich.

```python 
from itertools import *

a = [1, 2, 3]
b = ['lorem', 'ipsum']
c = list('abcd')

for x in chain(a, b, c):
	print(x)
```
#### zip
Wbudowana funcja, pozwalająca na iterowanie po kilku listach jednocześnie. Ilość wynikowych elementów determinuje długość najkrótszej z sekwencji.
```python 
from itertools import *

a = [1, 2, 3]
b = ['lorem', 'ipsum']
c = list('abcd')

for x in zip(a, b, c):
	print(x)

### (1, 'lorem', 'a')
### (2, 'ipsum', 'b')
```
Sekwencje tak utworzonych tupli można też odpakować przy użyciu zip.
```python 
from itertools import *

zipped = [(1, 'a'), (2, 'b')]
x, y = zip(*zipped)
print(x)
print(y)
### (1, 2)
### ('a', 'b')
```
#### groupby
Pozwala na grupowanie danych po wskazanym kluczu
```python 
from itertools import *

expenses = [
	(500, 'ZUS', 'firma'),
	(100, 'księgowa', 'firma'),
	(400, 'OC', 'samochód'),
	(60, 'kino', 'rozrywka'),
	(200, 'paliwo', 'samochód'),
	(700, 'drukarka', 'firma'),
]

category = lambda x: x[-1]

for key, values in groupby(sorted(expenses, key=category), key=category):
	print(key, list(values))

### firma [(500, 'ZUS', 'firma'), ...]
### rozrywka [...]
### samochód [...]
```
#### islice
Pozwala na uzyskanie wycinka z iteratora.
```python 
from itertools import *

it = range(int(1e6))
### Wycinek 10 pierwszych elementów z iteratora it zawierającego milion elementów
list(islice(it, 10)
```
#### Inne metody
* combinations_with_replacement
* accumulate
* count
* cycle
* chain
* compress
* dropwhile
* filterfalse
* product
* repeat
* starmap
* takewhile
* tee
* zip_longest
# Backend\Python\Logging\001_Logging_basics.md

### Logging basics

Sources: 
* https://www.samyakinfo.tech/blog/logging-in-python
* https://realpython.com/python-logging/

Logging is the process of recording information about the execution of a program. This information, known as log messages, includes details about the application's state, error messages, warnings, and other relevant data.

Logging is essential for several reasons:

`Debugging`: Logs help developers identify and fix issues by providing a trail of execution flow and variable values.

`Monitoring`: Logs enable monitoring of application behavior in real-time, helping detect performance bottlenecks and unexpected behavior.

`Auditing and compliance`: For applications handling sensitive information, logging can be essential for auditing user actions and ensuring compliance with regulations.

```python
import logging

### Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

### Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```
# Backend\Python\Logging\002_Log_levels.md

### Log levels

Sources: 
* https://www.samyakinfo.tech/blog/logging-in-python
* https://realpython.com/python-logging/

`DEBUG`: The lowest log level, used for detailed information during development and debugging. Typically not used in a production environment.

`INFO`: General information about the application's execution. It is used to confirm that things are working as expected.

`WARNING`: Indicates a potential issue or something that might lead to an error in the future. The application can still continue to run.

`ERROR`: Indicates a more severe issue that prevents a specific operation from completing successfully.

`CRITICAL`: The highest log level, indicating a critical error that may lead to the termination of the application.
# Backend\Python\Logging\003_Log_handlers.md

### Log handlers

Sources: 
* https://www.samyakinfo.tech/blog/logging-in-python
* https://realpython.com/python-logging/

Log handlers in Python's logging module determine where log messages should go once they are created. Handlers are responsible for routing log messages to specific destinations, such as the console, files, email, or external services. In this part, we'll explore the concept of log handlers and how to use them effectively.

#### StreamHandler
Directs log messages to the console(stream):

```python
import logging

### Configure logging
logging.basicConfig(level=logging.DEBUG)

### Create a StreamHandler and set its log level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

### Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

### Create a logger and add the console handler
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

### Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```
In this example, we create a StreamHandler, set its log level to DEBUG, create a formatter to customize the log message format, and attach the formatter to the handler. Finally, we add the handler to the logger.

#### FileHandler
Directs log messages to a file:
```python
import logging

### Configure logging
logging.basicConfig(level=logging.DEBUG)

### Create a FileHandler and set its log level to DEBUG
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

### Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

### Create a logger and add the file handler
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

### Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```
In this example, we create a FileHandler, set its log level, create a formatter, and attach it to the handler. The log messages will be written to a file named app.log.

#### RotatingFileHandler
Similar to FileHandler, but it rotates log files based on size and keeps a specified number of backup files.

```python
rotating_file_handler = logging.RotatingFileHandler("logfile.log", maxBytes=1024, backupCount=3)
logging.getLogger().addHandler(rotating_file_handler)
```
#### SMTPHandler

Sends log messages via email.
```python
smtp_handler = logging.handlers.SMTPHandler(mailhost=("smtp.example.com", 587),
                                            fromaddr="sender@example.com",
                                            toaddrs=["recipient@example.com"],
                                            subject="Error in your application")
logging.getLogger().addHandler(smtp_handler)
```
# Backend\Python\Logging\004_Log_formatters.md

### Log Formatters

Sources: 
* https://www.samyakinfo.tech/blog/logging-in-python
* https://realpython.com/python-logging/

A log formatter is an object responsible for specifying the layout of log records. It determines how the information within a log message should be presented. Python's logging module provides a Formatter class that allows developers to create custom formatting rules.

#### Base Formatter

```python
import logging

### Configure logging
logging.basicConfig(level=logging.DEBUG)

### Create a StreamHandler and set its log level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

### Create a formatter with a custom format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

### Create a logger and add the console handler
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

### Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

In this example, the Formatter class is used to create a formatter with a specific format string. The format string contains placeholders enclosed in %() that represent various attributes such as asctime, name, levelname, and message.

#### Custom Formatter

```python
import logging

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_message = f"{record.levelname} - {record.name} - {record.message}"
        if record.exc_info:
            log_message += '\n' + self.formatException(record.exc_info)
        return log_message

### Configure logging
logging.basicConfig(level=logging.DEBUG)

### Create a StreamHandler and set its log level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

### Create an instance of the custom formatter
custom_formatter = CustomFormatter()

### Set the formatter for the console handler
console_handler.setFormatter(custom_formatter)

### Create a logger and add the console handler
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

### Log messages
logger.debug("This is a debug message")
logger.error("An error occurred", exc_info=True)

```
# Backend\Python\Logging\005_Other_options.md

### Other options

Source: https://realpython.com/python-logging

#### Date format

```python
>>> import logging
>>> logging.basicConfig(
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> logging.error("Something went wrong!")
2024-07-22 09:26 - ERROR - Something went wrong!
```

#### Logging to file

```python
>>> import logging
>>> logging.basicConfig(
...     filename="app.log",
...     encoding="utf-8",
...     filemode="a",
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> logging.warning("Save me!")
```

#### Displaying Variable Data

```python
>>> import logging
>>> logging.basicConfig(
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
...     level=logging.DEBUG,
... )

>>> name = "Samara"
>>> logging.debug(f"{name=}")
2024-07-22 14:49 - DEBUG - name='Samara'
```

F-strings are eagerly evaluated. That means that they are interpolated even if the log message is never handled. If you’re interpolating a lot of lower level log messages, you should consider using the modulo operator (%) for interpolation instead of f-strings. This style is supported by logging natively, such that you can write code like the following:

```python
>>> import logging
>>> logging.basicConfig(
...     format="%(asctime)s - %(levelname)s - %(message)s",
...     style="%",
...     datefmt="%Y-%m-%d %H:%M",
...     level=logging.DEBUG,
... )

>>> name = "Samara"
>>> logging.debug("name=%s", name)
2024-07-22 14:51 - DEBUG - name=Samara
```

#### Capturing Stack Traces

```python
>>> import logging
>>> logging.basicConfig(
...     filename="app.log",
...     encoding="utf-8",
...     filemode="a",
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> donuts = 5
>>> guests = 0
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.error("DonutCalculationError", exc_info=True)
...
```

```text
2024-07-22 15:04 - ERROR - DonutCalculationError
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

```python
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.exception("DonutCalculationError")
...
```
Calling logging.exception() is like calling logging.error(exc_info=True). Since the logging.exception() function always dumps exception information, you should only call logging.exception() from an exception handler.

#### Filtering Logs

There are three approaches to creating filters for logging. You can create a:

* Subclass of logging.Filter() and overwrite the .filter() method
* Class that contains a .filter() method
* Callable that resembles a .filter() method

```python
>>> import logging
>>> def show_only_debug(record):
...     return record.levelname == "DEBUG"
...

>>> logger = logging.getLogger(__name__)
>>> logger.setLevel("DEBUG")
>>> formatter = logging.Formatter("{levelname} - {message}", style="{")

>>> console_handler = logging.StreamHandler()
>>> console_handler.setLevel("DEBUG")
>>> console_handler.setFormatter(formatter)
>>> console_handler.addFilter(show_only_debug)
>>> logger.addHandler(console_handler)

>>> file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
>>> file_handler.setLevel("WARNING")
>>> file_handler.setFormatter(formatter)
>>> logger.addHandler(file_handler)

>>> logger.debug("Just checking in!")
DEBUG - Just checking in!

>>> logger.warning("Stay curious!")
>>> logger.error("Stay put!")
```
# Backend\Python\Memory\001_tracemalloc.md

### tracemalloc

Sources: 
* https://tech.buzzfeed.com/finding-and-fixing-memory-leaks-in-python-413ce4266e7d
* https://www.fugue.co/blog/diagnosing-and-fixing-memory-leaks-in-python.html

#### Basics
In the case of memory a well-behaved service will use memory and free memory. It performs like this chart reporting on the memory used over a three-month period.

![](_images/001_tracemalloc_good.png)

A microservice that leaks memory over time will exhibit a saw-tooth behavior as memory increases until some point (for example, maximum memory available) where the service is shut down, freeing all the memory and then restarted.

![](_images/001_tracemalloc_bad.png)

If a code review does not turn up any viable suspects, then it is time to turn to tools for tracking down memory leaks. The first tool should provide a way to chart memory usage over time. At BuzzFeed we use DataDog to monitor microservices performance. Leaks may accumulate slowly over time, several bytes at a time. In this case it is necessary to chart the memory growth to see the trend.

The other tool, **tracemalloc**, is part of the Python system library. Essentially **tracemalloc** is used to take snapshots of the Python memory. To begin using tracemalloc first call `tracemalloc.start()` to initialize tracemalloc, then take a snapshot using
```python
snapshot=tracemalloc.take_snapshot()
```
tracemalloc can show a sorted list of the top allocations in the snapshot using the statistics() method on a snapshot. In this snippet the top five allocations grouped by source filename are logged.
```python
for i, stat in enumerate(snapshot.statistics(‘filename’)[:5], 1):
    logging.info(“top_current”,i=i, stat=str(stat))
```
The output will look similar to this:
![](_images/001_tracemalloc_01.png)
This shows the size of the memory allocation, the number of objects allocated and the average size each on a per module basis.

#### Snapshots comparison

We take a snapshot at the start of our program and implement a callback that runs every few minutes to take a snapshot of the memory. Comparing two snapshots shows changes with memory allocation. We compare each snapshot to the one taken at the start. By observing any allocation that is increasing over time we may capture an object that is leaking memory. The method compare_to() is called on snapshots to compare it with another snapshot. The 'filename' parameter is used to group all allocations by module. This helps to narrow a search to a module that is leaking memory.

```python
current = tracemalloc.take_snapshot()
stats = current.compare_to(start, ‘filename’)
for i, stat in enumerate(stats[:5], 1):
    logging.info(“since_start”, i=i, stat=str(stat))
```

The output will look similar to this:

![](_images/001_tracemalloc_02.png)

This shows the size and the number of objects and a comparison of each and the average allocation size on a per module basis.

#### Leaking code detection
Once a suspect module is identified, it may be possible to find the exact line of code responsible for a memory allocation. tracemalloc provides a way to view a stack trace for any memory allocation. As with a Python exception traceback, it shows the line and module where an allocation occurred and all the calls that came before.
```python
traces = current.statistics('traceback')
for stat in traces[1]:
    logging.info('traceback', memory_blocks=stat.count, size_kB=stat.size / 1024)
    for line in stat.traceback.format():
        logging.info(info)
```
![](_images/001_tracemalloc_03.png)
Reading bottom to top, this shows a trace to a line in the socket module where a memory allocation took place. With this information it may be possible to finally isolate the cause of the memory leak.

#### The Search for Memory Leak
# Backend\Python\Metaprogramming\001_Decorators.md

### Dekoratory
Funkcja, przyjmująca jako argument funkcję i zwracająca funkcję. 
```python
def password():
	return 'top_s3cret'

def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

encrypted_password = encrypted(password)
encrypted_password()
```
Powyższy zapis można skrócić do następującego:
```python
def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

@encrypted
def password():
	return 'top_s3cret'

password()
```
Jednym z głównych celów zastosowania dekoratorów jest memoizacja, czyli cache'owania wyników funkcji w celu przyspieszenia obliczeń. Poniżej przykład zastosowania dekoratora cache'ującego wyniki rekurencyjnych wyników wywołań wyliczających składniki ciągu Fibonacciego. 
```python
### import functools
def cache(function):
	history = {}
	def wrapper(n):
		if n not in history:
			history[n] = function(n)
		return history[n]
	return wrapper
	
### @functools.lru_cache(maxsize=128)
@cache
def fib(n):
	return 1 if n < 2 else fib(n-2) + fin(n-1)
```
Dekoratory mogą też przyjmować więcej parametrów niż samą dekorowaną funkcję, ale wymaga to dodatkowego poziomu zagnieżdżenia.
```python
import functools

def ignore(ExceptionClass):
	def decorator(function):
		@functools.wraps(function) # pozwala na przekazanie metadanych (np. __name__) funkcji w argumencie do dekorowanej funkcji
		def wrapper(*args, **kwargs):
			try:
				return function(*args, **kwargs)
			except ExceptionClass as ex:
				pass
		return wrapper
	return decorator

@ignore(ZeroDivisionError)
def divide(a, b):
	return a / b
```
# Backend\Python\Metaprogramming\002_Context_managers.md

### Menedżer kontekstu
Obiekt implementujący interfejs składający się z dwóch magicznych metod - \_\_enter__ oraz \_\_exit__, które umożliwiają jego użycie w konstrukcji with. Menedżer kontekstu przydaje się w takim razie do zarządzania stanem, który musi zostać najpierw zainicjowany, a następnie uwolniony, żeby nie dopuścić do wycieków pamięci. Menedżer kontekstu można zdefiniować klasowo albo funkcyjnie.
```python
from time import time

class MockedTime:
	def __enter__(self):
		# tymczasowe nadpisanie funkcji time
		global time
		self._time = time
		time = lambda: 42
	
	def __exit__(self, exception_class, exception, traceback):
		# powrót do domyślnej funkcji time
		global time
		time = self._time

with MockedTime():
	print(time())
print(time())
```
```python
from time import time, sleep

class Timed:
	def __enter__(self):
		self.t1 = time()
		return self # pozwala na przypisanie menedżera do zmiennej poprzez słówo "as" w konstukcji "with"
	
	def __exit__(self, *args):
		self.t2 = time()
	
	@property
	def delta(self):
		return self.t2 - self.t1

with Timed() as timed:
	sleep(0.5)

print(timed.delta)
```
Do utworzenia menedżera kontekstu jako funkcji służy biblioteka contextlib.
```python
from contextlib import contextmanager

@contextmanager
def logging():
	print('__enter__')
	try:
		yield
	finally:
		print('__exit__')

with logging() as value:
	print('The value is:', value)
```
Instrukcja yield dzieli zawiesza działanie funkcji i dzieli ją na dwie części. Pierwsza część odpowiada instrukcji \_\_enter__, w której dokonuje się inicjalizacji. Druga część (za yield) odpowiada za to instukcji \_\_exit__. Konieczne jest opakowanie słówa kluczowego yield blokiem try/finally, ponieważ w innym razie, w przypadku wystąpienia wyjątku nie doszłoby do "zamknięcia" menedżera kontekstu.

# Backend\Python\Metaprogramming\003_Descriptior.md

### Deskryptor
Można go sobie wyobrazić jako property wielokrotnego użytku, które może być wykorzystywane w wielu klasach. Zgodnie z definicją, jest to klasa definiująca jedną z trzech magicznych metod: \_\_get__, \_\_set__, \_\_delete__. Występują szczególne przypadki: 
* data descriptor - definiuje wszystkie trzy metody
* non data descriptor - definiuje tylko metodę \_\_get__. Pozwalają na leniwą inicjalizację atrybutów w klasie

Pożej przykład zastosowania domknięcia wykorzystującego dekorator property do przypisania niezmiennych atrybutów w klasie.
```python
### Zwrócenie wartości atrybutu _attr przy próbie wyciągnięcia atrybutu poprzez Class.attr
def read_only(name):
	@property
	def getter(self):
		return getattr(self, '_' + name)
	return getter

class Person:
	name = read_only('name')
	married = read_only('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
Ten sam problem można rozwiązać przy użyciu deskryptora:
```python
class ReadOnly:
	def __init__(self, name)
		self.name = name
	
	def __get__(self, obj, cls):
		if obj is None:
			return self
		return getattr(obj, '_' + self.name)
	
	def __set__(self, obj, value):
		raise AttributeError

class Person:
	name = ReadOnly('name')
	married = ReadOnly('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
# Backend\Python\Metaprogramming\004_new_magic_method.md

###  \_\_new__
Metoda magiczna wywoływana przed \_\_init__. Jest to metoda klasowa zwracająca nowy obiekt klasy. Poniżej przykład definicji Singletona.
```python
class Singleton:
	instance = None
	def __new__(cls):
		if Singleton.instance is None:
			Singleton.instance = super().__new__(cls)
		return Singleton.instance

a = Singleton()
b = Singleton()

a is b, id(a) == id(b) # (True, True), obie zmienne wskazują na tę samą instancję obiektu
```
# Backend\Python\Metaprogramming\005_Metaclasses.md

### Metaklasy
Najprostszym przykładem metaklasy jest type - jest on metaklasą dla wszystkich podstawowych (i nie tylko) typów w Pythonie np. int, float itp. Używając type można także zdefiniować nową klasę. Poniżej przykład zdefiniowania metaklasy przy użyciu funkcji.
```python
def n_tuple(name, bases, attrs, n):
	def __new__(cls, *args):
		if len(args) != n:
			raise TypeError(f'expected {n} but got {len(args)} arguments')
		return tuple(args)
	return type(f'Tuple {n}', (tuple,), {'__new__': __new__})

class Point(metaclass=n_tuple, n=2):
	pass

Point(1, 2)
```
Metaklasę można również zdefiniować przy użyciu klasy.
```python
class Meta(type):
	def __new__(cls, name, bases, dct):
		x = super().__new__(cls, name, bases, dct)
		x.attr = 100
		return x

class Foo(metaclass=Meta):
	pass

Foo.attr # 100
```
# Backend\Python\Metaprogramming\006_Dataclass.md

### Dataclass
Chcąc uniknąć żmudnego definiowania klas można zastosować mechanizm dataclass. W wyniku takiego zabiegu można zastąpić taką typową klasę:
```python
class Person:
	def __init__(self, name, age, married=False):
		self.name = name
		self.age = age
		self.married = married
```
Taką klasą:
```python
def dataclass(cls):
	def __init__(self, *args, **kwargs):
		# Zapisanie w kwargs argumentów przekazanych przez args zmapowanych przy użyciu cls.__annotations__
		kwargs.update(zip(cls.__annotations__, args))
		# Zapisanie zaktualizowanych kwargs w słowniku obiektu
		self.__dict__.update(kwargs)
	cls.__init__ = __init__
	return cls


@dataclass
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
Od Pythona 3.7. dostępny jest bardziej rozbudowany dekorator spełniający tę samą funkcję, dlatego finalnie taka klasa wyglądałaby tak:
```python
from dataclasses import dataclass

@dataclass
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
Domyślnie klasy udekorowane przez @dataclass są mutowalne, natomiast w celu "zamrożenia" ich wartości stosuje się następujący zapis:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```

# Backend\Python\Object_oriented_programming\001_Objects_copying.md

### Kopiowanie obiektów
Kopiowanie obiektów może odbywać się w sposób płytki i głęboki. W przypadku kopiowania płytkiego mutowalne elementy nie są rzeczywistą kopią pierwotnych elementów, ale kopią referencji do tych obiektów w pamięci
```python
import copy

x = [1, [2, 3]]
### shallow copy - płytkie kopiowanie
### y = x[:]
### y = list(x)
y = copy.copy(x)

y.append(5)
### x = [1, [2,3]]
### y = [1, [2,3], 5]

y[1].append(5)
### Jako, że lista jest mutowalna, to po dodaniu do niej elementu w jednej z list, element ten jest widoczny w obu kopiach listy
### x = [1, [2, 3, 4]]
### x = [1, [2, 3, 4], 5] 
```
Rozwiązaniem powyższego problemu może być użycie deepcopy, które rekurencyjnie kopiuje kolejne elementy z drzewa obiektu (nie ich referencje, jak w przypadku mutowalnych obiektów przy płytkim kopiowaniu).

```python
import copy

x = [1, [2, 3]]
### deep copy - głębokie kopiowanie
y = copy.deepcopy(x)

y[1].append(5)
### x = [1, [2, 3]]
### x = [1, [2, 3, 4]] 
```
# Backend\Python\Object_oriented_programming\002_Abstract_classes.md

### Abstract Classes

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535822/posts/2158612840

Abstract classes lets to write base model / sketch for other functions that will share same interfaces.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import math

class Vehicle(ABC):
    @abstractmethod
    def reserve(self, start_date: datetime, days: int):
        """A vehicle can be reserved for renting"""

    @abstractmethod
    def renew_license(self, new_license_date: datetime):
        """Renews the license of a vehicle."""

@dataclass
class Car(Vehicle):
    model: str
    reserved: bool = False

    def reserve(self, start_date: datetime, days: int):
        self.reserved = True
        print(f"Reserving car {self.model} for {days} days at date {start_date}.")

    def renew_license(self, new_license_date: datetime):
        print(f"Renewing license of car {self.model} to {new_license_date}.")


@dataclass
class Truck(Vehicle):
    model: str
    reserved: bool = False
    reserved_trailer: bool = False

    def reserve(self, start_date: datetime, days: int):
        months = math.ceil(days / 30)
        self.reserved = True
        self.reserved_trailer = True
        print(
            f"Reserving truck {self.model} for {months} month(s) at date {start_date}, including a trailer."
        )
```
# Backend\Python\Object_oriented_programming\003_Functions_overloading.md

### Przeciążanie funkcji
Python nie obsługuje przeciążania funkcji i metod, ale można za to dostosować działanie funkcji w zależności od przyjętych przez nią argumentów. Najprościej zrobić to przez użycie isinstance, ale jest to antywzorzec. Zamiast tego można wykorzystać metodę singledispatch.
```python
from functools import singledispatch

### Zdefiniowanie wzorca funkcji
@singledispatch
def pretty_print(x):
	print(x)

### Zarejestrowanie specjalnego działania funkcji po podaniu jej listy oraz tupli jako argumentu
@pretty_print.register(list)
@pretty_print.register(tuple)
def _(items):
	for i, value in enumerate(items):
		print(f'[{i}] = {value}')
```

Powyższe rozwiązanie nie zadziała dla metod w klasie oraz nie obsługuje więcej niż jednego argumentu. Aby rozwiązać ten drugi problem można skorzystać z zewnętrznej biblioteki multipledispatch.

```python
from multipledispatch import dispatch

@dispatch(int, int)
def add(x, y):
	return x + y

@dispatch(object, object)
def add(x, y):
	return f'{x} + {y}'
```
# Backend\Python\Object_oriented_programming\004_Operators_overloading.md

### Przeciążanie operatorów
Przykład przeciążania operatora dodawania i dodawania prawostronnego klasy namedtuple.

```python
from collections import namedtuple

class Vector(namedtuple('Vector', 'x y')):
	def __add__(self, other):
		if isinstance(other, Vector):
			return Vector(*map(sum, zip(self, other)))
		elif isinstance(other, int):
			return Vector(self.x + other, self.y + other)
	
	def __radd__(self, other):
		return self + other
```

### __repr__ i __str__
Metoda \_\_str__ powinna zwracać reprezentację obiektu do czytania przez ludzi, natomiast metoda \_\_repr__ powinna zawierać zapis (najlepiej kod Pythona) umożliwiający odtworzenie danego obiektu po wklejeniu do funkcji eval.
```python
class Vector:
	def __init__(self, x, y)
		self.x, self.y = x, y
	
	def __str__(self):
		return f'A vector of {self.x}, {self.y}'
	
	def __repr__(self):
		return f'Vector({self.x}, {self.y})'

a = Vector(3, -4)
str(a) # 'A vector of 3, -4'
b = eval(repr(a)) # Nowa instancja wektora Vector(3, -4)
```
# Backend\Python\Object_oriented_programming\005_Class_methods.md

### Metody klasowe
Metoda klasowa to taka, która zawiera odwołanie nie do konkretnej instancji obiektu, ale do samej klasy. Może być wywoływana bez inicjowania obiektu.
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@classmethod
	def monaco_blue(cls):
		return cls(0.2, 0.5, 0.75)
		
	@classmethod
	def exotic_red(cls):
		return cls(1, 0, 0)
	
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))

Color.monaco_blue() # zwraca obiekt z metody klasowej Color(0.2, 0.5, 0.75)
```
# Backend\Python\Object_oriented_programming\006_Static_methods.md

### Metody statyczne
Nie posiadają odniesienia ani do danego obiektu, ani do samej klasy - zachowują się bardziej jak zwykłe funkcje, niż metody. Z optymalizacyjnego punktu widzenia nie są one dobrym rozwiązaniem, ponieważ wiążę się z dodatkowym kosztem ze względu na przeglądanie przez Pythona przestrzeni nazw w trakcie działania programu. Jedynym logicznym zastosowaniem @staticmethod jest ich pogrupowanie pod jedną, wspólną przestrzenią nazw klasy
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@staticmethod
	def blend(color1, color2, alpha=0.5):
		return color1*alpha + color2*(1-alpha)
		
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))
	
	def __mul__(self, scalar):
		return Color(*[x*scalar for x in self])
	
	def __add__(self, other):
		return Color(*[sum(x) for x in zip(self, other)])
```

# Backend\Python\Object_oriented_programming\007_property.md

### @property
Dekorator @property, pozwala na utworzenie właściwości obiektu, do której dostęp można uzyskać przy użyciu kropki, tak samo jak do atrybutów definiowanych w konstruktorze. Właściwości obiektu są jednak możliwe do nadpisania tylko po zdefiniowaniu settera.
```python
class Person:
	def __init__(self, name, married=False):
		self._name = name
		self.married = married
	
	@property
	def name(self):
		return self._name
	
	@property
	def married(self):
		return self._married
	
	@married.setter
	def married(self, value):
		if not(isinstance(value, bool)):
			raise TypeError('married must be bool')
		self._married = value
	
	@married.deleter
	def married(self):
		del self._married
```
# Backend\Python\Object_oriented_programming\008_Protocols.md

### Protocols

> Sources: 
> * https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535822/posts/2158612869
> * https://realpython.com/python-protocol

Instead of abstract classes it's possible to use protocols in Python. They don't rely on inheritance, but they rely on Python typing mechanism (duck typing).

```python
from typing import Protocol
from dataclasses import dataclass
import datetime
import math

### Protocol class with .reserve() method declared
class Vehicle(Protocol):
    def reserve(self, start_date: datetime, days: int):
        ...

### Dataclass with .reserve() method implemented. No need to inherit Vehicle class.
@dataclass
class Car:
    model: str
    reserved: bool = False

    def reserve(self, start_date: datetime, days: int):
        self.reserved = True
        print(f"Reserving car {self.model} for {days} days at date {start_date}.")

    def renew_license(self, new_license_date: datetime):
        print(f"Renewing license of car {self.model} to {new_license_date}.")

### Another class with .reserver() method.
@dataclass
class Truck:
    model: str
    reserved: bool = False
    reserved_trailer: bool = False

    def reserve(self, start_date: datetime, days: int):
        months = math.ceil(days / 30)
        self.reserved = True
        self.reserved_trailer = True
        print(
            f"Reserving truck {self.model} for {months} month(s) at date {start_date}, including a trailer."
        )

### Typing vehicle as Vehicle is fine here, because both Car and Truck have .reserve() methods, so for typing system (duck typing) they are "the same" 
def reserve_now(vehicle: Vehicle):
    vehicle.reserve(datetime.now(), 40)
```

#### Generic protocols
```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class GenericProtocol(Protocol[T]):
    def method(self, arg: T) -> T:
        ...
```
```python
from typing import Protocol, TypeVar

T = TypeVar("T", bound=int | float)

class Adder(Protocol[T]):
    def add(self, x: T, y: T) -> T:
        ...

class IntAdder:
    def add(self, x: int, y: int) -> int:
        return x + y

class FloatAdder:
    def add(self, x: float, y: float) -> float:
        return x + y

def add(adder: Adder) -> None:
    print(adder.add(2, 3))

add(IntAdder())
add(FloatAdder())
```
In this example, you first define a generic type for your protocol. You use the bound argument to state that the generic type can be an int or float object. Then, you have your concrete adders. In this case, you have IntAdder and FloatAdder to sum numbers.

If you’re using Python 3.12, then you can use a simplified syntax:
```python
from typing import Protocol

class Adder(Protocol):
    def add[T: int | float](self, x: T, y: T) -> T:
        ...

### ...
```

#### Class vars
```python
from abc import abstractmethod
from typing import ClassVar, Protocol

class ProtocolMembersDemo(Protocol):
    class_attribute: ClassVar[int]
    instance_attribute: str = ""

    def instance_method(self, arg: int) -> str:
        ...

    @classmethod
    def class_method(cls) -> str:
        ...

    @staticmethod
    def static_method(arg: int) -> str:
        ...

    @property
    def property_name(self) -> str:
        ...

    @property_name.setter
    def property_name(self, value: str) -> None:
        ...

    @abstractmethod
    def abstract_method(self) -> str:
        ...
```

#### Recursive protocols
You can also define recursive protocols, which are protocols that reference themselves in their definition. To reference a protocol, you must provide its name as strings.

```python
from typing import Optional, Protocol

class LinkedListNode(Protocol):
    value: int
    next_node: Optional["LinkedListNode"]

    def __str__(self) -> str:
        return f"{self.value} -> {self.next_node}"
```
To reference a protocol within its definition, you must include its name as a string literal to avoid errors. That’s because you can’t refer to a type that isn’t fully defined yet. While this limitation will change in the future, for now, you can use a future import as an alternative:
```python
from __future__ import annotations
from typing import Optional, Protocol

class LinkedListNode(Protocol):
    value: int
    next_node: Optional[LinkedListNode]

    def __str__(self) -> str:
        return f"{self.value} -> {self.next_node}"
```
#### Predefined protocols
|Class|	Methods|
|-|-|
|Container|	.__contains__()|
|Hashable|	.__hash__()|
|Iterable|	.__iter__()|
|Iterator|	.__next__() and .__iter__()|
|Reversible|	.__reversed__()|
|Generator|	.send(), .throw(), .close(), .__iter__(), and .__next__()|
|Sized|	.__len__()|
|Callable|	.__call__()|
|Collection|	.__contains__(), .__iter__(), and .__len__()|
|Sequence|	.__getitem__(), .__len__(), .__contains__(), .__iter__(), .__reversed__(), .index(), and .count()|
|MutableSequence|	.__getitem__(), .__setitem__(), .__delitem__(), .__len__(), .insert(), .append(), .clear(), .reverse(), .extend(), .pop(), .remove(), and .__iadd__()|
|ByteString|	.__getitem__() and .__len__()|
|Set|	.__contains__(), .__iter__(), .__len__(), .__le__(), .__lt__(), .__eq__(), .__ne__(), .__gt__(), .__ge__(), .__and__(), .__or__(), .__sub__(), .__xor__(), and .isdisjoint()|
|MutableSet|	.__contains__(), .__iter__(), .__len__(), .add(), .discard(), .clear(), .pop(), .remove(), .__ior__(), .__iand__(), .__ixor__(), and .__isub__()|
|Mapping|	.__getitem__(), .__iter__(), .__len__(), .__contains__(), .keys(), .items(), .values(), .get(), .__eq__(), and .__ne__()|
|MutableMapping|	.__getitem__(), .__setitem__(), .__delitem__(), .__iter__(), .__len__(), .pop(), .popitem(), .clear(), .update(), and .setdefault()|
|AsyncIterable|	.__aiter__()|
|AsyncIterator|	.__anext__() and .__aiter__()|
|AsyncGenerator|	.asend(), .athrow(), .aclose(), .__aiter__(), and .__anext__()|
|Buffer|	.__buffer__()|
# Backend\Python\Profiling\001_Profiling.md

### Profiling

Source: https://www.freecodecamp.org/news/python-debugging-handbook/#profiling

Profiling involves analyzing the performance of your code to identify bottlenecks and areas that can be optimized. Python provides built-in tools and external libraries for profiling, helping developers gain insights into their code's execution time and resource usage.

* Identify Performance Issues: Profiling allows you to pinpoint sections of your code that consume the most time and resources, aiding in optimization efforts.
* Optimize Code: Once bottlenecks are identified, developers can focus on optimizing specific functions or code blocks to enhance overall performance.
* Memory Usage Analysis: Profiling tools can also help in analyzing memory consumption, aiding in the detection of memory leaks and inefficient memory usage.

#### cProfile

cProfile is a built-in module that provides a deterministic profiling of Python programs. It records the time each function takes to execute, making it easier to identify performance bottlenecks.

Example:
```python
import cProfile

def example_function():
    # Your code here

if __name__ == "__main__":
    cProfile.run('example_function()')
```
This will output a detailed report of function calls, their execution time, and the percentage of total time spent in each function.

#### profile

profile:
The profile module is similar to cProfile but is implemented in pure Python. It provides a more detailed analysis of function calls and can be used when a more fine-grained profiling is needed.
```python
import profile

def example_function():
    # Your code here

if __name__ == "__main__":
    profile.run('example_function()')
```
Both cProfile and profile produce similar outputs, but the former is generally preferred for its lower overhead.

#### snakeviz

While the built-in modules provide textual reports, visualizing the results can make it easier to understand and analyze. One popular tool for this is snakeviz.

```commandline
pip install snakeviz
```

```python
import cProfile
import snakeviz

def example_function():
    # Your code here

if __name__ == "__main__":
    cProfile.run('example_function()', 'profile_results')
    snakeviz.view('profile_results')
```
This will open a browser window displaying an interactive visualization of the profiling results.
# Backend\Python\Profiling\002_Line_profiling.md

### Line profiling

Source: https://www.freecodecamp.org/news/python-debugging-handbook/#profiling

Line profiling allows you to see how much time is spent on each line of code within a function. The line_profiler module is commonly used for this purpose.

```commandline
pip install line_profiler
```

```python
from line_profiler import LineProfiler

def example_function():
    # Your code here

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler.add_function(example_function)

    profiler.run('example_function()')

    # Display the results
    profiler.print_stats()
```

This will show a detailed report with the time spent on each line within the example_function.
# Backend\Python\Profiling\003_Memory_profiling.md

### Line profiling

Source: https://www.freecodecamp.org/news/python-debugging-handbook/#profiling

Understanding memory usage is crucial for optimizing code. The memory_profiler module helps in profiling memory consumption.

```commandline
pip install memory-profiler
```

```python
from memory_profiler import profile

@profile
def example_function():
    # Your code here

if __name__ == "__main__":
    example_function()
```

When executed, this will display a line-by-line analysis of memory usage during the execution of the example_function

Understanding memory usage is crucial for optimizing code. The memory_profiler module helps in profiling memory consumption.
# Backend\Python\Servers\001_Gunicorn_vs_uvicorn.md

### Gunicorn vs Uvicorn

Source: https://ismatsamadov.medium.com/gunicorn-vs-uvicorn-369635b92809

Imagine you’re hosting a party. You need a capable host (web server) to manage the guests (requests) and ensure a smooth experience.

Gunicorn and Uvicorn are two popular options, but they excel in different ways.

In the world of Python web development, you’ll encounter two terms that might seem interchangeable at first glance: GUVICORN and UVICORN. But these two players serve distinct purposes in running your web applications. Let’s break down their roles and when to use each one, with a touch of fun to make it easier to remember!

#### Gunicorn

* **Built for WSGI applications**: Gunicorn shines when dealing with WSGI frameworks like Django or Flask. It can handle many guests (requests) efficiently, even with limited resources.
* **Synchronous processing**: Gunicorn follows a traditional approach, handling one guest (request) at a time. This works well for most web applications.
* **Mature and reliable**: Gunicorn is a proven solution with a long track record of stability.

**The WSGI Wrapper, a.k.a. The Adapter**

GUVICORN, is like a resourceful engineer. It can take your brave knight, Uvicorn, and equip it with heavier armor. GUVICORN itself is an ASGI to WSGI (Web Server Gateway Interface) adapter. WSGI is an older protocol commonly used by web frameworks like Flask and Django.

**Why Use GUVICORN?**

* Taming Uvicorn for WSGI Servers: GUVICORN allows you to leverage Uvicorn’s ASGI prowess even with WSGI servers like Gunicorn, a popular option for production environments. Gunicorn excels at managing worker processes, ensuring your application can handle heavy traffic.
* Best of Both Worlds: With GUVICORN, you get the asynchronous magic of Uvicorn for development and the battle-tested stability of Gunicorn for production.

#### Uvicorn 

* **Built for ASGI applications**: Uvicorn is designed for modern ASGI frameworks like Starlette or FastAPI. It can leverage asynchronous processing to handle a large influx of guests (requests) simultaneously.
* **Asynchronous processing**: Uvicorn can juggle multiple guests (requests) at once, ideal for real-time features like chat applications or live updates.
* **Built for speed and scalability**: Uvicorn is optimized for performance, making it perfect for high-traffic web applications.

Key Points about Uvicorn:

* Built for ASGI: Uvicorn is the perfect companion for modern web frameworks like FastAPI, which leverage the power of ASGI.
* Development Server: Uvicorn shines during development. It’s lightweight and easy to use, allowing you to quickly test and debug your web application as you code.
* Limited Worker Support: While Uvicorn can spin up multiple worker processes, its capabilities in this area are more basic compared to GUVICORN.

#### Analogy

* **Gunicorn**: Imagine a party host who takes coat checks one by one (synchronous processing). They handle each guest efficiently but can get overwhelmed with a large crowd.
* **Uvicorn**: This host has multiple assistants who tag coats simultaneously (asynchronous processing). This allows them to handle a large number of guests efficiently, especially for high-traffic situations.

#### Examples
* Choosing Gunicorn: If you’re building a traditional Django blog or a data processing API with Flask, Gunicorn is a solid choice.
* Choosing Uvicorn: If you’re creating a real-time chat application with Starlette or a high-performance API with FastAPI, Uvicorn’s asynchronous processing will give you an edge.

#### Building a FastAPI Application with GUVicorn or UVicorn

```python
from fastapi import FastAPI

### Create an instance of the FastAPI class
app = FastAPI()

### Define a route and corresponding handler function
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
```

##### For GUVicorn
```commandline
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

##### For UVicorn
```commandline
uvicorn main:app --host 0.0.0.0 --port 8000
```
# Backend\Python\Setup\001_pyenv.md

### pyenv / pyenv-win
pyenv is tool that simplifies installing and switching between different versions of Python on the same machine. It keeps the system version of Python intact, which is required for some operating systems to run properly, while still making it easy to switch Python versions based on a specific project's requirements.

Installing Python versions:
```
$ pyenv install 3.8.5
$ pyenv install 3.8.6
$ pyenv install 3.9.0
$ pyenv install 3.10.2

$ pyenv versions
* system
  3.8.5
  3.8.6
  3.9.0
  3.10.2
```
Setting particular version as global:
```
$ pyenv global 3.8.6

$ pyenv versions
  system
  3.8.5
* 3.8.6 (set by /Users/michael/.pyenv/version)
  3.9.0
  3.10.2

$ python -V
Python 3.8.6
```

Setting particular version as local (for specific project):
```
$ pyenv local 3.10.2

$ pyenv versions
  system
  3.8.5
  3.8.6
  3.9.0
* 3.10.2 (set by /Users/michael/repos/testdriven/python-environments/.python-version)

$ python -V
Python 3.10.2
```
# Backend\Python\Setup\002_Poetry.md

### Poetry
Dependency management tool for Python. Works well with pyenv.

#### New project
```commandline
$ poetry new sample-project
$ cd sample-project
```
This will create the following files and folders:

```
sample-project
├── README.rst
├── pyproject.toml
├── sample_project
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_sample_project.py
```

#### pyproject.toml
Dependencies are managed inside the pyproject.toml file:
```toml
[tool.poetry]
name = "sample-project"
version = "0.1.0"
description = ""
authors = ["John Doe <john@doe.com>"]

[tool.poetry.dependencies]
python = "^3.10"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```
#### Add new dependency
To add new a dependency, simply run:
```commandline
$ poetry add [--dev] <package name>
```

The --dev flag indicates that the dependency is meant to be used in development mode only. Development dependencies are not installed by default.

For example:

```commandline
$ poetry add flask
```
This downloads and installs Flask from PyPI inside the virtual environment managed by Poetry, adds it along with all sub-dependencies to the poetry.lock file, and automatically adds it (a top-level dependency) to pyproject.toml:

```toml
[tool.poetry.dependencies]
python = "^3.10"
Flask = "^2.0.3"
```
#### Running command in virtual environment
To run a command inside the virtual environment, prefix the command with poetry run. For example, to run tests with pytest:
```commandline
$ poetry run python -m pytest
```
poetry run <command> will run commands inside the virtual environment. It doesn't activate the virtual environment, though.

# Backend\Python\Setup\003_Initing_new_project.md

### Initing new project
Let's take a look on how to manage a Flask project using pyenv and Poetry.

First, create a new directory called "flask_example" and move inside it:

```commandline
$ mkdir flask_example
$ cd flask_example
```

Second, set the Python version for the project with pyenv:

```commandline
$ pyenv local 3.10.2
```

Next, initialize a new Python project with Poetry:

```commandline
$ poetry init

Package name [flask_example]:
Version [0.1.0]:
Description []:
Author [Your name <your@email.com>, n to skip]:
License []:
Compatible Python versions [^3.10]:

Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] no
Do you confirm generation? (yes/no) [yes]
```

Add Flask:

```commandline
$ poetry add flask
```

Last but not least, add pytest as a development dependency:

```commandline
$ poetry add --dev pytest
```

Now that we have a basic environment set up, we can write a test for a single endpoint.

Add a file called test_app.py:

```python
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/health-check/')

    assert response.status_code == 200
```

After that, add a basic Flask app to a new file called app.py:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/health-check/')
def health_check():
    return 'OK'


if __name__ == '__main__':
    app.run()
```

Now, to run the tests, run:

```commandline
$ poetry run python -m pytest
```

And you can run the development server like so:

```commandline
$ poetry run python -m flask run
```

The ```poetry run``` command runs a command inside Poetry's virtual environment.
# Backend\Python\Sorting\001_Base_sorting.md

### Sortowanie
W Pythonie dane można posortować na dwa sposoby używając wbudowanych mechanizmów.
```python 
[2, 1, 3].sort() # sortuje istniejącą listę
sorted([2, 1, 3]) # tworzy posortowaną kopię podanej listy
```
# Backend\Python\Sorting\002_Operator_module.md

### Moduł operator

W celu ułatwienia przekazywania klucza sortowania do metody sorted można posłużyć się modułem operator.

### operator.itemgetter
```python 
from operator import *

people = [
	('Jan', 'Kowalski'),
	('Anna', 'Woźniak'),
	('Anna', 'Nowak')
]

sorted(people, key=itemgetter(0, 1)) # itemgetter wyciąga elementy z kolejno z indeksów 0 i 1 w formie krotki dla każdego z obiektów listy people. Lista jest posortowana najpierw względem pierwszej podanej wartości, a następnie drugiej
```
### operator.attrgetter
```python 
from operator import *
from collections import namedtuple

Person = namedtuple('Person', 'first_name last_name')

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=attrgetter('first_name', 'last_name')) # attrgetter wyciąga atrybuty kolejno 'first_name' i 'last_name' i sortuje listę obiektów na ich podstawie
```
### operator.methodcaller
```python 
from operator import *
from collections import namedtuple

class Person(namedtuple('Person', 'first_name last_name')):
	def get_length(self):
		return len(str(self))

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=methodcaller('get_length')) # methodcaller sortuje listę na podstawie wartości zwróconych przez metodę, której nazwa przekazana jest w argumencie
```
# Backend\Python\Syntax\001_lambda.md

### lambda  
Lambda w Pythonie to funkcja, która może przyjąć każdą liczbę argumentów, ale mieć tylko jedno wyrażenie. Co ważne, jest to funkcja anonimowa, a zatem nie jest powiązana z żadnym identyfikatorem. Pozwala wyeliminować funkcję zainicjowane na potrzeby funkcji wyższego rzędu i przekazać jej parametry.
```python
### lambda argument : wyrażenie
### lambda x:x+2

L = [('Anna',82), ('Robert',33), ('Arthur',40), ('John',56)]
### Funkcja sorted pobiera sekwencję danych do posortowania i klucz, po którym będzie sortować.
### Sekwencją jest lista L, a kluczem lambda, która dla kolejnego elementu listy L (czyli tupli)
### zwraca drugi element danej tupli.
L_sorted = sorted(L, key = lambda x:x[1])
```
# Backend\Python\Syntax\002_map_and_filter.md

### map i filter
```python
names = ['jan kot', 18, 'ANNA KRÓL', 'jÓzef BYK', ['nie', 'wasza','sprawa'], 'ROBERT wąŻ']

### filter(funkcja,sekwencja)
### elementy z listy names przekazywane są do lambdy, która sprawdza czy ich typ to string
### jeśli tak, to element zostaje dodany do listy names_cleaned
names_cleaned = list(filter(lambda x:type(x) is str, names))

### map(funkcja,sekwencja)
### elementy z listy names_cleaned przekazane są do lambdy
### która najpierw zamienia wszystkie litery danego stringa na małe,
### a następnie pierwsza literę każdego słowa zmienia na dużą
### tak zmodyfikowany string zostaje dodany do listy names_corrected
names_corrected = list(map(lambda x: x.lower().title(), names_cleaned))
```
# Backend\Python\Syntax\003_Decorators.md

### Dekoratory
```python
def add_stars(function):     # definicja dekoratora niczym nie różni się od definicji zwykłej funkcji
    def decorated_function():   # wewnątrz dekoratowa tworzymy WEWNĘTRZNĄ funkcję, w której udekorujemy funkcję pobraną jako argument
        print("***")             # dekorowanie funkcji
        function()               # wywołanie funkcji będącej argumentem dekoratora
        print("***")             # dekorowanie funkcji
    return decorated_function    # zwrócenie funkcji WEWNĘTRZNEJ, w której udekorowano funkcję będącą argumentem dekoratora

@add_stars                       # zapis @add_stars BEZPOŚREDNIO nad definicją funkcji f() powoduje, że funkcja f() zostaje udekorowana
def f():                         # definicja funkcji f()
    print("Cześć, jestem f()")
```
# Backend\Python\Syntax\004_List_comprehension.md

### List Ccomprehension
```python
L = [1,2,3,4,5,6]
L1 = [x for x in range(5)]        # elementy z zakresu od 0 do 4
L2 = [x**2 for x in L]            # elementy z listy L podniesione do kwadratu
L3 = [x for x in L if x % 2 == 0] # elementy z listy L, tylko jeśli dany element jest podzielny przez 2
L4 = ['Parzysta' if x%2 == 0 else 'Nieparzysta' for x in range(5)]
                                  # 'Parzysta' lub 'Nieparzysta' w zależności od tego czy kolejny element
                                  # z zakresu 0 do 4 jest podzielny lub nie jest podzielny przez 2
L5 = [(x, x+10) for x in L]       # dwuelementowe tuple, które na indeksie 0 mają kolejny element z listy L
                                  # a na indeksie 1 ten sam element zwiększony o 10
```
### Zagnieżdżone List Comprehension
```python
### 2-D List
matrix = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
  
### Nested List Comprehension to flatten a given 2-D matrix
flatten_matrix = [val for sublist in matrix for val in sublist]

### [val
### for sublist in matrix
### for val in sublist]
```
# Backend\Python\Syntax\005_slots.md

### __slots__

Source: https://medium.com/@apps.merkurev/dont-forget-about-slots-in-python-c397f414c490

#### Base usage

Python’s __slots__ is a simple yet powerful feature that is often overlooked and misunderstood by many. By default, Python stores instance attributes in a dictionary called __dict__ that belongs to the instance itself. This common approach is associated with significant overhead. However, this behavior can be altered by defining a class attribute called __slots__.

When __slots__ is defined, Python uses an alternative storage model for instance attributes: the attributes are stored in a hidden array of references, which consumes significantly less memory than a dictionary. The __slots__ attribute itself is a sequence of the instance attribute names. It must be present at the time of class declaration; adding or modifying it later has no effect.

Attributes listed in __slots__ behave just as if they were listed in __dict__ - there’s no difference. However, __dict__ is no longer used and attempting to access it will result in an error:

```python
import datetime

class Book:
    __slots__ = ('title', 'author', 'isbn', 'pub_date', 'rating')

book = Book()
book.title = 'Learning Python'
book.author = 'Mark Lutz'
book.pub_date = datetime.date(2013, 7, 30)
book.rating = 4.98

print(book.title)  # Learning Python
print(book.rating)  # 4.98

### This will raise AttributeError: 'Book' object has no attribute '__dict__'
print(book.__dict__)
```

So, what are the benefits of using __slots__ over the traditional __dict__? There are three main aspects:

##### I. Faster access to instance attributes
This might be hard to notice in practice, but it is indeed the case.

##### II. Memory savings
This is probably the main argument for using __slots__. We save memory because we are not storing instance attributes in a hash table (__dict__), thus avoiding the additional overhead associated with using a hash table.

```python
from pympler import asizeof

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        
class SlotPoint:
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        
p = [Point(n, n+1) for n in range(1000)]
print(f'Point: {asizeof.asizeof(p)} bytes')  # Point: 216768 bytes

p = [SlotPoint(n, n+1) for n in range(1000)]
print(f'SlotPoint: {asizeof.asizeof(p)} bytes')  # SlotPoint: 112656 bytes
```
In our example, the memory savings were almost twofold. However, the savings will not be as significant if the object has more attributes or if their types are complex. The savings might only amount to a few percent.

##### III. More secure access to instance attributes
__dict__ allows us to define new attributes on the fly and use them. __slots__ restricts us to what is listed in it:

```python
class Book:
    pass

class SlotBook:
    __slots__ = ()

book = Book()
book.title = 'Learning Python'  # no error, a new attribute is created
print(book.title)  # Learning Python

book = SlotBook()
### This will raise AttributeError: 'SlotBook' object has no attribute 'title'
book.title = 'Learning Python'
```

#### Inheriting from class using __slots__
Whether to use __slots__ or not depends on the specific case. It might be beneficial in some cases and problematic in others, especially in more complex scenarios, like when inheriting from a class that has defined __slots__. In this case, the interpreter ignores the inherited __slots__ attribute, and __dict__ reappears in the subclass:
```python
class SlotBook:
    __slots__ = ()

class Book(SlotBook):
    pass

book = Book()
book.title = 'Learning Python'  # no error, a new attribute is created
print(book.title)  # Learning Python
```

# Backend\Python\TDD\001_How_to_test.md

### How to test?

Three guidelines that (hopefully) most developers will agree with that will help you write valuable tests:

1. Tests should tell you the expected behavior of the unit under test. Therefore, it's advisable to keep them short and to the point. The GIVEN, WHEN, THEN structure can help with this:

* GIVEN - what are the initial conditions for the test?
* WHEN - what is occurring that needs to be tested?
* THEN - what is the expected response?

    So you should prepare your environment for testing, execute the behavior, and, at the end, check that output meets expectations.

2. Each piece of behavior should be tested once -- and only once. Testing the same behavior more than once does not mean that your software is more likely to work. Tests need to be maintained too. If you make a small change to your code base and then twenty tests break, how do you know which functionality is broken? When only a single test fails, it's much easier to find the bug.

3. Each test must be independent from other tests. Otherwise, you'll have hard time maintaining and running the test suite.
# Backend\Python\TDD\002_Project_structure.md

### Project structure

```
├── sum
│   ├── __init__.py
│   └── another_sum.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── pytest.ini
    └── test_sum
        ├── __init__.py
        └── test_another_sum.py
```

Keeping your tests together in single package allows you to:

- Reuse pytest configuration across all tests
- Reuse fixtures across all tests
- Simplify the running of tests
# Backend\Python\TDD\003_Test_doctstring.md

### Test docstring

Test docstring may contain details based on GIVEN, WHEN, THEN model. Example:

```python
def test_create_article():
    """
    GIVEN CreateArticleCommand with valid author, title, and content properties
    WHEN the execute method is called
    THEN a new Article must exist in the database with the same attributes
    """
    cmd = CreateArticleCommand(
        author="john@doe.com",
        title="New Article",
        content="Super awesome article"
    )

    article = cmd.execute()

    db_article = Article.get_by_id(article.id)

    assert db_article.id == article.id
    assert db_article.author == article.author
    assert db_article.title == article.title
    assert db_article.content == article.content
```
```python
def test_create_article_already_exists():
    """
    GIVEN CreateArticleCommand with a title of some article in database
    WHEN the execute method is called
    THEN the AlreadyExists exception must be raised
    """

    Article(
        author="jane@doe.com",
        title="New Article",
        content="Super extra awesome article"
    ).save()

    cmd = CreateArticleCommand(
        author="john@doe.com",
        title="New Article",
        content="Super awesome article"
    )

    with pytest.raises(AlreadyExists):
        cmd.execute()
```
# Backend\Python\TDD\004_End_to_end.md

### End-to-end testing
#### Prepare end-to-end test
We have a working API at this point that's fully tested. We can now look at how to write some end-to-end (e2e) tests. Since we have a simple API we can write a single e2e test to cover the following scenario:

1. create a new article
2. list articles
3. get the first article from the list


```python
@pytest.mark.e2e
def test_create_list_get(client):
    requests.post(
        "http://localhost:5000/create-article/",
        json={
            "author": "john@doe.com",
            "title": "New Article",
            "content": "Some extra awesome content"
        }
    )
    response = requests.get(
        "http://localhost:5000/article-list/",
    )

    articles = response.json()

    response = requests.get(
        f"http://localhost:5000/article/{articles[0]['id']}/",
    )

    assert response.status_code == 200
```
#### Register marker
Register a marker called e2e with pytest by adding the following code to pytest.ini:
```ini
[pytest]
markers =
    e2e: marks tests as e2e (deselect with '-m "not e2e"')
```
pytest markers are used to exclude some tests from running or to include selected tests independent of their location.

To run only the e2e tests, run:

```commandline
(venv)$ python -m pytest tests -m 'e2e'
```

To run all tests except e2e:

```commandline
(venv)$ python -m pytest tests -m 'not e2e'
```
e2e tests are more expensive to run and require the app to be up and running, so you probably don't want to run them at all times.
# Backend\Python\Types_and_hints\001_Static_dynamic_stron_week_typing.md

### Static vs. dynamic and strong vs. weak typing

Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535947

#### Static vs dynamic typing

Those types of typings indicates in which moment type information are required.

`Static` - on compilation

`Dynamic` - on runtime

#### Strong vs weak typing

Those types indicate if type of variable may change during code execution depending on usage. 

`Strong` - Types don't change during code execution - Python `print(1 + '1')` will raise an error

`Weak` - Types may change during code execution - JavaScript `console.log(1 + "1")` won't raise an error
# Backend\Python\Types_and_hints\002_Type_hints.md

### Type hints

Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535947/posts/2158623370

#### Base type hints

```python
def add_three(x: int) -> int:
    return x + 3
```

`x: int` -> `x` argument is suggested to be integer, if not no error will be raised, but it informs, that function was created for int arguments.
`-> int` -> function will return `int`

#### Callables

```python
from typing import Callable

IntFunction = Callable[[int], int]

def add_three(x: int) -> int:
    return x + 3

def main():
    my_var: IntFunction = add_three
    print(my_var(5))
```

```Callable[[int], int]``` -> defines type for Callable (function in this case), that takes int as argument (`[int]`) and returns int (second `int` in declaration)

```my_var: IntFunction``` -> typing variable with custom type
# Backend\SQL\001_Create_new_table.md

## Tworzenie nowej tabeli
```sql
CREATE TABLE table (column type, ...);

Example:
CREATE TABLE genres (
	show_id INTEGER, 
	genre TEXT NOT NULL, 
	FOREIGN KEY(show_id) REFERENCES shows(id)
);
```
# Backend\SQL\002_Insert_row.md

## Dodanie wiersza tabeli
```sql
INSERT INTO genres (show_id, genre) VALUES(159, "Comedy");
```

# Backend\SQL\003_Update_row.md

#### Zmiana istniejącej wartości
```sql
UPDATE favorites SET title = "The Office" WHERE title = "Thevoffice";
```
Przy zmianie wartości kluczowa jest klauzula WHERE - bez niej wszystkie rekordy w bazie danych zostaną nadpisane nową wartością pola.

# Backend\SQL\004_Create_index.md

## Tworzenie indeksów
```sql
CREATE INDEX "title_index" ON "shows" ("title");
```
Indeks to struktura danych podobna do B-tree, gdzie dzięki zorganizowaniu węzłów jak na rysunku poniżej nie ma potrzeby wyszukiwać elementów liniowo. 

![tree with root node and four child nodes, each with two or three child nodes](https://cs50.harvard.edu/x/2022/notes/7/b_tree.png)

Computer Science
================

# Computer Science\Algorithms\001_Complexity.md

## Analiza algorytmów
Algorytmy można analizować na przykład na bazie ich złożoności obliczeniowej.
### 1. Czas stały - O(1)
Najbardziej efektywny, wymaga wykonania jednego kroku niezależnie od wielkości danych wejściowych. Przykład: Wyciągnięcie pojedynczego elementu z listy.
### 2. Czas logarytmiczny - O(log n)
Liczba kroków jest proporcjonalna do logarytmu wielkości danych wejściowych, zatem rośnie wolniej od nich. Przykład: algorytm wyszukiwania binarnego.
### 3. Czas liniowy - O(n)
Liczba kroków jest wprost proporcjonalna do ilości danych wejściowych. Przykład: Wyświetlenie każdego elementu listy. 
### 4. Czas logarytmiczno-liniowy - O(n log n)
Liczba kroków jest iloczynem złożoności logarytmicznej i liniowej. Dzieje się tak, gdy np. algorytm wykonuje n razy czynność o złożoności O(log n). Przykład: algorytm merge sort.
### 5. Czas kwadratowy - O(n**2)
Liczba kroków wprost proporcjonalna do kwadratu wielkości danych wejściowych. Przykład: Sortowanie bąbelkowe.
### 6. Czas sześcienny - O(n**3)
Liczba kroków wprost proporcjonalna do sześcianu wielkości danych wejściowych. Przykład: Trzy zagnieżdżone pętle.
### 7. Czas wykładniczy - O(c**n)
Najgorsza możliwa złożoność. Liczba kroków jest równa pewnej stałej podniesionej do potęgi równej wielkości danych wejściowych. Przykład: program odgadujący hasło o długości n metodą brute force (sprawdzanie każdej możliwej kombinacji).

# Computer Science\Algorithms\002_Searching.md

## Wyszukiwanie
### 1. Wyszukiwanie liniowe
Algorytm, który przegląda kolejno wszystkie wartości dostępne w zbiorze danych i porównuje je z poszukiwaną wartością. Wyszukiwanie liniowe stosowane jest na danych nieposortowanych.
```python
def linear_search(a_list, n):
	for i in a_list:
		if i == n:
			return True
	return False
```
### 2. Wyszukiwanie binarne
Algorytm wyszukiwania użyteczny jedynie dla posortowanych danych. Algorytm wyszukuje wskazaną wartość dzieląc analizowany zbiór danych na połowy.
```python
def binary_search(a_list, n):
	first = 0
	last = len(a_list) - 1
	while last >= first:
		mid = (first + last) // 2
		if a_list[mid] == n:
			return True
		else:
			if n < a_list[mid]:
				last = mid - 1
			else:
				first = mid + 1
	return False
```
# Computer Science\Algorithms\003_Sorting.md

## Sortowanie
### 1. Sortowanie bąbelkowe
Algorytm sortowania, który przegląda listę liczb, porównuje każdą liczbę z następną i zamienia je miejscami, jeśli są zapisane w nieodpowiedniej kolejności.
### 2. Sortowanie przez wstawianie
Stabilny algorytm sortowania, w którym dane są porządkowane w sposób przypominający sortowanie talii kart. W trakcie całego procesu zbiór dzieli się na dwie cześci - posortowaną i nieposortowaną. Na samym początku w części posortowanej znajduje się pierwszy element zbioru. Porównujemy pierwszy element listy nieposortowanej z ostatnim elementem listy posortowanej i zamieniamy je miejscami aż do momentu, gdy będą w odpowiedniej kolejności. Powtarzamy ten krok aż do ostatniego elementu listy nieposortowanej.
### 3. Sortowanie przez scalanie
Stabilny algorytm rekurencyjny (typu "dziel i rządź"), który dzieli listę na połowy tak długo, aż uzyska listy o długości jednego elementu, które następnie łączy w odpowiedniej kolejności.
#### Algorytmy typu "Dziel i rządź"
Algorytmy, które rekurencyjnie dzielą problem na dwa lub więcej podproblemów, aż do momentu, gdy będą one na tyle proste, że będzie je można łatwo rozwiązać.
### 4. Timsort
Algorytm wykorzystywany we wbudowanych funkcja Pythona sort i sorted. Stanowi on hybrydowe połączenie sortowania przez scalanie oraz sortowania przez wstawianie.
# Computer Science\Algorithms\004_Euclidean_algorithm.md

## Algorytm Euklidesa
Najefektywniejszy sposób znajdowania wspólnego czynnika. Składa się z następujących kroków:
* Podzielenie liczby x przez y i wyznaczenie reszty z dzielenia,
* Zastąpienie liczby y resztą z dzielenia oraz liczby x liczbą y i ponowne wykonanie dzielenia,
* Poprzedni krok powtarzany jest do momentu otrzymania reszty dzielenia równej 0
* Ostatni dzielnik jest największym wspólnym czynnikiem
# Computer Science\Data structures\001_Array.md

## Tablice
Python jako swoją implementację abstrakcyjnej struktury danych tablicy stosuje listy, wykorzystujące nadmierną alokację (zabezpieczają się większą ilością pamięci niż zajmują przechowywane dane). 
Chcąc wykorzystać "klasyczny" rodzaj tablicy wykorzystywany jest moduł array.
```python
import array

## pierwszy parametr określa typ danych (tutaj float), drugi to lista wartości
arr = array.array('f', (1.0, 1.5, 2.0, 2.5))
``` 
### Zadanie - Przesuwanie zer
Zadanie polega na wyszukaniu w tablicy wszystkich zer i przesunięcie ich na sam koniec bez zmieniania kolejności pozostąłych elementów tablicy. 
```python
def move_zeros(a_list):
	zero_index = 0
	for index, n in enumerate(a_list):
		if n != 0:
			a_list[zero_index] = n
			if zero_index != index:
				a_list[index] = 0
			zero_index += 1
	return a_list

a_list = [8, 0, 3, 0, 12] 
move_zeros(a_list)
print(a_list) #  [8, 3, 12, 0, 0]
```
# Computer Science\Data structures\002_Linked_list.md

## Lista połączona
Implementacja abstrakcyjnego typu danych listy. Pozwala na dodawanie, usuwanie oraz wyszukiwanie elementów. Elementy listy nie są indeksowane, ponieważ komputer nie przechowuje ich w jednym, ciągłym obszarze pamięci. Zamiast tego lista połączona stanowi łańcuch wierzchołków, z których każdy zawiera jakieś dane oraz adres następnego wierzchołka listy.
* Wyszukiwanie elementu na liście połączonej wymaga w najgorszym wypadku przeszukania wszystkich elementów listy  - złożoność O(n).
* Dodawanie i usuwanie elementów jest za to operacją o stałym czasie - złożoność O(1). 
* Konieczność zapisywania wskaźników do kolejnych elementów zużywa zasoby systemowe, przez co listy połączone wymagają więcej pamięci niż tablice.
* Listy połączone nie pozwalają na swobodny dostęp do elementów (odwołanie do dowolnego elementu w stałym czasie).
```python
class Node:
	def __init__(self, data, next=None):
		self.data = data
		self.next = next

class LinkedList:
	def __init__(self):
		self.head = None
	
	def append(self, data):
		if not self.head:
			self.head = Node(data)
			return
		current = self.head
		while current.next:
			current = current.next
		current.next = Node(data)
```
### 1. Lista jednokierunkowa
Typ listy połączonej, w której każdy wierzchołek zawiera tylko jeden wskaźnik - odwołujący się do następnego elementu listy.
#### 2. Lista dwukierunkowa (podwójnie połączona)
Lista połączona, która zawiera dwa wskaźniki: jeden wskazuje na następny wierzchołek, a drugi na poprzedni.
#### 3. deque
Python nie zawiera wbudowanej implementacji list kierunkowych, natomiast udostępnia strukturę danych deque, która wewnętrznie używa takich list.
```python
from collections import deque

d = deque()
d.append('Harry')
d.append('Potter')
```
# Computer Science\Data structures\003_Queue.md

## Kolejki
### 1. Kolejka
Podstawowy rodzaj kolejki, który wykorzystuje schemat FIFO (First in, first out). Działa na wzór kolejki np. na poczcie. Elementy mogą być dodawane na koniec kolejki i zdejmowane z jej początku.
### 2. Stos
Kolejka, stosująca schemat LIFO (Last in, first out). Działa na wzór np. stosu książek. Zawartość stosu może być dodawana lub zdejmowana z tzw. szczytu.
### 3. Kolejka priorytetowa
Często nazywana kopcem binarnym. Elementy kopca są wstawiane wraz z priorytetem w pierwsze wolne miejsce na dole kopca. Zdejmowany jest element o najwyższym, lub najniższym priorytecie.

![Priority Queue Data Structure](https://cdn.programiz.com/sites/tutorial2program/files/insert-1_0.png)

# Computer Science\Test-Driven Development\001_Test-Driven Development.md

## Test-Driven Development

Source: https://testdriven.io/courses/django-rest-framework/tdd-search-filtering/#H-0-test-driven-development

[Test-driven Development](https://testdriven.io/test-driven-development/) (abbreviated TDD) is a methodology in software development where you write a test before a particular piece of code is implemented.

With TDD, you use the following cycle:

RED - write a failing test
GREEN - write the simplest piece of code that will get the test to pass
REFACTOR - improve the code while keeping the test green (passing)
Although confusing and time-consuming at first, once you get a grip on TDD, your development process will be quicker and less prone to bugs.

A straightforward example of TDD would be a function that sums up two numbers.

Start with a test:
```python
def test_sum_two_numbers():
    result = sum_two_numbers(2, 3)

    assert result == 5
```
Run the test to ensure it fails (RED).

After that, you'd write the simplest piece of code that will provide the desired result (GREEN):

```python
def sum_two_numbers(x, y):
    return 5
```

This code accomplishes what we wanted, but it can clearly be improved (REFACTOR):

```python
def sum_two_numbers(x, y):
    return x + y
```  

DevOps
======

# DevOps\Commandline\001_pwd.md

## pwd
Komenda zwracająca katalog, w którym obecnie się znajdujemy (rozwinięcie skrótu - Print Working Directory).

```commandline 
pwd
``` 
# DevOps\Commandline\002_ls.md

## ls
Komenda zwracająca wylistowaną zawartość bieżącego katalogu
```commandline 
ls       // simple list
ls -a    // list including hidden files
ls -l    // list with details (file sizes, modification dates, etc.)
ls -al   // list with hidden files and details (file sizes, modification dates, etc.)
``` 
# DevOps\Commandline\003_mkdir.md

## mkdir
Komenda tworząca katalog w bieżącym katalogu.
```commandline 
mkdir dirname                                // creates dir 'dirname' 
mkdir -p directory1/directory2/directory3    // creates nested directory with all parent directories (if they don't exists)
```
# DevOps\Commandline\004_cd.md

## cd
Komenda przenosząca do innego katalogu.
```commandline 
cd ..       // goes to the parent directory
cd dirname  // goes to 'dirname' directory (if exists) 
``` 
# DevOps\Commandline\005_touch.md

## touch
Komenda tworząca nowy plik
```commandline 
touch newfile1.txt      // creates new file
``` 
# DevOps\Commandline\006_cp.md

## cp
Komenda kopiująca wskazany plik do wskazanego folderu
```commandline 
cp newfile1.txt testdir     // copies newfile1.txt to testdir
```
# DevOps\Commandline\007_mv.md

## mv
Komenda przenosząca wskazany plik do wskazanego folderu. Może również służyć do zmiany nazwy wskazanych plików.
```commandline 
mv newfile1.txt testdir     // moves newfile1.txt to testdir
mv newfile1.txt cheese.txt  // changes newfile1.txt name to cheese.txt
``` 
# DevOps\Commandline\008_rm.md

## rm
Komenda usuwająca wskazany plik/folder
```commandline 
rm test.txt      // deletes test.txt file
rm -rf testdir   // removes testdir and all it contents. Flag -rf is needed to delete directory
``` 
# DevOps\Commandline\009_cat.md

## cat
Komenda służąca do konkatenacji (łączenia) plików, ale może być również wykorzystana do wyświetlenia plików czy stworzenia nowego pliku.
```commandline 
$ cat plik1.txt plik2.txt
```

Powyższy przykład wyświetli na ekranie połączone dwa pliki.  
Możemy wynik tego działania zapisać do nowego pliku:

```commandline 
$ cat plik1.txt plik2.txt > plik3.txt
```

# DevOps\Docker\Basics\001_Docker.md

### Docker
Source: https://testdriven.io/blog/docker-for-beginners

#### Docker Engine
When people refer to Docker, they're typically referring to Docker Engine.

Docker Engine is the underlying open source containerization technology for building, managing, and running containerized applications. It's a client-server application with the following components:

1. Docker daemon (called dockerd) is a service that runs in the background that listens for Docker Engine API requests and manages Docker objects like images and containers.
2. Docker Engine API is a RESTful API that's used to interact with Docker daemon.
3. Docker client (called docker) is the command line interface used for interacting with Docker daemon. So, when you use a command like docker build, you're using Docker client, which in turn leverages Docker Engine API to communicate with Docker daemon.

#### Docker Desktop

These days, when you try to install Docker, you'll come across Docker Desktop. While Docker Engine is included with Docker Desktop, it's important to understand that Docker Desktop is not the same as Docker Engine. Docker Desktop is an integrated development environment for Docker containers. It makes it much easier to get your operating system configured for working with Docker.

#### Docker Concepts

At the heart of Docker, there are three core concepts:

1. Dockerfile - a text file that serves as a blueprint for your container. In it, you define a list of instructions that Docker uses to build an image.
2. Image - a read-only embodiment of the Dockerfile. It's built out of layers -- each layer corresponds to a single line of instructions from a Dockerfile.
3. Container - running a Docker image produces a container, which is a controlled environment for your application. If we draw parallels with object-oriented programming, a container is an instance of a Docker image.
# DevOps\Docker\Basics\002_Dockerfile.md

### Dockerfile
Source: https://testdriven.io/blog/docker-for-beginners

Again, a Dockerfile is a text file that contains instructions for Docker on how to build an image. By default, a Dockerfile has no extension, but you can add one if you need more than one -- e.g., Dockerfile.prod.

```dockerfile
FROM python:3.10-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### CMD and ENTRYPOINT

Some Docker instructions are so similar it can be hard to understand why both commands are needed. One of those "couples" are CMD and ENTRYPOINT.

First, for the similarities:

* CMD and ENTRYPOINT both specify a command / an executable that will be executed when running a container. Unlike RUN, which executes the command right away (the result is used in the image layer), the CMD/ENTRYPOINT command in the build-up specifies the command that will be used only when the container starts.
* You can have only one CMD/ENTRYPOINT instruction in a Dockerfile, but it can point to a more complicated executable file.

There's actually only one difference between those instructions:

* CMD can easily be overridden from Docker CLI.

You should use CMD if you want the flexibility to run different executables depending on your needs when starting the container. If you want to clearly communicate that command is not meant to be overridden and prevent accidentally changing it, use ENTRYPOINT.

You may also use both CMD and ENTRYPOINT in the same Dockerfile, in which case CMD serves as the default argument for the ENTRYPOINT.

You can have only one CMD instruction in a Dockerfile, but it can point to a more complicated executable file. If you have more than one CMD, only the last CMD will take effect. The same goes for the ENTRYPOINT instruction.

There's a big chance you'll see the ENTRYPOINT argument as an executable file since commands that should be executed are often more than a one-liner.

Example of ENTRYPOINT as executable file usage:

```dockerfile
ENTRYPOINT ["./entrypoint.sh"]
```

And this is what the entrypoint.sh file might look like:

```bash
###!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
```

#### ADD and COPY

Another pair similar to one another is ADD and COPY.

Both instructions copy new files or directories from the path to the filesystem of the image at the path:

```dockerfile
ADD <src> <dest>
COPY <src> <dest>
```

Additionally, ADD can copy from remote file URLs (for example, it allows adding a git repository to an image directly) and directly from a compressed archive (ADD will automatically unpack the contents to the given location).

You should prefer COPY over ADD unless you specifically need one of the two additional features of ADD -- i.e., downloading example files or unpacking a compressed file

Examples of ADD and COPY instruction usage:

```dockerfile
### copy local files on the host to the destination
COPY /source/path  /destination/path
COPY ./requirements.txt .

### download external file and copy to the destination
ADD http://external.file/url  /destination/path
ADD --keep-git-dir=true https://github.com/moby/buildkit.git#v0.10.1 /buildkit

### copy and extract local compresses files
ADD source.file.tar.gz /destination/path
```
# DevOps\Docker\Basics\003_Docker_image.md

### Docker image

Source: https://testdriven.io/blog/docker-for-beginners/#image

#### What image is?

An image might be the most confusing concept of the three. You create a Dockerfile and then use a container, but an image lies between those two.

So, an image is a read-only embodiment of a Dockerfile that's used to create a Docker container. It consists of layers -- each line in a Dockerfile makes one layer. You can't change an image directly; you change it by changing the Dockerfile. You don't directly use an image either; you use a container created from an image.

The most important image-related tasks are:

* building images from Dockerfiles
* listing all the built images
* removing images

#### Building image

To build an image from a Dockerfile, you use the docker image build command. This command requires one argument: either a path or URL of the context.

This image will use the current directory as a context:

```commandline
$ docker image build .
```
There are a number of options you can provide. For example, -f is used to specify a specific Dockerfile when you have multiple Dockerfiles (e.g., `Dockerfile.prod`) or when the Dockerfile isn't in the current directory (e.g., `docker image build . -f docker/Dockerfile.prod`).

Probably the most important is the -t tag that is used to name/tag an image.

When you build an image, it gets assigned an ID. Contrary to what you might expect, the IDs are not unique. If you want to be able to easily reference your image, you should name/tag it. With -t, you can assign a name and a tag to it.

Here's an example of creating three images: one without the usage of -t, one with a name assigned, and one with a name and a tag assigned.

```commandline
$ docker image build .
$ docker image build . -t hello_world
$ docker image build . -t hello_world:67d19c27b60bd782c9d3600ae914604a94bddfd4

$ docker image ls
REPOSITORY    TAG                                        IMAGE ID       CREATED          SIZE
hello_world   67d19c27b60bd782c9d3600ae914604a94bddfd4   e03784993f22   25 minutes ago   181MB
hello_world   latest                                     e03784993f22   26 minutes ago   181MB
<none>        <none>                                     7a615d108866   29 minutes ago   181MB
```

Notes:
* For the image that was built without a name or tag, you can only reference it via its image ID. Not only is it difficult to remember, but, again, it might not be unique (which is the case above). You should avoid this.
* For the image that only has a name (-t hello_world), the tag is automatically set to latest. You should avoid this as well. For more, review Version Docker Images.

#### Listing
The docker image ls command lists all built images.

Example:
```commandline
$ docker image ls

REPOSITORY      TAG       IMAGE ID       CREATED         SIZE
hello_world     latest    c50405e84d39   9 minutes ago   245MB
<none>          <none>    2700a62cd8f1   42 hours ago    245MB
alpine/git      latest    692618a0d74d   2 weeks ago     43.4MB
todo_app        test      999740882932   3 weeks ago     1.03GB
```

#### Removing
There are two use cases for removing images:

* You want to remove one or more selected images
* You want to remove all the unused images (you don't care which images specifically)

For the first case, you use `docker image rm;` for the second, you use `docker image prune`.

# DevOps\Docker\Basics\004_Docker_container.md

### Docker container

Source: https://testdriven.io/blog/docker-for-beginners/#container

#### What container is?

The third concept you need to understand is a container, which is a controlled environment for your application. An image becomes a container when it's run on Docker Engine. It's the end goal: You use Docker so you can have a container for your application.

The main operations you can do with a container are

* running a container
* listing all the containers
* stopping a container
* removing a container

#### Running

You can either create a new container of an image and run it, or you can start an existing container that was previously stopped.

The docker container run command actually combines two other commands, docker container create and docker container start.

```commandline
$ docker container run my_image

### the same as:

$ docker container create my_image
88ce9c60aeabbb970012b5f8dbae6f34581fa61ec20bd6d87c6831fbb5999263
$ docker container start 88ce9c60aeabbb970012b5f8dbae6f34581fa61ec20bd6d87c6831fbb5999263
```

Since you can override a number of the defaults, there are many options. You can see all of them in the official docs. The most important option is --publish/-p, which is used to publish ports to the outside world. Although it is technically possible to run a container without a port, it's not very useful since the service(s) running inside the container wouldn't be accessible outside the container. You can use --publish/-p for both the create and run commands:

```commandline
$ docker container run -p 8000:8000 my_image
```

You can run your container in detached mode by using --detach/-d, which lets you keep using the terminal.

```commandline
$ docker container run -p 8000:8000 -d my_image

0eb20b715f42bc5a053dc7878b3312c761058a25fc1efaffb7920b3b4e48df03
```

Your container gets a unique, quirky name by default, but you can assign your own name:

```commandline
$ docker container run -p 8000:8000 --name my_great_container my_image
```

To start a stopped or just created container, you use the docker container start command. Since with this command, you're starting an existing container, you have to specify the container instead of an image (as with `docker container run`).

Another difference from docker container run is that docker container start by default runs the container in the detached mode. You can attach it using --attach/-a (reverse from docker container run -d).

```commandline
$ docker container start -a reverent_sammet
```

#### Listing

You can list all running containers with docker container ls.

```commandline
$ docker container ls

CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
0f21395ec96c   9973e9c65229   "/bin/sh -c 'gunicor…"   6 minutes ago   Up 6 minutes   0.0.0.0:80->8000/tcp     shopping
73bd69d041ae   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago     Up 2 hours     0.0.0.0:8000->8000/tcp   my_great_container
```

If you want to also see the stopped containers, you can add the -a flag:

```commandline
$ docker container ls -a

CONTAINER ID   IMAGE          COMMAND                  CREATED              STATUS                     PORTS                    NAMES
0f21395ec96c   9973e9c65229   "/bin/sh -c 'gunicor…"   About a minute ago   Up About a minute          0.0.0.0:80->8000/tcp     shopping
73bd69d041ae   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago          Up 2 hours                 0.0.0.0:8000->8000/tcp   my_great_container
0eb20b715f42   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago          Exited (137) 2 hours ago                            agitated_gagarin
489a02b8cfac   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago          Created                                             vigorous_poincare
```

1. CONTAINER ID (73bd69d041ae) and its NAMES (my_great_container) are both unique, so you can use them to access the container.
2. IMAGE (my_image) tells you which image was used to run the container.
3. CREATED is pretty self-explanatory: when the container was created (2 hours ago).
4. We already discussed the need for specifying a command for starting a container... COMMAND tells you which command was used ("/bin/sh -c 'uvicorn…").
5. STATUS is useful when you don't know why your container isn't working (Up 2 hours means your container is running, Exited or Created means it's not)

#### Stopping

To stop a container, use docker container stop. The name or ID of the stopped container is then returned.

```commandline
$ docker container stop my_great_container
my_great_container

$ docker container stop 73bd69d041ae
73bd69d041ae
```

#### Removing
Similar to images, to remove a container, you can either:

* remove one or more selected containers via docker container rm.
* remove all stopped containers via docker container prune

```commandline
$ docker container rm festive_euclid
festive_euclid
```

```commandline
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
0f21395ec96c28b443bad8aac40197fe0468d24e0eed49e5f56011de1c81b589
80c693693f3d99999925eae5f4bbfc03236cde670db509797d83f50e732fcf31
0eb20b715f42bc5a053dc7878b3312c761058a25fc1efaffb7920b3b4e48df03
1273cf44c551f8ab9302e6d090e3c4e135ca6f7e1ab3d90a62bcbf5e83ba9342
```
# DevOps\Docker\Basics\005_Docker_commands.md

### Docker commands

| Command                                     | Alias	        | Usage                             |
|---------------------------------------------|---------------|-----------------------------------|
| docker image build                          | docker build  | Build an image from a Dockerfile  |
| docker image ls	                            | docker images | 	List images                      |
| docker image rm	                            | docker rmi    | 	Remove selected images           |
| docker image prune                          | 	N/A	         | Remove unused images              |
| docker container run                        | 	docker run	  | Create the container and start it |
| docker container start                      | 	docker start | 	Start an existing container      |
| docker container ls	                        | docker ps	    | List all containers               |
| docker container stop                       | 	docker stop  | 	Stop a container                 |
| docker container rm	                        | docker rm     | 	Remove a container               |
| docker container prune                      | 	N/A          | 	Remove all stopped containers    |
| docker container logs <CONTAINER ID / name> | N/A | Show container logs |
# DevOps\Docker\Basics\006_Volume.md

### Volume
Volume to przestrzeń w kontenerze, gdzie mogą być wykonywane trwałe operacje na plikach, które będą widoczne nawet po usunięciu kontenera. Aby określić ścieżkę do volume'a należy użyć klauzuli **VOLUME** w Dockerfile:
```commandline 
VOLUME [<PATH 1>, ... <PATH n>]
``` 
Przykład:
```commandline 
VOLUME ["/appdata"]
``` 
Aby sprawdzić, istniejące volume'y należy użyć komendy poniżej. Zwrócone zostaną dane o driverze i nazwie volume'a.
```commandline 
docker volume ls
``` 
Aby uruchomić nowy kontener z wykorzystaniem istniejącego volume'a należy użyć flagi **mount**:
```commandline 
docker container run ... --mount 'src=<VOLUME_NAME>, dst=<VOLUME_PATH>' ...
``` 
**VOLUME_NAME** to nazwa volume'a pobrana z komendy *docker volume ls*, natomiast **VOLUME_PATH** to ścieżka zdefiniowana przez nas w Dockerfile'u.

# DevOps\Docker\Basics\007_Bind_mount.md

### Bind mount
Podłączenie konkretnego folderu z używanego hosta do obraz (np. konkretnej ścieżki do folderu na komputerze, gdzie kontener jest uruchomiony lokalnie).
```commandline 
docker container run ... <HOST_PATH>:<CONTAINER_PATH> ...
``` 
**HOST_PATH** to ścieżka, z której mają zostać załadowane pliki współdzielone z kontenerem. **CONTAINER_PATH** to ścieżka w kontenerze, do której mają zostać załadowane pliki ze ścieżki hosta. 

Synchronizacja działa w dwie strony. Jeżli plik zostanie utworzony w kontenerze, to również zostanie przeniesiony do hosta.

# DevOps\Docker\Dockerfile_best_practices\001_Multi-stage_Builds.md

### Multi-stage Builds

Source: https://testdriven.io/blog/docker-best-practices/#use-multi-stage-builds

Multi-stage Docker builds allow you to break up your Dockerfiles into several stages. For example, you can have a stage for compiling and building your application, which can then be copied to subsequent stages. Since only the final stage is used to create the image, the dependencies and tools associated with building your application are discarded, leaving a lean and modular production-ready image.

```dockerfile
### temp stage
FROM python:3.12.2-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


### final stage
FROM python:3.12.2-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*
```

In this example, the GCC compiler is required for installing certain Python packages, so we added a temp, build-time stage to handle the build phase. Since the final run-time image does not contain GCC, it's much lighter and more secure.

Size comparison:
```commandline
REPOSITORY                 TAG                    IMAGE ID       CREATED          SIZE
docker-single              latest                 8d6b6a4d7fb6   16 seconds ago   259MB
docker-multi               latest                 813c2fa9b114   3 minutes ago    156MB
```
# DevOps\Docker\Dockerfile_best_practices\002_Order_Dockerfile_commands_appropriately.md

### Order Dockerfile Commands Appropriately

Source: https://testdriven.io/blog/docker-best-practices/#order-dockerfile-commands-appropriately

Docker caches each step (or layer) in a particular Dockerfile to speed up subsequent builds. When a step changes, the cache will be invalidated not only for that particular step but all succeeding steps.

```dockerfile
FROM python:3.12.2-slim

WORKDIR /app

COPY sample.py .

COPY requirements.txt .

RUN pip install -r requirements.txt
```

In this Dockerfile, we copied over the application code before installing the requirements. Now, each time we change sample.py, the build will reinstall the packages. This is very inefficient, especially when using a Docker container as a development environment. Therefore, it's crucial to keep the files that frequently change towards the end of the Dockerfile.

So, in the above Dockerfile, you should move the COPY sample.py . command to the bottom:

```dockerfile
FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY sample.py .
```
Notes:

* Always put layers that are likely to change as low as possible in the Dockerfile.
* Combine RUN apt-get update and RUN apt-get install commands. (This also helps to reduce the image size. We'll touch on this shortly.)
* If you want to turn off caching for a particular Docker build, add the --no-cache=True flag.
# DevOps\Docker\Dockerfile_best_practices\003_Use_Small_Docker_Base_Images.md

### Use Small Docker Base Images

Source: https://testdriven.io/blog/docker-best-practices/#use-small-docker-base-images

Building, pushing, and pulling images is quicker with smaller images. They also tend to be more secure since they only include the necessary libraries and system dependencies required for running your application.

*Which Docker base image should you use?*

Unfortunately, it depends.

Here's a size comparison of various Docker base images for Python:

```commandline
REPOSITORY   TAG                    IMAGE ID         CREATED          SIZE
python       3.12.2-bookworm        939b824ad847     40 hours ago     1.02GB
python       3.12.2-slim            24c52ee82b5c     40 hours ago     130MB
python       3.12.2-slim-bookworm   24c52ee82b5c     40 hours ago     130MB
python       3.12.2-alpine          c54b53ca8371     40 hours ago     51.8MB
python       3.12.2-alpine3.19      c54b53ca8371     40 hours ago     51.8MB
```

While the Alpine flavor, based on Alpine Linux, is the smallest, it can often lead to increased build times if you can't find compiled binaries that work with it. As a result, you may end up having to build the binaries yourself, which can increase the image size (depending on the required system-level dependencies) and the build times (due to having to compile from the source).

In the end, it's all about balance. When in doubt, start with a *-slim flavor, especially in development mode, as you're building your application. You want to avoid having to continually update the Dockerfile to install necessary system-level dependencies when you add a new Python package. As you harden your application and Dockerfile(s) for production, you may want to explore using Alpine for the final image from a multi-stage build.
# DevOps\Docker\Dockerfile_best_practices\004_Minimize_number_of_layers.md

### Minimize the Number of Layers

Source: https://testdriven.io/blog/docker-best-practices/#minimize-the-number-of-layers

It's a good idea to combine the RUN, COPY, and ADD commands as much as possible since they create layers. Each layer increases the size of the image since they are cached. Therefore, as the number of layers increases, the size also increases.

You can test this out with the docker history command:

```commandline
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
dockerfile   latest    180f98132d02   51 seconds ago   259MB

$ docker history 180f98132d02

IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
180f98132d02   58 seconds ago       COPY . . # buildkit                             6.71kB    buildkit.dockerfile.v0
<missing>      58 seconds ago       RUN /bin/sh -c pip install -r requirements.t…   35.5MB    buildkit.dockerfile.v0
<missing>      About a minute ago   COPY requirements.txt . # buildkit              58B       buildkit.dockerfile.v0
<missing>      About a minute ago   WORKDIR /app
...
```
Take note of the sizes. Only the RUN, COPY, and ADD commands add size to the image. You can reduce the image size by combining commands wherever possible. For example:
```dockerfile
RUN apt-get update
RUN apt-get install -y netcat
```
Can be combined into a single RUN command:

```dockerfile
RUN apt-get update && apt-get install -y netcat
```

While it's a good idea to reduce the number of layers, it's much more important for that to be less of a goal in itself and more a side-effect of reducing the image size and build times. In other words, focus more on the previous three practices -- multi-stage builds, order of your Dockerfile commands, and using a small base image -- than trying to optimize every single command.

Notes:

* RUN, COPY, and ADD each create layers.
* Each layer contains the differences from the previous layer.
* Layers increase the size of the final image.

Tips:

* Combine related commands.
* Remove unnecessary files in the same RUN step that created them.
* Minimize the number of times apt-get upgrade is run since it upgrades all packages to the latest version.
* With multi-stage builds, don't worry too much about overly optimizing the commands in temp stages.

```dockerfile
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    matplotlib \
    pillow  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

Additionally, it's crucial to perform clean-up actions within the same RUN instruction to avoid unnecessary bloat in your Docker images. This approach ensures that temporary files or cache used during installation are not included in the final image layer, effectively reducing the image size. For example, after installing packages with apt-get, use && apt-get clean && rm -rf /var/lib/apt/lists/* to remove the package lists and any temporary files created during the installation process, as demonstrated above. This practice is essential for keeping your Docker images as lean and efficient as possible.
# DevOps\Docker\Dockerfile_best_practices\005_Use_unprivilaged_containers.md

### Use Unprivileged Containers

Source: https://testdriven.io/blog/docker-best-practices/#use-unprivileged-containers

By default, Docker runs container processes as root inside of a container. However, this is a bad practice since a process running as root inside the container is running as root in the Docker host. Thus, if an attacker gains access to your container, they have access to all the root privileges and can perform several attacks against the Docker host, like-
* copying sensitive info from the host's filesystem to the container
* executing remote commands

To prevent this, make sure to run container processes with a non-root user:

```dockerfile
RUN addgroup --system app && adduser --system --group app

USER app
```

You can take it a step further and remove shell access and ensure there's no home directory as well:
```dockerfile
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app
```

Verify:

```commandline
$ docker run -i sample id

uid=1001(app) gid=1001(app) groups=1001(app)
```


# DevOps\Docker\Dockerfile_best_practices\006_Prefer_COPY_over_ADD.md

### Prefer COPY Over ADD

Source: https://testdriven.io/blog/docker-best-practices/#prefer-copy-over-add

Use COPY unless you're sure you need the additional functionality that comes with ADD.

Both commands allow you to copy files from a specific location into a Docker image:

```dockerfile
ADD <src> <dest>
COPY <src> <dest>
```

While they look like they serve the same purpose, ADD has some additional functionality:

* COPY is used for copying local files or directories from the Docker host to the image.
* ADD can be used for the same thing as well as downloading external files. Also, if you use a compressed file (tar, gzip, bzip2, etc.) as the <src> parameter, ADD will automatically unpack the contents to the given location.

```dockerfile
### copy local files on the host to the destination
COPY /source/path  /destination/path
ADD /source/path  /destination/path

### download external file and copy to the destination
ADD http://external.file/url  /destination/path

### copy and extract local compresses files
ADD source.file.tar.gz /destination/path
```
# DevOps\Docker\Dockerfile_best_practices\007_Cache_Python_packages_to_Docker_host.md

### Cache Python Packages to the Docker Host

Source: https://testdriven.io/blog/docker-best-practices/#cache-python-packages-to-the-docker-host

When a requirements file is changed, the image needs to be rebuilt to install the new packages. The earlier steps will be cached, as mentioned in Minimize the Number of Layers. Downloading all packages while rebuilding the image can cause a lot of network activity and takes a lot of time. Each rebuild takes up the same amount of time for downloading common packages across builds.

You can avoid this by mapping the pip cache directory to a directory on the host machine. So for each rebuild, the cached versions persist and can improve the build speed.

Add a volume to the docker run as `-v $HOME/.cache/pip-docker/:/root/.cache/pip` or as a mapping in the Docker Compose file.

Moving the cache from the docker image to the host can save you space in the final image.


# DevOps\Docker\Dockerfile_best_practices\008_Run_only_one_process_per_container.md

### Run Only One Process Per Container

Source: https://testdriven.io/blog/docker-best-practices/#run-only-one-process-per-container

Why is it recommended to run only one process per container?

Let's assume your application stack consists of a two web servers and a database. While you could easily run all three from a single container, you should run each in a separate container to make it easier to reuse and scale each of the individual services.

1. Scaling - With each service in a separate container, you can scale one of your web servers horizontally as needed to handle more traffic.
2. Reusability - Perhaps you have another service that needs a containerized database. You can simply reuse the same database container without bringing two unnecessary services along with it.
3. Logging - Coupling containers makes logging much more complex. We'll address this in further detail later in this article.
4. Portability and Predictability - It's much easier to make security patches or debug an issue when there's less surface area to work with.
# DevOps\Docker\Dockerfile_best_practices\009_Prefer_array_over_string_syntax.md

### Prefer Array Over String Syntax

Source: https://testdriven.io/blog/docker-best-practices/#prefer-array-over-string-syntax

You can write the CMD and ENTRYPOINT commands in your Dockerfiles in both array (exec) or string (shell) formats:

```dockerfile
### array (exec)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

### string (shell)
CMD "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
```

Both are correct and achieve nearly the same thing; however, you should use the exec format whenever possible. From the Docker documentation:

1. Make sure you're using the exec form of CMD and ENTRYPOINT in your Dockerfile.
2. For example use ["program", "arg1", "arg2"] not "program arg1 arg2". Using the string form causes Docker to run your process using bash, which doesn't handle signals properly. Compose always uses the JSON form, so don't worry if you override the command or entrypoint in your Compose file.

So, since most shells don't process signals to child processes, if you use the shell format, CTRL-C (which generates a SIGTERM) may not stop a child process.

```dockerfile
FROM ubuntu:24.04

### BAD: shell format
ENTRYPOINT top -d

### GOOD: exec format
ENTRYPOINT ["top", "-d"]
```

Try both of these. Take note that with the shell format flavor, `CTRL-C` won't kill the process. Instead, you'll see `^C^C^C^C^C^C^C^C^C^C^C`.


# DevOps\Docker\Dockerfile_best_practices\010_Understand_difference_between_ENTRYPOINT_and_CMD.md

### Understand the Difference Between ENTRYPOINT and CMD

Source: https://testdriven.io/blog/docker-best-practices/#understand-the-difference-between-entrypoint-and-cmd

There are two ways to run commands in a container:

```dockerfile
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]

### and

ENTRYPOINT ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
```

Both essentially do the same thing: Start the application at `config.wsgi` with a Gunicorn server and bind it to `0.0.0.0:8000`.

The CMD is easily overridden. If you run `docker run <image_name> uvicorn config.asgi`, the above `CMD` gets replaced by the new arguments -- i.e., `uvicorn config.asgi`. Whereas to override the `ENTRYPOINT` command, one must specify the `--entrypoint` option:
```commandline
docker run --entrypoint uvicorn config.asgi <image_name>
```

Here, it's clear that we're overriding the entrypoint. So, it's recommended to use `ENTRYPOINT` over `CMD` to prevent accidentally overriding the command.

They can be used together as well.

```dockerfile
ENTRYPOINT ["gunicorn", "config.wsgi", "-w"]
CMD ["4"]
```

When used together like this, the command that is run to start the container is:

```commandline
gunicorn config.wsgi -w 4
```
As discussed above, CMD is easily overridden. Thus, CMD can be used to pass arguments to the ENTRYPOINT command. The number of workers can be easily changed like so:

```commandline
docker run <image_name> 6
```
This will start the container with six Gunicorn workers rather then four.


# DevOps\Docker\Dockerfile_best_practices\011_Include_HEALHCHECK.md

### Include a HEALTHCHECK Instruction

Source: https://testdriven.io/blog/docker-best-practices/#include-a-healthcheck-instruction

Use a HEALTHCHECK to determine if the process running in the container is not only up and running, but is "healthy" as well.

Docker exposes an API for checking the status of the process running in the container, which provides much more information than just whether the process is "running" or not since "running" covers "it is up and working", "still launching", and even "stuck in some infinite loop error state". You can interact with this API via the HEALTHCHECK instruction.

For example, if you're serving up a web app, you can use the following to determine if the / endpoint is up and can handle serving requests:

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1
```

If you run `docker ps`, you can see the status of the HEALTHCHECK.

Healthy example:

```commandline
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS                            PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   10 seconds ago   Up 8 seconds (health: starting)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

Unhealthy example:
```commandline
CONTAINER ID   IMAGE         COMMAND                  CREATED              STATUS                          PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   About a minute ago   Up About a minute (unhealthy)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

You can take it a step further and set up a custom endpoint used only for health checks and then configure the 
`HEALTHCHECK` to test against the returned data. For example, if the endpoint returns a JSON 
response of `{"ping": "pong"}`, you can instruct the `HEALTHCHECK` to validate the response body.

Here's how you view the status of the health check status using docker inspect:

```commandline
❯ docker inspect --format "{{json .State.Health }}" ab94f2ac7889
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2021-09-28T15:22:57.5764644Z",
      "End": "2021-09-28T15:22:57.7825527Z",
      "ExitCode": 0,
      "Output": "..."
```

You can also add a health check to a Docker Compose file:

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - '8000:8000'
    healthcheck:
      test: curl --fail http://localhost:8000 || exit 1
      interval: 10s
      timeout: 10s
      start_period: 10s
      retries: 3
```
Options:

* `test`: The command to test.
* `interval`: The interval to test for -- e.g., test every x unit of time.
* `timeout`: Max time to wait for the response.
* `start_period`: When to start the health check. It can be used when additional tasks are performed before the containers are ready, like running migrations.
* `retries`: Maximum retries before designating a test as failed.
# DevOps\Docker\Dockerfile_best_practices\012_Optimizing_Dockefile_build_with_poetry.md

### Optimizing Dockerfile build with poetry

Source: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

#### Project structure

``` 
.
├── Dockerfile
├── README.md
├── annapurna
│   ├── __init__.py
│   └── main.py
├── poetry.lock
└── pyproject.toml
```

pyproject.toml
```toml
[tool.poetry]
name = "annapurna"
version = "1.0.0"
description = ""
authors = ["Riccardo Albertazzi <my@email.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"

fastapi = "^0.95.1"


[tool.poetry.group.dev.dependencies]
black = "^23.3.0"
mypy = "^1.2.0"
ruff = "^0.0.263"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### Naive approach

```dockerfile
FROM python:3.11-buster

RUN pip install poetry

COPY .. .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

#### First improvements

```dockerfile
FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY annapurna ./annapurna
RUN touch README.md

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

* Pin the `poetry` version, as Poetry can contain breaking changes from one minor version to other, and you don’t want your builds to suddenly break when a new version is released. 
* Just `COPY` the data that you need, and nothing else. 
* Poetry will complain if a README.md is not found (I don’t really share this choice) and as such I create an empty one. 
* Avoid installing development dependencies with `poetry install --without dev` , as you won’t need linters and tests suites in your production environment.

#### Cleaning Poetry cache

```dockerfile
FROM python:3.11-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY annapurna ./annapurna
RUN touch README.md

RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

* By default, Poetry caches downloaded packages so that they can be re-used for future installation commands. We clearly don’t care about this in a Docker build (do we?) and as such we can remove this duplicate storage.
* When removing the cache folder make sure this is done in the same RUN command. If it’s done in a separate RUN command the cache will still be part of the previous Docker layer (the one containing poetry install ), effectively rendering your optimization useless.
* While doing this I’m also setting a few Poetry environment variables to further strengthen the determinism of my build. The most controversial one is POETRY_VIRTUALENVS_CREATE=1. What’s the point why would I want to create a virtual environment inside a Docker container? I honestly prefer this solution over who disables this flag, as it makes sure that my environment will be as isolated as possible and above all that my installation will not mess up with the system Python or, even worse, with Poetry itself.

#### Installing dependencies before copying code 

```dockerfile
FROM python:3.11-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY annapurna ./annapurna

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
```

* The solution here is to provide Poetry with the minimal information needed to build the virtual environment and only later COPY our codebase. We can achieve this with the --no-root option, which instructs Poetry to avoid installing the current project into the virtual environment.
* The additional RUN poetry install --without dev instruction is needed to install your project in the virtual environment. This can be useful for example for installing any custom script. Depending on your project you may not even need this step. Anyways, this layer execution will be super fast since the project dependencies have already been installed.

#### Using Docker multi-stage builds

```dockerfile
### The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

### The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY annapurna ./annapurna

ENTRYPOINT ["python", "-m", "annapurna.main"]
```
* Python `buster` is a big image that comes with development dependencies, and we will use it to install a virtual environment. Python `slim-buster` is a smaller image that comes with the minimal dependencies to just run Python, and we will use it to run our application.
* Poetry isn’t even installed in the runtime stage. Poetry is in fact an unnecessary dependency for running your Python application once your virtual environment is built. We just need to play with environment variables (such as the VIRTUAL_ENV variable) to let Python recognize the right virtual environment.
* For simplicity I removed the second installation step (`RUN poetry install --without dev `) as I don’t need it for my toy project, although one could still add it in the runtime image in a single instruction: `RUN pip install poetry && poetry install --without dev && pip uninstall poetry` .

#### Buildkit Cache Mounts

```dockerfile
FROM python:3.11-buster as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY annapurna ./annapurna

ENTRYPOINT ["python", "-m", "annapurna.main"]
```

* Once Dockerfiles get more complex I also suggest using Buildkit, the new build backend plugged into the Docker CLI. If you are looking for fast and secure builds, that’s the tool to use.
```
DOCKER_BUILDKIT=1 docker build --target=runtime .
```
* This final trick is not known to many as it’s rather newer compared to the other features I presented. It leverages Buildkit cache mounts, which basically instruct Buildkit to mount and manage a folder for caching reasons. The interesting thing is that such cache will persist across builds!
* By plugging this feature with Poetry cache (now you understand why I did want to keep caching?) we basically get a dependency cache that is re-used every time we build our project. The result we obtain is a fast dependency build phase when building the same image multiple times on the same environment.
* Note how the Poetry cache is not cleared after installation, as this would prevent to store and re-use the cache across builds. This is fine, as Buildkit will not persist the managed cache in the built image (plus, it’s not even our runtime image).
# DevOps\Docker\Docker_compose\001_Docker_compose_file.md

### Plik docker_compose
Plik *docker-compose.yaml* pozwala na zdefiniowanie zależności między kontenerami, wolumenami i sieciami w uporządkowany sposób. 

Schemat pliku:
```dockerfile
version: '3.7'

services: # definicja kontenerów (odpowiednik docker container run)
	servicename1: # nazwa serwisu (np. elasticsearch), będzie to także DNS serwisu w sieci
		image: # nazwa obrazu którego użyć do uruchomienia kontenera (opcjonalny w przypadku użycia build)
		environment: # zmienne środowiskowe przekazywane do kontenera przy jego uruchomieniu
			KEY: value
			KEY2: value2
			# - KEY=value
			# - KEY2=value2
		env_file: # zmienne środowiskowe z pliku
			- a.env
		command: # nadpisanie domyślnego polecenia kontenera/obrazu
		volumes: # odpowiednik -v z docker run (wsparcie zarówno starszej jak i nowszej składni)
	servicename2: # kolejny serwis

volumes: # definicja wolumenu (docker volume create)

networks: # definicja sieci (docker network create)
``` 

Przykładowe zastosowanie docker-compose do uruchomienia obrazu Elasticsearch.
```dockerfile
version: '3.7'

### docker container run -p 9200:9200 -e cluster.name=kursdockera -v $(pwd)/esdata:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:6.5.4

services:
	elasticsearch:
		container_name: elasticsearch
		image: docker.elastic.co/elasticsearch/elasticsearch:6.5.4
		volumes:
			- ./esdata:/usr/share/elasticsearch/data
		environment:
			- cluster.name=kursdockera
		ports:
			- 9200:9200
```
# DevOps\Docker\Docker_compose\002_Docker_compose_commands.md

### Komendy dla docker compose
```commandline 
docker compose up
``` 
Tworzy wszystkie sieci, wolumeny, uruchamia wszystkie kontenery.
```commandline 
docker compose ps
``` 
Lista uruchomionych kontenerów w docker-compose.
```commandline 
docker compose stop
``` 
Zastopowanie wszystkich kontenerów.
```commandline 
docker compose down
``` 
Zatrzymanie i usunięcie konterów, usunięcie sieci.

# DevOps\Docker\General_best_practices\001_Using_Python_Virtual_Environments.md

### Using Python Virtual Environments

In most cases, virtual environments are unnecessary as long as you stick to running only a single process per container. Since the container itself provides isolation, packages can be installed system-wide. That said, you may want to use a virtual environment in a multi-stage build rather than building wheel files.

Example with wheels:

```dockerfile
### temp stage
FROM python:3.12.2-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


### final stage
FROM python:3.12.2-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*
```

Example with virtualenv:

```dockerfile
### temp stage
FROM python:3.12.2-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


### final stage
FROM python:3.12.2-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"
```

# DevOps\Docker\General_best_practices\002_Set_Memory_and_CPU_limits.md

### Set Memory and CPU Limits

Source: https://testdriven.io/blog/docker-best-practices/#set-memory-and-cpu-limits

It's a good idea to limit the memory usage of your Docker containers, especially if you're running multiple containers on a single machine. This can prevent any of the containers from using all available memory and thereby crippling the rest.

The easiest way to limit memory usage is to use --memory and --cpu options in the Docker CLI:

```commandline
$ docker run --cpus=2 -m 512m nginx
```

The above command limits the container usage to 2 CPUs and 512 megabytes of main memory.

You can do the same in a Docker Compose file like so:

```yaml
version: "3.9"
services:
  redis:
    image: redis:alpine
    deploy:
      resources:
        limits:
          cpus: 2
          memory: 512M
        reservations:
          cpus: 1
          memory: 256M
```

Take note of the `reservations` field. It's used to set a soft limit, which takes priority when the host machine has low memory or CPU resources.


# DevOps\Docker\General_best_practices\003_Log_to_stdout_or_stderr.md

### Log to stdout or stderr

Source: https://testdriven.io/blog/docker-best-practices/#log-to-stdout-or-stderr

Applications running within your Docker containers should write log messages to standard output (stdout) and standard error (stderr) rather than to a file.

You can then configure the Docker daemon to send your log messages to a centralized logging solution (like CloudWatch Logs or Papertrail).


# DevOps\Docker\General_best_practices\004_Use_Shared_Memory_Mount_for_Gunicorn_Heartbeat.md

### Use a Shared Memory Mount for Gunicorn Heartbeat

Source: https://testdriven.io/blog/docker-best-practices/#use-a-shared-memory-mount-for-gunicorn-heartbeat

Gunicorn uses a file-based heartbeat system to ensure that all of the forked worker processes are alive.

In most cases, the heartbeat files are found in "/tmp", which is often in memory via tmpfs. Since Docker does not leverage tmpfs by default, the files will be stored on a disk-backed file system. This can cause problems, like random freezes since the heartbeat system uses os.fchmod, which may block a worker if the directory is in fact on a disk-backed filesystem.

Fortunately, there is a simple fix: Change the heartbeat directory to a memory-mapped directory via the --worker-tmp-dir flag.

```commandline
gunicorn --worker-tmp-dir /dev/shm config.wsgi -b 0.0.0.0:8000
```
# DevOps\Docker\General_best_practices\005_Secure_Communication_with_TLS.md

### Secure Communication with TLS

Source: https://testdriven.io/blog/docker-best-practices/#secure-communication-with-tls

When a Docker daemon is exposed to the network or accessed over a network, securing the communication channel is crucial to prevent unauthorized access and ensure the integrity and confidentiality of the data being transmitted. Using TLS (Transport Layer Security) helps in encrypting the communication between the Docker client and the Docker daemon, making it significantly more secure.

To set up TLS for Docker, you'll need to generate SSL certificates: a CA (Certificate Authority) certificate, a server certificate for the Docker daemon, and a client certificate for the Docker client. These certificates are used to encrypt the communication and authenticate the client and server to each other.
# DevOps\Docker\Images_best_practices\001_Version_Docker_Images.md

### Version Docker Images

Source: https://testdriven.io/blog/docker-best-practices/#version-docker-images

Whenever possible, avoid using the latest tag.

If you rely on the latest tag (which isn't really a "tag" since it's applied by default when an image isn't explicitly tagged), you can't tell which version of your code is running based on the image tag. It makes it challenging to do rollbacks and makes it easy to overwrite it (either accidentally or maliciously). Tags, like your infrastructure and deployments, should be immutable.

Regardless of how you treat your internal images, you should never use the latest tag for base images since you could inadvertently deploy a new version with breaking changes to production.

For internal images, use descriptive tags to make it easier to tell which version of the code is running, handle rollbacks, and avoid naming collisions.

For example, you can use the following descriptors to make up a tag:

1. Timestamps
2. Docker image IDs
3. Git commit hashes
4. Semantic version

For example:
```commandline
docker build -t web-prod-a072c4e5d94b5a769225f621f08af3d4bf820a07-0.1.4 .
```

Here, we used the following to form the tag:

1. Project name: web
2. Environment name: prod
3. Git commit hash: a072c4e5d94b5a769225f621f08af3d4bf820a07
4. Semantic version: 0.1.4

It's essential to pick a tagging scheme and be consistent with it. Since commit hashes make it easy to tie an image tag back to the code quickly, it's highly recommended to include them in your tagging scheme.
# DevOps\Docker\Images_best_practices\002_No_secrets_in_images.md

### Don't Store Secrets in Images

Source: https://testdriven.io/blog/docker-best-practices/#dont-store-secrets-in-images

Secrets are sensitive pieces of information such as passwords, database credentials, SSH keys, tokens, and TLS certificates, to name a few. These should not be baked into your images without being encrypted since unauthorized users who gain access to the image can merely examine the layers to extract the secrets.

Do not add secrets to your Dockerfiles in plaintext, especially if you're pushing the images to a public registry like Docker Hub:

```dockerfile
FROM python:3.12.2-slim

ENV DATABASE_PASSWORD "SuperSecretSauce"
```

Instead, they should be injected via:

* Environment variables (at run-time)
* Build-time arguments (at build-time)
* An orchestration tool like Docker Swarm (via Docker secrets) or Kubernetes (via Kubernetes secrets)

Also, you can help prevent leaking secrets by adding common secret files and folders to your .dockerignore file:
```commandline
**/.env
**/.aws
**/.ssh
```
Finally, be explicit about what files are getting copied over to the image rather than copying all files recursively:
```dockerfile
### BAD
COPY . .

### GOOD
copy ./app.py .
```

Being explicit also helps to limit cache-busting.

#### Environment Variables
You can pass secrets via environment variables, but they will be visible in all child processes, linked containers, and logs, as well as via docker inspect. It's also difficult to update them.

```commandline
$ docker run --detach --env "DATABASE_PASSWORD=SuperSecretSauce" python:3.9-slim

d92cf5cf870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239


$ docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' d92cf5cf870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239

DATABASE_PASSWORD=SuperSecretSauce
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
PYTHON_VERSION=3.9.7
PYTHON_PIP_VERSION=21.2.4
PYTHON_SETUPTOOLS_VERSION=57.5.0
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/c20b0cfd643cd4a19246ccf204e2997af70f6b21/public/get-pip.py
PYTHON_GET_PIP_SHA256=fa6f3fb93cce234cd4e8dd2beb54a51ab9c247653b52855a48dd44e6b21ff28b
```

This is the most straightforward approach to secrets management. While it's not the most secure, it will keep the honest people honest since it provides a thin layer of protection, helping to keep the secrets hidden from curious wandering eyes.

Passing secrets in using a shared volume is a better solution, but they should be encrypted, via Vault or AWS Key Management Service (KMS), since they are saved to disc.

#### Build-time Arguments

You can pass secrets in at build-time using build-time arguments, but they will be visible to those who have access to the image via docker history.

```dockerfile
FROM python:3.12.2-slim

ARG DATABASE_PASSWORD
```

```commandline
$ docker build --build-arg "DATABASE_PASSWORD=SuperSecretSauce" .
```

If you only need to use the secrets temporarily as part of the build -- e.g., SSH keys for cloning a private repo or downloading a private package -- you should use a multi-stage build since the builder history is ignored for temporary stages:

```dockerfile
### temp stage
FROM python:3.12.2-slim as builder

### secret
ARG SSH_PRIVATE_KEY

### install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git

### use ssh key to clone repo
RUN mkdir -p /root/.ssh/ && \
    echo "${PRIVATE_SSH_KEY}" > /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts &&
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN git clone git@github.com:testdrivenio/not-real.git


### final stage
FROM python:3.12.2-slim

WORKDIR /app

### copy the repository from the temp image
COPY --from=builder /your-repo /app/your-repo

### use the repo for something!
```
The multi-stage build only retains the history for the final image. Keep in mind that you can use this functionality for permanent secrets that you need for your application, like a database credential.

You can also use the new --secret option in Docker build to pass secrets to Docker images that do not get stored in the images.
```dockerfile
### "docker_is_awesome" > secrets.txt

FROM alpine

### shows secret from default secret location:
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```
This will mount the secret from the secrets.txt file.

Build the image:

```commandline
docker build --no-cache --progress=plain --secret id=mysecret,src=secrets.txt .

### output
...
###4 [1/2] FROM docker.io/library/alpine
###4 sha256:665ba8b2cdc0cb0200e2a42a6b3c0f8f684089f4cd1b81494fbb9805879120f7
###4 CACHED

###5 [2/2] RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
###5 sha256:75601a522ebe80ada66dedd9dd86772ca932d30d7e1b11bba94c04aa55c237de
###5 0.635 docker_is_awesome#5 DONE 0.7s

###6 exporting to image
```

Finally, check the history to see if the secret is leaking:

```commandline
❯ docker history 49574a19241c
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
49574a19241c   5 minutes ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      5 minutes ago   RUN /bin/sh -c cat /run/secrets/mysecret # b…   0B        buildkit.dockerfile.v0
<missing>      4 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      4 weeks ago     /bin/sh -c #(nop) ADD file:aad4290d27580cc1a…   5.6MB
```

# DevOps\Docker\Images_best_practices\003_dockerignore_file.md

#### Use a .dockerignore File

Source: https://testdriven.io/blog/docker-best-practices/#use-a-dockerignore-file

his file is used to specify the files and folders that you don't want to be added to the initial build context sent to the Docker daemon, which will then build your image. Put another way, you can use it to define the build context that you need.

When a Docker image is built, the entire Docker context -- e.g., the root of your project -- is sent to the Docker daemon before the COPY or ADD commands are evaluated. This can be pretty expensive, especially if you have many dependencies, large data files, or build artifacts in your project. Plus, the Docker CLI and daemon may not be on the same machine. So, if the daemon is executed on a remote machine, you should be even more mindful of the size of the build context.

What should you add to the .dockerignore file?

* Temporary files and folders
* Build logs
* Local secrets
* Local development files like docker-compose.yml
* Version control folders like ".git", ".hg", and ".svn"

Example:

```commandline
**/.git
**/.gitignore
**/.vscode
**/coverage
**/.env
**/.aws
**/.ssh
Dockerfile
README.md
docker-compose.yml
**/.DS_Store
**/venv
**/env
```

In summary, a properly structured .dockerignore can help:

* Decrease the size of the Docker image
* Speed up the build process
* Prevent unnecessary cache invalidation
* Prevent leaking secrets
# DevOps\Docker\Images_best_practices\004_Lint_and_scan_Dockerfiles_and_images.md

### Lint and Scan Your Dockerfiles and Images

Source: https://testdriven.io/blog/docker-best-practices/#lint-and-scan-your-dockerfiles-and-images

Linting is the process of checking your source code for programmatic and stylistic errors and bad practices that could lead to potential flaws. Just like with programming languages, static files can also be linted. With your Dockerfiles specifically, linters can help ensure they are maintainable, avoid deprecated syntax, and adhere to best practices. Linting your images should be a standard part of your CI pipelines.

Hadolint is the most popular Dockerfile linter:

```commandline
$ hadolint Dockerfile

Dockerfile:1 DL3006 warning: Always tag the version of an image explicitly
Dockerfile:7 DL3042 warning: Avoid the use of cache directory with pip. Use `pip install --no-cache-dir <package>`
Dockerfile:9 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
Dockerfile:17 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments
```

You can see it in action online at https://hadolint.github.io/hadolint/. There's also a VS Code Extension.

You can couple linting your Dockerfiles with scanning images and containers for vulnerabilities.


# DevOps\Docker\Images_best_practices\005_Sign_and_verify_images.md

### Sign and Verify Images

Source: https://testdriven.io/blog/docker-best-practices/#sign-and-verify-images

How do you know that the images used to run your production code have not been tampered with?

Tampering can come over the wire via man-in-the-middle (MITM) attacks or from the registry being compromised altogether.

Docker Content Trust (DCT) enables the signing and verifying of Docker images from remote registries.

To verify the integrity and authenticity of an image, set the following environment variable:

```dotenv
DOCKER_CONTENT_TRUST=1
```

Now, if you try to pull an image that hasn't been signed, you'll receive the following error:

```commandline
Error: remote trust data does not exist for docker.io/namespace/unsigned-image:
notary.docker.io does not have trust data for docker.io/namespace/unsigned-image
```

You can learn about signing images from the Signing Images with [Docker Content Trust documentation](https://docs.docker.com/engine/security/trust/#signing-images-with-docker-content-trust).
# DevOps\GIT\001_Basics.md

## Podstawy
`GIT` - rozproszony system kontroli wersji  
`remote (origin)` - centralne repozytorium  
`local` - lokalne repozytorium  
`working directory` - kod, nad którym wciąż pracujemy znajduje się w tym obszarze. Aby przenieść go do staging area, należy użyć komendy **git add**  
`staging area` - przestrzeń, w której znajdują się pliki, które planujemy dodać do commita. Jest to krok pośredni między pracą nad plikiem, a wysłaniem do go centralnego repozytorium  
  
# DevOps\GIT\002_Base_commands.md

## Podstawowe komendy
### git config

```bash  
git config --global user.name "<username>"
git config --global user.email "<email>"
```  
### git init  
```bash  
git init
```  
### git remote  
```bash  
git remote add origin "<remote_repository_url>"
```  
### git clone  
Klonowanie repozytorium z podanego linka  
```bash  
git clone "<remote_repository_url>"
```  
### git status  
Stan aktualnego brancha w porównaniu do ostatniego commita  
```bash  
git status
```  
### git log  
Historia commitów na aktualnym branchu (od najnowszego do najstarszego)  
```bash  
git log
```  
### git branch  
Lista branchy w lokalnym repozytorium oraz wyświetlenia nazwy aktualnego brancha  
```bash  
git branch
``` 
### git checkout  
```bash  
git checkout <nazwa_brancha>        // przełączenie się na inną, istniejącą gałąź
git checkout  -b "<nazwa_brancha>"  // stworzenie nowego brancha na bazie aktualnego brancha i przełączenie się na niego
git checkout -                      // przełączenie się na wcześniej używanego brancha
git checkout <nazwa_pliku>          // zresetowanie zawartości brancha do tej, z ostatniego commita
```  

### git reset  
```bash  
git reset --hard // cofnięcie gałęzi do stanu z ostatniego commita
```  
# DevOps\GIT\003_Pushing_changes_to_remote.md

## Wypchanie zmian na serwer
### git add  
Dodanie plików do z working directory do staging area,  
```bash  
git add <nazwa_pliku> [<kolejne_nazwy_plików>]
git add --all
```  
### git commit  
Dodanie plików do z working directory do staging area,  
```bash  
git commit -m "<nazwa_commita>"   // tworzy commit z nadaną nazwą
git commit -am "<nazwa_commita>"  // dodaje wszystkie ZMIENIONE pliki na staging i tworzy commit z nadaną nazwą. NOWE pliki należy dodać do commita ręcznie przy użyciu git add
```  
### git push  
Wypychanie zmian na aktualnym branchu z lokalnego repozytorium do repozytorium centralnego   
```bash  
git push
```  
# DevOps\GIT\004_Pulling_changes_from_remote.md

## Pobieranie zmian z serwera
### git pull  
Aktualizowanie lokalnego repozytorium o nowe commity z repozytorium centralnego z aktualnego brancha   
```bash  
git pull
git pull --rebase
```  
### git fetch  
Aktualizowanie lokalnego repozytorium o nowe branche powstałe w repozytorium zewnętrznym  
```bash  
git fetch
```  
### git merge  
Ta komenda łączy wszystkie zmiany powstałe we wskazanej w komendzie gałęzi w jeden wspólny commit (merge commit) i dołącza je do brancha, na którym obecnie się znajdujemy, jako najnowszy commit.  
```bash  
git merge <nazwa-brancha>
```  
  
### git rebase  
Komenda zaciąga historię commitów oraz zmiany ze wskazanego brancha, a zmiany, które commity, które zostały w międzyczasie utworzone na obecnej gałęzi przesunięte są w historii commitów jako najnowsze  
```bash  
git rebase <nazwa-brancha>
```

### rebase czy merge?  
Aby zachować liniową historię commitów najlepiej zastosować podany zestaw komend przed zmergowaniem zmian na branch master. Mergując zmiany bez wcześniejszego wykonania rebase'a  tworzymy tzw. merge commita, który burzy liniową strukturę historii commitów i tworzy w niej rozgałęzienia, które trudniej potem rozwiązać.  
```bash  
git checkout feature-branch // przeniesienie na aktualnego brancha
git rebase master           // zaciągnięcie historii zmian z mastera do aktualnego brancha
git checkout master         // przeniesienie na aktualnego brancha
git merge feature-branch    // dodanie zmian z feature-brancha na branch master
```

# DevOps\GIT\005_Interactive_rebase.md

## Interaktywny rebase
### Uruchomienie interaktywnego rebase
Interaktywny rebase pozwala na edytowanie historii commitów, łączenie wielu commitów w jeden commit, usuwanie niechcianych commitów.
```bash  
git rebase -i <hash commita poprzedzającego commit od którego chcemy edytować historię>
```  
Po wykonaniu powyższej komendy znajdziemy się w interaktywnej powłoce, gdzie jest do wyboru kilka opcji. Aby przejść do trybu edycji należy nacisnąć **A**.

Na liście commitów na górze powłoki domyślnie ustawione są komendy **pick**, które pozostawiają commit w niezmienionej formie. Przykład:
```bash  
pick cd7ab52 Commit 1
pick xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
### Zmiana nazwy commita
Jeżeli chcemy zmienić nazwę któregoś z commitów komendę **pick** należy zamienić na komendę **reword** lub **r** i zatwierdzić zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
```bash  
pick cd7ab52 Commit 1
r xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
W nowym oknie wchodzimy do trybu edycji, podajemy nową nazwę commita i zatwierdzamy zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
### Łączenie commitów
Jeżeli chcemy połączyć wskazany commit z commitem znajdującym się powyżej, komendę **pick** należy zamienić na komendę **fixup** lub **f** i zatwierdzić zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
```bash  
pick cd7ab52 Commit 1
f xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
Frontend
========

# Frontend\JavaScript\001_Basics\001_Variables.md

### Zmienne
-   `var` - służy do definiowania globalnych zmiennych
```
var age = 20;
```

-   `let` - służy do definiowania zmiennych dla ograniczonego zakresu - danej funkcji lub pętli
```
let counter = 1;
```

-   `const` - służy do definiowania niezmiennych wartości
```
const PI = 3.14;
```
# Frontend\JavaScript\001_Basics\002_String_formatting.md

### Formatowanie stringów
```javascript
let number = 1
let formattedString = `Number: ${number}`
```
# Frontend\JavaScript\001_Basics\003_Ternary_operator.md

### Ternary Operator
Skrócony zapis bloku if - else. Przy jego użyciu taki zapis:
```js
if (a < b)  {        
    let output = a + b;    
} else if (a > b) {
    let output = a - b;    
} else {        
    let output = a * b;    
}
```
Można zastąpić takim zapisem:
```js
(a < b) ? a + b : a - b;
```
# Frontend\JavaScript\001_Basics\004_Object.md

### Object
Struktura podobna do słowników w Pythonie. Przykład użycia:
```javascript
let person = {
    first: 'Harry',
    last: 'Potter'
};
```
![Harry Potter](https://cs50.harvard.edu/web/2020/notes/5/images/console.png)
# Frontend\JavaScript\001_Basics\005_Functions.md

### Funkcje
Funkcje można zdefiniować na kilka sposobów:
* Funkcja nazwana
```javascript
function test(a, b){
	return a + b;
}
```
* Funkcja anonimowa (anonymous function)

Funkcję można również zdefiniować "w locie" - będzie ona wtedy wykorzystywana jedynie w miejscu jej zdefiniowania. Poniżej przykład użycia anonimowej funkcji w definicji eventListenera.
```javascript
let form = document.querySelector('form')
form.addEventListener('submit', function(e) {
		console.log('Submitted');
});
```
* Funkcja strzałkowa (arrow function)

Jeszcze prostszy sposób na zdefiniowanie funkcji. Znika potrzeba użycia słowa kluczowego **function**, jest ono zastąpione przez **=>**.
```javascript
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            document.querySelector("#hello").style.color = button.dataset.color;
        }
    });
});
```
# Frontend\JavaScript\001_Basics\006_map_filter_reduce.md

### map
```js
let fruits = ["pawpaw", "orange", "banana"];   

let mappedFruits = fruits.map(item => item + "s");    

console.log(mappedFruits); // ["pawpaws", "oranges", "bananas"]
```
### filter
```js
let fruits = ["pawpaw", "orange", "banana", "grape"];
    
let filteredFruits = fruits.filter(fruit => fruit.length > 5);

console.log(filteredFruits);  // ["pawpaw", "orange", "banana"]
```
### reduce
```js
let evenNumbers = [2, 4, 6, 8, 10]; 
    
evenNumbers.reduce((sum, current) => sum += current, 0);
```
# Frontend\JavaScript\002_DOM_operations\001_querySelector.md

### querySelector
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca pierwszy element pasujący do zapytania.
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let name = document.querySelector('#name');
```
Przykład użycia:
```javascript
// Zmiana koloru tła elementu o tagu "body" na czerwony
let body = document.querySelector('body');
body.style.backgroundColor = 'red';
```

### querySelectorAll
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca listę obiektów pasujących do zapytania,
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let buttons = document.querySelectorAll('button');
```



# Frontend\JavaScript\002_DOM_operations\002_addEventListener.md

### addEventListener
Pozwala na zdefiniowanie zachowania strony w momencie, gdy user wykona jakieś działanie, np. kliknie w odpowiedni element.
```javascript
// Kliknięcie elementu o id "name" powoduje zalogowanie do consoli słowa "CLICKED"
document.querySelector('#name').addEventListener('click', function()
	{
	    console.log('CLICKED');
	}
);
```

Przykład użycia:

```javascript
// Skrypt wykonany przy załadowaniu strony
document.addEventListener('DOMContentLoaded', function() {
    // Some code here
});
```


# Frontend\JavaScript\002_DOM_operations\003_dataset.md

### dataset
Specjalny rodzaj atrybutów dla elementów DOM.
```html
...
<body>
    <button data-color="red">Red</button>
    <button data-color="blue">Blue</button>
    <button data-color="green">Green</button>
</body>
...
```
Dostęp do wartości *color* każdego z buttonów można uzyskać w następujący sposób:
```javascript
document.querySelectorAll('button').forEach(function(button) {
    let color = button.dataset.color;
});
```
# Frontend\JavaScript\002_DOM_operations\004_fetch.md

### fetch
Pozwala na wykonanie zapytania pod wskazanym adresem URL.
```javascript
 fetch('https://api.exchangeratesapi.io/latest?base=USD')
 .then(response => response.json())
 .then(data => {
     console.log(data);
 });
```
# Frontend\JavaScript\002_DOM_operations\005_Local_storage.md

### Local storage
Dane składowane w oknie przeglądarki. Wykorzystuje dwie podstawowe funkcje:
-   `localStorage.getItem(key)`
-   `localStorage.setItem(key, value)`

# Frontend\React\001_Basics\001_Project_init.md

### Przygotowanie projektu
Żeby uruchomić aplikację reactową we własnym środowisku konieczne jest zainstalowanie [Node.js](https://nodejs.org/en).
Po jego instalacji w konsoli możliwe jest użycie polecenia, które zbuduje podstawowy schemat aplikacji.
```commandline
npx create-react-app <nazwa-aplikacji>
```
Gdy aplikcja jest już gotowa, możliwe jest jej uruchomienie na lokalnym serwerze:
```
  npm start
```
Tak przygotowany projekt pozwala na utworzenie single page app poprzez edycję pliku **nazwa-aplikacji/src/App.js**, którego zawartość jest eksportowana do **nazwa-aplikacji/src/index.js**, który to jest wykorzystwany w **nazwa-aplikacji/public/index.html**.


# Frontend\React\002_Components\001_Creating_component.md

### Tworzenie komponentów
Podstawowy element wykorzystywany w React'cie. Komponent to javascriptowa funkcja, która zwraca znaczniki HTML. Nie ma ograniczenia co do wielkości komponentu - może zwracać np. button (jak w przykładzie poniżej) lub nawet całą stronę.
```js
function MyButton() {  
	return (  
		<button>I'm a button</button>  
	);  
}
```
**WAŻNE:** Reactowe komponenty zawsze zaczynają się z dużej litery - pozwala to odróżnić je od zwykłych znaczników HTML.
# Frontend\React\002_Components\002_Nesting_components.md

### Zagnieżdżanie komponentów
Tak zadeklarowany komponent można zagnieździć w innym komponencie:
```js
export default function MyApp() {  
	return (  
		<div>  
			<h1>Welcome to my app</h1>  
			<MyButton />  
		</div>  
	);  
}
```
# Frontend\React\002_Components\003_className_in_component.md

### Nadawanie klas w komponentach
Aby zdefiniować klasę dla elementu w komponencie konieczne jest użycie **className** zamiast **class**.
```html
<img  className="avatar"  />
```
W kontekście nadawania stylów działanie **className** jest takie samo jak **class**
```css
/* In your CSS */  

.avatar {  
	border-radius: 50%;  
}
```
# Frontend\React\002_Components\004_Variables_displaying.md

### Wyświetlanie zmiennych
Aby zagnieździć wartość zmiennej w składniku komponentu umieszcza się taką zmienną w nawiasach klamrowych.
```js
const user = {  
  name: 'Hedy Lamarr',  
  imageUrl: 'https://i.imgur.com/yXOvdOSs.jpg',  
  imageSize: 90,  
};  
  
function App() {  
return (  
	<>  
		<h1>{user.name}</h1>  
		<img   
			className="avatar"   
			src={user.imageUrl}   
			alt={'Photo of ' + user.name}   
			style={{  
				width: user.imageSize,  
				height: user.imageSize  
			}}  
		/>  
	</>  
);  
}
```
# Frontend\React\003_Rendering\001_List_rendering.md

### Renderowanie list elementów
Aby wyświetlić listę elementów można przygotować przygotować taką listę elementów przy użyciu pętli for lub funkcji map(). Poniżej przykład zmapowania obiektów na reprezentujące je \<li>.
```js
const products = [  
  { title: 'Cabbage', isFruit: false, id: 1 },  
  { title: 'Garlic', isFruit: false, id: 2 },  
  { title: 'Apple', isFruit: true, id: 3 },  
];  
  
function App() {  
	const listItems = products.map(product =>  
		<li  
			key={product.id}  
			style={{  
				color: product.isFruit ? 'magenta' : 'darkgreen'  
			}}  
		>  
			{product.title}  
		</li>  
	);  

	return (  
		<ul>{listItems}</ul>  
	);  
}
```
**WAŻNE:** ważne zdefiniowanie atrybutu **key** w \<li> jako unikalnego identyfikatora dla elementu listy (np. id z bazy danych), ponieważ React wykorzystuje ten atrybut do operacji na wskazanym obiekcie.
# Frontend\React\003_Rendering\002_Conditional_rendering.md

### Renderowanie warunkowe
Elementy mogą być wyświetlane lub nie w zależności od sprawdzanych warunków. Poza tradycyjną konstrukcją if / else możliwe jest użycie typowych dla JavaScriptu skrótów:
* `{cond ? <A /> : <B />}`  => jeżeli `cond`, wyświetl `<A />`, w innym wypadku wyświetl `<B />`
* `{cond && <A />}`  => jeżeli `cond`, wyświetl `<A />`, w innym wypadku nie wyświetlaj niczego
# Frontend\React\004_Hooks\001_useState.md

### useState
Aby wykorzystać stan aplikacji i dynamiczne wyświetlanie jego zmian konieczne jest zaimportowanie hooka useState z biblioteki Reacta poprzez umieszczenie w pliku następującego polecenia:

```js
import {useState} from 'Notes/Frontend/React/React';
```
Utworzenie zmiennej odzwierciedlającej stan w aplikacji odbywa się poprzez następującą definicję:
```js
const [variable, setVariable] = useState(0);
```
Zmienna **variable** to zmienna zawierająca bieżący stan aplikacji (w przykładzie powyżej zdefiniowana z wartością 0), natomiast **setVariable** to funkcja pozwalająca na zmianę stanu zawartego w zmiennej **variable**. Przykładowo, chcąc zmienić wartość **variable** z 0 na 1 napiszemy:
```js
setVariable(1);
```
#### Stan pojedynczego komponentu
Stan może być zapamiętany w kontekście pojedynczego komponentu. W tym celu zmienna stanu oraz odpowiadająca jej funkcja aktualizująca muszą zostać zadeklarowane wewnątrz definicji komponentu. Poniżej przykład wyświetlenia dwóch buttonów z osobnymi licznikami kliknięć.

```js
import {useState} from 'Notes/Frontend/React/React';

function MyButton() {
    const [count, setCount] = useState(0);

    function handleClick() {
        setCount(count + 1);
    }

    return (
        <button onClick={handleClick}>
            Clicked {count} times
        </button>
    );
}

function App() {
    return (
        <div>
            <h1>Counters that update separately</h1>
            <MyButton/>
            <MyButton/>
        </div>
    );
}
```
#### Wspólny stan dla wielu komponentów
W celu współdzielenia stanu przez wiele komponentów konieczne jest umieszczenie definicji zmiennej zawierającej stan w komponencie zawierającym komponenty, które mają z tego wspólnego stanu korzystać. 
Chcąc, aby w przykładzie z punktu 4.1.1. oba buttony aktualizowały jeden, wspólny licznik konieczny będzie następujący refactoring:
```js
function MyButton({ count, onClick }) {  
  return (  
    <button onClick={onClick}>  
      Clicked {count} times  
    </button>  
  );  
}  
  
function App() {  
  const [count, setCount] = useState(0);  
  
  function handleClick() {  
    setCount(count + 1);  
  }  
  
  return (  
    <div>  
      <h1>Counters that update together</h1>  
      <MyButton count={count} onClick={handleClick} />  
      <MyButton count={count} onClick={handleClick} />  
    </div>  
  );
``` 
Definicja stanu została przeniesiona z komponentu MyButton do komponentu App, gdzie sama zmienna **count** i eventHandler **handleClick** są przekazywane do komponentów MyButton jako tzw. props.

