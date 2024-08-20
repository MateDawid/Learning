# Avoid type abuse

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129429

```python
from dataclasses import dataclass

@dataclass
class User:
    first_name: str
    last_name: str
    role: str
```

`role` field in this case is passed as `str`, so you can pass anything to this. Instead of such approach, use Enum for
controlling content of such fields.

```python
from dataclasses import dataclass
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


@dataclass
class User:
    first_name: str
    last_name: str
    role: Role
```