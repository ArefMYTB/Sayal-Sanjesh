from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import  WaterMeters, CalculateUnites
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class CalculateUnitesSerializer():

    @staticmethod
    def admin_add_calculate_unites_serializer(token, water_meter_serial, calculate_unites):
        """
            param : [token, water_meter_serial, calculate_unites]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Consumption'):
                admin = Admins.objects.get(admin_id=admin_id)
                try:
                    water_meter = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                    calculateUnits = CalculateUnites()
                    calculateUnits.admin = admin
                    calculateUnits.calculate_unites = calculate_unites
                    calculateUnits.calculate_water_meter = water_meter
                    calculateUnits.save()
                except:
                    wrong_data_result["farsi_message"] = "water_meter_serial اشتباه است"
                    wrong_data_result["english_message"] = "wrong water_meter_serial"
                    return False, wrong_data_result

                return True, status_success_result

            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_calculate_unites_serializer(token, calculate_id):
        """
            param : [token, calculate_id]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Consumption'):
                try:
                    CalculateUnites.objects.filter(calculate_id=calculate_id).delete()
                except:
                    wrong_data_result["farsi_message"] = "calculate_id وجود ندارد"
                    wrong_data_result["english_message"] = "wrong calculate_id"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_calculate_price_serializer(token, page, count):
        """
            param : [token, page, count]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Consumption'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    try:
                        all_calculate_unit = CalculateUnites.objects.all()
                        all_calculate_unit_pagination = all_calculate_unit.order_by(
                            '-calculate_create_date')[offset:offset + limit]
                        calculate_unit_result = [calculate_unit.as_dict() for calculate_unit in
                                                 all_calculate_unit_pagination]
                    except:
                        wrong_data_result["farsi_message"] = ""
                        wrong_data_result["english_message"] = "field"
                        return False, wrong_data_result
                    return True, calculate_unit_result
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
