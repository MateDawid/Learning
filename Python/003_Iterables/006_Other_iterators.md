# Iteratory pozostałe
## chain
Pozwala na iterowanie po kilku sekwencjach na raz. Po wyczerpaniu elementów w sekwencji chain przechodzi do pobierania elementów z kolejnej z nich.

```python 
from itertools import *

a = [1, 2, 3]
b = ['lorem', 'ipsum']
c = list('abcd')

for x in chain(a, b, c):
	print(x)
```
## zip
Wbudowana funcja, pozwalająca na iterowanie po kilku listach jednocześnie. Ilość wynikowych elementów determinuje długość najkrótszej z sekwencji.
```python 
from itertools import *

a = [1, 2, 3]
b = ['lorem', 'ipsum']
c = list('abcd')

for x in zip(a, b, c):
	print(x)

# (1, 'lorem', 'a')
# (2, 'ipsum', 'b')
```
Sekwencje tak utworzonych tupli można też odpakować przy użyciu zip.
```python 
from itertools import *

zipped = [(1, 'a'), (2, 'b')]
x, y = zip(*zipped)
print(x)
print(y)
# (1, 2)
# ('a', 'b')
```
## groupby
Pozwala na grupowanie danych po wskazanym kluczu
```python 
from itertools import *

expenses = [
	(500, 'ZUS', 'firma'),
	(100, 'księgowa', 'firma'),
	(400, 'OC', 'samochód'),
	(60, 'kino', 'rozrywka'),
	(200, 'paliwo', 'samochód'),
	(700, 'drukarka', 'firma'),
]

category = lambda x: x[-1]

for key, values in groupby(sorted(expenses, key=category), key=category):
	print(key, list(values))

# firma [(500, 'ZUS', 'firma'), ...]
# rozrywka [...]
# samochód [...]
```
## islice
Pozwala na uzyskanie wycinka z iteratora.
```python 
from itertools import *

it = range(int(1e6))
# Wycinek 10 pierwszych elementów z iteratora it zawierającego milion elementów
list(islice(it, 10)
```
## Inne metody
* combinations_with_replacement
* accumulate
* count
* cycle
* chain
* compress
* dropwhile
* filterfalse
* product
* repeat
* starmap
* takewhile
* tee
* zip_longest