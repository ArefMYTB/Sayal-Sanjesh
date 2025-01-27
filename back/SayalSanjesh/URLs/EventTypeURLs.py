from django.urls import path
from SayalSanjesh.Views.EventTypeView import EventTypeView

event_type_view = EventTypeView()
urlpatterns = [
    path('admin/getAll', event_type_view.admin_get_all_event_type_view),
    path('admin/getOne', event_type_view.admin_get_one_event_type_view),
    path('admin/create', event_type_view.admin_create_event_type_view),
    path('admin/edit', event_type_view.admin_edit_event_type_view),
    path('admin/delete', event_type_view.admin_remove_event_type_view),
]