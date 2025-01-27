from django.urls import path
from SayalSanjesh.Views.UsersView import UsersView

user_view = UsersView()

urlpatterns = [
    path('guest/login', user_view.login_guest, name='guest'),
    path('admin/add', user_view.admin_create_new_user, name='guest'),
    path('user/getProfile', user_view.user_get_profile),
    path('admin/getAllUsers', user_view.admin_get_all_users),
    path('admin/getOneUser', user_view.admin_get_one_user),
    path('admin/changeUserProfile', user_view.admin_change_user_profile),
]
