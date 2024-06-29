# Listing all url patterns in project

```python
from django.urls import get_resolver

patterns = get_resolver().url_patterns
```
Example output:
![img.png](img.png)