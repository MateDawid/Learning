# Constraints

Sources:
* https://adamj.eu/tech/2020/03/10/django-check-constraints-sum-percentage-fields/
* https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/
* https://adamj.eu/tech/2020/03/25/django-check-constraints-one-field-set/

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