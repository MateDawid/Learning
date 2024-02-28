# Tworzenie unit testów
Testy tworzone są jako metody dla klasy dziedziczącej po APITestCase. Przykładowy unit test:
```python
from .models import Contact  
from rest_framework.test import APIClient  
from rest_framework.test import APITestCase  
from rest_framework import status  
  
  
class ContactTestCase(APITestCase):  
	...    
	def test_create_contact(self):  
		'''  
		test ContactViewSet create method 
		'''  
		data = self.data  
		response = self.client.post(self.url, data)  
		self.assertEqual(response.status_code, status.HTTP_200_OK)  
		self.assertEqual(Contact.objects.count(), 1)  
		self.assertEqual(Contact.objects.get().title, "Billy Smith")
```