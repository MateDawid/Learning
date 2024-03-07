# Ternary Operator
Skrócony zapis bloku if - else. Przy jego użyciu taki zapis:
```js
if (a < b)  {        
    let output = a + b;    
} else if (a > b) {
    let output = a - b;    
} else {        
    let output = a * b;    
}
```
Można zastąpić takim zapisem:
```js
(a < b) ? a + b : a - b;
```