# Protected values

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

To prevent from overriding dataclass field during initialization you can use `init=False` statement on class value.

```python
@dataclass
class Vehicle:
    ...
    accessories: list[Accessory] = field(default_factory=lambda: [Accessory.AIRCO], init=False)
```

It will end up with error if during initialization field `accessories` will be provided.
