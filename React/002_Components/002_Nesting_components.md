# Zagnieżdżanie komponentów
Tak zadeklarowany komponent można zagnieździć w innym komponencie:
```js
export default function MyApp() {  
	return (  
		<div>  
			<h1>Welcome to my app</h1>  
			<MyButton />  
		</div>  
	);  
}
```