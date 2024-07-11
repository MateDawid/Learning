# Factories

Source: https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories#fakes

## Creating Factories

```python
# models.py

from django.db import models
from django.utils import timezone

class VehiclePurchase(models.Model):
    price = models.DecimalField(max_digits=19, decimal_places=2)
    color = models.ForeignKey(
        VehicleColor, null=True, blank=True, on_delete=models.SET_NULL
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        BaseUser, null=True, blank=True, on_delete=models.SET_NULL
    )
    sales_member = models.ForeignKey(
        BaseUser, null=True, blank=True, on_delete=models.SET_NULL
    )
    requested_at = models.DateTimeField(db_index=True, default=timezone.now)
    cancelled_at = models.DateTimeField(null=True, blank=True)
```

```python
# factories.py

import factory

from my_project.utils.tests import faker

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.LazyAttribute(lambda _: faker.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())

class VehiclePurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehiclePurchase

    price = factory.LazyAttribute(lambda _: faker.pyfloat(positive=True))
    color = factory.SubFactory(ColorFactory)
    vehicle = factory.SubFactory(VehicleFactory)
    plan = factory.SubFactory(PlanFactory)
    customer = factory.SubFactory(UserFactory)
    sales_member = factory.SubFactory(UserFactory)
```

## DjangoModelFactory

DjangoModelFactory is a basic interface from factory_boy that gives "ORM powers" to your factories.

It's main feature here is that it provides you with a common "create" and "build" strategies that you can use to generate objects in your tests.

* SomeFactory.create() / SomeFactory() - saves the generated object to the database. The related sub factories are also created in the database.
* SomeFactory.build() - generates a model instance without saving it to the database. The related sub factories are also not stored in the database.

## Faker

As you may have noticed, we don't create a Faker instance in the factories file. We import it from another file in the application. This is intentional!

We highly recommend "proxying" the Faker instance and using it in your app that way.

You'd most likely want to have the same configuration when you use fakes around your app. Same goes if you want to customize the providers and use them in different places.
```python
# my_project/utils/tests/base.py

from faker import Faker

faker = Faker()
```

## LazyAttribute
It's an extremely simple but yet powerful abstraction that represents the symbiosis between the factories and the fakes.

It accepts a method which is invoked when a Factory instance is being generated. The return value of the method is used for the value of the desired attribute.

If you don't use it, you're actually setting a class attribute to your Factory. This means that this attribute will be generated when you define your Factory class, not when you instantiate it.
```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = faker.unique.email()
```
Defining your Factory this way will produce the following result:

```python
for _ in range(5):
    print(UserFactory.build().email)
 
erobinson@example.org
erobinson@example.org
erobinson@example.org
erobinson@example.org
erobinson@example.org
```
For most of the cases, you would want your objects to be generated with different values every time:
```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.unique.email())
```
This is the output when you use LazyAttribute:

```python
for _ in range(5):
    print(UserFactory.build().email)
    
woodtammy@example.net
justin56@example.com
rachel10@example.com
michaelthompson@example.com
mkennedy@example.com
```
