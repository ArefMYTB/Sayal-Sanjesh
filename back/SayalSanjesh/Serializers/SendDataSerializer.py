import requests
import json
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from TCPConnection.client import send_message_to_node


class SendDataSerializer:
    @staticmethod
    def admin_send_data_serializer(token, data_message):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):

                response = send_message_to_node(data=data_message)
                print(response)
                if response == 'OK':
                    return True, status_success_result
                else:
                    wrong_data_result['farsi_message'] = ''
                    wrong_data_result['english_message'] = response

                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result

    # @staticmethod
    # def admin_send_order_by_sms_serializer(token, phone_number, order):
    #     token_result = token_to_user_id(token)
    #     if token_result["status"] == "OK":
    #         admin_id = token_result["data"]["user_id"]
    #         if AdminsSerializer.admin_check_permission(admin_id, ''):
    #             SendDataSerializer.send_order_sms(phone_number=phone_number,order=order)
    #             return True, status_success_result
    #
    #         else:
    #             return False, wrong_token_result
    #     else:
    #
    #         return False, wrong_token_result
    #
    # @staticmethod
    # def send_order_sms(phone_number, order):
    #     try:
    #         url = "https://api.sms.ir/v1/send/verify"
    #         payload = {
    #             "mobile": phone_number,
    #             "templateId": 707833,
    #             "parameters": [
    #                 {
    #                     "name": "ORDER",
    #                     "value": order
    #                 },
    #
    #             ]
    #         }
    #         headers = {
    #             'X-API-KEY': 'Zkn4SxmAw69DdtXsjHbgqmsQwcj8ohhZYfmaE5iujDzC4PcdwdVjdDRUH0bVGjue',
    #             'Content-Type': "application/json",
    #             'ACCEPT': 'application/json'
    #         }
    #         response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    #         print(response.json())
    #     except:
    #         pass
