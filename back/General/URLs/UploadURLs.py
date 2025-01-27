from django.urls import path
from General.Views.UploadView import UploadView

upload_view = UploadView()
urlpatterns = [
    path('admin', upload_view.admin_upload_file_view),
    # path('user', upload_view.admin_upload_file)
]