import uuid
from django.db import models
from datetime import datetime
from Authorization.models.Admins import Admins
from SayalSanjesh.models.Meters import WaterMeters

class Snapshots(models.Model):
    snapshot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    snapshot_watermeter = models.ForeignKey(WaterMeters, on_delete=models.CASCADE)
    snapshot_admin = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
    snapshot_create_time = models.DateTimeField(default=datetime.now, blank=True)
    snapshot_mechanic_value = models.FloatField(default=0.0)
    snapshot_cumulative_value = models.FloatField(default=0.0)

    class Meta:
        db_table = 'Snapshots'
        indexes = [
            models.Index(fields=['snapshot_create_time', 'snapshot_watermeter']),
        ]

    def as_dict(self):
        return {
            "watermeter": self.snapshot_watermeter,
            "admin": self.snapshot_admin,
            "create_time": self.snapshot_create_time,
            "mechanic_value": self.snapshot_mechanic_value,
            "cumulative_value": self.snapshot_cumulative_value,
        }
