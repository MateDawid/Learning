# **pytest**
## 1. Instalacja
Instalacja biblioteki pytest oraz pluginu do sprawdzenia pokrycia kodu testami.
```commandline
pip install pytest
pip install pytest-cov
```
## 2. Podstawowe operacje
Żeby zdefiniować test konieczne jest utworzenie funkcji rozpoczynającej się od słowa "test". Przykład:
```python
def test_sum() -> None:  
    a = 1
    b = 2  
    assert a + b == 3
```
Uruchomienie testów w bieżącym katalogu:
```commandline
pytest
```
Uruchomienie sprawdzenia pokrycia kodu testami:
```commandline
pytest --cov
```
Raport o pokryciu testami i ze wskazaniem nieprzetestowanych fragmentów kodu:
```commandline
coverage html
```
## 3. Uruchomienie testów
W celu uruchomienia napisanych testów w konsoli należy wpisać następującą komendę:
```
py.test
```

## 4.  Testowanie wyjątków
Jeżeli dany test ma sprawdzić wystąpienie wyjątku, należy użyć konstrukcji **with pytest.raises([nazwa_wyjątku])**.
```python
from pay.processor import PaymentProcessor  
import pytest  
  
API_KEY = "6cfb67f3-6281-4031-b893-ea85db0dce20"  

def test_api_key_invalid() -> None:  
    with pytest.raises(ValueError):  
        processor = PaymentProcessor("")  
        processor.charge("1249190007575069", 12, 2024, 100)
```
## 6. Parametryzacja testów
Żeby uniknąć konieczności kopiowania i wykonywania testów dla różnych danych możliwe jest parametryzowanie testów.
Testujemy metodę find_hashtags() klasy Twitter, która wyszukuje słów oznaczonych hashtagiem w podanej wiadomości.
```python
class Twitter:  
	...  
    def find_hashtags(self, message):  
        return [m.lower() for m in re.findall("#(\w+)", message)]
```
Żeby przetestować różne przypadki test dla takiej metody można sparametryzować używając dekoratora @pytest.mark.parametrize.
```python
@pytest.mark.parametrize("message, expected", (  
	("Test #first message", ["first"]),  
	("#first Test message", ["first"]),  
	("#FIRST Test message", ["first"]),  
	("Test message #first", ["first"]),  
	("Test message #first #second", ["first", "second"]),  
))  
def test_tweet_with_hashtag(message, expected):  
    twitter = Twitter()  
    assert twitter.find_hashtags(message) == expected
```
Jako pierwszy argument dekoratora podane są nazwy zmiennych, które chcemy przekazać do testu (w tym przypadku "message" oraz "expected"). Jako drugi argument przekazana jest tupla, zawierające poszczególne zestawy wartości do testowania.
## 7. Fixtures
### 7.1. Podstawowy fixture
W celu przygotowania parametrów wejściowych do testów, które można wielokrotnie wykorzystać używa się tzw. fixtures. 
Mamy dwa testy testujące klasę Twitter. W obu tych testach inicjalizowany jest obiekt klasy Twitter.
```python
def test_twitter_initialization():
	twitter = Twitter()
    assert twitter

def test_tweet_single_message():  
    twitter = Twitter()  
    twitter.tweet('Test message')  
    assert twitter.tweets == ['Test message']
```
Żeby uniknąć takiej redundancji można utworzyć fixture przy użyciu dekoratora @pytest.fixture.
```python
@pytest.fixture  
def twitter():  
    twitter = Twitter()  
    return twitter
```
Tak zdefiniowany dekorator można przekazać do testu jako argument o takiej samej nazwie, jak nazwa fixture'a.
```python
def test_twitter_initialization(twitter):  
    assert twitter  
  
def test_tweet_single_message(twitter):  
    twitter.tweet('Test message')  
    assert twitter.tweets == ['Test message']
```
###  7.2. Fixture jako generator
Fixture z punktu 7.1. można również napisać w formie generatora.
```python
@pytest.fixture  
def twitter():  
    twitter = Twitter()  
    yield twitter  
    twitter.delete()
```
W takiej sytuacji w momencie wykonywania testu na fixturze będącym generatorem wykonywana jest po raz pierwszy metoda \_\_next\_\_(), która zwraca obiekt klasy Twitter. W momencie zakończenia testu na fixturze wykonywana jest po raz drugi metoda \_\_next\_\_, co zgodnie z działaniem generatorów prowadzi do wykonania metody twitter.delete() i zwrócenia wyjątku StopIteration. Mechanizm ten jest często wykorzystywany w testach do wykonania dodatkowych operacji przy zakończeniu testu.
###  7.3. Request jako argument fixture'a
Do fixture'a można również przekazać argument request, który zawiera dodatkowe dane związane z kontekstem wykonywanego testu.
```python
@pytest.fixture  
def twitter(request):  
    twitter = Twitter()  
    yield twitter  
    twitter.delete()
```
###  7.4. Parametryzacja fixture'ów
Request można również wykorzystać do parametryzowania fixture'ów. W fixturze twitter chcemy zainicjować klasę Twitter z dwoma różnymi parametrami. W tym celu do dekoratora przekazujemy żądane parametry w zmiennej param.
```python
@pytest.fixture(params=[None, 'test.txt'])  
def twitter(request):  
    twitter = Twitter(backend=request.param)  
    yield twitter  
    twitter.delete()
```
W takiej sytuacji wszystkie testy wykorzystujące ten fixture zostaną wykonane dwukrotnie - raz z wartością parametru None, a raz z wartością 'test.txt'.
###  7.5. Tymczasowe pliki
Aby utworzyć tymczasowe pliki w ramach fixture'a możliwe jest skorzystanie z tymczasowej ścieżki tmpdir. Po wykonaniu testu plik taki zostanie natychmiastowo usunięty.
```python
@pytest.fixture  
def backend(tmpdir):  
    temp_file = tmpdir.join('test.txt')  
    temp_file.write('')  
    return temp_file
```

