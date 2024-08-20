# Full clean

Source: https://jamescooke.info/djangos-model-save-vs-full_clean.html

* Creating an instance of a Model and calling `save` on that instance does not call `full_clean`. Therefore it’s possible for invalid data to enter your database if you don’t manually call the `full_clean` function before saving.

* Object managers’ default `create` function also doesn’t call `full_clean`.