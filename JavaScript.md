# **JavaScript**
## SKŁADNIA
### Funkcje
Funkcje można zdefiniować na kilka sposobów
```javascript
function test(a, b)
    {
        return a + b;
    }
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
let body= document.querySelector('body');
body.style.backgroundColor = 'red';
```
