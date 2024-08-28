# Setting up a complex software project

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150391480/posts/2153274176

## Project files

* LICENSE
* README.md
* requirements.txt / pyproject.toml / other dependencies file
* .pylintrc
* .gitignore

## Project folders

* assets - images, json files, pdfs, other data files
* docs - documentation files for users
* wiki - documentation files for developers
* locales - translations in multilanguage apps
* src - source directory for code
* tests - unit tests
* tools - script for development purposes

## Modules and packages

Every file in Python is considered as module and every directory is considered as package.

## Import tips

```python
# OK
from package_1.file_1 import function_1
from package import file
import package

# Not OK
from package_1.file_1 import *
```

## Code organising

Avoid generic packages names like utils, helpers, etc. It would lead to group unrelated things in single package - 
we need to avoid that. Better solution is to split it into smaller packages focused on particular goal.  

## Architecture as structure

To make code organization easier you can translate picked architecture to directories in application. Example: if you use 
Model-View-Controller architecture pattern you can create model, view, controller directories to store logic for particular architecture part.
