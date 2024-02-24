# Analiza algorytmów
Algorytmy można analizować na przykład na bazie ich złożoności obliczeniowej.
## 1. Czas stały - O(1)
Najbardziej efektywny, wymaga wykonania jednego kroku niezależnie od wielkości danych wejściowych. Przykład: Wyciągnięcie pojedynczego elementu z listy.
## 2. Czas logarytmiczny - O(log n)
Liczba kroków jest proporcjonalna do logarytmu wielkości danych wejściowych, zatem rośnie wolniej od nich. Przykład: algorytm wyszukiwania binarnego.
## 3. Czas liniowy - O(n)
Liczba kroków jest wprost proporcjonalna do ilości danych wejściowych. Przykład: Wyświetlenie każdego elementu listy. 
## 4. Czas logarytmiczno-liniowy - O(n log n)
Liczba kroków jest iloczynem złożoności logarytmicznej i liniowej. Dzieje się tak, gdy np. algorytm wykonuje n razy czynność o złożoności O(log n). Przykład: algorytm merge sort.
## 5. Czas kwadratowy - O(n**2)
Liczba kroków wprost proporcjonalna do kwadratu wielkości danych wejściowych. Przykład: Sortowanie bąbelkowe.
## 6. Czas sześcienny - O(n**3)
Liczba kroków wprost proporcjonalna do sześcianu wielkości danych wejściowych. Przykład: Trzy zagnieżdżone pętle.
## 7. Czas wykładniczy - O(c**n)
Najgorsza możliwa złożoność. Liczba kroków jest równa pewnej stałej podniesionej do potęgi równej wielkości danych wejściowych. Przykład: program odgadujący hasło o długości n metodą brute force (sprawdzanie każdej możliwej kombinacji).
