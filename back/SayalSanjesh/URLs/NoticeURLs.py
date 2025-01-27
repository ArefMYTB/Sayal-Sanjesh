from django.urls import path
from SayalSanjesh.Views.NoticeView import NoticeView

notice = NoticeView()
urlpatterns = [
    path('admin/getone', notice.admin_get_one_notice),
    path('admin/getall', notice.admin_get_all_notice),
    path('admin/getSelves', notice.admin_get_my_notice),
    path('admin/replay', notice.admin_replay_notice),
    path('user/create', notice.user_create_notice),
    path('user/replay', notice.user_replay_notice),
    path('user/getSelves', notice.user_get_my_notice),
    path('user/getOne', notice.user_get_one_notice),
    path('user/getAll', notice.user_get_all_notice),
]
