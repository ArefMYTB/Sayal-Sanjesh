from django.urls import path
from SayalSanjesh.Views.CitiesView import citiesView

city = citiesView()
urlpatterns = [
    path('admin/create', city.admin_create_city_view),
    path('admin/edit', city.admin_edit_city_view),
    path('admin/delete', city.admin_delete_city_view),
    path('admin/getAll', city.admin_get_all_cities_view),
    path('admin/getOne', city.admin_get_one_city_view),
]
