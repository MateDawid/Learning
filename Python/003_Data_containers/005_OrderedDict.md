# OrderedDict
Słownik zachowujący porządek wstawianych kluczy. Wykorzystuje wewnętrznie listę dwukierunkową.
```python
from collections import OrderedDict

row = OrderedDict()
row['id'] = '123'
row['firstName'] = 'Jan'
row['lastName'] = 'Kowalski'

list(row.items())
# Poszczególne elementy słownika są zachowana w kolejności, w jakiej zostały dodane
# [('id', '123'), ('firstName', 'Jan'), ('lastName', 'Kowalski')]
```