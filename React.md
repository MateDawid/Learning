# **React**
## 1.  Przygotowanie projektu
Żeby uruchomić aplikację reactową we własnym środowisku konieczne jest zainstalowanie [Node.js](https://nodejs.org/en).
Po jego instalacji w konsoli możliwe jest użycie polecenia, które zbuduje podstawowy schemat aplikacji.
```commandline
npx create-react-app <nazwa-aplikacji>
```
Gdy aplikcja jest już gotowa, możliwe jest jej uruchomienie na lokalnym serwerze:
```
  npm start
```
Tak przygotowany projekt pozwala na utworzenie single page app poprzez edycję pliku **nazwa-aplikacji/src/App.js**, którego zawartość jest eksportowana do **nazwa-aplikacji/src/index.js**, który to jest wykorzystwany w **nazwa-aplikacji/public/index.html**.
## 2. Komponenty
### 2.1. Tworzenie komponentów
Podstawowy element wykorzystywany w React'cie. Komponent to javascriptowa funkcja, która zwraca znaczniki HTML. Nie ma ograniczenia co do wielkości komponentu - może zwracać np. button (jak w przykładzie poniżej) lub nawet całą stronę.
```js
function MyButton() {  
	return (  
		<button>I'm a button</button>  
	);  
}
```
**WAŻNE:** Reactowe komponenty zawsze zaczynają się z dużej litery - pozwala to odróżnić je od zwykłych znaczników HTML.
### 2.2. Zagnieżdżanie komponentów
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
### 2.3. Nadawanie klas w komponentach
Aby zdefiniować klasę dla elementu w komponencie konieczne jest użycie **className** zamiast **class**.
```html
<img  className="avatar"  />
```
W kontekście nadawania stylów działanie **className** jest takie samo jak **class**
```css
/* In your CSS */  

.avatar {  
	border-radius: 50%;  
}
```
### 2.4. Wyświetlanie zmiennych
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
## 3. Renderowanie list elementów
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
## 4. Renderowanie warunkowe
Elementy mogą być wyświetlane lub nie w zależności od sprawdzanych warunków. Poza tradycyjną konstrukcją if / else możliwe jest użycie typowych dla JavaScriptu skrótów:
* `{cond ? <A /> : <B />}`  => jeżeli `cond`, wyświetl `<A />`, w innym wypadku wyświetl `<B />`
* `{cond && <A />}`  => jeżeli `cond`, wyświetl `<A />`, w innym wypadku nie wyświetlaj niczego
## 5. Hooks
### 5.1. useState
Aby wykorzystać stan aplikacji i dynamiczne wyświetlanie jego zmian konieczne jest zaimportowanie hooka useState z biblioteki Reacta poprzez umieszczenie w pliku następującego polecenia:
```js
import { useState } from 'react';
```
Utworzenie zmiennej odzwierciedlającej stan w aplikacji odbywa się poprzez następującą definicję:
```js
const [variable, setVariable] = useState(0);
```
Zmienna **variable** to zmienna zawierająca bieżący stan aplikacji (w przykładzie powyżej zdefiniowana z wartością 0), natomiast **setVariable** to funkcja pozwalająca na zmianę stanu zawartego w zmiennej **variable**. Przykładowo, chcąc zmienić wartość **variable** z 0 na 1 napiszemy:
```js
setVariable(1);
```
#### 5.1.1. Stan pojedynczego komponentu
Stan może być zapamiętany w kontekście pojedynczego komponentu. W tym celu zmienna stanu oraz odpowiadająca jej funkcja aktualizująca muszą zostać zadeklarowane wewnątrz definicji komponentu. Poniżej przykład wyświetlenia dwóch buttonów z osobnymi licznikami kliknięć.
```js
import { useState } from 'react';  
  
function MyButton() {  
  const [count, setCount] = useState(0);  
  
  function handleClick() {  
    setCount(count + 1);  
  }  
  
  return (  
    <button onClick={handleClick}>  
      Clicked {count} times  
    </button>  
  );  
}  
  
function App() {  
  return (  
    <div>  
      <h1>Counters that update separately</h1>  
      <MyButton />  
      <MyButton />  
    </div>  
  );  
}
```
#### 5.1.2. Wspólny stan dla wielu komponentów
W celu współdzielenia stanu przez wiele komponentów konieczne jest umieszczenie definicji zmiennej zawierającej stan w komponencie zawierającym komponenty, które mają z tego wspólnego stanu korzystać. 
Chcąc, aby w przykładzie z punktu 4.1.1. oba buttony aktualizowały jeden, wspólny licznik konieczny będzie następujący refactoring:
```js
function MyButton({ count, onClick }) {  
  return (  
    <button onClick={onClick}>  
      Clicked {count} times  
    </button>  
  );  
}  
  
function App() {  
  const [count, setCount] = useState(0);  
  
  function handleClick() {  
    setCount(count + 1);  
  }  
  
  return (  
    <div>  
      <h1>Counters that update together</h1>  
      <MyButton count={count} onClick={handleClick} />  
      <MyButton count={count} onClick={handleClick} />  
    </div>  
  );
``` 
Definicja stanu została przeniesiona z komponentu MyButton do komponentu App, gdzie sama zmienna **count** i eventHandler **handleClick** są przekazywane do komponentów MyButton jako tzw. props.
