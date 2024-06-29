# Combining and Excluding Permission Classes

Source: https://testdriven.io/blog/custom-permission-classes-drf/#combining-and-excluding-permission-classes

## AND operator

AND is the default behavior of permission classes, achieved by using ,:
```python
permission_classes = [IsAuthenticated, IsStaff, SomeCustomPermissionClass]
```

It can also be written with &:
```python
permission_classes = [IsAuthenticated & IsStaff & SomeCustomPermissionClass]
```

## OR operator

With the OR (|), when any of the permission classes return True, the permission is granted. You can use the OR operator to offer multiple possibilities in which the user gets granted permission.
```python
permission_classes = [IsStaff | IsOwner]
```

## NOT operator

The NOT operator results in the exact opposite to the defined permission class. In other words, permission is granted to all users except the ones from the permission class.

```python
permission_classes = [~IsFinancesMember] 
```

Be careful! If you only use the NOT operator, everybody else will be allowed access, including unauthenticated users! If that's not what you meant to do, you can fix that by adding another class like so:
```python
permission_classes = [~IsFinancesMember & IsAuthenticated]
```

## Parentheses

Inside permission_classes you can also use parentheses (()) to control which expression gets resolved first.
```python
permission_classes = [(IsFinancesMember | IsTechMember) & IsOwner]
```
In this example, (IsFinancesMember | IsTechMember) will be resolved first. Then, the result of that will be used with & IsOwner.