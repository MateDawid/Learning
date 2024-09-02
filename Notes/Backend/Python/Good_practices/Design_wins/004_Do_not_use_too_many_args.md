# Don't use too many arguments

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129469

```python
@dataclass
class Reservation:
    room_id: str
    customer_first_name: str
    customer_last_name: str
    customer_email_address: str
    from_date: datetime
    to_date: datetime
    price: int

@dataclass
class Hotel:
    ...
    def reserve_room(
        self,
        room_id: str,
        customer_first_name: str,
        customer_last_name: str,
        customer_email_address: str,
        from_date: datetime,
        to_date: datetime,
    ) -> None:
        ...

def main():
    hotel = Hotel()
    hotel.add_room(Room(id="1A", size=20, price=200_00))
    
    hotel.reserve_room(
        "1A",
        "Arjan",
        "Codes",
        "hi@arjancodes.com",
        datetime(2022, 7, 15),
        datetime(2022, 7, 17),
    )
```
In this case reserving a room needs plenty of arguments, that describes Customer, that may become separate class.

```python
@dataclass
class Customer:
    first_name: str
    last_name: str
    email_address: str


@dataclass
class Reservation:
    room_id: str
    customer_id: str
    from_date: datetime
    to_date: datetime
    price: int

@dataclass
class Hotel:
    ...
    def reserve_room(
        self,
        room_id: str,
        customer_id: str,
        from_date: datetime,
        to_date: datetime,
    ) -> None:
    ...

def main():
    hotel = Hotel()
    hotel.add_room(Room(id="1A", size=20, price=200_00))

    hotel.add_customer(
        Customer(
            first_name="Arjan", last_name="Codes", email_address="hi@arjancodes.com"
        )
    )
    hotel.reserve_room(
        "1A",
        "hi@arjancodes.com",
        datetime(2022, 7, 15),
        datetime(2022, 7, 17),
    )
```