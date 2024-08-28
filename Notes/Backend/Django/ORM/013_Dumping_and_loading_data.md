# Dumping and loading data

Source: https://testdriven.io/courses/django-rest-framework/multiple-lists/#H-1-populating-the-new-database

Dumping data to file:
```commandline
// python manage.py dumpdata app_name.model app_name.model > file_path
python manage.py dumpdata shopping_list.shoppinglist shopping_list.shoppingitem > shopping_list/fixtures/initial_shopping_lists_with_items.json
```


Loading data from file:
```commandline
// python manage.py loaddata file_path
python manage.py loaddata initial_shopping_lists_with_items.json
```