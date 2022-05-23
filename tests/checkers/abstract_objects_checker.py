from django.contrib.auth.models import Group, User

from object_checker.base_object_checker import RbacChecker, AbacChecker
from tests.checkers.custom_checker import CustomChecker


class RbacObjectChecker(RbacChecker):
    @classmethod
    def check_rbac(cls, role: Group, user: User, obj):
        if role:
            if role.name == 'manager':
                return True
        return False


class CustomObjectChecker(CustomChecker):
    @classmethod
    def check_kwargs(cls, user: User, obj):
        return True


class AbacObjectChecker(AbacChecker):
    @classmethod
    def check_abac(cls, user: User, obj):
        try:
            user_group = user.groups.get(name='manager')
            group_name = user_group.name
        except Group.DoesNotExist:
            group_name = ''

        if group_name == 'manager':
            return True
        return False
