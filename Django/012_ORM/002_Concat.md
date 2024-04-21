# Concat()

Source: https://pogromcykodu.pl/django-orm-w-akcji-wyrazenie-f/

## Joining same Field types

```python
from django.db.models import F, Value
from django.db.models.functions import Concat
from employees.models import Employee

employees = Employee.objects.annotate(position_extra=Concat(Value("Senior "), F("position"))).all()

print(employees[0].position) # Developer
print(employees[0].position_extra) # Senior Developer 
```

> String values have to be "packed" with Value() to properly perform database operations.

## Joining CharField and TextField with Concat()

To join CharField and TextField it's needed to provide **output_field**, to specify which type of field we need to return.

```python
# first_name -> CharField, 
# last_name -> TextField

employees = Employee.objects.annotate(full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())).all()
print(employees[0].first_name) # Jan
print(employees[0].last_name) # Kowalski
print(employees[0].full_name) # Jan Kowalski 
```
