# **Python - Clean code**
## Code standards
### PEP 8
PEP 8 naming conventions:
* class names should be CamelCase (MyClass)
* variable names should be snake_case and all lowercase (first_name)
* function names should be snake_case and all lowercase (quick_sort())
* constants should be snake_case and all uppercase (PI = 3.14159)
* modules should have short, snake_case names and all lowercase (numpy)
* single quotes and double quotes are treated the same (just pick one and be consistent)

PEP 8 line formatting:
-   indent using 4 spaces (spaces are preferred over tabs)
-   lines should not be longer than 79 characters
-   avoid multiple statements on the same line
-   top-level function and class definitions are surrounded with two blank lines
-   method definitions inside a class are surrounded by a single blank line
-   imports should be on separate lines

PEP 8 whitespace:
-   avoid extra spaces within brackets or braces
-   avoid trailing whitespace anywhere
-   always surround binary operators with a single space on either side
-   if operators with different priorities are used, consider adding whitespace around the operators with the lowest priority
-   don't use spaces around the = sign when used to indicate a keyword argument

PEP 8 comments:
-   comments should not contradict the code
-   comments should be complete sentences
-   comments should have a space after the # sign with the first word capitalized
-   multi-line comments used in functions (docstrings) should have a short single-line description followed by more text

### Pythonic Code
There's a big difference between writing Python code and writing Pythonic code. To write Pythonic code you can't just idiomatically translate another language (like Java or C++) to Python; you need to be thinking in Python to being with.
Let's look at an example. We have to add the first 10 numbers together like so  `1 + 2 + ... + 10`.

A non-Pythonic solution would be something like this:
```python
n = 10
sum_all = 0

for i in range(1, n + 1):
    sum_all = sum_all + i

print(sum_all)  # 55
```

A more Pythonic solution might look like this:
```python
n = 10
sum_all = sum(range(1, n + 1))

print(sum_all)  # 55
```
### The Zen of Python
```
>>> import this

The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```
## Code Principles
### DRY (Don't repeat yourself)
This is one of the simplest coding principles. Its only rule is that code should not be duplicated. Instead of duplicating lines, find an algorithm that uses iteration. DRY code is easily maintainable. You can take this principle even further with model/data abstraction.

The cons of the DRY principle are that you can end up with too many abstractions, external dependency creations, and complex code. DRY can also cause complications if you try to change a bigger chunk of your codebase. This is why you should avoid DRYing your code too early. It's always better to have a few repeated code sections than wrong abstractions.
### KISS (Keep it simple, stupid)
The KISS principle states that most systems work best if they are kept simple rather than made complicated. Simplicity should be a key goal in design, and unnecessary complexity should be avoided.
### SoC (Separation of concerns)
SoC is a design principle for separating a computer program into distinct sections such that each section addresses a separate concern. A concern is a set of information that affects the code of a computer program.

A good example of SoC is  MVC (Model - View - Controller).

If you decide to go with this approach be careful not to split your app into too many modules. You should only create a new module when it makes sense to do so. More modules equals more problems.
### SOLID
SOLID is extremely useful when writing OOP code. It talks about splitting your class into multiple subclasses, inheritance, abstraction, interfaces, and more.

It consists of the following five concepts:

-   The  **S**ingle-responsibility principle "A class should have one, and only one, reason to change."
-   The  **O**pen–closed principle: "Entities should be open for extension, but closed for modification."
-   The  **L**iskov substitution principle: "Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."
-   The  **I**nterface segregation principle: "A client should not be forced to implement an interface that it doesn’t use."
-   The  **D**ependency inversion principle: "Depend upon abstractions, not concretions."

## Code Formatters
