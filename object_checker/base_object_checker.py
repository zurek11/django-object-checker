import importlib
from typing import Callable
from abc import ABC

from django.conf import settings
from django.contrib.auth.models import User


class CheckingManager(ABC):
    loaded_checkers = {}

    @classmethod
    def get_checkers(cls):
        importlib.import_module(settings.OBJECT_CHECKERS_MODULE)
        checking_subclasses = cls.__subclasses__()

        if not cls.loaded_checkers:
            for checking_subclass in checking_subclasses:
                subclasses = checking_subclass.__subclasses__()

                for subclass in subclasses:
                    for attr_name in dir(subclass):
                        if 'check_' in attr_name and isinstance(getattr(subclass, attr_name), Callable):
                            if attr_name in cls.loaded_checkers:
                                raise Exception(
                                    'Checker {checker_name} has two instances with the same name.'.format(
                                        checker_name=attr_name
                                    )
                                )
                            else:
                                cls.loaded_checkers.update(
                                    {f'{attr_name}': (getattr(subclass, attr_name), checking_subclass)}
                                )

        return cls.loaded_checkers

    @classmethod
    def retrieve_checker(cls, checker_name: str):
        checkers = cls.get_checkers()

        if checker_name in checkers:
            checker = checkers[checker_name]
        else:
            checker = None
        return checker


class AbacChecker(CheckingManager):
    @classmethod
    def get_checkers(cls):
        importlib.import_module(settings.OBJECT_CHECKERS_MODULE)
        subclasses = cls.__subclasses__()

        if not cls.loaded_checkers:
            for subclass in subclasses:
                for attr_name in dir(subclass):
                    if 'check_' in attr_name and isinstance(getattr(subclass, attr_name), Callable):
                        if attr_name in cls.loaded_checkers:
                            raise Exception(
                                'Checker {checker_name} has two instances with the same name.'.format(
                                    checker_name=attr_name
                                )
                            )
                        else:
                            cls.loaded_checkers.update({f'{attr_name}': (getattr(subclass, attr_name), cls)})

        return cls.loaded_checkers


class RbacChecker(CheckingManager):
    @classmethod
    def get_checkers(cls):
        importlib.import_module(settings.OBJECT_CHECKERS_MODULE)
        subclasses = cls.__subclasses__()

        if not cls.loaded_checkers:
            for subclass in subclasses:
                for attr_name in dir(subclass):
                    if 'check_' in attr_name and isinstance(getattr(subclass, attr_name), Callable):
                        if attr_name in cls.loaded_checkers:
                            raise Exception(
                                'Checker {checker_name} has two instances with the same name.'.format(
                                    checker_name=attr_name
                                )
                            )
                        else:
                            cls.loaded_checkers.update({f'{attr_name}': (getattr(subclass, attr_name), cls)})

        return cls.loaded_checkers

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
        checker = CheckingManager.retrieve_checker(checker_name)

        if checker:
            if checker[1] is RbacChecker:
                user_roles = RbacChecker.get_user_roles(user)
                has_permission = any([checker[0](user_role, user, obj) for user_role in user_roles])
            elif checker[1] is AbacChecker:
                has_permission = checker[0](user, obj)
            else:
                has_permission = False
        else:
            raise Exception('Checker with name {checker_name} was not registered.'.format(checker_name=checker_name))

    return has_permission


__all__ = [
    'RbacChecker',
    'AbacChecker',
    'has_object_permission'
]
