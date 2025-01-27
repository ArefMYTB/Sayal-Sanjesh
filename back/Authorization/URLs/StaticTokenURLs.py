from django.urls import path
from Authorization.Views.StaticTokenView import StaticTokenView

static_token = StaticTokenView()

urlpatterns = [
    path('admin/add', static_token.add_static_token_view),
]
