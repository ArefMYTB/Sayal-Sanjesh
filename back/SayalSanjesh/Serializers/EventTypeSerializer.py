from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import EventType
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class EventTypeSerializer:
    @staticmethod
    def admin_get_all_event_types_serializer(token, page, count):
        """
            param : [token, page, count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                offset = int((page - 1) * count)
                limit = int(count)
                queryset = EventType.objects.all().order_by('event_type_create_time')[offset:offset + limit]
                response = EventType.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:

            return False, wrong_token_result

    @staticmethod
    def admin_get_one_event_type_serializer(token, event_type_id, event_type_code):
        """
            param : [token, event_type_id, event_type_code]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                filters = {
                    "event_type_id": event_type_id,
                    "event_type_code": event_type_code,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                try:
                    queryset = EventType.objects.get(**filters)
                    response = EventType.objects.serialize(queryset=queryset)
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
    def admin_remove_event_type_serializer(token, event_type_id):
        """
            param : [token, event_type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):

                try:
                    event_type = EventType.objects.get(event_type_id=event_type_id)
                    event_type.delete()
                except:
                    wrong_data_result["farsi_message"] = "حذف غیرمجاز"
                    wrong_data_result["english_message"] = "Invalid Deletion"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_create_event_type_serializer(
            token, event_type_keyword, event_type_importance, evnet_type_information):
        """
            param : [token, event_type_keyword, event_type_importance, evnet_type_information]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                admin = Admins.objects.get(admin_id=admin_id)
                importance_choice = ('H', 'M', 'L')
                if event_type_importance not in importance_choice:
                    wrong_data_result[
                        "farsi_message"] = "فیلد event_type_importance باید از بین 'H', 'M', 'L' انتخاب شود"
                    wrong_data_result[
                        "english_message"] = "event_type_importance field must be selected from 'H', 'M', 'L'"
                    wrong_data_result["code"] = 444
                    return False, wrong_data_result
                try:
                    # get all events to check event number
                    event_type_codes = list(
                        map(lambda x: int(x['event_type_code']), EventType.objects.all().values('event_type_code')))
                    generate_event_type_code = max(event_type_codes) + 1
                    key = '{:03d}'.format(generate_event_type_code)

                    # event_type_codes = list(map(lambda x: int(x['event_type_code']), event_type_codes))
                    # missing_code = sorted(set(range(event_type_codes[0], event_type_codes[-1])) - set(event_type_codes))
                    # if len(missing_code) > 0:
                    #     event_type_code = min(missing_code)
                    # else:
                    #     event_type_code = max(event_type_codes) + 1
                    # key = '{:03d}'.format(event_type_code)
                    EventType.objects.create(event_type_admin=admin, event_type_code=key,
                                             event_type_keyword=event_type_keyword,
                                             event_type_importance=event_type_importance,
                                             evnet_type_information=evnet_type_information)
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

    @staticmethod
    def admin_edit_event_type_serializer(
            token, event_type_id, event_type_dashboard_view, event_type_importance, evnet_type_information):
        """
            param : [token, event_type_keyword, event_type_importance, evnet_type_information]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                admin = Admins.objects.get(admin_id=admin_id)
                importance_choice = ('H', 'M', 'L')
                if event_type_importance is not None and event_type_importance not in importance_choice:
                    wrong_data_result[
                        "farsi_message"] = "فیلد event_type_importance باید از بین 'H', 'M', 'L' انتخاب شود"
                    wrong_data_result[
                        "english_message"] = "event_type_importance field must be selected from 'H', 'M', 'L'"
                    wrong_data_result["code"] = 444
                    return False, wrong_data_result
                try:
                    filters = {
                        'event_type_dashboard_view': event_type_dashboard_view,
                        'event_type_importance': event_type_importance,
                        'evnet_type_information': evnet_type_information,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    update = EventType.objects.filter(event_type_id=event_type_id).update(**filters)
                    if update == 0:
                        wrong_data_result["farsi_message"] = "event_type_id اشتباه است"
                        wrong_data_result["english_message"] = "invalid event_type_id"
                        wrong_data_result["code"] = 444
                        return False, wrong_data_result
                except:
                    wrong_data_result["farsi_message"] = "event_type_id اشتباه است"
                    wrong_data_result["english_message"] = "invalid event_type_id"
                    wrong_data_result["code"] = 444
                    return False, wrong_data_result
                return True, status_success_result
            else:
                wrong_token_result['code'] = 403
                return False, wrong_token_result
        else:
            wrong_token_result['code'] = 403
            return False, wrong_token_result
