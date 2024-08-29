# Pominięcie testu
Istnieje możliwość pominięcia testu w przypadku, gdy dla danych parametrów nie chcemy go wykonywać.
```python
def test_tweet_with_username(twitter):  
    if twitter.username:  
        pytest.skip()  
    twitter.tweet('Test message')  
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test'}]
```