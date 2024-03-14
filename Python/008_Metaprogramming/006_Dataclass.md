# Dataclass
Chcąc uniknąć żmudnego definiowania klas można zastosować mechanizm dataclass. W wyniku takiego zabiegu można zastąpić taką typową klasę:
```python
class Person:
	def __init__(self, name, age, married=False):
		self.name = name
		self.age = age
		self.married = married
```
Taką klasą:
```python
def dataclass(cls):
	def __init__(self, *args, **kwargs):
		# Zapisanie w kwargs argumentów przekazanych przez args zmapowanych przy użyciu cls.__annotations__
		kwargs.update(zip(cls.__annotations__, args))
		# Zapisanie zaktualizowanych kwargs w słowniku obiektu
		self.__dict__.update(kwargs)
	cls.__init__ = __init__
	return cls


@dataclass
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
Od Pythona 3.7. dostępny jest bardziej rozbudowany dekorator spełniający tę samą funkcję, dlatego finalnie taka klasa wyglądałaby tak:
```python
from dataclasses import dataclass

@dataclass
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
Domyślnie klasy udekorowane przez @dataclass są mutowalne, natomiast w celu "zamrożenia" ich wartości stosuje się następujący zapis:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
