from django.urls import path
from SayalSanjesh.Views.OrderView import OrderView

order_view = OrderView()
urlpatterns = [
    path('admin/getAll', order_view.admin_get_all_order_view),
    path('admin/getOne', order_view.admin_get_one_order_view),
    path('admin/create', order_view.create_order_view),
    path('admin/delete', order_view.admin_remove_order_view),
]
