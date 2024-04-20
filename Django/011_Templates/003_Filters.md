# Filters

Source: https://pogromcykodu.pl/html-na-sterydach/

## Pattern

`{{ variable | filter_name }} `

## Example data
```python
student_1 = {
    'name': 'John', 
    'surname': 'Black', 
    'grade': 5.0,
    'birth_date': datetime(2000, 10, 27, 16, 25),  
    'has_graduated': True, 
    'bio': 'Very smart n and intelligent.', 
    'scholarship': ''
}
```
## String operations
* `lower` – lowercasing string. Example: `{{ student_1.name | lower }}`  ➜  john.
* `upper` – uppercasing string. Example: `{{ student_1.name | upper }}`   ➜  JOHN 
* `title` – changing first letter of single word to upper case.  Example:  `{{ student_1.bio | title }}`   ➜  Very Smart And Intelligent.
* `slice` – slicing string. Example:  `{{ student_1.bio | slice:"5:16" }}`   ➜  smart and
* `truncatechars` – cutting string to given length, including '...'. Example:  `{{ student_1.bio | truncatechars:7 }}`   ➜  Very s…
* `truncatewords` – cutting string to given words count, adding '...'. Example:  `{{ student_1.bio | truncatewords:2 }}`   ➜  Very smart …
* `linebreaksbr` – replacing '\n' with <br>.

## Date/hour formatting
`date` – date in given format. Example: `{{ student_1.birth_date | date:"d/m/Y" }}`   ➜  27/10/2000
`time` – time in given format. Example: `{{ student_1.birth_date | time:"H:i" }}`   ➜  16:25
## Empty/default values
`default` – replacing empty string or none with default. Example: `{{ student_1.scholarship | default:"Brak" }}`   ➜  Brak 
`yesno` – custom string for boolean values.. Example: `{{ student_1.has_graduated | yesno:"Tak,Nie" }}`   ➜  Tak
