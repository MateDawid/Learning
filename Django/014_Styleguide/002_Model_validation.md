# Model validation

Sources:
* https://github.com/HackSoftware/Django-Styleguide

## clean and full_clean
Lets take a look at an example model:

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")
```

We are defining the model's clean method, because we want to make sure we get good data in our database.

Now, in order for the clean method to be called, someone must call full_clean on an instance of our model, before saving.

Our recommendation is to do that in the service, right before calling save:

```python
def course_create(*, name: str, start_date: date, end_date: date) -> Course:
    obj = Course(name=name, start_date=start_date, end_date=end_date)

    obj.full_clean()
    obj.save()

    return obj
```

This also plays well with Django admin, because the forms used there will trigger full_clean on the instance.

We have few general rules of thumb for when to add validation in the model's clean method:

* If we are validating based on multiple, non-relational fields, of the model.
* If the validation itself is simple enough. 

Validation should be moved to the service layer if:

* The validation logic is more complex.
* Spanning relations & fetching additional data is required.

It's OK to have validation both in clean and in the service, but we tend to move things in the service, if that's the case.

## constraints

As proposed in this issue, if you can do validation using Django's constraints, then you should aim for that.

Less code to write, less to code to maintain, the database will take care of the data even if it's being inserted from a different place.

Lets look at an example!

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```
