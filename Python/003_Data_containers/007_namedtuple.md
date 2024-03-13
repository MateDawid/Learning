# namedtuple
Namedtuple to po prostu tuple z nazwanymi polami
```python
import collections import namedtuple

p = 1, 2
Point = namedtuple('Point', ['x', 'y'])
Point(*p)
# Point(x=1, x=2)
d = {'x': 3, 'y': 4}
Point(**d)
# Point(x=3, x=4)
Point(x=5, y=6)
# Point(x=5, x=6)
```