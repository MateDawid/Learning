#  \_\_new__
Metoda magiczna wywoływana przed \_\_init__. Jest to metoda klasowa zwracająca nowy obiekt klasy. Poniżej przykład definicji Singletona.
```python
class Singleton:
	instance = None
	def __new__(cls):
		if Singleton.instance is None:
			Singleton.instance = super().__new__(cls)
		return Singleton.instance

a = Singleton()
b = Singleton()

a is b, id(a) == id(b) # (True, True), obie zmienne wskazują na tę samą instancję obiektu
```