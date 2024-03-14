# Code Principles
## DRY (Don't repeat yourself)
This is one of the simplest coding principles. Its only rule is that code should not be duplicated. Instead of duplicating lines, find an algorithm that uses iteration. DRY code is easily maintainable. You can take this principle even further with model/data abstraction.

The cons of the DRY principle are that you can end up with too many abstractions, external dependency creations, and complex code. DRY can also cause complications if you try to change a bigger chunk of your codebase. This is why you should avoid DRYing your code too early. It's always better to have a few repeated code sections than wrong abstractions.
## KISS (Keep it simple, stupid)
The KISS principle states that most systems work best if they are kept simple rather than made complicated. Simplicity should be a key goal in design, and unnecessary complexity should be avoided.
## SoC (Separation of concerns)
SoC is a design principle for separating a computer program into distinct sections such that each section addresses a separate concern. A concern is a set of information that affects the code of a computer program.

A good example of SoC is  MVC (Model - View - Controller).

If you decide to go with this approach be careful not to split your app into too many modules. You should only create a new module when it makes sense to do so. More modules equals more problems.
## SOLID
SOLID is extremely useful when writing OOP code. It talks about splitting your class into multiple subclasses, inheritance, abstraction, interfaces, and more.

It consists of the following five concepts:

-   The  **S**ingle-responsibility principle "A class should have one, and only one, reason to change."
-   The  **O**pen–closed principle: "Entities should be open for extension, but closed for modification."
-   The  **L**iskov substitution principle: "Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."
-   The  **I**nterface segregation principle: "A client should not be forced to implement an interface that it doesn’t use."
-   The  **D**ependency inversion principle: "Depend upon abstractions, not concretions."
