## 10. ITERACJA





### 10.5. Sortowanie
W Pythonie dane można posortować na dwa sposoby używając wbudowanych mechanizmów.
```python 
[2, 1, 3].sort() # sortuje istniejącą listę
sorted([2, 1, 3]) # tworzy posortowaną kopię podanej listy
```
W celu ułatwienia przekazywania klucza sortowania do metody sorted można posłużyć się modułem operator.
#### 10.5.1.  operator.itemgetter
```python 
from operator import *

people = [
	('Jan', 'Kowalski'),
	('Anna', 'Woźniak'),
	('Anna', 'Nowak')
]

sorted(people, key=itemgetter(0, 1)) # itemgetter wyciąga elementy z kolejno z indeksów 0 i 1 w formie krotki dla każdego z obiektów listy people. Lista jest posortowana najpierw względem pierwszej podanej wartości, a następnie drugiej
```
#### 10.5.2. operator.attrgetter
```python 
from operator import *
from collections import namedtuple

Person = namedtuple('Person', 'first_name last_name')

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=attrgetter('first_name', 'last_name')) # attrgetter wyciąga atrybuty kolejno 'first_name' i 'last_name' i sortuje listę obiektów na ich podstawie
```
#### 10.5.3. operator.methodcaller
```python 
from operator import *
from collections import namedtuple

class Person(namedtuple('Person', 'first_name last_name')):
	def get_length(self):
		return len(str(self))

people = [
	Person('Jan', 'Kowalski'),
	Person('Anna', 'Woźniak'),
	Person('Anna', 'Nowak')
]

sorted(people, key=methodcaller('get_length')) # methodcaller sortuje listę na podstawie wartości zwróconych przez metodę, której nazwa przekazana jest w argumencie
```
## 11. Programowanie funkcyjne
### 11.1. Funkcje wyższego rzędu (Higher order functions)
#### 11.1.1. map
Wykonuje wskazaną funkcję na każdym elemencie podanej sekwencji i zwraca listę wyników tej funkcji
```python 
# Zwraca iterator pozycji poszczególnych elementów stringa w Unicode
map(ord, 'zażółć gęślą jaźń') 
```
#### 11.1.2. filter
Filtruje sekwencje bazując podanej funkcji.
```python 
filter(str.isupper, 'Hello World') 
```
#### 11.1.3. functools.reduce
Iteruje po elementach sekwencji i redukuje ją do pojedynczej wartości.
**Przykład 1: Sumowanie liczb**
```python
import operator
from functools import reduce
 
numbers = [42, 15, 2, 33]

# Pierwsza wartość funkcji to tzw. akumulator, na którym wykonywane są operacje bazujące na drugim argumencie
def f(subtotal, number):
	return subtotal + number

#reduce(f, numbers)
reduce(operator.add, numbers)
```
**Przykład 2: Grupowanie liczb parzystych i nieparzystych**
```python
import operator
from functools import reduce
 
numbers = [42, 15, 2, 33]

def f(grouped, number):
	key = 'even' if number % 2 == 0 else 'odd'
	grouped[key].append(number)
	return grouped

reduce(f, numbers, {'even': [], 'odd': []})
```
### 11.2. Funkcje zagnieżdżone
Jako, że funkcje to typ pierwszoklasowy, można je bez ograniczeń zagnieżdżać. Stosowanie funkcji zagnieżdżonych umożliwia ukrywanie implementacji. Funkcja zagnieżdżona ma zasięg lokalny, przez co ma bezpośredni dostęp do argumentów przekazanych do funkcji nadrzędnej.  
```python
def selection_sort(items):

	def recursive(items, i):
		
		def min_index(i):
			return items.index(items[i:], i)
		
		def swap(i, j):
			items[i], items[j] = items[j], items[i]
		
		if i < len(items):
			j = min_index(i)
			swap(i, j)
			selection_sort(items, i + 1)
	
	recursive(items, 0)

items = ['bob', 'alice', 'max']
selection_sort(items) 
```
### 11.3. Zasięg zmiennych
Wartości zmiennych wyszukiwane są w kolejności LEGB - local, enclosed, global, built-in.
```python
%reset -f

x = 'global'

def outer():
	x = 'enclosed'
	def inner():
		x = 'local'
		print(x)
	inner()
	print(x)

outer()
print(x)

# local
# enclosed
# global
```
### 11.4. Domknięcia
Zapamiętuje wartości tzw. zmiennych wolnych (nonlocal) w swoim zasięgu leksykalnym. Domknięcia pozwalają dołączać pewien stan do funkcji, a także metody manipulowania tym stanem, jak np, ze zmienną color i metodą set_color z przykładu poniżej. Domknięcia są stosowane np. przy tworzeniu dekoratorów.
```python
def tag(name):
	color = 'black'
	def wrap(text):
		return f'<{name} style="color: {color}">{text}</{name}>'
	def set_color(value):
		nonlocal color
		color = value
	wrap.set_color = set_color
	return wrap
p = tag('p')
p('Python')
```

