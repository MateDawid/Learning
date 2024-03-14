# Kolejki

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