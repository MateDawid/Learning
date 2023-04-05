
# **PYTHON**
## 1. WŁAŚCIWOŚCI JĘZYKA
### 1.1. Przestrzenie nazw  
W pewnym sensie powiązane z zakresami są przestrzenie nazw. Są to zakresy zapewniające nam to, że nazwa danego obiektu będzie unikalna i że można z nich będzie korzystać bez ryzyka wystąpienia jakichkolwiek konfliktów. To swojego rodzaju zbiór nazw i definicji, które mogą mieć zastosowanie lokalne (podobnie jak zakresy, w obrębie funkcji), ale także globalnie, które określają nazwy dla całego kodu, zaimportowanych paczek. W Pythonie funkcjonują także wbudowane przestrzenie nazw kluczowych funkcji w tym języku, dzięki którym możemy mieć pewność, że utworzony przez nas obiekt nie będzie w konflikcie z którąkolwiek z wbudowanych funkcji Pythona.  
### 1.2. Różnica między modułem i paczką  
Zarówno moduły jak i paczki wykorzystywane są do modularyzacji kodu, co przekłada się na jego łatwość w utrzymaniu i ułatwia pracę z omówionymi już zakresami. Moduły są plikami zawierający zestaw zdefiniowanych instrukcji, klas i zmiennych. Można zaimportować zarówno całe moduły, jak i ich części.  
Paczka w Pythonie zazwyczaj składa się z kilku modułów. Jest ona jednak na tyle przydatna, że określa dla nich przestrzenie nazw i eliminuje konflikty pomiędzy poszczególnymi modułami.  
### 1.3. Zakresy  
Zakresy, czy też scope’y, w Pythonie nie różnią się od tego, co znamy z innych języków programowania. Scope to blok kodu, w którym działa dany obiekt i tylko w nim jest dostępny. Na przykład lokalny zakres odnosi się do wszystkich obiektów w danej funkcji, zaś zakres globalny będzie zawierał wszystkie obiekty w całym kodzie.  
```python
x = 10             # zmienna globalna

def f():
    global x       # słowo global informuje Pythona, że poprzez zmienną x będziemy odnosić się do zmiennej globalnej
    x = 111        # zmiana wartości przypisanej do zmiennej globalnej
    y = 12         # zmienna lokalna (przestaje istnieć po zakończeniu wykonywania funkcji)
    print(x, y)

f()                # uruchomienie funkcji wydrukuje zmienną globalną x i zmienna lokalną y
print(x)           # drukuje zmienną globalną x
```
###   1.4. Typy wbudowane  
- `str` – string, tekstowy typ danych,  
- `int` – liczba,  
- `float` – liczba zmiennoprzecinkowa,  
- `complex` – liczba zespolona,  
- `list` – lista  
- `tuple` – kortka  
- `range` – zakres, liczby naturalne stanowiące szereg arytmetyczny,  
- `dict` – słownik,  
- `set` – zbiór,  
- `frozenset` – zbiór niemutowalny,  
- `bool` – logika boolowska,  
- `bytes` – konwersja ciągu na bajty,  
- `bytearray` – mutowalny wariant bytes,  
- `memoryview` – dostęp do wewnętrznych danych obiektów obsługujących bufory protokołów.  

