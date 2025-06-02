from django.urls import path
from SayalSanjesh.Views.WaterMeterView import WaterMeterView
from SayalSanjesh.Views.ConsumptionView import ConsumptionView

water_meter_view = WaterMeterView()
consumption_view = ConsumptionView()
urlpatterns = [
    # ------------------------------------------------- Meter Urls -----------------------------------------------------
    # Admin apies
    path('admin/create', water_meter_view.admin_create_water_meter_view),
    path('admin/remove', water_meter_view.admin_remove_water_meter_view),
    path('admin/smartRemove', water_meter_view.admin_remove_smart_water_meter_view),
    path('admin/edit', water_meter_view.admin_edit_water_meter_view),
    path('admin/getAllFilter', water_meter_view.admin_get_all_water_meters_by_filter_view),
    path('admin/getAll', water_meter_view.admin_get_all_water_meters_view),
    path('admin/assign/user', water_meter_view.admin_assign_user_to_water_meter_view),
    path('v2/admin/getAll', water_meter_view.v2_admin_get_all_water_meters_view),
    path('admin/getOne', water_meter_view.admin_get_one_water_meter_view),
    path('admin/countAll', water_meter_view.admin_count_all_water_meter_view),
    path('admin/getlocations', water_meter_view.admin_get_location_view),    
    path('admin/assignUser', water_meter_view.admin_assign_user_view),    
    # End admin apies .

    # User apies
    path('user/getOne', water_meter_view.user_get_one_water_meter_view),
    path('user/getAll', water_meter_view.user_get_all_water_meters_view),
    path('user/countAll', water_meter_view.user_count_all_water_meter_view),
    path('user/countAll/filter', water_meter_view.user_count_all_by_filters_water_meter_view),
    path('v2/user/getOne', water_meter_view.user_get_one_water_meter_view_v2),
    path('v2/user/getAll', water_meter_view.user_get_all_water_meters_view_v2),
    # End user apies

    # middle admin api
    path('admin/countAll/filter', water_meter_view.admin_count_all_by_filters_water_meter_view),

    # this api is only use for test
    path('test/edit', water_meter_view.admin_edit_value_water_meter_view),
    # -----------------------------------------------------------------------------------------------------------------

    # ------------------------------------------ consumption Urls -----------------------------------------------------
    # Admin apies
    path('admin/getOne/consumption', consumption_view.admin_get_one_consumption_view),
    path('admin/getAll/consumption', consumption_view.admin_get_all_consumptions_view),
    path('admin/getAll/consumption/date', consumption_view.admin_get_all_consumptions_by_date_view),
    path('admin/getAll/consumption/chart', consumption_view.admin_get_all_consumptions_by_date_for_chart_view),
    path('admin/getAll/consumption/date/meter', consumption_view.admin_get_all_consumptions_by_date__per_meter_view),
    path('admin/getAll/consumption/date/app', consumption_view.admin_get_all_consumptions_by_date_app_view),
    path('admin/delete/consumption', consumption_view.admin_remove_consumption_view),
    path('admin/edit/consumption', consumption_view.admin_edit_consumption_view),
    path('admin/cumulative/consumption', consumption_view.admin_get_cumulative_consumptions_view),
    path('admin/getLast/consumption', consumption_view.admin_get_last_consumption_data_by_water_meter_view),
    path('admin/countAll/consumptionValues', consumption_view.admin_get_all_all_water_meter_consumption_view),
    path('admin/consumption/total/statistics', consumption_view.admin_consumption_total_statistics_view),
    path('v2/admin/cumulative/consumption', consumption_view.v2_admin_get_cumulative_consumptions_view),
    path('admin/cumulative/consumption/tag', consumption_view.admin_get_cumulative_consumptions_per_tag_view),
    path('admin/create/csv/overall', consumption_view.admin_create_csv_file_overall_view),
    path('admin/create/csv/single', consumption_view.admin_create_csv_file_single_view),
    path('admin/create/csv/all', consumption_view.admin_create_csv_file_all_view),
    path('admin/getOne/csv', consumption_view.admin_get_one_csv_file_view),
    path('admin/update/sumValue', consumption_view.admin_update_sum_value_view),
    # End Admin apies .

    # Add apies
    path('add/consumption', consumption_view.add_consumptions_water_meter_view),
    path('v1/add/consumption', consumption_view.v1_add_consumptions_water_meter_view),
    path('v2/add/consumption', consumption_view.v2_add_consumptions_water_meter_view),
    path('add/levelGauge/consumption', consumption_view.add_level_gauge_consumptions_water_meter_view),
    # End Add apies .

    # User apies
    path('user/cumulative/consumption', consumption_view.user_get_cumulative_consumptions_per_tag_view),
    path('user/getAll/consumption', consumption_view.user_get_all_consumptions_view),
    path('user/getAll/consumption/date', consumption_view.user_get_all_consumptions_by_date_view),
    path('user/getLast/consumption', consumption_view.user_get_last_consumption_data_by_water_meter_view),
    path('user/getOne/consumption', consumption_view.user_get_one_consumptions_view),
    # End User apies .
    # -----------------------------------------------------------------------------------------------------------------
]
