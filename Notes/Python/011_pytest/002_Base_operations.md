# Podstawowe operacje
Żeby zdefiniować test konieczne jest utworzenie funkcji rozpoczynającej się od słowa "test". Przykład:
```python
def test_sum() -> None:  
    a = 1
    b = 2  
    assert a + b == 3
```
Uruchomienie testów w bieżącym katalogu:
```commandline
pytest
```
Uruchomienie sprawdzenia pokrycia kodu testami:
```commandline
pytest --cov
```
Raport o pokryciu testami i ze wskazaniem nieprzetestowanych fragmentów kodu:
```commandline
coverage html
```
# Uruchomienie testów
W celu uruchomienia napisanych testów w konsoli należy wpisać następującą komendę:
```
py.test
```