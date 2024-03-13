# Zasięg zmiennych
Wartości zmiennych wyszukiwane są w kolejności LEGB - local, enclosed, global, built-in.
```python
%reset -f

x = 'global'

def outer():
	x = 'enclosed'
	def inner():
		x = 'local'
		print(x)
	inner()
	print(x)

outer()
print(x)

# local
# enclosed
# global
```