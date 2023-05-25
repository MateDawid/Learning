# **JavaScript**
## 1.  Zmienne
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
## 2.  Formatowanie stringów
```javascript
let number = 1
let formattedString = `Number: ${number}`
```
## 3. Ternary Operator
Skrócony zapis bloku if - else. Przy jego użyciu taki zapis:
```js
if (a < b)  {        
    let output = a + b;    
} else if (a > b) {
    let output = a - b;    
} else {        
    let output = a * b;    
}
```
Można zastąpić takim zapisem:
```js
(a < b) ? a + b : a - b;
```
## 4.  JavaScript Object
Struktura podobna do słowników w Pythonie. Przykład użycia:
```javascript
let person = {
    first: 'Harry',
    last: 'Potter'
};
```
![Harry Potter](https://cs50.harvard.edu/web/2020/notes/5/images/console.png)
## 5. Funkcje
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
## 6. querySelector
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca pierwszy element pasujący do zapytania.
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let name = document.querySelector('#name');
```
## 7. querySelectorAll
Pozwala na wyszukiwanie elementów DOM na bazie podanego query. Zwraca listę obiektów pasujących do zapytania,
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let buttons = document.querySelectorAll('button');
```

## 8. addEventListener
Pozwala na zdefiniowanie zachowania strony w momencie, gdy user wykona jakieś działanie, np. kliknie w odpowiedni element.
```javascript
// Kliknięcie elementu o id "name" powoduje zalogowanie do consoli słowa "CLICKED"
document.querySelector('#name').addEventListener('click', function()
	{
	    console.log('CLICKED');
	}
);
```
## 9. dataset
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
## 10. fetch
Pozwala na wykonanie zapytania pod wskazanym adresem URL.
```javascript
 fetch('https://api.exchangeratesapi.io/latest?base=USD')
 .then(response => response.json())
 .then(data => {
     console.log(data);
 });
```
## 11. Local storage
Dane składowane w oknie przeglądarki. Wykorzystuje dwie podstawowe funkcje:
-   `localStorage.getItem(key)`
-   `localStorage.setItem(key, value)`

## 12. map
```js
let fruits = ["pawpaw", "orange", "banana"];   

let mappedFruits = fruits.map(item => item + "s");    

console.log(mappedFruits); // ["pawpaws", "oranges", "bananas"]
```
## 13. filter
```js
let fruits = ["pawpaw", "orange", "banana", "grape"];
    
let filteredFruits = fruits.filter(fruit => fruit.length > 5);

console.log(filteredFruits);  // ["pawpaw", "orange", "banana"]
```
## 14. reduce
```js
let evenNumbers = [2, 4, 6, 8, 10]; 
    
evenNumbers.reduce((sum, current) => sum += current, 0);
```
## 15. Przykładowe problemy
### 15.1. Skrypt wykonany przy załadowaniu strony
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Some code here
});
```

### 15.2. Operacje na stylu elementu
```javascript
// Zmiana koloru tła elementu o tagu "body" na czerwony
let body = document.querySelector('body');
body.style.backgroundColor = 'red';
```
