# map
```js
let fruits = ["pawpaw", "orange", "banana"];   

let mappedFruits = fruits.map(item => item + "s");    

console.log(mappedFruits); // ["pawpaws", "oranges", "bananas"]
```
# filter
```js
let fruits = ["pawpaw", "orange", "banana", "grape"];
    
let filteredFruits = fruits.filter(fruit => fruit.length > 5);

console.log(filteredFruits);  // ["pawpaw", "orange", "banana"]
```
# reduce
```js
let evenNumbers = [2, 4, 6, 8, 10]; 
    
evenNumbers.reduce((sum, current) => sum += current, 0);
```