# Mixins

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150391101/posts/2153184360

Mixin is a pattern that uses multiple inheritance to inject some additional behaviour to existing class.

## Tradeoffs

1. Order of inheritance matters

Python resolves hierarchy of inheritance from right to left as stands in MRO.

```python
class Example(Mixin, A, B):
    ...
```
So all methods from class Mixin will override methods with the same names from class A. Only uniquely named methods 
from classes A and B will stay untouched.

So in that case Mixin class has to be always on the left to make sure that it's behaviour is actually executed.

2. Mixin as group of methods

It's strict that mixins should be groups of methods and should not contain any instance variables - otherwise they are 
just usual classes. 

## Better approach

Instead of injecting additional methods to class it's better to use composition (as stands in "Favor composition over 
inheritance" principle). It makes your code better to read and understand.