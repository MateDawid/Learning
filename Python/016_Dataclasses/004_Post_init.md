# __post_init__

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

To perform some actions just before initialization of dataclass objects they have to be specified in `.__post__init__` method.

```python
@dataclass
class Vehicle:
    ...
    def __post_init__(self):
        self.license_plate = generate_vehicle_license()
```