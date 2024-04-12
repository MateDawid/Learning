# Email Verification and Password Reset

Source: https://testdriven.io/blog/django-rest-auth/#email-verification-and-password-reset

## SMTP Settings

You can use your own SMTP server or utilize Brevo (formerly SendInBlue), Mailgun, SendGrid, or a similar service. I suggest you go with Brevo since they're relatively cheap and allow you to send a decent amount of emails daily (for free).

To configure SMTP, add the following to core/settings.py:
```python
# core/settings.py

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "<your email host>"                    # smtp-relay.sendinblue.com
EMAIL_USE_TLS = False                               # False
EMAIL_PORT = "<your email port>"                    # 587
EMAIL_HOST_USER = "<your email user>"               # your email address
EMAIL_HOST_PASSWORD = "<your email password>"       # your password
DEFAULT_FROM_EMAIL = "<your default from email>"    # email ending with @sendinblue.com
```

## Email verification and password reset

Add the following django-allauth settings to core/settings.py:
```python
# core/settings.py

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
# core/settings.py

# <EMAIL_CONFIRM_REDIRECT_BASE_URL>/<key>
EMAIL_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/email/confirm/"

# <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uidb64>/<token>/
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/password-reset/confirm/"
```
Make sure to include the trailing slash / at the end of the URLs.

Next, add the following two views to authentication/views.py:
```python
# authentication/views.py

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
# authentication/urls.py

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
## Testing
### Register
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
### Verify Email
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

### Password Reset
To request a new password, you need to POST to /api/auth/password/reset/ like so:
```
$ curl -XPOST -H "Content-type: application/json" -d '{
      "email": "<your email address>"
  }' 'http://localhost:8000/api/auth/password/reset/' | jq
```
After you send the request you'll receive aa email.