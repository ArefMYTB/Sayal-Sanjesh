from django.urls import path
from General.Views.LogViews import LogViews

log_view = LogViews()
urlpatterns = [
    # -------------------------------------------------MqttLoger--------------------------------------------------------
    path('admin/mqttLog/getAll', log_view.admin_get_all_mqtt_log_view),
    # ------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------SystemLog--------------------------------------------------------
    path('sysetem/log/create', log_view.system_log_create_view),
    path('admin/sysetem/log/getAll', log_view.admin_get_all_system_log_view),
    # ------------------------------------------------------------------------------------------------------------------

]
