import json
import os
import shutil
from Authorization.TokenManager import token_to_user_id
from django.db.models import Sum, Count
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMetersProjects, WaterMeters, WaterMetersTypes, WaterMetersConsumptions
from Authorization.models.MiddleAdmins import MiddleAdmins
from Authorization.models.Admins import Admins
from General.models import Utils
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from Authorization.Serializers.MiddleAdminsSerializer import MiddleAdminsSerializer
from General.FileUploadHandler import FileManager
from General.Serializers.LogSerializers import LogSerializers
from django.db.models import Q


class WaterMeterProjectsSerializer:

    @staticmethod
    def admin_add_water_meter_project(token, water_meter_project_name, water_meter_project_title,
                                      water_meter_project_other_information, water_meter_project_start_date,
                                      water_meter_project_employer_description, water_meter_project_contract_number,
                                      water_meter_project_images, water_meter_project_urls):
        """
            param : [token, water_meter_project_name, water_meter_project_title,
                                      water_meter_project_other_information, water_meter_project_start_date,
                                      water_meter_project_employer_description, water_meter_project_contract_number,
                                      water_meter_project_images, water_meter_project_urls]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Joker'):
                admin = Admins.objects.get(admin_id=admin_id)
                admin_permissions = admin.admin_permissions
                water_meter_project = WaterMetersProjects()
                fields = {
                    "water_meter_project_name": (water_meter_project_name, str),
                    "water_meter_project_title": (water_meter_project_title, str)
                }
                result = wrong_result(fields)

                if result == None:
                    water_meter_project.admin = admin
                    water_meter_project.water_meter_project_name = water_meter_project_name
                    water_meter_project.water_meter_project_title = water_meter_project_title
                    water_meter_project.water_meter_project_other_information = water_meter_project_other_information
                    if water_meter_project_start_date != None:
                        water_meter_project.water_meter_project_start_date = water_meter_project_start_date
                    else:
                        pass
                    water_meter_project.water_meter_project_employer_description = water_meter_project_employer_description
                    water_meter_project.water_meter_project_contract_number = water_meter_project_contract_number
                    water_meter_project.water_meter_project_images = water_meter_project_images
                    water_meter_project.water_meter_project_urls = water_meter_project_urls
                    water_meter_project.save()
                    # TODO: Remove This Section -- Project Manager can't create project
                    # if middle create projects added to middle project lists
                    if 'ProjectManager' in admin_permissions:
                        try:
                            project_id = str(WaterMetersProjects.objects.get(
                                admin__admin_id=admin_id, water_meter_project_name=water_meter_project_name,
                                water_meter_project_title=water_meter_project_title).water_meter_project_id)
                            middle_object = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                            middle_object_project_list = middle_object.project_ids
                            middle_object_project_list.append(project_id)
                            middle_object.project_ids = middle_object_project_list
                            middle_object.save()
                        except:
                            pass
                    # update all project number in utils table
                    utils_object = Utils.objects.filter(name='all_record_count_in_system')
                    information = list(utils_object.values())[0].get('information')
                    information['water_meter_project'] = information['water_meter_project'] + 1
                    utils_object.update(information=information)
                    # ----- add to loger -------
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_project_name,
                        system_log_action_table='WaterMetersProjects')
                    # -------------------------
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_water_meter_project(token, water_meter_project_id, water_meter_project_name,
                                       water_meter_project_other_information, water_meter_project_title,
                                       water_meter_project_start_date,
                                       water_meter_project_employer_description, water_meter_project_contract_number,
                                       filepath, water_meter_project_images, water_meter_project_urls):
        """
                param : [token, water_meter_project_id, water_meter_project_name,
                                       water_meter_project_other_information, water_meter_project_title,
                                       water_meter_project_start_date,
                                       water_meter_project_employer_description, water_meter_project_contract_number,
                                       filepath, water_meter_project_images, water_meter_project_urls]
                return :
                A tuple containing a boolean indicating the success or failure of the operation, and a list of
                serialized data results.  it returns a false status along with an error message.
            """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            print("HI")
            if AdminsSerializer.admin_check_permission(admin_id, 'Joker'):
                admin = Admins.objects.get(admin_id=admin_id)
                try:
                    water_meter_project = WaterMetersProjects.objects.get(
                        water_meter_project_id=water_meter_project_id)
                except:
                    wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                    return False, wrong_data_result
                fields = {
                    "water_meter_project_name": (water_meter_project_name, str)
                }

                result = wrong_result(fields)
                if result == None:
                    first_device_state_dict = {
                        "water_meter_project_id": water_meter_project.water_meter_project_id,
                        "water_meter_project_name": water_meter_project.water_meter_project_name,
                        "water_meter_project_title": water_meter_project.water_meter_project_title,
                        "water_meter_project_create_date": water_meter_project.water_meter_project_create_date,
                        "water_meter_project_start_date": water_meter_project.water_meter_project_start_date,
                        "water_meter_project_employer_description": water_meter_project.water_meter_project_employer_description,
                        "water_meter_project_contract_number": water_meter_project.water_meter_project_contract_number,
                        "water_meter_project_other_information": water_meter_project.water_meter_project_other_information,
                        "water_meter_project_images": water_meter_project.water_meter_project_images,
                        "water_meter_project_files": water_meter_project.water_meter_project_files,
                        "water_meter_project_urls": water_meter_project.water_meter_project_urls,
                        # "water_meter_types": water_meter_project.water_meter_types
                    }
                    water_meter_project.admin = admin
                    water_meter_project.water_meter_project_id = water_meter_project_id
                    water_meter_project.water_meter_project_name = water_meter_project_name
                    water_meter_project.water_meter_project_title = water_meter_project_title
                    water_meter_project.water_meter_project_other_information = water_meter_project_other_information
                    water_meter_project.water_meter_project_images = water_meter_project_images
                    water_meter_project.water_meter_project_urls = water_meter_project_urls

                    if water_meter_project_start_date != None:
                        water_meter_project.water_meter_project_start_date = water_meter_project_start_date
                    else:
                        pass
                    water_meter_project.water_meter_project_employer_description = water_meter_project_employer_description
                    water_meter_project.water_meter_project_contract_number = water_meter_project_contract_number
                    if filepath != "":
                        folder_name = str(water_meter_project_id)
                        file_manager = FileManager()
                        file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                       owner_name='Project')
                        water_meter_project.water_meter_project_files.append(file_result)
                        water_meter_project.save()
                    water_meter_project.save()
                    # ----- add to loger -------
                    second_state = WaterMetersProjects.objects.get(water_meter_project_id=water_meter_project_id)
                    second_device_state_dict = {
                        "water_meter_project_id": second_state.water_meter_project_id,
                        "water_meter_project_name": second_state.water_meter_project_name,
                        "water_meter_project_title": second_state.water_meter_project_title,
                        "water_meter_project_create_date": second_state.water_meter_project_create_date,
                        "water_meter_project_start_date": second_state.water_meter_project_start_date,
                        "water_meter_project_employer_description": second_state.water_meter_project_employer_description,
                        "water_meter_project_contract_number": second_state.water_meter_project_contract_number,
                        "water_meter_project_other_information": second_state.water_meter_project_other_information,
                        "water_meter_project_images": second_state.water_meter_project_images,
                        "water_meter_project_files": second_state.water_meter_project_files,
                        "water_meter_project_urls": second_state.water_meter_project_urls,
                        # "water_meter_types": second_state.water_meter_types
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
                                                                  system_log_object_action_on=water_meter_project_id,
                                                                  system_log_action='Edit',
                                                                  system_log_action_table='WaterMetersProjects',
                                                                  system_log_message=system_log_message,
                                                                  system_log_field_changes=changed_fields)
                    # -------------------------
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_water_meter_project(token, water_meter_project_id):
        """
            param : [token, water_meter_project_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Joker'):
                try:
                    water_meter_project = WaterMetersProjects.objects.get(
                        water_meter_project_id=water_meter_project_id)
                except:
                    wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                    return False, wrong_data_result
                name = water_meter_project.water_meter_project_name
                title = water_meter_project.water_meter_project_title
                final_path = title + "_" + name
                try:
                    base_dir = os.getcwd()
                    media_path = os.path.join(base_dir, 'media')
                    project_path = os.path.join(media_path, 'Project')
                    directory_path = os.path.join(project_path, final_path)
                    shutil.rmtree(directory_path)
                except:
                    pass
                water_meter_project.delete()
                # update all project number in utils table
                utils_object = Utils.objects.filter(name='all_record_count_in_system')
                information = list(utils_object.values())[0].get('information')
                information['water_meter_project'] = information['water_meter_project'] - 1
                utils_object.update(information=information)
                # ------------ add to logger -------------
                admin_object = Admins.objects.get(admin_id=admin_id)
                LogSerializers().system_log_create_serializer(
                    token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                    system_log_field_changes=None, system_log_message=None,
                    system_log_object_action_on=water_meter_project_id, system_log_action_table='WaterMetersProjects')
                # ---------------------------------------
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meter_projects(token, water_meter_project_name, water_meter_project_create_date, page,
                                           count, user_id):
        """
            param : [token, water_meter_project_name, water_meter_project_create_date, page,
                                           count, user_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            # Admin can see all projects
            if AdminsSerializer.admin_check_permission(admin_id, 'Admin'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    if user_id is None:
                        filters = {
                            "water_meter_project_name__contains": water_meter_project_name,
                            "water_meter_project_create_date__contains": water_meter_project_create_date,
                        }
                        filters = {k: v for k, v in filters.items() if v is not None}
                        queryset = WaterMetersProjects.objects.filter(**filters).order_by(
                            '-water_meter_project_create_date')[
                                   offset:offset + limit]
                        response = WaterMetersProjects.objects.serialize(queryset=queryset)
                    else:
                        response = []
                    return True, response
                else:
                    return field_result
            elif AdminsSerializer.admin_check_permission(admin_id, 'ViewProject'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    try:
                        middle_admin_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                    except:
                        wrong_data_result["farsi_message"] = "پروژه ای برای این ادمین ثبت نشده یا ای دی اشتباه است"
                        wrong_data_result[
                            "english_message"] = "project for this admin is not registered or the ID is wrong"
                        return False, wrong_data_result
                    middle_admin_projects = middle_admin_projects.project_ids
                    offset = int((page - 1) * count)
                    limit = int(count)
                    if user_id is None:
                        filters = {
                            "water_meter_project_id__in": middle_admin_projects,
                            "water_meter_project_name__contains": water_meter_project_name,
                            "water_meter_project_create_date__contains": water_meter_project_create_date,
                        }
                        filters = {k: v for k, v in filters.items() if v is not None}
                        queryset = WaterMetersProjects.objects.filter(
                            Q(**filters) | Q(admin__admin_id=admin_id)).order_by(
                            '-water_meter_project_create_date')[
                                   offset:offset + limit]
                        # response = WaterMetersProjects.objects.serialize(queryset=queryset)
                    else:
                        try:
                            all_user_water_meters = WaterMeters.objects.filter(
                                water_meter_project__in=middle_admin_projects,
                                water_meter_user__user_id=user_id).values(
                                'water_meter_project')
                            queryset = WaterMetersProjects.objects.filter(
                                water_meter_project_id__in=all_user_water_meters).order_by(
                                '-water_meter_project_create_date')[
                                       offset:offset + limit]
                            # response = WaterMetersProjects.objects.serialize(queryset=queryset)
                        except:
                            wrong_data_result["farsi_message"] = "user_id اشتباه است"
                            wrong_data_result["english_message"] = "Wrong user_id"
                            return False, wrong_data_result
                    response = WaterMetersProjects.objects.serialize(queryset=queryset, is_middel=True,
                                                                     middel_id=admin_id)
                    return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_water_meter_project(token, water_meter_project_id):
        """
            param : [token, water_meter_project_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ViewProject'):
                # try:
                queryset = WaterMetersProjects.objects.get(
                    water_meter_project_id=water_meter_project_id)
                response = WaterMetersProjects.objects.serialize(queryset=queryset, modify_response=True,
                                                                 pop_item=['all_project_numbers'])
                # except:
                #     wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                #     wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                #     return False, wrong_data_result
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_add_type_too_project_serializer(token, water_meter_type_id, water_meter_project_id):
        """
            param : [token, water_meter_type_id, water_meter_project_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ViewProject'):
                fields = {
                    "water_meter_type_name": (water_meter_type_id, list),
                }
                result = wrong_result(fields)
                if result == None:
                    for id in water_meter_type_id:
                        water_meter_type_id = id
                        type = WaterMetersTypes.objects.get(water_meter_type_id=water_meter_type_id)
                        all_project = WaterMetersProjects.objects.filter(water_meter_project_id=water_meter_project_id)
                        this_project_type = all_project[0].water_meter_types.all().filter(
                            water_meter_type_id=water_meter_type_id)
                        if len(this_project_type) == 0:
                            all_project[0].water_meter_types.add(type)
                        else:
                            pass
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meter_projects_city_count_serializer(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            def city_count(projects):
                all_cities = {}
                for project in projects:
                    project_city = project.water_meter_project_title
                    if project_city not in all_cities:
                        all_cities[project_city] = 1
                    else:
                        all_cities[project_city] += 1
                return all_cities

            if AdminsSerializer.admin_check_permission(admin_id, ['ViewProject', 'Reports']):
                projects = WaterMetersProjects.objects.all()
                all_cities = {}
                for project in projects:
                    project_city = project.water_meter_project_title
                    if project_city not in all_cities:
                        all_cities[project_city] = 1
                    else:
                        all_cities[project_city] += 1
                return True, all_cities
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager', 'Project']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_project = middle_admin.project_ids
                all_cities = {}
                for project_id in middle_admin_project:
                    projects = WaterMetersProjects.objects.filter(water_meter_project_id=project_id)
                    for project in projects:
                        project_city = project.water_meter_project_title
                        if project_city not in all_cities:
                            all_cities[project_city] = 1
                        else:
                            all_cities[project_city] += 1
                return True, all_cities
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_admin_total_statistics_serializer(token):
        """
                    param : [token]
                    return :
                    A tuple containing a boolean indicating the success or failure of the operation, and a list of
                    serialized data results.  it returns a false status along with an error message.
                """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['Reports']):
                all_water_meters = WaterMeters.objects.all()
                project_with_max_counters = all_water_meters.values_list('water_meter_project_id').annotate(
                    max_count=Count('water_meter_project_id')).order_by('-max_count')
                project_counters = []
                projects = WaterMetersProjects.objects.all()
                projects_city_count = projects.values('water_meter_project_title').annotate(
                    all_cities=Count('water_meter_project_title', distinct=True)).count()
                max_city_repetition = projects.values_list('water_meter_project_title').annotate(
                    max_count=Count('water_meter_project_title')).order_by('-max_count')
                max_city_repetition_result = []
                for city in max_city_repetition:
                    if city[1] == max_city_repetition[0][1]:
                        max_city_repetition_result.append(city)
                for project_id in project_with_max_counters:
                    if project_id[1] == project_with_max_counters[0][1]:
                        number_of_counter = all_water_meters.filter(water_meter_project=project_id[0]).count()
                        if project_id[0] != None:
                            project_detail = projects.get(water_meter_project_id=project_id[0])
                            max_project_info = {
                                "water_meter_project_id": str(project_detail.water_meter_project_id),
                                "water_meter_project_title": project_detail.water_meter_project_title,
                                "water_meter_project_name": project_detail.water_meter_project_name,
                                "number_of_counter": number_of_counter,
                            }
                            project_counters.append(max_project_info)
                result = {
                    "all_projects": projects.count(),
                    "all_cities": projects_city_count,
                    "city_with_max_projects": list(max_city_repetition_result),
                    "project_with_max_counters": project_counters,
                }

                return True, result
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager', 'Project']):
                # get middel admin project
                middel_admin_project = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                all_water_meters = WaterMeters.objects.filter(
                    water_meter_project__water_meter_project_id__in=middel_admin_project)
                project_with_max_counters = all_water_meters.values_list('water_meter_project_id').annotate(
                    max_count=Count('water_meter_project_id')).order_by('-max_count')
                project_counters = []
                projects = WaterMetersProjects.objects.filter(water_meter_project_id__in=middel_admin_project)
                projects_city_count = projects.values('water_meter_project_title').annotate(
                    all_cities=Count('water_meter_project_title', distinct=True)).count()
                max_city_repetition = projects.values_list('water_meter_project_title').annotate(
                    max_count=Count('water_meter_project_title')).order_by('-max_count')
                max_city_repetition_result = []
                for city in max_city_repetition:
                    if city[1] == max_city_repetition[0][1]:
                        max_city_repetition_result.append(city)
                for project_id in project_with_max_counters:
                    if project_id[1] == project_with_max_counters[0][1]:
                        number_of_counter = all_water_meters.filter(water_meter_project=project_id[0]).count()
                        if project_id[0] != None:
                            project_detail = projects.get(water_meter_project_id=project_id[0])
                            max_project_info = {
                                "water_meter_project_id": project_detail.water_meter_project_id,
                                "water_meter_project_title": project_detail.water_meter_project_title,
                                "water_meter_project_name": project_detail.water_meter_project_name,
                                "number_of_counter": number_of_counter,
                            }
                            project_counters.append(max_project_info)
                result = {
                    "all_projects": projects.count(),
                    "all_cities": projects_city_count,
                    "city_with_max_projects": max_city_repetition_result,
                    "project_with_max_counters": project_counters,
                }

                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meter_projects(token):
        """
                    param : [token]
                    return :
                    A tuple containing a boolean indicating the success or failure of the operation, and a list of
                    serialized data results.  it returns a false status along with an error message.
                """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            all_user_project = WaterMeters.objects.filter(water_meter_user=user_id).distinct('water_meter_project')
            user_project_list = []
            for project in all_user_project:
                project_dict = project.water_meter_project.as_dict()
                project_dict.pop('admin_info')
                project_dict.pop('water_meter_types')
                user_project_list.append(project_dict)

            return True, user_project_list
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_water_meter_projects(token, water_meter_project_id):
        """
                    param : [token, water_meter_project_id]
                    return :
                    A tuple containing a boolean indicating the success or failure of the operation, and a list of
                    serialized data results.  it returns a false status along with an error message.
                """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                water_meter_project = WaterMetersProjects.objects.get(water_meter_project_id=water_meter_project_id)
            except:
                wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                return False, wrong_data_result
            result = water_meter_project.as_dict()
            result.pop('admin_info')
            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meter_projects_v2(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            all_user_project = WaterMeters.objects.filter(water_meter_user=user_id).distinct(
                'water_meter_project').values('water_meter_project')
            queryset = WaterMetersProjects.objects.filter(water_meter_project_id__in=all_user_project)
            response = WaterMetersProjects.objects.serialize(queryset=queryset)
            return True, response
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_water_meter_projects_v2(token, water_meter_project_id):
        """
            param : [token, water_meter_project_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                water_meter_project = WaterMetersProjects.objects.filter(water_meter_project_id=water_meter_project_id)
            except:
                wrong_data_result["farsi_message"] = "water_meter_project_id اشتباه است"
                wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                return False, wrong_data_result
            queryset = water_meter_project
            response = WaterMetersProjects.objects.serialize(queryset=queryset, req_from='user')
            return True, response
        else:
            return False, wrong_token_result
