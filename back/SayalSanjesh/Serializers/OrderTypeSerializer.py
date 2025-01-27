from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import OrderType
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.Serializers.LogSerializers import LogSerializers


class OrderTypeSerializer:
    @staticmethod
    def admin_get_all_order_types_serializer(token, page, count):
        """
            param : [token, page, count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderTypeList'):
                offset = int((page - 1) * count)
                limit = int(count)
                queryset = OrderType.objects.all().order_by('order_type_create_time')[offset:offset + limit]
                response = OrderType.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result

    @staticmethod
    def admin_get_one_order_type_serializer(token, order_type_id, order_type_code):
        """
            param : [token, order_type_id, order_type_code]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderTypeDetail'):
                filters = {
                    "order_type_id": order_type_id,
                    "order_type_code": order_type_code,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                try:
                    queryset = OrderType.objects.get(**filters)
                    response = OrderType.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "ای دی های ورودی اشتباه است"
                    wrong_data_result["english_message"] = "input IDs are wrong"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_remove_order_type_serializer(token, order_type_id):
        """
            param : [token, order_type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderTypeRemove'):

                try:
                    order_type = OrderType.objects.get(order_type_id=order_type_id)
                    order_type.delete()
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=order_type_id, system_log_action_table='OrderType')
                except:
                    wrong_data_result["farsi_message"] = "ای دی های ورودی اشتباه است"
                    wrong_data_result["english_message"] = "input IDs are wrong"
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_create_order_type_serializer(
            token, order_type_name, order_type_information):
        """
            param : [token, order_type_name, order_type_information]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderTypeCreate'):
                admin = Admins.objects.get(admin_id=admin_id)

                try:
                    # get all orders to check order number
                    order_type_codes = list(
                        map(lambda x: int(x['order_type_code']), OrderType.objects.all().values('order_type_code')))
                    generate_order_type_code = max(order_type_codes) + 1
                    key = '{:03d}'.format(generate_order_type_code)

                    OrderType.objects.create(order_type_admin=admin, order_type_code=key,
                                             order_type_name=order_type_name,
                                             order_type_information=order_type_information)
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=order_type_name, system_log_action_table='OrderType')
                except:
                    wrong_data_result["farsi_message"] = "خطای نامشخص"
                    wrong_data_result["english_message"] = "unknown error"
                    wrong_data_result["code"] = 444
                    return False, wrong_data_result
                return True, status_success_result
            else:
                wrong_token_result['code'] = 403
                return False, wrong_token_result
        else:
            wrong_token_result['code'] = 403
            return False, wrong_token_result
