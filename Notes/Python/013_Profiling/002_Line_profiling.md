# Line profiling

Source: https://www.freecodecamp.org/news/python-debugging-handbook/#profiling

Line profiling allows you to see how much time is spent on each line of code within a function. The line_profiler module is commonly used for this purpose.

```commandline
pip install line_profiler
```

```python
from line_profiler import LineProfiler

def example_function():
    # Your code here

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler.add_function(example_function)

    profiler.run('example_function()')

    # Display the results
    profiler.print_stats()
```

This will show a detailed report with the time spent on each line within the example_function.