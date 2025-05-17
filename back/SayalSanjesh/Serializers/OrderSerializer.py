import json
from Authorization.TokenManager import token_to_user_id
from Authorization.Serializers.StaticTokenSerializer import StaticTokenSerializer
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from SayalSanjesh.models import OrderType, Order, WaterMeters
from MQQTReceiver.publisher import ResponsePublisher


class OrderSerializer:
    @staticmethod
    def admin_get_all_order_serializer(token, page, count, order_meter, order_type_id, order_type_code):
        """
            param : [token, page, count, order_meter, order_type_id, order_type_code]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderList'):
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "order_type__order_type_id": order_type_id,
                    "order_type__order_type_code": order_type_code,
                    "order_meter": order_meter,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = Order.objects.filter(**filters).order_by('-order_create_time')[offset:offset + limit]
                # all_orders = queryset.count()
                response = Order.objects.serialize(queryset=queryset)
                # for order in queryset:
                #     order['all_orders_number'] = all_orders
                return True, response
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result

    @staticmethod
    def admin_get_one_order_serializer(token, order_id):
        """
            param : [token, order_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderDetail'):

                try:
                    queryset = Order.objects.get(order_id=order_id)
                    response = Order.objects.serialize(queryset=queryset)
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
    def admin_remove_order_serializer(token, order_id):
        """
            param : [token, order_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderDelete'):

                try:
                    order = Order.objects.get(order_id=order_id)
                    order.delete()
                except:
                    wrong_data_result["farsi_message"] = "ای دی  ورودی اشتباه است"
                    wrong_data_result["english_message"] = "input ID are wrong"
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def create_order_serializer(
            token, order_type_id_list, water_meter_serial, order_information):
        """
            param : [token, order_type_id, water_meter_serial, order_information]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'OrderCreate'):
                try:
                    order_meter_obj = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                    response_publisher_class = ResponsePublisher()
                    publish_prepared_data = {
                        "DevInfo": {
                            "SerialNum": water_meter_serial
                        }
                    }
                    check_order = Order.objects.filter(order_meter=order_meter_obj, order_status=-1)
                    check_order_types = check_order.values_list('order_type', flat=True)
                    check_order_types = list(map(lambda x: str(x), check_order_types))
                    for obj in order_type_id_list:
                        if obj in check_order_types:
                            order_type_code = OrderType.objects.get(order_type_id=obj).order_type_code
                            wrong_data_result["farsi_message"] = f" قبلا انتخاب شده {order_type_code}"
                            wrong_data_result["english_message"] = f"{order_type_code} already selected"
                            wrong_data_result["code"] = 444
                            return False, wrong_data_result
                    if len(check_order) > 0:
                        for obj in check_order:
                            publish_prepared_data[f"{obj.order_type.order_type_code}"] = {
                                'Counter': obj.order_counter,
                                'Status': -1
                            }
                    for order_type_id in order_type_id_list:
                        order_type_obj = OrderType.objects.get(order_type_id=order_type_id)
                        last_object = Order.objects.filter(order_meter=order_meter_obj).order_by(
                            'order_create_time').last()
                        if last_object is not None:
                            order_counter = last_object.order_counter + 1
                        else:
                            order_counter = 0
                        response = Order.objects.create(order_type=order_type_obj, order_meter=order_meter_obj,
                                                        order_information=order_information,
                                                        order_counter=order_counter)
                        publish_prepared_data[f'{response.order_type.order_type_code}'] = {
                            'Counter': order_counter,
                            'Status': -1
                        }
                    # publish to meter topic
                    response_publisher_class.send_commands(topic_name=f'/meters/commands/{water_meter_serial}',
                                                           message=json.dumps(publish_prepared_data))
                except:
                    wrong_data_result["farsi_message"] = "ای دی های ورودی اشتباه است"
                    wrong_data_result["english_message"] = "The input IDs are incorrect"
                    wrong_data_result["code"] = 444
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
