import uuid
from datetime import datetime
from django.db import models


# Create your models here.

class StaticToken(models.Model):
    token_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_name = models.CharField(max_length=200)
    token = models.TextField()
    create_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'StaticToken'

    def as_dict(self):
        return {
            "token_id": self.token_id,
            "token_name": self.token_name,
            "token": self.token,
            "create_time": self.create_time
        }
