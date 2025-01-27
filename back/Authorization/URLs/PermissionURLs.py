from django.urls import path
from Authorization.Views.PermissionViews import PermissionViews

permissions_view = PermissionViews()

urlpatterns = [
    path('admin/create', permissions_view.admin_create_permission_view),
    path('admin/edit', permissions_view.admin_edit_permission_view),
    path('admin/delete', permissions_view.admin_delete_permission_view),
    path('admin/getAll', permissions_view.admin_get_all_permission_view),
]


