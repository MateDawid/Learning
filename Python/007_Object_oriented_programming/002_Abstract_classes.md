# Klasy abstrakcyjne
Użycie klas abstrakcyjnych pozwala na wymuszenie zaimplementowania wszystkich abstrakcyjnych metod w klasach pochodnych od abstrakcyjnej klasy bazowej.

```python
import abc
import json

class Plugin(metaclass=abc.ABCMeta):
	"""Abstract base for plugins."""
	
	@abc.abstractmethod
	def load(self, path):
		"""Return a dict with values from the given file."""
	
	@abc.abstractmethod
	def save(self, data, path):
		"""Serialize data and save it to the given file."""


class JsonPlugin(Plugin):

	def load(self, path):
		with open(path) as fp:
			return json.load(fp)
	
	def save(self, data, path):
		with open(path, 'w') as fp:
			json.dump(data, fp, indent=4, sort_keys=True)
```