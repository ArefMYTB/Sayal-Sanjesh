from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator

from SayalSanjesh.Serializers.CalculateUnitsSerializer import CalculateUnitesSerializer

from SayalSanjesh.models import NoticeCategories


class CalculateUnitesView():

    @csrf_exempt
    def admin_add_calculate_unites_view(self, request):
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
        fields = ["water_meter_serial", "calculate_unites"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data['water_meter_serial']
        calculate_unites = input_data['calculate_unites']
        result, data = CalculateUnitesSerializer.admin_add_calculate_unites_serializer(
            token=token, water_meter_serial=water_meter_serial, calculate_unites=calculate_unites)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_calculate_unites_view(self, request):
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
        if 'calculate_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است calculate_id",
                                  english_message="calculate_id is Null.")
        calculate_id = input_data['calculate_id']
        result, data = CalculateUnitesSerializer.admin_delete_calculate_unites_serializer(
            token=token, calculate_id=calculate_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_calculate_price_view(self, request):
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
        page = input_data['page']
        count = input_data['count']
        result, data = CalculateUnitesSerializer.admin_get_all_calculate_price_serializer(
            token=token, page=page, count=count)
        print(type(data))
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
