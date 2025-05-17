import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models
from Authorization.models.Admins import Admins
from .Meters import WaterMeters


# Create your models here.


# ----------------------------------------------------OrderType---------------------------------------------------------

class CustomOrderTypeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        all_order_type_numbers = OrderType.objects.count()
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                # "event_type_admin": {
                #     "admin_id": obj.order_type_admin.admin_id,
                #     "admin_name": obj.order_type_admin.admin_name,
                #     "admin_lastname": obj.order_type_admin.admin_lastname,
                #     "admin_phone": obj.order_type_admin.admin_phone,
                # },
                "order_type_id": obj.order_type_id,
                "order_type_code": obj.order_type_code,
                "order_type_name": obj.order_type_name,
                "order_type_information": obj.order_type_information,
                "order_type_create_time": obj.order_type_create_time,
            }
            if hasattr(queryset, '__iter__') is True:
                serialized_obj['all_orders_number'] = all_order_type_numbers
            serialized_data.append(serialized_obj)
        return serialized_data


class OrderType(models.Model):
    order_type_admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    order_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_type_code = models.CharField(max_length=255, unique=True)
    order_type_name = models.CharField(max_length=255)
    order_type_information = models.JSONField()
    order_type_create_time = models.DateTimeField(auto_now_add=True)
    objects = CustomOrderTypeManager()

    class Meta:
        db_table = 'OrderType'

    def as_dict(self):
        admin_information = {
            "admin_id": self.order_type_admin.as_dict().get('admin_id'),
            "admin_name": self.order_type_admin.as_dict().get('admin_name'),
            "admin_lastname": self.order_type_admin.as_dict().get('admin_lastname'),
        }
        return {
            "event_type_admin": admin_information,
            "order_type_id": self.order_type_id,
            "order_type_code": self.order_type_code,
            "order_type_name": self.order_type_name,
            "order_type_information": self.order_type_information,
            "order_type_create_time": self.order_type_create_time,
        }


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------Order-------------------------------------------------------------

class CustomOrderManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        all_orders_number = Order.objects.count()
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "order_id": obj.order_id,
                "order_type": {
                    "order_type_id": obj.order_type.order_type_id,
                    "order_type_code": obj.order_type.order_type_code,
                    "order_type_name": obj.order_type.order_type_name,
                    "order_type_information": obj.order_type.order_type_information,
                },
                "order_meter": {
                    # "water_meter_user": obj.order_meter.water_meter_user.user_id,
                    "water_meter_serial": obj.order_meter.water_meter_serial,
                    "water_meter_name": obj.order_meter.water_meter_name,
                },
                "order_counter": obj.order_counter,
                "order_information": obj.order_information,
                "order_create_time": obj.order_create_time,
                "order_status": obj.order_status,
                "order_status_time": obj.order_status_time,
            }
            if hasattr(queryset, '__iter__') is True:
                serialized_obj['all_orders_number'] = all_orders_number
            serialized_data.append(serialized_obj)
        return serialized_data


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_type = models.ForeignKey(OrderType, on_delete=models.DO_NOTHING)
    order_meter = models.ForeignKey(WaterMeters, on_delete=models.DO_NOTHING)
    order_information = models.JSONField()
    order_status = models.IntegerField(default=-1)
    order_status_time = models.DateTimeField(null=True)
    order_create_time = models.DateTimeField(auto_now_add=True)
    order_counter = models.IntegerField(null=True)
    objects = CustomOrderManager()

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return f"{self.order_id},{self.order_counter},{self.order_type.order_type_code}"

    def as_dict(self):
        return {
            "order_id": self.order_id,
            "order_type": self.order_type.as_dict(),
            "order_meter": self.order_meter.as_dict().get('water_meter_serial'),
            "order_information": self.order_information,
            "order_create_time": self.order_create_time,
            "order_status": self.order_status,
            "order_status_time": self.order_status_time,
        }

