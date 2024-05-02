# Default values

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

Initially dataclasses do not allow to specify mutable values (like lists) as defaults for fields.
```python
@dataclass
class Vehicle:
    brand: str
    model: str
    color: str = 'white'
    license_plate: str
    fuel_type: FuelType = FuelType.ELECTRIC
    accessories: list[Accessory] = []  # It won't work
```

Instead we can use `field` method to specify it with `lambda` statement or function (like `list`).

```python
from dataclasses import dataclass, field
from enum import Enum, auto

class Accessory(Enum):
    AIRCO = auto()
    CRUISECONTROL = auto()
    NAVIGATION = auto()
    OPENROOF = auto()
    BATHTUB = auto()
    MINIBAR = auto()


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
    accessories: list[Accessory] = field(default_factory=lambda: [Accessory.AIRCO])
```
