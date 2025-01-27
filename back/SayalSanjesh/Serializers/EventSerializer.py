import pytz
from datetime import datetime
from Authorization.TokenManager import token_to_user_id
from Authorization.Serializers.StaticTokenSerializer import StaticTokenSerializer
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from Authorization.models.Admins import Admins
from SayalSanjesh.models import EventType, WaterMetersModules, Event, WaterMeters, EventView
from MQQTReceiver import websockets_publisher
from General.Serializers.LogSerializers import LogSerializers

class EventSerializer:
    @staticmethod
    def admin_get_all_event_serializer(token, page, count, module_id, module_code):
        """
            param : [token, page, count, module_id, module_code]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'EventList'):
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "event_module__water_meter_module_code": module_code,
                    "event_module__water_meter_module_id": module_id,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = Event.objects.filter(**filters).order_by('-event_create_time')[offset:offset + limit]
                response = Event.objects.serialize(queryset=queryset ,admin_id = admin_id)
                return True, response
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result

    @staticmethod
    def admin_get_one_event_serializer(token, event_id):
        """
            param : [token, event_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'EventDetail'):

                try:
                    event = Event.objects.get(event_id=event_id)
                    event_result = event.as_dict()
                    return True, event_result
                except:
                    wrong_data_result["farsi_message"] = "ای دی های ورودی اشتباه است"
                    wrong_data_result["english_message"] = "input IDs are wrong"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_remove_event_serializer(token, event_id):
        """
            param : [token, event_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'EventDelete'):

                try:
                    event = Event.objects.get(event_id=event_id)
                    event.delete()
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=event_id, system_log_action_table='Event')
                except:
                    wrong_data_result["farsi_message"] = "ای دی  ورودی اشتباه است"
                    wrong_data_result["english_message"] = "input ID are wrong"
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def create_event_serializer(
            token, event_type_code, meter_serial, event_count, event_information, event_counter,
            event_last_occurrence, event_create_time, event_module_code=None):
        """
            param : [token, event_type_code, event_module_code, event_value, event_information]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:

            try:
                event_type_obj = EventType.objects.get(event_type_code=event_type_code)
                if event_module_code is None:
                    event_module_id = WaterMeters.objects.get(water_meter_serial=meter_serial).water_meter_module_id
                    event_module_obj = WaterMetersModules.objects.get(water_meter_module_id=event_module_id)
                else:
                    event_module_obj = WaterMetersModules.objects.get(water_meter_module_code=event_module_code)
                utc_timezone = pytz.utc
                utc_event_create_time = utc_timezone.localize(datetime.strptime(event_create_time, '%m/%d/%Y-%H:%M:%S'))
                utc_event_last_occurrence = utc_timezone.localize(
                    datetime.strptime(event_last_occurrence, '%m/%d/%Y-%H:%M:%S'))

                Event.objects.create(event_type=event_type_obj, event_module=event_module_obj,
                                     event_count=event_count,
                                     event_information=event_information,
                                     event_last_occurrence=utc_event_last_occurrence,
                                     event_counter=event_counter,
                                     event_create_time=utc_event_create_time)
            except:
                wrong_data_result["farsi_message"] = "ای دی های ورودی اشتباه است"
                wrong_data_result["english_message"] = "The input IDs are incorrect"
                wrong_data_result["code"] = 444
                return False, wrong_data_result
            # # call mqtt event publisher
            water_meter_object = WaterMeters.objects.get(water_meter_serial=meter_serial)
            prepared_data = {
                "project_id": str(water_meter_object.water_meter_project.water_meter_project_id),
                "meter_serial": str(water_meter_object.water_meter_serial),
                "event_type_keyword": str(event_type_code),
                "event_type_code": str(event_type_code),
            }
            websockets_publisher.publish_event_message(data_dict=prepared_data)
            # print(f"publish_response :{publish_response}")
            return True, status_success_result
        else:
            return False, wrong_token_result

    @staticmethod
    def get_last_event_counter(token, meter_serial, event_create_time):
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result is None:
            event_module_obj = WaterMeters.objects.get(water_meter_serial=meter_serial).water_meter_module_id
            utc_timezone = pytz.utc
            utc_event_create_time = utc_timezone.localize(datetime.strptime(event_create_time, '%m/%d/%Y-%H:%M:%S'))
            last_counter = Event.objects.filter(event_module=event_module_obj,
                                                event_create_time=utc_event_create_time)
            if len(last_counter) == 1:
                prepared_data = {
                    "SendResponse": True,
                    "event_counter": int(last_counter.last().event_counter)
                }
                return True, prepared_data
            else:
                prepared_data = {
                    "SendResponse": False,
                    "event_counter": int(last_counter.last().event_counter)
                }
                return True, prepared_data
        else:
            return False, wrong_token_result

    # -------------------------------------------------EventView--------------------------------------------------------
    @staticmethod
    def admin_create_event_view_serializer(token, event_id_list):
        """
                    param : [token, event_id_list]
                    return :
                    A tuple containing a boolean indicating the success or failure of the operation, and a list of
                    serialized data results.  it returns a false status along with an error message.
                """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Event'):
                for id in event_id_list:
                    event_obj = Event.objects.get(event_id = id)
                    admin_obj = Admins.objects.get(admin_id = admin_id)
                    EventView.objects.create(admin=admin_obj, event=event_obj)
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result
    # ------------------------------------------------------------------------------------------------------------------
