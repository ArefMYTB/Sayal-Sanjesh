from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.NoticeCategoriesSerializer import NoticeCategoriesSerializer
from SayalSanjesh.Serializers.WaterMeterTypesSerializer import WaterMeterTypesSerializer

from SayalSanjesh.models import NoticeCategories


class WaterMeterTypesView():

    @csrf_exempt
    def admin_add_water_meter_type(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            data = request.POST['data']
            input_data = json.loads(data)
            filepath = request.FILES['file'] if 'file' in request.FILES else False
            if filepath != False:
                filepath = filepath
            else:
                filepath = ""
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_type_name", "water_meter_tag", "water_meter_type_other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_type_name = input_data['water_meter_type_name']
        water_meter_type_other_information = input_data['water_meter_type_other_information']
        water_meter_tag = input_data['water_meter_tag']
        result, data = WaterMeterTypesSerializer.admin_add_water_meter_type(
            token=token, water_meter_type_name=water_meter_type_name,
            water_meter_type_other_information=water_meter_type_other_information,
            water_meter_tag=water_meter_tag, filepath=filepath)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_water_meter_project(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            data = request.POST['data']
            input_data = json.loads(data)
            filepath = request.FILES['file'] if 'file' in request.FILES else False
            if filepath != False:
                filepath = filepath
            else:
                filepath = ""
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_tag_id", "water_meter_type_new_name", "water_meter_type_id",
                  "water_meter_type_other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_tag_id = input_data['water_meter_tag_id']
        water_meter_type_new_name = input_data['water_meter_type_new_name']
        water_meter_type_id = input_data['water_meter_type_id']
        water_meter_type_other_information = input_data['water_meter_type_other_information']
        result, data = WaterMeterTypesSerializer.admin_edit_water_meter_type(
            token=token, water_meter_tag_id=water_meter_tag_id, water_meter_type_new_name=water_meter_type_new_name,
            water_meter_type_id=water_meter_type_id,
            water_meter_type_other_information=water_meter_type_other_information, filepath=filepath)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_water_meter_project(self, request):
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
        if 'water_meter_type_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_type_id",
                                  english_message="water_meter_type_id is Null.")
        water_meter_type_id = input_data['water_meter_type_id']
        result, data = WaterMeterTypesSerializer.admin_delete_water_meter_type(
            token=token, water_meter_type_id=water_meter_type_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_categories(self, request):
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
        fields = ["water_meter_type_name", "water_meter_type_create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_type_name = input_data['water_meter_type_name']
        water_meter_type_create_date = input_data['water_meter_type_create_date']
        page = input_data['page']
        count = input_data['count']
        result, data = WaterMeterTypesSerializer.admin_get_all_water_meter_types(
            token=token, water_meter_type_name=water_meter_type_name,
            water_meter_type_create_date=water_meter_type_create_date, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_water_meter_type(self, request):
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
        if 'water_meter_type_id' in input_data:
            water_meter_type_id = input_data['water_meter_type_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_type_id",
                                  english_message="water_meter_type_id is Null.")
        result, data = WaterMeterTypesSerializer.admin_get_one_water_meter_type(
            token=token, water_meter_type_id=water_meter_type_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_type_sort_by_values_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterTypesSerializer.admin_get_all_water_meter_type_sort_by_values_serializer(
            token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_total_statistics_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterTypesSerializer.admin_total_statistics_serializer(
            token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meter_categories(self, request):
        if request.method.lower() == "options":
            return result_creator()

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterTypesSerializer.user_get_all_water_meter_types(token=token)
        if result:
            result = {
                'types': data
            }
            if result['types'].__len__() > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=403, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_water_meter_project(self, request):
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
        if 'water_meter_type_name' in input_data:
            water_meter_type_name = input_data['water_meter_type_name']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_type_name",
                                  english_message="water_meter_type_name is Null.")
        result, data = WaterMeterTypesSerializer.user_get_one_water_meter_types(
            token=token, water_meter_type_name=water_meter_type_name)
        if result:
            result = {
                "category": data
            }
            return result_creator(result)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_water_meter_project_v2(self, request):
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
        if 'water_meter_type_name' in input_data:
            water_meter_type_name = input_data['water_meter_type_name']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_type_name",
                                  english_message="water_meter_type_name is Null.")
        result, data = WaterMeterTypesSerializer.user_get_one_water_meter_types_v2(
            token=token, water_meter_type_name=water_meter_type_name)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meter_categories_v2(self, request):
        if request.method.lower() == "options":
            return result_creator()

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterTypesSerializer.user_get_all_water_meter_types_v2(token=token)
        if result:
            result = {
                'types': data
            }
            if result['types'].__len__() > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=403, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])