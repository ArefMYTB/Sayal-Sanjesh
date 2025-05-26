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
    WaterMeterRequestsURL, EventTypeURLs, EventURLs, PattrenURLs, \
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

# New Permissions
# Self: Everybody
# Admin
# ProjectManager
# Joker: Edit other admins, Edit&Delete Projects&Devices
# CRUDProject: Joker in back
# ViewProject: View Project Details (like number/types of devices) - Admin&ProjectManager
# ClearDeviceData: Clearing Device Consumption Data & Events - Admin
# ViewUser: View End Users - Admin&ProjectManager&Financial (also a lower lever project manager)
# CRUDUser: CreateReadUpdateDeleteUser - Admin&ProjectManager (also a lower lever project manager)
# CRUDManager: CreateReadUpdateDeleteManager - Joker&ProjectManager
# ViewAdmin: View All Admins - Admin
# CRUDAdmin: CreateReadUpdateDeleteAdmin - Joker
# Store: Store Management - Admin
# ViewDevice: View Device Details & Consumption - Admin&ProjectManager&User
# CRUDDevice: CreateReadUpdateDeleteDevice - Joker
# BillManaging: View&Create Bills - ProjectManager (also a lower lever project manager like Financial)
# Reports: View System Report Tab - Admin&ProjectManager (also a lower lever project manager)
# LogDevice: View Device Data Logs - Admin
# LogSystem: View System Logs - Joker
# OrderManaging: Order Devices to Do Something - Joker&ProjectManager&User (also a lower lever project manager) - But They Must be prioritized.
# Settings - Managing All System Settings - Admin
# Verification - Managin Verification - Admin


# New User Types
# Joker: Developer&Ansari 
# Admin: Sayal Sanjesh employees 
# ProjectManager: Project Managers
# User:
# Financial:


