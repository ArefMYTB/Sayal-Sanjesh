import uuid
from datetime import datetime
from django.db import models
from Authorization.models.Admins import Admins
from django.core import exceptions
from django.db import (
    transaction
)
from django.db.models import sql
from django.db.models.sql.constants import CURSOR
from .Permissions import Permissions


# Create your models here.

# --------------------------------------------------Permission----------------------------------------------------------
class CustomPermissionCategoryManager(models.Manager):
    def create(self, **kwargs):
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def update(self, **kwargs):
        """
        Update all elements in the current QuerySet, setting all the given
        fields to the appropriate values.
        """
        self._not_support_combined_queries("update")
        if self.query.is_sliced:
            raise TypeError("Cannot update a query once a slice has been taken.")
        self._for_write = True
        query = self.query.chain(sql.UpdateQuery)
        query.add_update_values(kwargs)

        # Inline annotations in order_by(), if possible.
        new_order_by = []
        for col in query.order_by:
            if annotation := query.annotations.get(col):
                if getattr(annotation, "contains_aggregate", False):
                    raise exceptions.FieldError(
                        f"Cannot update when ordering by an aggregate: {annotation}"
                    )
                new_order_by.append(annotation)
            else:
                new_order_by.append(col)
        query.order_by = tuple(new_order_by)

        # Clear any annotations so that they won't be present in subqueries.
        query.annotations = {}
        with transaction.mark_for_rollback_on_error(using=self.db):
            rows = query.get_compiler(self.db).execute_sql(CURSOR)
        self._result_cache = None
        return rows

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        all_permission_category_numbers = PermissionCategory.objects.count()
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "admin": {
                    "admin_id": obj.admin.admin_id,
                    "admin_name": obj.admin.admin_name,
                    "admin_lastname": obj.admin.admin_lastname,
                    "admin_phone": obj.admin.admin_phone,
                    "other_information": obj.admin.other_information,
                },
                "permission_category_id": obj.permission_category_id,
                "permission_category_persian_name": obj.permission_category_persian_name,
                "permission_category_english_name": obj.permission_category_english_name,
                "permission_category_description": obj.permission_category_description,
                "permission_category_create_date": obj.permission_category_create_date,
                "permissions_with_this_category": list(obj.permissions.values(
                    'permission_id', 'permission_english_name', 'permission_persian_name')),
                "permission_numbers_with_this_category": obj.permissions.count()
            }
            if hasattr(queryset, '__iter__') is True:
                serialized_obj['all_permission_category_numbers'] = all_permission_category_numbers
            serialized_data.append(serialized_obj)
        return serialized_data


class PermissionCategory(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    permission_category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_category_persian_name = models.CharField(max_length=200, null=True)
    permission_category_english_name = models.CharField(max_length=200, unique=True)
    permission_category_description = models.TextField(null=True)
    permission_category_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    permissions = models.ManyToManyField(Permissions)
    objects = CustomPermissionCategoryManager()

    class Meta:
        db_table = 'PermissionCategory'
    def __str__(self):
        return self.permission_category_english_name
# ----------------------------------------------------------------------------------------------------------------------
