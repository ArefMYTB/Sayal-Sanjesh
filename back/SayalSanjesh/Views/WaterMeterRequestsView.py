from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.WaterMeterRequestsSerializer import WaterMeterRequestsSerializer

from SayalSanjesh.models import NoticeCategories


class WaterMeterRequestsView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """

    @csrf_exempt
    def admin_add_water_meter_request_view(self, request):
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
        fields = ["water_meter_request_title", "water_meter_request_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")

        water_meter_request_title = input_data['water_meter_request_title']
        water_meter_request_information = input_data['water_meter_request_information']
        result, data = WaterMeterRequestsSerializer.admin_add_water_meter_request_serializer(
            token=token, water_meter_request_title=water_meter_request_title,
            water_meter_request_information=water_meter_request_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_water_meter_request_view(self, request):
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
        fields = ["water_meter_request_id", "water_meter_request_title", "water_meter_request_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")

        water_meter_request_id = input_data['water_meter_request_id']
        water_meter_request_title = input_data['water_meter_request_title']
        water_meter_request_information = input_data['water_meter_request_information']

        result, data = WaterMeterRequestsSerializer.admin_edit_water_meter_request_serializer(
            token=token, water_meter_request_id=water_meter_request_id,
            water_meter_request_title=water_meter_request_title,
            water_meter_request_information=water_meter_request_information
        )
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_water_meter_request_view(self, request):
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
        if 'water_meter_request_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_request_id",
                                  english_message="water_meter_request_id is Null.")
        water_meter_request_id = input_data['water_meter_request_id']
        result, data = WaterMeterRequestsSerializer.admin_delete_water_meter_request_serializer(
            token=token, water_meter_request_id=water_meter_request_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_request_view(self, request):
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
        fields = ["water_meter_request_title", "water_meter_request_create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_request_title = input_data['water_meter_request_title']
        water_meter_request_create_date = input_data['water_meter_request_create_date']
        page = input_data['page']
        count = input_data['count']
        result, data = WaterMeterRequestsSerializer.admin_get_all_water_meter_request_serializer(
            token=token, water_meter_request_title=water_meter_request_title,
            water_meter_request_create_date=water_meter_request_create_date, page=page, count=count)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_water_meter_request_view(self, request):
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
        if 'water_meter_request_id' in input_data:
            water_meter_request_id = input_data['water_meter_request_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_request_id",
                                  english_message="water_meter_request_id is Null.")
        result, data = WaterMeterRequestsSerializer.admin_get_one_water_meter_request_serializer(
            token=token, water_meter_request_id=water_meter_request_id)
        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
