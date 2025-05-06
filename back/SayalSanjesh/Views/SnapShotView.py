from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Serializers.SnapShotSerializer import SnapShotSerializer
from SayalSanjesh.Views import result_creator


@csrf_exempt
class SnapShotView:

    @csrf_exempt
    def admin_create_snap_shot_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="json نامعتبر است",
                                english_message="Invalid JSON format.")

        token = request.headers.get("Token", "")

        result, data = SnapShotSerializer.admin_create_snap_shot_serializer(token=token, input_data=input_data)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                english_message=data["english_message"])


    @csrf_exempt
    def admin_edit_snap_shot_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="json نامعتبر است",
                                english_message="Invalid JSON format.")

        token = request.headers.get("Token", "")

        result, data = SnapShotSerializer.admin_edit_snap_shot_serializer(token=token, input_data=input_data)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                english_message=data["english_message"])


    @csrf_exempt
    def admin_get_all_snap_shots_view(self, request):
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

        page = input_data["page"]
        count = input_data["count"]
        if 'user_id' not in input_data:
            user_id = None
        else:
            user_id = input_data["user_id"]

        if 'water_meter_serial' not in input_data:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
        else:
            water_meter_serial = input_data["water_meter_serial"]

        result, data = SnapShotSerializer.admin_get_all_snap_shots_serializer(
            request=request, token=token, page=page, count=count, user_id=user_id,
            water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])


    @csrf_exempt
    def admin_upload_snap_shot_view(self, request):
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
            
        result, data = SnapShotSerializer.admin_upload_snap_shot_serializer(
            token=token, file=file)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
