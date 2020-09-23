# django-object-checker

[![codecov](https://codecov.io/gh/zurek11/django-object-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/zurek11/django-object-checker)

Hello. I'm just an abstract object 📦 and I would be very glad to have user authorization because I hate criminals 🦹‍♂️ like pedophiles, robbers, hackers and so on.

## Introduction

Project django-object-checker extends standard django role base access control to be able to check individual object types.

Main purpose of this extended authorization system is to maintain control for each objects individually with modular solution.

## Installation

```python
# pip
pip install django-object-checker

# pipenv
pipenv install django-object-checker

# poetry
poetry add django-object-checker
```

## Setup

#### Just add checkers module path to `settings.OBJECT_CHECKERS_MODULE`:

> The path is path to the module, where you going to implement all your checkers.
> This is required for our BaseObjectChecker to be able to find his subclasses.

```python
OBJECT_CHECKERS_MODULE = 'app.checkers'
```

## Example

#### 1. Create module according to specified path in settings

#### 2. Create your own ObjectChecker class with checker method

> Valid check methods are only these, which name starts with `check_`.
> So if you want to implement your custom methods which you want to be ignored by BaseObjectChecker your hands are free.

```python
from django.contrib.auth.models import Group, User

from object_checker.base_object_checker import ObjectChecker


class MyObjectChecker(ObjectChecker):
    @staticmethod
    def check_my_object(role: Group, user: User, obj):
        result = False

        if role.name == 'manager':
            result = True

        return result
```

#### 3. Add new object check class to module `__init__.py`

```python
from app.checkers.my_object_checker import MyObjectChecker
```

#### 4. Example usage of your custom object checker in your project

> Method to check is `has_object_permission` and has three arguments:
> 1. name of check method
> 2. user object
> 3. object/objects to be checked

```python
from object_checker.base_object_checker import has_object_permission

if has_object_permission('check_my_object', user, my_object):
    print('User has access to this/these object/objects.')
else:
    print('User has NOT access to this/these object/objects.')
```

---
Made with ❤ by [Adam Žúrek](https://zurek11.github.io/) & [BACKBONE s.r.o.](https://www.backbone.sk/en/)
