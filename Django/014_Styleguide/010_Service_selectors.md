# Service - selectors

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#selectors

In most of our projects, we distinguish between "Pushing data to the database" and "Pulling data from the database":

* Services take care of the push.
* Selectors take care of the pull.
* Selectors can be viewed as a "sub-layer" to services, that's specialized in fetching data.

A selector follows the same rules as a service.

For example, in a module <your_app>/selectors.py, we can have the following:
```python
def user_list(*, fetched_by: User) -> Iterable[User]:
    user_ids = user_get_visible_for(user=fetched_by)

    query = Q(id__in=user_ids)

    return User.objects.filter(query)
```
As you can see, user_get_visible_for is another selector.

You can return querysets, or lists or whatever makes sense to your specific case.

