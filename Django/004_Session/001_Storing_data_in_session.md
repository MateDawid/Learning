# Przechowywanie danych w sesji
```python
# module/views.py
def index(request):
    # Check if there already exists a "tasks" key in our session
    if "tasks" not in request.session:
        # If not, create a new list in session
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })
```