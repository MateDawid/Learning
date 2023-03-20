# **FLASK**
## MVC
Flask wykorzystuje paradygmat **MVC**, co oznacza Model–view–controller:  
    ![Model with arrow to View labeled Updates; View with arrow to User labeled Sees; User with arrow to Controlled labeled Uses; Controller with arrow to Model labeled Manipulates](https://cs50.harvard.edu/x/2022/notes/9/mvc.png)
   - Controller zawiera logikę biznesową - w tym przypadku wykonywaną przez kod pythonowy
   -  View oznacza wszystkie elementy wizualne - template'y, HTML, CSS oraz wszystko co user "widzi",
   - Model oznacza dane aplikacji składowane w dowolnej formie - bazie danych SQL, pliku CSV, etc.

## Jinja2
Do umieszczenia logiki w na template'ach Flask wykorzystuje biblioteka Jinja2. Działa ona na podobnej zasadzie, co template'y w Django.
Dokumentacja: https://jinja.palletsprojects.com/en/3.1.x/

 
## Inicjowanie aplikacji
```python
# app.py
from flask import Flask, render_template, request

app = Flask(__name__)
```
## Definiowanie podstawowych endpointów
```python
# app.py
...
@app.route("/")
def index():
    return render_template("index.html")
```
## Endpoint typu POST
```python
# app.py
...
@app.route("/greet", methods=["POST"])
def greet():
    return render_template("greet.html", name=request.form.get("name", "world"))
```
