# WŁAŚCIWOŚCI JĘZYKA
## 1.1. Przestrzenie nazw  
W pewnym sensie powiązane z zakresami są przestrzenie nazw. Są to zakresy zapewniające nam to, że nazwa danego obiektu będzie unikalna i że można z nich będzie korzystać bez ryzyka wystąpienia jakichkolwiek konfliktów. To swojego rodzaju zbiór nazw i definicji, które mogą mieć zastosowanie lokalne (podobnie jak zakresy, w obrębie funkcji), ale także globalnie, które określają nazwy dla całego kodu, zaimportowanych paczek. W Pythonie funkcjonują także wbudowane przestrzenie nazw kluczowych funkcji w tym języku, dzięki którym możemy mieć pewność, że utworzony przez nas obiekt nie będzie w konflikcie z którąkolwiek z wbudowanych funkcji Pythona.  
## 1.2. Różnica między modułem i paczką  
Zarówno moduły jak i paczki wykorzystywane są do modularyzacji kodu, co przekłada się na jego łatwość w utrzymaniu i ułatwia pracę z omówionymi już zakresami. Moduły są plikami zawierający zestaw zdefiniowanych instrukcji, klas i zmiennych. Można zaimportować zarówno całe moduły, jak i ich części.  
Paczka w Pythonie zazwyczaj składa się z kilku modułów. Jest ona jednak na tyle przydatna, że określa dla nich przestrzenie nazw i eliminuje konflikty pomiędzy poszczególnymi modułami.  
## 1.3. Zakresy  
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
##   1.4. Typy wbudowane  
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

## 1.5. PYTHONPATH  
`PYTHONPATH` to zmienna środowiskowa pozwalająca wskazać dodatkowe lokalizacje, z których Python będzie mógł zaciągnąć moduły i paczki.  
## 1.6. PEP8  
PEP 8 to opracowany jeszcze w 2001 r. dokument, w którym opisane zostały najlepsze praktyki w zakresie pisania czytelnego kodu w Pythonie. Stanowi część oficjalnej dokumentacji języka. Stanowi on powszechnie respektowaną normę i w zasadzie stanowi lekturę obowiązkową dla każdego, kto chce programować w Pythonie. Z treścią dokumentu zapoznać się można na  [oficjalnej stronie Pythona](https://www.python.org/dev/peps/pep-0008/#introduction).
