# Lista połączona
Implementacja abstrakcyjnego typu danych listy. Pozwala na dodawanie, usuwanie oraz wyszukiwanie elementów. Elementy listy nie są indeksowane, ponieważ komputer nie przechowuje ich w jednym, ciągłym obszarze pamięci. Zamiast tego lista połączona stanowi łańcuch wierzchołków, z których każdy zawiera jakieś dane oraz adres następnego wierzchołka listy.
* Wyszukiwanie elementu na liście połączonej wymaga w najgorszym wypadku przeszukania wszystkich elementów listy  - złożoność O(n).
* Dodawanie i usuwanie elementów jest za to operacją o stałym czasie - złożoność O(1). 
* Konieczność zapisywania wskaźników do kolejnych elementów zużywa zasoby systemowe, przez co listy połączone wymagają więcej pamięci niż tablice.
* Listy połączone nie pozwalają na swobodny dostęp do elementów (odwołanie do dowolnego elementu w stałym czasie).
```python
class Node:
	def __init__(self, data, next=None):
		self.data = data
		self.next = next

class LinkedList:
	def __init__(self):
		self.head = None
	
	def append(self, data):
		if not self.head:
			self.head = Node(data)
			return
		current = self.head
		while current.next:
			current = current.next
		current.next = Node(data)
```
## 1. Lista jednokierunkowa
Typ listy połączonej, w której każdy wierzchołek zawiera tylko jeden wskaźnik - odwołujący się do następnego elementu listy.
### 2. Lista dwukierunkowa (podwójnie połączona)
Lista połączona, która zawiera dwa wskaźniki: jeden wskazuje na następny wierzchołek, a drugi na poprzedni.
### 3. deque
Python nie zawiera wbudowanej implementacji list kierunkowych, natomiast udostępnia strukturę danych deque, która wewnętrznie używa takich list.
```python
from collections import deque

d = deque()
d.append('Harry')
d.append('Potter')
```