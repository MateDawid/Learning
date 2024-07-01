# Testing

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#testing-2

## Organization

In our Django projects, we split our tests depending on the type of code they represent.

Meaning, we generally have tests for models, services, selectors & APIs / views.

The file structure usually looks like this:
```
project_name
├── app_name
│   ├── __init__.py
│   └── tests
│       ├── __init__.py
│       ├── factories.py
│       ├── models
│       │   └── __init__.py
│       │   └── test_some_model_name.py
│       ├── selectors
│       │   └── __init__.py
│       │   └── test_some_selector_name.py
│       └── services
│           ├── __init__.py
│           └── test_some_service_name.py
└── __init__.py
```

## Naming conventions
We follow 2 general naming conventions:

* The test file names should be ```test_the_name_of_the_thing_that_is_tested.py```
* The test case should be `class TheNameOfTheThingThatIsTestedTests(TestCase):`

For example, if we have:
```python
def a_very_neat_service(*args, **kwargs):
    pass
```
We are going to have the following for file name:
```python
project_name/app_name/tests/services/test_a_very_neat_service.py
```
And the following for test case:
```python
class AVeryNeatServiceTests(TestCase):
    pass
```
For tests of utility functions, we follow a similar pattern.

For example, if we have `project_name/common/utils.py`, then we are going to have `project_name/common/tests/test_utils.py` and place different test cases in that file.

If we are to split the utils.py module into submodules, the same will happen for the tests:
* project_name/common/utils/files.py
* project_name/common/tests/utils/test_files.py
We try to match the structure of our modules with the structure of their respective tests.