# Callback

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2150393709/posts/2160000927

## Callback pattern

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Button:
    label: str
    on_click: Callable[[Button], None] = lambda _: None

    def click(self) -> None:
        print(f"Clicked on [{self.label}].")
        self.on_click(self)


def main() -> None:
    def click_handler(button: Button) -> None:
        print(f"Handling click for button [{button.label}].")

    my_button = Button(label="Do something", on_click=click_handler)
    # my_button = Button(
    #     label="Do something", on_click=lambda _: print("Handling click!")
    # )
    my_button.click()
```
* Button class having `click` method.
* `click` method performing `on_click` function defined on class setup
