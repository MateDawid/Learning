# Wyświetlanie zmiennych
Aby zagnieździć wartość zmiennej w składniku komponentu umieszcza się taką zmienną w nawiasach klamrowych.
```js
const user = {  
  name: 'Hedy Lamarr',  
  imageUrl: 'https://i.imgur.com/yXOvdOSs.jpg',  
  imageSize: 90,  
};  
  
function App() {  
return (  
	<>  
		<h1>{user.name}</h1>  
		<img   
			className="avatar"   
			src={user.imageUrl}   
			alt={'Photo of ' + user.name}   
			style={{  
				width: user.imageSize,  
				height: user.imageSize  
			}}  
		/>  
	</>  
);  
}
```