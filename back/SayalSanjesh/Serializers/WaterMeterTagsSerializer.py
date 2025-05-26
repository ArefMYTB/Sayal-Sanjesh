from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMeters, WaterMetersTags
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.FileUploadHandler import FileManager
from General.Serializers.LogSerializers import LogSerializers
from Authorization.models.MiddleAdmins import MiddleAdmins


class WaterMeterTagsSerializer:

    @staticmethod
    def admin_add_water_meter_tag_serializer(token, water_meter_tag_name, water_meter_tag_other_information, filepath):
        """
            param : [token, water_meter_tag_name, water_meter_tag_other_information, filepath]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                admin = Admins.objects.get(admin_id=admin_id)
                water_meter_tag = WaterMetersTags()
                fields = {
                    "water_meter_type_name": (water_meter_tag_name, str)
                }
                result = wrong_result(fields)
                if result == None:
                    water_meter_tag.admin = admin
                    water_meter_tag.water_meter_tag_name = water_meter_tag_name
                    water_meter_tag.water_meter_tag_other_information = water_meter_tag_other_information
                    if filepath != "":
                        folder_name = str(water_meter_tag.water_meter_tag_id)
                        file_manager = FileManager()
                        file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                       owner_name='Tag')
                        water_meter_tag.water_meter_tag_files.append(file_result)
                        water_meter_tag.save()
                    water_meter_tag.save()
                    # ----- add to loger -------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_tag_name,
                        system_log_action_table='WaterMetersTags')
                    # -------------------------
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_water_meter_tag_serializer(token, water_meter_tag_id):
        """
            param : [token, water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                try:
                    deleted_item = WaterMetersTags.objects.filter(water_meter_tag_id=water_meter_tag_id).delete()
                    # ------- add to logger -------------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_tag_id,
                        system_log_action_table='WaterMetersTags')
                    # -----------------------------------
                except:
                    wrong_data_result["farsi_message"] = "ای دی اشتباه است"
                    wrong_data_result["english_message"] = "tag id is worng"
                    return False, wrong_data_result
                if deleted_item[0] == 0:
                    wrong_data_result["farsi_message"] = "water_meter_tag_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong water_meter_tag_id"
                    return False, wrong_data_result
                else:
                    return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meter_tags_serializer(token, water_meter_tag_name, water_meter_type_create_date, page,
                                                  count):
        """
            param : [token, water_meter_tag_name, water_meter_type_create_date, page,
                                                  count]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            fields = {
                "page": (page, int),
                "count": (count, int)
            }
            field_result = wrong_result(fields)
            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                all_tags = WaterMetersTags.objects.filter(
                    water_meter_tag_name__contains=water_meter_tag_name,
                    water_meter_tag_create_date__contains=water_meter_type_create_date).order_by(
                    '-water_meter_tag_create_date')[offset:offset + limit]

                result = []
                for tag in all_tags:
                    tag = tag.as_dict()
                    tag.update(
                        {
                            "admin_info": tag['admin_info']['admin_id'],
                            "all_tags": len(all_tags)
                        }
                    )
                    result.append(tag)
                return True, result
            else:
                return field_result
            
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_total_statists_tags_serializer(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            # ['Base', 'Consumption']Tag
            if AdminsSerializer.admin_check_permission(admin_id, ['ViewProject', 'Reports']):
                all_water_tags = WaterMetersTags.objects.all()
                all_water_meters = WaterMeters.objects.filter(water_meter_type__water_meter_tag__in=all_water_tags)
                all_water_meters_count = all_water_meters.count()
                result = {
                    "all_water_meters_count": all_water_meters_count
                }
                for tag in all_water_tags:
                    tag_count = all_water_meters.filter(
                        water_meter_type__water_meter_tag__water_meter_tag_id=tag.water_meter_tag_id).count()
                    # if tag_count!= 0 :
                    result[tag.water_meter_tag_name] = tag_count
                return True, result
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager', 'Tag']):
                all_water_tags = WaterMetersTags.objects.all()
                middel_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                middel_meters = WaterMeters.objects.filter(water_meter_project__water_meter_project_id__in=middel_projects)
                result = {
                    "all_water_meters_count": middel_meters.count()
                }
                for tag in all_water_tags:
                    tag_count = middel_meters.filter(
                        water_meter_type__water_meter_tag__water_meter_tag_id=tag.water_meter_tag_id).count()
                    # if tag_count!= 0 :
                    result[tag.water_meter_tag_name] = tag_count
                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meter_tags_serializer(token, water_meter_tag_name, water_meter_type_create_date, page,
                                                 count):
        """
                param : [token, water_meter_tag_name, water_meter_type_create_date, page,
                                                 count]
                return :
                A tuple containing a boolean indicating the success or failure of the operation, and a list of
                serialized data results.  it returns a false status along with an error message.
            """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                "page": (page, int),
                "count": (count, int)
            }
            field_result = wrong_result(fields)
            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                all_tags = WaterMetersTags.objects.filter(
                    water_meter_tag_name__contains=water_meter_tag_name,
                    water_meter_tag_create_date__contains=water_meter_type_create_date).order_by(
                    '-water_meter_tag_create_date')[offset:offset + limit]

                result = []
                for tag in all_tags:
                    tag = tag.as_dict()
                    tag.update(
                        {
                            "all_tags": len(all_tags)
                        }
                    )
                    result.append(tag)
                    tag.pop('admin_info')
                return True, result
            else:
                return field_result
        else:
            return False, wrong_token_result
