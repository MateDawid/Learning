# Custom user model

Source: https://testdriven.io/blog/django-custom-user-model

## Start project with custom User!
Do this on project init to omit problems in the future. In case you want to migrate to custom User model in existing project check [this link](https://testdriven.io/blog/django-custom-user-model-migration/).

## Base classes for custom User
Options:

**AbstractUser**: Use this option if you are happy with the existing fields on the user model and just want to remove the username field.

**AbstractBaseUser**: Use this option if you want to start from scratch by creating your own, completely new user model. 

## Custom User manager

Custom manager subclassing BaseUserManager, that uses email as the unique identifier instead of a username.

```python
# users/managers.py

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

## Custom User model

### AbstractUser - use predefined fields
* Set *username* field to None. 
* Add *email* field, make it unique and required, and mark it as *USERNAME_FIELD*. 
* Specify that all objects for the class come from the CustomUserManager

```python
# users/models.py

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
### AbstractBaseUser - add all fields manually
* Add fields *email*, *is_staff*, *is_active*, and *date_joined*.
* Mark *email* field as *USERNAME_FIELD*. 
* Specify that all objects for the class come from the CustomUserManager

## Settings
Add the following line to the settings.py file so that Django knows to use the new custom user class:

```python
# settings.py

AUTH_USER_MODEL = "users.CustomUser"
```

After that, make migrations and migrate changes to database.

## Forms
```python
# users/forms.py

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

## Admin
```python
# users/admin.py

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