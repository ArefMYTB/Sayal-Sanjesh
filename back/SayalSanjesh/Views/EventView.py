from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.EventSerializer import EventSerializer


@csrf_exempt
class EventView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """

    @csrf_exempt
    def admin_get_all_event_view(self, request):
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
        fields = ["page", "count", "module_id", "module_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        module_id = input_data["module_id"]
        module_code = input_data["module_code"]

        result, data = EventSerializer.admin_get_all_event_serializer(token=token, page=page, count=count,
                                                                      module_id=module_id, module_code=module_code)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_event_view(self, request):
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
        fields = ["event_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_id = input_data['event_id']
        result, data = EventSerializer.admin_get_one_event_serializer(
            token=token, event_id=event_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_event_view(self, request):
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
        fields = ["event_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_id = input_data['event_id']

        result, data = EventSerializer.admin_remove_event_serializer(
            token=token, event_id=event_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_all_event_view(self, request):
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
        fields = ["meter_serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        meter_serial = input_data['meter_serial']

        result, data = EventSerializer.admin_remove_all_event_serializer(
            token=token, meter_serial=meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def create_event_view(self, request):
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

        fields = ['event_type_code', 'meter_serial', 'event_information', 'event_counter', 'event_last_occurrence',
                  'event_create_time', 'event_module_code', 'event_count']
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        event_type_code = input_data["event_type_code"]
        meter_serial = input_data["meter_serial"]
        event_count = input_data["event_count"]
        event_information = input_data["event_information"]
        event_counter = input_data["event_counter"]
        event_last_occurrence = input_data["event_last_occurrence"]
        event_create_time = input_data["event_create_time"]
        event_module_code = input_data["event_module_code"]
        result, data = EventSerializer.create_event_serializer(
            token=token, event_type_code=event_type_code, event_module_code=event_module_code,
            event_count=event_count, event_information=event_information, meter_serial=meter_serial,
            event_counter=event_counter, event_last_occurrence=event_last_occurrence,
            event_create_time=event_create_time)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