### 11.5. Funkcje cząstkowe
Funkcje wykonujące działanie innej funkcji, ale z mniejszą wymaganą do podania liczbą argumentów.

```python
from functools import partial

def quadratic(x, a, b, c):
	return a*x**2 + b*x + c

# Funkcja cząstkowa - zapis 1
def y(x):
	return quadratic(x, 3, 1, -4)

# Funkcja cząstkowa - zapis 2
y = partial(quadratic, a=3, b=1, c=-4)
```
## 12. PROGRAMOWANIE OBIEKTOWE
### 12.1. Kopiowanie obiektów
Kopiowanie obiektów może odbywać się w sposób płytki i głęboki. W przypadku kopiowania płytkiego mutowalne elementy nie są rzeczywistą kopią pierwotnych elementów, ale kopią referencji do tych obiektów w pamięci
```python
import copy

x = [1, [2, 3]]
# shallow copy - płytkie kopiowanie
# y = x[:]
# y = list(x)
y = copy.copy(x)

y.append(5)
# x = [1, [2,3]]
# y = [1, [2,3], 5]

y[1].append(5)
# Jako, że lista jest mutowalna, to po dodaniu do niej elementu w jednej z list, element ten jest widoczny w obu kopiach listy
# x = [1, [2, 3, 4]]
# x = [1, [2, 3, 4], 5] 
```
Rozwiązaniem powyższego problemu może być użycie deepcopy, które rekurencyjnie kopiuje kolejne elementy z drzewa obiektu (nie ich referencje, jak w przypadku mutowalnych obiektów przy płytkim kopiowaniu).

```python
import copy

x = [1, [2, 3]]
# deep copy - głębokie kopiowanie
y = copy.deepcopy(x)

y[1].append(5)
# x = [1, [2, 3]]
# x = [1, [2, 3, 4]] 
```
### 12.2. Klasy abstrakcyjne
Użycie klas abstrakcyjnych pozwala na wymuszenie zaimplementowania wszystkich abstrakcyjnych metod w klasach pochodnych od abstrakcyjnej klasy bazowej.

```python
import abc
import json

class Plugin(metaclass=abc.ABCMeta):
	"""Abstract base for plugins."""
	
	@abc.abstractmethod
	def load(self, path)
		"""Return a dict with values from the given file."""
	
	@abc.abstractmethod
	def save(self, data, path)
		"""Serialize data and save it to the given file."""


class JsonPlugin(Plugin):

	def load(self, path):
		with open(path) as fp:
			return json.load(fp)
	
	def save(self, data, path):
		with open(path, 'w') as fp:
			json.dump(data, fp, indent=4, sort_keys=True)
```
### 12.3. Przeciążanie funkcji
Python nie obsługuje przeciążania funkcji i metod, ale można za to dostosować działanie funkcji w zależności od przyjętych przez nią argumentów. Najprościej zrobić to przez użycie isinstance, ale jest to antywzorzec. Zamiast tego można wykorzystać metodę singledispatch.
```python
from functools import singledispatch

# Zdefiniowanie wzorca funkcji
@singledispatch
def pretty_print(x):
	print(x)

# Zarejestrowanie specjalnego działania funkcji po podaniu jej listy oraz tupli jako argumentu
@pretty_print.register(list)
@pretty_print.register(tuple)
def _(items):
	for i, value in enumerate(items):
		print(f'[{i}] = {value}')
```

