# Line profiling

Source: https://www.freecodecamp.org/news/python-debugging-handbook/#profiling

Understanding memory usage is crucial for optimizing code. The memory_profiler module helps in profiling memory consumption.

```commandline
pip install memory-profiler
```

```python
from memory_profiler import profile

@profile
def example_function():
    # Your code here

if __name__ == "__main__":
    example_function()
```

When executed, this will display a line-by-line analysis of memory usage during the execution of the example_function

Understanding memory usage is crucial for optimizing code. The memory_profiler module helps in profiling memory consumption.