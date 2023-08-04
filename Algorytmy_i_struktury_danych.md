# **Algorytmy i struktury danych**
## 1. Wyszukiwanie
### 1.1. Wyszukiwanie liniowe
Algorytm, który przegląda kolejno wszystkie wartości dostępne w zbiorze danych i porównuje je z poszukiwaną wartością.
### 1.2. Wyszukiwanie binarne
Algorytm wyszukiwania dla posortowanych danych. Algorytm wyszukuje wskazaną wartość dzieląc analizowanyc zbiór danych na połowy.
## 2. Sortowanie
### 2.1. Sortowanie bąbelkowe
Algorytm sortowania, który przegląda listę liczb, porównuje każdą liczbę z następną i zamienia je miejscami, jeśli są zapisane w nieodpowiedniej kolejności.
### 2.2. Sortowanie przez wstawianie
Stabilny algorytm sortowania, w którym dane są porządkowane w sposób przypominający sortowanie talii kart. W trakcie całego procesu zbiór dzieli się na dwie cześci - posortowaną i nieposortowaną. Na samym początku w części posortowanej znajduje się pierwszy element zbioru. Porównujemy pierwszy element listy nieposortowanej z ostatnim elementem listy posortowanej i zamieniamy je miejscami aż do momentu, gdy będą w odpowiedniej kolejności. Powtarzamy ten krok aż do ostatniego elementu listy nieposortowanej.
### 2.3. Sortowanie przez scalanie
Stabilny algorytm rekurencyjny (typu "dziel i rządź"), który dzieli listę na połowy tak długo, aż uzyska listy o długości jednego elementu, które następnie łączy w odpowiedniej kolejności.
#### 2.3.1. Algorytmy typu "Dziel i rządź"
Algorytmy, które rekurencyjnie dzielą problem na dwa lub więcej podproblemów, aż do momentu, gdy będą one na tyle proste, że będzie je można łatwo rozwiązać.
### 2.4. Timsort
Algorytm wykorzystywany we wbudowanych funkcja Pythona sort i sorted. Stanowi on hybrydowe połączenie sortowania przez scalanie oraz sortowania przez wstawianie.
## 3. Algorytm Euklidesa
Najefektywniejszy sposób znajdowania wspólnego czynnika. Składa się z następujących kroków:
* Podzielenie liczby x przez y i wyznaczenie reszty z dzielenia,
* Zastąpienie liczby y resztą z dzielenia oraz liczby x liczbą y i ponowne wykonanie dzielenia,
* Poprzedni krok powtarzany jest do momentu otrzymania reszty dzielenia równej 0
* Ostatni dzielnik jest największym wspólnym czynnikiem
## 4. Tablice
Python jako swoją implementację abstrakcyjnej struktury danych tablicy stosuje listy, wykorzystujące nadmierną alokację (zabezpieczają się większą ilością pamięci niż zajmują przechowywane dane). 
Chcąc wykorzystać "klasyczny" rodzaj tablicy wykorzystywany jest moduł array.
```python
import array

# pierwszy parametr określa typ danych (tutaj float), drugi to lista wartości
arr = array.array('f', (1.0, 1.5, 2.0, 2.5))
``` 
## ?. Kolejki
#### 2.1. Kolejka
Podstawowy rodzaj kolejki, który wykorzystuje schemat FIFO (First in, first out). Działa na wzór kolejki np. na poczcie. Elementy mogą być dodawane na koniec kolejki i zdejmowane z jej początku.
#### 2.2. Stos
Kolejka, stosująca schemat LIFO (Last in, first out). Działa na wzór np. stosu książek. Zawartość stosu może być dodawana lub zdejmowana z tzw. szczytu.
#### 2.3. Kolejka priorytetowa
Często nazywana kopcem binarnym. Elementy kopca są wstawiane wraz z priorytetem w pierwsze wolne miejsce na dole kopca. Zdejmowany jest element o najwyższym, lub najniższym priorytecie.

![Priority Queue Data Structure](https://cdn.programiz.com/sites/tutorial2program/files/insert-1_0.png)
