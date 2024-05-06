# Protocols

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535822/posts/2158612869

Instead of abstract classes it's possible to use protocols in Python. They don't rely on inheritance, but they rely on Python typing mechanism (duck typing).

```python
from typing import Protocol
from dataclasses import dataclass
import datetime
import math

# Protocol class with .reserve() method declared
class Vehicle(Protocol):
    def reserve(self, start_date: datetime, days: int):
        ...

# Dataclass with .reserve() method implemented. No need to inherit Vehicle class.
@dataclass
class Car:
    model: str
    reserved: bool = False

    def reserve(self, start_date: datetime, days: int):
        self.reserved = True
        print(f"Reserving car {self.model} for {days} days at date {start_date}.")

    def renew_license(self, new_license_date: datetime):
        print(f"Renewing license of car {self.model} to {new_license_date}.")

# Another class with .reserver() method.
@dataclass
class Truck:
    model: str
    reserved: bool = False
    reserved_trailer: bool = False

    def reserve(self, start_date: datetime, days: int):
        months = math.ceil(days / 30)
        self.reserved = True
        self.reserved_trailer = True
        print(
            f"Reserving truck {self.model} for {months} month(s) at date {start_date}, including a trailer."
        )

# Typing vehicle as Vehicle is fine here, because both Car and Truck have .reserve() methods, so for typing system (duck typing) they are "the same" 
def reserve_now(vehicle: Vehicle):
    vehicle.reserve(datetime.now(), 40)
```