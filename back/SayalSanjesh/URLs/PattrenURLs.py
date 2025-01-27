from django.urls import path
from SayalSanjesh.Views.PatternView import PatternView

pattern_view = PatternView()
urlpatterns = [
    path('admin/create', pattern_view.admin_create_pattern_view),
    path('admin/edit', pattern_view.admin_edit_pattern_view),
    path('admin/delete', pattern_view.admin_delete_pattern_view),
    path('admin/getAll', pattern_view.admin_get_all_pattern_view),
    path('admin/getOne', pattern_view.admin_get_one_pattern_view),
]