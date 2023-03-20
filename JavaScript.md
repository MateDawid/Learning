# **JavaScript**
## SKŁADNIA
### Funkcje
Funkcje można zdefiniować na kilka sposobów:
* Funkcja nazwana
```javascript
function test(a, b){
	return a + b;
}
```
* Funkcja anonimowa

Funkcję można również zdefiniować "w locie" - będzie ona wtedy wykorzystywana jedynie w miejscu jej zdefiniowania. Poniżej przykład użycia anonimowej funkcji w definicji eventListenera.
```javascript
let form = document.querySelector('form')
form.addEventListener('submit', function(e) {
		console.log('Submitted');
});
```
### querySelector
Pozwala na wyszukiwanie elementów DOM na bazie podanego query
```javascript
// Wyszukiwanie w całym dokumencie pierwszego elementu z id "name"
let name = document.querySelector('#name');
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
### Operacje na stylu elementu
```javascript
// Zmiana koloru tła elementu o tagu "body" na czerwony
let body = document.querySelector('body');
body.style.backgroundColor = 'red';
```
