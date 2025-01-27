from django.views.decorators.csrf import csrf_exempt
import json
from Authorization.Serializers.MiddleAdminsSerializer import MiddleAdminsSerializer
from SayalSanjesh.Views import result_creator


@csrf_exempt
class MiddleAdminsView:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """

    @csrf_exempt
    def add_middle_admin_data_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["project_ids", "water_meter_ids", "middle_admin_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        project_ids = input_data['project_ids']
        water_meter_ids = input_data['water_meter_ids']
        middle_admin_id = input_data['middle_admin_id']
        result, data = MiddleAdminsSerializer.add_middle_admin_data_serializer(
            token=token, project_ids=project_ids, water_meter_ids=water_meter_ids, middle_admin_id=middle_admin_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def edit_middle_admin_data_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["project_ids", "water_meter_ids", "middle_admin_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        project_ids = input_data['project_ids']
        water_meter_ids = input_data['water_meter_ids']
        middle_admin_id = input_data['middle_admin_id']
        result, data = MiddleAdminsSerializer.edit_middle_admin_data_serializer(
            token=token, project_ids=project_ids, water_meter_ids=water_meter_ids, middle_admin_id=middle_admin_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_middle_admin_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = MiddleAdminsSerializer.admin_get_all_middle_admin_serializer(token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_middle_admin_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["middle_admin_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        middle_admin_id = input_data['middle_admin_id']
        result, data = MiddleAdminsSerializer.admin_get_one_middle_admin_serializer(token=token,
                                                                                    middle_admin_id=middle_admin_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def middle_admin_get_all_users_view(self, request):
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
        result, data = MiddleAdminsSerializer.middle_admin_get_all_users_serializer(token=token, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
