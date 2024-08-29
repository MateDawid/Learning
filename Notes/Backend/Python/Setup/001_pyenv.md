# pyenv / pyenv-win
pyenv is tool that simplifies installing and switching between different versions of Python on the same machine. It keeps the system version of Python intact, which is required for some operating systems to run properly, while still making it easy to switch Python versions based on a specific project's requirements.

Installing Python versions:
```
$ pyenv install 3.8.5
$ pyenv install 3.8.6
$ pyenv install 3.9.0
$ pyenv install 3.10.2

$ pyenv versions
* system
  3.8.5
  3.8.6
  3.9.0
  3.10.2
```
Setting particular version as global:
```
$ pyenv global 3.8.6

$ pyenv versions
  system
  3.8.5
* 3.8.6 (set by /Users/michael/.pyenv/version)
  3.9.0
  3.10.2

$ python -V
Python 3.8.6
```

Setting particular version as local (for specific project):
```
$ pyenv local 3.10.2

$ pyenv versions
  system
  3.8.5
  3.8.6
  3.9.0
* 3.10.2 (set by /Users/michael/repos/testdriven/python-environments/.python-version)

$ python -V
Python 3.10.2
```