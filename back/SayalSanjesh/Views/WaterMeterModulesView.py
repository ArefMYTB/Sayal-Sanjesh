from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.WaterMeterModulesSerializer import WaterMeterModulesSerializer

from SayalSanjesh.models import NoticeCategories


class WaterMeterModulesView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """

    @csrf_exempt
    def admin_add_water_meter_module_view(self, request):
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
        fields = ["module_type_id", "water_meter_module_name", "water_meter_module_other_information",
                  "water_meter_module_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        non_required_fields = {
            "water_meter_module_unit": None,
            "water_meter_module_sim": None,
            "water_meter_module_sim_operator": None,
            "water_meter_module_property": None

        }
        for non_required_field in non_required_fields.keys():
            if non_required_field in input_data:
                non_required_fields[non_required_field] = input_data[non_required_field]

        water_meter_module_name = input_data['water_meter_module_name']
        water_meter_module_other_information = input_data['water_meter_module_other_information']
        water_meter_module_code = input_data['water_meter_module_code']
        module_type_id = input_data['module_type_id']
        result, data = WaterMeterModulesSerializer.admin_add_water_meter_module(
            token=token, water_meter_module_name=water_meter_module_name,
            water_meter_module_other_information=water_meter_module_other_information,
            water_meter_module_code=water_meter_module_code, module_type_id=module_type_id, **non_required_fields)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_water_meter_module_view(self, request):
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
        fields = ["water_meter_module_id", "water_meter_module_name", "water_meter_module_other_information",
                  "module_type_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        non_required_fields = {
            "water_meter_module_unit": None,
            "water_meter_module_sim": None,
            "water_meter_module_sim_operator": None,
            "water_meter_module_property": None

        }
        for non_required_field in non_required_fields.keys():
            if non_required_field in input_data:
                non_required_fields[non_required_field] = input_data[non_required_field]
        water_meter_module_id = input_data['water_meter_module_id']
        water_meter_module_name = input_data['water_meter_module_name']
        water_meter_module_other_information = input_data['water_meter_module_other_information']
        module_type_id = input_data['module_type_id']
        result, data = WaterMeterModulesSerializer.admin_edit_water_meter_module(
            token=token, water_meter_module_id=water_meter_module_id,
            water_meter_module_name=water_meter_module_name,
            water_meter_module_other_information=water_meter_module_other_information, module_type_id=module_type_id,
            **non_required_fields
        )
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_water_meter_module_view(self, request):
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
        if 'water_meter_module_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_module_id",
                                  english_message="water_meter_module_id is Null.")
        water_meter_module_id = input_data['water_meter_module_id']
        result, data = WaterMeterModulesSerializer.admin_delete_water_meter_module(
            token=token, water_meter_module_id=water_meter_module_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_modules_view(self, request):
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
        fields = ["water_meter_module_name", "water_meter_module_create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'mood' not in input_data:
            mood = 'all'
        else:
            mood = input_data['mood']
        water_meter_module_name = input_data['water_meter_module_name']
        water_meter_module_create_date = input_data['water_meter_module_create_date']
        page = input_data['page']
        count = input_data['count']
        result, data = WaterMeterModulesSerializer.admin_get_all_water_meter_modules(
            token=token, mood=mood, water_meter_module_name=water_meter_module_name,
            water_meter_module_create_date=water_meter_module_create_date, page=page, count=count)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_water_meter_module_view(self, request):
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
        if 'water_meter_module_id' in input_data:
            water_meter_module_id = input_data['water_meter_module_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_module_id",
                                  english_message="water_meter_module_id is Null.")
        if 'water_meter_module_code' in input_data:
            water_meter_module_code = input_data['water_meter_module_code']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_module_code",
                                  english_message="water_meter_module_code is Null.")
        result, data = WaterMeterModulesSerializer.admin_get_one_water_meter_module(
            token=token, water_meter_module_id=water_meter_module_id, water_meter_module_code=water_meter_module_code)
        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_add_request_too_water_meter_module_view(self, request):
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
        fields = ["water_meter_module_id", "water_meter_request_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_module_id = input_data['water_meter_module_id']
        water_meter_request_id = input_data['water_meter_request_id']
        result, data = WaterMeterModulesSerializer.admin_add_request_too_water_meter_module_serializer(
            token=token, water_meter_module_id=water_meter_module_id, water_meter_request_id=water_meter_request_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
