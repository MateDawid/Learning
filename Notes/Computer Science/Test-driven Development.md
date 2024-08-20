# Test-Driven Development

Source: https://testdriven.io/courses/django-rest-framework/tdd-search-filtering/#H-0-test-driven-development

[Test-driven Development](https://testdriven.io/test-driven-development/) (abbreviated TDD) is a methodology in software development where you write a test before a particular piece of code is implemented.

With TDD, you use the following cycle:

RED - write a failing test
GREEN - write the simplest piece of code that will get the test to pass
REFACTOR - improve the code while keeping the test green (passing)
Although confusing and time-consuming at first, once you get a grip on TDD, your development process will be quicker and less prone to bugs.

A straightforward example of TDD would be a function that sums up two numbers.

Start with a test:
```python
def test_sum_two_numbers():
    result = sum_two_numbers(2, 3)

    assert result == 5
```
Run the test to ensure it fails (RED).

After that, you'd write the simplest piece of code that will provide the desired result (GREEN):

```python
def sum_two_numbers(x, y):
    return 5
```

This code accomplishes what we wanted, but it can clearly be improved (REFACTOR):

```python
def sum_two_numbers(x, y):
    return x + y
```  
