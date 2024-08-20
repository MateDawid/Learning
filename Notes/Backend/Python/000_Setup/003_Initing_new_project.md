# Initing new project
Let's take a look on how to manage a Flask project using pyenv and Poetry.

First, create a new directory called "flask_example" and move inside it:

```commandline
$ mkdir flask_example
$ cd flask_example
```

Second, set the Python version for the project with pyenv:

```commandline
$ pyenv local 3.10.2
```

Next, initialize a new Python project with Poetry:

```commandline
$ poetry init

Package name [flask_example]:
Version [0.1.0]:
Description []:
Author [Your name <your@email.com>, n to skip]:
License []:
Compatible Python versions [^3.10]:

Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] no
Do you confirm generation? (yes/no) [yes]
```

Add Flask:

```commandline
$ poetry add flask
```

Last but not least, add pytest as a development dependency:

```commandline
$ poetry add --dev pytest
```

Now that we have a basic environment set up, we can write a test for a single endpoint.

Add a file called test_app.py:

```python
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/health-check/')

    assert response.status_code == 200
```

After that, add a basic Flask app to a new file called app.py:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/health-check/')
def health_check():
    return 'OK'


if __name__ == '__main__':
    app.run()
```

Now, to run the tests, run:

```commandline
$ poetry run python -m pytest
```

And you can run the development server like so:

```commandline
$ poetry run python -m flask run
```

The ```poetry run``` command runs a command inside Poetry's virtual environment.