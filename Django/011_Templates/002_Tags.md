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

## Reversed list iteration

```html
{% for pizza in pizza_menu reversed %}
    <div>{{ pizza }}</div>
{% endfor %} 
```

## Item index during iteration

* `{{ forloop.counter0 }}`

Returns loop counter starting from 0.

```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.counter0 }} - {{ pizza }}
    </div>
{% endfor %}
```
* `{{ forloop.counter }}`
Returns loop counter starting from 1.
```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.counter }} - {{ pizza }}
    </div>
{% endfor %} 
```
* `{{ forloop.revcounter0 }}`
Returns reverted loop counter ending on 0.
```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.revcounter0 }} - {{ pizza }}
    </div>
{% endfor %} 
```
* `{{ forloop.revcounter }}`
Returns reverted loop counter ending on 1.
```html
{% for pizza in pizza_menu %}
    <div>
    {{ forloop.revcounter }} - {{ pizza }}
    </div>
{% endfor %} 
```

## Detecting first/last element during iteration

* `{{ forloop.first }}`
```html
{% for pizza in pizza_menu %}
<div>
    {{ pizza }}
    {% if forloop.first %} - MNIAM
    {% endif %}
</div>
{% endfor %}
```
* `{{ forloop.last }}`
```html
{% for pizza in pizza_menu %}
<div>
    {{ pizza }}
    {% if forloop.last %} - MNIAM
    {% endif %}
</div>
{% endfor %}
```

## Detecting empty list
`{% empty %}`
```html
<ul>
{% for pizza in pizza_menu %}
    <li>{{ pizza.name }}</li>
{% empty %}
    <li>Wszystko zjedzone :( </li>
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
