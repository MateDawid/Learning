# Przeciążanie funkcji
Python nie obsługuje przeciążania funkcji i metod, ale można za to dostosować działanie funkcji w zależności od przyjętych przez nią argumentów. Najprościej zrobić to przez użycie isinstance, ale jest to antywzorzec. Zamiast tego można wykorzystać metodę singledispatch.
```python
from functools import singledispatch

# Zdefiniowanie wzorca funkcji
@singledispatch
def pretty_print(x):
	print(x)

# Zarejestrowanie specjalnego działania funkcji po podaniu jej listy oraz tupli jako argumentu
@pretty_print.register(list)
@pretty_print.register(tuple)
def _(items):
	for i, value in enumerate(items):
		print(f'[{i}] = {value}')
```

Powyższe rozwiązanie nie zadziała dla metod w klasie oraz nie obsługuje więcej niż jednego argumentu. Aby rozwiązać ten drugi problem można skorzystać z zewnętrznej biblioteki multipledispatch.

```python
from multipledispatch import dispatch

@dispatch(int, int)
def add(x, y):
	return x + y

@dispatch(object, object)
def add(x, y):
	return f'{x} + {y}'
```