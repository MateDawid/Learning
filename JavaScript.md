# **JavaScript**
## SKŁADNIA
### Zmienne
-   `var` - służy do definiowania globalnych zmiennych
```
var age = 20;
```

-   `let` - służy do definiowania zmiennych dla ograniczonego zakresu - danej funkcji lub pętli
```
let counter = 1;
```

-   `const` - służy do definiowania niezmiennych wartości
```
const PI = 3.14;
```
### Formatowanie stringów
```javascript
let number = 1
let formattedString = `Number: ${number}`
```
### JavaScript Object
Struktura podobna do słowników w Pythonie. Przykład użycia:
```javascript
let person = {
    first: 'Harry',
    last: 'Potter'
};
```
![Harry Potter](https://cs50.harvard.edu/web/2020/notes/5/images/console.png)
### Funkcje
Funkcje można zdefiniować na kilka sposobów:
* Funkcja nazwana
```javascript
function test(a, b){
	return a + b;
}
```
* Funkcja anonimowa (anonymous function)

Funkcję można również zdefiniować "w locie" - będzie ona wtedy wykorzystywana jedynie w miejscu jej zdefiniowania. Poniżej przykład użycia anonimowej funkcji w definicji eventListenera.
```javascript
let form = document.querySelector('form')
form.addEventListener('submit', function(e) {
		console.log('Submitted');
});
```
* Funkcja strzałkowa (arrow function)

Jeszcze prostszy sposób na zdefiniowanie funkcji. Znika potrzeba użycia słowa kluczowego **function**, jest ono zastąpione przez **=>**.
```javascript
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            document.querySelector("#hello").style.color = button.dataset.color;
        }
    });
});
```
### querySelector
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca pierwszy element pasujący do zapytania.
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let name = document.querySelector('#name');
```
### querySelector
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca listę obiektów pasujących do zapytania,
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let buttons = document.querySelectorAll('button');
```

### addEventListener
Pozwala na zdefiniowanie zachowania strony w momencie, gdy user wykona jakieś działanie, np. kliknie w odpowiedni element.
```javascript
// Kliknięcie elementu o id "name" powoduje zalogowanie do consoli słowa "CLICKED"
document.querySelector('#name').addEventListener('click', function()
	{
	    console.log('CLICKED');
	}
);
```
### dataset
Specjalny rodzaj atrybutów dla elementów DOM.
```html
...
<body>
    <button data-color="red">Red</button>
    <button data-color="blue">Blue</button>
    <button data-color="green">Green</button>
</body>
...
```
Dostęp do wartości *color* każdego z buttonów można uzyskać w następujący sposób:
```javascript
document.querySelectorAll('button').forEach(function(button) {
    let color = button.dataset.color;
});
```
### fetch
Pozwala na wykonanie zapytania pod wskazanym adresem URL.
```javascript
 fetch('https://api.exchangeratesapi.io/latest?base=USD')
 .then(response => response.json())
 .then(data => {
     console.log(data);
 });
```
## Local storage
Dane składowane w oknie przeglądarki. Wykorzystuje dwie podstawowe funkcje:
-   `localStorage.getItem(key)`
-   `localStorage.setItem(key, value)`

## Use case'y
### Skrypt wykonany przy załadowaniu strony
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Some code here
});
```

### Operacje na stylu elementu
```javascript
// Zmiana koloru tła elementu o tagu "body" na czerwony
let body = document.querySelector('body');
body.style.backgroundColor = 'red';
```
