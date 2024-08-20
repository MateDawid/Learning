# useState
Aby wykorzystać stan aplikacji i dynamiczne wyświetlanie jego zmian konieczne jest zaimportowanie hooka useState z biblioteki Reacta poprzez umieszczenie w pliku następującego polecenia:

```js
import {useState} from 'Notes/Frontend/React/React';
```
Utworzenie zmiennej odzwierciedlającej stan w aplikacji odbywa się poprzez następującą definicję:
```js
const [variable, setVariable] = useState(0);
```
Zmienna **variable** to zmienna zawierająca bieżący stan aplikacji (w przykładzie powyżej zdefiniowana z wartością 0), natomiast **setVariable** to funkcja pozwalająca na zmianę stanu zawartego w zmiennej **variable**. Przykładowo, chcąc zmienić wartość **variable** z 0 na 1 napiszemy:
```js
setVariable(1);
```
## Stan pojedynczego komponentu
Stan może być zapamiętany w kontekście pojedynczego komponentu. W tym celu zmienna stanu oraz odpowiadająca jej funkcja aktualizująca muszą zostać zadeklarowane wewnątrz definicji komponentu. Poniżej przykład wyświetlenia dwóch buttonów z osobnymi licznikami kliknięć.

```js
import {useState} from 'Notes/Frontend/React/React';

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
            <MyButton/>
            <MyButton/>
        </div>
    );
}
```
## Wspólny stan dla wielu komponentów
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
