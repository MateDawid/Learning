# Eager loading

Source: https://rex-chiang.medium.com/django-rest-framework-eager-loading-a67e6be15b3

## Implementation example

```python
class EagerLoadingMixin:
  @classmethod
  def setup_eager_loading(cls, queryset):
    if hasattr(cls, "SELECT"):
      queryset = queryset.select_related(*cls.SELECT)

    if hasattr(cls, "PREFETCH"):
      queryset = queryset.prefetch_related(*cls.PREFETCH)

    return queryset
```

```python
class OrderSerializer(ModelSerializer, EagerLoadingMixin):
  account = AccountSerializer()
  product = productSerializer()
  coupon = couponSerializer()

  SELECT = ["account", "coupon"]
  PREFETCH = ["product"]
```

```python
orders = Order.objects.all()
queryset = OrderSerializer.setup_eager_loading(orders)
data = OrderSerializer(queryset, many=True).data
```