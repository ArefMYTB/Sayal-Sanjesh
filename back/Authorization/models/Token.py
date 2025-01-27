import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from Authorization.models.Admins import Admins
from Authorization.models.Users import Users


# Create your models here.

class CustomTokenManager(models.Manager):
    user_rows = None

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {

                "token": obj.token,
                "owner_id": obj.owner_id
            }

            serialized_data.append(serialized_obj)
        return serialized_data


class Token(models.Model):
    owner_id = models.CharField(max_length=200)
    token = models.TextField()
    other_information = models.JSONField(null=True)
    objects = CustomTokenManager()

    class Meta:
        db_table = 'Token'
