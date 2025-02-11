from django.db.models import Count
from persiantools.jdatetime import JalaliDate
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMeters, WaterMetersConsumptions, WaterMetersProjects, \
    WaterMetersTypes, WaterMetersModules
from Authorization.models.Users import Users
from Authorization.models.Admins import Admins
from Authorization.models.MiddleAdmins import MiddleAdmins
from General.models import Utils
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from MQQTReceiver.publisher import publish_message_to_client
from django.db.models import Sum, Q, F, Case, When, Value, IntegerField, Subquery, OuterRef
from General.Serializers.LogSerializers import LogSerializers


class WaterMeterSerializer:
    # ------------------------------------------------- AdminSerializers ----------------------------------------------
    @staticmethod
    def admin_create_water_meter_serializer(
            token, water_meter_user_id, water_meter_serial, water_meter_location, water_meter_validation,
            water_meter_activation, water_meter_condition, other_information, water_meter_type, water_meter_project,
            water_meter_name, water_meter_module, water_meter_manual_number, water_meter_order_mode, water_meter_size,
            water_meter_model):
        """
            param : [token, water_meter_user_id, water_meter_serial, water_meter_location, water_meter_validation,
            water_meter_activation, water_meter_condition, other_information, water_meter_type, water_meter_project,
            water_meter_name, water_meter_module, water_meter_manual_number, water_meter_order_mode]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'MeterCreate'):
                if water_meter_user_id != None and water_meter_project != None:

                    try:

                        admin = Admins.objects.get(admin_id=admin_id)
                        user = Users.objects.get(user_id=water_meter_user_id)
                        type = WaterMetersTypes.objects.get(water_meter_type_id=water_meter_type)
                        project = WaterMetersProjects.objects.get(
                            water_meter_project_id=water_meter_project).water_meter_project_id
                        user_phone_number = user.user_phone
                    except:
                        wrong_data_result["farsi_message"] = "لطفا ای دی های ورودی را چک کنید."
                        wrong_data_result["english_message"] = "please check your input id's. "
                        return False, wrong_data_result
                else:
                    try:
                        admin = Admins.objects.get(admin_id=admin_id)
                        type = WaterMetersTypes.objects.get(water_meter_type_id=water_meter_type)
                        user = water_meter_user_id
                        project = water_meter_project
                        user_phone_number = None
                    except:
                        wrong_data_result["farsi_message"] = "لطفا ای دی های ورودی را چک کنید."
                        wrong_data_result["english_message"] = "please check your input id's. "
                        return False, wrong_data_result
                fields = {
                    "water_meter_location": (water_meter_location, dict),
                    "other_information": (other_information, dict)
                }
                result = wrong_result(fields)
                if result == None:
                    try:
                        if project is not None:
                            project_obj = WaterMetersProjects.objects.get(water_meter_project_id=project)
                        else:
                            project_obj = None
                        if water_meter_module is not None:
                            module_obj = WaterMetersModules.objects.get(
                                water_meter_module_id=water_meter_module).water_meter_module_id
                        else:
                            module_obj = None
                        if user is not None:
                            user_obj = Users.objects.get(user_id=user.user_id)
                        else:
                            user_obj = None

                        WaterMeters.objects.create(
                            water_meter_serial=water_meter_serial, water_meter_admin=admin, water_meter_user=user_obj,
                            water_meter_location=water_meter_location, water_meter_validation=water_meter_validation,
                            water_meter_activation=water_meter_activation, water_meter_condition=water_meter_condition,
                            other_information=other_information, water_meter_type=type, water_meter_project=project_obj,
                            water_meter_name=water_meter_name, water_meter_module_id=module_obj,
                            water_meter_manual_number=water_meter_manual_number,
                            water_meter_order_mode=water_meter_order_mode, water_meter_size=water_meter_size,
                            water_meter_model=water_meter_model
                        )
                        if user_phone_number is not None:
                            publish_message_to_client(phone_number=user_phone_number, from_where='add_device')
                        # update all meter number in utils table
                        utils_object = Utils.objects.filter(name='all_record_count_in_system')
                        information = list(utils_object.values())[0].get('information')
                        information['all_water_meter'] = information['all_water_meter'] + 1
                        utils_object.update(information=information)
                    except:
                        wrong_data_result["farsi_message"] = "کنتور از قبل موجود است"
                        wrong_data_result["english_message"] = "already exists."
                        return False, wrong_data_result
                    admin_object = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(
                        token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                        system_log_field_changes=None, system_log_message=None,
                        system_log_object_action_on=water_meter_serial, system_log_action_table='WaterMeters')
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_remove_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'MeterDelete'):
                try:
                    water_meter = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result
                if water_meter.water_meter_user is not None:
                    user_phone = water_meter.water_meter_user.user_phone
                    publish_message_to_client(phone_number=user_phone, from_where='delete_device')
                if water_meter.water_meter_admin is not None:
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    admin_phone_number = admin_obj.admin_phone
                    middle_admin_publish_data = {
                        'admin_phone_number': admin_phone_number,
                        'meter_serial': water_meter.water_meter_serial,
                        'from_where': 'delete_device'
                    }
                    publish_message_to_client(publish_func='middle_admin', data=middle_admin_publish_data)
                water_meter.delete()
                # update all meter number in utils table
                utils_object = Utils.objects.filter(name='all_record_count_in_system')
                information = list(utils_object.values())[0].get('information')
                information['all_water_meter'] = information['all_water_meter'] - 1
                utils_object.update(information=information)
                admin_object = Admins.objects.get(admin_id=admin_id)
                LogSerializers().system_log_create_serializer(
                    token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                    system_log_field_changes=None, system_log_message=None,
                    system_log_object_action_on=water_meter_serial, system_log_action_table='WaterMeters')
                return True, status_success_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_water_meter_serializer(
            token, water_meter_serial, water_meter_location, water_meter_validation, water_meter_activation,
            water_meter_condition, other_information, water_meter_name, water_meter_module_id, water_meter_user_id,
            water_meter_project_id, call_publisher, water_meter_bill, water_meter_manual_number, water_meter_size,
            water_meter_model):
        """
            param : [token, water_meter_serial, water_meter_location, water_meter_validation, water_meter_activation,
            water_meter_condition, other_information, water_meter_name, water_meter_module_id, water_meter_user_id,
            water_meter_project_id, call_publisher, water_meter_bill, water_meter_manual_number]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            def edit_water_meter(water_meter_serial):
                try:
                    water_meter = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                    first_device_state_dict = {
                        "water_meter_admin": water_meter.water_meter_admin,
                        "water_meter_user": water_meter.water_meter_user,
                        "water_meter_serial": water_meter.water_meter_serial,
                        "water_meter_location": water_meter.water_meter_location,
                        "water_meter_validation": water_meter.water_meter_validation,
                        "water_meter_activation": water_meter.water_meter_activation,
                        "water_meter_condition": water_meter.water_meter_condition,
                        "other_information": water_meter.other_information,
                        "water_meter_create_date": water_meter.water_meter_create_date,
                        "water_meter_type": water_meter.water_meter_type,
                        "water_meter_project": water_meter.water_meter_project,
                        "water_meter_name": water_meter.water_meter_name,
                        "water_meter_module": water_meter.water_meter_module,
                        "water_meter_bill": water_meter.water_meter_bill,
                        "water_meter_manual_number": water_meter.water_meter_manual_number,
                        "water_meter_order_mode": water_meter.water_meter_order_mode,
                        "water_meter_size": water_meter.water_meter_size,
                        "water_meter_model": water_meter.water_meter_model,
                    }
                    if water_meter.water_meter_user is not None:
                        first_device_state_dict['water_meter_user'] = str(water_meter.water_meter_user.user_id)
                    if water_meter.water_meter_type is not None:
                        first_device_state_dict['water_meter_type'] = str(
                            water_meter.water_meter_type.water_meter_type_id)
                    if water_meter.water_meter_project is not None:
                        first_device_state_dict['water_meter_project'] = str(
                            water_meter.water_meter_project.water_meter_project_id)
                    if water_meter.water_meter_module is not None:
                        first_device_state_dict['water_meter_module'] = str(
                            water_meter.water_meter_module.water_meter_module_id)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است،water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result
                fields = {
                    "water_meter_name": (water_meter_name, str),
                    "water_meter_location": (water_meter_location, dict),
                    "water_meter_validation": (water_meter_validation, int),
                    "water_meter_activation": (water_meter_activation, int),
                    "water_meter_condition": (water_meter_condition, int),
                    "other_information": (other_information, dict)
                }
                result = wrong_result(fields)
                if result == None:
                    water_meter.water_meter_location = water_meter_location
                    water_meter.water_meter_validation = water_meter_validation
                    water_meter.water_meter_activation = water_meter_activation
                    water_meter.water_meter_condition = water_meter_condition
                    water_meter.other_information = other_information
                    water_meter.water_meter_name = water_meter_name
                    water_meter.water_meter_manual_number = water_meter_manual_number
                    water_meter.water_meter_size = water_meter_size
                    water_meter.water_meter_model = water_meter_model
                    if water_meter_bill is not None:
                        water_meter.water_meter_bill = water_meter_bill
                    if water_meter_module_id != None:
                        try:
                            module = WaterMetersModules.objects.get(water_meter_module_id=water_meter_module_id)
                            water_meter.water_meter_module = module
                            water_meter.water_meter_validation = 1
                        except:
                            wrong_data_result["farsi_message"] = "اشتباه است water_meter_module_id"
                            wrong_data_result["english_message"] = "Wrong water_meter_module_id"
                            return False, wrong_data_result
                    else:
                        water_meter.water_meter_module = None
                    if water_meter_project_id != None:
                        if water_meter.water_meter_project == None:
                            try:
                                project = WaterMetersProjects.objects.get(water_meter_project_id=water_meter_project_id)
                                project_types = project.water_meter_types.all()
                                project_type_id_list = []
                                for project_type in project_types:
                                    type_id = project_type.water_meter_type_id
                                    project_type_id_list.append(type_id)
                                water_meter_type_id = water_meter.water_meter_type.water_meter_type_id
                                if water_meter_type_id not in project_type_id_list:
                                    wrong_data_result["farsi_message"] = "تایپ کنتور در تایپ های پروژه موجود نیست"
                                    wrong_data_result[
                                        "english_message"] = "Counter type is not available in project types."
                                    return False, wrong_data_result
                                water_meter.water_meter_project = project
                            except:
                                wrong_data_result["farsi_message"] = "اشتباه است water_meter_project_id"
                                wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                                return False, wrong_data_result
                        else:
                            # first_project_id = str(water_meter.water_meter_project.water_meter_project_id)
                            # input_project_id = water_meter_project_id
                            #
                            # if first_project_id == input_project_id:
                            try:
                                project = WaterMetersProjects.objects.get(
                                    water_meter_project_id=water_meter_project_id)
                                project_types = project.water_meter_types.all()
                                project_type_id_list = []
                                for project_type in project_types:
                                    type_id = project_type.water_meter_type_id
                                    project_type_id_list.append(type_id)
                                water_meter_type_id = water_meter.water_meter_type.water_meter_type_id
                                if water_meter_type_id not in project_type_id_list:
                                    wrong_data_result["farsi_message"] = "تایپ کنتور در تایپ های پروژه موجود نیست"
                                    wrong_data_result[
                                        "english_message"] = "Counter type is not available in project types."
                                    return False, wrong_data_result
                                water_meter.water_meter_project = project
                            except:
                                wrong_data_result["farsi_message"] = "اشتباه است water_meter_project_id"
                                wrong_data_result["english_message"] = "Wrong water_meter_project_id"
                                return False, wrong_data_result
                            # else:
                            #     wrong_data_result["farsi_message"] = "این کنتور در پروژه دیگری می باشد ."
                            #     wrong_data_result["english_message"] = "This meter is in another project."
                            #     return False, wrong_data_result
                    else:
                        water_meter.water_meter_project_id = None
                    if water_meter_user_id != None:
                        if water_meter.water_meter_project == None or water_meter.water_meter_module == None:
                            wrong_data_result["farsi_message"] = "ابتدا پروژه و ماژول را اضافه کنید"
                            wrong_data_result["english_message"] = "plz add project and module"
                            return False, wrong_data_result
                        else:
                            try:
                                user = Users.objects.get(user_id=water_meter_user_id)
                                water_meter.water_meter_user = user
                                water_meter.water_meter_activation = 1
                            except:
                                wrong_data_result["farsi_message"] = "اشتباه است water_meter_user_id"
                                wrong_data_result["english_message"] = "Wrong water_meter_user_id"
                                return False, wrong_data_result
                    else:
                        water_meter.water_meter_user = None
                    try:
                        water_meter.save()
                    except:
                        wrong_data_result["farsi_message"] = "این ماژول قبلا انتخاب شده است"
                        wrong_data_result["english_message"] = "This module is already selected."
                        return False, wrong_data_result
                    if water_meter.water_meter_user is not None or water_meter_user_id is not None:
                        if call_publisher is None or call_publisher is True:
                            user_phone = water_meter.water_meter_user.user_phone
                            publish_message_to_client(phone_number=user_phone, from_where='edit_device')
                    if water_meter.water_meter_project is not None:
                        admin_obj = Admins.objects.get(admin_id=admin_id)
                        middle_admin_publish_data = {
                            'admin_phone_number': admin_obj.admin_phone,
                            'meter_serial': water_meter.water_meter_serial,
                            'from_where': 'edit_device'
                        }
                        publish_message_to_client(publish_func='middle_admin', data=middle_admin_publish_data)
                    second_device_state = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                    second_device_state_dict = {"water_meter_admin": second_device_state.water_meter_admin,
                                                "water_meter_user": second_device_state.water_meter_user,
                                                "water_meter_serial": second_device_state.water_meter_serial,
                                                "water_meter_location": second_device_state.water_meter_location,
                                                "water_meter_validation": second_device_state.water_meter_validation,
                                                "water_meter_activation": second_device_state.water_meter_activation,
                                                "water_meter_condition": second_device_state.water_meter_condition,
                                                "other_information": second_device_state.other_information,
                                                "water_meter_create_date": second_device_state.water_meter_create_date,
                                                "water_meter_type": second_device_state.water_meter_type,
                                                "water_meter_project": second_device_state.water_meter_project,
                                                "water_meter_name": second_device_state.water_meter_name,
                                                "water_meter_module": second_device_state.water_meter_module,
                                                "water_meter_bill": second_device_state.water_meter_bill,
                                                "water_meter_manual_number": second_device_state.water_meter_manual_number,
                                                "water_meter_order_mode": second_device_state.water_meter_order_mode,
                                                "water_meter_size": water_meter.water_meter_size,
                                                "water_meter_model": water_meter.water_meter_model,
                                                }
                    if water_meter.water_meter_user is not None:
                        second_device_state_dict['water_meter_user'] = str(water_meter.water_meter_user.user_id)
                    if water_meter.water_meter_type is not None:
                        second_device_state_dict['water_meter_type'] = str(
                            water_meter.water_meter_type.water_meter_type_id)
                    if water_meter.water_meter_project is not None:
                        second_device_state_dict[
                            'water_meter_project'] = str(water_meter.water_meter_project.water_meter_project_id)
                    if water_meter.water_meter_module is not None:
                        second_device_state_dict[
                            'water_meter_module'] = str(water_meter.water_meter_module.water_meter_module_id)

                    changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                      first_device_state_dict if
                                      first_device_state_dict[key] != second_device_state_dict[key]}
                    system_log_message = ''
                    for key, values in changed_fields.items():
                        system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(token=token, system_log_admin=admin_obj,
                                                                  system_log_user=None,
                                                                  system_log_object_action_on=water_meter_serial,
                                                                  system_log_action='Edit',
                                                                  system_log_action_table='WaterMeters',
                                                                  system_log_message=system_log_message,
                                                                  system_log_field_changes=changed_fields)
                    return True, status_success_result
                else:
                    return result

            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', "MeterEdit"]):
                result = edit_water_meter(water_meter_serial=water_meter_serial)
                return result
            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'MeterEdit']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_water_meters = middle_admin.water_meter_ids
                if water_meter_serial in middle_admin_water_meters:
                    result = edit_water_meter(water_meter_serial=water_meter_serial)
                    return result
                else:
                    wrong_data_result["farsi_message"] = "شماره سریال متعلق به کنتور های این ادمین نیست"
                    wrong_data_result["english_message"] = "water_meter_serial is not middle admin water meter's ."
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meters_serializer_by_filter(
            token, page, count, water_meter_validation, water_meter_activation, water_meter_condition,
            water_meter_location, water_meter_type, water_meter_project):
        """
            param : [token, page, count, water_meter_validation, water_meter_activation, water_meter_condition,
            water_meter_location, water_meter_type, water_meter_project]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        global all_water_meters
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Admin'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    if len(water_meter_type) == 0 and len(water_meter_project) == 0:
                        all_water_meters = WaterMeters.objects.filter(
                            water_meter_validation__icontains=water_meter_validation,
                            water_meter_activation__contains=water_meter_activation,
                            water_meter_condition__contains=water_meter_condition,
                            water_meter_location__icontains=water_meter_location
                        ).order_by('-water_meter_create_date')[offset:offset + limit]
                    elif len(water_meter_type) > 0 and len(water_meter_project) == 0:
                        try:
                            input_type = WaterMetersTypes.objects.get(water_meter_type_name=water_meter_type)
                        except:
                            wrong_data_result["farsi_message"] = "اشتباه است water_meter_type_name"
                            wrong_data_result["english_message"] = "Wrong water_meter_type_name"
                            return False, wrong_data_result
                        all_water_meters = WaterMeters.objects.filter(
                            # water_meter_validation__contains=water_meter_validation,
                            # water_meter_activation__contains=water_meter_activation,
                            # water_meter_condition__contains=water_meter_condition,
                            # water_meter_location__icontains=water_meter_location,
                            water_meter_type=input_type
                        ).order_by('-water_meter_create_date')[offset:offset + limit]
                    elif len(water_meter_type) == 0 and len(water_meter_project) > 0:
                        try:
                            input_project = WaterMetersProjects.objects.get(water_meter_project_id=water_meter_project)
                        except:
                            wrong_data_result["farsi_message"] = "اشتباه است water_meter_project_id"
                            wrong_data_result[
                                "english_message"] = "Wrong water_meter_project_id"
                            return False, wrong_data_result
                        all_water_meters = WaterMeters.objects.filter(
                            # water_meter_validation__contains=water_meter_validation,
                            # water_meter_activation__contains=water_meter_activation,
                            # water_meter_condition__contains=water_meter_condition,
                            # water_meter_location__icontains=water_meter_location,
                            water_meter_project=input_project
                        ).order_by('-water_meter_create_date')[offset:offset + limit]

                    elif len(water_meter_type) > 0 and len(water_meter_project) > 0:
                        try:
                            input_project = WaterMetersProjects.objects.get(water_meter_project_id=water_meter_project)
                            input_type = WaterMetersTypes.objects.get(water_meter_type_name=water_meter_type)
                        except:
                            wrong_data_result["farsi_message"] = "اشتباه است  water_meter_project_id با type"
                            wrong_data_result[
                                "english_message"] = "Wrong water_meter_project_id or type"
                            return False, wrong_data_result
                        all_water_meters = WaterMeters.objects.filter(
                            # water_meter_validation__contains=water_meter_validation,
                            # water_meter_activation__contains=water_meter_activation,
                            # water_meter_condition__contains=water_meter_condition,
                            # water_meter_location__icontains=water_meter_location,
                            water_meter_project=input_project,
                            water_meter_type=input_type
                        ).order_by('-water_meter_create_date')[offset:offset + limit]

                    # water_meter_count = (WaterMeters.objects.count())
                    # all_water_meters = [water_meter.as_dict() for water_meter in all_water_meters]
                    All_water_meters = []
                    for water_meter in all_water_meters:
                        water_meter_result = water_meter.as_dict()
                        print(water_meter_result['water_meter_type_info'])
                        water_meter_result.update({
                            'admin': water_meter_result['admin']['admin_id'],
                            'user': {'user_id': water_meter_result['user']['user_id'],
                                     'user_name': water_meter_result['user']['user_name'],
                                     'user_lastname': water_meter_result['user']['user_lastname'],
                                     },
                            'water_meter_type_info': water_meter_result['water_meter_type_info'][
                                'water_meter_type_name'],
                            'water_meter_project_info': {
                                'water_meter_project_name':
                                    water_meter_result['water_meter_project_info']['water_meter_project_name'],
                                'water_meter_project_id':
                                    water_meter_result['water_meter_project_info']['water_meter_project_id'],
                            },
                            "all water meters": len(all_water_meters)
                        })
                        All_water_meters.append(water_meter_result)
                    return True, All_water_meters
                else:
                    return field_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_water_meters_serializer(token, page, count, user_id, project_id, water_meter_serial,
                                              water_meter_tag_id):
        """
            param : [token, page, count, user_id, project_id, water_meter_serial,
                                              water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'MeterList']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    if user_id == 0 and project_id == 0:
                        queryset = WaterMeters.objects.filter(
                            Q(water_meter_user=None), Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]
                        response = WaterMeters.objects.serialize(queryset=queryset)

                    elif user_id == 0 or project_id == 0:
                        queryset = WaterMeters.objects.filter(
                            Q(water_meter_user=None) | Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]
                        response = WaterMeters.objects.serialize(queryset=queryset)
                    else:
                        filters = {
                            'water_meter_serial__icontains': water_meter_serial,
                            'water_meter_user__user_id': user_id,
                            'water_meter_project__water_meter_project_id': project_id,
                            "water_meter_type__water_meter_tag__water_meter_tag_id": water_meter_tag_id
                        }
                        filters = {k: v for k, v in filters.items() if v is not None}
                        try:
                            queryset = WaterMeters.objects.filter(**filters).order_by(
                                '-water_meter_create_date')[
                                       offset:offset + limit]
                            response = WaterMeters.objects.serialize(queryset=queryset)
                            # response = list(queryset)
                        except:
                            response = []

                    return True, response
                else:
                    return field_result

            elif AdminsSerializer.admin_check_permission(admin_id, ['Middle']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_water_meters = middle_admin.water_meter_ids
                middle_admin_projects = middle_admin.project_ids
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    if user_id == 0 and project_id == 0:
                        queryset = WaterMeters.objects.filter(
                            Q(water_meter_serial__in=middle_admin_water_meters),
                            Q(water_meter_user=None), Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]
                        response = WaterMeters.objects.serialize(queryset=queryset)

                    elif user_id == 0 or project_id == 0:
                        queryset = WaterMeters.objects.filter(
                            Q(water_meter_project__in=middle_admin_projects),
                            Q(water_meter_user=None) | Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]
                        response = WaterMeters.objects.serialize(queryset=queryset)
                    else:
                        filters = {
                            'water_meter_user__user_id': user_id,
                        }
                        if project_id is None:
                            filters['water_meter_project__in'] = middle_admin_projects
                        else:
                            filters['water_meter_project__water_meter_project_id'] = project_id
                        filters = {k: v for k, v in filters.items() if v is not None}
                        try:
                            queryset = WaterMeters.objects.filter(**filters).order_by(
                                '-water_meter_create_date')[
                                       offset:offset + limit]
                            response = WaterMeters.objects.serialize(queryset=queryset)
                        except:
                            response = []

                    return True, response
                else:
                    return field_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, 'MeterDetail'):
                try:
                    queryset = WaterMeters.objects.filter(water_meter_serial=water_meter_serial)
                    response = WaterMeters.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
        
    @staticmethod
    def admin_get_location_serializer(token, type_id_list, project_id_list, tag_id_list):
        """
            param : [token, type_id_list, project_id_list, tag_id_list]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results. If unsuccessful, returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            # SuperAdmin Logic
            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
                filters = {
                    'water_meter_type__in': type_id_list,
                    'water_meter_project__in': project_id_list,
                    'water_meter_type__water_meter_tag__water_meter_tag_id__in': tag_id_list,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                
                try:
                    queryset = WaterMeters.objects.filter(**filters).values(
                        'water_meter_serial', 'water_meter_location', 'water_meter_name',
                        'water_meter_type__water_meter_type_name', 
                        'water_meter_type__water_meter_tag__water_meter_tag_name',
                        'water_meter_project__water_meter_project_name'
                    ).order_by('-water_meter_create_date')
                    response = list(queryset)
                except:
                    response = []
                return True, response

            # MiddleAdmin Logic: Only return locations within projects assigned to this MiddleAdmin
            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'ProjectList']):
                try:
                    middle_admin_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                except:
                    wrong_data_result = {
                        "farsi_message": "پروژه ای برای این ادمین ثبت نشده یا ای دی اشتباه است",
                        "english_message": "Project for this admin is not registered or the ID is wrong"
                    }
                    return False, wrong_data_result

                middle_admin_projects = middle_admin_projects.project_ids
                
                filters = {
                    'water_meter_project__in': middle_admin_projects,
                    'water_meter_type__in': type_id_list,
                    'water_meter_type__water_meter_tag__water_meter_tag_id__in': tag_id_list,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                
                try:
                    queryset = WaterMeters.objects.filter(**filters).values(
                        'water_meter_serial', 'water_meter_location', 'water_meter_name',
                        'water_meter_type__water_meter_type_name', 
                        'water_meter_type__water_meter_tag__water_meter_tag_name',
                        'water_meter_project__water_meter_project_name'
                    ).order_by('-water_meter_create_date')
                    response = list(queryset)
                except:
                    response = []
                return True, response

            # Invalid token or permissions
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_count_all_water_meter_serializer(token, type, project, water_meter_activation,
                                               water_meter_validation):
        """
            param : [token, type, project, water_meter_activation,
                                               water_meter_validation]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'Meter']):
                # result = Utils.objects.get(name='all_record_count_in_system').information
                result = {
                    "all_users": Users.objects.count(),
                    "all_water_meter": WaterMeters.objects.count(),
                    "water_meter_type": WaterMetersTypes.objects.count(),
                    "water_meter_project": WaterMetersProjects.objects.count(),
                    "water_meter_condition": WaterMeters.objects.filter(water_meter_condition=1).count(),
                    "water_meter_activation": WaterMeters.objects.filter(water_meter_activation=1).count(),
                    "water_meter_validation": WaterMeters.objects.filter(water_meter_validation=1).count(),
                    "all_consumption_records": 266421
                }
                return True, result

            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'Meter']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                # middle_admin_water_meters = middle_admin.water_meter_ids
                middle_admin_projects = middle_admin.project_ids
                middle_admin_water_meters = WaterMeters.objects.filter(water_meter_project__in=middle_admin_projects)
                # all_water_meter_count
                all_water_meter_count = middle_admin_water_meters.count()

                # water_meter_activation count
                if water_meter_activation != None:
                    activated_water_meter = middle_admin_water_meters.filter(
                        water_meter_activation=water_meter_activation).count()
                else:
                    activated_water_meter = middle_admin_water_meters.filter(water_meter_activation=1).count()
                # water_meter_validation count
                if water_meter_validation != None:
                    validated_water_meter = middle_admin_water_meters.filter(
                        water_meter_validation=water_meter_validation).count()
                else:
                    validated_water_meter = middle_admin_water_meters.filter(water_meter_validation=1).count()
                # condition count
                condition = middle_admin_water_meters.filter(water_meter_condition=1).count()

                # type count
                if type != None:
                    water_meter_type = middle_admin_water_meters.filter(water_meter_type_name=type).count()
                else:
                    water_meter_type = middle_admin_water_meters.values('water_meter_type').distinct().count()

                # project count
                if project != None:
                    water_meter_project = middle_admin_water_meters.filter(
                        water_meter_project_name=project).count()
                else:
                    water_meter_project = middle_admin_water_meters.values('water_meter_project').distinct().count()

                # users count
                users_from_user = Users.objects.filter(admin=admin_id).values('user_id').distinct()
                users_from_water_meter = middle_admin_water_meters.values('water_meter_user').distinct()
                users_count = users_from_water_meter.count()
                for user in users_from_user:
                    if user not in users_from_water_meter:
                        users_count += 1

                # all_consumptions count
                all_consumption_records = WaterMetersConsumptions.objects.filter(
                    water_meters__in=middle_admin_water_meters).count()

                result = {
                    "water_meter_activation": activated_water_meter,
                    "water_meter_validation": validated_water_meter,
                    "water_meter_condition": condition,
                    "water_meter_type": water_meter_type,
                    "water_meter_project": water_meter_project,
                    "all_users": users_count,
                    "all_consumption_records": all_consumption_records,
                    # "sum_all_consumption_value": sum_all_consumption_value,
                    "all_water_meter": all_water_meter_count
                }
                return True, result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_count_all_by_filters_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, type, project, water_meter_activation,
                                               water_meter_validation]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'Meter']):
                try:
                    # get middle admin project
                    middle_admin_object = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                    middle_admin_projects = middle_admin_object.project_ids
                    filters = {
                        "water_meters__water_meter_serial": water_meter_serial,
                        "water_meters__water_meter_project__water_meter_project_id__in": middle_admin_projects,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    consumptions = WaterMetersConsumptions.objects.filter(**filters).values(
                        'water_meters').annotate(consumption_records_number=Count('water_meters'))
                    # result = dict(map(lambda x: (x['water_meters'], x['consumption_records_number']), consumptions))
                    result = list(consumptions)
                    return True, result
                except:
                    wrong_data_result["farsi_message"] = "کنتوری یافت نشد"
                    wrong_data_result["english_message"] = "Meters not found"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_assign_user_to_water_meter_serializer(token, user_phone, water_meter_list):
        """
            param : [token, user_phone, water_meter_list]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            def assign_user(user_phone, water_meter_list):
                try:
                    user_obj = Users.objects.get(user_phone=user_phone)
                except:
                    wrong_data_result["farsi_message"] = "شماره تلفن کاربر اشتباه است"
                    wrong_data_result["english_message"] = "user's phone number is wrong"
                    return False, wrong_data_result

                # get water meter object's
                water_meter_objects = WaterMeters.objects.filter(water_meter_serial__in=water_meter_list)
                water_meters_updated = water_meter_objects.update(water_meter_user=user_obj)
                result = {
                    "water_meter_update_number": water_meters_updated
                }
                return True, result

            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'Meter']):
                result = assign_user(user_phone=user_phone, water_meter_list=water_meter_list)
                return result
            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'Meter']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_projects = middle_admin.project_ids
                middle_admin_water_meters = WaterMeters.objects.filter(water_meter_project__in=middle_admin_projects)
                for water_meter_serial in water_meter_list:
                    if water_meter_serial not in middle_admin_water_meters:
                        wrong_data_result["farsi_message"] = "شماره سریال متعلق به کنتور های این ادمین نیست"
                        wrong_data_result["english_message"] = "water_meter_serial is not middle admin water meter's ."
                        return False, wrong_data_result
                result = assign_user(user_phone=user_phone, water_meter_list=water_meter_list)
                return result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_value_water_meter_serializer(token, consumption_id, value, cumulative_value):
        """
            param : [token, consumption_id, value, cumulative_value]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'Meter']):
                if value is not None and cumulative_value is None:
                    WaterMetersConsumptions.objects.filter(consumption_id=consumption_id) \
                        .update(value=value)
                    return True, status_success_result
                if value is not None and cumulative_value is not None:
                    WaterMetersConsumptions.objects.filter(consumption_id=consumption_id) \
                        .update(value=value, cumulative_value=cumulative_value)
                    return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def v2_admin_get_all_water_meters_serializer(token, page, count, user_id, project_id, water_meter_serial,
                                                 water_meter_tag_id, water_meter_size, water_meter_model,
                                                 water_meter_type_id, has_module,has_user):
        """
            param : [token, page, count, user_id, project_id, water_meter_serial,
                                                 water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'Meter']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    if user_id == 0 and project_id == 0:
                        queryset = WaterMeters.objects.filter(
                            Q(water_meter_user=None), Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]

                    elif user_id == 0 or project_id == 0:
                        queryset = WaterMeters.objects.filter(
                            Q(water_meter_user=None) | Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]
                    else:
                        filters = {
                            'water_meter_size': water_meter_size,
                            'water_meter_model': water_meter_model,
                            'water_meter_serial__icontains': water_meter_serial,
                            'water_meter_user__user_id': user_id,
                            'water_meter_type__water_meter_type_id': water_meter_type_id,
                            'water_meter_project__water_meter_project_id': project_id,
                            "water_meter_type__water_meter_tag__water_meter_tag_id": water_meter_tag_id
                        }
                        filters = {k: v for k, v in filters.items() if v is not None}
                        try:
                            meters = WaterMeters.objects.filter(**filters)
                            if has_module is False:
                                meters = meters.filter(water_meter_module=None)
                            if has_module is True:
                                meters = meters.exclude(water_meter_module=None)
                                if has_user is False:
                                    meters = meters.filter(water_meter_user=None)
                                if has_user is True:
                                    meters = meters.exclude(water_meter_user=None)

                            sub_query = len(meters)
                            queryset = meters.annotate(
                                all_water_meters=Value(sub_query, output_field=IntegerField()))
                            response = queryset.values(
                                'all_water_meters',
                                'water_meter_name',
                                'water_meter_serial',
                                'water_meter_location',
                                'water_meter_validation',
                                'water_meter_condition',
                                'water_meter_activation',
                                'other_information',
                                # 'water_meter_create_date',
                                # 'water_meter_create_date',
                                'water_meter_bill',
                                'water_meter_manual_number',
                                'water_meter_order_mode',
                                'water_meter_size',
                                'water_meter_model',
                                'water_meter_type__water_meter_type_name',
                                'water_meter_type__water_meter_type_id',
                                'water_meter_type__water_meter_tag__water_meter_tag_name',
                                'water_meter_type__water_meter_tag__water_meter_tag_id',
                                # 'water_meter_type__water_meter_tag__water_meter_tag_create_date',
                                'water_meter_user__user_id',
                                'water_meter_user__user_name',
                                'water_meter_user__user_lastname',
                                'water_meter_user__user_phone',
                                'water_meter_user__other_information',
                                'water_meter_user__other_information',
                                'water_meter_project__water_meter_project_id',
                                'water_meter_project__water_meter_project_name',
                                'water_meter_project__water_meter_project_title',
                                # 'water_meter_project__water_meter_project_create_date',
                                'water_meter_module__water_meter_module_id',
                                'water_meter_module__water_meter_module_code',
                                'water_meter_module__water_meter_module_name',
                                'water_meter_module__water_meter_module_property',
                                # 'water_meter_module__water_meter_module_create_date',
                                'water_meter_module__module_type__module_type_id',
                                'water_meter_module__module_type__module_type_name',
                                'water_meter_module__module_type__module_type_create_date',
                                'water_meter_module__module_type__module_other_information',
                            ).order_by(
                                '-water_meter_create_date')[
                                       offset:offset + limit]
                            response = list(response)
                        except:
                            response = []
                        return True, response
                else:
                    return field_result

            elif AdminsSerializer.admin_check_permission(admin_id, ['MiddleAdmin', 'Meter']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    middel_admin_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                    middel_water_meters = WaterMeters.objects.filter(Q(water_meter_admin__admin_id=admin_id) |
                                                                     Q(water_meter_project__water_meter_project_id__in=middel_admin_projects))
                    if user_id == 0 and project_id == 0:
                        queryset = middel_water_meters.filter(
                            Q(water_meter_user=None), Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]

                    elif user_id == 0 or project_id == 0:
                        queryset = middel_water_meters.filter(
                            Q(water_meter_user=None) | Q(water_meter_project=None)).order_by(
                            '-water_meter_create_date')[
                                   offset:offset + limit]
                    else:
                        filters = {
                            'water_meter_size': water_meter_size,
                            'water_meter_model': water_meter_model,
                            'water_meter_type__water_meter_type_id': water_meter_type_id,
                            'water_meter_serial__icontains': water_meter_serial,
                            'water_meter_user__user_id': user_id,
                            'water_meter_project__water_meter_project_id': project_id,
                            "water_meter_type__water_meter_tag__water_meter_tag_id": water_meter_tag_id
                        }
                        filters = {k: v for k, v in filters.items() if v is not None}
                        try:
                            sub_query = middel_water_meters.count()
                            queryset = middel_water_meters.filter(**filters).annotate(
                                all_water_meters=Value(sub_query, output_field=IntegerField()))
                        except:
                            response = []
                    response = queryset.values(
                        'all_water_meters',
                        'water_meter_name',
                        'water_meter_serial',
                        'water_meter_location',
                        'water_meter_validation',
                        'water_meter_condition',
                        'water_meter_size',
                        'water_meter_model',
                        'other_information',
                        'water_meter_create_date',
                        'water_meter_create_date',
                        'water_meter_bill',
                        'water_meter_manual_number',
                        'water_meter_order_mode',
                        'water_meter_order_mode',
                        'water_meter_type__water_meter_type_name',
                        'water_meter_type__water_meter_tag__water_meter_tag_name',
                        'water_meter_type__water_meter_tag__water_meter_tag_id',
                        'water_meter_type__water_meter_tag__water_meter_tag_create_date',
                        'water_meter_user__user_id',
                        'water_meter_user__user_name',
                        'water_meter_user__user_lastname',
                        'water_meter_user__user_phone',
                        'water_meter_user__other_information',
                        'water_meter_user__other_information',
                        'water_meter_project__water_meter_project_id',
                        'water_meter_project__water_meter_project_name',
                        'water_meter_project__water_meter_project_title',
                        'water_meter_project__water_meter_project_create_date',
                        'water_meter_module__water_meter_module_id',
                        'water_meter_module__water_meter_module_code',
                        'water_meter_module__water_meter_module_name',
                        'water_meter_module__water_meter_module_create_date',
                        'water_meter_module__water_meter_module_other_information',
                    ).order_by(
                        '-water_meter_create_date')[
                               offset:offset + limit]

                    response = list(response)

                    return True, response
                else:
                    return field_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    # -----------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------- UserSerializers -----------------------------------------------
    @staticmethod
    def user_get_one_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            if user_id == user_id:
                try:
                    water_meter = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                    consumptions = WaterMetersConsumptions.objects.filter(water_meters=water_meter).last()
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result
                water_meter_info = {
                    "water_meter_name": water_meter.water_meter_name,
                    "water_meter_serial": water_meter.water_meter_serial,
                    "water_meter_location": water_meter.water_meter_location,
                    "water_meter_validation": water_meter.water_meter_validation,
                    "water_meter_activation": water_meter.water_meter_activation,
                    "water_meter_condition": water_meter.water_meter_condition,
                    "other_information": water_meter.other_information,
                    "water_meter_create_date": water_meter.water_meter_create_date,
                    # "all_consumption_value": consumption.sum_all_value,
                    "water_meter_type_info": {
                        "water_meter_type_name": water_meter.water_meter_type.water_meter_type_name,
                        "water_meter_type_id": water_meter.water_meter_type.water_meter_type_id,
                        "water_meter_type_files": water_meter.water_meter_type.water_meter_type_files,
                        "water_meter_type_create_date": water_meter.water_meter_type.water_meter_type_create_date,
                    },
                    "water_meter_tag_info": {
                        "water_meter_tag_name": water_meter.water_meter_type.water_meter_tag.water_meter_tag_name,
                        "water_meter_tag_id": water_meter.water_meter_type.water_meter_tag.water_meter_tag_id,
                        "water_meter_tag_create_date": water_meter.water_meter_type.water_meter_tag.water_meter_tag_create_date
                    },
                    "water_meter_user_info": {"user_id": water_meter.water_meter_user.user_id,
                                              "user_name": water_meter.water_meter_user.user_name,
                                              "user_lastname": water_meter.water_meter_user.user_lastname,
                                              "user_phone": water_meter.water_meter_user.user_phone,
                                              "other_information": water_meter.water_meter_user.other_information, },
                    "water_meter_project_info": {
                        "project_id": water_meter.water_meter_project.water_meter_project_id,
                        "project_name": water_meter.water_meter_project.water_meter_project_name,
                        "project_title": water_meter.water_meter_project.water_meter_project_title,
                        "project_create_date": water_meter.water_meter_project.water_meter_project_create_date, },
                    "water_meter_module_info": {},
                    # "all_water_meters": len(all_user_water_meters),
                }
                if consumptions != None:
                    water_meter_info['sum_all_consumptions'] = consumptions.sum_all_value
                else:
                    water_meter_info['sum_all_consumptions'] = ""
                if water_meter.water_meter_module != None:
                    water_meter_info['water_meter_module_info'] = {
                        "water_meter_module_id": water_meter.water_meter_module.water_meter_module_id,
                        "water_meter_module_code": water_meter.water_meter_module.water_meter_module_code,
                        "water_meter_module_name": water_meter.water_meter_module.water_meter_module_name,
                        "water_meter_module_unit": water_meter.water_meter_module.water_meter_module_unit,
                        "water_meter_module_create_date": water_meter.water_meter_module.water_meter_module_create_date,
                        "water_meter_module_other_information": water_meter.water_meter_module.water_meter_module_other_information,
                    }
                else:
                    water_meter_info['water_meter_module_info'] = {
                        "water_meter_module_id": "",
                        "water_meter_module_code": "",
                        "water_meter_module_name": "",
                        "water_meter_module_create_date": "",
                        "water_meter_module_other_information": "",
                    }
                return True, water_meter_info
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meters_serializer(token, page, count, water_meter_tag_id):
        """
            param : [token, page, count, water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                "page": (page, int),
                "count": (count, int),
            }
            field_result = wrong_result(fields)
            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "water_meter_user": user_id,
                    "water_meter_type__water_meter_tag": water_meter_tag_id,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                try:
                    all_user_water_meters = WaterMeters.objects.filter(**filters)
                    all_user_water_meters_paginated = all_user_water_meters.order_by(
                        '-water_meter_create_date')[
                                                      offset:offset + limit]
                    all_user_water_meters_count = all_user_water_meters.count()
                    all_user_consumptions = WaterMetersConsumptions.objects.filter(
                        water_meters__in=all_user_water_meters)
                    all_user_consumptions_count = all_user_consumptions.count()
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_tag"
                    wrong_data_result["english_message"] = "Wrong water_meter_tag"
                    return False, wrong_data_result
                user_consumption_water_meters = []
                for user_cons_val in all_user_consumptions.values('water_meters'):
                    user_consumption_water_meters.append(user_cons_val['water_meters'])
                All_water_meters = []
                for water_meter in all_user_water_meters_paginated:
                    consumption_count_per_water_meter = all_user_consumptions.filter(
                        water_meters=water_meter.water_meter_serial)
                    if len(consumption_count_per_water_meter) != 0:
                        consumptions_count = consumption_count_per_water_meter.count()
                        consumptions_last = consumption_count_per_water_meter.last()
                    else:
                        consumptions_count = 0
                        consumptions_last = None
                    water_meter_info = {
                        "water_meter_name": water_meter.water_meter_name,
                        "water_meter_serial": water_meter.water_meter_serial,
                        "water_meter_location": water_meter.water_meter_location,
                        "water_meter_validation": water_meter.water_meter_validation,
                        "water_meter_activation": water_meter.water_meter_activation,
                        "water_meter_condition": water_meter.water_meter_condition,
                        "other_information": water_meter.other_information,
                        "water_meter_create_date": water_meter.water_meter_create_date,
                        "water_meter_type_info": {
                            "water_meter_type_name": water_meter.water_meter_type.water_meter_type_name,
                            "water_meter_type_id": water_meter.water_meter_type.water_meter_type_id,
                            "water_meter_type_files": water_meter.water_meter_type.water_meter_type_files,
                            "water_meter_type_create_date": water_meter.water_meter_type.water_meter_type_create_date,
                        },
                        "water_meter_tag_info": {
                            "water_meter_tag_name": water_meter.water_meter_type.water_meter_tag.water_meter_tag_name,
                            "water_meter_tag_id": water_meter.water_meter_type.water_meter_tag.water_meter_tag_id,
                            "water_meter_tag_create_date": water_meter.water_meter_type.water_meter_tag.water_meter_tag_create_date
                        },
                        "water_meter_user_info": {"user_id": water_meter.water_meter_user.user_id,
                                                  "user_name": water_meter.water_meter_user.user_name,
                                                  "user_lastname": water_meter.water_meter_user.user_lastname,
                                                  "user_phone": water_meter.water_meter_user.user_phone,
                                                  "other_information": water_meter.water_meter_user.other_information, },
                        "water_meter_project_info": {
                            "project_id": water_meter.water_meter_project.water_meter_project_id,
                            "project_name": water_meter.water_meter_project.water_meter_project_name,
                            "project_title": water_meter.water_meter_project.water_meter_project_title,
                            "project_create_date": water_meter.water_meter_project.water_meter_project_create_date, },
                        "water_meter_module_info": {},
                        "all_water_meters": all_user_water_meters_count,
                        "all_water_meter_consumption": consumptions_count,
                        "all_user_consumption": all_user_consumptions_count,
                    }

                    if consumptions_last != None:
                        water_meter_info['sum_all_consumptions'] = consumptions_last.sum_all_value
                    else:
                        water_meter_info['sum_all_consumptions'] = ""
                    if water_meter.water_meter_module != None:
                        water_meter_info['water_meter_module_info'] = {
                            "water_meter_module_id": water_meter.water_meter_module.water_meter_module_id,
                            "water_meter_module_code": water_meter.water_meter_module.water_meter_module_code,
                            "water_meter_module_name": water_meter.water_meter_module.water_meter_module_name,
                            "water_meter_module_unit": water_meter.water_meter_module.water_meter_module_unit,
                            "water_meter_module_create_date": water_meter.water_meter_module.water_meter_module_create_date,
                            "water_meter_module_other_information": water_meter.water_meter_module.water_meter_module_other_information,
                        }
                    else:
                        water_meter_info['water_meter_module_info'] = {
                            "water_meter_module_id": "",
                            "water_meter_module_code": "",
                            "water_meter_module_name": "",
                            "water_meter_module_create_date": "",
                            "water_meter_module_other_information": {"description": ""},
                        }
                    All_water_meters.append(water_meter_info)
                return True, All_water_meters
            else:
                return field_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_count_all_water_meter_serializer(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            user_water_meters = WaterMeters.objects.filter(water_meter_user__user_id=user_id)
            user_types = WaterMetersTypes.objects.filter(
                water_meter_type_id__in=user_water_meters.values('water_meter_type'))
            user_projects = WaterMetersProjects.objects.filter(
                water_meter_project_id__in=user_water_meters.values('water_meter_project'))
            user_consumption_records = WaterMetersConsumptions.objects.filter(
                water_meters__in=user_water_meters.values('water_meter_serial'))
            user_water_meters_count = user_water_meters.count()
            user_types_count = user_types.count()
            user_consumptions_count = user_consumption_records.count()
            user_consumption_records_per_date = user_consumption_records.values_list('create_time__date',
                                                                                     flat=True).distinct().count()

            user_projects_count = user_projects.count()
            result = {
                "all_water_meter": user_water_meters_count,
                "all_consumption_records": user_consumptions_count,
                "user_consumption_records_per_date": user_consumption_records_per_date,
                "water_meter_type": user_types_count,
                "water_meter_project": user_projects_count,
            }

            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_count_all_by_filters_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            filters = {
                'water_meters__water_meter_serial': water_meter_serial,
                'water_meters__water_meter_user__user_id': user_id
            }
            filters = {k: v for k, v in filters.items() if v is not None}
            all_consumption = WaterMetersConsumptions.objects.filter(**filters)
            # all_consumption_order_by  = all_consumption.order_by('-create_time')
            user_consumption_records = all_consumption.count()
            result = {
                "consumption_records_number": user_consumption_records,
            }

            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_water_meter_serializer_v2(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            if user_id == user_id:
                try:
                    queryset = WaterMeters.objects.filter(water_meter_serial=water_meter_serial)
                    response = WaterMeters.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_water_meters_serializer_v2(token, page, count, water_meter_tag_id):
        """
            param : [token, page, count, water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                "page": (page, int),
                "count": (count, int),
            }
            field_result = wrong_result(fields)
            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "water_meter_user": user_id,
                    "water_meter_type__water_meter_tag": water_meter_tag_id,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                try:
                    all_user_water_meters = WaterMeters.objects.filter(**filters)
                    all_user_water_meters_paginated = all_user_water_meters.order_by(
                        '-water_meter_create_date')[
                                                      offset:offset + limit]
                    queryset = all_user_water_meters_paginated
                    response = WaterMeters.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_tag"
                    wrong_data_result["english_message"] = "Wrong water_meter_tag"
                    return False, wrong_data_result

            else:
                return field_result
        else:
            return False, wrong_token_result
    # -----------------------------------------------------------------------------------------------------------------
