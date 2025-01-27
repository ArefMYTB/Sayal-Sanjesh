from django.urls import path
from Authorization.Views.PermissionCategoryViews import PermissionCategoryViews

permission_category_views = PermissionCategoryViews()

urlpatterns = [
    path('admin/create', permission_category_views.admin_create_permission_category_view),
    path('admin/edit', permission_category_views.admin_edit_permission_category_view),
    path('admin/delete', permission_category_views.admin_delete_permission_category_view),
    path('admin/getAll', permission_category_views.admin_get_all_permission_category_view),
]
