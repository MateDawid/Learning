## Variables
### 1. Use nouns for variable names
### 2. Use descriptive/intention-revealing names
Other developers should be able to figure out what a variable stores just by reading its name.
### 3. Use pronounceable names
You should always use pronounceable names; otherwise, you'll have a hard time explaining your algorithms out loud.
### 4. Avoid using ambiguous abbreviations
Don't try to come up with your own abbreviations. It's better for a variable to have a longer name than a confusing name.
### 5. Always use the same vocabulary
Avoid using synonyms when naming variables.
```python
# This is bad
client_first_name = 'Bob'
customer_last_name = 'Smith'

# This is good
client_first_name = 'Bob'
client_last_name = 'Smith'
```
### 6. Don't use "magic numbers"
Magic numbers are strange numbers that appear in code, which do not have a clear meaning. Let's take a look at an example:
```python
import random

# This is bad
def roll():
    return random.randint(0, 36)  # what is 36 supposed to represent?

# This is good
ROULETTE_POCKET_COUNT = 36

def roll():
    return random.randint(0, ROULETTE_POCKET_COUNT)
```
Instead of using magic numbers, we can extract them into a meaningful variable.
### 7. Use solution domain names
If you use a lot of different data types in your algorithm or class and you can't figure them out from the variable name itself, don't be afraid to add data type suffix to your variable name. For example:
```python
# This is good
score_list = [12, 33, 14, 24]
word_dict = {
    'a': 'apple',
    'b': 'banana',
    'c': 'cherry',
}

# This is bad  (because you can't figure out the data type from the variable name)
names = ["Nick", "Mike", "John"]
```
### 8. Don't add redundant context
```python
# This is bad
class Person:
    def __init__(self, person_first_name, person_last_name, person_age):
        self.person_first_name = person_first_name
        self.person_last_name = person_last_name
        self.person_age = person_age


# This is good
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
```
We're already inside the `Person` class, so there's no need to add a `person_` prefix to every class variable.