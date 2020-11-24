from django.contrib.auth.models import Group, User

from object_checker.base_object_checker import RbacChecker, AbacChecker


class RbacObjectChecker(RbacChecker):
    @classmethod
    def check_rbac(cls, role: Group, user: User, obj):
        if role:
            if role.name == 'manager':
                return True
        return False


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


class RbacExceptionSibling(RbacChecker):
    @classmethod
    def check_exception(cls, role: Group, user: User, obj):
        return True


class AbacExceptionSibling(AbacChecker):
    @classmethod
    def check_exception(cls, user: User, obj):
        return True
