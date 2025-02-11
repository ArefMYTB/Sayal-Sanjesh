from django.views.decorators.csrf import csrf_exempt
import json
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from SayalSanjesh.Views import result_creator


@csrf_exempt
class AdminsView:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """

    @csrf_exempt
    def login_admin(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        admin_phone = input_data["admin_phone"]
        admin_password = input_data["admin_password"]
        result, data = AdminsSerializer.admin_login_serializer(admin_phone=admin_phone, admin_password=admin_password)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message="شماره موبایل و رمز عبور مطابقت ندارند.",
                                  english_message="Wrong phone number or password.")

    @csrf_exempt
    def admin_set_profile(self, request):

        if request.method.lower() == "options":
            return result_creator()
        data = request.POST['data']
        filepath = request.FILES['file'] if 'file' in request.FILES else False
        if filepath != False:
            filepath = filepath
        else:
            filepath = ""
        input_data = json.loads(data)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["admin_name", "admin_lastname", "other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        admin_name = input_data["admin_name"]
        admin_lastname = input_data["admin_lastname"]
        other_information = input_data["other_information"]
        if 'admin_password' not in input_data:
            admin_password = None
        else:
            admin_password = input_data["admin_password"]
        result, data = AdminsSerializer.admin_set_profile_serializer(
            token=token, admin_name=admin_name, admin_lastname=admin_lastname, other_information=other_information,
            filepath=filepath, admin_password=admin_password)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_profile(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = AdminsSerializer.admin_get_profile_serializer(token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_admin(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        other_admin_id = input_data["other_admin_id"]
        result, data = AdminsSerializer.admin_get_other_admin(token=token, other_admin_id=other_admin_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_change_password(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        admin_password = input_data["admin_password"]
        admin_old_password = input_data["admin_old_password"]
        result, data = AdminsSerializer.admin_change_password_serializer(token=token, new_password=admin_password,
                                                                         admin_old_password=admin_old_password)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_new_admin(self, request):
        if request.method.lower() == "options":
            return result_creator()
        data = request.POST['data']
        input_data = json.loads(data)
        filepath = request.FILES['file'] if 'file' in request.FILES else False

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        admin_name = input_data["admin_name"]
        admin_phone = input_data["admin_phone"]
        admin_lastname = input_data["admin_lastname"]
        admin_password = input_data["admin_password"]
        admin_permissions = input_data["admin_permissions"]
        other_information = input_data["other_information"]
        if filepath != False:
            filepath = filepath
        else:
            filepath = ""
        result, data = AdminsSerializer.admin_create_new_admin_serializer(
            token=token, admin_name=admin_name, admin_phone=admin_phone, admin_lastname=admin_lastname,
            admin_password=admin_password, admin_permissions=admin_permissions, other_information=other_information,
            filepath=filepath)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_admins(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        admin_name = input_data["admin_name"]
        admin_phone = input_data["admin_phone"]
        admin_lastname = input_data["admin_lastname"]
        result, data = AdminsSerializer.get_all_admins_serializer(token=token, admin_name=admin_name,
                                                                  admin_lastname=admin_lastname,
                                                                  admin_phone=admin_phone)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_other_admin(self, request):
        if request.method.lower() == "options":
            return result_creator()
        data = request.POST['data']
        filepath = request.FILES['file'] if 'file' in request.FILES else False
        if filepath != False:
            filepath = filepath
        else:
            filepath = ""
        input_data = json.loads(data)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        other_admin_id = input_data["other_admin_id"]
        admin_name = input_data["admin_name"]
        admin_lastname = input_data["admin_lastname"]
        admin_permissions = input_data["admin_permissions"]
        other_information = input_data["other_information"]
        result, data = AdminsSerializer.admin_edit_others_serializer(
            token, other_admin_id, admin_name, admin_lastname, admin_permissions, other_information, filepath)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_other_admin(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        other_admin_id = input_data["other_admin_id"]
        result, data = AdminsSerializer.admin_remove_other_serializer(token, other_admin_id)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_own_file_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        other_admin_id = input_data["other_admin_id"]
        result, data = AdminsSerializer.admin_get_other_admin_files_serializer(token, other_admin_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_admin_files_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        file_name = input_data["file_name"]
        other_admin_id = input_data["other_admin_id"]
        result, data = AdminsSerializer.admin_delete_admin_files_serializer(
            token=token, other_admin_id=other_admin_id, file_name=file_name)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_check_phone_number_validation_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        fields = ["phone", "sms_code", "send_sms", "password", "hash_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        phone = input_data["phone"]
        sms_code = input_data["sms_code"]
        send_sms = input_data["send_sms"]
        password = input_data["password"]
        hash_code = input_data["hash_code"]
        result, data = AdminsSerializer.admin_check_phone_number_validation_serializer(
            phone=phone, sms_code=sms_code, send_sms=send_sms, password=password, hash_code=hash_code)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_set_category_permission_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["admin_id", "permission_category_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        permission_category_id = input_data['permission_category_id']
        admin_id = input_data['admin_id']
        result, data = AdminsSerializer.admin_set_category_permission_serializer(
            token, admin_id=admin_id, permission_category_id=permission_category_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_set_permission_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["admin_id", "permission_english_name_list"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        permission_english_name_list = input_data['permission_english_name_list']
        admin_id = input_data['admin_id']
        result, data = AdminsSerializer.admin_set_permission_serializer(
            token, admin_id=admin_id, permission_english_name_list=permission_english_name_list)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def logout_admin(self, request):

        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = AdminsSerializer.admin_logout_serializer(token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
