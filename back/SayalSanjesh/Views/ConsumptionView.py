from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Serializers.ConsumptionSerializer import ConsumptionSerializer
from SayalSanjesh.Views import result_creator


@csrf_exempt
class ConsumptionView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """
    serializer_class = ConsumptionSerializer()

    # ------------------------------------------------AdminViews--------------------------------------------------------
    @csrf_exempt
    def admin_get_cumulative_consumptions_view(self, request):
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
        if 'water_meter_tag' not in input_data:
            water_meter_tag = None
        else:
            water_meter_tag = input_data["water_meter_tag"]
        if 'sort_value' not in input_data:
            sort_value = None
        else:
            sort_value = input_data["sort_value"]
        if 'reverse' not in input_data:
            reverse = None
        else:
            reverse = input_data["reverse"]
        result, data = self.serializer_class.admin_get_cumulative_consumptions_serializer(
            token=token, page=page, count=count, user_id=user_id, project_id=project_id,
            water_meter_serial=water_meter_serial, water_meter_tag=water_meter_tag, sort_value=sort_value,
            input_reverse=reverse)
        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_cumulative_consumptions_per_tag_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

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

        result, data = self.serializer_class.admin_get_cumulative_consumptions_per_tag_serializer(
            token=token, user_id=user_id, project_id=project_id,
            water_meter_serial=water_meter_serial)
        if result:

            return result_creator(data=data)

        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_consumptions_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meters", "water_meter_user", "water_meter_project", "water_meter_type",
                  "start_time", "end_time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meters = input_data["water_meters"]
        water_meter_user = input_data["water_meter_user"]
        water_meter_project = input_data["water_meter_project"]
        water_meter_type = input_data["water_meter_type"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]
        result, data = self.serializer_class.admin_get_all_consumptions_serializer(
            token=token, page=page, count=count, water_meters=water_meters, water_meter_user=water_meter_user,
            water_meter_project=water_meter_project,
            water_meter_type=water_meter_type, start_time=start_time, end_time=end_time)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_consumption_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'consumption_id' in input_data:
            consumption_id = input_data['consumption_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_serial",
                                  english_message="water_meter_serial is Null.")

        result, data = self.serializer_class.admin_get_one_consumption_serializer(
            token=token, consumption_id=consumption_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_consumption_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_serial", "consumption_id", "mode", "time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data["water_meter_serial"]
        consumption_id = input_data["consumption_id"]
        mode = input_data["mode"]
        time = input_data["time"]
        result, data = self.serializer_class.admin_remove_consumption_serializer(
            token, consumption_id, water_meter_serial, mode, time)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_consumption_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["consumption_id", "value", "information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'create_time' not in input_data:
            create_time = None
        else:
            create_time = input_data['create_time']
        if 'from_previous_record' not in input_data:
            from_previous_record = None
        else:
            from_previous_record = input_data['from_previous_record']
        if 'to_current_record' not in input_data:
            to_current_record = None
        else:
            to_current_record = input_data['to_current_record']
        consumption_id = input_data["consumption_id"]
        value = input_data["value"]
        information = input_data["information"]
        result, data = self.serializer_class.admin_edit_consumption_serializer(
            token=token, consumption_id=consumption_id, value=value, information=information, create_time=create_time,
            from_previous_record=from_previous_record, to_current_record=to_current_record)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_last_consumption_data_by_water_meter_view(self, request):
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

        result, data = self.serializer_class.admin_get_last_consumption_data_by_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_all_water_meter_consumption_view(self, request):
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = self.serializer_class.admin_get_all_all_water_meter_consumption(
            token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_consumptions_by_date_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meters", "start_time",
                  "end_time"]
        # "user_id", "project_id", "type_id", "tag_id",
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meters = input_data["water_meters"]
        if 'user_id' not in input_data:
            user_id = None
        else:
            user_id = input_data["user_id"]
        if 'project_id' not in input_data:
            project_id = None
        else:
            project_id = input_data["project_id"]
        if 'type_id' not in input_data:
            type_id = None
        else:
            type_id = input_data["type_id"]
        if 'tag_id' not in input_data:
            tag_id = None
        else:
            tag_id = input_data["tag_id"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        print("Vanilla")

        result, data = self.serializer_class.admin_get_all_consumptions_by_date_serializer(
            token=token, page=page, count=count, water_meters=water_meters, user_id=user_id, project_id=project_id,
            tag_id=tag_id, type_id=type_id,
            start_time=start_time, end_time=end_time)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_consumptions_by_date_for_chart_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meters", "start_time",
                  "end_time"]
        # "user_id", "project_id", "type_id", "tag_id",
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meters = input_data["water_meters"]
        if 'user_id' not in input_data:
            user_id = None
        else:
            user_id = input_data["user_id"]
        if 'project_id' not in input_data:
            project_id = None
        else:
            project_id = input_data["project_id"]
        if 'type_id' not in input_data:
            type_id = None
        else:
            type_id = input_data["type_id"]
        if 'tag_id' not in input_data:
            tag_id = None
        else:
            tag_id = input_data["tag_id"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        print("for chart")

        result, data = self.serializer_class.admin_get_all_consumptions_by_date_for_chart_serializer(
            token=token, page=page, count=count, water_meters=water_meters, user_id=user_id, project_id=project_id,
            tag_id=tag_id, type_id=type_id,
            start_time=start_time, end_time=end_time)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_consumptions_by_date__per_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meters_list", "start_time", "end_time"]
        # "user_id", "project_id", "type_id", "tag_id",
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")

        water_meters_list = input_data["water_meters_list"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        result, data = self.serializer_class.admin_get_all_consumptions_by_date__per_meter_serializer(
            token=token, water_meters_list=water_meters_list, start_time=start_time, end_time=end_time)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_consumption_total_statistics_view(self, request):
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = self.serializer_class.admin_consumption_total_statistics_serializer(token=token)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_csv_file_overall_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project", "water_meter_tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project = input_data["water_meter_project"]
        water_meter_tag_id = input_data["water_meter_tag_id"]

        result, data = self.serializer_class.admin_create_csv_file_overall_serializer(
            token=token, water_meter_project=water_meter_project, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_csv_file_single_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project", "water_meter_tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project = input_data["water_meter_project"]
        water_meter_tag_id = input_data["water_meter_tag_id"]

        result, data = self.serializer_class.admin_create_csv_file_single_serializer(
            token=token, water_meter_project=water_meter_project, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_csv_file_all_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project", "water_meter_tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project = input_data["water_meter_project"]
        water_meter_tag_id = input_data["water_meter_tag_id"]

        result, data = self.serializer_class.admin_create_csv_file_all_serializer(
            token=token, water_meter_project=water_meter_project, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_csv_file_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_serial", "start_time", "end_time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data["water_meter_serial"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        result, data = self.serializer_class.admin_get_one_csv_file_serializer(
            token=token, water_meter_serial=water_meter_serial, start_time=start_time, end_time=end_time)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_update_sum_value_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["meter_list"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")

        meter_list = input_data['meter_list']

        result, data = self.serializer_class.admin_update_sum_value_serializer(
            token=token, meter_list=meter_list)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_csv_file_overall_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project", "water_meter_tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project = input_data["water_meter_project"]
        water_meter_tag_id = input_data["water_meter_tag_id"]

        result, data = self.serializer_class.admin_create_csv_file_overall_serializer(
            token=token, water_meter_project=water_meter_project, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_csv_file_single_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project", "water_meter_tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project = input_data["water_meter_project"]
        water_meter_tag_id = input_data["water_meter_tag_id"]

        result, data = self.serializer_class.admin_create_csv_file_single_serializer(
            token=token, water_meter_project=water_meter_project, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_csv_file_all_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_project", "water_meter_tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_project = input_data["water_meter_project"]
        water_meter_tag_id = input_data["water_meter_tag_id"]

        result, data = self.serializer_class.admin_create_csv_file_all_serializer(
            token=token, water_meter_project=water_meter_project, water_meter_tag_id=water_meter_tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_csv_file_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["water_meter_serial", "start_time", "end_time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data["water_meter_serial"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        result, data = self.serializer_class.admin_get_one_csv_file_serializer(
            token=token, water_meter_serial=water_meter_serial, start_time=start_time, end_time=end_time)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_update_sum_value_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["meter_list"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")

        meter_list = input_data['meter_list']

        result, data = self.serializer_class.admin_update_sum_value_serializer(
            token=token, meter_list=meter_list)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_consumptions_by_date_app_view(self, request):

        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meters", "start_time",
                  "end_time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meters = input_data["water_meters"]
        if 'user_id' not in input_data:
            user_id = None
        else:
            user_id = input_data["user_id"]
        if 'project_id' not in input_data:
            project_id = None
        else:
            project_id = input_data["project_id"]
        if 'type_id' not in input_data:
            type_id = None
        else:
            type_id = input_data["type_id"]
        if 'tag_id' not in input_data:
            tag_id = None
        else:
            tag_id = input_data["tag_id"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        result, data = self.serializer_class.admin_get_all_consumptions_by_date_app_serializer(
            token=token, page=page, count=count, water_meters=water_meters, user_id=user_id, project_id=project_id,
            tag_id=tag_id, type_id=type_id,
            start_time=start_time, end_time=end_time)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def v2_admin_get_cumulative_consumptions_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "project_id", "water_meter_serial", "water_meter_tag", "sort_value", "reverse"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'sort_value' in fields and input_data["sort_value"] is not None:
            valid_sort_value = ['last_cons_object_create_time', 'last_consumption_value', 'month', 'year']
            if input_data["sort_value"] is not None and input_data["sort_value"] not in valid_sort_value:
                return result_creator(status="failure", code=406,
                                      farsi_message=f"مقادیر مجاز برای sort_value : {valid_sort_value}",
                                      english_message=f"valid sort_value is :{valid_sort_value}")
        page = input_data["page"]
        count = input_data["count"]
        user_id = input_data["user_id"]
        project_id = input_data["project_id"]
        water_meter_serial = input_data["water_meter_serial"]
        water_meter_tag = input_data["water_meter_tag"]
        sort_value = input_data["sort_value"]
        reverse = input_data["reverse"]
        result, data = self.serializer_class.v2_admin_get_cumulative_consumptions_serializer(
            token=token, page=page, count=count, user_id=user_id, project_id=project_id,
            water_meter_serial=water_meter_serial, water_meter_tag=water_meter_tag, sort_value=sort_value,
            input_reverse=reverse)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def v2_admin_get_cumulative_consumptions_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "project_id", "water_meter_serial", "water_meter_tag", "sort_value", "reverse"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'sort_value' in fields and input_data["sort_value"] is not None:
            valid_sort_value = ['last_cons_object_create_time', 'last_consumption_value', 'month', 'year']
            if input_data["sort_value"] is not None and input_data["sort_value"] not in valid_sort_value:
                return result_creator(status="failure", code=406,
                                      farsi_message=f"مقادیر مجاز برای sort_value : {valid_sort_value}",
                                      english_message=f"valid sort_value is :{valid_sort_value}")
        page = input_data["page"]
        count = input_data["count"]
        user_id = input_data["user_id"]
        project_id = input_data["project_id"]
        water_meter_serial = input_data["water_meter_serial"]
        water_meter_tag = input_data["water_meter_tag"]
        sort_value = input_data["sort_value"]
        reverse = input_data["reverse"]
        result, data = self.serializer_class.v2_admin_get_cumulative_consumptions_serializer(
            token=token, page=page, count=count, user_id=user_id, project_id=project_id,
            water_meter_serial=water_meter_serial, water_meter_tag=water_meter_tag, sort_value=sort_value,
            input_reverse=reverse)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------UserViews---------------------------------------------------------
    @csrf_exempt
    def user_get_all_consumptions_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meters", "water_meter_project", "water_meter_type",
                  "start_time", "end_time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meters = input_data["water_meters"]
        water_meter_project = input_data["water_meter_project"]
        water_meter_type = input_data["water_meter_type"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]

        result, data = self.serializer_class.user_get_all_consumptions_serializer(
            token=token, page=page, count=count, water_meters=water_meters, water_meter_project=water_meter_project,
            water_meter_type=water_meter_type, start_time=start_time, end_time=end_time)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_consumptions_by_date_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "water_meters", "start_time", "end_time"]
        # "user_id", "project_id", "type_id", "tag_id",
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meters = input_data["water_meters"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]
        if 'project_id' not in input_data:
            project_id = None
        else:
            project_id = input_data['project_id']
        if 'type_id' not in input_data:
            type_id = None
        else:
            type_id = input_data['type_id']
        if 'tag_id' not in input_data:
            tag_id = None
        else:
            tag_id = input_data['tag_id']

        result, data = self.serializer_class.user_get_all_consumptions_by_date_serializer(
            token=token, page=page, count=count, water_meters=water_meters, project_id=project_id,
            type_id=type_id, tag_id=tag_id, start_time=start_time, end_time=end_time)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_last_consumption_data_by_water_meter_view(self, request):
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

        result, data = self.serializer_class.user_get_last_consumption_data_by_water_meter_serializer(
            token=token, water_meter_serial=water_meter_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_consumptions_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'consumption_id' in input_data:
            consumption_id = input_data["consumption_id"]
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است consumption_id",
                                  english_message="consumption_id is Null.")

        result, data = self.serializer_class.user_get_one_consumptions_view_serializer(
            token=token, consumption_id=consumption_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_cumulative_consumptions_per_tag_view(self, request):
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

        if 'water_meter_serial' not in input_data:
            water_meter_serial = None
        else:
            water_meter_serial = input_data["water_meter_serial"]
        if 'water_meter_tag' not in input_data:
            water_meter_tag = None
        else:
            water_meter_tag = input_data["water_meter_tag"]
        if 'sort_value' not in input_data:
            sort_value = None
        else:
            sort_value = input_data["sort_value"]
        if 'reverse' not in input_data:
            reverse = None
        else:
            reverse = input_data["reverse"]
        result, data = self.serializer_class.user_get_cumulative_consumptions_serializer(
            token=token, page=page, count=count, water_meter_serial=water_meter_serial, water_meter_tag=water_meter_tag,
            sort_value=sort_value,
            input_reverse=reverse)
        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------AddViews--------------------------------------------------------
    @csrf_exempt
    def add_consumptions_water_meter_view(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["value", "water_meters", "information", "module_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'cumulative_value' not in input_data:
            cumulative_value = None
        else:
            cumulative_value = input_data['cumulative_value']

        if 'from_previous_record' not in input_data:
            from_previous_record = None
        else:
            from_previous_record = input_data['from_previous_record']
        if 'to_current_record' not in input_data:
            to_current_record = None
        else:
            to_current_record = input_data['to_current_record']
        if 'create_time' not in input_data:
            create_time = None
        else:
            create_time = input_data['create_time']
        value = input_data["value"]
        water_meters = input_data["water_meters"]
        information = input_data["information"]
        module_code = input_data["module_code"]
        result, data = self.serializer_class.add_consumptions_water_meter_serializer(
            token=token, value=value, water_meters=water_meters, information=information, module_code=module_code,
            from_previous_record_input=from_previous_record, to_current_record_input=to_current_record,
            create_time_input=create_time, cumulative_value=cumulative_value)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def v1_add_consumptions_water_meter_view(self, request):

        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["value", "water_meters", "information", "module_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'cumulative_value' not in input_data:
            cumulative_value = None
        else:
            cumulative_value = input_data['cumulative_value']
        value = input_data["value"]
        water_meters = input_data["water_meters"]
        information = input_data["information"]
        module_code = input_data["module_code"]
        result, data = self.serializer_class.v1_add_consumptions_water_meter_serializer(
            token=token, value=value, water_meters=water_meters, information=information, module_code=module_code,
            cumulative_value=cumulative_value)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def v2_add_consumptions_water_meter_view(self, request):

        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["value", "water_meters", "information", "module_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'cumulative_value' not in input_data:
            cumulative_value = None
        else:
            cumulative_value = input_data['cumulative_value']

        if 'from_previous_record' not in input_data:
            from_previous_record = None
        else:
            from_previous_record = input_data['from_previous_record']
        if 'to_current_record' not in input_data:
            to_current_record = None
        else:
            to_current_record = input_data['to_current_record']
        if 'create_time' not in input_data:
            create_time = None
        else:
            create_time = input_data['create_time']
        value = input_data["value"]
        water_meters = input_data["water_meters"]
        information = input_data["information"]
        module_code = input_data["module_code"]
        result, data = self.serializer_class.v2_add_consumptions_water_meter_serializer(
            token=token, value=value, water_meters=water_meters, information=information, module_code=module_code,
            from_previous_record_input=from_previous_record, to_current_record_input=to_current_record,
            create_time_input=create_time, cumulative_value=cumulative_value)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def add_level_gauge_consumptions_water_meter_view(self, request):

        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["value", "water_meters", "information", "module_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        if 'cumulative_value' not in input_data:
            cumulative_value = None
        else:
            cumulative_value = input_data['cumulative_value']
        value = input_data["value"]
        water_meters = input_data["water_meters"]
        information = input_data["information"]
        module_code = input_data["module_code"]
        result, data = self.serializer_class.add_level_gauge_consumptions_water_meter_serializer(
            token=token, value=value, water_meters=water_meters, information=information, module_code=module_code,
            cumulative_value=cumulative_value)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
    # ------------------------------------------------------------------------------------------------------------------
