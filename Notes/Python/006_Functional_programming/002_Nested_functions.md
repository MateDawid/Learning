# Funkcje zagnieżdżone
Jako, że funkcje to typ pierwszoklasowy, można je bez ograniczeń zagnieżdżać. Stosowanie funkcji zagnieżdżonych umożliwia ukrywanie implementacji. Funkcja zagnieżdżona ma zasięg lokalny, przez co ma bezpośredni dostęp do argumentów przekazanych do funkcji nadrzędnej.  
```python
def selection_sort(items):

	def recursive(items, i):
		
		def min_index(i):
			return items.index(items[i:], i)
		
		def swap(i, j):
			items[i], items[j] = items[j], items[i]
		
		if i < len(items):
			j = min_index(i)
			swap(i, j)
			selection_sort(items, i + 1)
	
	recursive(items, 0)

items = ['bob', 'alice', 'max']
selection_sort(items) 
```