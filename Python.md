
# **PYTHON**
## WŁAŚCIWOŚCI JĘZYKA
### Przestrzenie nazw  
W pewnym sensie powiązane z zakresami są przestrzenie nazw. Są to zakresy zapewniające nam to, że nazwa danego obiektu będzie unikalna i że można z nich będzie korzystać bez ryzyka wystąpienia jakichkolwiek konfliktów. To swojego rodzaju zbiór nazw i definicji, które mogą mieć zastosowanie lokalne (podobnie jak zakresy, w obrębie funkcji), ale także globalnie, które określają nazwy dla całego kodu, zaimportowanych paczek. W Pythonie funkcjonują także wbudowane przestrzenie nazw kluczowych funkcji w tym języku, dzięki którym możemy mieć pewność, że utworzony przez nas obiekt nie będzie w konflikcie z którąkolwiek z wbudowanych funkcji Pythona.  
### Różnica między modułem i paczką  
Zarówno moduły jak i paczki wykorzystywane są do modularyzacji kodu, co przekłada się na jego łatwość w utrzymaniu i ułatwia pracę z omówionymi już zakresami. Moduły są plikami zawierający zestaw zdefiniowanych instrukcji, klas i zmiennych. Można zaimportować zarówno całe moduły, jak i ich części.  
Paczka w Pythonie zazwyczaj składa się z kilku modułów. Jest ona jednak na tyle przydatna, że określa dla nich przestrzenie nazw i eliminuje konflikty pomiędzy poszczególnymi modułami.  
### Zakresy  
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
###   Typy wbudowane  
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

### PYTHONPATH  
`PYTHONPATH` to zmienna środowiskowa pozwalająca wskazać dodatkowe lokalizacje, z których Python będzie mógł zaciągnąć moduły i paczki.  
### PEP8  
PEP 8 to opracowany jeszcze w 2001 r. dokument, w którym opisane zostały najlepsze praktyki w zakresie pisania czytelnego kodu w Pythonie. Stanowi część oficjalnej dokumentacji języka. Stanowi on powszechnie respektowaną normę i w zasadzie stanowi lekturę obowiązkową dla każdego, kto chce programować w Pythonie. Z treścią dokumentu zapoznać się można na  [oficjalnej stronie Pythona](https://www.python.org/dev/peps/pep-0008/#introduction).
## SYNTAX
### Różnica między 'is', a '=='
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
### Porównania łańcuchowe
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
### lambda  
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
### map i filter
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
### Dekoratory
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
### Generatory
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
## STRING
### Zamiana elementów stringa
```python
a = "abcdefg"            # do zmiennej a przypisz zostaje string 'abcdefg'
print(a[1])              # wydrukuj element znajdujący się pod indeksem 1 w stringu a
# a[1] = 'X'             # próba modyfikacji stringa - operacja zabroniona skutkująca TypeError
a_list = list(a)        # stwórz listę a_list zawierającą litery ze stringa a
a_list[1] = 'X'         # zmodyfikuj zawartość listy pod indeksem 1
a = "".join(a_lista)     # stwórz stringa a łącząc elementy listy a_list przy użyciu pustego separatora ""
print(a)
```
## LIST
### Lista niepowtarzalnych elementów
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
### Różnice między listą i krotką
```python
L = [1, 2, 3, True, (1, 2)]
T = (4, 5, 6, False, ['x', 'y'])
L[2] = 'trzy'   # modyfikacja zawartości listy - operacja legalna
T[2] = 'sześć'  # próba modyfikacji zawartości tupli - operacja zabroniona, skutkuje TypeError
```
### Różnice między listą i tablicą  
Tablice w Pythonie są homogeniczne. Oznacza to, że zawierają dane tylko i wyłącznie jednego typu. W przypadku list nie ma tego ograniczenia i swobodnie można wewnątrz nich zawrzeć np. liczby i stringi. Warto wspomnieć, że homogeniczne listy zużywają znacznie mniej pamięci.  
### Kopiowanie list
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
### Odwrócenie listy
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
### List comprehension
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
## DICTIONARY
### Poprawne tworzenie słowników
Klucze słownika muszą być elementem niemutowalnym, a więc mogą być typu int, string lub tuple, ale nie mogą być listą lub innym słownikiem.
```python
A = {1: 1, 2: 4, 3: 9}
B = {'imie': 'Anna', 'nazwisko': 'Kowalska'}
# C = {[4, 5]: [16, 25]}    # lista jako element mutowalny nie może byc kluczem słownika!
D = {(4, 5): [16, 25]}
# E = {{1:2}: 'jeden_dwa'}  # słownik jako element mutowalny równiez nie może być kluczem!
```
### Dict comprehension
```python
L = [1,2,3,4,5,6]
D1 = {x:x % 2 == 0 for x in L}   
# pary klucz:wartość, gdzie kluczem są elementy z listy L a wartościami 
# True lub False, w zależności od tego czy dany klucz jest podzielny przez 2
```
## KLASY
### init 
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
## USE CASES
### Palindrom
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
### Ciąg Fibonacciego
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
### Tworzenie plików
```python
with open('file.txt', 'w') as f:    # otwórz plik 'file.txt' w wersji do zapisu ('w' od write), nadaj mu alias f
    for n in range(1, 101):             # dla kolejnych liczb z zakresu od 1 do 100
        f.write(str(n) + '\n')          # wpisz do pliku stringa utworzonego na podstawie liczby oraz znak nowej linii '\n'

with open('file.txt', 'r') as f:    # otwórz plik 'file.txt' w wersji do odczytu ('r' od read), nadaj mu alias f
    file_lines = f.readlines()             # do listy file_lines wpisz kolejne linijki przeczytane z pliku 'file.txt'
                                        # każda linijka będzie osobnym elementem listy
```
## TESTY
### assert
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
### Biblioteka unittest
```python
# Import the unittest library and our function
import unittest

class Tests(unittest.TestCase):

    def test_1(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
```
## KONTENERY DANYCH
### ARRAY
Struktura danych przypominająca działaniem array stosowany np. w C i służy między innymi do komunikacji z softem pisanym w tym języku. 
```python
import array

# Konieczne zadeklarowanie typu zmiennych.
example = array.array('b')
```
### ChainMap
Struktura umożliwiająca połączenie dwóch słowników. W przypadku, gdy w którymś ze składowych słowników zajdzie jakaś zmiana, będzie ona uwzględniona w obiekcie ChainMap.
```python
from collections import ChainMap

d1 = {'color': 'red'}
d2 = {'pet': 'cat'}

d = dict(ChainMap(d1, d2))  # {'color': 'red', 'pet': 'cat'}

maps = d,maps # lista słowników w kolejności, w jakiej zostały dodane[{'color': 'red'}, {'pet': 'cat'}]
```
Przy próbie podania wartości dla już istniejącego klucza w ChainMap pozostanie pierwotna wartość.

### Counter
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
### defaultdict
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
Ten sam efekt można uzyskać używając defaultdict.

```python
from collections import defaultdict

names_by_length = defaultdict(list)
# argument "list" oznacza, że przy próbie wyciągnięcia danych dla nieistniejącego klucza zostanie utworzona pusta lista

for name in ('bob', 'alice', 'max', 'adam', 'eve'):
	names_by_length[key].append(name)
	
# names_by_length = {3: ['bob', 'max', 'eve'], 4: ['adam'], 5: ['alice']}
```
### OrderedDict
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
### deque
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
### namedtuple
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
### enum

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
