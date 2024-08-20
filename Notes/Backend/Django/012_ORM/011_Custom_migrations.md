# Custom migrations

Source: https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/

```python
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Follow = apps.get_model("core", "Follow")
    db_alias = schema_editor.connection.alias
    Follow.objects.using(db_alias).filter(from_user=models.F("to_user")).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_auto_20210225_0320"),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_func,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.CheckConstraint(
                check=models.Q(_negated=True, from_user=models.F("to_user")),
                name="core_follow_prevent_self_follow",
            ),
        ),
    ]
```

* We use the same template for `forwards_func` as in the RunPython [documentation](https://docs.djangoproject.com/en/stable/ref/migration-operations/#django.db.migrations.operations.RunPython).
* We fetch the point-in-history version of the `Follow` model through `apps.get_model()`, rather than importing the latest version. Using the latest version would fail since it could reference fields that haven’t been added to the database yet.
* We also use the current database alias. It’s best to this even if our project only uses a single database, in case it gains multiple in the future.
* We declare `reverse_code` as a no-op, so that this migration is reversible. Reversing the migration won’t be able to restore deleted self-follow relationships because we aren’t backing them up anywhere.
* We declare the operation as elidable. This means Django can drop the operation when squashing the migration history. This is always worth considering when writing a `RunPython` or `RunSQL` operation, as it helps you make smaller, faster squashes.