# Testowanie wyjątków
Jeżeli dany test ma sprawdzić wystąpienie wyjątku, należy użyć konstrukcji **with pytest.raises([nazwa_wyjątku])**.
```python
from pay.processor import PaymentProcessor  
import pytest  
  
API_KEY = "6cfb67f3-6281-4031-b893-ea85db0dce20"  

def test_api_key_invalid() -> None:  
    with pytest.raises(ValueError):  
        processor = PaymentProcessor("")  
        processor.charge("1249190007575069", 12, 2024, 100)
```