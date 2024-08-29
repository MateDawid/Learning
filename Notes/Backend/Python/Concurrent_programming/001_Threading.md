# Obsługa wątków
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