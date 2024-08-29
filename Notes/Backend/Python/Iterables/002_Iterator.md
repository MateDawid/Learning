# Iterator
Hermetyzuje strategię sekwencyjnego dostępu do elementów kompozytu, bez względu na rzeczywistą ich organizację. Jego zadanie polega na dostarczaniu kolejnych elementów według ustalonego wzorca.
```python
class Iterator:
	def __next__(self):
		return (...)
	def __iter__(self):
		return self # Obiekt iteratora musi mieć zdefiniowaną metodę __iter__, gdzie zwraca samego siebie

iterator = iter(iterable)

# Wywoływanie kolejnych elementów.
element_1 = next(iterator)
element_2 = next(iterator)
```
Gdy nie ma już obiektów do pobrania, przy kolejnej próbie użycia funkcji **next** wystąpi wyjątek *StopIteration*.

Iterator można utworzyć również z "wartownikiem", będącym wartością przerywającą iterację.

```python
# iterator = iter(callable, sentinel)

def function():
	return random.randrange(10)

list(iter(function, 5))
```