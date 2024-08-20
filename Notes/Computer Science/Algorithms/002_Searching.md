# Wyszukiwanie
## 1. Wyszukiwanie liniowe
Algorytm, który przegląda kolejno wszystkie wartości dostępne w zbiorze danych i porównuje je z poszukiwaną wartością. Wyszukiwanie liniowe stosowane jest na danych nieposortowanych.
```python
def linear_search(a_list, n):
	for i in a_list:
		if i == n:
			return True
	return False
```
## 2. Wyszukiwanie binarne
Algorytm wyszukiwania użyteczny jedynie dla posortowanych danych. Algorytm wyszukuje wskazaną wartość dzieląc analizowany zbiór danych na połowy.
```python
def binary_search(a_list, n):
	first = 0
	last = len(a_list) - 1
	while last >= first:
		mid = (first + last) // 2
		if a_list[mid] == n:
			return True
		else:
			if n < a_list[mid]:
				last = mid - 1
			else:
				first = mid + 1
	return False
```