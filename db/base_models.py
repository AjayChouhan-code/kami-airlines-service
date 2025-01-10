import uuid

from django.db import models
from django.db.models import Max

from django_mysql.models import Bit1BooleanField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    # ID settings
    id = models.BigAutoField(primary_key=True, unique=True)
    uuid = models.BigIntegerField(editable=False, unique=True)

    # Create and update triggers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @classmethod
    def get_new_uuid(cls):
        last_uuid = cls.objects.aggregate(Max("uuid")).get("uuid__max")
        last_uuid = last_uuid or 0
        new_uuid = last_uuid + 1
        return new_uuid

    def save(self, **kwargs):
        if not self.uuid:
            self.uuid = self.get_new_uuid()

        super(BaseModel, self).save(**kwargs)


class BooleanField(Bit1BooleanField, models.BooleanField):
    def db_type(self, connection):
        if connection.settings_dict["ENGINE"] == "django.db.backends.mysql":
            return super(Bit1BooleanField, self).db_type(connection)
        else:
            return super(BooleanField, self).db_type(connection)


# Soft Delete #
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = BooleanField(default=False, null=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True
