# Credentials-based Authentication

Source: https://testdriven.io/blog/django-rest-auth

## Settings
```python
# core/settings.py

INSTALLED_APPS = [
    # ...
    "rest_framework",
    "rest_framework.authtoken",
]
```

The authtoken app is required since we'll use TokenAuthentication instead of Django's default SessionAuthentication. Token authentication is a simple token-based HTTP authentication scheme that is appropriate for client-server setups.
```python
# settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}
```

## django-allauth

```python
# core/settings.py

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
# core/settings.py

SITE_ID = 1  # make sure SITE_ID is set
```
## dj-rest-auth
```commandline
pip install "dj-rest-auth[with_social]==4.0.0"
```
We need to use the with_social specifier since we want to enable the standard registration process. Additionally, we'll utilize this package later when we enable social authentication.
```python
# core/settings.py

INSTALLED_APPS = [
    # ...
    "dj_rest_auth",
    "dj_rest_auth.registration",
]
```
Update authentication/urls.py like so:
```python
# authentication/urls.py

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
## Testing

### #Register
Then, to create an account run the following in a new terminal window:
```commandline
$ curl -XPOST -H "Content-type: application/json" -d '{
      "username": "user1",
      "password1": "complexpassword123",
      "password2": "complexpassword123"
  }' 'http://localhost:8000/api/auth/register/' | jq
```
By default, you'll get an empty response.

### Login
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
### User Details
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
### Logout
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
