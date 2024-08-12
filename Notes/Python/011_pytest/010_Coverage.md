# Coverage

Source: https://testdriven.io/courses/django-rest-framework/full-test-coverage/#H-11-test-coverage

Install the pytest-cov plugin:

```commandline
(venv)$ pip install pytest-cov==5.0.0
```

To use, you can simply run the following command:
```commandline
(venv)$ python -m pytest --cov=shopping_list shopping_list/tests/
```

Notes:
* --cov tells pytest-cov which module you want to test.
* The second argument tells pytest-cov which test suite you want to run (it needs to be a full path).

```commandline
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
shopping_list/__init__.py                      0      0   100%
shopping_list/admin.py                         4      0   100%
shopping_list/api/__init__.py                  0      0   100%
shopping_list/api/serializers.py              15      0   100%
shopping_list/api/views.py                    16      0   100%
shopping_list/apps.py                          4      0   100%
shopping_list/migrations/0001_initial.py       7      0   100%
shopping_list/migrations/__init__.py           0      0   100%
shopping_list/models.py                       14      2    86%
shopping_list/tests/__init__.py                0      0   100%
shopping_list/tests/conftest.py                9      0   100%
shopping_list/tests/tests.py                 149      0   100%
shopping_list/urls.py                          3      0   100%
--------------------------------------------------------------
TOTAL                                        221      2    99%
```

There's a command that adds the line numbers that don't have code coverage to the report:

```commandline
(venv)$ python -m pytest --cov-report term-missing --cov=shopping_list
```