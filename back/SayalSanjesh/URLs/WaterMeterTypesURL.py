from django.urls import path
from SayalSanjesh.Views.WaterMeterTypesView import WaterMeterTypesView

water_meter_types = WaterMeterTypesView()

urlpatterns = [
    path('admin/add', water_meter_types.admin_add_water_meter_type),
    path('admin/edit', water_meter_types.admin_edit_water_meter_project),
    path('admin/delete', water_meter_types.admin_delete_water_meter_project),
    path('admin/getAll', water_meter_types.admin_get_all_water_meter_categories),
    path('admin/getOne', water_meter_types.admin_get_one_water_meter_type),
    path('admin/getAllValues', water_meter_types.admin_get_all_water_meter_type_sort_by_values_view),
    path('admin/total/statistics', water_meter_types.admin_total_statistics_view),
    path('user/getAll', water_meter_types.user_get_all_water_meter_categories),
    path('user/getOne', water_meter_types.user_get_one_water_meter_project),
    path('v2/user/getAll', water_meter_types.user_get_all_water_meter_categories_v2),
    path('v2/user/getOne', water_meter_types.user_get_one_water_meter_project_v2),

]