Powyższe rozwiązanie nie zadziała dla metod w klasie oraz nie obsługuje więcej niż jednego argumentu. Aby rozwiązać ten drugi problem można skorzystać z zewnętrznej biblioteki multipledispatch.

```python
from multipledispatch import dispatch

@dispatch(int, int)
def add(x, y):
	return x + y

@dispatch(object, object)
def add(x, y):
	return f'{x} + {y}'
```
### 12.4. Przeciążanie operatorów
Przykład przeciążania operatora dodawania i dodawania prawostronnego klasy namedtuple.

```python
from collections import namedtuple

class Vector(namedtuple('Vector', 'x y'):
	def __add__(self, other):
		if isinstance(other, Vector):
			return Vector(*map(sum, zip(self, other)))
		elif isinstance(other, int):
			return Vector(self.x + other, self.y + other)
	
	def __radd__(self, other):
		return self + other
```

#### 12.4.1. __repr__ i __str__
Metoda \_\_str__ powinna zwracać reprezentację obiektu do czytania przez ludzi, natomiast metoda \_\_repr__ powinna zawierać zapis (najlepiej kod Pythona) umożliwiający odtworzenie danego obiektu po wklejeniu do funkcji eval.
```python
class Vector:
	def __init__(self, x, y)
		self.x, self.y = x, y
	
	def __str__(self):
		return f'A vector of {self.x}, {self.y}'
	
	def __repr__(self):
		return f'Vector({self.x}, {self.y})'

a = Vector(3, -4)
str(a) # 'A vector of 3, -4'
b = eval(repr(a)) # Nowa instancja wektora Vector(3, -4)
```
### 12.5. Metody
#### 12.5.1. Metody klasowe
Metoda klasowa to taka, która zawiera odwołanie nie do konkretnej instancji obiektu, ale do samej klasy. Może być wywoływana bez inicjowania obiektu.
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@classmethod
	def monaco_blue(cls):
		return cls(0.2, 0.5, 0.75)
		
	@classmethod
	def exotic_red(cls):
		return cls(1, 0, 0)
	
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))

Color.monaco_blue() # zwraca obiekt z metody klasowej Color(0.2, 0.5, 0.75)
```
#### 12.5.2. Metody statyczne
Nie posiadają odniesienia ani do danego obiektu, ani do samej klasy - zachowują się bardziej jak zwykłe funkcje, niż metody. Z optymalizacyjnego punktu widzenia nie są one dobrym rozwiązaniem, ponieważ wiążę się z dodatkowym kosztem ze względu na przeglądanie przez Pythona przestrzeni nazw w trakcie działania programu. Jedynym logicznym zastosowaniem @staticmethod jest ich pogrupowanie pod jedną, wspólną przestrzenią nazw klasy
```python
from collections import namedtuple
from IPython.display import SVG, display


class Color(namedtuple('Color', 'r g b')):
	@staticmethod
	def blend(color1, color2, alpha=0.5)
		return color1*alpha + color2*(1-alpha)
		
	def draw(self):
		r, g, b = [int(x*100) for x in self]
		display(SVG(f'''\
			<svg>
				<rect width="100" height="100" style="fill:rgb({r}%, {g}%, {b}%)"/>
			</svg>
		'''))
	
	def __mul__(self, scalar):
		return Color(*[x*scalar for x in self])
	
	def __add__(self, other):
		return Color(*[sum(x) for x in zip(self, other)])
