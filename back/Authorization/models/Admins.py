import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models


class CustomAdminManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "admin_id": obj.admin_id,
                "admin_name": obj.admin_name,
                "admin_lastname": obj.admin_lastname,
                "admin_phone": obj.admin_phone,
                # "admin_password": obj.admin_password,
                "admin_sms_code": obj.admin_sms_code,
                "admin_permissions": obj.admin_permissions,
                "other_information": obj.other_information,
                "admin_create_date": obj.admin_create_date,
                "admin_phone_number_validation": obj.admin_phone_number_validation,
                "admin_images": obj.admin_images,
                "admin_creator_id": obj.admin_creator_id,
                "lockout_until": obj.lockout_until,
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class Admins(models.Model):
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_name = models.CharField(max_length=200)
    admin_lastname = models.CharField(max_length=200)
    admin_phone = models.CharField(max_length=20, unique=True)
    admin_password = models.CharField(max_length=200)
    admin_sms_code = models.CharField(max_length=10, null=True)
    admin_permissions = ArrayField(models.CharField(max_length=100))
    other_information = models.JSONField()
    admin_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    admin_phone_number_validation = models.IntegerField(default=0)
    admin_sms_code_start_time = models.DateTimeField(null=True)
    admin_images = ArrayField(models.CharField(max_length=400), default=list, null=True)
    admin_creator_id = models.CharField(max_length=200, null=True)
    # Session Policy 
    last_successful_login = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_attempt = models.DateTimeField(null=True, blank=True)
    lockout_until = models.DateTimeField(null=True, blank=True)
    objects = CustomAdminManager()

    class Meta:
        db_table = 'Admins'

    def __str__(self):
        return f"{self.admin_name},  {self.admin_lastname} ,{self.admin_phone}"

    def as_dict(self):
        return {
            "admin_id": self.admin_id,
            "admin_name": self.admin_name,
            "admin_lastname": self.admin_lastname,
            "admin_phone": self.admin_phone,
            "admin_password": self.admin_password,
            "admin_sms_code": self.admin_sms_code,
            "admin_permissions": self.admin_permissions,
            "other_information": self.other_information,
            "admin_create_date": self.admin_create_date,
            "admin_phone_number_validation": self.admin_phone_number_validation,
            "admin_images": self.admin_images,
        }

    def as_dict_customise(self):
        return {
            "admin_id": self.admin_id,
            "admin_name": self.admin_name,
            "admin_lastname": self.admin_lastname,
            "admin_phone": self.admin_phone,
            "admin_permissions": self.admin_permissions,
        }
