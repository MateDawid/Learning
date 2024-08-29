# Moduł operator

W celu ułatwienia przekazywania klucza sortowania do metody sorted można posłużyć się modułem operator.

# operator.itemgetter
```python 
from operator import *

people = [
	('Jan', 'Kowalski'),
	('Anna', 'Woźniak'),
	('Anna', 'Nowak')
]

sorted(people, key=itemgetter(0, 1)) # itemgetter wyciąga elementy z kolejno z indeksów 0 i 1 w formie krotki dla każdego z obiektów listy people. Lista jest posortowana najpierw względem pierwszej podanej wartości, a następnie drugiej
```
# operator.attrgetter
```python 
from operator import *
from collections import namedtuple

Person = namedtuple('Person', 'first_name last_name')

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=attrgetter('first_name', 'last_name')) # attrgetter wyciąga atrybuty kolejno 'first_name' i 'last_name' i sortuje listę obiektów na ich podstawie
```
# operator.methodcaller
```python 
from operator import *
from collections import namedtuple

class Person(namedtuple('Person', 'first_name last_name')):
	def get_length(self):
		return len(str(self))

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=methodcaller('get_length')) # methodcaller sortuje listę na podstawie wartości zwróconych przez metodę, której nazwa przekazana jest w argumencie
```