from django.urls import path
from SayalSanjesh.Views.WaterMeterProjectsView import WaterMeterProjectView

water_meter_projects = WaterMeterProjectView()
urlpatterns = [
    path('admin/add', water_meter_projects.admin_add_water_meter_project_view),
    path('admin/addType', water_meter_projects.admin_add_type_too_project_view),
    path('admin/edit', water_meter_projects.admin_edit_water_meter_project_view),
    path('admin/delete', water_meter_projects.admin_delete_water_meter_project_view),
    path('admin/getAll', water_meter_projects.admin_get_all_water_meter_projects_view),
    path('admin/getAll/city/count', water_meter_projects.admin_get_all_water_meter_projects_city_count_view),
    path('admin/total/statistics', water_meter_projects.admin_total_statistics_view),
    path('admin/getOne', water_meter_projects.admin_get_one_water_meter_project_view),
    path('user/getAll', water_meter_projects.user_get_all_water_meter_projects_view),
    path('user/getOne', water_meter_projects.user_get_one_water_meter_project_view),

    path('v2/user/getAll', water_meter_projects.user_get_all_water_meter_projects_view_v2),
    path('v2/user/getOne', water_meter_projects.user_get_one_water_meter_project_view_v2),

]
