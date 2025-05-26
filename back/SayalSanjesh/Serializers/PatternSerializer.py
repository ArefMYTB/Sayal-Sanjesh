from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result
from SayalSanjesh.models import WaterMetersProjects, WaterMetersTags, Pattern
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.Serializers.LogSerializers import LogSerializers


class PatternSerializer:

    @staticmethod
    def admin_create_pattern_serializer(
            token, pattern_tag, pattern_project, pattern_list):
        """
            param : [token, pattern_tag, pattern_project, pattern_list]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'BillManaging'):
                admin = Admins.objects.get(admin_id=admin_id)
                # valid input_tag_id
                try:
                    tag_obj = WaterMetersTags.objects.get(water_meter_tag_id=pattern_tag)
                except:
                    wrong_data_result["farsi_message"] = "pattern_tag اشتباه است"
                    wrong_data_result["english_message"] = "pattern_tag is wrong"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                # valid input_project_id
                try:
                    project_obj = WaterMetersProjects.objects.get(water_meter_project_id=pattern_project)
                except:
                    wrong_data_result["farsi_message"] = "pattern_project اشتباه است"
                    wrong_data_result["english_message"] = "pattern_project is wrong"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                # create new pattern
                print("code in serializer")
                try:
                    pattern_obj = Pattern()
                    pattern_obj.admin = admin
                    pattern_obj.pattern_tag = tag_obj
                    pattern_obj.pattern_project = project_obj
                    pattern_obj.pattern_list = pattern_list
                    pattern_obj.save()
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on='', system_log_action_table='Pattern')
                except:
                    wrong_data_result["farsi_message"] = "خطایی رخ داده است"
                    wrong_data_result["english_message"] = "An error has occurred"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_pattern_serializer(
            token, pattern_tag, pattern_project, pattern_list, pattern_id):
        """
            param : [token, pattern_tag, pattern_project, pattern_list, pattern_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            admin_object = Admins.objects.get(admin_id =admin_id )
            if AdminsSerializer.admin_check_permission(admin_id, 'BillManaging'):
                admin = Admins.objects.get(admin_id=admin_id)
                # valid input_tag_id
                if pattern_tag is not None:
                    try:
                        tag_obj = WaterMetersTags.objects.get(water_meter_tag_id=pattern_tag)
                    except:
                        wrong_data_result["farsi_message"] = "pattern_tag اشتباه است"
                        wrong_data_result["english_message"] = "pattern_tag is wrong"
                        wrong_data_result["code"] = 406
                        return False, wrong_data_result
                else:
                    tag_obj = None
                # valid input_project_id
                if pattern_project is not None:
                    try:
                        project_obj = WaterMetersProjects.objects.get(water_meter_project_id=pattern_project)
                    except:
                        wrong_data_result["farsi_message"] = "pattern_project اشتباه است"
                        wrong_data_result["english_message"] = "pattern_project is wrong"
                        wrong_data_result["code"] = 406
                        return False, wrong_data_result
                else:
                    project_obj = None
                # get pattern obj
                try:
                    pattern_obj = Pattern.objects.get(pattern_id=pattern_id)
                    first_device_state_dict = {
                        "pattern_tag": pattern_obj.pattern_tag,
                        "pattern_project": pattern_obj.pattern_project,
                        "pattern_list": pattern_obj.pattern_list
                    }
                except:
                    wrong_data_result["farsi_message"] = "pattern_id اشتباه است"
                    wrong_data_result["english_message"] = "pattern_id is wrong"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                # update new pattern
                try:
                    pattern_obj.admin = admin
                    pattern_obj.pattern_tag = tag_obj
                    pattern_obj.pattern_project = project_obj
                    pattern_obj.pattern_list = pattern_list
                    pattern_obj.save()
                    second_device_state = Pattern.objects.get(pattern_id=pattern_id)
                    second_device_state_dict = {"pattern_tag": second_device_state.pattern_tag,
                                                "pattern_project": second_device_state.pattern_project,
                                                "pattern_list": second_device_state.pattern_list}
                    if second_device_state.pattern_project is not None:
                        second_device_state_dict['pattern_project'] = str(
                            second_device_state.pattern_project.water_meter_project_id)
                    if second_device_state.pattern_tag is not None:
                        second_device_state_dict['pattern_tag'] = str(
                            second_device_state.pattern_tag.water_meter_tag_id)

                    changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                      first_device_state_dict if
                                      first_device_state_dict[key] != second_device_state_dict[key]}
                    system_log_message = ''
                    for key, values in changed_fields.items():
                        system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    # LogSerializers().system_log_create_serializer(
                    #     token=token, system_log_admin=admin_object, system_log_action='Edit', system_log_user=None,
                    #     system_log_field_changes=None, system_log_message=None,
                    #     system_log_object_action_on='', system_log_action_table='Pattern')
                except:
                    wrong_data_result["farsi_message"] = "خطایی رخ داده است"
                    wrong_data_result["english_message"] = "An error has occurred"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_pattern_serializer(
            token, pattern_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'BillManaging'):
                admin = Admins.objects.get(admin_id=admin_id)

                # get pattern obj
                try:
                    pattern_obj = Pattern.objects.get(pattern_id=pattern_id)
                except:
                    wrong_data_result["farsi_message"] = "pattern_id اشتباه است"
                    wrong_data_result["english_message"] = "pattern_id is wrong"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                # delete new pattern
                try:
                    pattern_obj.delete()
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=pattern_id, system_log_action_table='Pattern')
                except:
                    wrong_data_result["farsi_message"] = "خطایی رخ داده است"
                    wrong_data_result["english_message"] = "An error has occurred"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_pattern_serializer(
            token, page, count, project_id, tag_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'BillManaging'):
                # admin = Admins.objects.get(admin_id=admin_id)
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "pattern_tag__water_meter_tag_id": tag_id,
                    "pattern_project__water_meter_project_id": project_id,
                }

                filters = {k: v for k, v in filters.items() if v is not None}
                try:
                    patterns = Pattern.objects.filter(**filters)
                except:
                    wrong_data_result["farsi_message"] = "داده های ورودی اشتباه است."
                    wrong_data_result["english_message"] = "input data is incorrect."
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
                queryset = patterns.order_by('-pattern_create_date')[offset:offset + limit]
                # all_pattern_number = queryset.count()
                # for pattern in queryset:
                #     pattern['all_pattern_number'] = all_pattern_number
                response = Pattern.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_pattern_serializer(
            token, pattern_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'BillManaging'):
                # admin = Admins.objects.get(admin_id=admin_id)

                try:
                    queryset = Pattern.objects.get(pattern_id=pattern_id)
                    response = Pattern.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "pattern_id اشتباه است"
                    wrong_data_result["english_message"] = "pattern_id is wrong"
                    wrong_data_result["code"] = 406
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
