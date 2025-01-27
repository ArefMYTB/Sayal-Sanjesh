import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from Authorization.models.Admins import Admins
from Authorization.models.Users import Users


# Create your models here.
# -------------------------------------------------------MqttLoger------------------------------------------------------
class CustomMqttLogerManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        all_mqtt_logs = MqttLoger.objects.count()
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "log_id": obj.log_id,
                "topic_name": obj.topic_name,
                "message": obj.message,
                "state": obj.state,
                "create_date": obj.create_date,
                "all_mqtt_logs": all_mqtt_logs
            }
            if obj.admin is not None:
                serialized_obj['admin'] = obj.admin.admin_id
            else:
                serialized_obj['admin'] = obj.admin
            serialized_data.append(serialized_obj)
        return serialized_data


class MqttLoger(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE, null=True)
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic_name = models.CharField(max_length=200, null=True)
    message = models.TextField(null=True)
    state = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    objects = CustomMqttLogerManager()

    class Meta:
        db_table = 'MqttLoger'


# -----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------SystemLog------------------------------------------------------
class CustomSystemLogManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        all_system_logs = SystemLog.objects.count()
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "system_log_id": obj.system_log_id,
                "system_log_action": obj.system_log_action,
                "system_log_object_action_on": obj.system_log_object_action_on,
                "system_log_action_table": obj.system_log_action_table,
                "system_log_field_changes": obj.system_log_field_changes,
                "system_log_message": obj.system_log_message,
                "system_log_create_time": obj.system_log_create_time,
                "all_system_logs": all_system_logs
            }
            if obj.system_log_admin is not None:
                serialized_obj[
                    'system_log_admin'] = f"{obj.system_log_admin.admin_name} {obj.system_log_admin.admin_lastname}"
            else:
                serialized_obj['system_log_admin'] = obj.system_log_admin
            if obj.system_log_user is not None:
                serialized_obj[
                    'system_log_user'] = f"{obj.system_log_user.user_name} {obj.system_log_user.user_lastname}"
            else:
                serialized_obj['system_log_user'] = obj.system_log_user
            serialized_data.append(serialized_obj)
        return serialized_data


class SystemLog(models.Model):
    system_log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_log_admin = models.ForeignKey(Admins, on_delete=models.CASCADE, null=True)
    system_log_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    system_log_action = models.CharField(max_length=200)
    system_log_object_action_on = models.CharField(max_length=200)
    system_log_action_table = models.CharField(max_length=200)
    system_log_field_changes = models.JSONField(null=True)
    system_log_message = models.TextField(null=True)
    system_log_information = models.JSONField(null=True)
    system_log_create_time = models.DateTimeField(default=datetime.now)
    objects = CustomSystemLogManager()

    class Meta:
        db_table = 'SystemLog'
# ----------------------------------------------------------------------------------------------------------------------
