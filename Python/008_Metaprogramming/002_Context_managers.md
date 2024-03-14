# Menedżer kontekstu
Obiekt implementujący interfejs składający się z dwóch magicznych metod - \_\_enter__ oraz \_\_exit__, które umożliwiają jego użycie w konstrukcji with. Menedżer kontekstu przydaje się w takim razie do zarządzania stanem, który musi zostać najpierw zainicjowany, a następnie uwolniony, żeby nie dopuścić do wycieków pamięci. Menedżer kontekstu można zdefiniować klasowo albo funkcyjnie.
```python
from time import time

class MockedTime:
	def __enter__(self):
		# tymczasowe nadpisanie funkcji time
		global time
		self._time = time
		time = lambda: 42
	
	def __exit__(self, exception_class, exception, traceback):
		# powrót do domyślnej funkcji time
		global time
		time = self._time

with MockedTime():
	print(time())
print(time())
```
```python
from time import time, sleep

class Timed:
	def __enter__(self):
		self.t1 = time()
		return self # pozwala na przypisanie menedżera do zmiennej poprzez słówo "as" w konstukcji "with"
	
	def __exit__(self, *args):
		self.t2 = time()
	
	@property
	def delta(self):
		return self.t2 - self.t1

with Timed() as timed:
	sleep(0.5)

print(timed.delta)
```
Do utworzenia menedżera kontekstu jako funkcji służy biblioteka contextlib.
```python
from contextlib import contextmanager

@contextmanager
def logging():
	print('__enter__')
	try:
		yield
	finally:
		print('__exit__')

with logging() as value:
	print('The value is:', value)
```
Instrukcja yield dzieli zawiesza działanie funkcji i dzieli ją na dwie części. Pierwsza część odpowiada instrukcji \_\_enter__, w której dokonuje się inicjalizacji. Druga część (za yield) odpowiada za to instukcji \_\_exit__. Konieczne jest opakowanie słówa kluczowego yield blokiem try/finally, ponieważ w innym razie, w przypadku wystąpienia wyjątku nie doszłoby do "zamknięcia" menedżera kontekstu.
