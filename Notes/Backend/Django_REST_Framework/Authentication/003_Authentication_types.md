# Authentication types

> Sources: https://testdriven.io/courses/taxi-react/authentication/

Here's what you need to know: Every authentication method requires the client to send a user's credentials to the server at least once.

1. In the case of basic authentication, the client must send the user's credentials over the wire with every request. This stipulation gives bad actors more opportunities to steal a user's password.
2. Remote authentication passes the responsibility of verifying a user's identity to a third party. Most of the time, the third party is a centralized single sign-on server that supports a protocol such as LDAP, CAS, or SAML.
3. With both session and token authentication, the client exchanges a user's credentials for an encrypted string. The client sends the secure string back to the server in subsequent requests to validate the user's identity. The server stores a record that associates the user with the secure string, usually in a database table. When the user logs out of the application, the server deletes that record, invalidating any additional attempts to use the old string for authentication.

The method of exchanging a secure string between the client and the server is important.

1. Session authentication passes the string back and forth using cookies.
2. Token authentication requires the client to explicitly send the string in the request, typically in an authentication header.

Any of these authentication methods are straightforward to use over HTTP, but some of them are difficult to use with WebSockets. The JavaScript WebSocket API supports cookies but does not support custom headers. Session authentication can work nicely here, but since we're designing this application to be run on a mobile device, token authentication is more desirable. We'll have to find a creative way to send the token over a WebSocket connection.

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