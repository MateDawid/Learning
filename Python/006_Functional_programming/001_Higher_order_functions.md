# Funkcje wyższego rzędu (Higher order functions)
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