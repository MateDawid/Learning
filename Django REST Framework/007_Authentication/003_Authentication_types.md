# Authentication types
## BasicAuthentication

Username + password (base64 encoded)

```python
# settings/core.py

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

## SessionAuthentication

Cookie files stored in browser session after first authentication.

```python
# settings/core.py

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

## TokenAuthentication

Using token generated with single username & password authentication.

```python
# settings/core.py
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

## RemoteUserAuthentication

Rarely used, mostly for intranet sites.

```python
# settings/core.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.RemoteUserAuthentication",
    ]
}
```

## JWTAuthentication

JSON Web Token generated with djangorestframework-simplejwt package.

jwt.io - site to destructuring  JWT token

```python
# settings/core.py

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