import uuid
from datetime import datetime
from django.db import models
from Authorization.models.Admins import Admins


# Create your models here.


class WaterMetersRequests(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    water_meter_request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    water_meter_request_title = models.CharField(max_length=200, null=True, blank=True)
    water_meter_request_information = models.JSONField()
    water_meter_request_create_date = models.DateTimeField(
        default=datetime.now, blank=True)

    class Meta:
        db_table = 'WaterMetersRequests'

    def as_dict(self):
        return {
            "admin": self.admin.as_dict(),
            "water_meter_request_id": self.water_meter_request_id,
            "water_meter_request_title": self.water_meter_request_title,
            "water_meter_request_information": self.water_meter_request_information,
            "water_meter_request_create_date": self.water_meter_request_create_date,
        }
