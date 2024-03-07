# Funkcje
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