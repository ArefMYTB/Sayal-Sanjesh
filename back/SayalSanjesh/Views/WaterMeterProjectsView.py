from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.NoticeCategoriesSerializer import NoticeCategoriesSerializer
from SayalSanjesh.Serializers.WaterMeterProjectsSerializer import WaterMeterProjectsSerializer

from SayalSanjesh.models import NoticeCategories


class WaterMeterProjectView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """

    @csrf_exempt
    def admin_add_water_meter_project_view(self, request):
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
        fields = ["water_meter_project_name", "water_meter_project_title", "water_meter_project_other_information",
                  "water_meter_project_start_date", "water_meter_project_employer_description",
                  "water_meter_project_contract_number", "water_meter_project_images", "water_meter_project_urls"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project_name = input_data['water_meter_project_name']
        water_meter_project_title = input_data['water_meter_project_title']
        water_meter_project_other_information = input_data['water_meter_project_other_information']
        water_meter_project_start_date = input_data['water_meter_project_start_date']
        water_meter_project_employer_description = input_data['water_meter_project_employer_description']
        water_meter_project_contract_number = input_data['water_meter_project_contract_number']
        water_meter_project_images = input_data['water_meter_project_images']
        water_meter_project_urls = input_data['water_meter_project_urls']
        result, data = WaterMeterProjectsSerializer.admin_add_water_meter_project(
            token=token, water_meter_project_name=water_meter_project_name,
            water_meter_project_title=water_meter_project_title,
            water_meter_project_start_date=water_meter_project_start_date,
            water_meter_project_employer_description=water_meter_project_employer_description,
            water_meter_project_contract_number=water_meter_project_contract_number,
            water_meter_project_other_information=water_meter_project_other_information,
            water_meter_project_images=water_meter_project_images, water_meter_project_urls=water_meter_project_urls)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_water_meter_project_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        filepath = ""
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project_name", "water_meter_project_id", "water_meter_project_other_information",
                  "water_meter_project_title", "water_meter_project_start_date",
                  "water_meter_project_employer_description", "water_meter_project_contract_number",
                  "water_meter_project_urls"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'water_meter_project_images' not in input_data:
            water_meter_project_images = None
        else:
            water_meter_project_images = input_data['water_meter_project_images']
        water_meter_project_id = input_data['water_meter_project_id']
        water_meter_project_name = input_data['water_meter_project_name']
        water_meter_project_title = input_data['water_meter_project_title']
        water_meter_project_other_information = input_data['water_meter_project_other_information']
        water_meter_project_start_date = input_data['water_meter_project_start_date']
        water_meter_project_employer_description = input_data['water_meter_project_employer_description']
        water_meter_project_contract_number = input_data['water_meter_project_contract_number']
        water_meter_project_urls = input_data['water_meter_project_urls']
        result, data = WaterMeterProjectsSerializer.admin_edit_water_meter_project(
            token=token, water_meter_project_id=water_meter_project_id,
            water_meter_project_name=water_meter_project_name,
            water_meter_project_title=water_meter_project_title,
            water_meter_project_other_information=water_meter_project_other_information,
            water_meter_project_start_date=water_meter_project_start_date,
            water_meter_project_employer_description=water_meter_project_employer_description,
            water_meter_project_contract_number=water_meter_project_contract_number, filepath=filepath,
            water_meter_project_images=water_meter_project_images, water_meter_project_urls=water_meter_project_urls)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_water_meter_project_view(self, request):
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
        if 'water_meter_project_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_project_id",
                                  english_message="category_id is Null.")
        water_meter_project_id = input_data['water_meter_project_id']
        result, data = WaterMeterProjectsSerializer.admin_delete_water_meter_project(
            token=token, water_meter_project_id=water_meter_project_id)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_projects_view(self, request):
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
        fields = ["water_meter_project_name", "water_meter_project_create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project_name = input_data['water_meter_project_name']
        water_meter_project_create_date = input_data['water_meter_project_create_date']
        page = input_data['page']
        count = input_data['count']
        if 'user_id' not in input_data:
            user_id = None
        else:
            user_id = input_data['user_id']
        result, data = WaterMeterProjectsSerializer.admin_get_all_water_meter_projects(
            token=token, water_meter_project_name=water_meter_project_name,
            water_meter_project_create_date=water_meter_project_create_date, page=page, count=count, user_id=user_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_water_meter_project_view(self, request):
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
        if 'water_meter_project_id' in input_data:
            water_meter_project_id = input_data['water_meter_project_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_project_id",
                                  english_message="water_meter_project_id is Null.")
        result, data = WaterMeterProjectsSerializer.admin_get_one_water_meter_project(
            token=token, water_meter_project_id=water_meter_project_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_add_type_too_project_view(self, request):
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
        fields = ["water_meter_type_id", "water_meter_project_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_type_id = input_data['water_meter_type_id']
        water_meter_project_id = input_data['water_meter_project_id']
        result, data = WaterMeterProjectsSerializer.admin_add_type_too_project_serializer(
            token=token, water_meter_type_id=water_meter_type_id, water_meter_project_id=water_meter_project_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meter_projects_city_count_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = WaterMeterProjectsSerializer.admin_get_all_water_meter_projects_city_count_serializer(
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

        result, data = WaterMeterProjectsSerializer.admin_admin_total_statistics_serializer(
            token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meter_projects_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterProjectsSerializer.user_get_all_water_meter_projects(token=token)

        if result:
            if len(data) > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=403, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_water_meter_project_view(self, request):
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
        if 'water_meter_project_id' in input_data:
            water_meter_project_id = input_data['water_meter_project_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_project_id",
                                  english_message="water_meter_project_id is Null.")
        result, data = WaterMeterProjectsSerializer.user_get_one_water_meter_projects(
            water_meter_project_id=water_meter_project_id, token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meter_projects_view_v2(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterProjectsSerializer.user_get_all_water_meter_projects_v2(token=token)

        if result:
            if len(data) > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=403, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_water_meter_project_view_v2(self, request):
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
        if 'water_meter_project_id' in input_data:
            water_meter_project_id = input_data['water_meter_project_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_project_id",
                                  english_message="water_meter_project_id is Null.")
        result, data = WaterMeterProjectsSerializer.user_get_one_water_meter_projects_v2(
            water_meter_project_id=water_meter_project_id, token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])