# Login i logout
```python
# project/module/urls.py
...

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]
```
## Login
```python
# project/module/views.py
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "module/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "module/login.html")
```
### 5.2. Logout
```python
# module/views.py
def logout_view(request):
    logout(request)
    return render(request, "module/login.html", {
                "message": "Logged Out"
            })
```