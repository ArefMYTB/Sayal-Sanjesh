from django.urls import path
from SayalSanjesh.Views.CalculateUnitesView import CalculateUnitesView

calculate_units = CalculateUnitesView()

urlpatterns = [
    path('admin/add', calculate_units.admin_add_calculate_unites_view),
    path('admin/delete', calculate_units.admin_delete_calculate_unites_view),
    path('admin/getAll', calculate_units.admin_get_all_calculate_price_view),
]
