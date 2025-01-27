from django.urls import path
from SayalSanjesh.Views.WaterMeterModulesView import WaterMeterModulesView

water_meter_projects = WaterMeterModulesView()

urlpatterns = [
    path('admin/add', water_meter_projects.admin_add_water_meter_module_view),
    path('admin/addRequest', water_meter_projects.admin_add_request_too_water_meter_module_view),
    path('admin/edit', water_meter_projects.admin_edit_water_meter_module_view),
    path('admin/delete', water_meter_projects.admin_delete_water_meter_module_view),
    path('admin/getAll', water_meter_projects.admin_get_all_water_meter_modules_view),
    path('admin/getOne', water_meter_projects.admin_get_one_water_meter_module_view),
]
