# Advanced serialization

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#advanced-serialization

Sometimes, the end result of an API can be quite complex. Sometimes, we want to optimize the queries that we do and the optimization itself can be quite complex.

Trying to stick with just an OutputSerializer in that case might limit our options.

In those cases, we can implement our output serialization as a function, and have the optimizations we need there, instead of having all the optimizations in the selector.

Lets take this API as an example:
```python
class SomeGenericFeedApi(BaseApi):
    def get(self, request):
        feed = some_feed_get(
            user=request.user,
        )

        data = some_feed_serialize(feed)

        return Response(data)
```
In this scenario, some_feed_get has the responsibility of returning a list of feed items (can be ORM objects, can be just IDs, can be whatever works for you).

And we want to push the complexity of serializing this feed, in an optimal manner, to the serializer function - some_feed_serialize.

This means we don't have to do any unnecessary prefetches & optimizations in some_feed_get.

Here's an example of some_feed_serialize:
```python
class FeedItemSerializer(serializers.Serializer):
    ... some fields here ...
    calculated_field = serializers.IntegerField(source="_calculated_field")


def some_feed_serialize(feed: List[FeedItem]):
    feed_ids = [feed_item.id for feed_item in feed]

    # Refetch items with more optimizations
    # Based on the relations that are going in
    objects = FeedItem.objects.select_related(
      # ... as complex as you want ...
    ).prefetch_related(
      # ... as complex as you want ...
    ).filter(
      id__in=feed_ids
    ).order_by(
      "-some_timestamp"
    )

    some_cache = get_some_cache(feed_ids)

    result = []

    for feed_item in objects:
        # An example, adding additional fields for the serializer
        # That are based on values outside of our current object
        # This may be some optimization to save queries
        feed_item._calculated_field = some_cache.get(feed_item.id)

        result.append(FeedItemSerializer(feed_item).data)

    return result
```
As you can see, this is a pretty generic example, but the idea is simple:

* Refetch your data, with the needed joins & prefetches.
* Fetch or build in-memory caches, that will save you queries for specific computed values.
* Return a result, that's ready to be an API response.

Even though this is labeled as "advanced serialization", the pattern is really powerful and can be used for all serializations.

Such serializer functions usually live in a serializers.py module, in the corresponding Django app.