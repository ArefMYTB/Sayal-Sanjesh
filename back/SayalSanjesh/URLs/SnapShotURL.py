from django.urls import path
from SayalSanjesh.Views.SnapShotView import SnapShotView

snap_shot_view = SnapShotView()
urlpatterns = [
    # ------------------------------------------------- Meter Urls -----------------------------------------------------
    # Admin apies
    path('admin/getAll', snap_shot_view.admin_get_all_snap_shots_view),
]