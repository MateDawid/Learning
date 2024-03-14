# Metaklasy
Najprostszym przykładem metaklasy jest type - jest on metaklasą dla wszystkich podstawowych (i nie tylko) typów w Pythonie np. int, float itp. Używając type można także zdefiniować nową klasę. Poniżej przykład zdefiniowania metaklasy przy użyciu funkcji.
```python
def n_tuple(name, bases, attrs, n):
	def __new__(cls, *args):
		if len(args) != n:
			raise TypeError(f'expected {n} but got {len(args)} arguments')
		return tuple(args)
	return type(f'Tuple {n}', (tuple,), {'__new__': __new__})

class Point(metaclass=n_tuple, n=2):
	pass

Point(1, 2)
```
Metaklasę można również zdefiniować przy użyciu klasy.
```python
class Meta(type):
	def __new__(cls, name, bases, dct):
		x = super().__new__(cls, name, bases, dct)
		x.attr = 100
		return x

class Foo(metaclass=Meta):
	pass

Foo.attr # 100
```