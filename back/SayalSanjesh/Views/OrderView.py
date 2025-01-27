from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.OrderSerializer import OrderSerializer


@csrf_exempt
class OrderView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """
    @csrf_exempt
    def admin_get_all_order_view(self, request):
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
        fields = ["page", "count", "order_meter", "order_type_id", "order_type_code"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data["page"]
        count = input_data["count"]
        order_meter = input_data["order_meter"]
        order_type_id = input_data["order_type_id"]
        order_type_code = input_data["order_type_code"]

        result, data = OrderSerializer.admin_get_all_order_serializer(token=token, page=page, count=count,
                                                                      order_meter=order_meter,
                                                                      order_type_id=order_type_id,
                                                                      order_type_code=order_type_code)
        print('result, data')
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_order_view(self, request):
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
        fields = ["order_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        order_id = input_data['order_id']
        result, data = OrderSerializer.admin_get_one_order_serializer(
            token=token, order_id=order_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_remove_order_view(self, request):
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
        fields = ["order_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        order_id = input_data['order_id']

        result, data = OrderSerializer.admin_remove_order_serializer(
            token=token, order_id=order_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def create_order_view(self, request):
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
        fields = ['order_type_id_list', 'water_meter_serial', 'order_information']
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        order_type_id_list = input_data["order_type_id_list"]
        water_meter_serial = input_data["water_meter_serial"]
        order_information = input_data["order_information"]
        result, data = OrderSerializer.create_order_serializer(
            token=token, order_type_id_list=order_type_id_list, water_meter_serial=water_meter_serial,
            order_information=order_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
