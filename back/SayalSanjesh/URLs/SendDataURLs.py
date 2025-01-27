from django.urls import path
from SayalSanjesh.Views.SendDataView import DataView

data_view = DataView()
urlpatterns = [
    path('admin/send', data_view.admin_send_data_view),
    # path('admin/order/sms', data_view.admin_send_data_view),
]