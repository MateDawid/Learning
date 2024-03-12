# map i filter
```python
names = ['jan kot', 18, 'ANNA KRÓL', 'jÓzef BYK', ['nie', 'wasza','sprawa'], 'ROBERT wąŻ']

# filter(funkcja,sekwencja)
# elementy z listy names przekazywane są do lambdy, która sprawdza czy ich typ to string
# jeśli tak, to element zostaje dodany do listy names_cleaned
names_cleaned = list(filter(lambda x:type(x) is str, names))

# map(funkcja,sekwencja)
# elementy z listy names_cleaned przekazane są do lambdy
# która najpierw zamienia wszystkie litery danego stringa na małe,
# a następnie pierwsza literę każdego słowa zmienia na dużą
# tak zmodyfikowany string zostaje dodany do listy names_corrected
names_corrected = list(map(lambda x: x.lower().title(), names_cleaned))
```