# Closures

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150904384/posts/2160071962

Functions defined within the function. It enables to pass variables to Callable types of arguments

## Manual closure

```python

def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")

def is_eligible_closure(cutoff_age: int) -> Callable[[Customer], bool]:
    def is_eligible(customer: Customer) -> bool:
        return customer.age > cutoff_age

    return is_eligible

def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    # Using closure enables to pass argument to is_eligible_closure function
    send_email_promotion(customers, is_eligible_closure(50))
```

## functools.partial

Same effect may be achieved by using partial function from functools package.

```python
from functools import partial

def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")

def is_eligible_for_promotion(customer: Customer, cutoff_age: int) -> bool:
    return customer.age > cutoff_age

def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    is_eligible = partial(is_eligible_for_promotion, cutoff_age=25)
    send_email_promotion(customers, is_eligible(50))
```