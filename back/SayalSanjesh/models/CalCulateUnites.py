import uuid
from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from Authorization.models.Admins import Admins

# Create your models here.


class CalculateUnites(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    calculate_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calculate_unites = models.JSONField()
    calculate_water_meter = models.ForeignKey('WaterMeters', on_delete=CASCADE)
    calculate_create_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'CalculateUnites'

    def as_dict(self):
        water_meter_type_info = {
            "water_meter_type_name": self.calculate_water_meter.water_meter_type.water_meter_type_name,
            "water_meter_type_id": self.calculate_water_meter.water_meter_type.water_meter_type_id,
        }
        water_meter_info = {
            "water_meter_serial": self.calculate_water_meter.water_meter_serial,
            "water_meter_type_info": water_meter_type_info,
        }
        return {
            "admin": self.admin.as_dict()['admin_id'],
            "calculate_id": self.calculate_id,
            "calculate_unites": self.calculate_unites,
            "calculate_create_date": self.calculate_create_date,
            "water_meter_info": water_meter_info
        }
