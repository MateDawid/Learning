# Mockowanie
W celu zastąpienia pewnych obiektów / systemów w ramach testowania wykorzystywane jest tzw. mockowanie. Proces ten polega na umieszczeniu "atrapy" domyślnie używanego obiektu, która przejmie jego funkcje w czasie testowania. Jest to bardziej zaawansowana forma monkey patchingu.
## Mockowanie z unittestem
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
## Specyfikacja dla Mocka
Żeby uniknąć zdefiniowania niechcianego parametru do obiektu Mock można przekazać listę dopuszczalnych parametrów.
```python
>>> from unittest.mock import Mock
>>> calendar = Mock(spec=['is_weekday', 'get_holidays'])

>>> calendar.is_weekday()
<Mock name='mock.is_weekday()' id='4569015856'>
>>> calendar.create_event()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 582, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'create_event'
```
Można również przekazać cały imitowany obiekt:
```python
>>> import my_calendar
>>> from unittest.mock import create_autospec

>>> calendar = create_autospec(my_calendar)
>>> calendar.is_weekday()
<MagicMock name='mock.is_weekday()' id='4579049424'>
>>> calendar.create_event()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 582, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'create_event'
```
Aby wykorzystać ten mechanizm w patchu wystarczy określić parametr **autospec** jako True.
```python
>>> import my_calendar
>>> from unittest.mock import patch

>>> with patch('__main__.my_calendar', autospec=True) as calendar:
...     calendar.is_weekday()
...     calendar.create_event()
...
<MagicMock name='my_calendar.is_weekday()' id='4579094312'>
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 582, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'create_event'
```