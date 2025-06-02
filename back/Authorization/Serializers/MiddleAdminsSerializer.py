from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result
from SayalSanjesh.models import WaterMetersProjects, WaterMeters
from Authorization.models.Users import Users
from Authorization.models.Admins import Admins
from Authorization.models.MiddleAdmins import MiddleAdmins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class MiddleAdminsSerializer:

    @staticmethod
    def add_middle_admin_data_serializer(token, project_ids, water_meter_ids, middle_admin_id):
        """
           param : [token, project_ids, water_meter_ids, middle_admin_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['CRUDAdmin', 'CRUDManager']):
                try:
                    middle_admin = Admins.objects.get(admin_id=middle_admin_id)
                except:
                    wrong_data_result["farsi_message"] = "middle_admin اشتباه است"
                    wrong_data_result["english_message"] = "middle_admin is worng"
                    return False, wrong_data_result
                Project_id = []
                Water_meters_id = []
                try:
                    for id in project_ids:
                        project = WaterMetersProjects.objects.get(water_meter_project_id=id)
                        project_water_meter = WaterMeters.objects.filter(water_meter_project_id=id)
                        if not project_water_meter:
                            pass
                        else:
                            for water_meter in project_water_meter:
                                project_water_meter_id = water_meter.water_meter_serial
                                Water_meters_id.append(project_water_meter_id)
                        Project_id.append(project.water_meter_project_id)

                except:
                    wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                    wrong_data_result["english_message"] = "water_meter_project_id is worng"
                    return False, wrong_data_result
                try:
                    for id in water_meter_ids:
                        water_meter = WaterMeters.objects.get(water_meter_serial=id)
                        Water_meters_id.append(water_meter.water_meter_serial)

                except:
                    wrong_data_result["farsi_message"] = "water_meter_serial اشتباه است"
                    wrong_data_result["english_message"] = "water_meter_serial is worng"
                    return False, wrong_data_result
                middleAdmin = MiddleAdmins()
                middleAdmin.middle_admin_id = middle_admin
                middleAdmin.project_ids = Project_id
                middleAdmin.water_meter_ids = Water_meters_id
                middleAdmin.save()

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def edit_middle_admin_data_serializer(token, project_ids, water_meter_ids, middle_admin_id):
        """
           param : [token, project_ids, water_meter_ids, middle_admin_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['CRUDAdmin', 'CRUDManager']):
                try:
                    middle_admin = MiddleAdmins.objects.get(middle_admin_id=middle_admin_id)
                except:
                    wrong_data_result["farsi_message"] = "middle_admin اشتباه است"
                    wrong_data_result["english_message"] = "middle_admin is worng"
                    return False, wrong_data_result
                middle_admin_projects = middle_admin.project_ids
                middle_admin_water_meters = middle_admin.water_meter_ids
                # if middle_admin_projects is None:
                #     Project_id = []
                # else:
                #     Project_id = middle_admin_projects
                #
                # if middle_admin_water_meters is None:
                #     Water_meters_id = []
                # else:
                #     Water_meters_id = middle_admin_water_meters
                Project_id = []
                Water_meters_id = []
                try:
                    for id in project_ids:
                        project = WaterMetersProjects.objects.get(water_meter_project_id=id)
                        project_water_meter = WaterMeters.objects.filter(water_meter_project_id=id)
                        if not project_water_meter:
                            pass
                        else:
                            for water_meter in project_water_meter:
                                project_water_meter_id = water_meter.water_meter_serial
                                Water_meters_id.append(project_water_meter_id)
                        Project_id.append(project.water_meter_project_id)

                except:
                    wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                    wrong_data_result["english_message"] = "water_meter_project_id is worng"
                    return False, wrong_data_result
                try:
                    for id in water_meter_ids:
                        water_meter = WaterMeters.objects.get(water_meter_serial=id)
                        Water_meters_id.append(water_meter.water_meter_serial)

                except:
                    wrong_data_result["farsi_message"] = "water_meter_serial اشتباه است"
                    wrong_data_result["english_message"] = "water_meter_serial is worng"
                    return False, wrong_data_result
                middle_admin.project_ids = Project_id
                middle_admin.water_meter_ids = Water_meters_id
                middle_admin.save()
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_middle_admin_serializer(token):
        """
           param : [token]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            # TODO: Remove This Section
            # if AdminsSerializer.admin_check_permission(admin_id, ['CRUDAdmin', 'ViewAdmin', 'CRUDManager']):
            #     list_of_middle_admins = Admins.objects.filter(admin_permissions__contains=['CRUDManager'])
            #     middle_admin_data = MiddleAdmins.objects.filter(middle_admin_id__in=list_of_middle_admins)
            #     result = []
            #     print(middle_admin_data)
            #     for obj in middle_admin_data:
            #         # middle_admin_obj = Admins.objects.get(admin_id=obj.middle_admin_id)
            #         result_dict = {
            #             "admin_id": obj.middle_admin_id.admin_id,
            #             "admin_name": obj.middle_admin_id.admin_name,
            #             "admin_lastname": obj.middle_admin_id.admin_lastname,
            #             "admin_phone": obj.middle_admin_id.admin_phone,
            #         }
            #         middle_project_objects = WaterMetersProjects.objects.filter(
            #             water_meter_project_id__in=obj.project_ids)
            #         response = WaterMetersProjects.objects.serialize(
            #             queryset=middle_project_objects, modify_response=True,
            #             pop_item=['admin_info', 'water_meters_with_this_id', 'types'])
            #         print("response: ", response)
            #         result_dict['middel_admin_projects'] = response
            #         result.append(result_dict)
            #     return True, result
            
            if AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager', 'Admin']):
                admin_obj = Admins.objects.get(admin_id=admin_id)
                list_of_middle_admins = Admins.objects.filter(admin_permissions__contains=['ProjectManager'],
                                                              admin_creator_id=admin_id).exclude(
                    admin_phone=admin_obj.admin_phone)
                middle_admin_data = MiddleAdmins.objects.filter(middle_admin_id__in=list_of_middle_admins)
                result = []
                for obj in middle_admin_data:
                    # middle_admin_obj = Admins.objects.get(admin_id=obj.middle_admin_id)
                    result_dict = {
                        "admin_id": obj.middle_admin_id.admin_id,
                        "admin_name": obj.middle_admin_id.admin_name,
                        "admin_lastname": obj.middle_admin_id.admin_lastname,
                        "admin_phone": obj.middle_admin_id.admin_phone,
                    }
                    middle_project_objects = WaterMetersProjects.objects.filter(
                        water_meter_project_id__in=obj.project_ids)
                    response = WaterMetersProjects.objects.serialize(
                        queryset=middle_project_objects, modify_response=True,
                        pop_item=['admin_info', 'water_meters_with_this_id', 'types'])
                    result_dict['middel_admin_projects'] = response
                    result.append(result_dict)
                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_middle_admin_serializer(token, middle_admin_id):
        """
           param : [token, middle_admin_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                try:
                    middle_admin = MiddleAdmins.objects.get(middle_admin_id=middle_admin_id)
                except:
                    wrong_data_result["farsi_message"] = "middle_admin اشتباه است"
                    wrong_data_result["english_message"] = "middle_admin is worng"
                    return False, wrong_data_result
                middle_admin_water_meters = WaterMeters.objects.filter(
                    water_meter_serial__in=middle_admin.water_meter_ids)
                middle_admin_water_meters_list = []
                middle_admin_projects = WaterMetersProjects.objects.filter(
                    water_meter_project_id__in=middle_admin.project_ids)
                middle_admin_projects_list = []
                if middle_admin.water_meter_ids is not None:
                    for water_meter in middle_admin_water_meters:
                        water_meter_info = {
                            "water_meter_serial": water_meter.water_meter_serial,
                            "water_meter_name": water_meter.water_meter_name,
                            "water_meter_condition": water_meter.water_meter_condition,
                            "water_meter_activation": water_meter.water_meter_activation,
                            "water_meter_type_info": {
                                "water_meter_type_id": water_meter.water_meter_type.water_meter_type_id,
                                "water_meter_type_name": water_meter.water_meter_type.water_meter_type_name,
                                "water_meter_type_create_date": water_meter.water_meter_type.water_meter_type_create_date,
                                "water_meter_tag_info": {
                                    "water_meter_tag_name": water_meter.water_meter_type.water_meter_tag.water_meter_tag_name,
                                    "water_meter_tag_id": water_meter.water_meter_type.water_meter_tag.water_meter_tag_id,
                                    "water_meter_tag_create_date": water_meter.water_meter_type.water_meter_tag.water_meter_tag_create_date,
                                }
                            },
                        }
                        if water_meter.water_meter_user is not None:
                            water_meter_info['water_meter_user_info'] = {
                                "user_id": water_meter.water_meter_user.user_id,
                                "user_name": water_meter.water_meter_user.user_name,
                                "user_lastname": water_meter.water_meter_user.user_lastname,
                                "user_phone": water_meter.water_meter_user.user_phone,
                            }
                        else:
                            water_meter_info['water_meter_user_info'] = {
                                "user_id": None,
                                "user_name": None,
                                "user_lastname": None,
                                "user_phone": None,
                            }
                        if water_meter.water_meter_module is not None:
                            water_meter_info['water_meter_module_info'] = {
                                "water_meter_module_name": water_meter.water_meter_module.water_meter_module_name,
                                "water_meter_module_id": water_meter.water_meter_module.water_meter_module_id,
                                "water_meter_module_code": water_meter.water_meter_module.water_meter_module_code,
                                "water_meter_module_create_date": water_meter.water_meter_module.water_meter_module_create_date,
                            }
                        else:
                            water_meter_info['water_meter_module_info'] = {
                                "water_meter_module_name": None,
                                "water_meter_module_id": None,
                                "water_meter_module_code": None,
                                "water_meter_module_create_date": None,
                            }
                        if water_meter.water_meter_project is not None:
                            water_meter_info['water_meter_project_info'] = {
                                "water_meter_project_id": water_meter.water_meter_project.water_meter_project_id,
                                "water_meter_project_name": water_meter.water_meter_project.water_meter_project_name,
                                "water_meter_project_title": water_meter.water_meter_project.water_meter_project_title,
                                "water_meter_project_create_date": water_meter.water_meter_project.water_meter_project_create_date,
                            }
                        else:
                            water_meter_info['water_meter_project_info'] = {
                                "water_meter_project_id": None,
                                "water_meter_project_name": None,
                                "water_meter_project_title": None,
                                "water_meter_project_create_date": None,
                            }
                        middle_admin_water_meters_list.append(water_meter_info)
                if middle_admin.project_ids is not None:
                    for project in middle_admin_projects:
                        project_info = {
                            "water_meter_project_name": project.water_meter_project_name,
                            "water_meter_project_id": project.water_meter_project_id,
                            "water_meter_project_title": project.water_meter_project_title,
                            "water_meter_project_other_information": project.water_meter_project_other_information,
                            "water_meter_project_create_date": project.water_meter_project_create_date,
                        }
                        middle_admin_projects_list.append(project_info)
                result = {
                    "middle_admin_id": middle_admin.middle_admin_id.admin_id,
                    "create_date": middle_admin.create_date,
                    "middle_admin_water_meters": middle_admin_water_meters_list,
                    "middle_admin_projects": middle_admin_projects_list,
                }
                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def middle_admin_get_all_users_serializer(token, page, count):
        """
           param : [token, page, count]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                offset = int((page - 1) * count)
                limit = int(count)
                users_list = []
                users_dict = {}
                # middle admin user from projects
                middle_admin_obj = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_water_meter_obj = WaterMeters.objects.filter(
                    water_meter_project_id__in=middle_admin_obj.project_ids).order_by(
                    '-water_meter_create_date')[
                                               offset:offset + limit]
                # get users from water meter table
                for water_meter_obj in middle_admin_water_meter_obj:
                    if water_meter_obj.water_meter_user is not None:
                        user_id = water_meter_obj.water_meter_user.user_id
                        water_meter_user = water_meter_obj.water_meter_user.as_dict()
                        water_meter_user.pop('admin')
                        if user_id not in users_dict:
                            users_dict[user_id] = water_meter_user
                # middle admin user from users.
                users_objects = Users.objects.filter(admin=admin_id)
                for user_obj in users_objects:
                    user_id = user_obj.user_id
                    user_obj = user_obj.as_dict()
                    user_obj.pop('admin')
                    if user_id not in users_dict:
                        users_dict[user_id] = user_obj
                for user_info in users_dict:
                    users_list.append(users_dict[user_info])

                return True, users_list
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
