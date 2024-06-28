# Service - testing

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#testing-1

Since services hold our business logic, they are an ideal candidate for tests.

If you decide to cover the service layer with tests, we have few general rules of thumb to follow:

* The tests should cover the business logic in an exhaustive manner.
* The tests should hit the database - creating & reading from it.
* The tests should mock async task calls & everything that goes outside the project.

When creating the required state for a given test, one can use a combination of:

* Fakes (We recommend using faker)
* Other services, to create the required objects.
* Special test utility & helper methods.
* Factories (We recommend using factory_boy)
* Plain Model.objects.create() calls, if factories are not yet introduced in the project.
* Usually, whatever suits you better.

Let's take a look at our service from the example:
```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from project.payments.selectors import items_get_for_user
from project.payments.models import Item, Payment
from project.payments.tasks import payment_charge


@transaction.atomic
def item_buy(
    *,
    item: Item,
    user: User,
) -> Payment:
    if item in items_get_for_user(user=user):
        raise ValidationError(f'Item {item} already in {user} items.')

    payment = Payment(
        item=item,
        user=user,
        successful=False
    )
    payment.full_clean()
    payment.save()

    # Run the task once the transaction has commited,
    # guaranteeing the object has been created.
    transaction.on_commit(
        lambda: payment_charge.delay(payment_id=payment.id)
    )

    return payment
```
The service:

* Calls a selector for validation.
* Creates an object.
* Delays a task.

Those are our tests:
```python
from unittest.mock import patch, Mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.services import item_buy
from django_styleguide.payments.models import Payment, Item


class ItemBuyTests(TestCase):
    @patch('project.payments.services.items_get_for_user')
    def test_buying_item_that_is_already_bought_fails(
        self, items_get_for_user_mock: Mock
    ):
        """
        Since we already have tests for `items_get_for_user`,
        we can safely mock it here and give it a proper return value.
        """
        user = User(username='Test User')
        item = Item(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        items_get_for_user_mock.return_value = [item]

        with self.assertRaises(ValidationError):
            item_buy(user=user, item=item)

    @patch('project.payments.services.payment_charge.delay')
    def test_buying_item_creates_a_payment_and_calls_charge_task(
        self,
        payment_charge_mock: Mock
    ):
        # How we prepare our tests is a topic for a different discussion
        user = given_a_user(username="Test user")
        item = given_a_item(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        self.assertEqual(0, Payment.objects.count())

        payment = item_buy(user=user, item=item)

        self.assertEqual(1, Payment.objects.count())
        self.assertEqual(payment, Payment.objects.first())

        self.assertFalse(payment.successful)

        payment_charge_mock.assert_called_once()
```