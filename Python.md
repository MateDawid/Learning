## **PYTHON**

Typy wbudowane:
-   `str`  – string, tekstowy typ danych,
-   `int`  – liczba,
-   `float`  – liczba zmiennoprzecinkowa,
-   `complex`  – liczba zespolona,
-   `list`  – lista
-   `tuple`  – kortka
-   `range`  – zakres, liczby naturalne stanowiące szereg arytmetyczny,
-   `dict`  – słownik,
-   `set`  – zbiór,
-   `frozenset`  – zbiór niemutowalny,
-   `bool`  – logika boolowska,
-   `bytes`  – konwersja ciągu na bajty,
-   `bytearray`  – mutowalny wariant bytes,
-   `memoryview`  – dostęp do wewnętrznych danych obiektów obsługujących bufory protokołów.


###   Co to jest  `__init__`  w Pythonie?

Jest to metoda specjalna wywoływana automatycznie podczas po utworzeniu instancji klasy. Dzięki niej możliwe jest na przykład doczytanie kodu czy automatycznie dodanie atrybutów zawsze, gdy tworzony będzie nowy obiekt lub instancja. Pozwala także odróżnić metody i atrybuty klasy od lokalnych zmiennych.

###   Czym w Pythonie jest  `lambda`?

Lambda w Pythonie to funkcja, która może przyjąć każdą liczbę argumentów, ale mieć tylko jedno wyrażenie. Co ważne, jest to funkcja anonimowa, a zatem nie jest powiązana z żadnym identyfikatorem. Pozwala wyeliminować funkcję zainicjowane na potrzeby funkcji wyższego rzędu i przekazać jej parametry

###   Jak kopiuje się obiekty w Pythonie?

W Pythonie kopiowanie nie odbywa się z użyciem operatora  `=`. Wówczas jedynie tworzymy powiązanie istniejącym już obiektem a docelową nazwą zmiennej. Zamiast wspomnianego operatora, w Pythonie wykorzystuje się moduł copy. Mamy dzięki niemu dwie możliwości kopiowania: płytkie i głębokie. W pierwszym przypadku tworzy się bitową kopię 1:1, zaś głęboka kopia pozwala na re kursywne kopiowanie wszystkich wartości. Składnia:

```python
list_1 = [1, 2, 3]
list_2 = copy(list_1) # płytkie kopiowanie
list_3 = deepcopy(list_1) # głębokie kopiowanie
```
### Czym w Pythonie są zakresy?

Zakresy, czy też scope’y, w Pythonie nie różnią się od tego, co znamy z innych języków programowania. Scope to blok kodu, w którym działa dany obiekt i tylko w nim jest dostępny. Na przykład lokalny zakres odnosi się do wszystkich obiektów w danej funkcji, zaś zakres globalny będzie zawierał wszystkie obiekty w całym kodzie.

### Czym są przestrzenie nazw w Pythonie?

W pewnym sensie powiązane z zakresami są przestrzenie nazw. Są to zakresy zapewniające nam to, że nazwa danego obiektu będzie unikalna i że można z nich będzie korzystać bez ryzyka wystąpienia jakichkolwiek konfliktów. To swojego rodzaju zbiór nazw i definicji, które mogą mieć zastosowanie lokalne (podobnie jak zakresy, w obrębie funkcji), ale także globalnie, które określają nazwy dla całego kodu, zaimportowanych paczek. W Pythonie funkcjonują także wbudowane przestrzenie nazw kluczowych funkcji w tym języku, dzięki którym możemy mieć pewność, że utworzony przez nas obiekt nie będzie w konflikcie z którąkolwiek z wbudowanych funkcji Pythona.

### Czym są przestrzenie nazw w Pythonie?

W pewnym sensie powiązane z zakresami są przestrzenie nazw. Są to zakresy zapewniające nam to, że nazwa danego obiektu będzie unikalna i że można z nich będzie korzystać bez ryzyka wystąpienia jakichkolwiek konfliktów. To swojego rodzaju zbiór nazw i definicji, które mogą mieć zastosowanie lokalne (podobnie jak zakresy, w obrębie funkcji), ale także globalnie, które określają nazwy dla całego kodu, zaimportowanych paczek. W Pythonie funkcjonują także wbudowane przestrzenie nazw kluczowych funkcji w tym języku, dzięki którym możemy mieć pewność, że utworzony przez nas obiekt nie będzie w konflikcie z którąkolwiek z wbudowanych funkcji Pythona.

###   Jaka jest różnica pomiędzy modułem i paczką w Pythonie?

Zarówno moduły jak i paczki wykorzystywane są do modularyzacji kodu, co przekłada się na jego łatwość w utrzymaniu i ułatwia pracę z omówionymi już zakresami. Moduły są plikami zawierający zestaw zdefiniowanych instrukcji, klas i zmiennych. Można zaimportować zarówno całe moduły, jak i ich części.

Paczka w Pythonie zazwyczaj składa się z kilku modułów. Jest ona jednak na tyle przydatna, że określa dla nich przestrzenie nazw i eliminuje konflikty pomiędzy poszczególnymi modułami.

###   Czym w Pythonie różni się lista od tablicy?

Tablice w Pythonie są homogeniczne. Oznacza to, że zawierają dane tylko i wyłącznie jednego typu. W przypadku list nie ma tego ograniczenia i swobodnie można wewnątrz nich zawrzeć np. liczby i stringi. Warto wspomnieć, że homogeniczne listy zużywają znacznie mniej pamięci.

###   Co to jest  `PYTHONPATH`?

`PYTHONPATH`  to zmienna środowiskowa pozwalająca wskazać dodatkowe lokalizacje, z których Python będzie mógł zaciągnąć moduły i paczki.

###   Czym jest PEP 8?

PEP 8 to opracowany jeszcze w 2001 r. dokument, w którym opisane zostały najlepsze praktyki w zakresie pisania czytelnego kodu w Pythonie. Stanowi część oficjalnej dokumentacji języka. Stanowi on powszechnie respektowaną normę i w zasadzie stanowi lekturę obowiązkową dla każdego, kto chce programować w Pythonie. Z treścią dokumentu zapoznać się można na  [oficjalnej stronie Pythona](https://www.python.org/dev/peps/pep-0008/#introduction).
