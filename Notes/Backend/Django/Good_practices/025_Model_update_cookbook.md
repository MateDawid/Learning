# Model update cookbook

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#cookbook

As for updating, we have a generic update service that we use inside of the actual update services. Here's what a sample user_update service would look like:
```python
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ['first_name', 'last_name']

    user, has_updated = model_update(
        instance=user,
        fields=non_side_effect_fields,
        data=data
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
```
* We're calling the generic model_update service for the fields that have no side-effects related to them (meaning that they're just set to the value that we provide).
* This pattern allows us to extract the repetitive field setting in a generic service and perform only the specific tasks inside of the update service (side-effects).
* We can be smart & provide the update_fields kwarg, when saving the instance. This way, in the UPDATE query, we'll only send values that are actually updated.

The full implementations of these services can be found in our example project:
* [model_update](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/services.py)
* [user_update](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/users/services.py)

If you are going to include model_update in your project, make sure to read the [tests](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/tests/services/test_model_update.py) & include them too!

