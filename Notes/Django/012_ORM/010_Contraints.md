# Constraints

Sources:
* https://adamj.eu/tech/2020/03/10/django-check-constraints-sum-percentage-fields/
* https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/
* https://adamj.eu/tech/2020/03/25/django-check-constraints-one-field-set/
* https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/

## Fields calculation constraint

```python
from django.db import models


class Book(models.Model):
    percent_read = models.PositiveIntegerField()
    percent_unread = models.PositiveIntegerField()
    percent_ignored = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} - {self.percent_read}% read"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    percent_read=(
                        100 - models.F("percent_unread") - models.F("percent_ignored")
                    )
                ),
                name="%(app_label)s_%(class)s_percentages_sum_100",
            )
        ]
```
## Choice field constraint

Django’s model validation is designed mostly for forms. It trusts that other code paths in your application “know what they’re doing.”

```python
from django.db import models


class Status(models.TextChoices):
    UNPUBLISHED = "UN", "Unpublished"
    PUBLISHED = "PB", "Published"


class Book(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.UNPUBLISHED,
    )

    def __str__(self):
        return f"{self.id} - {Status(self.status).label}"
```

For Book class above we can save item in database with status other than declared in choices:
```python
book = Book.objects.get(id=1)
book.status = 'republished'
book.save()
```
or
```python
Book.objects.update(status="republished")
```

To prevent that, use contraints:
```python
class Book(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.UNPUBLISHED,
    )

    def __str__(self):
        return f"{self.id} - {Status(self.status).label}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=Status.values),
            )
        ]
```

## One of fields filled constraint

To make sure that only one field has a value, when other one is Null use constraint as below.

```python
from django.db import models


class ScoreType(models.IntegerChoices):
    POINTS = 1, "Points"
    DURATION = 2, "Duration"


class Score(models.Model):
    type = models.IntegerField(choices=ScoreType.choices)
    value_points = models.IntegerField(null=True)
    value_duration = models.DurationField(null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_value_matches_type",
                check=(
                    models.Q(
                        type=ScoreType.POINTS,
                        value_points__isnull=False,
                        value_duration__isnull=True,
                    )
                    | models.Q(
                        type=ScoreType.DURATION,
                        value_points__isnull=True,
                        value_duration__isnull=False,
                    )
                ),
            )
        ]
```
You can also combine this with proxy models to split Scores based on type. 
```python
class PointsScoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=ScoreType.POINTS)


class PointsScore(Score):
    objects = PointsScoreManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ScoreType.POINTS

    class Meta:
        proxy = True
```

## Many-to-many field constraint

### Follow mechanism

Imagine we have a user model that we’d like to introduce a social media “following” pattern to. Users can follow other users to receive updates on our site. We’d like to ensure that users do not follow themselves, since that would need special care in all our code.

To add the followers relationship, we’ll be using ManyToManyField. By default, ManyToManyField creates a hidden model class to hold the relationships. Because we want to customize our model with add an extra constraint, we’ll need to use the through argument to define our own visible model class instead.

```python
from django.db import models


class User(models.Model):
    ...
    followers = models.ManyToManyField(
        to="self",
        through="Follow",
        related_name="following",
        symmetrical=False,
    )


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["from_user", "to_user"],
            ),
        ]
```
Note:

* We use to="self" to define that the relationship is from User to itself. Django calls this a recursive relationship.
* We use the string format of through, because we’re defining User before Follow. We could define Follow first, but then we’d need to use strings to specify User in its definition.
* We declare the relationship as asymmetrical with symmetrical=False. If Alice follows Bob, it does not mean Bob follows Alice. If our relationship was a mutual “friend request” style, we would instead make the relationship symmetrical.
* The Follow class uses two foreign keys to link up the related users. ManyToManyField will automatically use the first foreign key as the “source” of the relationship and the other as the destination. It’s possible Follow could have a third foreign key to User, for example to track another user who suggested the follow. In this case, we’d need to use ManyToManyField.through_fields to specify which foreign keys actually form the relationship.

* We have already added a constraint to the model - a UniqueConstraint to ensure that exactly one relationship exists between users. Without this, multiple follows could exist between e.g. Alice and Bob, and it would be confusing what that means. This is copying what Django’s default hidden through model.

* We use string interpolation in our constraint’s name to namespace it to our model. This prevents naming collisions with constraints on other models. Databases have only one namespace for constraints across all tables, so we need to be careful.

### Preventing self follow

```python
class Follow(models.Model):
    ...

    class Meta:
        constraints = [
            ...,
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        ]
```