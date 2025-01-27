from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.SendDataSerializer import SendDataSerializer


@csrf_exempt
class DataView:

    @csrf_exempt
    def admin_send_data_view(self, request):
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
        fields = ["data_message"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        data_message = input_data["data_message"]

        result, data = SendDataSerializer.admin_send_data_serializer(
            token=token, data_message=data_message)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    # @csrf_exempt
    # def admin_send_order_by_sms_view(self, request):
    #     if request.method.lower() == "options":
    #         return result_creator()
    #     try:
    #         input_data = json.loads(request.body)
    #     except:
    #         return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
    #                               english_message="invalid JSON error")
    #     if "Token" in request.headers:
    #         token = request.headers["Token"]
    #     else:
    #         token = ''
    #     fields = ["phone_number", "order_type"]
    #     for field in fields:
    #         if field not in input_data:
    #             return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
    #                                   english_message=f"{field} is Null.")
    #     phone_number = input_data["phone_number"]
    #     order_type = input_data["order_type"]
    #
    #     result, data = SendDataSerializer.admin_send_order_by_sms_serializer(
    #         token=token, phone_number=phone_number, order_type=order_type)
    #     if result:
    #         return result_creator(data=data)
    #     else:
    #         return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
    #                               english_message=data["english_message"])
