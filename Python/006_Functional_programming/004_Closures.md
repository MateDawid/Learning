# Domknięcia
Zapamiętuje wartości tzw. zmiennych wolnych (nonlocal) w swoim zasięgu leksykalnym. Domknięcia pozwalają dołączać pewien stan do funkcji, a także metody manipulowania tym stanem, jak np, ze zmienną color i metodą set_color z przykładu poniżej. Domknięcia są stosowane np. przy tworzeniu dekoratorów.
```python
def tag(name):
	color = 'black'
	def wrap(text):
		return f'<{name} style="color: {color}">{text}</{name}>'
	def set_color(value):
		nonlocal color
		color = value
	wrap.set_color = set_color
	return wrap
p = tag('p')
p('Python')
```