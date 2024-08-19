# Throttling

Source: https://testdriven.io/courses/django-rest-framework/user-management/#H-4-throttling

As with permissions, throttling is used to determine if the request should be authorized. The difference is that throttling is a temporary state while user permissions are more or less permanent. In essence, throttling controls the rate of requests that clients can make to an API. When the throttling rate is exceeded, DRF returns a 429 Too Many Requests status.

Throttling can help improve the user experience and protect against slow performance or DoS (denial-of-service) attacks.

DRF provides two types of throttle classes:
1. `UserRateThrottle` - used to throttle authenticated users
2. `AnonRateThrottle` - used to throttle unauthenticated users

You can also create your own throttle class.

## Default

As with the other default DRF settings, you can configure the default settings in the REST_FRAMEWORK dict in the settings.py file.

For the throttling to work, you need to add two settings:

1. `DEFAULT_THROTTLE_CLASSES` - determines how the throttle works (e.g., authenticated/unauthenticated users, scope)
2. `DEFAULT_THROTTLE_RATES` - determines how many requests are allowed (e.g., n/hour, n/second).

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/hour",
        "user": "2/hour"
    },
}
```

## Custom

Let's create a throttle limitation per day and minute separately. That way, you avoid slow performance of your API and at the same time ensure the client has enough requests available throughout the day.

We need to create multiple UserRateThrottles to achieve that, one for a daily rate and one for a rate per minute.

```python
# shopping_list/api/throttling.py


from rest_framework.throttling import UserRateThrottle


class MinuteRateThrottle(UserRateThrottle):
    scope = "user_minute"


class DailyRateThrottle(UserRateThrottle):
    scope = "user_day"
```

Here, we simply set a unique scope, so we can then set the rate numbers in settings.

Back in core/settings.py, update `DEFAULT_THROTTLE_CLASSES` and `DEFAULT_THROTTLE_RATES` like so:

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "shopping_list.api.throttling.MinuteRateThrottle",
        "shopping_list.api.throttling.DailyRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/hour",
        "user_day": "10000/day",
        "user_minute": "200/minute",
    },
}
```