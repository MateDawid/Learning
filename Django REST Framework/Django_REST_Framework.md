


### 3.3. Mixins
W celu uproszczenia kodu możliwe jest wykorzystanie wbudowanych mixinów zapewniających typowe dla API funkcjonalności, którymi obudować można podstawowy widok bazujący na klasach. 

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```
Oba widoki bazują na GenericAPIView, który zapewnia podstawowe funkcjonalności widoku. 
SnippetList wykorzystuje mixiny zapewniające funkcjonalności listy obiektów (ListModelMixin) oraz tworzenia nowego obiektu (CreateModelMixin).
Za to SnippetDetail rozszerzony jest o pobieranie (RetrieveModelMixin), aktualizowanie (UpdateModelMixin) oraz usuwanie obiektów (DestroyModelMixin).
### 3.4. Generyczne klasowe widoki
Widoki można uprościć jeszcze bardziej poprzez pominięcie użycia mixinów i wykorzystanie predefiniowanych generycznych widoków. W takiej sytuacji widoki zdefiniowane w punkcie 7.3.3. prezentują się następująco:
```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```


 
## 4. Router oraz adresy URL
W celu udostępnienia widoku trzeba przypisać go do konkretnego adresu URL. W tym celu do poprzednio przygotowanego w punkcie 7.1. zestawu adresów URL należy dodać kolejny adres i przypisać do niego utworzony widok. 
```python
# urls.py

from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()), # NEW URL
]
```
Jeżeli chcemy dodać url do obiektu ViewSet (np. dziedziczącego z GenericViewSet) należy go zarejestrować bezpośrednio w routerze.

```python
from ecommerce import views as ecommerce_views  
from rest_framework import routers    
  
router = routers.DefaultRouter()  
router.register(r'item', ecommerce_views.ItemViewSet, basename='item')  
router.register(r'order', ecommerce_views.OrderViewSet, basename='order')
```
## 5. Permissions
```python
#permissions.py
from rest_framework import permissions  
  
  
class UpdateOwnProfile(permissions.BasePermission):  
	"""Allow user to edit their own profile"""  
	  
	def has_object_permission(self, request, view, obj):  
		"""Check user is trying to edit their own profile"""  
		if request.method in permissions.SAFE_METHODS:  
			return True  
		return obj.id == request.user.id
```
```python
# views.py
class UserProfileViewSet(viewsets.ModelViewSet):  
	"""Handle creating and updating profiles"""  
	...
	permission_classes = (permissions.UpdateOwnProfile,)  
```
## 6. Testowanie
DRF zapewnia moduł wspierający testowanie napisanego API. W tym celu należy zaimportować klasę APITestCase z modułu rest_framework.test
```python
# tests.py

from rest_framework.test import APITestCase  
  
class ContactTestCase(APITestCase):  
    """  
    Test suite for Contact 
    """
    pass
```

### 6.1. setUp
Zdefiniowanie metody setUp() w klasie dziedziczącej po klasie APITestCase pozwala sprawia, że kod, napisany w tej metodzie wykona się przed wykonaniem zestawu testów zdefiniowanym w klasie.

```python
# tests.py

from rest_framework.test import APIClient  
from rest_framework.test import APITestCase   


class ContactTestCase(APITestCase):  
    """  
 Test suite for Contact """  
  def setUp(self):  
        self.client = APIClient()  
        self.data = {  
			"name": "Billy Smith",  
			"message": "This is a test message",  
			"email": "billysmith@test.com"  
		}  
        self.url = "/contact/"
```
### 6.2. Tworzenie unit testów
Testy tworzone są jako metody dla klasy dziedziczącej po APITestCase. Przykładowy unit test:
```python
from .models import Contact  
from rest_framework.test import APIClient  
from rest_framework.test import APITestCase  
from rest_framework import status  
  
  
class ContactTestCase(APITestCase):  
	...    
	def test_create_contact(self):  
		'''  
		test ContactViewSet create method 
		'''  
		data = self.data  
		response = self.client.post(self.url, data)  
		self.assertEqual(response.status_code, status.HTTP_200_OK)  
		self.assertEqual(Contact.objects.count(), 1)  
		self.assertEqual(Contact.objects.get().title, "Billy Smith")
```
### 6.3. Uruchomienie testów
Uruchomienie wszystkich istniejących w projekcie testów odbywa się poprzez uruchomienie komendy:
```
python manage.py test
```
