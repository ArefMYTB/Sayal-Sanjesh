from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMetersRequests
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class WaterMeterRequestsSerializer:

    @staticmethod
    def admin_add_water_meter_request_serializer(token, water_meter_request_title, water_meter_request_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'WaterMeterModule'):

                admin = Admins.objects.get(admin_id=admin_id)

                fields = {
                    "water_meter_request_title": (water_meter_request_title, str)
                }
                result = wrong_result(fields)
                if result == None:
                    try:
                        WaterMetersRequests.objects.create(
                            admin=admin, water_meter_request_title=water_meter_request_title,
                            water_meter_request_information=water_meter_request_information)
                    except:
                        wrong_data_result["farsi_message"] = ""
                        wrong_data_result["english_message"] = "something wrong"
                        return False, wrong_data_result
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_edit_water_meter_request_serializer(token, water_meter_request_id, water_meter_request_title,
                                                  water_meter_request_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'WaterMeterModule'):
                fields = {
                    "water_meter_module_name": (water_meter_request_title, str)
                }

                result = wrong_result(fields)
                if result == None:
                    try:
                        request = WaterMetersRequests.objects.get(water_meter_request_id=water_meter_request_id)
                        request.water_meter_request_title = water_meter_request_title
                        request.water_meter_request_information = water_meter_request_information
                        request.save()
                        return True, status_success_result
                    except:
                        wrong_data_result["farsi_message"] = "ای دی اشتباه است"
                        wrong_data_result["english_message"] = "id is wrong."
                        return False, wrong_data_result

                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_water_meter_request_serializer(token, water_meter_request_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'WaterMeterModule'):
                try:
                    request = WaterMetersRequests.objects.get(water_meter_request_id=water_meter_request_id)
                    request.delete()
                    return True, status_success_result
                except:
                    wrong_data_result["farsi_message"] = "ای دی اشتباه است"
                    wrong_data_result["english_message"] = "water_meter_module_id is wrong"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meter_request_serializer(token, water_meter_request_title, water_meter_request_create_date,
                                                     page, count):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'WaterMeterModule'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    all_requests = WaterMetersRequests.objects.filter(
                        water_meter_request_title__contains=water_meter_request_title,
                        water_meter_request_create_date__contains=water_meter_request_create_date).order_by(
                        '-water_meter_request_create_date')[offset:offset + limit]
                    requests = [req.as_dict() for req in all_requests]
                    return True, requests
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_water_meter_request_serializer(token, water_meter_request_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'WaterMeterModule'):
                try:
                    request = WaterMetersRequests.objects.get(water_meter_request_id=water_meter_request_id)
                except:
                    wrong_data_result["farsi_message"] = "ای دی ماژول اشتباه است"
                    wrong_data_result["english_message"] = "water_meter_module_id is wrong."
                    return False, wrong_data_result
                req = request.as_dict()
                return True, req
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
