# timeit

> Source: https://www.youtube.com/watch?v=zPfSwhofPpk

```python
import timeit

# Implementation 1: List comprehension
code1 = """
a = [1 ,2, 3, 4, 5]
b = [x * 2 for x in a]
"""

# Implementation 2: map function
def code2():
    a = [1, 2, 3, 4, 5]
    b = list(map(lambda x: x * 2, a))


# Check execution time of both functions
time1 = timeit.timeit(code1, number=100000)
time2 = timeit.timeit(code1, number=100000)
```
