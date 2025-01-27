from django.contrib import admin
from Authorization.models.Admins import Admins
from Authorization.models.Permissions import Permissions
from Authorization.models.PermissionCategory import PermissionCategory
# Register your models here.
admin.site.register(Admins)
admin.site.register(Permissions)
admin.site.register(PermissionCategory)