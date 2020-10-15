import importlib
from typing import Callable

from django.conf import settings
from django.contrib.auth.models import User


class ObjectChecker(object):
    loaded_checkers = {}

    @classmethod
    def get_checkers(cls):
        importlib.import_module(settings.OBJECT_CHECKERS_MODULE)
        subclasses = cls.__subclasses__()

        if not cls.loaded_checkers:
            for subclass in subclasses:
                for attr_name in dir(subclass):
                    if 'check_' in attr_name and isinstance(getattr(subclass, attr_name), Callable):
                        cls.loaded_checkers.update({f'{attr_name}': getattr(subclass, attr_name)})

        return cls.loaded_checkers

    @classmethod
    def retrieve_checker(cls, checker_name: str):
        checkers = cls.get_checkers()

        if checker_name in checkers:
            return checkers[checker_name]

        raise Exception('Checker with name {checker_name} was not registered.'.format(checker_name=checker_name))

    @classmethod
    def get_user_roles(cls, user: User):
        if user:
            groups = user.groups.all()
            return sorted(groups, key=lambda r: r.name)
        else:
            return []


def has_object_permission(checker_name: str, user: User, obj) -> bool:
    if user.is_superuser:
        has_permission = True
    else:
        checker = ObjectChecker.retrieve_checker(checker_name)
        user_roles = ObjectChecker.get_user_roles(user)

        has_permission = any([checker(user_role, user, obj) for user_role in user_roles])

    return has_permission
