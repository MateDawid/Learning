# **Django REST Framework**
## 1. Przygotowanie projektu
Przykładowa zawartość pliku requirements.txt, którą należy zainstalować.
```
Django==4.1.3  
django-extensions==3.2.1  
django-filter==22.1  
djangorestframework==3.14.0  
djangorestframework-jsonapi==6.0.0
```
Następnie w pliku settings.py dodać zainstalowane pakiety.

```python
# settings.py

INSTALLED_APPS = [  
    'django.contrib.admin',  
  'django.contrib.auth',  
  'django.contrib.contenttypes',  
  'django.contrib.sessions',  
  'django.contrib.messages',  
  'django.contrib.staticfiles',  
  'django_extensions', #Great package to access abstract models  
  'django_filters', #Used with DRF  
  'rest_framework', #DRF package  
]
```
W tym samym pliku dodać słownik REST_FRAMEWORK. Poniżej przykład z bazowymi wartościami z dokumentacji.
 ```python
#settings.py

REST_FRAMEWORK = {  
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',  
  'DEFAULT_PARSER_CLASSES': (  
        'rest_framework_json_api.parsers.JSONParser',  
  ),  
  'DEFAULT_RENDERER_CLASSES': (  
        'rest_framework_json_api.renderers.JSONRenderer',  
  'rest_framework.renderers.BrowsableAPIRenderer'  
  ),  
  'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',  
  'DEFAULT_FILTER_BACKENDS': (  
        'rest_framework_json_api.filters.QueryParameterValidationFilter',  
  'rest_framework_json_api.filters.OrderingFilter',  
  'rest_framework_json_api.django_filters.DjangoFilterBackend',  
  'rest_framework.filters.SearchFilter',  
  ),  
  'SEARCH_PARAM': 'filter[search]',  
  'TEST_REQUEST_RENDERER_CLASSES': (  
        'rest_framework_json_api.renderers.JSONRenderer',  
  ),  
  'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'  
}
```
W głównym pliku urls.py dodać router i jego adresy.
```python
#urls.py

from django.urls import path  
from django.contrib import admin  
from rest_framework import routers  
  
router = routers.DefaultRouter()  
  
urlpatterns = router.urls  
  
urlpatterns += [  
    path('admin/', admin.site.urls),  
]
```
Utworzyć i wykonać migracje
```
python manage.py makemigrations
python manage.py migrate
```
## 2. Serializacja
Serializacja danych odbywa się przy użyciu serializerów. Serializer konwertuje dane takie jak querysety lub instancje modelów na podstawowe typy Pythona w celu renderowania ich jako JSON, XML lub inny typ. Serializer również deserializuje dane z JSON / XML na obiekty typowe dla Django. Odpowiada również za walidacje wprowadzanych danych.

### 2.1. Serializer
Wymaga zdefiniowania wszystkich pól, jakie mają być serializowane. Odpowiednik modelu Form z bazowego Django.

Przykładowy model:
```python
# models.py

from django.db import models  
from pygments.lexers import get_all_lexers  
from pygments.styles import get_all_styles  
  
LEXERS = [item for item in get_all_lexers() if item[1]]  
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])  
  
  
class Snippet(models.Model):  
    created = models.DateTimeField(auto_now_add=True)  
    title = models.CharField(max_length=100, blank=True, default='')  
    code = models.TextField()  
    linenos = models.BooleanField(default=False)  
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)  
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)  
  
    class Meta:  
        ordering = ['created']
```
Serializer dla modelu:
```python
# serializers.py

from rest_framework import serializers  
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES  
  
  
class SnippetSerializer(serializers.Serializer):  
    id = serializers.IntegerField(read_only=True)  
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)  
    code = serializers.CharField(style={'base_template': 'textarea.html'})  
    linenos = serializers.BooleanField(required=False)  
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')  
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')  
  
    def create(self, validated_data):  
		"""  
		Create and return a new `Snippet` instance, given the validated data. 
		"""  
		return Snippet.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
		"""  
		Update and return an existing `Snippet` instance, given the validated data. 
		"""  
		instance.title = validated_data.get('title', instance.title)  
		instance.code = validated_data.get('code', instance.code)  
		instance.linenos = validated_data.get('linenos', instance.linenos)  
		instance.language = validated_data.get('language', instance.language)  
		instance.style = validated_data.get('style', instance.style)  
		instance.save()  
		return instance
```
### 2.2. ModelSerializer
Korzysta ze wskazanych pól modelu zdefiniowanego w klasie Meta, możliwe jest jednak dodanie własnych danych. Odpowiednik modelu ModelForm z bazowego Django.

