import requests, datetime, json, random, time, os, shutil, re
from datetime import timedelta, timezone
from threading import Thread
from Authorization.models.Admins import Admins
from Authorization.models.PermissionCategory import PermissionCategory
from Authorization.models.Permissions import Permissions
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from SayalSanjesh.Serializers import status_success_result, wrong_token_result, wrong_data_result, wrong_result
from Authorization.PasswordManager import Hashing
from General.FileUploadHandler import FileManager
from General.Serializers.UploadSerializer import UploadSerializer
from MQQTReceiver.publisher import publish_message_to_client
from General.Serializers.LogSerializers import LogSerializers
from Authorization.models.Token import Token
from django.db.models import Q


class AdminsSerializer:
    """
           This class is responsible for serializing data in our Django app
    """

    @staticmethod
    def admin_check_permission(admin_id, permission):
        """
            param : [admin_id, permission]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        admin = Admins.objects.get(admin_id=admin_id)
        if type(permission) == str:
            if permission in admin.admin_permissions:
                return True
            else:
                return False
        else:
            # counter = len(permission)
            counter_checker = 0
            for per in permission:
                if per in admin.admin_permissions:
                    counter_checker += 1
                else:
                    pass
            if counter_checker > 0:
                return True
            else:
                return False

    @staticmethod
    def admin_login_serializer(admin_phone, admin_password):
        """
            param : [admin_phone, admin_password]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        password_hashing = Hashing()
        password_hashing = password_hashing.get_password_string(admin_password)
        try:
            admin = Admins.objects.get(admin_phone=admin_phone, admin_password=password_hashing)
            admin_id = str(admin.admin_id)
            permissions = admin.admin_permissions
            admin_sms_code_start_time = admin.admin_sms_code_start_time
            token = user_id_to_token(admin_id, True, token_level="Admin")
            if admin_sms_code_start_time is not None:
                admin_sms_code_start_time = int(admin_sms_code_start_time.timestamp())
            result = {
                "permissions": permissions,
                "admin_sms_code_start_time": admin_sms_code_start_time,
                "token": token
            }
            return True, result
        except:
            return False, None

    @staticmethod
    def admin_set_profile_serializer(token, admin_name, admin_lastname, other_information, filepath, admin_password):
        """
           param : [token, admin_name, admin_lastname, other_information, filepath, admin_password]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """

        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            admin = Admins.objects.get(admin_id=admin_id)
            admin_phone_number = admin.admin_phone
            admin.admin_name = admin_name
            admin.admin_lastname = admin_lastname
            admin.other_information = other_information
            if admin_password != None:
                admin.admin_password = admin_password
            admin.save()
            if filepath != "":
                uploader_class = UploadSerializer()
                file_result = uploader_class.upload(file=filepath)[1]
                # folder_name = str(admin.admin_phone)
                # file_manager = FileManager()
                # file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                #                                                owner_name='Admin')
                # Count the number of occurrences of the word in the URL
                count = len(re.findall('/media', file_result['fileurl']))

                # If the word appears more than once, delete the first occurrence
                if count > 1:
                    file_result['fileurl'] = re.sub('/media', '', file_result['fileurl'], count=1)
                admin.admin_images = [file_result.get('fileurl')]
                print(file_result.get('fileurl'))
                admin.save()
                middle_admin_publish_data = {
                    'admin_phone_number': admin_phone_number,
                    'from_where': 'edit_user'
                }
                publish_message_to_client(publish_func='middle_admin', data=middle_admin_publish_data)
            return True, status_success_result
            
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_profile_serializer(token):
        """
           param : [token]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            # if AdminsSerializer.admin_check_permission(admin_id, 'Admin'):
            queryset = Admins.objects.get(admin_id=admin_id)
            response = Admins.objects.serialize(queryset=queryset)
            return True, response
            # else:
            #     return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_other_admin(token, other_admin_id):
        """
           param : [token]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                try:
                    queryset = Admins.objects.get(admin_id=admin_id)
                    response = Admins.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است admin_id"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_change_password_serializer(token, new_password, admin_old_password):
        """
           param : [token, new_password]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            admin = Admins.objects.get(admin_id=admin_id)
            if admin.admin_password == admin_old_password:
                admin.admin_password = new_password
                admin.save()
            else:
                wrong_data_result["farsi_message"] = "پسورد اشتباه است"
                wrong_data_result["english_message"] = "Wrong password"
                return False, wrong_data_result
            return True, status_success_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_create_new_admin_serializer(
            token, admin_name, admin_phone, admin_lastname, admin_password, admin_permissions, other_information,
            filepath):
        """
           param : [token, admin_name, admin_phone, admin_lastname, admin_password, admin_permissions, other_information,
                    filepath]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['CRUDAdmin', 'CRUDManager']):
                admin_permissions.append("Self")
                admin_obj = Admins.objects.get(admin_id=admin_id)
                if len(admin_phone) > 11 or len(admin_phone) < 11:
                    wrong_data_result["farsi_message"] = "لطفا یازده رقم وارد کنید "
                    wrong_data_result["english_message"] = "Please enter eleven digits"
                    return False, wrong_data_result
                if len(admin_phone) == 11:
                    # x = bool(re.search("09(0[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}", admin_phone))
                    # if x:
                    password_hashing = Hashing()
                    password_hashing = password_hashing.get_password_string(admin_password)
                    try:
                        admin = Admins()
                        admin.admin_name = admin_name
                        admin.admin_phone = admin_phone
                        admin.admin_lastname = admin_lastname
                        admin.admin_password = password_hashing
                        admin.admin_permissions = admin_permissions
                        admin.other_information = other_information
                        
                        if 'ProjectManager' in admin_permissions:
                            admin.admin_creator_id = str(admin_obj.admin_id)
                        admin.save()
                        admin_object = Admins.objects.get(admin_id=admin_id)
                        LogSerializers().system_log_create_serializer(
                            token=token, system_log_admin=admin_object, system_log_action='Add', system_log_user=None,
                            system_log_field_changes=None, system_log_message=None,
                            system_log_object_action_on=admin_name, system_log_action_table='Admins')
                        if filepath != "":
                            folder_name = str(admin_phone)
                            file_manager = FileManager()
                            file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                           owner_name='Admin')
                            other_information.update({
                                'file_url': file_result['file_location']
                            })
                            admin.other_information = other_information
                            admin.save()
                        admin.save()
                    except:
                        wrong_data_result["farsi_message"] = "شماره همراه در سیستم وجود دارد . "
                        wrong_data_result[
                            "english_message"] = "phone number already exist."
                        return False, wrong_data_result
                    return True, status_success_result
                wrong_data_result["farsi_message"] = "شماره موبایل صحیح نیست "
                wrong_data_result["english_message"] = "phone number not valid."
                return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def get_all_admins_serializer(token, admin_name, admin_lastname, admin_phone):
        """
           param : [token, admin_name, admin_lastname, admin_phone]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['CRUDManager', 'CRUDAdmin', 'ViewAdmin']):
                filters = {
                    "admin_name__contains": admin_name,
                    "admin_lastname__contains": admin_lastname,
                    "admin_phone__contains": admin_phone
                }
                filters = {k: v for k, v in filters.items() if v is not None or v != ""}
                if AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager']):
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    queryset = Admins.objects.filter(Q(admin_id=admin_id) | Q(admin_creator_id=str(admin_id))).exclude(
                        admin_phone=admin_obj.admin_phone).order_by(
                        'admin_create_date')
                    response = Admins.objects.serialize(queryset=queryset)
                    return True, response
                else:
                    queryset = Admins.objects.filter(**filters).order_by('admin_create_date')
                    response = Admins.objects.serialize(queryset=queryset)
                    return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_others_serializer(
            token, other_admin_id, admin_name, admin_lastname, admin_permissions, other_information, filepath):
        """
           param : [token, other_admin_id, admin_name, admin_lastname, admin_permissions, other_information,
                    filepath]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['CRUDAdmin', 'CRUDManager']):
                admin = Admins.objects.get(admin_id=other_admin_id)
                first_device_state_dict = {
                    "admin_name": admin.admin_name,
                    "admin_lastname": admin.admin_lastname,
                    "admin_permissions": admin.admin_permissions,
                    "other_information": admin.other_information,
                }
                admin_phone = admin.admin_phone
                if filepath != "":
                    folder_name = str(admin_phone)
                    file_manager = FileManager()
                    file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                   owner_name='Admin')
                    other_information.update({
                        'file_url': file_result['file_location']
                    })
                admin.admin_name = admin_name
                admin.admin_lastname = admin_lastname
                admin.admin_permissions = admin_permissions
                admin.other_information = other_information
                admin.save()
                second_device_state = Admins.objects.get(admin_id=other_admin_id)
                second_device_state_dict = {"admin_name": second_device_state.admin_name,
                                            "admin_lastname": second_device_state.admin_lastname,
                                            "admin_permissions": second_device_state.admin_permissions,
                                            "other_information": second_device_state.other_information
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
                                                              system_log_object_action_on=other_admin_id,
                                                              system_log_action='Edit',
                                                              system_log_action_table='Admins',
                                                              system_log_message=system_log_message,
                                                              system_log_field_changes=changed_fields)
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_remove_other_serializer(token, other_admin_id):
        """
           param : token, other_admin_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            # TODO: But It Should Be Priortize (Joker removes Admin&ProjectManager - Project Manager removes low level Project Manager)
            if AdminsSerializer.admin_check_permission(admin_id, ['CRUDAdmin', 'CRUDManager']):
                try:
                    admin = Admins.objects.get(admin_id=other_admin_id)

                except:
                    wrong_data_result["farsi_message"] = "اشتباه است admin_id"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                admin_phone = str(admin.admin_phone)
                try:
                    base_dir = os.getcwd()
                    media_path = os.path.join(base_dir, 'media')
                    admin_path = os.path.join(media_path, 'Admin')
                    directory_path = os.path.join(admin_path, admin_phone)
                    shutil.rmtree(directory_path)
                except:
                    pass
                admin.delete()
                admin_object = Admins.objects.get(admin_id=admin_id)
                LogSerializers().system_log_create_serializer(
                    token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                    system_log_field_changes=None, system_log_message=None,
                    system_log_object_action_on=admin_id, system_log_action_table='Admins')
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_other_admin_files_serializer(token, other_admin_id):
        """
           param : [token, other_admin_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                try:
                    other_admin_id = Admins.objects.get(admin_id=other_admin_id)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است admin_id"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                other_admin_id = other_admin_id.as_dict()
                admin_name = other_admin_id['admin_name']
                admin_lastname = other_admin_id['admin_lastname']
                admin_phone = other_admin_id['admin_phone']
                folder_name = admin_name + "_" + admin_lastname + "_" + admin_phone
                base_dir = os.getcwd()
                media_path = os.path.join(base_dir, 'media')
                admin_path = os.path.join(media_path, 'Admin')
                other_admin_path = os.path.join(admin_path, folder_name)
                files_list = os.listdir(other_admin_path)
                file_locations = {}
                for file in files_list:
                    final_file_path = os.path.join(other_admin_path, file)
                    file_locations.update({
                        f'{file}': final_file_path
                    })
                file_locations.update({
                    'all_files': len(files_list)
                })
                return True, file_locations
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_admin_files_serializer(token, other_admin_id, file_name):
        """
           param : [token, other_admin_id, file_name]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                try:
                    other_admin_id = Admins.objects.get(admin_id=other_admin_id)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است admin_id"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                other_admin_id = other_admin_id.as_dict()
                admin_name = other_admin_id['admin_name']
                admin_lastname = other_admin_id['admin_lastname']
                admin_phone = other_admin_id['admin_phone']
                folder_name = admin_name + "_" + admin_lastname + "_" + admin_phone
                base_dir = os.getcwd()
                media_path = os.path.join(base_dir, 'media')
                admin_path = os.path.join(media_path, 'Admin')
                other_admin_path = os.path.join(admin_path, folder_name)
                file_remove_path = os.path.join(other_admin_path, file_name)
                os.remove(file_remove_path)
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def send_verification_sms(phone_number, sms_code, hash_code):

        try:
            url = "https://api.sms.ir/v1/send/verify"
            payload = {
                "mobile": phone_number,
                "templateId": 658531,
                "parameters": [
                    {
                        "name": "Code",
                        "value": sms_code
                    },
                    {
                        "name": "Hash",
                        "value": hash_code
                    }
                ]
            }
            headers = {
                'X-API-KEY': 'Zkn4SxmAw69DdtXsjHbgqmsQwcj8ohhZYfmaE5iujDzC4PcdwdVjdDRUH0bVGjue',
                'Content-Type': "application/json",
                'ACCEPT': 'application/json'
            }
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            print(response.json())
        except:
            pass

    @staticmethod
    def admin_check_phone_number_validation_serializer(phone, sms_code, send_sms, password, hash_code):
        """
           param : [phone, sms_code, send_sms, password, hash_code]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """

        try:
            admin = Admins.objects.get(admin_phone=phone)
        except:
            wrong_data_result["farsi_message"] = "کاربری با این شماره در سیستم ثبت نشده است"
            wrong_data_result["english_message"] = "User with this number is not registered"
            return False, wrong_data_result
        admin_phone_number_validation = admin.admin_phone_number_validation
        current_time = datetime.datetime.utcnow()
        if sms_code == None and send_sms == None and password == None:
            if admin_phone_number_validation == 0:
                result = {
                    "admin_phone": admin.admin_phone,
                    "admin_phone_number_validation": admin_phone_number_validation,
                    "message": "The phone number is not active"
                }
                return True, result
            else:
                result = {
                    "admin_phone": admin.admin_phone,
                    "admin_phone_number_validation": admin_phone_number_validation,
                    "message": "The phone number is active"
                }
                return True, result
        elif sms_code == None and send_sms == 1:
            sms_code_api_result = str(random.randint(1000, 9999))
            AdminsSerializer.send_verification_sms(phone_number=phone, sms_code=sms_code_api_result,
                                                   hash_code=hash_code)
            admin.admin_sms_code = sms_code_api_result
            admin.admin_sms_code_start_time = current_time
            admin.save()

            def delete_sms_code():
                time_after_2_minutes = current_time + timedelta(minutes=2)
                for time_reminder in range(0, 122):
                    time.sleep(1)
                    time_checker = current_time + timedelta(seconds=time_reminder)
                    if time_checker >= time_after_2_minutes:
                        admin.admin_sms_code = None
                        admin.admin_sms_code_start_time = None
                        admin.save()

            t1 = Thread(target=delete_sms_code)
            t1.start()
            result = {
                "sms_code": sms_code_api_result
            }
            return True, result
        elif sms_code != None and send_sms == None:
            if str(sms_code) == str(admin.admin_sms_code):
                admin.admin_phone_number_validation = 1
                admin.save()
                return True, status_success_result
            else:
                wrong_data_result["farsi_message"] = "لطفا اس ام اس را صحیح وارد کنید."
                wrong_data_result["english_message"] = "Please enter the correct SMS."
                return False, wrong_data_result
        elif password != None and admin.admin_phone_number_validation == 1:
            password_hashing = Hashing()
            password_hashing = password_hashing.get_password_string(password)
            admin.admin_password = password_hashing
            admin.save()
            result = {
                "admin_phone": phone,
                "admin_password": "Password changed successfully"
            }
            return True, result
        else:
            wrong_data_result["farsi_message"] = "ابتدا شماره موبایل را فعال کنید"
            wrong_data_result["english_message"] = "Please activate phone number first"
            return False, wrong_data_result

    @staticmethod
    def admin_set_category_permission_serializer(token, admin_id, permission_category_id):
        """
           param : [token, other_admin_id, file_name]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_self_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_self_id, 'SetPermission'):
                try:
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    permission_category_obj = PermissionCategory.objects.get(
                        permission_category_id=permission_category_id)
                    first_device_state_dict = {
                        "admin_permissions": admin_obj.admin_permissions,
                    }
                except:
                    wrong_data_result["farsi_message"] = "داده نامعتبر"
                    wrong_data_result["english_message"] = "Invalid data"
                    return False, wrong_data_result
                permission_list = list(map(lambda x: x['permission_english_name'],
                                           list(permission_category_obj.permissions.values('permission_english_name'))))
                admin_permissions = admin_obj.admin_permissions
                for element in permission_list:
                    if element not in admin_permissions:
                        admin_permissions.append(element)
                admin_obj.save()
                second_device_state = Admins.objects.get(admin_id=admin_id)
                second_device_state_dict = {"admin_permissions": second_device_state.admin_permissions, }

                changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                  first_device_state_dict if
                                  first_device_state_dict[key] != second_device_state_dict[key]}
                system_log_message = ''
                for key, values in changed_fields.items():
                    system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                admin_obj = Admins.objects.get(admin_id=admin_id)
                LogSerializers().system_log_create_serializer(token=token, system_log_admin=admin_obj,
                                                              system_log_user=None,
                                                              system_log_object_action_on=admin_id,
                                                              system_log_action='Edit',
                                                              system_log_action_table='Admins',
                                                              system_log_message=system_log_message,
                                                              system_log_field_changes=changed_fields)
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_set_permission_serializer(token, admin_id, permission_english_name_list):
        """
           param : [token, admin_id, permission_english_name_list]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_self_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_self_id, 'SetPermission'):
                try:
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    first_device_state_dict = {
                        "admin_permissions": admin_obj.admin_permissions,
                    }
                    admin_obj_permissions = admin_obj.admin_permissions
                    permission_english_names = list(
                        map(lambda x: x[0], Permissions.objects.values_list('permission_english_name')))
                    result = all(item in permission_english_names for item in permission_english_name_list)
                    if result:
                        for permission in permission_english_name_list:
                            admin_obj_permissions.append(permission)
                        admin_obj.save()
                        second_device_state = Admins.objects.get(admin_id=admin_id)
                        second_device_state_dict = {"admin_permissions": second_device_state.admin_permissions, }

                        changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                          first_device_state_dict if
                                          first_device_state_dict[key] != second_device_state_dict[key]}
                        system_log_message = ''
                        for key, values in changed_fields.items():
                            system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                        admin_obj = Admins.objects.get(admin_id=admin_id)
                        LogSerializers().system_log_create_serializer(token=token, system_log_admin=admin_obj,
                                                                      system_log_user=None,
                                                                      system_log_object_action_on=admin_id,
                                                                      system_log_action='Edit',
                                                                      system_log_action_table='Admins',
                                                                      system_log_message=system_log_message,
                                                                      system_log_field_changes=changed_fields)
                    else:
                        wrong_data_result["farsi_message"] = "داده نامعتبر"
                        wrong_data_result["english_message"] = "Invalid data"
                        return False, wrong_data_result
                except:
                    wrong_data_result["farsi_message"] = "داده نامعتبر"
                    wrong_data_result["english_message"] = "Invalid data"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_logout_serializer(token):
        """
           param : [token]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_self_id = token_result["data"]["user_id"]
            # if AdminsSerializer.admin_check_permission(admin_self_id, 'Admin'):
            try:
                token_object = Token.objects.get(token=token)
                token_object.delete()

            except Token.DoesNotExist:
                wrong_data_result["farsi_message"] = "داده نامعتبر"
                wrong_data_result["english_message"] = "Invalid data"
                return False, wrong_data_result
            return True, status_success_result
            # else:
            #     return False, wrong_token_result
        else:
            return False, wrong_token_result
