# ChainMap
Struktura umożliwiająca połączenie dwóch słowników. W przypadku, gdy w którymś ze składowych słowników zajdzie jakaś zmiana, będzie ona uwzględniona w obiekcie ChainMap.
```python
from collections import ChainMap

d1 = {'color': 'red'}
d2 = {'pet': 'cat'}

d = dict(ChainMap(d1, d2))  # {'color': 'red', 'pet': 'cat'}

maps = d,maps # lista słowników w kolejności, w jakiej zostały dodane[{'color': 'red'}, {'pet': 'cat'}]
```
Przy próbie podania wartości dla już istniejącego klucza w ChainMap pozostanie pierwotna wartość.
