# defaultdict
Pozwala na uproszczenie i przyspieszenie kodu, którego celem jest np. budowa słownika. Przykładowo - poniżej kod, którego celem jest zbudowanie słownika, gdzie kluczem jest długość imienia, a wartością - lista podanych w sekwencji imion.
```python
names_by_length = {}
for name in ('bob', 'alice', 'max', 'adam', 'eve'):
	key = len(name)
	if key not in names_by_length:
		names_by_length[key] = []
	names_by_length[key].append(name)
	
# names_by_length = {3: ['bob', 'max', 'eve'], 4: ['adam'], 5: ['alice']}
```
Ten sam efekt można uzyskać używając defaultdict. W przypadku, gdy kod sięga do słownika przy użyciu nieistniejącego klucza wykonywana jest funkcja podana jako argument przy inicjalizacji defaultdicta (w tym przypadku funkcja list()).

```python
from collections import defaultdict

names_by_length = defaultdict(list)
# argument "list" oznacza, że przy próbie wyciągnięcia danych dla nieistniejącego klucza zostanie utworzona pusta lista

for name in ('bob', 'alice', 'max', 'adam', 'eve'):
	names_by_length[len(name)].append(name)
	
# names_by_length = {3: ['bob', 'max', 'eve'], 4: ['adam'], 5: ['alice']}
```