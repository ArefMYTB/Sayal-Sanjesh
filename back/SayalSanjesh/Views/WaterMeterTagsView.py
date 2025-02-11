from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.NoticeCategoriesSerializer import NoticeCategoriesSerializer
from SayalSanjesh.Serializers.WaterMeterTagsSerializer import WaterMeterTagsSerializer

from SayalSanjesh.models import NoticeCategories


class WaterMeterTagsView():

    @csrf_exempt
    def admin_add_water_meter_tag(self, request):
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
        fields = ["water_meter_tag_name", "water_meter_tag_other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_tag_name = input_data['water_meter_tag_name']
        water_meter_tag_other_information = input_data['water_meter_tag_other_information']
        result, data = WaterMeterTagsSerializer.admin_add_water_meter_tag_serializer(
            token=token, water_meter_tag_name=water_meter_tag_name,
            water_meter_tag_other_information=water_meter_tag_other_information, filepath=filepath)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_water_meter_tag_view(self, request):
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
        if 'water_meter_tag_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_tag_id",
                                  english_message="water_meter_tag_id is Null.")
        water_meter_tag_id = input_data['water_meter_tag_id']
        result, data = WaterMeterTagsSerializer.admin_delete_water_meter_tag_serializer(
            token=token, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_tags_view(self, request):
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
        fields = ["water_meter_tag_name", "water_meter_type_create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_tag_name = input_data['water_meter_tag_name']
        water_meter_type_create_date = input_data['water_meter_type_create_date']
        page = input_data['page']
        count = input_data['count']
        result, data = WaterMeterTagsSerializer.admin_get_all_water_meter_tags_serializer(
            token=token, water_meter_tag_name=water_meter_tag_name,
            water_meter_type_create_date=water_meter_type_create_date, page=page, count=count)
        if result:
            result = {
                "categories": data
            }
            if result['categories'].__len__() > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=403, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_total_statists_tags_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = WaterMeterTagsSerializer.admin_total_statists_tags_serializer(token=token)
        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meter_tags_view(self, request):
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
        fields = ["water_meter_tag_name", "water_meter_type_create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_tag_name = input_data['water_meter_tag_name']
        water_meter_type_create_date = input_data['water_meter_type_create_date']
        page = input_data['page']
        count = input_data['count']
        result, data = WaterMeterTagsSerializer.user_get_all_water_meter_tags_serializer(
            token=token, water_meter_tag_name=water_meter_tag_name,
            water_meter_type_create_date=water_meter_type_create_date, page=page, count=count)
        if result:

            return result_creator(data=data)

        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
