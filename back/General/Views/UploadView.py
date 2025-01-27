from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from General.Serializers.UploadSerializer import UploadSerializer


@csrf_exempt
class UploadView:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """
    @csrf_exempt
    def admin_upload_file_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            file = request.FILES['file'] if 'file' in request.FILES else False
            if file != False:
                file = file
            else:
                file = ""
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = UploadSerializer. admin_upload_file_serializer(
            token=token, file=file)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

