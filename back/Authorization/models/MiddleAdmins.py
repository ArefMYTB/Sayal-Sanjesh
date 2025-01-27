from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
# from .Admins import Admins
from Authorization.models.Admins import Admins


# Create your models here.

class CustomMiddleAdminManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "middle_admin_id": obj.middle_admin_id,
                "project_ids": obj.project_ids,
                "water_meter_ids": obj.water_meter_ids,
                "create_date": obj.create_date
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class MiddleAdmins(models.Model):
    # base_admin_id = models.ForeignKey(Admins, on_delete=models.CASCADE, related_name='base_admin')
    middle_admin_id = models.ForeignKey(Admins, primary_key=True, on_delete=models.CASCADE, editable=False)
    project_ids = ArrayField(models.CharField(max_length=100), null=True)
    water_meter_ids = ArrayField(models.CharField(max_length=100), null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    objects = CustomMiddleAdminManager()
    class Meta:
        db_table = 'MiddleAdmins'

    def as_dict(self):
        return {
            # "base_admin_id": self.base_admin_id,
            "middle_admin_id": self.middle_admin_id,
            "project_ids": self.project_ids,
            "water_meter_ids": self.water_meter_ids,
            "create_date": self.create_date
        }
