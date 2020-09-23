from django.db import models


class AbstractObject(models.Model):
    class Meta:
        app_label = 'tests'
        db_table = 'abstract_models'
        default_permissions = ()

    name = models.CharField(max_length=50, null=False, default='test_abstract_object')
