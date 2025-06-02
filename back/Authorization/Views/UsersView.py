import json

from django.views.decorators.csrf import csrf_exempt

from Authorization.Serializers.UsersSerializer import UsersSerializer
from SayalSanjesh.Views import result_creator


@csrf_exempt
class UsersView:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """
    @csrf_exempt
    def login_user(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        fields = ["user_phone", "user_password"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        user_phone = input_data["user_phone"]
        user_password = input_data["user_password"]
        result, data = UsersSerializer.user_login_serializer(user_phone=user_phone, user_password=user_password)
        if result:
            return result_creator(data=data)

        else:
            return result_creator(status="failure", code=403, farsi_message="شماره موبایل و رمز عبور مطابقت ندارند.",
                                  english_message="Wrong phone number or password.")

    @csrf_exempt
    def admin_create_new_user(self, request):
        try:
            data = request.POST['data']
            input_data = json.loads(data)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        filepath = request.FILES['file'] if 'file' in request.FILES else False
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["user_name", "user_phone", "user_password", "user_lastname", "other_information", "user_sms_code",
                  "user_profile"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        user_name = input_data["user_name"]
        user_lastname = input_data["user_lastname"]
        user_phone = input_data["user_phone"]
        user_password = input_data["user_password"]
        user_sms_code = input_data["user_sms_code"]
        other_information = input_data["other_information"]
        user_profile = input_data["user_profile"]
        if filepath != False:
            filepath = filepath
        else:
            filepath = ""
        result, data = UsersSerializer.admin_create_new_user_serializer(
            token=token, user_name=user_name, user_phone=user_phone, user_lastname=user_lastname,
            user_password=user_password, user_sms_code=user_sms_code, user_profile=user_profile,
            other_information=other_information, filepath=filepath)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_profile(self, request):
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = UsersSerializer.user_get_profile_serializer(token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_users(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "user_name", "user_lastname", "user_phone"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        user_name = input_data["user_name"]
        user_lastname = input_data["user_lastname"]
        user_phone = input_data["user_phone"]
        result, data = UsersSerializer.get_all_users_serializer(
            token=token, page=page, count=count, user_name=user_name, user_lastname=user_lastname,
            user_phone=user_phone)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_user(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'user_phone' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است user_phone",
                                  english_message="user_phone is Null.")
        if 'other_user_id' in input_data:
            other_user_id = input_data['other_user_id']
            user_phone = input_data['user_phone']
            result, data = UsersSerializer.admin_get_one_user_serializer(token=token, other_user_id=other_user_id,
                                                                         user_phone=user_phone)
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است other_user_id",
                                  english_message="other_user_id is Null.")
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_change_user_profile(self, request):
        try:
            data = request.POST['data']
            input_data = json.loads(data)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        filepath = request.FILES['file'] if 'file' in request.FILES else False
        if filepath != False:
            filepath = filepath
        else:
            filepath = ""
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["other_user_id", "user_name", "user_phone", "user_lastname", "user_password", "user_sms_code",
                  "user_profile", "other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        other_user_id = input_data["other_user_id"]
        user_name = input_data["user_name"]
        user_phone = input_data["user_phone"]
        user_lastname = input_data["user_lastname"]
        user_password = input_data["user_password"]
        user_sms_code = input_data["user_sms_code"]
        user_profile = input_data["user_profile"]
        other_information = input_data["other_information"]
        result, data = UsersSerializer.admin_change_user_profile(
            token=token, other_user_id=other_user_id, user_name=user_name, user_phone=user_phone,
            user_lastname=user_lastname, user_password=user_password, user_sms_code=user_sms_code,
            user_profile=user_profile, other_information=other_information, filepath=filepath)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_edit_profile(self, request):
        try:
            data = request.POST['data']
            input_data = json.loads(data)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        filepath = request.FILES['file'] if 'file' in request.FILES else False
        print(filepath)
        if filepath != False:
            filepath = filepath
        else:
            filepath = ""
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["user_name", "user_lastname", "user_profile", "other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        user_name = input_data["user_name"]
        user_lastname = input_data["user_lastname"]
        user_profile = input_data["user_profile"]
        other_information = input_data["other_information"]
        result, data = UsersSerializer.user_edit_profile(
            token=token, user_name=user_name, user_lastname=user_lastname, user_profile=user_profile,
            other_information=other_information, filepath=filepath)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_change_password(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if "user_new_password" not in input_data:
            return result_creator(status="failure", code=406, farsi_message="user_new_password وارد نشده است ",
                                  english_message="user_new_password is Null.")
        user_new_password = input_data["user_new_password"]
        result, data = UsersSerializer.user_change_password(token=token, user_new_password=user_new_password)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_user_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'user_id' in input_data:
            user_id = input_data['user_id']
            result, data = UsersSerializer.admin_delete_user_serializer(token=token, user_id=user_id)
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است user_id",
                                  english_message="user_id is Null.")
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_check_phone_number_validation_view(self, request):
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
        result, data = UsersSerializer.user_check_phone_number_validation_serializer(
            phone=phone, sms_code=sms_code, send_sms=send_sms, password=password, hash_code=hash_code)
        if result:
            return result_creator(data=data)

        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_add_app_view(self, request):
        try:
            data = request.POST['data']
            input_data = json.loads(data)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        filepath = request.FILES['file'] if 'file' in request.FILES else False
        if filepath != False:
            filepath = filepath
        else:
            return result_creator(status="failure", code=406, farsi_message="فایل وارد نشده است",
                                  english_message="file has not been imported")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["app_version_code", "app_version_name"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        app_version_code = input_data['app_version_code']
        app_name = input_data['app_name']
        result, data = UsersSerializer.user_add_app_serializer(
            token=token, filepath=filepath, app_version_code=app_version_code, app_name=app_name)
        # else:
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

