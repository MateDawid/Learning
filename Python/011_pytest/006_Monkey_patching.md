# Monkey patching
Monkey patching "nadpisuje" elementy programu np. funkcje innymi mechanizmami. Poniżej przyklad zastąpienia funkcji input.

```python
from pay.order import LineItem, Order  
from pay.payment import pay_order  
from pytest import MonkeyPatch  
  

# klasa MonkeyPatch musi być przekazana jako argument funkcji
def test_pay_order(monkeypatch: MonkeyPatch) -> None:
	# Przygotowanie inputów  
    inputs = ["1249190007575069", "12", "2024"]  
    # Zastąpienie domyślnego wywołania funkcji input przez zwrócenie pierwszego elementu listy inputs
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))  
    order = Order()  
    order.line_items.append(LineItem("Test", 100))  
    pay_order(order)
```
Do monkey patchingu można wykorzystać też funkcjonalność fixture'ów. Poniżej przykład zablokowania możliwości wykorzystania metody request. Parametr autouse wskazuje, że fixture ten będzie wykonany przed każdym testem.
```python
@pytest.fixture(autouse=True)  
def no_requests(monkeypatch):  
    monkeypatch.delattr('requests.sessions.Session.request')
```