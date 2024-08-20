# PathConverters

Source: https://pogromcykodu.pl/stworz-wlasny-walidator-url/

## Default URL converters:

```python
path('article/<int:pk>', ArticleDetailsView.as_view()),
```

* int – IntConverter
* str – StringConverter
* slug – SlugConverter
* uuid – UUIDConverter 
* path – PathConverter

## Example Converter

```python
class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
```

## Exceptions

* ValueError - on invalid value in `to_python` method
* NoReverseMatch - on invalid value in `to_url` method

## Custom Converter

```python
class YearConverter(IntConverter):

    def to_python(self, value):
        value = int(value)
        if value >= 1996 and value <= 2020:
            return value
        raise ValueError 
```

```python
# urls.py

register_converter(YearConverter, 'yyyy')

...

urlpatterns = {
    path('articles/<yyyy:year>', ArticlesListView.as_view()) 
}
```