import uuid
from datetime import datetime
from django.db import models
from Authorization.models.Admins import Admins

# Create your models here.


class Cities(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    city_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city_name = models.CharField(max_length=255, unique=True)
    city_state = models.CharField(max_length=255, blank=True, null=True)
    city_create_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'Cities'

    def as_dict(self):
        admin_information = {
            "admin_id": self.admin.admin_id,
            "admin_phone": self.admin.admin_phone,
        }
        return {
            "admin_information": admin_information,
            "city_id": self.city_id,
            "city_name": self.city_name,
            "city_state": self.city_state,
            "city_create_date": self.city_create_date
        }
