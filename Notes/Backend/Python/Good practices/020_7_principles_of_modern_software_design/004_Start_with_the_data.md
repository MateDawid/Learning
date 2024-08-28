# Start with the data

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150523714/posts/2153274137

You need to put the behaviour as closely as possible to the data, that it needs. It will reduce number of data, 
that you will need to pass along as parameters.

## Before

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from reader import read_kms_to_drive, read_rent_days, read_vehicle_type

FREE_KMS = 100


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    price_per_km: int
    price_per_day: int
    reserved: bool

    def total_price(self, days: int, additional_km: int) -> int:
        return days * self.price_per_day + additional_km * self.price_per_km


class ContractStatus(Enum):
    ORDERED = auto()
    PAID = auto()
    PICKED_UP = auto()
    DROPPED_OFF = auto()
    CANCELLED = auto()


@dataclass
class RentalContract:
    vehicle: Vehicle
    customer_id: int
    customer_name: str
    customer_address: str
    customer_postal_code: str
    customer_city: str
    customer_email: str
    contract_status: ContractStatus
    pickup_date: datetime
    days: int = 1
    additional_km: int = 0


VEHICLES = {
    "vw": Vehicle(
        "Volkswagen", "Golf", "black", FuelType.PETROL, "ABC123", 30, 6000, False
    ),
    "bmw": Vehicle("BMW", "X5", "green", FuelType.PETROL, "ABC123", 30, 8500, False),
    "ford": Vehicle(
        "Ford", "Fiesta", "white", FuelType.PETROL, "ABC123", 30, 12000, False
    ),
}


def main():

    vehicle_type = read_vehicle_type(list(VEHICLES.keys()))

    days = read_rent_days()

    additional_km = read_kms_to_drive()

    # setup the rental contract
    rental = RentalContract(
        VEHICLES[vehicle_type],
        12345,
        "Arjan",
        "Sesame street 104",
        "1234",
        "Amsterdam",
        "hi@arjancodes.com",
        ContractStatus.ORDERED,
        datetime.now(),
        days,
        max(additional_km - FREE_KMS, 0),
    )

    # log the rental information
    print(rental)

    # calculate the total price
    total_price = rental.vehicle.total_price(rental.days, rental.additional_km)
    print(f"Total price: ${total_price/100:.2f}")


if __name__ == "__main__":
    main()
```

## After

Data about customer was moved from `RentalContract` dataclass to separate `Customer` dataclass.

`total_price` property moved to `RentalContract` as in fact it is property of contract, not vehicle. Thanks to that change, 
in main function user won't need to know about implementation details (`total_price = rental.vehicle.total_price(rental.days, rental.additional_km)`) to make things working.

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from reader import read_kms_to_drive, read_rent_days, read_vehicle_type

FREE_KMS = 100


class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    price_per_km: int
    price_per_day: int
    reserved: bool


@dataclass
class Customer:
    id: int
    name: str
    address: str
    postal_code: str
    city: str
    email: str


class ContractStatus(Enum):
    ORDERED = auto()
    PAID = auto()
    PICKED_UP = auto()
    DROPPED_OFF = auto()
    CANCELLED = auto()


@dataclass
class RentalContract:
    vehicle: Vehicle
    customer: Customer
    contract_status: ContractStatus
    pickup_date: datetime
    days: int = 1
    additional_km: int = 0

    def total_price(self):
        return (
            self.days * self.vehicle.price_per_day
            + self.additional_km * self.vehicle.price_per_km
        )


VEHICLES = {
    "vw": Vehicle(
        "Volkswagen", "Golf", "black", FuelType.PETROL, "ABC123", 30, 6000, False
    ),
    "bmw": Vehicle("BMW", "X5", "green", FuelType.PETROL, "ABC123", 30, 8500, False),
    "ford": Vehicle(
        "Ford", "Fiesta", "white", FuelType.PETROL, "ABC123", 30, 12000, False
    ),
}


def main():
    customer = Customer(
        12345, "Arjan", "Sesame street 104", "1234", "Amsterdam", "hi@arjancodes.com"
    )

    vehicle_type = read_vehicle_type(list(VEHICLES.keys()))

    days = read_rent_days()

    additional_km = read_kms_to_drive()

    # setup the rental contract
    rental = RentalContract(
        VEHICLES[vehicle_type],
        customer,
        ContractStatus.ORDERED,
        datetime.now(),
        days,
        max(additional_km - FREE_KMS, 0),
    )

    # log the rental information
    print(rental)

    # calculate the total price
    print(f"Total price: ${rental.total_price()/100:.2f}")


if __name__ == "__main__":
    main()
```
