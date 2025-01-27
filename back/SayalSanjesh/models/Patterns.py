import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from Authorization.models.Admins import Admins
from .Tags import WaterMetersTags
from .Meters import WaterMetersProjects


# Create your models here.

class CustomPatternManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        all_pattern_number = Pattern.objects.count()
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "admin": {
                    "admin_id": obj.admin.admin_id,
                    "admin_name": obj.admin.admin_name,
                    "admin_lastname": obj.admin.admin_lastname,
                    "admin_phone": obj.admin.admin_phone,
                },
                "pattern_id": obj.pattern_id,
                "pattern_tag": {
                    "water_meter_tag_id": obj.pattern_tag.water_meter_tag_id,
                    "water_meter_tag_name": obj.pattern_tag.water_meter_tag_name,
                    "water_meter_tag_create_date": obj.pattern_tag.water_meter_tag_create_date,
                    "water_meter_tag_other_information": obj.pattern_tag.water_meter_tag_other_information,
                },
                "pattern_project": {
                    "water_meter_project_id": obj.pattern_project.water_meter_project_id,
                    "water_meter_project_name": obj.pattern_project.water_meter_project_name,
                    "water_meter_project_title": obj.pattern_project.water_meter_project_title,
                    "water_meter_project_create_date": obj.pattern_project.water_meter_project_create_date,
                },
                "pattern_list": obj.pattern_list,
                "pattern_create_date": obj.pattern_create_date,
            }
            if hasattr(queryset, '__iter__') is True:
                serialized_obj['all_pattern_number'] =all_pattern_number
            serialized_data.append(serialized_obj)
        return serialized_data


class Pattern(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    pattern_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pattern_tag = models.ForeignKey(WaterMetersTags, on_delete=models.DO_NOTHING)
    pattern_project = models.ForeignKey(WaterMetersProjects, on_delete=models.DO_NOTHING, null=True, blank=True)
    pattern_list = ArrayField(models.JSONField(blank=True), default=list)
    pattern_create_date = models.DateTimeField(default=datetime.now, blank=True)
    objects = CustomPatternManager()

    class Meta:
        db_table = 'Pattern'

    def as_dict(self):
        water_meter_tag_information = {
            "water_meter_tag_id": self.pattern_tag.water_meter_tag_id,
            "water_meter_tag_name": self.pattern_tag.water_meter_tag_name,
            "water_meter_tag_create_date": self.pattern_tag.water_meter_tag_create_date,
        }
        water_meter_project_information = {
            "water_meter_project_id": self.pattern_project.water_meter_project_id,
            "water_meter_project_name": self.pattern_project.water_meter_project_name,
            "water_meter_project_title": self.pattern_project.water_meter_project_title,
            "water_meter_project_create_date": self.pattern_project.water_meter_project_create_date,
        }
        return {
            "admin": self.admin.as_dict()['admin_id'],
            "pattern_id": self.pattern_id,
            "pattern_tag": water_meter_tag_information,
            "pattern_project": water_meter_project_information,
            "pattern_list": self.pattern_list,
            "pattern_create_date": self.pattern_create_date,
        }
