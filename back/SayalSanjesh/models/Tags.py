import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from Authorization.models.Admins import Admins


# Create your models here.


class CustomWaterMetersTagManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "admin_info": {
                    "admin_id": obj.admin.admin_id,
                    "admin_name": obj.admin.admin_name,
                    "admin_lastname": obj.admin.admin_lastname,
                    "admin_phone": obj.admin.admin_phone,
                },
                "water_meter_tag_id": obj.water_meter_tag_id,
                "water_meter_tag_name": obj.water_meter_tag_name,
                "water_meter_tag_create_date": str(obj.water_meter_tag_create_date),
                "water_meter_tag_other_information": obj.water_meter_tag_other_information,
                "water_meter_tag_files": obj.water_meter_tag_files,
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class WaterMetersTags(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    water_meter_tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    water_meter_tag_name = models.CharField(max_length=200)
    water_meter_tag_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    water_meter_tag_other_information = models.JSONField(default={"default": "default"})
    water_meter_tag_files = ArrayField(models.JSONField(blank=True), default=list)
    objects = CustomWaterMetersTagManager()

    class Meta:
        db_table = 'WaterMetersTags'
        indexes = [
            models.Index(fields=['water_meter_tag_id'])]

    def as_dict(self):
        return {
            "admin_info": self.admin.as_dict(),
            "water_meter_tag_id": self.water_meter_tag_id,
            "water_meter_tag_name": self.water_meter_tag_name,
            "water_meter_tag_create_date": str(self.water_meter_tag_create_date),
            "water_meter_tag_other_information": self.water_meter_tag_other_information,
            "water_meter_tag_files": self.water_meter_tag_files,
        }
