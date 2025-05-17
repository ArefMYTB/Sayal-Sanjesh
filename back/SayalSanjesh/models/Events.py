import uuid
from django.db import models
from Authorization.models.Admins import Admins
from .Moduls import WaterMetersModules


# Create your models here.

# --------------------------------------------------EventsType---------------------------------------------------------
class CustomEventTypeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "event_type_admin": {
                    "admin_id": obj.event_type_admin.admin_id,
                    "admin_name": obj.event_type_admin.admin_name,
                    "admin_lastname": obj.event_type_admin.admin_lastname,
                    "admin_phone": obj.event_type_admin.admin_phone,
                },
                "event_type_id": obj.event_type_id,
                "event_type_code": obj.event_type_code,
                "event_type_keyword": obj.event_type_keyword,
                "event_type_importance": obj.event_type_importance,
                "evnet_type_information": obj.evnet_type_information,
                "event_type_dashboard_view": obj.event_type_dashboard_view,
                "event_type_create_time": obj.event_type_create_time,
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class EventType(models.Model):
    IMPORTANCE_CHOICE = [
        ('H', 'High'),
        ('M', 'Modrate'),
        ('L', 'Low'),
    ]
    event_type_admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    event_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type_code = models.CharField(max_length=255, unique=True)
    event_type_keyword = models.CharField(max_length=255)
    event_type_importance = models.CharField(max_length=1, choices=IMPORTANCE_CHOICE)
    evnet_type_information = models.JSONField()
    event_type_create_time = models.DateTimeField(auto_now_add=True)
    event_type_dashboard_view = models.BooleanField(default=True)
    objects = CustomEventTypeManager()

    class Meta:
        db_table = 'EventType'

    def as_dict(self):
        admin_info = {
            "admin_id": self.event_type_admin.admin_id,
            "admin_name": self.event_type_admin.admin_name,
            "admin_lastname": self.event_type_admin.admin_lastname,
            "admin_phone": self.event_type_admin.admin_phone,
        }
        return {
            "event_type_admin": admin_info,
            "event_type_id": self.event_type_id,
            "event_type_code": self.event_type_code,
            "event_type_keyword": self.event_type_keyword,
            "event_type_importance": self.event_type_importance,
            "evnet_type_information": self.evnet_type_information,
            "event_type_create_time": self.event_type_create_time,
        }


# ----------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------Events--------------------------------------------------------------
class CustomEventsManager(models.Manager):

    def create(self, **kwargs):
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset, admin_id=None):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "event_id": obj.event_id,
                "event_type": {
                    "event_type_id": obj.event_type.event_type_id,
                    "event_type_code": obj.event_type.event_type_code,
                    "event_type_keyword": obj.event_type.event_type_keyword,
                    "event_type_importance": obj.event_type.event_type_importance,
                    "evnet_type_information": obj.event_type.evnet_type_information,
                    "event_type_create_time": obj.event_type.event_type_create_time,
                },
                "event_module": {
                    "water_meter_module_id": obj.event_module.water_meter_module_id,
                    "water_meter_module_unit": obj.event_module.water_meter_module_unit,
                    "water_meter_module_code": obj.event_module.water_meter_module_code,
                    "water_meter_module_name": obj.event_module.water_meter_module_name,
                    "water_meter_module_create_date": obj.event_module.water_meter_module_create_date,
                },
                "event_information": obj.event_information,
                "event_create_time": obj.event_create_time,
                "event_count": obj.event_count,
                "event_counter": obj.event_counter,
                "event_last_occurrence": obj.event_last_occurrence,
                "all_event_numbers": Event.objects.filter(event_module=obj.event_module).count(),
            }
            # try:
            #     event_view = EventView.objects.get(event=obj.event_id, admin=admin_id)
            #     serialized_obj['event_view_by_admin'] = (True, event_view.viewed_at)
            # except:
            #     serialized_obj['event_view_by_admin'] = (False, None)
            serialized_data.append(serialized_obj)
        return serialized_data


class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
    event_module = models.ForeignKey(WaterMetersModules, on_delete=models.DO_NOTHING)
    event_count = models.FloatField()
    event_counter = models.FloatField(null=True)
    event_information = models.JSONField()
    event_create_time = models.DateTimeField()
    event_last_occurrence = models.DateTimeField(null=True)
    event_response_send = models.BooleanField(default=False)
    # viewed_by = models.ManyToManyField(Admins, through='EventViewed', related_name='viewed_events')
    objects = CustomEventsManager()

    class Meta:
        db_table = 'Event'

    def as_dict(self):
        event_module_information = {
            "water_meter_module_id": self.event_module.water_meter_module_id,
            "water_meter_module_code": self.event_module.water_meter_module_code,
            "water_meter_module_name": self.event_module.water_meter_module_name,
            "water_meter_module_unit": self.event_module.water_meter_module_unit,
            "water_meter_module_other_information": self.event_module.water_meter_module_other_information,
            "water_meter_module_create_date": self.event_module.water_meter_module_create_date,
        }
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.as_dict(),
            "event_module": event_module_information,
            "event_value": self.event_value,
            "event_information": self.event_information,
            "event_create_time": self.event_create_time,
        }


# ----------------------------------------------------------------------------------------------------------------------
