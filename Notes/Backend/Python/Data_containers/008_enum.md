# enum

Moduł pozwalający na tworzenie typów wyliczeniowych.
```python
from enum import Enum

class Season(Enum):
	SPRING = 1
	SUMMER = 2
	AUTUMN = 3
	WINTER = 4

# printing enum member as string
Season.SPRING
# Season.SPRING

# printing name of enum member using "name" keyword
print(Season.SPRING.name)
# SPRING

# printing value of enum member using "value" keyword
print(Season.SPRING.value)
# 1

# printing the type of enum member using type()
print(type(Season.SPRING))
# <enum 'Season'>

# printing enum member as repr
print(repr(Season.SPRING))
# <Season.SPRING: 1>

# printing all enum member using "list" keyword
print(list(Season))
# [<Season.SPRING: 1>, <Season.SUMMER: 2>, <Season.AUTUMN: 3>, <Season.WINTER: 4>]
```