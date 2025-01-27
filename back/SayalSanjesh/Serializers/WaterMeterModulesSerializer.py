from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMetersModules, WaterMeters, WaterMetersRequests, ModuleTypes
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.Serializers.LogSerializers import LogSerializers


class WaterMeterModulesSerializer:

    @staticmethod
    def admin_add_water_meter_module(token, water_meter_module_name, water_meter_module_other_information,
                                     water_meter_module_code, water_meter_module_unit, water_meter_module_sim,
                                     water_meter_module_sim_operator, water_meter_module_property, module_type_id):
        """
            param : [token, water_meter_module_name, water_meter_module_other_information,
                                     water_meter_module_code, water_meter_module_unit]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ModuleCreate'):

                admin = Admins.objects.get(admin_id=admin_id)

                fields = {
                    "water_meter_module_name": (water_meter_module_name, str)
                }
                result = wrong_result(fields)
                if result == None:
                    try:
                        module_type_instance = ModuleTypes.objects.get(module_type_id=module_type_id)
                        WaterMetersModules.objects.create(
                            admin=admin, water_meter_module_name=water_meter_module_name,
                            water_meter_module_other_information=water_meter_module_other_information,
                            water_meter_module_unit=water_meter_module_unit,
                            water_meter_module_code=water_meter_module_code,
                            water_meter_module_sim=water_meter_module_sim,
                            water_meter_module_sim_operator=water_meter_module_sim_operator,
                            water_meter_module_property=water_meter_module_property, module_type=module_type_instance
                        )
                        admin_object = Admins.objects.get(admin_id=admin_id)
                        LogSerializers().system_log_create_serializer(
                            token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                            system_log_field_changes=None, system_log_message=None,
                            system_log_object_action_on=water_meter_module_code,
                            system_log_action_table='WaterMetersModules')
                    except:
                        wrong_data_result["farsi_message"] = "کد تکراری"
                        wrong_data_result["english_message"] = "please enter unique value for code "
                        return False, wrong_data_result
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_edit_water_meter_module(token, water_meter_module_id, water_meter_module_name,
                                      water_meter_module_other_information, water_meter_module_unit,
                                      water_meter_module_sim, water_meter_module_sim_operator,
                                      water_meter_module_property, module_type_id):
        """
            param : [token, water_meter_module_id, water_meter_module_name,
                                      water_meter_module_other_information, water_meter_module_unit]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ModuleEdit'):
                fields = {
                    "water_meter_module_name": (water_meter_module_name, str)
                }

                result = wrong_result(fields)
                if result == None:
                    try:
                        module_type_instance = ModuleTypes.objects.get(module_type_id=module_type_id)
                        module = WaterMetersModules.objects.get(water_meter_module_id=water_meter_module_id)
                        first_device_state_dict = {
                            "water_meter_module_name": module.water_meter_module_name,
                            "water_meter_module_other_information": module.water_meter_module_other_information,
                            "water_meter_module_unit": module.water_meter_module_unit,
                            "water_meter_module_sim": module.water_meter_module_sim,
                            "water_meter_module_sim_operator": module.water_meter_module_sim_operator,
                            "water_meter_module_property": module.water_meter_module_property,
                        }
                        module.water_meter_module_name = water_meter_module_name
                        module.water_meter_module_other_information = water_meter_module_other_information
                        module.water_meter_module_unit = water_meter_module_unit
                        module.water_meter_module_sim = water_meter_module_sim
                        module.water_meter_module_sim_operator = water_meter_module_sim_operator
                        module.water_meter_module_property = water_meter_module_property
                        module.module_type = module_type_instance
                        module.save()
                        second_device_state = WaterMetersModules.objects.get(
                            water_meter_module_id=water_meter_module_id)
                        second_device_state_dict = {
                            "water_meter_module_name": second_device_state.water_meter_module_name,
                            "water_meter_module_other_information": second_device_state.water_meter_module_other_information,
                            "water_meter_module_unit": second_device_state.water_meter_module_unit,
                            "water_meter_module_sim": module.water_meter_module_sim,
                            "water_meter_module_sim_operator": module.water_meter_module_sim_operator,
                            "water_meter_module_property": module.water_meter_module_property,
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
                                                                      system_log_object_action_on=water_meter_module_id,
                                                                      system_log_action='Edit',
                                                                      system_log_action_table='WaterMetersModules',
                                                                      system_log_message=system_log_message,
                                                                      system_log_field_changes=changed_fields)
                        return True, status_success_result
                    except:
                        wrong_data_result["farsi_message"] = "ای دی ماژول اشتباه است"
                        wrong_data_result["english_message"] = "water_meter_module_id is wrong."
                        return False, wrong_data_result

                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_water_meter_module(token, water_meter_module_id):
        """
            param : [token, water_meter_module_id, water_meter_module_name,
                                      water_meter_module_other_information, water_meter_module_unit]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ModuleRemove'):
                try:
                    module = WaterMetersModules.objects.get(water_meter_module_id=water_meter_module_id)
                    module.delete()
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_module_id, system_log_action_table='WaterMetersModules')
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
    def admin_get_all_water_meter_modules(token, mood, water_meter_module_name, water_meter_module_create_date, page,
                                          count):
        """
            param : [token, water_meter_module_name, water_meter_module_create_date, page, count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ModuleList'):
                valid_mood = ['all', 'modules_without_meter']
                if mood not in valid_mood:
                    wrong_data_result["farsi_message"] = "مقادیر مجاز برای : ['all', 'modules_without_meter']"
                    wrong_data_result["english_message"] = "valid mood is ['all', 'modules_without_meter']"
                    return False, wrong_data_result
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        "water_meter_module_name__contains": water_meter_module_name,
                        "water_meter_module_create_date__contains": water_meter_module_create_date,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None or v != ""}
                    if mood == 'modules_without_meter':
                        module_ids_with_meter = list(map(lambda x: str(x), list(
                            WaterMeters.objects.values_list('water_meter_module', flat=True))))
                        module_ids = list(
                            map(lambda x: str(x[0]), WaterMetersModules.objects.values_list('water_meter_module_id')))
                        module_ids_with_meter_set = set(module_ids_with_meter)
                        objects_not_in_meter = [module_id for module_id in module_ids if
                                                module_id not in module_ids_with_meter_set]

                        filters['water_meter_module_id__in'] = objects_not_in_meter
                        queryset = WaterMetersModules.objects.filter(**filters).order_by(
                            '-water_meter_module_create_date')[offset:offset + limit]
                    else:
                        queryset = WaterMetersModules.objects.filter(**filters).order_by(
                            '-water_meter_module_create_date')[offset:offset + limit]
                    kwargs = {
                        'modules_total_number': len(queryset)
                    }
                    response = WaterMetersModules.objects.serialize(queryset=queryset, **kwargs)
                    return True, response
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_water_meter_module(token, water_meter_module_id, water_meter_module_code):
        """
            param : [token, water_meter_module_id, water_meter_module_code]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ModuleDetail'):
                if water_meter_module_id == None and water_meter_module_code == None:
                    wrong_data_result["farsi_message"] = "ای دی یا کد را وارد کنید"
                    wrong_data_result["english_message"] = "Enter ID or Code"
                    return False, wrong_data_result
                if water_meter_module_id != None and water_meter_module_code == None:
                    try:
                        queryset = WaterMetersModules.objects.get(water_meter_module_id=water_meter_module_id)
                    except:
                        wrong_data_result["farsi_message"] = "water_meter_module_id اشتباه است"
                        wrong_data_result["english_message"] = "Wrong water_meter_module_id"
                        return False, wrong_data_result
                else:
                    try:
                        queryset = WaterMetersModules.objects.get(water_meter_module_code=water_meter_module_code)
                    except:
                        wrong_data_result["farsi_message"] = "water_meter_module_code اشتباه است"
                        wrong_data_result["english_message"] = "Wrong water_meter_module_code"
                        return False, wrong_data_result
                response = WaterMetersModules.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_add_request_too_water_meter_module_serializer(token, water_meter_module_id, water_meter_request_id):
        """
            param : [token, water_meter_module_id, water_meter_request_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Module'):
                try:
                    request = WaterMetersRequests.objects.get(water_meter_request_id=water_meter_request_id)
                    all_modules = WaterMetersModules.objects.filter(water_meter_module_id=water_meter_module_id)
                    this_module_request = all_modules[0].water_meter_request.all().filter(
                        water_meter_request_id=water_meter_request_id)
                    if len(this_module_request) == 0:
                        all_modules[0].water_meter_request.add(request)
                    else:
                        pass
                except:
                    wrong_data_result["farsi_message"] = "ای دی های ورودی اشتباه است"
                    wrong_data_result["english_message"] = "input IDs are wrong"
                    return False, wrong_data_result
            return True, status_success_result
        else:
            return False, wrong_token_result
