# Low coupling

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150527399/posts/2153184359

## Coupling

Coupling is degree in which all parts of code need each other to work. The lower coupling is the more modular your program becomes. 
When coupling is low it's easy to reuse modules in many applications.

## Types of coupling
* Content coupling - when one class/method/function changes data in another class

```python
def add_item(order: Order, name: str, quantity: int, price: int) -> None:
    order.items.append(name)
    order.quantities.append(quantity)
    order.prices.append(price)
```

* Global coupling - when class/method/functions relies on global data shared by many parts of code, like global constant variables

```python
VEHICLE_DATA = {
    "vw": VehicleData(brand="vw", price_per_km=30, price_per_day=6000),
    "bmw": VehicleData(brand="bmw", price_per_km=35, price_per_day=8500),
    "ford": VehicleData(brand="ford", price_per_km=25, price_per_day=12000),
}
```

* External coupling - when application communicates with external sources, like API.
* Control coupling - when one part of your code controls flow of another part of code.
* Stamp coupling - when data structures are coupled in some way
* Data coupling - when many functions/classes uses the same data/objects
* Import coupling - when your application needs some third party libraries

## Principle of Least Knowledge / Law of Demeter

It says that you have to try to create units that only have knowledge and talk to closely related units.

Example:

`add_item` function operates on params of `Order` class, so it has to "know" that they exists.

```python
def add_item(order: Order, name: str, quantity: int, price: int) -> None:
    order.items.append(name)
    order.quantities.append(quantity)
    order.prices.append(price)
```

To make it work according to Law of Demeter it would be better to make `add_item` function `Order` class method - 
then it will be operating closely on `Order` class.

```python
class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: str = "open"

    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)
```
