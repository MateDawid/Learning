# fetch
Pozwala na wykonanie zapytania pod wskazanym adresem URL.
```javascript
 fetch('https://api.exchangeratesapi.io/latest?base=USD')
 .then(response => response.json())
 .then(data => {
     console.log(data);
 });
```