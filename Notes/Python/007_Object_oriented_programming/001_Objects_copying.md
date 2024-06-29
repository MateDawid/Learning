# Kopiowanie obiektów
Kopiowanie obiektów może odbywać się w sposób płytki i głęboki. W przypadku kopiowania płytkiego mutowalne elementy nie są rzeczywistą kopią pierwotnych elementów, ale kopią referencji do tych obiektów w pamięci
```python
import copy

x = [1, [2, 3]]
# shallow copy - płytkie kopiowanie
# y = x[:]
# y = list(x)
y = copy.copy(x)

y.append(5)
# x = [1, [2,3]]
# y = [1, [2,3], 5]

y[1].append(5)
# Jako, że lista jest mutowalna, to po dodaniu do niej elementu w jednej z list, element ten jest widoczny w obu kopiach listy
# x = [1, [2, 3, 4]]
# x = [1, [2, 3, 4], 5] 
```
Rozwiązaniem powyższego problemu może być użycie deepcopy, które rekurencyjnie kopiuje kolejne elementy z drzewa obiektu (nie ich referencje, jak w przypadku mutowalnych obiektów przy płytkim kopiowaniu).

```python
import copy

x = [1, [2, 3]]
# deep copy - głębokie kopiowanie
y = copy.deepcopy(x)

y[1].append(5)
# x = [1, [2, 3]]
# x = [1, [2, 3, 4]] 
```