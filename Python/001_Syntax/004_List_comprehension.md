# List Ccomprehension
```python
L = [1,2,3,4,5,6]
L1 = [x for x in range(5)]        # elementy z zakresu od 0 do 4
L2 = [x**2 for x in L]            # elementy z listy L podniesione do kwadratu
L3 = [x for x in L if x % 2 == 0] # elementy z listy L, tylko jeśli dany element jest podzielny przez 2
L4 = ['Parzysta' if x%2 == 0 else 'Nieparzysta' for x in range(5)]
                                  # 'Parzysta' lub 'Nieparzysta' w zależności od tego czy kolejny element
                                  # z zakresu 0 do 4 jest podzielny lub nie jest podzielny przez 2
L5 = [(x, x+10) for x in L]       # dwuelementowe tuple, które na indeksie 0 mają kolejny element z listy L
                                  # a na indeksie 1 ten sam element zwiększony o 10
```
# Zagnieżdżone List Comprehension
```python
# 2-D List
matrix = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
  
# Nested List Comprehension to flatten a given 2-D matrix
flatten_matrix = [val for sublist in matrix for val in sublist]

# [val
# for sublist in matrix
# for val in sublist]
```