# Deskryptor
Można go sobie wyobrazić jako property wielokrotnego użytku, które może być wykorzystywane w wielu klasach. Zgodnie z definicją, jest to klasa definiująca jedną z trzech magicznych metod: \_\_get__, \_\_set__, \_\_delete__. Występują szczególne przypadki: 
* data descriptor - definiuje wszystkie trzy metody
* non data descriptor - definiuje tylko metodę \_\_get__. Pozwalają na leniwą inicjalizację atrybutów w klasie

Pożej przykład zastosowania domknięcia wykorzystującego dekorator property do przypisania niezmiennych atrybutów w klasie.
```python
# Zwrócenie wartości atrybutu _attr przy próbie wyciągnięcia atrybutu poprzez Class.attr
def read_only(name):
	@property
	def getter(self):
		return getattr(self, '_' + name)
	return getter

class Person:
	name = read_only('name')
	married = read_only('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
Ten sam problem można rozwiązać przy użyciu deskryptora:
```python
class ReadOnly:
	def __init__(self, name)
		self.name = name
	
	def __get__(self, obj, cls):
		if obj is None:
			return self
		return getattr(obj, '_' + self.name)
	
	def __set__(self, obj, value):
		raise AttributeError

class Person:
	name = ReadOnly('name')
	married = ReadOnly('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 