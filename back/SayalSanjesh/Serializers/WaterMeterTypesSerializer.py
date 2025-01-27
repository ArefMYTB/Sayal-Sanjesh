from django.db.models import Sum, Count
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMetersTypes, WaterMetersProjects, WaterMeters, WaterMetersTags, \
    WaterMetersConsumptions
from Authorization.models.Admins import Admins
from Authorization.models.MiddleAdmins import MiddleAdmins
from General.models import Utils
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.FileUploadHandler import FileManager
from General.Serializers.LogSerializers import LogSerializers


class WaterMeterTypesSerializer:

    @staticmethod
    def admin_add_water_meter_type(token, water_meter_type_name, water_meter_type_other_information, water_meter_tag,
                                   filepath):
        """
            param : [token, water_meter_type_name, water_meter_type_other_information, water_meter_tag,
                               filepath]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'TypeCreate'):
                try:
                    tag = WaterMetersTags.objects.get(water_meter_tag_id=water_meter_tag)
                except:
                    wrong_data_result["farsi_message"] = "تگ وجود ندارد"
                    wrong_data_result["english_message"] = "tag id is wroung"
                    return False, wrong_data_result
                admin = Admins.objects.get(admin_id=admin_id)

                fields = {
                    "water_meter_type_name": (water_meter_type_name, str)
                }
                result = wrong_result(fields)
                if result == None:
                    water_meter_type = WaterMetersTypes()
                    water_meter_type.admin = admin
                    water_meter_type.water_meter_type_name = water_meter_type_name
                    water_meter_type.water_meter_type_other_information = water_meter_type_other_information
                    water_meter_type.water_meter_tag = tag
                    water_meter_type.save()
                    if filepath != "":
                        folder_name = str(water_meter_type.water_meter_type_id)
                        file_manager = FileManager()
                        file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                       owner_name='Type')
                        water_meter_type.water_meter_type_files.append(file_result)
                        water_meter_type.save()
                    # update all type number in utils table
                    utils_object = Utils.objects.filter(name='all_record_count_in_system')
                    information = list(utils_object.values())[0].get('information')
                    information['water_meter_type'] = information['water_meter_type'] + 1
                    utils_object.update(information=information)
                    # ----- add to loger -------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_type_name,
                        system_log_action_table='WaterMetersTypes')
                    # -------------------------
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_edit_water_meter_type(token, water_meter_tag_id, water_meter_type_new_name, water_meter_type_id,
                                    water_meter_type_other_information, filepath):
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
            if AdminsSerializer.admin_check_permission(admin_id, 'TypeEdit'):
                # admin = Admins.objects.get(admin_id=admin_id)
                fields = {
                    "water_meter_type_new_name": (water_meter_type_new_name, str)
                }

                result = wrong_result(fields)
                if result == None:
                    try:
                        Update_type = WaterMetersTypes.objects.get(water_meter_type_id=water_meter_type_id)
                        first_device_state_dict = {
                            "water_meter_type_name": Update_type.water_meter_type_name,
                            "water_meter_type_create_date": Update_type.water_meter_type_create_date,
                            "water_meter_type_other_information": Update_type.water_meter_type_other_information,
                            "water_meter_tag": Update_type.water_meter_tag,
                            "water_meter_type_files": Update_type.water_meter_type_files,
                        }

                        tag_id = WaterMetersTags.objects.get(water_meter_tag_id=water_meter_tag_id)
                        Update_type.water_meter_type_name = water_meter_type_new_name
                        Update_type.water_meter_type_other_information = water_meter_type_other_information
                        Update_type.water_meter_tag = tag_id
                        if filepath != "":
                            folder_name = str(Update_type.water_meter_type_id)
                            file_manager = FileManager()
                            file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                           owner_name='Type')
                            Update_type.water_meter_type_files.append(file_result)
                            Update_type.save()
                        Update_type.save()
                        # ---------add to logger --------
                        second_state_query = WaterMetersTypes.objects.get(water_meter_type_id=water_meter_type_id)
                        second_device_state_dict = {
                            "water_meter_type_name": second_state_query.water_meter_type_name,
                            "water_meter_type_create_date": second_state_query.water_meter_type_create_date,
                            "water_meter_type_other_information": second_state_query.water_meter_type_other_information,
                            "water_meter_tag": second_state_query.water_meter_tag,
                            "water_meter_type_files": second_state_query.water_meter_type_files,
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
                                                                      system_log_object_action_on=water_meter_type_id,
                                                                      system_log_action='Edit',
                                                                      system_log_action_table='WaterMetersTypes',
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
    def admin_delete_water_meter_type(token, water_meter_type_id):
        """
            param : [token, water_meter_type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'TypeDelete'):
                try:
                    deleted_item = WaterMetersTypes.objects.filter(water_meter_type_id=water_meter_type_id).delete()
                    # update all type number in utils table
                    utils_object = Utils.objects.filter(name='all_record_count_in_system')
                    information = list(utils_object.values())[0].get('information')
                    information['water_meter_type'] = information['water_meter_type'] - 1
                    utils_object.update(information=information)
                    # ------------ add to logger -------------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_type_id,
                        system_log_action_table='WaterMetersTypes')
                    # ---------------------------------------
                except:
                    wrong_data_result["farsi_message"] = "کنتور این تایپ هنوز حذف نشده امکان تغییر و یا حذف وجود ندارد"
                    wrong_data_result["english_message"] = "water meter with this type is already exist."
                    return False, wrong_data_result
                if deleted_item[0] == 0:
                    wrong_data_result["farsi_message"] = "water_meter_type_name اشتباه است"
                    wrong_data_result["english_message"] = "Wrong water_meter_type_name"
                    return False, wrong_data_result
                else:
                    return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meter_types(token, water_meter_type_name, water_meter_type_create_date, page, count):
        """
            param : [token, water_meter_type_name, water_meter_type_create_date, page, count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'TypeList'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    queryset = WaterMetersTypes.objects.filter(
                        water_meter_type_name__contains=water_meter_type_name,
                        water_meter_type_create_date__contains=water_meter_type_create_date).order_by(
                        '-water_meter_type_create_date')[offset:offset + limit]
                    response = WaterMetersTypes.objects.serialize(queryset=queryset)
                    return True, response
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_water_meter_type(token, water_meter_type_id):
        """
            param : [token, water_meter_type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'TypeDetial'):
                try:
                    queryset = WaterMetersTypes.objects.filter(
                        water_meter_type_id=water_meter_type_id)
                    response = WaterMetersTypes.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "water_meter_type_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong water_meter_type_id"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meter_type_sort_by_values_serializer(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'Type']):
                all_types_info = {}
                all_types = WaterMetersTypes.objects.all()
                for type in all_types:
                    type_name = type.water_meter_type_name
                    type_id = type.water_meter_type_id
                    water_meters = WaterMeters.objects.filter(water_meter_type=type_id)
                    if len(water_meters) == 0:
                        all_types_info[type_name] = {
                            'activation': 0,
                            'condition': 0,
                            'validation': 0,
                            'all_water_meter': 0
                        }
                    if len(water_meters) > 0:
                        for water_meter in water_meters:
                            type_name = water_meter.water_meter_type.water_meter_type_name
                            activation = water_meter.water_meter_activation
                            condition = water_meter.water_meter_condition
                            validation = water_meter.water_meter_validation
                            values_list = [('activation', activation), ('condition', condition),
                                           ('validation', validation)]
                            if type_name not in all_types_info:
                                all_types_info[type_name] = {
                                    'activation': activation,
                                    'condition': condition,
                                    'validation': validation,
                                    'all_water_meter': len(water_meters)

                                }
                            else:
                                for value in values_list:
                                    if value[1] != 0:
                                        all_types_info[type_name][value[0]] += 1
                                        all_types_info[type_name]['all_water_meter'] = len(water_meters)

                return True, all_types_info
            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'Type']):
                middel_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                middel_meters = WaterMeters.objects.filter(
                    water_meter_project__water_meter_project_id__in=middel_projects)
                all_types_info = {}
                all_types = WaterMetersTypes.objects.all()
                for type in all_types:
                    type_name = type.water_meter_type_name
                    type_id = type.water_meter_type_id
                    water_meters = middel_meters.filter(water_meter_type=type_id)
                    if len(water_meters) == 0:
                        all_types_info[type_name] = {
                            'activation': 0,
                            'condition': 0,
                            'validation': 0,
                            'all_water_meter': 0
                        }
                    if len(water_meters) > 0:
                        for water_meter in water_meters:
                            type_name = water_meter.water_meter_type.water_meter_type_name
                            activation = water_meter.water_meter_activation
                            condition = water_meter.water_meter_condition
                            validation = water_meter.water_meter_validation
                            values_list = [('activation', activation), ('condition', condition),
                                           ('validation', validation)]
                            if type_name not in all_types_info:
                                all_types_info[type_name] = {
                                    'activation': activation,
                                    'condition': condition,
                                    'validation': validation,
                                    'all_water_meter': len(water_meters)

                                }
                            else:
                                for value in values_list:
                                    if value[1] != 0:
                                        all_types_info[type_name][value[0]] += 1
                                        all_types_info[type_name]['all_water_meter'] = len(water_meters)

                return True, all_types_info

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_total_statistics_serializer(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'Type']):
                all_types = WaterMetersTypes.objects.all()
                all_water_meters = WaterMeters.objects.all()
                all_tags = WaterMetersTags.objects.all()
                type_with_max_counters = all_water_meters.values_list('water_meter_type').annotate(
                    max_count=Count('water_meter_type')).order_by('-max_count')
                type_counters = []
                tag_information = []
                for type_id in type_with_max_counters:
                    if type_id[1] == type_with_max_counters[0][1]:
                        number_of_counter = all_water_meters.filter(water_meter_type=type_id[0]).count()
                        if type_id[0] != None:
                            type_detail = all_types.get(water_meter_type_id=type_id[0])
                            max_project_info = {
                                "water_meter_type_id": type_detail.water_meter_type_id,
                                "water_meter_type_name": type_detail.water_meter_type_name,
                                "number_of_counter": number_of_counter,
                            }
                            type_counters.append(max_project_info)
                for tag_value in all_tags:
                    count_type = all_types.filter(
                        water_meter_tag__water_meter_tag_id=tag_value.water_meter_tag_id).count()
                    tag_result = {
                        "water_meter_tag_id": tag_value.water_meter_tag_id,
                        "water_meter_tag_name": tag_value.water_meter_tag_name,
                        "water_meter_tag_create_date": tag_value.water_meter_tag_create_date,
                        "number_of_type": count_type,
                    }
                    tag_information.append(tag_result)
                total_type_result = {
                    "all_counter_types": all_types.count(),
                    "types_with_max_counter": type_counters,
                    "tags_info": tag_information,
                }
                return True, total_type_result
            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'Type']):
                middle_admin_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                all_water_meters = WaterMeters.objects.filter(
                    water_meter_project__water_meter_project_id__in=middle_admin_projects)
                all_types = WaterMetersTypes.objects.filter(
                    water_meter_type_id__in=all_water_meters.values_list('water_meter_type__water_meter_type_id'))
                type_with_max_counter = all_water_meters.values('water_meter_type__water_meter_type_id').annotate(
                    counter_count=Count('water_meter_type')).order_by('-counter_count').first()
                tag_response = []
                all_system_tags = WaterMetersTags.objects.all()

                for tag_object in all_system_tags:
                    tag_info = {
                        "water_meter_tag_id": tag_object.water_meter_tag_id,
                        "water_meter_tag_name": tag_object.water_meter_tag_name,
                        "water_meter_tag_create_date": tag_object.water_meter_tag_name,
                        "number_of_type": all_types.filter(
                            water_meter_tag__water_meter_tag_id=tag_object.water_meter_tag_id).count()
                    }
                    tag_response.append(tag_info)
                max_type_id = str(type_with_max_counter['water_meter_type__water_meter_type_id'])

                total_type_result = {
                    "all_counter_types": all_types.count(),
                    "types_with_max_counter": [
                        {
                            "water_meter_type_id": max_type_id,
                            "water_meter_type_name": WaterMetersTypes.objects.get(
                                water_meter_type_id=max_type_id).water_meter_type_name,
                            "number_of_counter": type_with_max_counter['counter_count'],
                        }
                    ],
                    "tags_info": tag_response,
                }
                return True, total_type_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meter_types(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            all_user_types = WaterMeters.objects.filter(water_meter_user=user_id)
            user_type_result = []
            for user_type in all_user_types:
                user_name = user_type.water_meter_user.user_name
                user_phone = user_type.water_meter_user.user_phone
                user_type_name = user_type.water_meter_type.water_meter_type_name
                user_type_create_date = user_type.water_meter_type.water_meter_type_create_date
                user_tag_name = user_type.water_meter_type.water_meter_tag.water_meter_tag_name
                user_project_name = user_type.water_meter_project.water_meter_project_name
                user_result = {
                    "user_name": user_name,
                    "user_phone": user_phone,
                    "user_project_name": user_project_name,
                    "user_type_name": user_type_name,
                    "user_type_create_date": user_type_create_date,
                    "user_tag_name": user_tag_name,
                }
                user_type_result.append(user_result)
            return True, user_type_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_water_meter_types(token, water_meter_type_name):
        """
            param : [token, water_meter_type_name]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                water_meter_type = WaterMetersTypes.objects.get(water_meter_type_name=water_meter_type_name)
            except:
                wrong_data_result["farsi_message"] = "water_meter_type_name اشتباه است"
                wrong_data_result["english_message"] = "Wrong water_meter_type_name"
                return False, wrong_data_result
            result = water_meter_type.as_dict()
            result.pop('admin_info')
            result.update({
                'water_meter_project_info': (result['water_meter_project_info']['water_meter_project_id'],
                                             result['water_meter_project_info']['water_meter_project_name'])
            })
            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meter_types_v2(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            user_types = WaterMeters.objects.filter(water_meter_user=user_id).values('water_meter_type')
            queryset = WaterMetersTypes.objects.filter(water_meter_type_id__in=user_types)
            response = WaterMetersTypes.objects.serialize(queryset=queryset, req_from='user')
            return True, response
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_water_meter_types_v2(token, water_meter_type_name):
        """
            param : [token, water_meter_type_name]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                water_meter_type = WaterMetersTypes.objects.filter(water_meter_type_name=water_meter_type_name)
            except:
                wrong_data_result["farsi_message"] = "water_meter_type_name اشتباه است"
                wrong_data_result["english_message"] = "Wrong water_meter_type_name"
                return False, wrong_data_result
            queryset = water_meter_type
            response = WaterMetersTypes.objects.serialize(queryset=queryset, req_from='user')
            return True, response
        else:
            return False, wrong_token_result
