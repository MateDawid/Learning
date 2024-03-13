# Iterable
Kompozyt zdolny do zwracania swoich elementów w pętli for. Są to np. typy sekwencyjne (listy, krotki, stringi), dict, set, file, itp.
```python
class Iterable:
	def __getitem__(self, key):
		(...)
	def __len__(self):
		return (...)

iterable[123]
iterable['foobar']
```
Dla bardziej skomplikowanej logiki iterowania definiuje się metodę **\_\_iter\_\_**
```python
class Iterable:
	(...)
	def __iter__(self):
		return Iterator(...)

# Wywołanie metody __iter__ obiektu Iterable w celu utworzenia iteratora 
iterator = iter(iterable)
```