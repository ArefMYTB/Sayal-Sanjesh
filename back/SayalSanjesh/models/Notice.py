import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.deletion import CASCADE
from Authorization.models.Users import Users

from Authorization.models.Admins import Admins


# Create your models here.

class NoticeCategories(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=200)
    category_index = models.IntegerField()
    create_date = models.DateTimeField(
        default=datetime.now, blank=True)

    class Meta:
        db_table = 'NoticeCategories'

    def as_dict(self):
        return {
            "admin_info": self.admin.as_dict(),
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_index": self.category_index,
            "create_date": self.create_date
        }


class Notice(models.Model):
    notice_category = models.ForeignKey(
        NoticeCategories, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=CASCADE)
    notice_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    notice_files = ArrayField(models.JSONField(blank=True), default=list)
    attachment = models.JSONField()

    class Meta:
        db_table = 'Notice'

    def as_dict(self):
        return {
            "notice_category_info": self.notice_category.as_dict(),
            "user_info": self.user.as_dict(),
            "notice_id": self.notice_id,
            "title": self.title,
            "message": self.message,
            "create_date": self.create_date,
            "attachment": self.attachment,
            "notice_files": self.notice_files
        }


class NoticeReplayAdmin(models.Model):
    replay_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    notice = models.ForeignKey(Notice, on_delete=CASCADE)
    admin = models.ForeignKey(Admins, on_delete=CASCADE)
    message = models.CharField(max_length=200)
    create_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'NoticeReplayAdmin'

    def as_dict(self):
        return {
            "notice_info": self.notice.as_dict(),
            "admin_info": self.admin.as_dict(),
            "message": self.message,
            "create_time": self.create_time
        }


class NoticeReplayUser(models.Model):
    replay_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notice = models.ForeignKey(Notice, on_delete=CASCADE)
    user = models.ForeignKey(Users, on_delete=CASCADE)
    message = models.CharField(max_length=200)
    create_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'NoticeReplayUser'

    def as_dict(self):
        return {
            "notice_ifo": self.notice.as_dict(),
            "user_info": self.user.as_dict(),
            "message": self.message,
            "create_time": self.create_time
        }
