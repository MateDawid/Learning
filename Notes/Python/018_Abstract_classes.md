# Abstract Classes

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535822/posts/2158612840

Abstract classes lets to write base model / sketch for other functions that will share same interfaces.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import math

class Vehicle(ABC):
    @abstractmethod
    def reserve(self, start_date: datetime, days: int):
        """A vehicle can be reserved for renting"""

    @abstractmethod
    def renew_license(self, new_license_date: datetime):
        """Renews the license of a vehicle."""

@dataclass
class Car(Vehicle):
    model: str
    reserved: bool = False

    def reserve(self, start_date: datetime, days: int):
        self.reserved = True
        print(f"Reserving car {self.model} for {days} days at date {start_date}.")

    def renew_license(self, new_license_date: datetime):
        print(f"Renewing license of car {self.model} to {new_license_date}.")


@dataclass
class Truck(Vehicle):
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
```