# Service naming conventions

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#naming-convention

Naming convention depends on your taste. It pays off to have something consistent throughout a project.

If we take the example above, our service is named user_create. The pattern is - <entity>_<action>.

This is what we prefer in HackSoft's projects. This seems odd at first, but it has few nice features:

* Namespacing. It's easy to spot all services starting with user_ and it's a good idea to put them in a users.py module.
* Greppability. Or in other words, if you want to see all actions for a specific entity, just grep for user_.