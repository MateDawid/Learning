# Parametryzacja testów
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
