# Use clear names

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129452

```python
from dataclasses import dataclass

@dataclass
class Contract:
    amount: float
    hourly_rate: int = 50_00

    def compute_pay(self):
        return self.amount * self.hourly_rate
```
In that case it's not known what `amount` exactly is. Renaming it to `hours_worked` makes it more understandable.

```python
from dataclasses import dataclass

@dataclass
class Contract:
    hours_worked: float
    hourly_rate: int = 50_00

    def compute_pay(self):
        return self.hours_worked * self.hourly_rate
```