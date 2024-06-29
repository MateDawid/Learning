# querySelector
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca pierwszy element pasujący do zapytania.
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let name = document.querySelector('#name');
```
Przykład użycia:
```javascript
// Zmiana koloru tła elementu o tagu "body" na czerwony
let body = document.querySelector('body');
body.style.backgroundColor = 'red';
```

# querySelectorAll
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca listę obiektów pasujących do zapytania,
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let buttons = document.querySelectorAll('button');
```


