# addEventListener
Pozwala na zdefiniowanie zachowania strony w momencie, gdy user wykona jakieś działanie, np. kliknie w odpowiedni element.
```javascript
// Kliknięcie elementu o id "name" powoduje zalogowanie do consoli słowa "CLICKED"
document.querySelector('#name').addEventListener('click', function()
	{
	    console.log('CLICKED');
	}
);
```

Przykład użycia:

```javascript
// Skrypt wykonany przy załadowaniu strony
document.addEventListener('DOMContentLoaded', function() {
    // Some code here
});
```

