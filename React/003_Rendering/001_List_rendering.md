# Renderowanie list elementów
Aby wyświetlić listę elementów można przygotować przygotować taką listę elementów przy użyciu pętli for lub funkcji map(). Poniżej przykład zmapowania obiektów na reprezentujące je \<li>.
```js
const products = [  
  { title: 'Cabbage', isFruit: false, id: 1 },  
  { title: 'Garlic', isFruit: false, id: 2 },  
  { title: 'Apple', isFruit: true, id: 3 },  
];  
  
function App() {  
	const listItems = products.map(product =>  
		<li  
			key={product.id}  
			style={{  
				color: product.isFruit ? 'magenta' : 'darkgreen'  
			}}  
		>  
			{product.title}  
		</li>  
	);  

	return (  
		<ul>{listItems}</ul>  
	);  
}
```
**WAŻNE:** ważne zdefiniowanie atrybutu **key** w \<li> jako unikalnego identyfikatora dla elementu listy (np. id z bazy danych), ponieważ React wykorzystuje ten atrybut do operacji na wskazanym obiekcie.