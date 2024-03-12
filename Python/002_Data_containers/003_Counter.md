# Counter
Zlicza ilość wystąpień elementów w sekwencji.
```python
from collections import Counter

c = Counter('abbac') 
# Counter({'a': 2, 'b': 2, 'c': 1})

c['x'] 
# Zwraca 0 zamiast wyjątku

c.most_common() 
# Zwraca posortowaną listę od najczęściej występującego elementu
# [('a', 2), ('b', 2), ('c', 1)]
```