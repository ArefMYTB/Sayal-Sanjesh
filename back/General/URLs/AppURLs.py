from django.urls import path
from General.Views.AppViews import AppViews

app_view = AppViews()
urlpatterns = [
    # path('admin/get/app', app_view.admin_get_app_view),
    path('get/app', app_view.get_app_view),
    path('admin/delete/app', app_view.admin_delete_app_view),
    path('admin/add/app', app_view.admin_add_app_view),
    # path('user/get/app', app_view.user_get_app_view),

]

