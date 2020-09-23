from django.contrib.auth.models import Group, User

from object_checker.base_object_checker import ObjectChecker


class AbstractObjectsChecker(ObjectChecker):
    @staticmethod
    def check_abstract_objects(role: Group, user: User, obj):
        if role:
            if role.name == 'manager':
                return True
        return False
