# Protocols

> Sources: 
> * https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150535822/posts/2158612869
> * https://realpython.com/python-protocol

Instead of abstract classes it's possible to use protocols in Python. They don't rely on inheritance, but they rely on Python typing mechanism (duck typing).

```python
from typing import Protocol
from dataclasses import dataclass
import datetime
import math

# Protocol class with .reserve() method declared
class Vehicle(Protocol):
    def reserve(self, start_date: datetime, days: int):
        ...

# Dataclass with .reserve() method implemented. No need to inherit Vehicle class.
@dataclass
class Car:
    model: str
    reserved: bool = False

    def reserve(self, start_date: datetime, days: int):
        self.reserved = True
        print(f"Reserving car {self.model} for {days} days at date {start_date}.")

    def renew_license(self, new_license_date: datetime):
        print(f"Renewing license of car {self.model} to {new_license_date}.")

# Another class with .reserver() method.
@dataclass
class Truck:
    model: str
    reserved: bool = False
    reserved_trailer: bool = False

    def reserve(self, start_date: datetime, days: int):
        months = math.ceil(days / 30)
        self.reserved = True
        self.reserved_trailer = True
        print(
            f"Reserving truck {self.model} for {months} month(s) at date {start_date}, including a trailer."
        )

# Typing vehicle as Vehicle is fine here, because both Car and Truck have .reserve() methods, so for typing system (duck typing) they are "the same" 
def reserve_now(vehicle: Vehicle):
    vehicle.reserve(datetime.now(), 40)
```

## Generic protocols
```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class GenericProtocol(Protocol[T]):
    def method(self, arg: T) -> T:
        ...
```
```python
from typing import Protocol, TypeVar

T = TypeVar("T", bound=int | float)

class Adder(Protocol[T]):
    def add(self, x: T, y: T) -> T:
        ...

class IntAdder:
    def add(self, x: int, y: int) -> int:
        return x + y

class FloatAdder:
    def add(self, x: float, y: float) -> float:
        return x + y

def add(adder: Adder) -> None:
    print(adder.add(2, 3))

add(IntAdder())
add(FloatAdder())
```
In this example, you first define a generic type for your protocol. You use the bound argument to state that the generic type can be an int or float object. Then, you have your concrete adders. In this case, you have IntAdder and FloatAdder to sum numbers.

If you’re using Python 3.12, then you can use a simplified syntax:
```python
from typing import Protocol

class Adder(Protocol):
    def add[T: int | float](self, x: T, y: T) -> T:
        ...

# ...
```

## Class vars
```python
from abc import abstractmethod
from typing import ClassVar, Protocol

class ProtocolMembersDemo(Protocol):
    class_attribute: ClassVar[int]
    instance_attribute: str = ""

    def instance_method(self, arg: int) -> str:
        ...

    @classmethod
    def class_method(cls) -> str:
        ...

    @staticmethod
    def static_method(arg: int) -> str:
        ...

    @property
    def property_name(self) -> str:
        ...

    @property_name.setter
    def property_name(self, value: str) -> None:
        ...

    @abstractmethod
    def abstract_method(self) -> str:
        ...
```

## Recursive protocols
You can also define recursive protocols, which are protocols that reference themselves in their definition. To reference a protocol, you must provide its name as strings.

```python
from typing import Optional, Protocol

class LinkedListNode(Protocol):
    value: int
    next_node: Optional["LinkedListNode"]

    def __str__(self) -> str:
        return f"{self.value} -> {self.next_node}"
```
To reference a protocol within its definition, you must include its name as a string literal to avoid errors. That’s because you can’t refer to a type that isn’t fully defined yet. While this limitation will change in the future, for now, you can use a future import as an alternative:
```python
from __future__ import annotations
from typing import Optional, Protocol

class LinkedListNode(Protocol):
    value: int
    next_node: Optional[LinkedListNode]

    def __str__(self) -> str:
        return f"{self.value} -> {self.next_node}"
```
## Predefined protocols
|Class|	Methods|
|-|-|
|Container|	.__contains__()|
|Hashable|	.__hash__()|
|Iterable|	.__iter__()|
|Iterator|	.__next__() and .__iter__()|
|Reversible|	.__reversed__()|
|Generator|	.send(), .throw(), .close(), .__iter__(), and .__next__()|
|Sized|	.__len__()|
|Callable|	.__call__()|
|Collection|	.__contains__(), .__iter__(), and .__len__()|
|Sequence|	.__getitem__(), .__len__(), .__contains__(), .__iter__(), .__reversed__(), .index(), and .count()|
|MutableSequence|	.__getitem__(), .__setitem__(), .__delitem__(), .__len__(), .insert(), .append(), .clear(), .reverse(), .extend(), .pop(), .remove(), and .__iadd__()|
|ByteString|	.__getitem__() and .__len__()|
|Set|	.__contains__(), .__iter__(), .__len__(), .__le__(), .__lt__(), .__eq__(), .__ne__(), .__gt__(), .__ge__(), .__and__(), .__or__(), .__sub__(), .__xor__(), and .isdisjoint()|
|MutableSet|	.__contains__(), .__iter__(), .__len__(), .add(), .discard(), .clear(), .pop(), .remove(), .__ior__(), .__iand__(), .__ixor__(), and .__isub__()|
|Mapping|	.__getitem__(), .__iter__(), .__len__(), .__contains__(), .keys(), .items(), .values(), .get(), .__eq__(), and .__ne__()|
|MutableMapping|	.__getitem__(), .__setitem__(), .__delitem__(), .__iter__(), .__len__(), .pop(), .popitem(), .clear(), .update(), and .setdefault()|
|AsyncIterable|	.__aiter__()|
|AsyncIterator|	.__anext__() and .__aiter__()|
|AsyncGenerator|	.asend(), .athrow(), .aclose(), .__aiter__(), and .__anext__()|
|Buffer|	.__buffer__()|