import json
from django.views.decorators.csrf import csrf_exempt
from Authorization.Serializers.PermissionCatergorySerializer import PermissionCategorySerializers
from SayalSanjesh.Views import result_creator


@csrf_exempt
class PermissionCategoryViews:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """

    @csrf_exempt
    def admin_create_permission_category_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["permission_category_persian_name", "permission_category_english_name",
                  "permission_category_description", "permissions"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        permission_category_persian_name = input_data["permission_category_persian_name"]
        permission_category_english_name = input_data["permission_category_english_name"]
        permission_category_description = input_data["permission_category_description"]
        permissions = input_data["permissions"]

        result, data = PermissionCategorySerializers.admin_create_permission_category_serializer(
            token=token, permission_category_persian_name=permission_category_persian_name,
            permission_category_english_name=permission_category_english_name,
            permission_category_description=permission_category_description, permissions=permissions)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_permission_category_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["permission_category_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        permission_category_id = input_data["permission_category_id"]
        if 'permission_category_english_name' not in input_data:
            permission_category_english_name = None
        else:
            permission_category_english_name = input_data["permission_category_english_name"]
        if 'permission_category_persian_name' not in input_data:
            permission_category_persian_name = None
        else:
            permission_category_persian_name = input_data["permission_category_persian_name"]
        if 'permission_category_description' not in input_data:
            permission_category_description = None
        else:
            permission_category_description = input_data["permission_category_description"]
        if 'permissions' not in input_data:
            permissions = None
        else:
            permissions = input_data["permissions"]

        result, data = PermissionCategorySerializers.admin_edit_permission_category_serializer(
            token=token, permission_category_id=permission_category_id,
            permission_category_english_name=permission_category_english_name,
            permission_category_persian_name=permission_category_persian_name,
            permission_category_description=permission_category_description, permissions=permissions)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_permission_category_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'permission_category_id' in input_data:
            permission_category_id = input_data['permission_category_id']
            result, data = PermissionCategorySerializers.admin_delete_permission_serializer(
                token=token, permission_category_id=permission_category_id)
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است permission_category_id",
                                  english_message="permission_category_id is Null.")
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_permission_category_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "permission_category_english_name"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        permission_category_english_name = input_data["permission_category_english_name"]
        result, data = PermissionCategorySerializers.admin_get_all_permission_category_serializer(
            token=token, page=page, count=count, permission_category_english_name=permission_category_english_name)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
