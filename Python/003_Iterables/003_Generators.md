# Generatory
```python
def get_next_even():                   # definicja generatora wygląda jak definicja zwykłej funkcji
    for n in range(2,20,2):            # range tworzący zakres od 2 do 20, przesuwając się o 2
        yield n                        # słowo yield informuje interpreter, że ta funkcja będzie generatorem

z = get_next_even()                    # tworzenie obiektu generatora

for i in range(10):                    # pętla for wykonująca się 10 razy
    print(next(z))                     # która za kazdym razem drukuje kolejną wartość zwróconą z obiektu genratora z

y = ('a' * n for n in range(5))        # generator expression - wyrażenie generatorowe
                                       # tworzy generator, który będzie zwracał kolejne wielokrotności stringa 'a'
                                       # zakresie od 0 do 4

for i in range(5):                     # wypisanie kolejnych wartości zwróconych przez obiekt genratora y
    print(next(y))
```

Generator to inny rodzaj iteratora. Używając kluczowego słowa **yield** wyciągamy następną wartość dostarczoną przez generator, po czym zapamiętuje on swój stan aż do kolejnego jego wywołania przez pętlę lub funkcję **next**. Jednym z benefitów generatorów może być tzw. separation of concernes, czyli oddzielenie iteracji od logiki przetwarzania pojedynczego elementu. 

```python
def create_generator(start, stop, step):
	x = start
	while x < stop:
		yield x # Słowo kluczowe przekształcające funkcję w generator
		x += step
		
generator = create_generator(0, 10, 2.5)
# Logika zawarta w funkcji generatora wykonuje się dopiero po zastosowaniu funkcji next() lub w czasie iteracji w pętli

# next(generator)
for value in generator:
	print(value)
```
Generator można również zdefiniować używając tzw. Generator Comprehensions.
```python
(x**2 for x in range(10) if x % 2 == 0)
```
Jako praktyczny przykład zastosowania generatora można podać operacje na plikach, gdzie logika przetwarzania poszczególnych wierszy, jest oddzielona od in filtrowania, za które odpowiada generator.
```python
def exclude_comments(fp):
	for line in fp:
		if not line.startswith('#'):
			yield line

with open('filename') as fp:
	for line in exclude_comments(fp):
		process(line)
```
Generatory wykorzystują tzw. leniwą ewaluację, która pozwala strumieniowo przetwarzać duże ilości danych bez konieczności wczytywania ich w całości do pamięci.