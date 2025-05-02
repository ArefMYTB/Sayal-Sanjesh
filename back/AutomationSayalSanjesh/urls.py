"""AutomationSayalSanjesh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from SayalSanjesh.URLs import NoticeCategoriesURLs, NoticeURLs, WaterMeterURL, SnapShotURL, BillsURL, \
    WaterMeterTypesURL, WaterMeterProjectsURL, WaterMeterTagsURL, WaterMeterModulesURL, \
    WaterMeterRequestsURL, CalculateUnitsURL, CitiesURLs, EventTypeURLs, EventURLs, PattrenURLs, \
    SendDataURLs, OrderTypeURLS, OrderURLS , ModuleType
from Authorization.URLs import AdminsURLs, MiddleAdminsURLs, UserURLs, StaticTokenURLs, PermissionURLs, \
    PermissionCategoryURLs
from General.URLs import UploadURLs, AppURLs ,LogURLs
from django.contrib import admin
from django.conf import settings
from SayalSanjesh.URLs.templateUrls import BillsTemplateURL
from django.views.static import serve

urlpatterns = [
    path('admins/', include(AdminsURLs)),
    path('users/', include(UserURLs)),
    path('categories/', include(NoticeCategoriesURLs)),
    path('notice/', include(NoticeURLs)),
    path('watermeters/', include(WaterMeterURL)),
    path('snapshots/', include(SnapShotURL)), # برداشت ها
    path('bills/', include(BillsURL)),
    path('WaterMeterTypes/', include(WaterMeterTypesURL)),
    path('WaterMeterTags/', include(WaterMeterTagsURL)),
    path('WaterMeterProjectsURL/', include(WaterMeterProjectsURL)),
    path('DjangoAdmin/', admin.site.urls),
    path('statictoken/', include(StaticTokenURLs)),
    path('WaterMeterModules/', include(WaterMeterModulesURL)),
    path('WaterMeterRequests/', include(WaterMeterRequestsURL)),
    path('middle/', include(MiddleAdminsURLs)),
    path('calculate/unit/', include(CalculateUnitsURL)),
    path('city/', include(CitiesURLs)),
    path('EventType/', include(EventTypeURLs)),
    path('Event/', include(EventURLs)),
    path('Templates/Bill/', include(BillsTemplateURL)),
    path('Pattern/', include(PattrenURLs)),
    path('Updload/', include(UploadURLs)),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('Data/', include(SendDataURLs)),
    path('OrderType/', include(OrderTypeURLS)),
    path('Order/', include(OrderURLS)),
    path('Apps/', include(AppURLs)),
    path('Permissions/', include(PermissionURLs)),
    path('PermissionCategory/', include(PermissionCategoryURLs)),
    path('Log/', include(LogURLs)),
    path('ModuleType/', include(ModuleType)),
]
