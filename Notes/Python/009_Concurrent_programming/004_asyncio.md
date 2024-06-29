# asyncio
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
