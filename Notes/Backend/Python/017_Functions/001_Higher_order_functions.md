# Higher order functions

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150904384/posts/2160071945

Functions that may take other function as an argument and/or return function as a return value.

```python
# This is higher-order function
def send_email_promotion(customers: list[Customer], is_eligible: Callable[[Customer], bool]) -> None:
    for customer in customers:
        if is_eligible(customer):
            print(f"{customer.name} is eligible for promotion.")
        else:
            print(f"{customer.name} is not eligible for promotion.")

            
def is_eligible_for_promotion(customer: Customer) -> bool:
    return customer.age >= 50


def main() -> None:
    customers = [
        Customer("Alice", 25),
        ...
    ]
    send_email_promotion(customers, is_eligible_for_promotion)
    # We can use lambda function also
    # send_email_promotion(customers, lambda customer: customer.age >= 50)
```