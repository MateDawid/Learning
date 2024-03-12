# Dekoratory
```python
def add_stars(function):     # definicja dekoratora niczym nie różni się od definicji zwykłej funkcji
    def decorated_function():   # wewnątrz dekoratowa tworzymy WEWNĘTRZNĄ funkcję, w której udekorujemy funkcję pobraną jako argument
        print("***")             # dekorowanie funkcji
        function()               # wywołanie funkcji będącej argumentem dekoratora
        print("***")             # dekorowanie funkcji
    return decorated_function    # zwrócenie funkcji WEWNĘTRZNEJ, w której udekorowano funkcję będącą argumentem dekoratora

@add_stars                       # zapis @add_stars BEZPOŚREDNIO nad definicją funkcji f() powoduje, że funkcja f() zostaje udekorowana
def f():                         # definicja funkcji f()
    print("Cześć, jestem f()")
```