# Atomic transactions

Sources: 
* https://www.reddit.com/r/django/comments/ypw0mg/can_somebody_explain_when_to_use_transaction/
* https://plainenglish.io/blog/understanding-djangos-transaction-atomic

## transaction.atomic

Before diving into transaction atomic, let’s understand the concept of transactions. In a database context, a transaction represents a logical unit of work that either succeeds as a whole or fails completely, ensuring data consistency. A transaction typically consists of multiple database operations, such as inserts, updates, and deletions.

Atomic transactions are about ensuring data consistency in your database.

So say you had 2 models, and a view that populated a record in both
```python
Model1.objects.create(...)
Model2.objects.create(...)
```

Say Model1 finished saving, then your application crashed. If the fact that the Model2 record is missing will lead to inconsistent/wrong results in your db then you want to save both record in 1 transaction
```python
with transaction.atomic():
  Model1.objects.create(...)
  Model2.objects.create(...)
```

With this, you are guaranteed to have either both, or no records saved.

"Inconsistent" is up to you to define. Relational schemas can only model your data to a certain extent, at some point you need guarantees about the data in your columns. When that data is "off" is a good definition of inconsistent.

During the execution of a transaction, two critical concepts come into play: commit and rollback. A commit operation signifies that the transaction is successful, and all changes made within the transaction are permanently saved to the database. On the other hand, a rollback operation discards any changes made within the transaction and reverts the database to its state before the transaction begins.

## select_for_update

Django’s transaction atomic already provides a basic level of concurrency control by using the transaction.atomic block. However, it doesn't handle concurrent updates outside of the transaction scope.

To implement more advanced locking mechanisms, you can use the select_for_update() method in Django's querysets.

```python
from django.db import transaction, models

def transfer(self, request):
    try:
        user_a = request.POST.get("user_a")
        user_b = request.POST.get("user_b")
        amount = request.POST.get("amount")

        with transaction.atomic():
            user_a_obj = Account.objects.select_for_update().get(user=user_a)
            user_a_obj.balance -= int(amount)
            user_a_obj.save()

            user_b_obj = Account.objects.select_for_update().get(user=user_b)
            user_b_obj.balance += int(amount)
            user_b_obj.save()

            return Response(
                {"status": "success", "message": "Your amount is transfered."}
            )

    except Exception as e:
        print(e)
        return Response({"status": "failed", "message": "Something went wrong."})
```

The select_for_update() method is called on the querysets for user_one_obj and user_two_obj. This method locks the selected rows in the database, preventing other transactions from modifying them until the current transaction is completed.

## Bulk inserting

Here’s an example of how to perform a bulk insert using Django’s transaction atomic feature with the Product model:

```python
from django.db import transaction

# Assume you have a list of products to insert
products_data = [
    {'name': 'Product 1', 'sku': 'SKU1', 'price': 10.99},
    {'name': 'Product 2', 'sku': 'SKU2', 'price': 19.99},
    {'name': 'Product 3', 'sku': 'SKU3', 'price': 14.99},
    # Add more products as needed
]

@transaction.atomic
def create_products(products_data):
    # Create a list to hold the Product objects
    products = []

    try:
        # Iterate over the products_data list
        for data in products_data:
            product = Product(name=data['name'], sku=data['sku'], price=data['price'])
            products.append(product)

        # Use the bulk_create method to insert the products in a single query
        Product.objects.bulk_create(products)

        # Transaction will be committed automatically if no exceptions occur
    except Exception as e:
        # Handle any exceptions that occur during the bulk creation process
        print(f"Error occurred: {e}")
        # Raise an exception to trigger a rollback
```

Here, we decorate the function with the transaction.atomic decorator to ensure the entire bulk insert operation is treated as an atomic transaction.

After iterating over all the data, we use the bulk_create method of the Product.objects manager to insert all the Product objects in a single query, improving performance compared to individual save() calls.

If any exception occurs during the bulk creation process, we catch it and handle it accordingly. By raising an exception, the transaction will be rolled back, and no changes will persist in the database. If no exceptions occur, the transaction will be committed automatically, and all the products will be inserted into the database.