from django.urls import path
from Authorization.Views.MiddleAdminsView import MiddleAdminsView

middle_admins_view = MiddleAdminsView()

urlpatterns = [
    path('admin/add/data', middle_admins_view.add_middle_admin_data_view),
    path('admin/edit/data', middle_admins_view.edit_middle_admin_data_view),
    path('admin/getAll', middle_admins_view.admin_get_all_middle_admin_view),
    path('admin/getOne', middle_admins_view.admin_get_one_middle_admin_view),
    path('getAll/users', middle_admins_view.middle_admin_get_all_users_view),

]
