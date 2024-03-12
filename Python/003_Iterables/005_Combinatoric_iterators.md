# Iteratory kombinatoryczne
## product
Iloczyn kartezjański dwóch lub więcej zbiorów (wszystkie możliwe kombinacje wartości).
```python 
from itertools import *


colors = {'black', 'white'}
sizes = {'S', 'M', 'L', 'XL'}
materials = {'cotton', 'polyester', 'lycra'}

for color, size, material in product(colors, sizes, materials):
	print(color, size, material)
	# black S lycra
	# black S cotton
	# ...
	# black M lycra
	# ...
	# white S lycra
	...

# Kombinacja kilku wartości z tego samego zakresu
list(product(range(10), repeat=4))
# [(0, 0, 0, 0),
# (0, 0, 0, 1),
...
# (9, 9, 9, 9)]
```
## permutations
Możliwe permutacje dla podanego zbioru (możliwe kolejności obiektów w zbiorze).
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in permutations(horses):
	for i, horse in enumerate(outcome, 1):
		print(i, horse)
	print()

# 1 Duke
# 2 Coco
# 3 Star
# 4 Dolly
# 5 Gypsy
# 
# 1 Duke
# 2 Coco
...
```
Możliwe jest również uzyskanie n-elementowych wariacji bez powtórzeń - tutaj w celu uzyskania pierwszych trzech miejsc na podium.
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in permutations(horses, 3):
	for i, horse in enumerate(outcome, 1):
		print(i, horse)
	print()
# 1 Duke
# 2 Coco
# 3 Star
...
```
## combinations
n-elementowe unikalne podzbiory bez względu na kolejność elementów.
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in combinations(horses, 3):
	print(outcome)
# 1 Duke
# 2 Coco
# 3 Star
...
```