# Depend on Abstractions

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150479414/posts/2153274138

The goal of this rule is to keep as least coupling in code as possible and it is achievable by using abstraction layers 
like abstract classes and protocols.

You have to have one "dirty" place, where all your implementations starts to "live". If you need to change your code in 
different your code in many places after minor change - you need to use more abstractions, because coupling is too high. 

## Using typing as abstraction
### Before

`__init__` method of `PaymentProcessor` class needing to "know" about all authorization methods, that exists in 
separate module.

```python
from pos.authorization import authorize_google, authorize_robot, authorize_sms


class PaymentProcessor:
    def __init__(self, authorizer_type: str):
        if authorizer_type == "google":
            self.authorize = authorize_google
        elif authorizer_type == "sms":
            self.authorize = authorize_sms
        else:
            self.authorize = authorize_robot
```

### After 
Particular authorizing functions replaced with abstraction created with Python typing system. In this case `PaymentProcessor` 
gets authorizing function as an argument instead of string. 

Another benefit is that `PaymentProcess` is no longer responsible for determining authorizing system. 
```python
from typing import Callable

AuthorizeFunction = Callable[[], bool]

class PaymentProcessor:
    def __init__(self, authorize: AuthorizeFunction):
        self.authorize = authorize
```

## Using protocol for abstraction 

### Before
`PaymentProcessor` dependent directly on `Order` class and changing it's params (so it needs to know about implementation details).

```python
class PaymentProcessor:
    ...
    
    def pay_debit(self, order: Order) -> None:
        if not self.authorize():
            raise Exception("Not authorized")
        print(f"Processing debit payment for amount: ${(order.total_price / 100):.2f}.")
        order.status = PaymentStatus.PAID
```
### After
Instead of using `Order` class in `PaymentProcessor` implementation using `Payable` protocol providing methods and properties needed by `PaymentProcessor`. 

```python
class Payable(Protocol):
    @property
    def total_price(self) -> int:
        ...

    def set_payment_status(self, status: PaymentStatus) -> None:
        ...

class PaymentProcessor:
    ...
    
    def pay_debit(self, payable: Payable) -> None:
        if not self.authorize():
            raise Exception("Not authorized")
        print(f"Processing debit payment for amount: ${(payable.total_price / 100):.2f}.")
        payable.set_payment_status(PaymentStatus.PAID)
```