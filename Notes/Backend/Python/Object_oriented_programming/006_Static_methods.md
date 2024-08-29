# Metody statyczne
Nie posiadają odniesienia ani do danego obiektu, ani do samej klasy - zachowują się bardziej jak zwykłe funkcje, niż metody. Z optymalizacyjnego punktu widzenia nie są one dobrym rozwiązaniem, ponieważ wiążę się z dodatkowym kosztem ze względu na przeglądanie przez Pythona przestrzeni nazw w trakcie działania programu. Jedynym logicznym zastosowaniem @staticmethod jest ich pogrupowanie pod jedną, wspólną przestrzenią nazw klasy
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@staticmethod
	def blend(color1, color2, alpha=0.5):
		return color1*alpha + color2*(1-alpha)
		
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))
	
	def __mul__(self, scalar):
		return Color(*[x*scalar for x in self])
	
	def __add__(self, other):
		return Color(*[sum(x) for x in zip(self, other)])
```
