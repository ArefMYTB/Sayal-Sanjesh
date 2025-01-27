import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class CustomAppManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "app_id": obj.app_id,
                "app_version_code": obj.app_version_code,
                "app_version_name": obj.app_version_name,
                "app_path": obj.app_path,
                "app_url": obj.app_url,
                "app_create_date": obj.app_create_date,
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class App(models.Model):
    app_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_version_code = models.IntegerField(unique=True)
    app_version_name = models.CharField(max_length=250, null=True)
    app_path = models.CharField(max_length=900)
    app_url = ArrayField(models.CharField(max_length=900), default=list)
    app_create_date = models.DateTimeField(default=datetime.now, blank=True)
    objects = CustomAppManager()

    class Meta:
        db_table = 'App'