### 1.5. PYTHONPATH  
`PYTHONPATH` to zmienna środowiskowa pozwalająca wskazać dodatkowe lokalizacje, z których Python będzie mógł zaciągnąć moduły i paczki.  
### 1.6. PEP8  
PEP 8 to opracowany jeszcze w 2001 r. dokument, w którym opisane zostały najlepsze praktyki w zakresie pisania czytelnego kodu w Pythonie. Stanowi część oficjalnej dokumentacji języka. Stanowi on powszechnie respektowaną normę i w zasadzie stanowi lekturę obowiązkową dla każdego, kto chce programować w Pythonie. Z treścią dokumentu zapoznać się można na  [oficjalnej stronie Pythona](https://www.python.org/dev/peps/pep-0008/#introduction).
## 2. SYNTAX
### 2.1. Różnica między 'is', a '=='
```python
print(1 == True) # == to operator porównania wartości
print(1 is True) # is to operator porównania identyczności/tożsamości

print(id(1), id(1), id(True))  # wydrukuj id integera 1 i booleana True

print(2 ** 3 == 10 - 2)        # wydrukuj wynik porównania wartości dwóch równań

A = [1,2,3]                    # stworzenie dwóch list o identycznej zawartości
B = [1,2,3]                    # i przypisanych do innych zmiennych A i B
print(A == B)                  # porównanie wartości list A i B
print(A is B)                  # porównanie identyczności/tożsamośli list A i B

a = 'abc'                    # stworzenie dwóch stringów o identycznej zawartości
b = 'abc'                    # i przypisanych do innych zmiennych a i b
print(a == b)                  # porównanie wartości stringów a i b
print(a is b)                  # porównanie identyczności/tożsamości stringów a i b
```
### 2.2. Porównania łańcuchowe
```python
print(False is False)
print(True is False)
print(False is False is False) # (False is False) and (False is False) -> (True) and (True) -> True
print(1 < 3 == 5)              # (1 < 3) and (3 == 5) -> (True) and (False) -> False

print(1 is not True in [1,2,3]) # ->
# (1 is not True) and (True in [1,2,3]) # ->
# (True) and (True) -> True

# różne wyniki dla operatorów "is not" oraz "!=" !
print(1 is not True)
print(1 != True)
```
Wszystkie porównania łańcuchowe w Pythonie traktowane są wg tego samego schematu: porównanie rozbijane jest na dwuelementowe podgrupy połączone operatorem 'and' Przykładowo, porównanie czteroelementowe zostanie potraktowane następująco:
```python
A is B == C > D  -> (A is B) and (B == C) and (C > D)
```
 Analogicznie postępujemy dla pięciu i więcej elementów.
### 2.3. lambda  
Lambda w Pythonie to funkcja, która może przyjąć każdą liczbę argumentów, ale mieć tylko jedno wyrażenie. Co ważne, jest to funkcja anonimowa, a zatem nie jest powiązana z żadnym identyfikatorem. Pozwala wyeliminować funkcję zainicjowane na potrzeby funkcji wyższego rzędu i przekazać jej parametry.
```python
# lambda argument : wyrażenie
# lambda x:x+2

L = [('Anna',82), ('Robert',33), ('Arthur',40), ('John',56)]
# Funkcja sorted pobiera sekwencję danych do posortowania i klucz, po którym będzie sortować.
# Sekwencją jest lista L, a kluczem lambda, która dla kolejnego elementu listy L (czyli tupli)
# zwraca drugi element danej tupli.
L_sorted = sorted(L, key = lambda x:x[1])
```
### 2.4. map i filter
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
### 2.5. Dekoratory
```python
def add_stars(function):     # definicja dekoratora niczym nie różni się od definicji zwykłej funkcji
    def decorated_function():   # wewnątrz dekoratowa tworzymy WEWNĘTRZNĄ funkcję, w której udekorujemy funkcję pobraną jako argument
        print("***")             # dekorowanie funkcji
        function()               # wywołanie funkcji będącej argumentem dekoratora
        print("***")             # dekorowanie funkcji
    return decorated_function    # zwrócenie funkcji WEWNĘTRZNEJ, w której udekorowano funkcję będącą argumentem dekoratora

@add_stars                       # zapis @add_stars BEZPOŚREDNIO nad definicją funkcji f() powoduje, że funkcja f() zostaje udekorowana
def f():                         # definicja funkcji f()
    print("Cześć, jestem f()")
```
### 2.6. Generatory
```python
def get_next_even():                   # definicja generatora wygląda jak definicja zwykłej funkcji
    for n in range(2,20,2):            # range tworzący zakres od 2 do 20, przesuwając się o 2
        yield n                        # słowo yield informuje interpreter, że ta funkcja będzie generatorem

z = get_next_even()                    # tworzenie obiektu generatora

for i in range(10):                    # pętla for wykonująca się 10 razy
    print(next(z))                     # która za kazdym razem drukuje kolejną wartość zwróconą z obiektu genratora z

y = ('a' * n for n in range(5))        # generator expression - wyrażenie generatorowe
                                       # tworzy generator, który będzie zwracał kolejne wielokrotności stringa 'a'
                                       # zakresie od 0 do 4

for i in range(5):                     # wypisanie kolejnych wartości zwróconych przez obiekt genratora y
    print(next(y))
```
## 3. STRING
### 3.1. Zamiana elementów stringa
```python
a = "abcdefg"            # do zmiennej a przypisz zostaje string 'abcdefg'
print(a[1])              # wydrukuj element znajdujący się pod indeksem 1 w stringu a
# a[1] = 'X'             # próba modyfikacji stringa - operacja zabroniona skutkująca TypeError
a_list = list(a)        # stwórz listę a_list zawierającą litery ze stringa a
a_list[1] = 'X'         # zmodyfikuj zawartość listy pod indeksem 1
a = "".join(a_lista)     # stwórz stringa a łącząc elementy listy a_list przy użyciu pustego separatora ""
print(a)
```
## 4. LIST
### 4.1. Lista niepowtarzalnych elementów
```python 
A = [1,2,3,3,2,1,2,3]
# rozwiązanie 1
B = []
for element in A:
  if element not in B:
    B.append(element)
print(B)
# rozwiązanie 2
B = list(set(A))
print(B)
```
### 4.2. Różnice między listą i krotką
```python
L = [1, 2, 3, True, (1, 2)]
T = (4, 5, 6, False, ['x', 'y'])
L[2] = 'trzy'   # modyfikacja zawartości listy - operacja legalna
T[2] = 'sześć'  # próba modyfikacji zawartości tupli - operacja zabroniona, skutkuje TypeError
```
### 4.3. Różnice między listą i tablicą  
Tablice w Pythonie są homogeniczne. Oznacza to, że zawierają dane tylko i wyłącznie jednego typu. W przypadku list nie ma tego ograniczenia i swobodnie można wewnątrz nich zawrzeć np. liczby i stringi. Warto wspomnieć, że homogeniczne listy zużywają znacznie mniej pamięci.  
### 4.4. Kopiowanie list
W Pythonie kopiowanie nie odbywa się z użyciem operatora  `=`. Wówczas jedynie tworzymy powiązanie między istniejącym już obiektem a docelową nazwą zmiennej. Zamiast wspomnianego operatora, w Pythonie wykorzystuje się moduł copy. Mamy dzięki niemu dwie możliwości kopiowania: płytkie i głębokie. W pierwszym przypadku tworzy się bitową kopię 1:1, zaś głęboka kopia pozwala na rekursywne kopiowanie wszystkich wartości. Składnia:  
```python  
list_1 = [1, 2, 3]  
list_2 = copy(list_1) # płytkie kopiowanie  
list_3 = deepcopy(list_1) # głębokie kopiowanie

A = [1,2,3,4,5]         # do zmiennej A przypisujemy REFERENCJĘ do przechowywanej w pamięci listy
B = A                   # do zmiennej B przepisujemy REFERENCJĘ do listy przechowywanej pod zmienną A.
C = A[:] # C = list(A)  # do zmiennej C przypisujemy KOPIĘ listy przechowywanej pod zmienną A
B[0] = 111              # zmieniamy pierwszy element listy, na który wskazują zarówno zmienne B jak i A
```  
### 4.5. Odwrócenie listy
```python
languages = ['Python', 'Java', 'C#', 'Ruby']
# 1
languages .reverse()             # odwróć listę languages (nastąpi nadpisanie wcześniejszej listy)
reversed_languages = languages # przypisz wartość listy languages do nowej zmiennej reversed_languages
# 2
reversed_languages= list(reversed(languages))  # stwórz listę na podstawie obiektu zawierającego odwrócone elementy listy languages i przypisz do reversed_languages
# 3
reversed_languages = languages[::-1]            # do zmiennej reversed_languages przypisz wartosci listy languages odczytane od tyłu
# 4
reversed_languages = []                  # stworz pusta liste reversed_languages 
for language in languages:                   # dla kolejnego jezyka w liscie languages
    reversed_languages.insert(0,language)   # umiesc ten jezyk na indeksie zerowym listy reversed_languages
```
### 4.6. List comprehension
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
### 4.7. Zagnieżdżone List Comprehension
```python
# 2-D List
matrix = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
  
# Nested List Comprehension to flatten a given 2-D matrix
flatten_matrix = [val for sublist in matrix for val in sublist]

# [val
# for sublist in matrix
# for val in sublist]
```
## 5. DICTIONARY
### 5.1. Poprawne tworzenie słowników
Klucze słownika muszą być elementem niemutowalnym, a więc mogą być typu int, string lub tuple, ale nie mogą być listą lub innym słownikiem.
```python
A = {1: 1, 2: 4, 3: 9}
B = {'imie': 'Anna', 'nazwisko': 'Kowalska'}
# C = {[4, 5]: [16, 25]}    # lista jako element mutowalny nie może byc kluczem słownika!
D = {(4, 5): [16, 25]}
# E = {{1:2}: 'jeden_dwa'}  # słownik jako element mutowalny równiez nie może być kluczem!
```
### 5.2. Dict comprehension
```python
L = [1,2,3,4,5,6]
D1 = {x:x % 2 == 0 for x in L}   
# pary klucz:wartość, gdzie kluczem są elementy z listy L a wartościami 
# True lub False, w zależności od tego czy dany klucz jest podzielny przez 2
```
## 6. KLASY
### 6.1. init 
Metoda specjalna \_\_init__ wywoływana automatycznie podczas po utworzeniu instancji klasy. Dzięki niej możliwe jest na przykład doczytanie kodu czy automatycznie dodanie atrybutów zawsze, gdy tworzony będzie nowy obiekt lub instancja. Pozwala także odróżnić metody i atrybuty klasy od lokalnych zmiennych. 
```python
class Dog:                               # tworzenie klasy Pies
    def __init__(self, name, breed):     # konstruktor klasy pobierający imię i rasę
        self.name = name                 # tworzenie pól klasy i przypisywanie do nich wartości podanych w konstruktorze
        self.breed = breed               # tworzenie pól klasy i przypisywanie do nich wartości podanych w konstruktorze

small_dog = Dog("Pikuś", 'ratler')    # tworzenie obiektu klasy Pies, z parametrami konstruktora "Pikuś" i 'ratler'
big_dog = Dog("Killer", 'doberman')   # tworzenie obiektu klasy Pies, z parametrami konstruktora "Killer" i 'doberman'

print(small_dog.name, small_dog.breed)    # wydrukowanie atrybutów obiektów
print(big_dog.imie, big_dog.breed)        # wydrukowanie atrybutów obiektów
```
## 7. USE CASES
### 7.1. Palindrom
```python
#1
def is_palindrome(word):
    reversed_word= word[::-1]     # utworz zmienna slowo_odwrocone odwracając przy użyciu sliców
    if word== reversed_word:      # jeśli slowo jest równe slowo_odwrocone
        return True               # zwróć True
    else:                         # w przeciwnym wypadku
        return False              # zwróć False
#2
def is_palindrome(word):
    return True if word== slowo[::-1] else False
    # zwróć True jeśli slowo jest rowne samemu sobie przeczytanemu od tyłu, 
    # w przeciwnym wypadku zwróć False
#3
def is_palindrome(word):
    start = 0                             # stwórz indeks poczatkowy równy 0
    end = len(word) - 1                   # stwórz indeks końcowy równy długości stringa zmniejszonej o 1
    while start <= end:                   # wykonuj pętlę dopóki indeks poczatkowy jest mniejszy lub równy indeksowi końcowemu
        if word[start ] != word[end]:     # jeśli wartosc zmiennej slowo od indeksu początkowego jest różna od wartości od indeksu końcowego
            return False                  # zwróć False
        else:                             # w przeciwnym wypadku
            start += 1                    # zwiększ indeks początkowy o 1
            end -= 1                      # zmniejsz indeks końcowy o 1
    return True                           # jeśli funkcja dotarła do tego miejsca, to znaczy że słowo jest palindromem i funkcja zwraca True
print(is_palindrome("kajak"))
print(is_palindrome("anakonda"))
```
### 7.2. Ciąg Fibonacciego
```python
# kolejny element ciągu: 0   1   2   3   4   5   6    7   8   9  10
# wartość dla elementu:  0   1   1   2   3   5   8   13  21  34  55

def fibonacci_l(n): # O(n)
    p, d = 0, 1              # inicjalizacja zmiennych p-pierwsza, d-druga
    for _ in range(n):       # _ - oznacza, że nie potrzebujemy zmiennej do przechowywania kolejnej wartości z range, chcemy tylko aby pętla wykonała się n razy
        p, d = d, p + d      # jednoczesne aktualizowanie zawartości zmiennych p i d, aby przypisać do nich wartości z poprzedniego obiegu pętli
    return p

print(fibonacci_l(8))

def fibonacci_r(n): # O(2 ^ n)
    if n <= 1:               # każda funkcja rekurencyjna musi mieć warunek, który powoduje returna bez kolejnego wywołania rekurencji
        return n             # tu tym warunkiem jest sytuacja gdy szukamy wartości dla zerowego lub pierwszego elementu ciągu Fibonacciego
    return fibonacci_r(n - 1) + fibonacci_r(n - 2)  # dla każdego elementu innego niż zerowy lub pierwszy, funkcja wywołuje samą siebie
                             # aby policzyć dwa poprzednie wyrazy ciągu i dodać je do siebie
print(fibonacci_r(10))
```
### 7.3. Tworzenie plików
```python
with open('file.txt', 'w') as f:    # otwórz plik 'file.txt' w wersji do zapisu ('w' od write), nadaj mu alias f
    for n in range(1, 101):             # dla kolejnych liczb z zakresu od 1 do 100
        f.write(str(n) + '\n')          # wpisz do pliku stringa utworzonego na podstawie liczby oraz znak nowej linii '\n'

with open('file.txt', 'r') as f:    # otwórz plik 'file.txt' w wersji do odczytu ('r' od read), nadaj mu alias f
    file_lines = f.readlines()             # do listy file_lines wpisz kolejne linijki przeczytane z pliku 'file.txt'
                                        # każda linijka będzie osobnym elementem listy
```
## 8. TESTY
### 8.1. assert
```python
def square(x):
    return x * x

assert square(10) == 20

""" Output:
Traceback (most recent call last):
  File "assert.py", line 4, in <module>
    assert square(10) == 20
AssertionError
"""
```
### 8.2. Biblioteka unittest
```python
# Import the unittest library and our function
import unittest

class Tests(unittest.TestCase):

    def test_1(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
```
## 9. KONTENERY DANYCH
### 9.1. Array
Struktura danych przypominająca działaniem array stosowany np. w C i służy między innymi do komunikacji z softem pisanym w tym języku. 
```python
import array

# Konieczne zadeklarowanie typu zmiennych.
example = array.array('b')
```
### 9.2. ChainMap
Struktura umożliwiająca połączenie dwóch słowników. W przypadku, gdy w którymś ze składowych słowników zajdzie jakaś zmiana, będzie ona uwzględniona w obiekcie ChainMap.
```python
from collections import ChainMap

d1 = {'color': 'red'}
d2 = {'pet': 'cat'}

d = dict(ChainMap(d1, d2))  # {'color': 'red', 'pet': 'cat'}

maps = d,maps # lista słowników w kolejności, w jakiej zostały dodane[{'color': 'red'}, {'pet': 'cat'}]
```
Przy próbie podania wartości dla już istniejącego klucza w ChainMap pozostanie pierwotna wartość.

### 9.3. Counter
Zlicza ilość wystąpień elementów w sekwencji.
```python
from collections import Counter

c = Counter('abbac') 
# Counter({'a': 2, 'b': 2, 'c': 1})

c['x'] 
# Zwraca 0 zamiast wyjątku

c.most_common() 
# Zwraca posortowaną listę od najczęściej występującego elementu
# [('a', 2), ('b', 2), ('c', 1)]
```
### 9.4. defaultdict
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
### 9.5. OrderedDict
Słownik zachowujący porządek wstawianych kluczy. Wykorzystuje wewnętrznie listę dwukierunkową.
```python
from collections import OrderedDict

row = OrderedDict()
row['id'] = '123'
row['firstName'] = 'Jan'
row['lastName'] = 'Kowalski'

list(row.items())
# Poszczególne elementy słownika są zachowana w kolejności, w jakiej zostały dodane
# [('id', '123'), ('firstName', 'Jan'), ('lastName', 'Kowalski')]
```
### 9.6. deque
Nazwa to skrót od "double ended queue". Wykorzystuje wewnętrznie listę dwukierunkową. Deque może służyć np. do składowania historii operacji. 
Dla określonej liczby elementów deque zachowuje ich kolejność przy użyciu wskaźnika początkowego i końcowego. Przy dodaniu nowego elementu wskaźnik końcowy wskazuje na nowy element, za to wskaźnik początkowy przenosi się na następujący po dotychczasowym elemencie początkowym.
```python
from collections import deque

history = deque(maxlen=3)
# maxlen określa maksymalną długość kolejki

text = "Houston we have a problem"
for word in text.split():
	history.append(word)

# W czasie iteracji zmienna history będzie zawierać zawsze 3 elementy, gdzie dodanie nowego elementu będzie usuwać pierwszy element z listy, jeżeli będzie ona miała długość równą maxlen

history.popleft()
# Usuwa element z lewej (początkowej) strony kolejki
history.appendleft('not')
# Dodaje element na początku kolejki
```
### 9.7. namedtuple
Namedtuple to po prostu tuple z nazwanymi polami
```python
import collections import namedtuple

p = 1, 2
Point = namedtuple('Point', ['x', 'y'])
Point(*p)
# Point(x=1, x=2)
d = {'x': 3, 'y': 4}
Point(**d)
# Point(x=3, x=4)
Point(x=5, y=6)
# Point(x=5, x=6)
```
### 9.8. enum

Moduł pozwalający na tworzenie typów wyliczeniowych.
```python
from enum import Enum

class Season(Enum):
	SPRING = 1
	SUMMER = 2
	AUTUMN = 3
	WINTER = 4

# printing enum member as string
Season.SPRING
# Season.SPRING

# printing name of enum member using "name" keyword
print(Season.SPRING.name)
# SPRING

# printing value of enum member using "value" keyword
print(Season.SPRING.value)
# 1

# printing the type of enum member using type()
print(type(Season.SPRING))
# <enum 'Season'>

# printing enum member as repr
print(repr(Season.SPRING))
# <Season.SPRING: 1>

# printing all enum member using "list" keyword
print(list(Season))
# [<Season.SPRING: 1>, <Season.SUMMER: 2>, <Season.AUTUMN: 3>, <Season.WINTER: 4>]
```
## 10. ITERACJA
### 10.1. Iterable
Kompozyt zdolny do zwracania swoich elementów w pętli for. Są to np. typy sekwencyjne (listy, krotki, stringi), dict, set, file, itp.
```python
class Iterable:
	def __getitem__(self, key):
		(...)
	def __len__(self):
		return (...)

iterable[123]
iterable['foobar']
```
Dla bardziej skomplikowanej logiki iterowania definiuje się metodę **\_\_iter\_\_**
```python
class Iterable:
	(...)
	def __iter__(self):
		return Iterator(...)

# Wywołanie metody __iter__ obiektu Iterable w celu utworzenia iteratora 
iterator = iter(iterable)
```

### 10.2. Iterator
Hermetyzuje strategię sekwencyjnego dostępu do elementów kompozytu, bez względu na rzeczywistą ich organizację. Jego zadanie polega na dostarczaniu kolejnych elementów według ustalonego wzorca.
```python
class Iterator:
	def __next__(self):
		return (...)
	def __iter__(self):
		return self # Obiekt iteratora musi mieć zdefiniowaną metodę __iter__, gdzie zwraca samego siebie

iterator = iter(iterable)

# Wywoływanie kolejnych elementów.
element_1 = next(iterator)
element_2 = next(iterator)
```
Gdy nie ma już obiektów do pobrania, przy kolejnej próbie użycia funkcji **next** wystąpi wyjątek *StopIteration*.

Iterator można utworzyć również z "wartownikiem", będącym wartością przerywającą iterację.

```python
# iterator = iter(callable, sentinel)

def function():
	return random.randrange(10)

list(iter(function, 5))
```
### 10.3 Generatory
Generator to inny rodzaj iteratora. Używając kluczowego słowa **yield** wyciągamy następną wartość dostarczoną przez generator, po czym zapamiętuje on swój stan aż do kolejnego jego wywołania przez pętlę lub funkcję **next**. Jednym z benefitów generatorów może być tzw. separation of concernes, czyli oddzielenie iteracji od logiki przetwarzania pojedynczego elementu. 

```python
def create_generator(start, stop, step):
	x = start
	while x < stop:
		yield x # Słowo kluczowe przekształcające funkcję w generator
		x += step
		
generator = create_generator(0, 10, 2.5)
# Logika zawarta w funkcji generatora wykonuje się dopiero po zastosowaniu funkcji next() lub w czasie iteracji w pętli

# next(generator)
for value in generator:
	print(value)
```
Generator można również zdefiniować używając tzw. Generator Comprehensions.
```python
(x**2 for x in range(10) if x % 2 == 0)
```
Jako praktyczny przykład zastosowania generatora można podać operacje na plikach, gdzie logika przetwarzania poszczególnych wierszy, jest oddzielona od in filtrowania, za które odpowiada generator.
```python
def exclude_comments(fp):
	for line in fp:
		if not line.startswith('#'):
			yield line

with open('filename') as fp:
	for line in exclude_comments(fp):
		process(line)
```
Generatory wykorzystują tzw. leniwą ewaluację, która pozwala strumieniowo przetwarzać duże ilości danych bez konieczności wczytywania ich w całości do pamięci.
### 10.4. itertools
Wbudowany w Pythona moduł do obsługi iteracji. Składa się na iteratory nieskończone, kombinatoryczne i pozostałe.

#### 10.4.1. Iteratory nieskończone
```python 
from itertools import *

# Kolejne wartości liczbowe
for i in count(10, 1):
	print(i)

# 10
# 11
# 12
# ...

# Kolejne wartości z listy podawane cyklicznie
for i in cycle(['spring', 'summer', 'fall', 'winter']):
	print(i)

# Powtórzenie tej samej wartości podaną ilość razy, lub w nieskończoność
for i in repeat('hello', 3):
	print(i)
```
####  10.4.2. Iteratory kombinatoryczne
##### 10.4.2.1. product
Iloczyn kartezjański dwóch lub więcej zbiorów (wszystkie możliwe kombinacje wartości).
```python 
from itertools import *


colors = {'black', 'white'}
sizes = {'S', 'M', 'L', 'XL'}
materials = {'cotton', 'polyester', 'lycra'}

for color, size, material in product(colors, sizes, materials):
	print(color, size, material)
	# black S lycra
	# black S cotton
	# ...
	# black M lycra
	# ...
	# white S lycra
	...

# Kombinacja kilku wartości z tego samego zakresu
list(product(range(10), repeat=4))
# [(0, 0, 0, 0),
# (0, 0, 0, 1),
...
# (9, 9, 9, 9)]
```
##### 10.4.2.2. permutations
Możliwe permutacje dla podanego zbioru (możliwe kolejności obiektów w zbiorze).
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in permutations(horses):
	for i, horse in enumerate(outcome, 1):
		print(i, horse)
	print()

# 1 Duke
# 2 Coco
# 3 Star
# 4 Dolly
# 5 Gypsy
# 
# 1 Duke
# 2 Coco
...
```
Możliwe jest również uzyskanie n-elementowych wariacji bez powtórzeń - tutaj w celu uzyskania pierwszych trzech miejsc na podium.
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in permutations(horses, 3):
	for i, horse in enumerate(outcome, 1):
		print(i, horse)
	print()
# 1 Duke
# 2 Coco
# 3 Star
...
```
##### 10.4.2.3. combinations
n-elementowe unikalne podzbiory bez względu na kolejność elementów.
```python 
from itertools import *

horses = {'Coco', 'Dolly', 'Duke', 'Gypsy', 'Star'}

for outcome in combinations(horses, 3):
	print(outcome)
# 1 Duke
# 2 Coco
# 3 Star
...
```
####  10.4.3. Iteratory pozostałe
##### 10.4.3.1. chain
Pozwala na iterowanie po kilku sekwencjach na raz. Po wyczerpaniu elementów w sekwencji chain przechodzi do pobierania elementów z kolejnej z nich.

```python 
from itertools import *

a = [1, 2, 3]
b = ['lorem', 'ipsum']
c = list('abcd')

for x in chain(a, b, c):
	print(x)
```
##### 10.4.3.2. zip
Wbudowana funcja, pozwalająca na iterowanie po kilku listach jednocześnie. Ilość wynikowych elementów determinuje długość najkrótszej z sekwencji.
```python 
from itertools import *

a = [1, 2, 3]
b = ['lorem', 'ipsum']
c = list('abcd')

for x in zip(a, b, c):
	print(x)

# (1, 'lorem', 'a')
# (2, 'ipsum', 'b')
```
Sekwencje tak utworzonych tupli można też odpakować przy użyciu zip.
```python 
from itertools import *

zipped = [(1, 'a'), (2, 'b')]
x, y = zip(*zipped)
print(x)
print(y)
# (1, 2)
# ('a', 'b')
```
##### 10.4.3.3. groupby
Pozwala na grupowanie danych po wskazanym kluczu
```python 
from itertools import *

expenses = [
	(500, 'ZUS', 'firma'),
	(100, 'księgowa', 'firma'),
	(400, 'OC', 'samochód'),
	(60, 'kino', 'rozrywka'),
	(200, 'paliwo', 'samochód'),
	(700, 'drukarka', 'firma'),
]

category = lambda x: x[-1]

for key, values in groupby(sorted(expenses, key=category), key=category):
	print(key, list(values))

# firma [(500, 'ZUS', 'firma'), ...]
# rozrywka [...]
# samochód [...]
```
##### 10.4.3.4. islice
Pozwala na uzyskanie wycinka z iteratora.
```python 
from itertools import *

it = range(int(1e6))
# Wycinek 10 pierwszych elementów z iteratora it zawierającego milion elementów
list(islice(it, 10)
```
### 10.5. Sortowanie
W Pythonie dane można posortować na dwa sposoby używając wbudowanych mechanizmów.
```python 
[2, 1, 3].sort() # sortuje istniejącą listę
sorted([2, 1, 3]) # tworzy posortowaną kopię podanej listy
```
W celu ułatwienia przekazywania klucza sortowania do metody sorted można posłużyć się modułem operator.
#### 10.5.1.  operator.itemgetter
```python 
from operator import *

people = [
	('Jan', 'Kowalski'),
	('Anna', 'Woźniak'),
	('Anna', 'Nowak')
]

sorted(people, key=itemgetter(0, 1)) # itemgetter wyciąga elementy z kolejno z indeksów 0 i 1 w formie krotki dla każdego z obiektów listy people. Lista jest posortowana najpierw względem pierwszej podanej wartości, a następnie drugiej
```
#### 10.5.2. operator.attrgetter
```python 
from operator import *
from collections import namedtuple

Person = namedtuple('Person', 'first_name last_name')

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=attrgetter('first_name', 'last_name')) # attrgetter wyciąga atrybuty kolejno 'first_name' i 'last_name' i sortuje listę obiektów na ich podstawie
```
#### 10.5.3. operator.methodcaller
```python 
from operator import *
from collections import namedtuple

class Person(namedtuple('Person', 'first_name last_name')):
	def get_length(self):
		return len(str(self))

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=methodcaller('get_length')) # methodcaller sortuje listę na podstawie wartości zwróconych przez metodę, której nazwa przekazana jest w argumencie
```
## 11. Programowanie funkcyjne
### 11.1. Funkcje wyższego rzędu (Higher order functions)
#### 11.1.1. map
Wykonuje wskazaną funkcję na każdym elemencie podanej sekwencji i zwraca listę wyników tej funkcji
```python 
# Zwraca iterator pozycji poszczególnych elementów stringa w Unicode
map(ord, 'zażółć gęślą jaźń') 
```
#### 11.1.2. filter
Filtruje sekwencje bazując podanej funkcji.
```python 
filter(str.isupper, 'Hello World') 
```
#### 11.1.3. functools.reduce
Iteruje po elementach sekwencji i redukuje ją do pojedynczej wartości.
**Przykład 1: Sumowanie liczb**
```python
import operator
from functools import reduce
 
numbers = [42, 15, 2, 33]

# Pierwsza wartość funkcji to tzw. akumulator, na którym wykonywane są operacje bazujące na drugim argumencie
def f(subtotal, number):
	return subtotal + number

#reduce(f, numbers)
reduce(operator.add, numbers)
```
**Przykład 2: Grupowanie liczb parzystych i nieparzystych**
```python
import operator
from functools import reduce
 
numbers = [42, 15, 2, 33]

def f(grouped, number):
	key = 'even' if number % 2 == 0 else 'odd'
	grouped[key].append(number)
	return grouped

reduce(f, numbers, {'even': [], 'odd': []})
```
### 11.2. Funkcje zagnieżdżone
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
### 11.3. Zasięg zmiennych
Wartości zmiennych wyszukiwane są w kolejności LEGB - local, enclosed, global, built-in.
```python
%reset -f

x = 'global'

def outer():
	x = 'enclosed'
	def inner():
		x = 'local'
		print(x)
	inner()
	print(x)

outer()
print(x)

# local
# enclosed
# global
```
### 11.4. Domknięcia
Zapamiętuje wartości tzw. zmiennych wolnych (nonlocal) w swoim zasięgu leksykalnym. Domknięcia pozwalają dołączać pewien stan do funkcji, a także metody manipulowania tym stanem, jak np, ze zmienną color i metodą set_color z przykładu poniżej. Domknięcia są stosowane np. przy tworzeniu dekoratorów.
```python
def tag(name):
	color = 'black'
	def wrap(text):
		return f'<{name} style="color: {color}">{text}</{name}>'
	def set_color(value):
		nonlocal color
		color = value
	wrap.set_color = set_color
	return wrap
p = tag('p')
p('Python')
```

### 11.5. Funkcje cząstkowe
Funkcje wykonujące działanie innej funkcji, ale z mniejszą wymaganą do podania liczbą argumentów.

```python
from functools import partial

def quadratic(x, a, b, c):
	return a*x**2 + b*x + c

# Funkcja cząstkowa - zapis 1
def y(x):
	return quadratic(x, 3, 1, -4)

# Funkcja cząstkowa - zapis 2
y = partial(quadratic, a=3, b=1, c=-4)
```
## 12. PROGRAMOWANIE OBIEKTOWE
### 12.1. Kopiowanie obiektów
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
### 12.2. Klasy abstrakcyjne
Użycie klas abstrakcyjnych pozwala na wymuszenie zaimplementowania wszystkich abstrakcyjnych metod w klasach pochodnych od abstrakcyjnej klasy bazowej.

```python
import abc
import json

class Plugin(metaclass=abc.ABCMeta):
	"""Abstract base for plugins."""
	
	@abc.abstractmethod
	def load(self, path)
		"""Return a dict with values from the given file."""
	
	@abc.abstractmethod
	def save(self, data, path)
		"""Serialize data and save it to the given file."""


class JsonPlugin(Plugin):

	def load(self, path):
		with open(path) as fp:
			return json.load(fp)
	
	def save(self, data, path):
		with open(path, 'w') as fp:
			json.dump(data, fp, indent=4, sort_keys=True)
```
### 12.3. Przeciążanie funkcji
Python nie obsługuje przeciążania funkcji i metod, ale można za to dostosować działanie funkcji w zależności od przyjętych przez nią argumentów. Najprościej zrobić to przez użycie isinstance, ale jest to antywzorzec. Zamiast tego można wykorzystać metodę singledispatch.
```python
from functools import singledispatch

# Zdefiniowanie wzorca funkcji
@singledispatch
def pretty_print(x):
	print(x)

# Zarejestrowanie specjalnego działania funkcji po podaniu jej listy oraz tupli jako argumentu
@pretty_print.register(list)
@pretty_print.register(tuple)
def _(items):
	for i, value in enumerate(items):
		print(f'[{i}] = {value}')
```

Powyższe rozwiązanie nie zadziała dla metod w klasie oraz nie obsługuje więcej niż jednego argumentu. Aby rozwiązać ten drugi problem można skorzystać z zewnętrznej biblioteki multipledispatch.

```python
from multipledispatch import dispatch

@dispatch(int, int)
def add(x, y):
	return x + y

@dispatch(object, object)
def add(x, y):
	return f'{x} + {y}'
```
### 12.4. Przeciążanie operatorów
Przykład przeciążania operatora dodawania i dodawania prawostronnego klasy namedtuple.

```python
from collections import namedtuple

class Vector(namedtuple('Vector', 'x y'):
	def __add__(self, other):
		if isinstance(other, Vector):
			return Vector(*map(sum, zip(self, other)))
		elif isinstance(other, int):
			return Vector(self.x + other, self.y + other)
	
	def __radd__(self, other):
		return self + other
```

#### 12.4.1. __repr__ i __str__
Metoda \_\_str__ powinna zwracać reprezentację obiektu do czytania przez ludzi, natomiast metoda \_\_repr__ powinna zawierać zapis (najlepiej kod Pythona) umożliwiający odtworzenie danego obiektu po wklejeniu do funkcji eval.
```python
class Vector:
	def __init__(self, x, y)
		self.x, self.y = x, y
	
	def __str__(self):
		return f'A vector of {self.x}, {self.y}'
	
	def __repr__(self):
		return f'Vector({self.x}, {self.y})'

a = Vector(3, -4)
str(a) # 'A vector of 3, -4'
b = eval(repr(a)) # Nowa instancja wektora Vector(3, -4)
```
### 12.5. Metody
#### 12.5.1. Metody klasowe
Metoda klasowa to taka, która zawiera odwołanie nie do konkretnej instancji obiektu, ale do samej klasy. Może być wywoływana bez inicjowania obiektu.
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@classmethod
	def monaco_blue(cls):
		return cls(0.2, 0.5, 0.75)
		
	@classmethod
	def exotic_red(cls):
		return cls(1, 0, 0)
	
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))

