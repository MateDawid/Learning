# Plik conftest.py
Plik conftest.py to plik konfiguracyjny dla testów pytestowych, gdzie można np:
*  Składować wielokrotnie używane fixtury, które będą automatycznie wykryte przez testy zdefiniowane w innych plikach.
* Ustalić czynności, które mają zostać wykonane przed wszystkimi testami, np:
```python
def pytest_runtest_setup():  
	# Funkcja wykonana przed każdym testem  
	print('Start test')
```
