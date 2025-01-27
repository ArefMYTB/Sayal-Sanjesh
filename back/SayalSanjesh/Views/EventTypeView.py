from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.EventTypeSerializer import EventTypeSerializer


@csrf_exempt
class EventTypeView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """
    @csrf_exempt
    def admin_get_all_event_type_view(self, request):
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
        fields = ["page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]

        result, data = EventTypeSerializer.admin_get_all_event_types_serializer(token=token, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_event_type_view(self, request):
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
        fields = ["event_type_id", "event_type_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_type_id = input_data['event_type_id']
        event_type_code = input_data['event_type_code']
        result, data = EventTypeSerializer.admin_get_one_event_type_serializer(
            token=token, event_type_id=event_type_id, event_type_code=event_type_code)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_event_type_view(self, request):
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
        fields = ["event_type_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_type_id = input_data['event_type_id']

        result, data = EventTypeSerializer.admin_remove_event_type_serializer(
            token=token, event_type_id=event_type_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_event_type_view(self, request):
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
        fields = ['event_type_keyword', 'event_type_importance', 'evnet_type_information', ]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_type_keyword = input_data["event_type_keyword"]
        event_type_importance = input_data["event_type_importance"]
        evnet_type_information = input_data["evnet_type_information"]
        result, data = EventTypeSerializer.admin_create_event_type_serializer(
            token=token,  event_type_keyword=event_type_keyword,
            event_type_importance=event_type_importance, evnet_type_information=evnet_type_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_event_type_view(self, request):
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
        fields = ['event_type_id','event_type_dashboard_view', 'event_type_importance', 'evnet_type_information']
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_type_id = input_data["event_type_id"]
        event_type_dashboard_view = input_data["event_type_dashboard_view"]
        event_type_importance = input_data["event_type_importance"]
        evnet_type_information = input_data["evnet_type_information"]
        result, data = EventTypeSerializer.admin_edit_event_type_serializer(
            token=token, event_type_id=event_type_id,event_type_dashboard_view=event_type_dashboard_view,
            event_type_importance=event_type_importance, evnet_type_information=evnet_type_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])