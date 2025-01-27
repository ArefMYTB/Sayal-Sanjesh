from django.urls import path
from SayalSanjesh.Views.WaterMeterRequestsView import WaterMeterRequestsView

water_meter_requests = WaterMeterRequestsView()

urlpatterns = [
    path('admin/add', water_meter_requests.admin_add_water_meter_request_view),
    path('admin/edit', water_meter_requests.admin_edit_water_meter_request_view),
    path('admin/delete', water_meter_requests.admin_delete_water_meter_request_view),
    path('admin/getAll', water_meter_requests.admin_get_all_water_meter_request_view),
    path('admin/getOne', water_meter_requests.admin_get_one_water_meter_request_view),
]
