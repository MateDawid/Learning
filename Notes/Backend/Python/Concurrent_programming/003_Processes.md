# Procesy
```python
from multiprocessing import Process

def reverse(text):
	return text[::-1]

if __name__ == '__main__':
	p = Process(target=reverse, args=('foobar',))
	p.start()
	p.join()
```