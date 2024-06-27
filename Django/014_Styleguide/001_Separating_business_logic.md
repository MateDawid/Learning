# Separating business logic

Sources: 
* https://emcarrio.medium.com/business-logic-in-a-django-project-a25abc64718c
* https://github.com/HackSoftware/Django-Styleguide

## Shortly

In Django, business logic should live in:

* Services - functions, that mostly take care of writing things to the database.
* Selectors - functions, that mostly take care of fetching things from the database.
* Model properties (with some exceptions).
* Model clean method for additional validations (with some exceptions).

In Django, business logic should not live in:

* APIs and Views.
* Serializers and Forms.
* Form tags.
* Model save method.
* Custom managers or querysets.
* Signals.

Model properties vs selectors:

* If the property spans multiple relations, it should better be a selector.
* If the property is non-trivial & can easily cause N + 1 queries problem, when serialized, it should better be a selector.

The general idea is to "separate concerns" so those concerns can be maintainable / testable.

## In detail

>As a rule-of-thumb, your application logic should live in modules that aren’t Django-specific modules (eg not in views.py, models.py or forms.py). If I had my way, Django would create an empty business_logic.py in each new app to encourage this.

Just be careful of not taking too much away from your models or you will be left with anemic domain models. Only business logic is meant to leave, the domain logic like validations, calculations, etc are already at home.

The answer is treating it like a data repository. A really not used pattern to a big part of the Django developers I used to know (highly influenced by using the Django ORM everywhere).

In reality, this solution is the recommended way of doing things, although it is not advertised as a data repository at all. In every Django tutorial, you are suggested to write your queries inside custom managers to avoid repetition and writing the same query every time. But you are gaining a lot more than that, implementing the queries there decouples the ORM implementation from its use in the application, a win-win situation.

Following this principle, you can then use your Model.objects as it was your data repository in the business logic, reducing the coupling to the ORM and allowing you to do integration tests for the database interactions only. In the next example, we’ll see how to use it.

## Example

The example is very simple: we have an Address model that has an is_default field that indicates if that address is the default one of its user.

And then we have an action that makes an address instance the default one, setting its is_default to True and setting it to False to the other user’s addresses. After setting the default address, we publish the changes to anyone interested.

Here first we have the example done using fat models (high coupling and low cohesion):

```python
# models.py
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    is_default = models.BooleanField()

    @property
    def full_address(self):
        return f'{self.street}, {self.number}'

    # Business logic inside the model
    def set_default(self):
        # Dependencies with other models (in this case the same one)
        Address.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True
        self.save()

        # Side-effects of the action inside the model, SRP ko
        events.publish(events.DEFAULT_ADDRESS_CHANGED, address=self)


# tests.py
class TestSetDefault:

    @pytest.fixture
    def address(self, user):
        return Address(user=user, street='Fake', number=1, is_default=False)

    def test_sets_address_as_default_and_publishes_changes(self, mocker, address):
        mock_filter = mocker.patch.object(Address.objects, 'filter')
        mock_update = mocker.patch.object(mock_filter.return_value, 'update')
        mock_save = mocker.patch.object(address, 'save')
        mock_publish = mocker.patch.object(events, 'publish')

        address.set_default()

        # We lose the integration tests of the database flows
        mock_filter.assert_called_with(user=address.user)
        mock_update.assert_called_with(is_default=False)
        assert address.is_default == True
        mock_save.assert_called()
        mock_publish.assert_called_with(events.DEFAULT_ADDRESS_CHANGED, address=address)
```

Some important things to notice are:

* The model indeed contains the business action set_default.
* It has dependencies with other models (in this case itself).
* There are side-effects in the action inside the model, breaking the SRP.
* To achieve unit tests for our business logic we need to mock up all the dependencies. 

In the last point, we have something important to discuss. You can follow 2 approaches: do an integration test where you validate the business flow with all its dependencies or do a unit test mocking all the external calls.

The problem with the integration test is that you have to test the behaviour using a real database as all the dependencies will end using the ORM, slowing down your tests and not validating the logic flow independently of the dependencies. The problem with the unit test is that you lose the integration validation of database behaviours and you have to mock everything.

So let’s look to the same example but applying a business logic layer and abstracting the database interactions to a manager (low coupling and high cohesion):

```python
# managers.py
class AddressManager(models.Manager):

    # We use the manager as a data repository
    def set_default(self, address):
        self.filter(user=address.user).update(is_default=False)
        address.is_default = True
        address.save()


# models.py
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    is_default = models.BooleanField()

    @property
    def full_address(self):
        return f'{self.street}, {self.number}'

    objects = AddressManager()


# business_logic.py
# The business rule is simple and easily testeable
def set_default(address):
    Address.objects.set_default(address)
    events.publish(events.DEFAULT_ADDRESS_CHANGED, address=address)


# tests.py
@pytest.mark.django_db
class TestAddressManagerSetDefault:

    # We make integration tests for the manager to validate database behaviours
    def test_sets_address_as_default(self, saved_user):
        old_default_address = Address.objects.create(
            user=saved_user, street='Fake', number=1, is_default=True)
        address = Address.objects.create(
            user=saved_user, street='Fake', number=2, is_default=False)

        Address.objects.set_default(address)

        old_default_address.refresh_from_db()
        address.refresh_from_db()
        assert not old_default_address.is_default
        assert address.is_default


class TestSetDefault:

    @pytest.fixture
    def address(self, user):
        return Address(user=user, street='Fake', number=1, is_default=False)

    def test_sets_address_as_default_and_publishes_changes(self, mocker, address):
        # In this case a lot less dependencies
        mock_set_default = mocker.patch.object(Address.objects, 'set_default')
        mock_publish = mocker.patch.object(events, 'publish')

        set_default(address)

        # We test only the logic and forget about ORM interactions
        mock_set_default.assert_called_with(address)
        mock_publish.assert_called_with(events.DEFAULT_ADDRESS_CHANGED, address=address)
```

As you can see we have easier tests and more maintainable code. In this case, we implement unit tests for our business logic that are fast and validate its flow. And then integration tests for the manager that validate the data operations and its dependencies with the database.

The key in this structure is that our business logic is not aware of data integrity or how it is stored, that is the job of the managers. This way we can unit test every flow and leave the integrity checks for the integration tests of the data layer.