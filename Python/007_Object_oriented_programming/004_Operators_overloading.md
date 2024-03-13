# Przeciążanie operatorów
Przykład przeciążania operatora dodawania i dodawania prawostronnego klasy namedtuple.

```python
from collections import namedtuple

class Vector(namedtuple('Vector', 'x y')):
	def __add__(self, other):
		if isinstance(other, Vector):
			return Vector(*map(sum, zip(self, other)))
		elif isinstance(other, int):
			return Vector(self.x + other, self.y + other)
	
	def __radd__(self, other):
		return self + other
```

# __repr__ i __str__
Metoda \_\_str__ powinna zwracać reprezentację obiektu do czytania przez ludzi, natomiast metoda \_\_repr__ powinna zawierać zapis (najlepiej kod Pythona) umożliwiający odtworzenie danego obiektu po wklejeniu do funkcji eval.
```python
class Vector:
	def __init__(self, x, y)
		self.x, self.y = x, y
	
	def __str__(self):
		return f'A vector of {self.x}, {self.y}'
	
	def __repr__(self):
		return f'Vector({self.x}, {self.y})'

a = Vector(3, -4)
str(a) # 'A vector of 3, -4'
b = eval(repr(a)) # Nowa instancja wektora Vector(3, -4)
```