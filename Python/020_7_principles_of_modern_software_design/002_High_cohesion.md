# High cohesion

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150528069/posts/2153184358

We can say that function has high cohesion, when it has single responsibility and uses other classes and functions to do other things.

## Order class with low cohesion

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

    def pay(self, payment_type: str, security_code: str) -> None:
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")


def main() -> None:
    order = Order()
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    order.pay("debit", "0372846")


if __name__ == "__main__":
    main()
```

`Order` class has many responsibilities - it handles adding new items to order and paying for order with many payment types.

## Order with high cohesion

```python
from enum import Enum, auto


class PaymentStatus(Enum):
    """Payment status"""

    OPEN = auto()
    PAID = auto()


class Order:
    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[int] = []
        self.status: PaymentStatus = PaymentStatus.OPEN

    def add_item(self, name: str, quantity: int, price: int) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)


class PaymentProcessor:
    def pay_debit(self, order: Order, security_code: str) -> None:
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = PaymentStatus.PAID

    def pay_credit(self, order: Order, security_code: str) -> None:
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = PaymentStatus.PAID


def main():
    order = Order()
    order.add_item("Keyboard", 1, 5000)
    order.add_item("SSD", 1, 15000)
    order.add_item("USB cable", 2, 500)

    processor = PaymentProcessor()
    processor.pay_debit(order, "0372846")


if __name__ == "__main__":
    main()

```

After minor refactoring `Order` class has only responsibility to add items and store order data.
Payment processes were moved to separate `PaymentProcessor` class, where all payment types have separate method for handling payment.
Statuses were changed to Enum instead of raw string.