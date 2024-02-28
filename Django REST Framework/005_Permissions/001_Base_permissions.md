## 5. Permissions
```python
#permissions.py
from rest_framework import permissions  
  
  
class UpdateOwnProfile(permissions.BasePermission):  
	"""Allow user to edit their own profile"""  
	  
	def has_object_permission(self, request, view, obj):  
		"""Check user is trying to edit their own profile"""  
		if request.method in permissions.SAFE_METHODS:  
			return True  
		return obj.id == request.user.id
```
```python
# views.py
class UserProfileViewSet(viewsets.ModelViewSet):  
	"""Handle creating and updating profiles"""  
	...
	permission_classes = (permissions.UpdateOwnProfile,)  
```