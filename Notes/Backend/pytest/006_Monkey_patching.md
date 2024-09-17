# Monkey patching

> Source: https://testdriven.io/courses/tdd-django/pytest-monkeypatching/

Monkeypatching is the act of dynamically changing a piece of code at runtime. Essentially, it allows you to override the default behavior of a module, object, method, or function without changing its source code.

Source code:

```python
# twitter.py

import os
import tweepy

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_key = os.getenv("ACCESS_KEY")
access_secret = os.getenv("ACCESS_SECRET")


def get_friends(user):
    """
    Given a valid Twitter user 20 friends are returned
    """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    friends = []

    try:
        user = api.get_user(user)
    except tweepy.error.TweepError:
        return "Failed to get request token."

    for friend in user.friends():
        friends.append(friend.screen_name)

    return friends
```

So, the `get_friends` function uses `tweepy` to authenticate against the Twitter API. Once authenticated, it then returns a list of twenty friends.

Test:

```python
# test.py

import twitter


def test_get_friends(monkeypatch):
    def mock_get_friends(user):
        return [(lambda x: f"friend{x}")(x) for x in range(20)]

    monkeypatch.setattr(twitter, "get_friends", mock_get_friends)

    assert len(twitter.get_friends("testdrivenio")) == 20
```

`test_get_friends` uses the pytest monkeypatch fixture to create a mocked version of `get_friends`, called `mock_get_friends`, that returns a list of twenty strings. Then, during a test run, `mock_get_friends` gets called rather than the real `get_friends` function. This not only decreases the amount of time it will take for the test to run, but it also makes the test more predictable since it is not affected by network connectivity issues, outages in the Twitter API, or rate limiting issues.

That said, keep in mind that the test is not actually testing the get_friends function call; it's replacing the function's default behavior (authenticating and calling the Twitter API) with new behavior (simply returning a list of strings).

While mocking or monkeypatching can speed up test runs and make the tests more predictable, at some point in the testing process, possibly in a staging environment, you should test out all external communication so that you can be confident that the system works as expected. This is often achieved with some form of end-to-end tests.