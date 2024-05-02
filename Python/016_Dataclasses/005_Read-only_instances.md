# Read-only dataclass instance

>Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535932

If we want to prevent from changing dataclass object after its initialization we have to use `frozen=True` param on `@dataclass` decorator.

```python
@dataclass(frozen=True)
class Vehicle:
    ...
```

>It will also disable all operations performed in `__post_init__` method! You can use `field(default_factory=)` as workaround.