from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from General.Serializers.AppSerializers import AppSerializers


@csrf_exempt
class AppViews:
    """
            A view class for handling GET and POST requests.

            Methods:
            - get: Handles GET requests and returns a JSON response.
            - post: Handles POST requests and returns a JSON response.
        """

    @csrf_exempt
    def get_app_view(self, request):

        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = AppSerializers.get_app_serializer(token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_app_view(self, request):

        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = AppSerializers.admin_get_app_serializer(token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_app_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["app_version_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        app_version_code = input_data['app_version_code']
        result, data = AppSerializers.admin_delete_app_serializer(
            token=token, app_version_code=app_version_code)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data["code"], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_add_app_view(self, request):
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
        app_version_name = input_data['app_version_name']
        result, data = AppSerializers.admin_add_app_serializer(
            token=token, filepath=filepath, app_version_code=app_version_code, app_version_name=app_version_name)
        # else:

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data["code"], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_app_view(self, request):
        if request.method.lower() == "options":
            return result_creator()

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = AppSerializers.user_get_app_serializer(token=token)
        # else:
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])