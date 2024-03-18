# End-to-end testing
## Prepare end-to-end test
We have a working API at this point that's fully tested. We can now look at how to write some end-to-end (e2e) tests. Since we have a simple API we can write a single e2e test to cover the following scenario:

1. create a new article
2. list articles
3. get the first article from the list


```python
@pytest.mark.e2e
def test_create_list_get(client):
    requests.post(
        "http://localhost:5000/create-article/",
        json={
            "author": "john@doe.com",
            "title": "New Article",
            "content": "Some extra awesome content"
        }
    )
    response = requests.get(
        "http://localhost:5000/article-list/",
    )

    articles = response.json()

    response = requests.get(
        f"http://localhost:5000/article/{articles[0]['id']}/",
    )

    assert response.status_code == 200
```
## Register marker
Register a marker called e2e with pytest by adding the following code to pytest.ini:
```ini
[pytest]
markers =
    e2e: marks tests as e2e (deselect with '-m "not e2e"')
```
pytest markers are used to exclude some tests from running or to include selected tests independent of their location.

To run only the e2e tests, run:

```commandline
(venv)$ python -m pytest tests -m 'e2e'
```

To run all tests except e2e:

```commandline
(venv)$ python -m pytest tests -m 'not e2e'
```
e2e tests are more expensive to run and require the app to be up and running, so you probably don't want to run them at all times.