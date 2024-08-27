# HTTP Basic Authentication

Source: https://testdriven.io/blog/web-authentication-methods/#http-basic-authentication

## Intro

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

## Flow
![001_Flow.png](_images/001_Flow.png)
## Pros
* Since there aren't many operations going on, authentication can be faster with this method.
* Easy to implement.
* Supported by all major browsers.
## Cons
* Base64 is not the same as encryption. It's just another way to represent data. The base64 encoded string can easily be decoded since it's sent in plain text. This poor security feature calls for many types of attacks. Because of this, HTTPS/SSL is absolutely essential.
* Credentials must be sent with every request.
* Users can only be logged out by rewriting the credentials with an invalid one.