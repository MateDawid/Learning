# Serializing

Source: https://testdriven.io/courses/django-rest-framework/getting-started/#H-2-serializers

While working with Django, you tend to use complex data types and structures, like model instances. Since those are specific to Django, a client wouldn't know what to do with it. So, complex, Django-specific data structures need to be converted into something less complex that a client knows how to work with. That's what serializers are for. They convert complex data structures to native Python data types. Native data types can then be easily converted to content types, like JSON and XML, that other computers or systems can read and understand:

Django QuerySets -> Python dictionaries -> JSON

This also happens vice versa: Parsed data is deserialized into complex data types:

JSON -> Python dictionaries -> Django QuerySets

While deserializing the data, serializers also perform validation.

Generally, you write your serializers in a serializers.py file. If it becomes too big, you can restructure it into a separate Python package.

