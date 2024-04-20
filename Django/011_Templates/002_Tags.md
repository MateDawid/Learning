# Tags

Source: https://pogromcykodu.pl/html-na-sterydach/

## List iteration

`{% for ... in ... %}`

Template:
```html
<ul>
    {% for student in students_list %}
        <li>{{ student.name }} {{ student.surname }}</li>
    {% endfor %}
</ul> 
```

## If/else
`{% if ... elif ... else %}`
Template:
```html
<ul>
    {% for student in students_list %}
        <li>
        {{ student.name }} {{ student.surname }}
        {% if student.grade == 5.0 %} - Kujon
        {% elif student.grade > 4 %} - Tak trzymaj!
        {% else %} - Pora na naukę!
        {% endif %}
        </li>
     {% endfor %}
</ul> 
```

## Inheritance and templates extending

* `{% block ... %} {% endblock %}` – defining block to override in different template
* `{% extends ... %}` – indicating template to extend
* `{% include %}` – input other template
* `{% load %}` – loading additional tags
