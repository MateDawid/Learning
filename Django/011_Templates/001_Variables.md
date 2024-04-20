# Variables in templates

Source: https://pogromcykodu.pl/html-na-sterydach/

## Example view
```python
class StudentsView(View):
    def get(self, request):
        student_1 = {'name': 'John', 'surname': 'Black', 'grade':5.0}
        student_2 = {'name': 'Mary', 'surname': 'White', 'grade': 3.5}
        context = {
            'student_1': student_1,
            'student_2': student_2
        }
        return render(request, 'students.html', context=context)
```
## Variables
Template:
```html
Student 1 : {{ student_1 }}
Student 2 : {{ student_2 }} 
```
Display:
```
Student 1: {'name': 'John', 'surname': 'Black', 'grade': 5.0}
Student 2: {'name': 'Mary', 'surname': 'White', 'grade': 3.5}
```
## Dict values
Template:
```html
Student 1:
Imię: {{ student_1.name }}, Nazwisko: {{ student_1.surname }}
```
Output:
```
Student 1:
Imię: John, Nazwisko: Black
```
## Class objects
```python
class Student:
    def __init__(self, name, surname, grade):
        self.name = name
        self.surname = surname
        self.grade = grade 

...

student_3 = Student(name='Mike', surname='Doe', grade=4.5)
context = {
            ...
            'student_3': student_3
}    
```
Template:
```html
Student 3:
Imię: {{ student_3.name}}, Nazwisko: {{ student_3.surname }} 
```
Output:
```
Student 3:
Imię: Mike, Nazwisko: Doe
```

## Lists

```python
students_list = [student_1, student_2, student_3]
context = {
            ...
            'students_list': students_list
} 
```
Template:
```html
Pierwszy student z listy: {{ students_list.0 }}
Drugi student z listy: {{ students_list.1 }} 
```
Output:
```
Pierwszy student z listy: {'name': 'John', 'surname': 'Black', 'grade': 5.0}
Drugi student z listy: {'name': 'Mary', 'surname': 'White', 'grade': 3.5}
```

