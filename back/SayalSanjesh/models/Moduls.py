import uuid
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from Authorization.models.Admins import Admins


# -----------------------------------------------ModuleType model-------------------------------------------------------
class CustomModuleTypeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                # Add any other custom fields you want to include in the response
                "admin_info": obj.admin.as_dict()['admin_id'],
                "module_type_id": obj.module_type_id,
                "module_type_name": obj.module_type_name,
                "module_type_create_date": str(obj.module_type_create_date),
                "module_other_information": obj.module_other_information,
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class ModuleTypes(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    module_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module_type_name = models.CharField(max_length=200)
    module_type_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    # water_meter_project = models.ForeignKey(WaterMetersProjects, on_delete=models.DO_NOTHING)
    module_other_information = models.JSONField()
    objects = CustomModuleTypeManager()

    class Meta:
        db_table = 'ModuleTypes'


# ----------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------Module model-----------------------------------------------------------
class CustomMetersModuleManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset, modules_total_number=None):
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
                "water_meter_module_id": obj.water_meter_module_id,
                "water_meter_module_code": obj.water_meter_module_code,
                "water_meter_module_name": obj.water_meter_module_name,
                "water_meter_module_unit": obj.water_meter_module_unit,
                "water_meter_module_sim": obj.water_meter_module_sim,
                "water_meter_module_sim_operator": obj.water_meter_module_sim_operator,
                "water_meter_module_property": obj.water_meter_module_property,
                "water_meter_module_create_date": str(obj.water_meter_module_create_date),
                "water_meter_module_other_information": obj.water_meter_module_other_information,
            }
            if obj.module_type is not None:
                serialized_obj['module_type_info'] = {
                    "module_type_id": obj.module_type.module_type_id,
                    "module_type_name": obj.module_type.module_type_name,
                    "module_type_create_date": str(obj.module_type.module_type_create_date),
                    "module_other_information": obj.module_type.module_other_information,
                }
            else:
                serialized_obj['module_type_info'] = {
                    "module_type_id": None,
                    "module_type_name": None,
                    "module_type_create_date": None,
                    "module_other_information": None,
                }
            if modules_total_number is not None:
                serialized_obj['modules_total_number'] = modules_total_number
            else:
                serialized_obj['modules_total_number'] = WaterMetersModules.objects.count()
            serialized_data.append(serialized_obj)
        return serialized_data


class WaterMetersModules(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    water_meter_module_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    water_meter_module_unit = models.CharField(max_length=200, null=True, blank=True)
    water_meter_module_code = models.CharField(max_length=200, unique=True)
    water_meter_module_name = models.CharField(max_length=200)
    water_meter_module_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    water_meter_module_other_information = models.JSONField()
    water_meter_module_sim = models.CharField(max_length=200, null=True, blank=True)
    water_meter_module_sim_operator = models.CharField(max_length=200, null=True, blank=True)
    water_meter_module_property = ArrayField(models.CharField(max_length=200), default=list, null=True)
    water_meter_request = models.ManyToManyField('WaterMetersRequests')
    module_type = models.ForeignKey(ModuleTypes, on_delete=models.CASCADE, null=True, blank=True)
    objects = CustomMetersModuleManager()

    class Meta:
        db_table = 'WaterMetersModules'

    def as_dict(self):
        return {
            "admin_info": self.admin.as_dict(),
            "water_meter_module_id": self.water_meter_module_id,
            "water_meter_module_code": self.water_meter_module_code,
            "water_meter_module_name": self.water_meter_module_name,
            "water_meter_module_unit": self.water_meter_module_unit,
            "water_meter_module_create_date": self.water_meter_module_create_date,
            "water_meter_module_other_information": self.water_meter_module_other_information,
            "water_meter_request": self.water_meter_request,
        }

# ----------------------------------------------------------------------------------------------------------------------
