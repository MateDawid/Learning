# Iteratory nieskończone
```python 
from itertools import *

# Kolejne wartości liczbowe
for i in count(10, 1):
	print(i)

# 10
# 11
# 12
# ...

# Kolejne wartości z listy podawane cyklicznie
for i in cycle(['spring', 'summer', 'fall', 'winter']):
	print(i)

# Powtórzenie tej samej wartości podaną ilość razy, lub w nieskończoność
for i in repeat('hello', 3):
	print(i)
```
