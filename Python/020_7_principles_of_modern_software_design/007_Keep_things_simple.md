# Keep things simple

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150437717/posts/2153274144

## DRY

Don't repeat yourself. Remove duplications. But it's not always needed to create too generic replacements for existing duplication,
let's keep things simple and easy to maintain.

### Before 

```python
def read_vehicle_type() -> str:
    vehicle_types = ["vw", "bmw", "tesla"]
    vehicle_type = ""
    while vehicle_type not in vehicle_types:
        vehicle_type = input(
            f"What type of vehicle would you like to rent ({', '.join(vehicle_types)})? "
        )
    return vehicle_type


def read_vehicle_color() -> str:
    vehicle_colors = ["black", "red", "blue"]
    vehicle_color = ""
    while vehicle_color not in vehicle_colors:
        vehicle_color = input(
            f"What color vehicle would you like to rent ({', '.join(vehicle_colors)})? "
        )
    return vehicle_color

def main():

    vehicle_type = read_vehicle_type()
    vehicle_color = read_vehicle_color()
```

### After

```python
def read_choice(question: str, choices: list[str]) -> str:
    choice = ""
    while choice not in choices:
        choice = input(f"{question} ({', '.join(choices)})? ")
    return choice

def main():

    vehicle_type = read_choice(
        "What type of vehicle would you like to rent", ["vw", "bmw", "tesla"]
    )

    vehicle_color = read_choice(
        "What color vehicle would you like to rent", ["black", "red", "blue"]
    )
```

## KISS

Keep it simple, stupid - this rule leads to not overcomplicating your code - do not use abstraction, protocols and other stuff,
if the only thing you need to do is to add two integers.

## YAGNI

You Ain't Gonna Need It - this rule speaks about not implementing something, that you don't need right now. Don't create extra 
features - users will ask you for them if they will be needed.  