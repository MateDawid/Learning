# Pipeline patterns

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946552/posts/2160000607

## Chain of responsibility pattern

```mermaid
classDiagram
    Client ..> Handler
    class Handler {
        <<abstract>>
        setNext(handler: Handler)
        handle(request)
    }
    Handler --> Handler : next
    class ConcreteHandler1 {
        setNext(handler: Handler)
        handle(request)
    }
    class ConcreteHandler2 {
        setNext(handler: Handler)
        handle(request)
    }
    ConcreteHandler1 --|> Handler
    ConcreteHandler2 --|> Handler
```

* Client uses a Handler for some process
* Handler has setNext() method to indicate, what next Handler should process request

```mermaid
classDiagram
    Client ..> Handler
    class Handler {
        <<abstract>>
        set_next(handler: Handler)
        handle_click_event()
        bool on_click()
    }
    Handler --> Handler : next
    class Button {
        name: str
        disabled: bool
        set_next(handler: Handler)
        handle_click_event(request)
        bool on_click()
    }
    class Panel {
        name: str
        disabled: bool
        set_next(handler: Handler)
        handle_click_event(request)
        bool on_click()
    }
    class Window {
        name: str
        set_next(handler: Handler)
        handle_click_event(request)
        bool on_click()
    }
    Button --|> Handler
    Panel --|> Handler
    Window --|> Handler
```
* Client uses a Handler subclasses for processing request
* Button, Panel and Window as subclasses of Handler abstract class

## Chain of responsibility implementation

```python
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Optional


class Handler(ABC):
    def __init__(self):
        self.next: Optional[Handler] = None

    def set_next(self, handler: Handler) -> None:
        self.next = handler

    def handle_click_event(self) -> None:
        if self.on_click() and self.next:
            self.next.handle_click_event()

    def on_click(self) -> bool:
        """Handle a click event."""
        return True


@dataclass
class Button(Handler):
    name: str = "button"
    disabled: bool = False

    def on_click(self) -> bool:
        if self.disabled:
            return True
        print(f"Button [{self.name}] handling click.")
        return False


@dataclass
class Panel(Handler):
    name: str = "panel"
    disabled: bool = False


@dataclass
class Window(Handler):
    name: str = "window"

    def on_click(self) -> bool:
        print(f"Window [{self.name}] handling click.")
        return False


def main() -> None:
    button = Button(name="my_button", disabled=False)
    panel = Panel(name="my_panel", disabled=False)
    window = Window(name="my_window")

    # setup the chain of responsibility
    button.set_next(panel)
    panel.set_next(window)

    button.handle_click_event()
```

## Sequence of functions

```python
from functools import partial, reduce
from typing import Callable

ComposableFunction = Callable[[float], float]

# Helper function for composing functions
def compose(*functions: ComposableFunction) -> ComposableFunction:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def add_three(x: float) -> float:
    return x + 3


def multiply_by_two(x: float) -> float:
    return x * 2


def add_n(x: float, n: float) -> float:
    return x + n


def main():
    x = 12
    # oldres = multiplyByTwo(multiplyByTwo(addThree(addThree(x))))
    myfunc = compose(
        partial(add_n, n=3), partial(add_n, n=2), multiply_by_two, multiply_by_two
    )
    result = myfunc(x)
    print(result)


if __name__ == "__main__":
    main()

```