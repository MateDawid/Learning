# dataset
Specjalny rodzaj atrybutów dla elementów DOM.
```html
...
<body>
    <button data-color="red">Red</button>
    <button data-color="blue">Blue</button>
    <button data-color="green">Green</button>
</body>
...
```
Dostęp do wartości *color* każdego z buttonów można uzyskać w następujący sposób:
```javascript
document.querySelectorAll('button').forEach(function(button) {
    let color = button.dataset.color;
});
```