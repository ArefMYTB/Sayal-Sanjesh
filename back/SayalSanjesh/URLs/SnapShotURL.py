from django.urls import path
from SayalSanjesh.Views.SnapShotView import SnapShotView

snap_shot_view = SnapShotView()
urlpatterns = [
    # ------------------------------------------------- Meter Urls -----------------------------------------------------
    # Admin apies
    path('admin/create', snap_shot_view.admin_create_snap_shot_view),
    path('admin/edit', snap_shot_view.admin_edit_snap_shot_view),
    path('admin/delete', snap_shot_view.admin_remove_snap_shot_view),
    path('admin/getAll', snap_shot_view.admin_get_all_snap_shots_view),
    path('admin/upload', snap_shot_view.admin_upload_snap_shot_view),
]