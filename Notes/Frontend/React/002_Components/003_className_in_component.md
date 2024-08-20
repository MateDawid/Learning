# Nadawanie klas w komponentach
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