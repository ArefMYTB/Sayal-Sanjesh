import requests
import json
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from TCPConnection.client import send_message_to_node


class SendDataSerializer:
    @staticmethod
    def admin_send_data_serializer(token, data_message):
        """
            param : [token, data_message]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Admin'):

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

