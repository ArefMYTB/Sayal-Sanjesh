from django.urls import path
from Authorization.Views.UsersView import UsersView

user_view = UsersView()

urlpatterns = [
    path('user/login', user_view.login_user),
    path('user/checkValidation', user_view.user_check_phone_number_validation_view),
    path('admin/add', user_view.admin_create_new_user, name='guest'),
    path('user/getProfile', user_view.user_get_profile),
    path('admin/getAllUsers', user_view.admin_get_all_users),
    path('admin/getOneUser', user_view.admin_get_one_user),
    path('admin/changeUserProfile', user_view.admin_change_user_profile),
    path('user/editProfile', user_view.user_edit_profile),
    path('user/changePass', user_view.user_change_password),
    path('admin/delete', user_view.admin_delete_user_view),

]
