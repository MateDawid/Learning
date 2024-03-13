# Metody klasowe
Metoda klasowa to taka, która zawiera odwołanie nie do konkretnej instancji obiektu, ale do samej klasy. Może być wywoływana bez inicjowania obiektu.
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@classmethod
	def monaco_blue(cls):
		return cls(0.2, 0.5, 0.75)
		
	@classmethod
	def exotic_red(cls):
		return cls(1, 0, 0)
	
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))

Color.monaco_blue() # zwraca obiekt z metody klasowej Color(0.2, 0.5, 0.75)
```