# Service naming conventions

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
