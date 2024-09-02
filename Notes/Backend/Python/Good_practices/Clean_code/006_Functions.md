## Functions
### 1. Use verbs for function names
### 2. Do not use different words for the same concept
Pick a word for each concept and stick to it. Using different words for the same concept will cause confusion.
```python
# This is bad
def get_name(): pass
def fetch_age(): pass

# This is good
def get_name(): pass
def get_age(): pass
```
### 3. Write short and simple functions
### 4. Functions should only perform a single task
```python
# This is bad
def fetch_and_display_personnel():
    data = # ...

    for person in data:
        print(person)


# This is good
def fetch_personnel():
    return # ...

def display_personnel(data):
    for person in data:
        print(person)
```
### 5. Keep your arguments at a minimum