```

### 12.6. @property
Dekorator @property, pozwala na utworzenie właściwości obiektu, do której dostęp można uzyskać przy użyciu kropki, tak samo jak do atrybutów definiowanych w konstruktorze. Właściwości obiektu są jednak możliwe do nadpisania tylko po zdefiniowaniu settera.
```python
class Person:
	def __init__(self, name, married=False):
		self._name = name
		self.married = married
	
	@property
	def name(self):
		return self._name
	
	@property
	def married(self):
		return self._married
	
	@married.setter
	def married(self, value):
		if not(isinstance(valie, bool):
			raise TypeError('married must be bool')
		self._married = value
	
	@married.deleter
	def married(self):
		del self._married
```
## 13. METAPROGRAMOWANIE
### 13.1. Dekoratory
Funkcja, przyjmująca jako argument funkcję i zwracająca funkcję. 
```python
def password():
	return 'top_s3cret'

def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

encrypted_password = encrypted(password)
encrypted_password()
```
Powyższy zapis można skrócić do następującego:
```python
def encrypted(function):
	def wrapper():
		import codecs
		return codecs.encode(function(), 'rot_13')
	return wrapper

@encrypted
def password():
	return 'top_s3cret'

password()
```
Jednym z głównych celów zastosowania dekoratorów jest memoizacja, czyli cache'owania wyników funkcji w celu przyspieszenia obliczeń. Poniżej przykład zastosowania dekoratora cache'ującego wyniki rekurencyjnych wyników wywołań wyliczających składniki ciągu Fibonacciego. 
```python
# import functools
def cache(function):
	history = {}
	def wrapper(n):
		if n not in history:
			history[n] = function(n)
		return history[n]
	return wrapper
	
# @functools.lru_cache(maxsize=128)
@cache
def fib(n):
	return 1 if n < 2 else fib(n-2) + fin(n-1)
```
Dekoratory mogą też przyjmować więcej parametrów niż samą dekorowaną funkcję, ale wymaga to dodatkowego poziomu zagnieżdżenia.
```python
import functools

def ignore(ExceptionClass):
	def decorator(function):
		@functools.wraps(function) # pozwala na przekazanie metadanych (np. __name__) funkcji w argumencie do dekorowanej funkcji
		def wrapper(*args, **kwargs):
			try:
				return function(*args, **kwargs)
			except ExceptionClass as ex:
				pass
		return wrapper
	return decorator

@ignore(ZeroDivisionError)
def divide(a, b):
	return a / b
```
### 13.2. Menedżer kontekstu
Obiekt implementujący interfejs składający się z dwóch magicznych metod - \_\_enter__ oraz \_\_exit__, które umożliwiają jego użycie w konstrukcji with. Menedżer kontekstu przydaje się w takim razie do zarządzania stanem, który musi zostać najpierw zainicjowany, a następnie uwolniony, żeby nie dopuścić do wycieków pamięci. Menedżer kontekstu można zdefiniować klasowo albo funkcyjnie.
```python
from time import time

class MockedTime:
	def __enter__(self):
		# tymczasowe nadpisanie funkcji time
		global time
		self._time = time
		time = lambda: 42
	
	def __exit__(self, exception_class, exception, traceback):
		# powrót do domyślnej funkcji time
		global time
		time = self._time

with MockedTime():
	print(time())
print(time())
```
```python
from time import time, sleep

class Timed:
	def __enter__(self):
		self.t1 = time()
		return self # pozwala na przypisanie menedżera do zmiennej poprzez słówo "as" w konstukcji "with"
	
	def __exit__(self, *args):
		self.t2 = time()
	
	@property
	def delta(self):
		return self.t2 - self.t1

with Timed() as timed:
	sleep(0.5)

print(timed.delta)
```
Do utworzenia menedżera kontekstu jako funkcji służy biblioteka contextlib.
```python
from contextlib import contextmanager

@contextmanager
def logging():
	print('__enter__')
	try:
		yield
	finally:
		print('__exit__')

with logging() as value:
	print('The value is:', value)
```
Instrukcja yield dzieli zawiesza działanie funkcji i dzieli ją na dwie części. Pierwsza część odpowiada instrukcji \_\_enter__, w której dokonuje się inicjalizacji. Druga część (za yield) odpowiada za to instukcji \_\_exit__. Konieczne jest opakowanie słówa kluczowego yield blokiem try/finally, ponieważ w innym razie, w przypadku wystąpienia wyjątku nie doszłoby do "zamknięcia" menedżera kontekstu.
### 13.3. Deskryptor
Można go sobie wyobrazić jako property wielokrotnego użytku, które może być wykorzystywane w wielu klasach. Zgodnie z definicją, jest to klasa definiująca jedną z trzech magicznych metod: \_\_get__, \_\_set__, \_\_delete__. Występują szczególne przypadki: 
* data descriptor - definiuje wszystkie trzy metody
* non data descriptor - definiuje tylko metodę \_\_get__. Pozwalają na leniwą inicjalizację atrybutów w klasie

Pożej przykład zastosowania domknięcia wykorzystującego dekorator property do przypisania niezmiennych atrybutów w klasie.
```python
# Zwrócenie wartości atrybutu _attr przy próbie wyciągnięcia atrybutu poprzez Class.attr
def read_only(name):
	@property
	def getter(self):
		return getattr(self, '_' + name)
	return getter

class Person:
	name = read_only('name')
	married = read_only('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
Ten sam problem można rozwiązać przy użyciu deskryptora:
```python
class ReadOnly:
	def __init__(self, name)
		self.name = name
	
	def __get__(self, obj, cls):
		if obj is None:
			return self
		return getattr(obj, '_' + self.name)
	
	def __set__(self, obj, value):
		raise AttributeError

class Person:
	name = ReadOnly('name')
	married = ReadOnly('married')
	
	def __init__(self, name, married=False):
		self._name = name
		self._married = married
``` 
### 13.4. \_\_new__
Metoda magiczna wywoływana przed \_\_init__. Jest to metoda klasowa zwracająca nowy obiekt klasy. Poniżej przykład definicji Singletona.
```python
class Singleton:
	instance = None
	def __new__(cls):
		if Singleton.instance is None:
			Singleton.instance = super().__new__(cls)
		return Singleton.instance

a = Singleton()
b = Singleton()

a is b, id(a) == id(b) # (True, True), obie zmienne wskazują na tę samą instancję obiektu
```
### 13.5. Metaklasy
Najprostszym przykładem metaklasy jest type - jest on metaklasą dla wszystkich podstawowych (i nie tylko) typów w Pythonie np. int, float itp. Używając type można także zdefiniować nową klasę. Poniżej przykład zdefiniowania metaklasy przy użyciu funkcji.
```python
def n_tuple(name, bases, attrs, n):
	def __new__(cls, *args):
		if len(args) != n:
			raise TypeError(f'expected {n} but got {len(args)} arguments')
		return tuple(args)
	return type(f'Tuple {n}', (tuple,), {'__new__': __new__})

class Point(metaclass=n_tuple, n=2):
	pass

Point(1, 2)
```
Metaklasę można również zdefiniować przy użyciu klasy.
```python
class Meta(type):
	def __new__(cls, name, bases, dct):
		x = super().__new__(cls, name, bases, dct)
		x.attr = 100
		return x

class Foo(metaclass=Meta):
	pass

Foo.attr # 100
```
### 13.6. Dataclass
Chcąc uniknąć żmudnego definiowania klas można zastosować mechanizm dataclass. W wyniku takiego zabiegu można zastąpić taką typową klasę:
```python
class Person:
	def __init__(self, name, age, married=False):
		self.name = name
		self.age = age
		self.married = married
```
Taką klasą:
```python
def dataclass(cls):
	def __init__(self, *args, **kwargs):
		# Zapisanie w kwargs argumentów przekazanych przez args zmapowanych przy użyciu cls.__annotations__
		kwargs.update(zip(cls.__annotations__, args))
		# Zapisanie zaktualizowanych kwargs w słowniku obiektu
		self.__dict__.update(kwargs)
	cls.__init__ = __init__
	return cls


@dataclass
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
Od Pythona 3.7. dostępny jest bardziej rozbudowany dekorator spełniający tę samą funkcję, dlatego finalnie taka klasa wyglądałaby tak:
```python
from dataclasses import dataclass

@dataclass
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
Domyślnie klasy udekorowane przez @dataclass są mutowalne, natomiast w celu "zamrożenia" ich wartości stosuje się następujący zapis:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Person:
	# Zdefiniowane w ten sposób zmienne to adnotacje, do których dostęp można uzyskać przez zmienną __annotations__ w obiekcie klasy
	name: str
	age: int
	married: bool = False
```
## 14. PROGRAMOWANIE WSPÓŁBIEŻNE
### 14.1. Obsługa wątków
Do obsługi wątków w Pythonie służy zapożyczony z Javy moduł threading.
```python
import threading
import time

class Task(threading.Thread):
	def run(self):
		time.sleep(1)
		print('task done')

Task().start()
print('program finished')

# program finished
# task done
```
Ostatnia linia powyższego kodu wykonała się w trakcie trwania programu. Jeżeli program ma czekać na wykonanie taska, konieczne jest zastosowanie metody .join() na tym tasku, lub określenie go jako daemon
```python
import threading
import time

class Task(threading.Thread):
	def run(self):
		time.sleep(1)
		print('task done')

task = Task()
# task.daemon = True
task.start()
task.join()
print('program finished')

# task done
# program finished
```
Tworzenie wątków jako klas jest niezalecane ze względu na konieczność dziedziczenia z modułu threading. Zamiast tego pisze się je funkcyjnie.

```python
import threading
import time

def task(name):
	time.sleep(1)
	print(f'{name} done')

threading.Thread(targer=task, args=('foo',)).start()
```
W sytuacji, gdy chcemy, aby kilka wątków rozpoczęło się równolegle można posłużyć się Barrier. Poniżej przykład wyścigu koni.
```python
import threading
import time
import random

def sleep(name, message):
	time.sleep(random.random())
	print(name, message)

def horse(name):
	sleep(name, 'ready...')
	barrier.wait()
	sleep(name, 'started')
	sleep(name, 'finished')

def on_start():
	print('--- RACE STARTED ---') 

horse_names = ('Alfie', 'Daisy', 'Unity')
# Barrier jako pierwszy argument przyjmuje liczbę wątków, które ma zatrzymać. Po zatrzymaniu podanej liczby uruchamia je ponownie.
barrier = threading.Barrier(len(horse_names), action=on_start)

# Inicjalizacja osobnego wątku dla każdego konia
horses = [
	threading.Thread(target=horse, args=(name,))
	for name in horse_names
]

for horse in horses:
	horse.start()

# Użycie drugiej pętli jest konieczne, ponieważ gdyby zastosować join() zaraz po użyciu start() dla jednego wątku, pozostałe wątki nie mogłyby się rozpocząć dopóki pierwszy by się nie zakończył
for horse in horses:
	horse.join()
```
W celu obsługi zdarzeń niezwiązanych z działaniem samych wątków wykorzystuje się klasę Event.
```python
import threading

key_pressed = threading.Event()
finished = threading.Event()

key on_key_press():
	while not finished.is_set():
		if key_pressed.wait(0.1):
			print('key pressed')
			key_pressed.clear()
	print('done')

for _ in range(3):
	input()
	key_pressed.set()

threading.Thread(target=on_key_press).start()

finished.set()
```
### 14.2. Kolejki

```python
import queue
import threading
import time

def downloader(q):
	while True:
		seconds, filename = q.get()
		time.sleep(seconds)
		print(f'downloaded {filename}')
		q,task_done()

files = [
	(1.5, 'data.xml'),
	(0.1, 'style.css'),
	(3, 'movie.avi'),
	(0.9, 'script.js'),
	(0.25, 'image.jpg'),
]

q = queue.PriorityQueue()

for file in files:
	q.put(file)

for _ in range(5):
	threading.Thread(target=downloader, args=(q,), daemon=True).start()

q.join()
```
### 14.3. Procesy
```python
from multiprocessing import Process

def reverse(text):
	return text[::-1]

if __name__ == '__main__':
	p = Process(target=reverse, args=('foobar',))
	p.start()
	p.join()
```
### 14.4. asyncio
Bilbioteka asyncio wykorzystywana jest do przetwarzania asynchronicznego. Poniżej przykład jej zastosowaniu w ciągu Fibonacciego.

```python
import asyncio

# Zdefiniowanie korutyny
async def fib(n):
	if n < 2:
		return n
	
	a = await fib(n - 2)
	b = await fib(n - 1)
	
	return a + b

loop = asyncio.get_event_loop()
loop.set_debug(True)

try:
	result = loop.run_until_complete(fib(10))
	print(result)
finally:
	loop.close()
```
