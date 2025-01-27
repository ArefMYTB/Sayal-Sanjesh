from django.urls import path
from SayalSanjesh.Views.OrderTypeView import OrderTypeView

order_type_view = OrderTypeView()
urlpatterns = [
    path('admin/getAll', order_type_view.admin_get_all_order_type_view),
    path('admin/getOne', order_type_view.admin_get_one_order_type_view),
    path('admin/create', order_type_view.admin_create_order_type_view),
    path('admin/delete', order_type_view.admin_remove_order_type_view),
]