from django.urls import path
from Authorization.Views.AdminsView import AdminsView

admins_view = AdminsView()

urlpatterns = [
    path('admin/login', admins_view.login_admin),
    path('admin/setProfile', admins_view.admin_set_profile),
    path('admin/getProfile', admins_view.admin_get_profile),
    path('admin/getOne', admins_view.admin_get_one_admin),
    path('admin/changePassword', admins_view.admin_change_password),
    path('admin/add', admins_view.admin_create_new_admin),
    path('admin/getAll', admins_view.admin_get_all_admins),
    path('admin/edit', admins_view.admin_edit_other_admin),
    path('admin/remove', admins_view.admin_remove_other_admin),
    path('admin/getAll/files', admins_view.admin_get_all_own_file_view),
    path('admin/delete/file', admins_view.admin_delete_admin_files_view),
    path('admin/checkValidation', admins_view.admin_check_phone_number_validation_view),
    path('admin/set/categoty/permissions', admins_view.admin_set_category_permission_view),
    path('admin/set/permissions', admins_view.admin_set_permission_view),
    path('admin/logout', admins_view.logout_admin),

]
