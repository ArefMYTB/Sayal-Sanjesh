from django.db.models import Sum, Count
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMetersTypes, WaterMetersProjects, WaterMeters, WaterMetersTags, \
    WaterMetersConsumptions, ModuleTypes
from Authorization.models.Admins import Admins
from Authorization.models.MiddleAdmins import MiddleAdmins
from General.models import Utils
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.FileUploadHandler import FileManager
from General.Serializers.LogSerializers import LogSerializers


class ModuleTypesSerializer:

    @staticmethod
    def admin_add_module_type_serializer(token, module_type_name, module_other_information):
        """
            param : [token, module_type_name, module_other_information]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):

                admin = Admins.objects.get(admin_id=admin_id)

                fields = {
                    "module_type_name": (module_type_name, str)
                }
                result = wrong_result(fields)
                if result == None:
                    ModuleTypes.objects.create(admin=admin, module_type_name=module_type_name,
                                               module_other_information=module_other_information)
                    # ----- add to loger -------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=module_type_name,
                        system_log_action_table='ModuleTypes')
                    # -------------------------
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_edit_module_type_serializer(token, module_type_id, module_type_name, module_other_information):
        """
            param : [token, water_meter_tag_id, water_meter_type_new_name, water_meter_type_id,
                                    water_meter_type_other_information, filepath]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                # admin = Admins.objects.get(admin_id=admin_id)
                fields = {
                    "module_type_name": (module_type_name, str)
                }

                result = wrong_result(fields)
                if result == None:
                    try:
                        Update_module_type = ModuleTypes.objects.get(module_type_id=module_type_id)
                        first_device_state_dict = {
                            "module_type_name": Update_module_type.module_type_name,
                            "module_type_create_date": Update_module_type.module_type_create_date,
                            "module_other_information": Update_module_type.module_other_information,
                        }
                        Update_module_type.module_type_name = module_type_name
                        Update_module_type.module_other_information = module_other_information
                        Update_module_type.save()
                        # ---------add to logger --------
                        second_state_query = ModuleTypes.objects.get(module_type_id=module_type_id)
                        second_device_state_dict = {
                            "module_type_name": second_state_query.module_type_name,
                            "module_type_create_date": second_state_query.module_type_create_date,
                            "module_other_information": second_state_query.module_other_information,
                        }
                        changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                          first_device_state_dict if
                                          first_device_state_dict[key] != second_device_state_dict[key]}
                        system_log_message = ''
                        for key, values in changed_fields.items():
                            system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                        admin_obj = Admins.objects.get(admin_id=admin_id)
                        LogSerializers().system_log_create_serializer(token=token, system_log_admin=admin_obj,
                                                                      system_log_user=None,
                                                                      system_log_object_action_on=module_type_id,
                                                                      system_log_action='Edit',
                                                                      system_log_action_table='ModuleTypes',
                                                                      system_log_message=system_log_message,
                                                                      system_log_field_changes=changed_fields)
                        # -------------------------
                        return True, status_success_result
                    except:
                        wrong_data_result[
                            "farsi_message"] = "کنتوری با این تایپ وجود دارد یا ای دی های ورودی اشتباه است"
                        wrong_data_result["english_message"] = "water meter with this type is already exist."
                        return False, wrong_data_result
                    # if updated_water_meter == 1:
                    #     return True, status_success_result
                    # else:
                    #     return False, wrong_data_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_module_type_serializer(token, module_type_id):
        """
            param : [token, water_meter_type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                try:
                    deleted_item = ModuleTypes.objects.filter(module_type_id=module_type_id).delete()
                    # ------------ add to logger -------------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=module_type_id,
                        system_log_action_table='ModuleTypes')
                    # ---------------------------------------
                except:
                    wrong_data_result["farsi_message"] = "کنتور این تایپ هنوز حذف نشده امکان تغییر و یا حذف وجود ندارد"
                    wrong_data_result["english_message"] = "water meter with this type is already exist."
                    return False, wrong_data_result
                if deleted_item[0] == 0:
                    wrong_data_result["farsi_message"] = "module_type_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong module_type_id"
                    return False, wrong_data_result
                else:
                    return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_module_type_serializer(token, module_type_name, page, count):
        """
            param : [token, module_type_name, page, count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        "module_type_name__contains": module_type_name,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    queryset = ModuleTypes.objects.filter(**filters).order_by(
                        '-module_type_create_date')[offset:offset + limit]
                    response = ModuleTypes.objects.serialize(queryset=queryset)
                    return True, response
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_module_type_serializer(token, module_type_id):
        """
            param : [token, water_meter_type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ModuleTypeDetial'):
                try:
                    queryset = ModuleTypes.objects.filter(
                        module_type_id=module_type_id)
                    response = ModuleTypes.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "water_meter_type_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong water_meter_type_id"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

