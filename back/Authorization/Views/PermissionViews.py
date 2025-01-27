import json
from django.views.decorators.csrf import csrf_exempt
from Authorization.Serializers.PermissionSerializer import PermissionSerializers
from SayalSanjesh.Views import result_creator


@csrf_exempt
class PermissionViews:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """

    @csrf_exempt
    def admin_create_permission_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["permission_persian_name", "permission_english_name", "permission_description"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        permission_english_name = input_data["permission_english_name"]
        permission_persian_name = input_data["permission_persian_name"]
        permission_description = input_data["permission_description"]

        result, data = PermissionSerializers.admin_create_permission_serializer(
            token=token, permission_english_name=permission_english_name,
            permission_persian_name=permission_persian_name, permission_description=permission_description)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_permission_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["permission_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        permission_id = input_data["permission_id"]
        if 'permission_english_name' not in input_data:
            permission_english_name = None
        else:
            permission_english_name = input_data["permission_english_name"]
        if 'permission_persian_name' not in input_data:
            permission_persian_name = None
        else:
            permission_persian_name = input_data["permission_persian_name"]
        if 'permission_description' not in input_data:
            permission_description = None
        else:
            permission_description = input_data["permission_description"]

        result, data = PermissionSerializers.admin_edit_permission_serializer(
            token=token, permission_id=permission_id, permission_english_name=permission_english_name,
            permission_persian_name=permission_persian_name, permission_description=permission_description)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_permission_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'permission_id' in input_data:
            permission_id = input_data['permission_id']
            result, data = PermissionSerializers.admin_delete_permission_serializer(token=token,
                                                                                    permission_id=permission_id)
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است permission_id",
                                  english_message="permission_id is Null.")
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_permission_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "permission_english_name"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        permission_english_name = input_data["permission_english_name"]
        result, data = PermissionSerializers.admin_get_all_permission_serializer(
            token=token, page=page, count=count, permission_english_name=permission_english_name)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