## 8. Monkey patching
Monkey patching "nadpisuje" elementy programu np. funkcje innymi mechanizmami. Poniżej przyklad zastąpienia funkcji input.

```python
from pay.order import LineItem, Order  
from pay.payment import pay_order  
from pytest import MonkeyPatch  
  

# klasa MonkeyPatch musi być przekazana jako argument funkcji
def test_pay_order(monkeypatch: MonkeyPatch) -> None:
	# Przygotowanie inputów  
    inputs = ["1249190007575069", "12", "2024"]  
    # Zastąpienie domyślnego wywołania funkcji input przez zwrócenie pierwszego elementu listy inputs
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))  
    order = Order()  
    order.line_items.append(LineItem("Test", 100))  
    pay_order(order)
```
Do monkey patchingu można wykorzystać też funkcjonalność fixture'ów. Poniżej przykład zablokowania możliwości wykorzystania metody request. Parametr autouse wskazuje, że fixture ten będzie wykonany przed każdym testem.
```python
@pytest.fixture(autouse=True)  
def no_requests(monkeypatch):  
    monkeypatch.delattr('requests.sessions.Session.request')
```
## 9. Mockowanie
W celu zastąpienia pewnych obiektów / systemów w ramach testowania wykorzystywane jest tzw. mockowanie. Proces ten polega na umieszczeniu "atrapy" domyślnie używanego obiektu, która przejmie jego funkcje w czasie testowania. Jest to bardziej zaawansowana forma monkey patchingu.
## 9.1. Mockowanie z unittestem
Możliwe jest użycie metody context managera patch z biblioteki unittest, który dla wskazanej funkcji zwraca określoną w zmiennej return_value wartość.
```python
from unittest.mock import patch

def test_tweet_single_message(twitter):  
    with patch('twitter.Twitter.get_user_avatar', return_value='test'):  
        twitter.tweet('Test message')  
        assert twitter.tweet_messages == ['Test message']
```
Podobnie można mockować metody klasy:
```python
def test_tweet_single_message(twitter):  
    with patch.object(Twitter, 'get_user_avatar', return_value='test'):  
        twitter.tweet('Test message')  
        assert twitter.tweet_messages == ['Test message']
```
Do użycia patch, jak i patch.object można też użyć dekoratora. W takim przypadku mockowania klasy w ten sposób, zostanie ona przekazana do testu jako pierwszy argument (w tym przypadku avatar_mock):
```python
@patch.object(Twitter, 'get_user_avatar', return_value='test')  
def test_tweet_single_message(avatar_mock, twitter):  
    twitter.tweet('Test message')  
    assert twitter.tweet_messages == ['Test message']
```
Możliwe jest również utworzenie mocka wewnątrz samego testu. Poniżej przykład nadpisania metody find_hashtags i ustawienie zwracanej przez nią wartości.
```python
from unittest.mock import Mock
  
def test_tweet_with_hashtag_mock(avatar_mock, twitter):  
    twitter.find_hashtags = Mock()  
    twitter.find_hashtags.return_value = ['first']  
    twitter.tweet('Test #second')  
    assert twitter.tweets[0]['hashtags'] == ['first']
```
Jeżeli chcemy zamockować metody magiczne Pythona to zamiast klasy Mock() konieczne jest użycie klasy MagicMock().
```python
from unittest.mock import MagicMock

def test_twitter_version(twitter):  
    twitter.version = MagicMock()  
    twitter.version.__eq__.return_value = '2.0'  
  assert twitter.version == '2.0'
```
## 10. Pominięcie testu
Istnieje możliwość pominięcia testu w przypadku, gdy dla danych parametrów nie chcemy go wykonywać.
```python
def test_tweet_with_username(twitter):  
    if twitter.username:  
        pytest.skip()  
    twitter.tweet('Test message')  
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test'}]
```
## 11. Plik conftest.py
Plik conftest.py to plik konfiguracyjny dla testów pytestowych, gdzie można np:
*  Składować wielokrotnie używane fixtury, które będą automatycznie wykryte przez testy zdefiniowane w innych plikach.
* Ustalić czynności, które mają zostać wykonane przed wszystkimi testami, np:
```python
def pytest_runtest_setup():  
	# Funkcja wykonana przed każdym testem  
	print('Start test')
```
