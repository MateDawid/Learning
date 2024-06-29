# Tworzenie komponentów
Podstawowy element wykorzystywany w React'cie. Komponent to javascriptowa funkcja, która zwraca znaczniki HTML. Nie ma ograniczenia co do wielkości komponentu - może zwracać np. button (jak w przykładzie poniżej) lub nawet całą stronę.
```js
function MyButton() {  
	return (  
		<button>I'm a button</button>  
	);  
}
```
**WAŻNE:** Reactowe komponenty zawsze zaczynają się z dużej litery - pozwala to odróżnić je od zwykłych znaczników HTML.