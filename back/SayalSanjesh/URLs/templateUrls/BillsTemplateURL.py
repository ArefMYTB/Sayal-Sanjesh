from django.urls import path
from SayalSanjesh.TemplateView.views import bill

# bill_view = bill()
urlpatterns = [
    path('<bill_id>/<random_token>', bill),
]
