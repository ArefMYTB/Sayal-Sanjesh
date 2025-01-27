from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from General.models.Log import MqttLoger, SystemLog
from Authorization.models.Admins import Admins


class LogSerializers:
    """
        A view class for handling GET and POST requests.

        Methods:
        - get: Handles GET requests and returns a JSON response.
        - post: Handles POST requests and returns a JSON response.
    """

    @staticmethod
    def admin_check_permission(admin_id, permission):
        """
            param : [admin_id, permission]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        admin = Admins.objects.get(admin_id=admin_id)
        if type(permission) == str:
            if permission in admin.admin_permissions:
                return True
            else:
                return False
        else:
            counter = len(permission)
            counter_checker = 0
            for per in permission:
                if per in admin.admin_permissions:
                    counter_checker += 1
                else:
                    pass
            if counter_checker == counter:
                return True
            else:
                return False

    # -------------------------------------------------MqttLoger--------------------------------------------------------
    @staticmethod
    def admin_get_all_mqtt_log_serializer(token, page, count, message__icontains):
        """
                    param : [token]

                    return :
                    A tuple containing a boolean indicating the success or failure of the operation, and a list of
                    serialized data
                    results.  it returns a false status along with an error message.
                """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            offset = int((page - 1) * count)
            limit = int(count)
            filters = {
                "message__icontains": message__icontains
            }
            filters = {k: v for k, v in filters.items() if v is not None}
            queryset = MqttLoger.objects.filter(**filters).order_by('-create_date')[offset:offset + limit]
            response = MqttLoger.objects.serialize(queryset=queryset)
            return True, response
        else:
            return False, wrong_token_result

    # ------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------SystemLog--------------------------------------------------------
    @staticmethod
    def system_log_create_serializer(token, system_log_admin, system_log_user, system_log_action, system_log_message,
                                     system_log_action_table, system_log_field_changes, system_log_object_action_on):
        """
                    param : [token, system_log_admin, system_log_user, system_log_action, system_log_message]

                    return :
                    A tuple containing a boolean indicating the success or failure of the operation, and a list of
                    serialized data
                    results.  it returns a false status along with an error message.
                """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            valid_log_action = ['Add', 'Edit', 'Delete']
            if system_log_action not in valid_log_action:
                wrong_data_result["farsi_message"] = "قادیر مجاز برایsystem_log_action  : ['Add', 'Edit', 'Delete']"
                wrong_data_result["english_message"] = "valid system_log_action  is : ['Add', 'Edit', 'Delete']"
                return False, wrong_data_result

            SystemLog.objects.create(system_log_admin=system_log_admin, system_log_user=system_log_user,
                                     system_log_action=system_log_action, system_log_message=system_log_message,
                                     system_log_action_table=system_log_action_table,
                                     system_log_field_changes=system_log_field_changes,
                                     system_log_object_action_on=system_log_object_action_on)

            return True, status_success_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_system_log_view(token, page, count, system_log_action, system_log_object_action_on__search,
                                      system_log_action_table):
        """
            param : [token, page, count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if LogSerializers.admin_check_permission(admin_id, 'LogList'):
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "system_log_action": system_log_action,
                    "system_log_action_table": system_log_action_table,
                    "system_log_object_action_on__search": system_log_object_action_on__search
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = SystemLog.objects.filter(**filters).order_by('-system_log_create_time')[
                           offset:offset + limit]
                response = SystemLog.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result
    # ------------------------------------------------------------------------------------------------------------------
