import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from Authorization.models.Admins import Admins


# Create your models here.

class CustomUserManager(models.Manager):
    user_rows = None

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        if hasattr(queryset, '__iter__') is True:
            CustomUserManager.user_rows = Users.objects.count()
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
                    "other_information": obj.admin.other_information,
                },
                "user_id": obj.user_id,
                "user_name": obj.user_name,
                "user_lastname": obj.user_lastname,
                "user_phone": obj.user_phone,
                "user_sms_code": obj.user_sms_code,
                "user_profile": obj.user_profile,
                "other_information": obj.other_information,
                "user_create_date": obj.user_create_date,
                "user_phone_number_validation": obj.user_phone_number_validation,
                "user_images": obj.user_images,
            }
            if obj.user_sms_code_start_time is not None:
                serialized_obj['user_sms_code_start_time'] = int(obj.user_sms_code_start_time.timestamp())
            else:
                serialized_obj['user_sms_code_start_time'] = obj.user_sms_code_start_time
            if hasattr(queryset, '__iter__') is True:
                serialized_obj['all users'] = CustomUserManager.user_rows
            serialized_data.append(serialized_obj)
        return serialized_data


class Users(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=200, null=True)
    user_lastname = models.CharField(max_length=200, null=True)
    user_phone = models.CharField(max_length=20, unique=True)
    user_password = models.CharField(max_length=200, null=True)
    user_sms_code = models.CharField(max_length=10, null=True)
    user_profile = models.JSONField(null=True)
    other_information = models.JSONField(null=True)
    user_password_changed = models.IntegerField(default=0)
    user_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    user_phone_number_validation = models.IntegerField(default=0)
    user_sms_code_start_time = models.DateTimeField(null=True)
    user_images = ArrayField(models.CharField(max_length=400), default=list, null=True)
    objects = CustomUserManager()

    class Meta:
        db_table = 'Users'

    def as_dict(self):
        return {
            "admin": self.admin.as_dict(),
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_lastname": self.user_lastname,
            "user_phone": self.user_phone,
            "user_password": self.user_password,
            "user_sms_code": self.user_sms_code,
            "user_profile": self.user_profile,
            "other_information": self.other_information,
            "user_create_date": self.user_create_date,
            "user_phone_number_validation": self.user_phone_number_validation,
            "user_sms_code_start_time": self.user_sms_code_start_time,
            "user_images": self.user_images

        }

    def as_dict_customise(self):
        return {
            "admin": self.admin.as_dict_customise(),
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_lastname": self.user_lastname,
            "user_phone": self.user_phone,
            "user_profile": self.user_profile,
            "other_information": self.other_information,
            "user_create_date": self.user_create_date
        }
