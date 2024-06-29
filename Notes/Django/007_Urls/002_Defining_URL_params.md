# Defining URL params

Source: https://pogromcykodu.pl/stworz-wlasny-walidator-url/

```python
urlpatterns = {
    path('article/<int:pk>', ArticleDetailsView.as_view()),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', ArticlesListView.as_view()), 
}

```

## URL variables types:
* int – integer -> `<int:pk>`
* str – non-empty string without '/' sign -> `<str:name>`
* slug – string containint letters, numbers, '-' and '_' -> `<slug:slug>`
* uuid – string containing groups of letters divided by '=' -> `<uuid:id>`
* path – non-empty string with '/' sign as path separator -> `<path:file_path>`