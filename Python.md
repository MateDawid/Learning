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

### Co to jest  `__init__`  w Pythonie?

Jest to metoda specjalna wywoływana automatycznie podczas po utworzeniu instancji klasy. Dzięki niej możliwe jest na przykład doczytanie kodu czy automatycznie dodanie atrybutów zawsze, gdy tworzony będzie nowy obiekt lub instancja. Pozwala także odróżnić metody i atrybuty klasy od lokalnych zmiennych.

### Czym w Pythonie jest  `lambda`?

Lambda w Pythonie to funkcja, która może przyjąć każdą liczbę argumentów, ale mieć tylko jedno wyrażenie. Co ważne, jest to funkcja anonimowa, a zatem nie jest powiązana z żadnym identyfikatorem. Pozwala wyeliminować funkcję zainicjowane na potrzeby funkcji wyższego rzędu i przekazać jej parametry
Programista Python to coraz częściej wybierana ścieżka kariery. Warto wiedzieć, jak przygotować się do rozmów kwalifikacyjnych na stanowisko  [Python Developera](https://bulldogjob.pl/companies/jobs/s/skills,Python)  i poznać najważniejsze zagadnienia, pytania i zadania rekrutacyjne!

Rozkwit popularności Pythona w ostatnich latach robi wrażenie – w niektórych rankingach popularności języków programowania zajmuje on już pierwsze miejsce, prześcigając JavaScript i Javę. Nieskomplikowana składnia, łagodna krzywa uczenia, brak konieczności korzystania z komercyjnych IDE – wszystkie te czynniki zachęcają do nauki i rozwoju kariery właśnie w kierunku stanowisk, na których wymagana jest znajomość Pythona.

Zanim jednak to zrobimy, warto zwrócić uwagę, że Python, wśród aktualnie popularnych języków programowania, jest jednym z najbardziej wszechstronnych. To oczywiście pociąga za sobą konsekwencje – nieco inny zestaw pytań otrzyma kandydat aplikujący na stanowisko związane z  [Django](https://bulldogjob.pl/news/1908-czy-warto-uczyc-sie-django), inny natomiast w firmach zajmujących się  [machine learningiem](https://bulldogjob.pl/news/324-kiedy-machine-learning-ma-sens).

Trzeba więc brać poprawkę na specjalizację i zgromadzone tu informacje rozszerzyć o te, które związane są już z konkretnym obszarem. My skupiliśmy się na zebraniu najbardziej uniwersalnych zagadnień, pytań i zadań, których spodziewać może się każdy, od kogo wymagana na danym stanowisku będzie znajomość Pythona.

##   
Rozmowa kwalifikacyjna

Rozmowa kwalifikacyjna na stanowisko Python Developera rozpoczyna się zazwyczaj od pytań ogólnych, które mają sprawdzić jeszcze nie tylko kompetencje techniczne, ale miękkie umiejętności kandydata. Wśród nich należy wskazać kompetencje komunikacyjne, umiejętność klarownego przekazywania swoich pomysłów i pracy zespołowej. Podobnie jak w przypadku innych stanowisk, warto jeszcze przed rozmową zadbać o aktywność w portalach społecznościowych, zwłaszcza na LinkedIn.

Kolejnym ważnym elementem jest przygotowanie własnego developerskiego portfolio, które będzie dowodzić nie tylko umiejętności programistycznych i prezentować dotychczasowe doświadczenia, ale także dowodzić, że oprócz pracy zawodowej kandydat programuje także hobbystycznie i pracuje nad autorskimi projektami. Często zdarza się bowiem, że po zapoznaniu się z portfolio kandydata, rekrutujący rezygnuje z wymogu rozwiązania zadań rekrutacyjnych.

Dalsze etapy będą sprawdzały konkretną wiedzę o Pythonie i programowaniu w ogóle. Spodziewać można się między innymi o omówienie typów wbudowanych:

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

Warto także odświeżyć sobie informację o najważniejszych bibliotekach standardowych:

-   `random`  – biblioteka służąca do pseudolosowego generowania liczb,
-   `datatime`  – moduł pozwalający na pracę z datą i godziną,
-   `json` – zapisuje listy, logikę, liczby, krotki i słowniki do pliku JSON,
-   `os`  – moduł pozwalający na integrację z systemem plików OS-a,
-   `logging`  – biblioteka z API pozwalającym na zapisywanie logów.

Można się także spodziewać sprawdzianu wiedzy w zakresie najpopularniejszych frameworków i bibliotek. Oto ich przykłady:

-   **Django**  – najpopularniejszy framework wykorzystywany do opracowywania aplikacji webowych czy po prostu web developmentu. Jego zaletą jest generowany automatycznie panel administracyjny, który w przejrzysty sposób umożliwia zarządzanie witryną i konfigurację.
-   **Flask**  – to także framework aplikacji przeglądarkowych, jednak w porównaniu z Django jest on znacznie prostszy i stanowi mikroframework – nie wymaga zatem do działania wcześniejszej instalacji żadnych zewnętrznych bibliotek. Ograniczoną domyślnie funkcjonalność można rozbudowywać w pożądanym kierunku za pomocą rozszerzeń.
-   **FastAPI**  – jak wskazuje sama nazwa, jest to framework pozwalający na budowanie API RESTful. Obsługuje programowanie asynchronicznie, jest stosunkowo prosty w obsłudze i bardzo wydajny. Kompatybilny z OpenAPI i JSON Schema.
-   **PyTorch**  – rozbudowana biblioteka wykorzystywana do machine learningu. Umożliwia przeprowadzanie obliczeń tensorowych z pełną akceleracją GPU. Dysponuje licznymi API pozwalającymi na rozwiązywanie problemów aplikacji związanych z integracją z sieciami neuronowymi, świetnie radzi sobie z przetwarzaniem języka naturalnego.
-   **Pandas**  – to biblioteka wykorzystywana przez Analityków danych, pozwala zarządzać strukturami danych i przeprowadzać operacje na tablicach numerycznych i szeregach czasowych. Obsługuje dane zapisane pochodzące z plików JSON, baz SQL, a nawet z arkuszy Excela.

Przed rozmową warto także odświeżyć sobie pozostałe najważniejsze zagadnienia, na czele z  **asynchronicznością i współbieżnością**, czy też  **funkcje języka**. Ponadto konieczna będzie przynajmniej podstawowa znajomość funkcjonowania  **relacyjnych baz danych**  i  **SQL**.

##   
Przykładowe pytania

Po omówieniu zagadnień związanych ogólnie ze specyfiką Pythona i jego cechami charakterystycznymi możemy się spodziewać serii bardziej szczegółowych pytań. Zebraliśmy te z nich, które padają najczęściej, wraz z odpowiedziami.

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