Przykładowy model:
```python
# models.py

from django.db import models  
from utils.model_abstracts import Model  
from django_extensions.db.models import (  
    TimeStampedModel,  
  ActivatorModel,  
  TitleDescriptionModel  
)  
  
  
class Contact(  
    TimeStampedModel,  
  ActivatorModel,  
  TitleDescriptionModel,  
  Model  
):  
    class Meta:  
        verbose_name_plural = "Contacts"  
  
  email = models.EmailField(verbose_name="Email")  
  
    def __str__(self):  
        return f'{self.title}'
```
Serializer dla modelu:
```python
# serializers.py

from . import models  
from rest_framework import serializers  
from rest_framework.fields import CharField, EmailField  
  
  
class ContactSerializer(serializers.ModelSerializer):  
    name = CharField(source="title", required=True)  
    message = CharField(source="description", required=True)  
    email = EmailField(required=True)  
  
    class Meta:  
        model = models.Contact  
        fields = (  
			'name',  
			'email',  
			'message'  
		)
```
### 2.3. Proces serializacji i deserializacji
Importujemy zdefiniowane w punkcie 7.2.1. model Snippet i jego serializer i tworzymy instancję obiektu.
```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='print("hello, world")\n')
snippet.save()
```
Serializujemy instancję obiektu przekazując ją do obiektu serializera.
```python
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```
Słownik zawarty w zmiennej serializer.data serializujemy przy użyciu klasy JSONRenderer. Uzyskujemy obiekt w postaci bajtowej.
```python
content = JSONRenderer().render(serializer.data)
content
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
```
Taki obiekt można również zdeserializować z powrotem do postaci instancji obiektu modelu Django.
```python
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>
```
### 2.4. Serializowanie querysetów
Do obiektu serializera możliwe jest też przekazanie całego querysetu. W tym celu konieczne jest podanie parametru **many** z wartością **True**.
```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```
### 2.5. extra_kwargs
Aby nadpisać niektóre właściwości dla poszczególnych pól można utworzyć zmienną extra_kwargs w klasie Meta serializera:
```python
class class UserSerializer(serializers.ModelSerializer):
  class Meta:
      ...
      extra_kwargs = {'password': {
          'write_only': True,  # password will be able to save in POST request, but won't be returned in response
          'min_length': 5
      }}
```
## 3. Views
### 3.1. Podstawowy widok Django
Odpowiednik podstawowego view z bazowego Django opartego na klasach.  Odpowiada za obsługę zapytań HTTP na odpowiadający widokowi adres. Przykład:
```python
# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 3.2. API View
Odpowiednik podstawowego view z bazowego Django opartego na klasach. Odpowiada za obsługę zapytań HTTP na odpowiadający widokowi adres.

Przykładowy widok dla modelu i serializera z poprzedniego punktu:
```python
# views.py

from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ContactSerializer
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response


class ContactAPIView(views.APIView):
    """
    A simple APIView for creating contact entires.
    """
    serializer_class = ContactSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
```
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
### 3.5. ViewSet
W celu jeszcze większego uproszczenia kodu możliwe jest zastosowanie ViewSetu. Automatyzuje on mapowanie endpoitów na poszczególne adresy URL. Nie ma również potrzeby tworzyć osobnych widoków listy i pojedynczego elementu - oba warianty można obsłużyć viewsetem.
```python 
# views.py

from .serializers import ItemSerializer
from .models import Item 
from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets 
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

class ItemViewSet(  
		ListModelMixin,  
		RetrieveModelMixin,  
		viewsets.GenericViewSet  
	):  
	"""  
	A simple ViewSet for listing or retrieving items. 
	"""  
	permission_classes = (IsAuthenticated,)  
	queryset = Item.objects.all()  
	serializer_class = ItemSerializer
```
### 3.6. Rodzaje ViewSetów
Bazowy ViewSet"
  ```python
  class ViewSet(ViewSetMixin, views.APIView):
      """
      The base ViewSet class does not provide any actions by default.
      """
      pass
  ```
 GenericViewSet:
  ```python
  class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
      """
      The GenericViewSet class does not provide any actions by default,
      but does include the base set of generic view behavior, such as
      the `get_object` and `get_queryset` methods.
      """
      pass
  ```
  ReadOnlyViewSet - pozwala jedynie na pobieranie danych, nie daje możliwości zmiany lub usunięcia.
  ```python
  class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
      """
      A viewset that provides default `list()` and `retrieve()` actions.
      """
      pass
  ```
  * ModelViewSet - pozwala na wszystkie możliwe operacje z zakresu CRUD.
  ```python
  class ModelViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
      """
      A viewset that provides default `create()`, `retrieve()`, `update()`,
      `partial_update()`, `destroy()` and `list()` actions.
      """
      pass
  ```
### 3.7. Własna akcja w ViewSecie
Aby utworzyć własny endpoint wewnątrz viewsetu, trzeba użyć dekoratora @action.
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
  ...
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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