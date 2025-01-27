from django.urls import path
from SayalSanjesh.Views.ModuleTypeView import ModuleTypesView

module_types = ModuleTypesView()

urlpatterns = [
    path('admin/add', module_types.admin_add_module_type_view),
    path('admin/edit', module_types.admin_edit_module_type_view),
    path('admin/delete', module_types.admin_delete_module_type_view),
    path('admin/getAll', module_types.admin_get_all_module_type_view),
    path('admin/getOne', module_types.admin_get_one_module_type_view),

    # path('user/getAll', module_types.user_get_all_module_type_view),
    # path('user/getOne', module_types.user_get_one_module_type_view),
    # path('v2/user/getAll', module_types.user_get_all_module_type_view_v2),
    # path('v2/user/getOne', module_types.user_get_one_module_type_view_v2),
]
