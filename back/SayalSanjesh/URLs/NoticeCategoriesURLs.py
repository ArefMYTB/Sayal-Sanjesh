from django.urls import path
from SayalSanjesh.Views.NoticeCategoriesView import NoticeCategoriesView

noticecategories = NoticeCategoriesView()
urlpatterns = [
    path('admin/add', noticecategories.admin_add_notice_category),
    path('admin/edit', noticecategories.admin_edit_notice_category),
    path('admin/delete', noticecategories.admin_delete_notice_category),
    path('admin/getAll', noticecategories.admin_get_all_notice_categories),
    path('user/getAll', noticecategories.user_get_all_notice_categories),
    path('user/getOne', noticecategories.user_get_one_notice_category_view),
]
