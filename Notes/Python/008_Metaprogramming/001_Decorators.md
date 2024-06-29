# Dekoratory
Funkcja, przyjmująca jako argument funkcję i zwracająca funkcję. 
```python
def password():
	return 'top_s3cret'

def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

encrypted_password = encrypted(password)
encrypted_password()
```
Powyższy zapis można skrócić do następującego:
```python
def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

@encrypted
def password():
	return 'top_s3cret'

password()
```
Jednym z głównych celów zastosowania dekoratorów jest memoizacja, czyli cache'owania wyników funkcji w celu przyspieszenia obliczeń. Poniżej przykład zastosowania dekoratora cache'ującego wyniki rekurencyjnych wyników wywołań wyliczających składniki ciągu Fibonacciego. 
```python
# import functools
def cache(function):
	history = {}
	def wrapper(n):
		if n not in history:
			history[n] = function(n)
		return history[n]
	return wrapper
	
# @functools.lru_cache(maxsize=128)
@cache
def fib(n):
	return 1 if n < 2 else fib(n-2) + fin(n-1)
```
Dekoratory mogą też przyjmować więcej parametrów niż samą dekorowaną funkcję, ale wymaga to dodatkowego poziomu zagnieżdżenia.
```python
import functools

def ignore(ExceptionClass):
	def decorator(function):
		@functools.wraps(function) # pozwala na przekazanie metadanych (np. __name__) funkcji w argumencie do dekorowanej funkcji
		def wrapper(*args, **kwargs):
			try:
				return function(*args, **kwargs)
			except ExceptionClass as ex:
				pass
		return wrapper
	return decorator

@ignore(ZeroDivisionError)
def divide(a, b):
	return a / b
```