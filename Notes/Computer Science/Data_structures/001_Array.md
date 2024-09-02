# Tablice
Python jako swoją implementację abstrakcyjnej struktury danych tablicy stosuje listy, wykorzystujące nadmierną alokację (zabezpieczają się większą ilością pamięci niż zajmują przechowywane dane). 
Chcąc wykorzystać "klasyczny" rodzaj tablicy wykorzystywany jest moduł array.
```python
import array

# pierwszy parametr określa typ danych (tutaj float), drugi to lista wartości
arr = array.array('f', (1.0, 1.5, 2.0, 2.5))
``` 
## Zadanie - Przesuwanie zer
Zadanie polega na wyszukaniu w tablicy wszystkich zer i przesunięcie ich na sam koniec bez zmieniania kolejności pozostąłych elementów tablicy. 
```python
def move_zeros(a_list):
	zero_index = 0
	for index, n in enumerate(a_list):
		if n != 0:
			a_list[zero_index] = n
			if zero_index != index:
				a_list[index] = 0
			zero_index += 1
	return a_list

a_list = [8, 0, 3, 0, 12] 
move_zeros(a_list)
print(a_list) #  [8, 3, 12, 0, 0]
```