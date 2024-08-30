# Higher order functions

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150904384/posts/2160071945
Functions that may take other function as an argument and/or return function as a return value.

```python
# This is higher-order function
def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")


def is_eligible_for_promotion(customer: Customer) -> bool:
    return customer.age >= 50


def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    send_email_promotion(customers, is_eligible_for_promotion)
    # We can use lambda function also
    # send_email_promotion(customers, lambda customer: customer.age >= 50)
```

## map
Wykonuje wskazaną funkcję na każdym elemencie podanej sekwencji i zwraca listę wyników tej funkcji
```python 
# Zwraca iterator pozycji poszczególnych elementów stringa w Unicode
map(ord, 'zażółć gęślą jaźń') 
```
## filter
Filtruje sekwencje bazując podanej funkcji.
```python 
filter(str.isupper, 'Hello World') 
```
## functools.reduce
Iteruje po elementach sekwencji i redukuje ją do pojedynczej wartości.
**Przykład 1: Sumowanie liczb**
```python
import operator
from functools import reduce

numbers = [42, 15, 2, 33]

# Pierwsza wartość funkcji to tzw. akumulator, na którym wykonywane są operacje bazujące na drugim argumencie
def f(subtotal, number):
	return subtotal + number

#reduce(f, numbers)
reduce(operator.add, numbers)
```
**Przykład 2: Grupowanie liczb parzystych i nieparzystych**
```python
import operator
from functools import reduce

numbers = [42, 15, 2, 33]

def f(grouped, number):
	key = 'even' if number % 2 == 0 else 'odd'
	grouped[key].append(number)
	return grouped

reduce(f, numbers, {'even': [], 'odd': []})
```