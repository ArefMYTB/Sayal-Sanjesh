import uuid
from django.db import models


# Create your models here.


class Utils(models.Model):
    utils_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, max_length=255)
    information = models.JSONField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Utils'
