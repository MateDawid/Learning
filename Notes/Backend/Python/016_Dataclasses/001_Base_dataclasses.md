# Dataclasses

Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

## Intro

Instead of usual class definitions, dataclasses enables to get rid of boilerplate code and define object oriented mainly on data instead of behaviour.

```python
from dataclasses import dataclass
from enum import Enum, auto


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()

@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    license_plate: str
    fuel_type: FuelType = FuelType.ELECTRIC
```