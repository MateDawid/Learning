# Type hints

Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535947/posts/2158623370

## Base type hints

```python
def add_three(x: int) -> int:
    return x + 3
```

`x: int` -> `x` argument is suggested to be integer, if not no error will be raised, but it informs, that function was created for int arguments.
`-> int` -> function will return `int`

## Callables

```python
from typing import Callable

IntFunction = Callable[[int], int]

def add_three(x: int) -> int:
    return x + 3

def main():
    my_var: IntFunction = add_three
    print(my_var(5))
```

```Callable[[int], int]``` -> defines type for Callable (function in this case), that takes int as argument (`[int]`) and returns int (second `int` in declaration)

```my_var: IntFunction``` -> typing variable with custom type