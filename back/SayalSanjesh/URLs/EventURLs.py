from django.urls import path
from SayalSanjesh.Views.EventView import EventView

event_view = EventView()
urlpatterns = [
    path('admin/getAll', event_view.admin_get_all_event_view),
    path('admin/getOne', event_view.admin_get_one_event_view),
    path('admin/create', event_view.create_event_view),
    path('admin/delete', event_view.admin_remove_event_view),
    path('admin/delete/all', event_view.admin_remove_all_event_view),

]