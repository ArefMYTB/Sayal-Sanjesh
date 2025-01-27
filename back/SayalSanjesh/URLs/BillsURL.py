from django.urls import path
from SayalSanjesh.Views.BillsView import BillsView

bill_view = BillsView()
urlpatterns = [
    path('admin/getAll', bill_view.admin_get_all_bills),
    path('admin/getOne', bill_view.admin_get_one_bill),
    path('admin/editBill', bill_view.admin_edit_bill),
    path('admin/removeBill', bill_view.admin_remove_bill),
    path('admin/createBill', bill_view.admin_create_new_bill),
    path('admin/createBill/v1', bill_view.admin_create_new_bill_v1),
    path('user/getOne', bill_view.user_get_one_bill),
    path('user/getAll', bill_view.user_get_all_bills),
    path('user/creatLink', bill_view.user_create_link),
    path('user/getLink', bill_view.user_get_link),
    # admin create bill from exel file
    path('admin/createbill/excel', bill_view.admin_create_exel_view),
    path('admin/create/power/excel', bill_view.admin_create_power_exel_view),
    # end admin create bill from exel file

    # bill for list
    path('admin/createBill/list', bill_view.admin_create_new_bill_list),
    # general get one api
    path('getOne', bill_view.get_one_bill),
]