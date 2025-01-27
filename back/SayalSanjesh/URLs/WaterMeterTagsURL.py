from django.urls import path
from SayalSanjesh.Views.WaterMeterTagsView import WaterMeterTagsView

water_meter_tags = WaterMeterTagsView()

urlpatterns = [
    path('admin/add', water_meter_tags.admin_add_water_meter_tag),
    path('admin/delete', water_meter_tags.admin_delete_water_meter_tag_view),
    path('admin/getAll', water_meter_tags.admin_get_all_water_meter_tags_view),
    path('admin/total/statistcs', water_meter_tags.admin_total_statists_tags_view),
    path('user/getAll', water_meter_tags.user_get_all_water_meter_tags_view),


]
