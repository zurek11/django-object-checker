import importlib
from typing import Callable
from abc import ABC

from django.conf import settings
from django.contrib.auth.models import User


class CheckingManager(ABC):
    loaded_checkers = {}

    @classmethod
    def all_subclasses(cls, cl):
        return set(cl.__subclasses__()).union(
            [s for c in cl.__subclasses__() for s in cls.all_subclasses(c)]
        )

    @classmethod
    def get_checkers(cls):
        importlib.import_module(settings.OBJECT_CHECKERS_MODULE)
        checking_subclasses = cls.all_subclasses(cls)

        if not cls.loaded_checkers:
            for checking_subclass in checking_subclasses:
                for attr_name in dir(checking_subclass):
                    if 'check_' in attr_name:
                        if isinstance(getattr(checking_subclass, attr_name), Callable):
                            if attr_name in cls.loaded_checkers:
                                raise Exception(
                                    'Checker {checker_name} has two instances with the same name.'.format(
                                        checker_name=attr_name
                                    )
                                )
                            else:
                                cls.loaded_checkers.update(
                                    {f'{attr_name}': (getattr(checking_subclass, attr_name), checking_subclass)}
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
    pass


class RbacChecker(CheckingManager):
    @classmethod
    def get_user_roles(cls, user: User, **kwargs):
        if user:
            groups = user.groups.all()
            return sorted(groups, key=lambda r: r.name)
        else:
            return []


def has_object_permission(checker_name: str, user: User, obj, **kwargs) -> bool:
    if user.is_superuser:
        has_permission = True
    else:
        checker = CheckingManager.retrieve_checker(checker_name)

        if checker:
            if issubclass(checker[1], RbacChecker):
                user_roles = checker[1].get_user_roles(user, **kwargs)
                has_permission = any([checker[0](user_role, user, obj, **kwargs) for user_role in user_roles])
            elif issubclass(checker[1], AbacChecker):
                has_permission = checker[0](user, obj, **kwargs)
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