Color.monaco_blue() # zwraca obiekt z metody klasowej Color(0.2, 0.5, 0.75)
```
#### 12.5.2. Metody statyczne
Nie posiadają odniesienia ani do danego obiektu, ani do samej klasy - zachowują się bardziej jak zwykłe funkcje, niż metody. Z optymalizacyjnego punktu widzenia nie są one dobrym rozwiązaniem, ponieważ wiążę się z dodatkowym kosztem ze względu na przeglądanie przez Pythona przestrzeni nazw w trakcie działania programu. Jedynym logicznym zastosowaniem @staticmethod jest ich pogrupowanie pod jedną, wspólną przestrzenią nazw klasy
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@staticmethod
	def blend(color1, color2, alpha=0.5)
		return color1*alpha + color2*(1-alpha)
		
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))
	
	def __mul__(self, scalar):
		return Color(*[x*scalar for x in self])
	
	def __add__(self, other):
		return Color(*[sum(x) for x in zip(self, other)])
```

### 12.6. @property
Dekorator @property, pozwala na utworzenie właściwości obiektu, do której dostęp można uzyskać przy użyciu kropki, tak samo jak do atrybutów definiowanych w konstruktorze. Właściwości obiektu są jednak możliwe do nadpisania tylko po zdefiniowaniu settera.
```python
class Person:
	def __init__(self, name, married=False):
		self._name = name
		self.married = married
	
	@property
	def name(self):
		return self._name
	
	@property
	def married(self):
		return self._married
	
	@married.setter
	def married(self, value):
		if not(isinstance(valie, bool):
			raise TypeError('married must be bool')
		self._married = value
	
	@married.deleter
	def married(self):
		del self._married
```
## 13. METAPROGRAMOWANIE
### 13.1. Dekoratory
Funkcja, przyjmująca jako argument funkcję i zwracająca funkcję. 
```python
def password():
	return 'top_s3cret'

def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

encrypted_password = encrypted(password)
encrypted_password()
```
Powyższy zapis można skrócić do następującego:
```python
def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

@encrypted
def password():
	return 'top_s3cret'

password()
```
Jednym z głównych celów zastosowania dekoratorów jest memoizacja, czyli cache'owania wyników funkcji w celu przyspieszenia obliczeń. Poniżej przykład zastosowania dekoratora cache'ującego wyniki rekurencyjnych wyników wywołań wyliczających składniki ciągu Fibonacciego. 
```python
# import functools
def cache(function):
	history = {}
	def wrapper(n):
		if n not in history:
			history[n] = function(n)
		return history[n]
	return wrapper
	
# @functools.lru_cache(maxsize=128)
@cache
def fib(n):
	return 1 if n < 2 else fib(n-2) + fin(n-1)
```
Dekoratory mogą też przyjmować więcej parametrów niż samą dekorowaną funkcję, ale wymaga to dodatkowego poziomu zagnieżdżenia.
```python
import functools

def ignore(ExceptionClass):
	def decorator(function):
		@functools.wraps(function) # pozwala na przekazanie metadanych (np. __name__) funkcji w argumencie do dekorowanej funkcji
		def wrapper(*args, **kwargs):
			try:
				return function(*args, **kwargs)
			except ExceptionClass as ex:
				pass
		return wrapper
	return decorator

@ignore(ZeroDivisionError)
def divide(a, b):
	return a / b
```
### 13.2. Menedżer kontekstu
Obiekt implementujący interfejs składający się z dwóch magicznych metod - \_\_enter__ oraz \_\_exit__, które umożliwiają jego użycie w konstrukcji with. Menedżer kontekstu przydaje się w takim razie do zarządzania stanem, który musi zostać najpierw zainicjowany, a następnie uwolniony, żeby nie dopuścić do wycieków pamięci. Menedżer kontekstu można zdefiniować klasowo albo funkcyjnie.
```python
from time import time

class MockedTime:
	def __enter__(self):
		# tymczasowe nadpisanie funkcji time
		global time
		self._time = time
		time = lambda: 42
	
	def __exit__(self, exception_class, exception, traceback):
		# powrót do domyślnej funkcji time
		global time
		time = self._time

with MockedTime():
	print(time())
print(time())
```
```python
from time import time, sleep

class Timed:
	def __enter__(self):
		self.t1 = time()
		return self # pozwala na przypisanie menedżera do zmiennej poprzez słówo "as" w konstukcji "with"
	
	def __exit__(self, *args):
		self.t2 = time()
	
	@property
	def delta(self):
		return self.t2 - self.t1

with Timed() as timed:
	sleep(0.5)

print(timed.delta)
```
Do utworzenia menedżera kontekstu jako funkcji służy biblioteka contextlib.
```python
from contextlib import contextmanager

@contextmanager
def logging():
	print('__enter__')
	try:
		yield
	finally:
		print('__exit__')

with logging() as value:
	print('The value is:', value)
```
Instrukcja yield dzieli zawiesza działanie funkcji i dzieli ją na dwie części. Pierwsza część odpowiada instrukcji \_\_enter__, w której dokonuje się inicjalizacji. Druga część (za yield) odpowiada za to instukcji \_\_exit__. Konieczne jest opakowanie słówa kluczowego yield blokiem try/finally, ponieważ w innym razie, w przypadku wystąpienia wyjątku nie doszłoby do "zamknięcia" menedżera kontekstu.
### 13.2. Deskryptor
Można go sobie wyobrazić jako property wielokrotnego użytku, które może być wykorzystywane w wielu klasach. Zgodnie z definicją, jest to klasa definiująca jedną z trzech magicznych metod: \_\_get__, \_\_set__, \_\_delete__. Występują szczególne przypadki: 
* data descriptor - definiuje wszystkie trzy metody
* non data descriptor - definiuje tylko metodę \_\_get__. Pozwalają na leniwą inicjalizację atrybutów w klasie

Pożej przykład zastosowania domknięcia wykorzystującego dekorator property do przypisania niezmiennych atrybutów w klasie.
```python
# Zwrócenie wartości atrybutu _attr przy próbie wyciągnięcia atrybutu poprzez Class.attr
def read_only(name):
	@property
	def getter(self):
		return getattr(self, '_' + name)
	return getter

class Person:
	name = read_only('name')
	married = read_only('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
Ten sam problem można rozwiązać przy użyciu deskryptora:
```python
class ReadOnly:
	def __init__(self, name)
		self.name = name
	
	def __get__(self, obj, cls):
		if obj is None:
			return self
		return getattr(obj, '_' + self.name)
	
	def __set__(self, obj, value):
		raise AttributeError

class Person:
	name = ReadOnly('name')
	married = ReadOnly('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
