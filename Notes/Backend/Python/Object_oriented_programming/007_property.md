# @property
Dekorator @property, pozwala na utworzenie właściwości obiektu, do której dostęp można uzyskać przy użyciu kropki, tak samo jak do atrybutów definiowanych w konstruktorze. Właściwości obiektu są jednak możliwe do nadpisania tylko po zdefiniowaniu settera.
```python
class Person:
	def __init__(self, name, married=False):
		self._name = name
		self.married = married
	
	@property
	def name(self):
		return self._name
	
	@property
	def married(self):
		return self._married
	
	@married.setter
	def married(self, value):
		if not(isinstance(value, bool)):
			raise TypeError('married must be bool')
		self._married = value
	
	@married.deleter
	def married(self):
		del self._married
```