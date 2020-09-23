import pytest
from django.contrib.auth.models import Group, User

from object_checker.base_object_checker import has_object_permission
from tests.models import AbstractObject


@pytest.fixture()
def super_user(db):
    return User.objects.create_superuser(
        username='superuser',
        password='superuser'
    )


@pytest.fixture()
def manager_user(db):
    user = User.objects.create(
        username='manager',
        password='manager'
    )

    group = Group.objects.create(name='manager')
    group.user_set.add(user)

    return user


@pytest.fixture()
def no_role_user(db):
    return User.objects.create(
        username='no_user',
        password='no_user'
    )


@pytest.fixture()
def abstract_objects(db):
    return AbstractObject.objects.bulk_create([
        AbstractObject(name='abstract_object_1'),
        AbstractObject(name='abstract_object_5'),
        AbstractObject(name='abstract_object_10')
    ])


@pytest.mark.django_db
class TestObjectAuthorization:
    def test_object_authorization_admin(self, abstract_objects, super_user):
        assert has_object_permission('check_abstract_objects', super_user, abstract_objects)

    def test_object_authorization_manager(self, abstract_objects, manager_user):
        assert has_object_permission('check_abstract_objects', manager_user, abstract_objects)

    def test_object_authorization_no_role(self, abstract_objects, no_role_user):
        assert not has_object_permission('check_abstract_objects', no_role_user, abstract_objects)
