from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Serializers.WaterMeterSerializer import WaterMeterSerializer
from SayalSanjesh.Views import result_creator
from SayalSanjesh.models import WaterMeters


@csrf_exempt
class WaterMeterView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """

    @csrf_exempt
    def admin_create_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_user_id", "water_meter_serial", "water_meter_location", "other_information",
                  "water_meter_validation", "water_meter_activation", "water_meter_condition", "water_meter_type",
                  "water_meter_project", "water_meter_name", "water_meter_module", "water_meter_order_mode"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        # water_meter_admin = input_data["water_meter_admin"]
        water_meter_user_id = input_data["water_meter_user_id"]
        water_meter_serial = input_data["water_meter_serial"]
        water_meter_location = input_data["water_meter_location"]
        water_meter_validation = input_data["water_meter_validation"]
        water_meter_activation = input_data["water_meter_activation"]
        water_meter_condition = input_data["water_meter_condition"]
        other_information = input_data["other_information"]
        water_meter_type = input_data["water_meter_type"]
        water_meter_project = input_data["water_meter_project"]
        water_meter_name = input_data["water_meter_name"]
        water_meter_module = input_data["water_meter_module"]
        water_meter_order_mode = input_data["water_meter_order_mode"]
        if 'water_meter_manual_number' not in input_data:
            water_meter_manual_number = None
        else:
            water_meter_manual_number = input_data["water_meter_manual_number"]
        if 'water_meter_size' not in input_data:
            water_meter_size = None
        else:
            water_meter_size = input_data["water_meter_size"]
        if 'water_meter_model' not in input_data:
            water_meter_model = None
        else:
            water_meter_model = input_data["water_meter_model"]
        result, data = WaterMeterSerializer.admin_create_water_meter_serializer(
            token=token, water_meter_user_id=water_meter_user_id, water_meter_serial=water_meter_serial,
            water_meter_location=water_meter_location, water_meter_validation=water_meter_validation,
            water_meter_activation=water_meter_activation, water_meter_condition=water_meter_condition,
            other_information=other_information, water_meter_type=water_meter_type,
            water_meter_project=water_meter_project, water_meter_name=water_meter_name,
            water_meter_module=water_meter_module, water_meter_manual_number=water_meter_manual_number,
            water_meter_order_mode=water_meter_order_mode, water_meter_size=water_meter_size,
            water_meter_model=water_meter_model)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
            
        if 'water_meter_serial' in input_data:
            water_meter_serial = input_data["water_meter_serial"]
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                english_message="water_meter_serial is Null.")
        try:
            water_meter = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
        except WaterMeters.DoesNotExist:
            return result_creator(status="failure", code=404, farsi_message="کنتور پیدا نشد",
                                english_message="Water meter not found.")
        water_meter.delete()

        return result_creator(status="success", farsi_message="کنتور و قبض‌ها با موفقیت حذف شدند",
                            english_message="Water meter and its bills were successfully deleted.")

    @csrf_exempt
    def admin_edit_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_serial", "water_meter_location", "other_information", "water_meter_validation",
                  "water_meter_activation", "water_meter_condition", "water_meter_name", "water_meter_module_id",
                  "water_meter_user_id", "water_meter_project_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data["water_meter_serial"]
        water_meter_location = input_data["water_meter_location"]
        other_information = input_data["other_information"]
        water_meter_validation = input_data["water_meter_validation"]
        water_meter_activation = input_data["water_meter_activation"]
        water_meter_condition = input_data["water_meter_condition"]
        water_meter_name = input_data["water_meter_name"]
        water_meter_module_id = input_data["water_meter_module_id"]
        water_meter_user_id = input_data["water_meter_user_id"]
        water_meter_project_id = input_data["water_meter_project_id"]
        if "call_publisher" not in input_data:
            call_publisher = None
        else:
            call_publisher = input_data["call_publisher"]
        if "water_meter_bill" not in input_data:
            water_meter_bill = None
        else:
            water_meter_bill = input_data["water_meter_bill"]

        if "water_meter_manual_number" not in input_data:
            water_meter_manual_number = None
        else:
            water_meter_manual_number = input_data["water_meter_manual_number"]
        if "water_meter_size" not in input_data:
            water_meter_size = None
        else:
            water_meter_size = input_data["water_meter_size"]
        if "water_meter_model" not in input_data:
            water_meter_model = None
        else:
            water_meter_model = input_data["water_meter_model"]
        result, data = WaterMeterSerializer.admin_edit_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial, water_meter_location=water_meter_location,
            other_information=other_information, water_meter_validation=water_meter_validation,
            water_meter_activation=water_meter_activation, water_meter_condition=water_meter_condition,
            water_meter_name=water_meter_name, water_meter_module_id=water_meter_module_id,
            water_meter_user_id=water_meter_user_id,
            water_meter_project_id=water_meter_project_id, call_publisher=call_publisher,
            water_meter_bill=water_meter_bill, water_meter_manual_number=water_meter_manual_number,
            water_meter_size=water_meter_size, water_meter_model=water_meter_model)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meters_by_filter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meter_location", "water_meter_validation", "water_meter_validation",
                  "water_meter_activation", "water_meter_condition", "water_meter_location", "water_meter_type",
                  "water_meter_project"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meter_validation = input_data["water_meter_validation"]
        water_meter_activation = input_data["water_meter_activation"]
        water_meter_condition = input_data["water_meter_condition"]
        water_meter_location = input_data["water_meter_location"]
        water_meter_type = input_data["water_meter_type"]
        water_meter_project = input_data["water_meter_project"]
        result, data = WaterMeterSerializer.admin_get_all_water_meters_serializer_by_filter(
            token=token, page=page, count=count, water_meter_validation=water_meter_validation,
            water_meter_activation=water_meter_activation, water_meter_condition=water_meter_condition,
            water_meter_location=water_meter_location, water_meter_type=water_meter_type,
            water_meter_project=water_meter_project)
        if result:
            data = {
                "water_meters": data
            }
            if data['water_meters'].__len__() > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=406, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_water_meters_view(self, request):
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
        if 'project_id' not in input_data:
            project_id = None
        else:
            project_id = input_data["project_id"]
        if 'water_meter_serial' not in input_data:
            water_meter_serial = None
        else:
            water_meter_serial = input_data["water_meter_serial"]
        if 'water_meter_tag_id' not in input_data:
            water_meter_tag_id = None
        else:
            water_meter_tag_id = input_data["water_meter_tag_id"]
        result, data = WaterMeterSerializer.admin_get_all_water_meters_serializer(
            token=token, page=page, count=count, user_id=user_id, project_id=project_id,
            water_meter_serial=water_meter_serial, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'water_meter_serial' in input_data:
            water_meter_serial = input_data['water_meter_serial']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                  english_message="water_meter_serial is Null.")

        result, data = WaterMeterSerializer.admin_get_one_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_count_all_water_meter_view(self, request):
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["type", "project", "water_meter_activation", "water_meter_validation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        type = input_data['type']
        project = input_data['project']
        water_meter_activation = input_data['water_meter_activation']
        water_meter_validation = input_data['water_meter_validation']
        result, data = WaterMeterSerializer.admin_count_all_water_meter_serializer(
            token=token, type=type, project=project, water_meter_activation=water_meter_activation,
            water_meter_validation=water_meter_validation)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
        
    @csrf_exempt
    def admin_get_location_view(self, request):
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["type_id_list", "project_id_list", "tag_id_list"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                    english_message=f"{field} is Null.")
        
        type_id_list = input_data["type_id_list"]
        project_id_list = input_data["project_id_list"]
        tag_id_list = input_data["tag_id_list"]
        result, data = WaterMeterSerializer.admin_get_location_serializer(
            token=token, type_id_list=type_id_list, project_id_list=project_id_list, tag_id_list=tag_id_list
        )
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                english_message=data["english_message"])

    def user_get_one_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'water_meter_serial' in input_data:
            water_meter_serial = input_data['water_meter_serial']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                  english_message="water_meter_serial is Null.")

        result, data = WaterMeterSerializer.user_get_one_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meters_view(self, request):
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
        if 'water_meter_tag_id' not in input_data:
            water_meter_tag_id = None
        else:
            water_meter_tag_id = input_data['water_meter_tag_id']
        result, data = WaterMeterSerializer.user_get_all_water_meters_serializer(
            token=token, page=page, count=count, water_meter_tag_id=water_meter_tag_id)

        if result:

            if len(data) > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=406, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_count_all_water_meter_view(self, request):
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = WaterMeterSerializer.user_count_all_water_meter_serializer(token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_count_all_by_filters_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'water_meter_serial' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                  english_message="water_meter_serial is Null.")
        water_meter_serial = input_data['water_meter_serial']
        result, data = WaterMeterSerializer.user_count_all_by_filters_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_assign_user_to_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["user_phone", "water_meter_list"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        user_phone = input_data["user_phone"]
        water_meter_list = input_data["water_meter_list"]

        result, data = WaterMeterSerializer.admin_assign_user_to_water_meter_serializer(
            token=token, user_phone=user_phone, water_meter_list=water_meter_list)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_count_all_by_filters_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'water_meter_serial' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                  english_message="water_meter_serial is Null.")
        water_meter_serial = input_data['water_meter_serial']
        result, data = WaterMeterSerializer.admin_count_all_by_filters_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_value_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["consumption_id", "value", "cumulative_value"]
        # "user_id", "project_id", "type_id", "tag_id",
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        consumption_id = input_data['consumption_id']
        value = input_data['value']
        cumulative_value = input_data['cumulative_value']
        result, data = WaterMeterSerializer.admin_edit_value_water_meter_serializer(
            token=token, consumption_id=consumption_id, value=value, cumulative_value=cumulative_value)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def v2_admin_get_all_water_meters_view(self, request):
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
        if 'project_id' not in input_data:
            project_id = None
        else:
            project_id = input_data["project_id"]
        if 'water_meter_serial' not in input_data:
            water_meter_serial = None
        else:
            water_meter_serial = input_data["water_meter_serial"]
        if 'water_meter_tag_id' not in input_data:
            water_meter_tag_id = None
        else:
            water_meter_tag_id = input_data["water_meter_tag_id"]
        if 'water_meter_size' not in input_data:
            water_meter_size = None
        else:
            water_meter_size = input_data["water_meter_size"]
        if 'water_meter_model' not in input_data:
            water_meter_model = None
        else:
            water_meter_model = input_data["water_meter_model"]
        if 'water_meter_type_id' not in input_data:
            water_meter_type_id = None
        else:
            water_meter_type_id = input_data["water_meter_type_id"]

        if 'has_module' not in input_data:
            has_module = None
        else:
            has_module = input_data["has_module"]
        if 'has_user' not in input_data:
            has_user = None
        else:
            has_user = input_data["has_user"]
        result, data = WaterMeterSerializer.v2_admin_get_all_water_meters_serializer(
            token=token, page=page, count=count, user_id=user_id, project_id=project_id,
            water_meter_serial=water_meter_serial, water_meter_tag_id=water_meter_tag_id,
            water_meter_size=water_meter_size, water_meter_model=water_meter_model,
            water_meter_type_id=water_meter_type_id, has_module=has_module, has_user=has_user)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_water_meter_view_v2(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'water_meter_serial' in input_data:
            water_meter_serial = input_data['water_meter_serial']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                  english_message="water_meter_serial is Null.")

        result, data = WaterMeterSerializer.user_get_one_water_meter_serializer_v2(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_water_meters_view_v2(self, request):
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
        if 'water_meter_tag_id' not in input_data:
            water_meter_tag_id = None
        else:
            water_meter_tag_id = input_data['water_meter_tag_id']
        result, data = WaterMeterSerializer.user_get_all_water_meters_serializer_v2(
            token=token, page=page, count=count, water_meter_tag_id=water_meter_tag_id)

        if result:

            if len(data) > 0:
                return result_creator(data=data)
            else:
                return result_creator(status="failure", code=406, farsi_message="هیچ موردی پیدا نشد",
                                      english_message="don't find anything")
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
