from django.contrib.auth.models import User

from object_checker.base_object_checker import RbacChecker


class CustomChecker(RbacChecker):
    @classmethod
    def get_user_roles(cls, user: User, **kwargs):
        if user:
            groups = user.groups.all()
            return sorted(groups, key=lambda r: r.name)
        else:
            return []
