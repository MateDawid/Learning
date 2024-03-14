# Fixtures
## Podstawowy fixture
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
## Fixture jako generator
Fixture z punktu 7.1. można również napisać w formie generatora.
```python
@pytest.fixture  
def twitter():  
    twitter = Twitter()  
    yield twitter  
    twitter.delete()
```
W takiej sytuacji w momencie wykonywania testu na fixturze będącym generatorem wykonywana jest po raz pierwszy metoda \_\_next\_\_(), która zwraca obiekt klasy Twitter. W momencie zakończenia testu na fixturze wykonywana jest po raz drugi metoda \_\_next\_\_, co zgodnie z działaniem generatorów prowadzi do wykonania metody twitter.delete() i zwrócenia wyjątku StopIteration. Mechanizm ten jest często wykorzystywany w testach do wykonania dodatkowych operacji przy zakończeniu testu.
## Request jako argument fixture'a
Do fixture'a można również przekazać argument request, który zawiera dodatkowe dane związane z kontekstem wykonywanego testu.
```python
@pytest.fixture  
def twitter(request):  
    twitter = Twitter()  
    yield twitter  
    twitter.delete()
```
## Parametryzacja fixture'ów
Request można również wykorzystać do parametryzowania fixture'ów. W fixturze twitter chcemy zainicjować klasę Twitter z dwoma różnymi parametrami. W tym celu do dekoratora przekazujemy żądane parametry w zmiennej param.
```python
@pytest.fixture(params=[None, 'test.txt'])  
def twitter(request):  
    twitter = Twitter(backend=request.param)  
    yield twitter  
    twitter.delete()
```
W takiej sytuacji wszystkie testy wykorzystujące ten fixture zostaną wykonane dwukrotnie - raz z wartością parametru None, a raz z wartością 'test.txt'.
## Tymczasowe pliki
Aby utworzyć tymczasowe pliki w ramach fixture'a możliwe jest skorzystanie z tymczasowej ścieżki tmpdir. Po wykonaniu testu plik taki zostanie natychmiastowo usunięty.
```python
@pytest.fixture  
def backend(tmpdir):  
    temp_file = tmpdir.join('test.txt')  
    temp_file.write('')  
    return temp_file
```
## getfixturevalue
Istnieje możliwość niepodawania fixture'a jako argumentu testu, ale wyciągnięcie go przy użyciu jego nazwy. Jest to przydatne w sytuacji, gdzie ten sam test chcemy wykonać dla różnych fixture'ów. Nie działa to jednak dobrze w przypadku sparametryzowanych fixture'ów.
```python
@pytest.mark.parametrize('file_type', ('zip_file', 'tar_file'))
def test_file(self, file_type: str, request):
	file = request.getfixturevalue(file_type)
	...
```