from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from General.Serializers.LogSerializers import LogSerializers


@csrf_exempt
class LogViews:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """

    # -------------------------------------------------MqttLoger--------------------------------------------------------
    @csrf_exempt
    def admin_get_all_mqtt_log_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "message__icontains"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data['page']
        count = input_data['count']
        message__icontains = input_data['message__icontains']
        topic_name__icontains = input_data['topic_name']
        result, data = LogSerializers.admin_get_all_mqtt_log_serializer(
            token=token, page=page, count=count, message__icontains=message__icontains, topic_name__icontains=topic_name__icontains)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    # ------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------SystemLog--------------------------------------------------------
    @csrf_exempt
    def system_log_create_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["system_log_action", "system_log_message"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'system_log_admin' not in input_data:
            system_log_admin = None
        else:
            system_log_admin = input_data['system_log_admin']
        if 'system_log_user' not in input_data:
            system_log_user = None
        else:
            system_log_user = input_data['system_log_user']
        system_log_action = input_data['system_log_action']
        system_log_message = input_data['system_log_message']
        system_log_object_action_on = input_data['system_log_object_action_on']
        system_log_action_table = input_data['system_log_action_table']
        system_log_field_changes = input_data['system_log_field_changes']
        result, data = LogSerializers.system_log_create_serializer(token=token, system_log_admin=system_log_admin,
                                                                   system_log_user=system_log_user,
                                                                   system_log_action=system_log_action,
                                                                   system_log_message=system_log_message,
                                                                   system_log_action_table=system_log_action_table,
                                                                   system_log_field_changes=system_log_field_changes,
                                                                   system_log_object_action_on=system_log_object_action_on)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_system_log_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "system_log_action", "system_log_object_action_on__search",
                  "system_log_action_table"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        system_log_action = input_data["system_log_action"]
        system_log_object_action_on__search = input_data["system_log_object_action_on__search"]
        system_log_action_table = input_data["system_log_action_table"]

        result, data = LogSerializers.admin_get_all_system_log_view(
            token=token, page=page, count=count, system_log_action=system_log_action,
            system_log_object_action_on__search=system_log_object_action_on__search,
            system_log_action_table=system_log_action_table)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
    # ------------------------------------------------------------------------------------------------------------------
