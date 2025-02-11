from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.BillsSerializer import BillsSerializer


@csrf_exempt
class BillsView:
    # TODO edit user getALl like admin.
    @csrf_exempt
    def admin_get_all_bills(self, request):
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
        fields = ["page", "count", "water_meter_serial", "bill_serial", "bill_start_date", "user_id", "bill_end_date",
                  "payment_dead_line", "bill_create_date", "project_id", "user_phone_number"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        water_meter_serial = input_data["water_meter_serial"]
        bill_serial = input_data["bill_serial"]
        bill_start_date = input_data["bill_start_date"]
        user_phone_number = input_data["user_phone_number"]
        user_id = input_data["user_id"]
        project_id = input_data["project_id"]
        bill_end_date = input_data["bill_end_date"]
        payment_dead_line = input_data["payment_dead_line"]
        bill_create_date = input_data["bill_create_date"]
        result, data = BillsSerializer.admin_get_all_bills_serializer(
            token=token, page=page, count=count, water_meter_serial=water_meter_serial, bill_serial=bill_serial,
            bill_start_date=bill_start_date, user_id=user_id, bill_end_date=bill_end_date,
            payment_dead_line=payment_dead_line, bill_create_date=bill_create_date, project_id=project_id,
            user_phone_number=user_phone_number)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_bill(self, request):
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
        fields = ["bill_id", "bill_serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        bill_id = input_data['bill_id']
        bill_serial = input_data['bill_serial']
        result, data = BillsSerializer.admin_get_one_bill_serializer(
            token=token, bill_id=bill_id, bill_serial=bill_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_bill(self, request):
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
        fields = ["bill_id", "payment_dead_line", "other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        bill_id = input_data["bill_id"]
        payment_dead_line = input_data["payment_dead_line"]
        other_information = input_data["other_information"]
        result, data = BillsSerializer.admin_edit_bill_serializer(
            token, bill_id, payment_dead_line, other_information)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_bill(self, request):
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
        if 'bill_id' in input_data:
            bill_id = input_data['bill_id']
        else:
            return result_creator(status="failure", code=406, farsi_message="bill_id .وارد نشده است ",
                                  english_message=" is Null bill_id")

        result, data = BillsSerializer.admin_remove_bill_serializer(token=token, bill_id=bill_id)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_new_bill(self, request):
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
        fields = ["water_meter_serial", "payment_dead_line", "other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data["water_meter_serial"]
        payment_dead_line = input_data["payment_dead_line"]
        other_information = input_data["other_information"]
        result, data = BillsSerializer.admin_create_new_bill_serializer(
            token=token, water_meter_serial=water_meter_serial, payment_dead_line=payment_dead_line,
            other_information=other_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_bill(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'bill_serial' in input_data:
            bill_serial = input_data['bill_serial']
        else:
            return result_creator(status="failure", code=406, farsi_message="bill_serial .وارد نشده است ",
                                  english_message=" is Null bill_serial")

        result, data = BillsSerializer.user_get_one_bill_serializer(token=token, bill_serial=bill_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_bills(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "bill_start_date", "bill_end_date", "water_meter_serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data['page']
        count = input_data['count']
        bill_start_date = input_data["bill_start_date"]
        bill_end_date = input_data["bill_end_date"]
        water_meter_serial = input_data["water_meter_serial"]
        result, data = BillsSerializer.user_get_all_bills_serializer(
            token=token, page=page, count=count, bill_start_date=bill_start_date, bill_end_date=bill_end_date,
            water_meter_serial=water_meter_serial)

        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_create_link(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["bill_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        bill_id = input_data['bill_id']
        result, data = BillsSerializer.user_create_link_serializer(
            token=token, bill_id=bill_id)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_link(self, request):
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        # if "Token" in request.headers:
        #     token = request.headers["Token"]
        # else:
        #     token = ''
        fields = ["bill_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        bill_id = input_data['bill_id']
        result, data = BillsSerializer.user_get_link_serializer(
            bill_id=bill_id)

        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_exel_view(self, request):
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
        fields = ["all_meter_serials", "project_id", "base_price", "meter_tag_id", "start_persian_time",
                  "end_persian_time"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        base_price = input_data['base_price']
        all_meter_serials = input_data['all_meter_serials']
        meter_tag_id = input_data['meter_tag_id']
        start_persian_time = input_data['start_persian_time']
        end_persian_time = input_data['end_persian_time']
        project_id = input_data['project_id']
        result, data = BillsSerializer.admin_create_exel_serializer(
            token=token, project_id=project_id, base_price=base_price, all_meter_serials=all_meter_serials,
            meter_tag_id=meter_tag_id, start_persian_time=start_persian_time, end_persian_time=end_persian_time)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=data["code"], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_power_exel_view(self, request):
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
        fields = ["tag_id", "project_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        tag_id = input_data['tag_id']
        project_id = input_data['project_id']
        result, data = BillsSerializer.admin_create_power_exel_serializer(
            token=token, tag_id=tag_id, project_id=project_id)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=data["code"], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    # version one after first edition
    @csrf_exempt
    def admin_create_new_bill_v1(self, request):
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
        fields = ["water_meter_serial", "payment_dead_line", "start_time", "end_time", "other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        water_meter_serial = input_data["water_meter_serial"]
        payment_dead_line = input_data["payment_dead_line"]
        other_information = input_data["other_information"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]
        result, data = BillsSerializer.admin_create_new_bill_v1_serializer(
            token=token, water_meter_serial=water_meter_serial, payment_dead_line=payment_dead_line,
            other_information=other_information, start_time=start_time, end_time=end_time)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_create_new_bill_list(self, request):
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
        fields = ["meter_serial_list", "payment_dead_line", "start_time", "end_time", "other_information",
                  "calculate_method", "project_id", "tag_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        meter_serial_list = input_data["meter_serial_list"]
        payment_dead_line = input_data["payment_dead_line"]
        other_information = input_data["other_information"]
        start_time = input_data["start_time"]
        end_time = input_data["end_time"]
        calculate_method = input_data["calculate_method"]
        project_id = input_data["project_id"]
        tag_id = input_data["tag_id"]
        result, data = BillsSerializer.admin_create_new_bill_list_serializer(
            token=token, meter_serial_list=meter_serial_list, payment_dead_line=payment_dead_line,
            other_information=other_information, start_time=start_time, end_time=end_time,
            calculate_method=calculate_method, project_id=project_id, tag_id=tag_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data['code'], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def get_one_bill(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        fields = ["bill_id", "bill_serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        bill_id = input_data['bill_id']
        bill_serial = input_data['bill_serial']
        result, data = BillsSerializer.get_one_bill_serializer(
             bill_id=bill_id, bill_serial=bill_serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
