# Funkcje cząstkowe
Funkcje wykonujące działanie innej funkcji, ale z mniejszą wymaganą do podania liczbą argumentów.

```python
from functools import partial

def quadratic(x, a, b, c):
	return a*x**2 + b*x + c

# Funkcja cząstkowa - zapis 1
def y(x):
	return quadratic(x, 3, 1, -4)

# Funkcja cząstkowa - zapis 2
y = partial(quadratic, a=3, b=1, c=-4)
```