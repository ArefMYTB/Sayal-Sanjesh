import datetime
import os
import shutil
import re
import time
import requests
import json
import random
import string
import pytz
from datetime import timedelta, timezone
from threading import Thread
from django.db.models import Sum
from django.db.models import Q
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from SayalSanjesh.Serializers import status_success_result, wrong_token_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMeters, WaterMetersConsumptions, WaterMetersTags
from Authorization.models.Users import Users
from Authorization.models.Admins import Admins
from Authorization.models.MiddleAdmins import MiddleAdmins
from General.models import App, Utils
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from Authorization.PasswordManager import Hashing
from General.FileUploadHandler import FileManager
from General.Serializers.UploadSerializer import UploadSerializer
from MQQTReceiver.publisher import publish_message_to_client
from General.Serializers.LogSerializers import LogSerializers


class UsersSerializer:
    @staticmethod
    def get_all_users_serializer(token, page, count, user_name, user_lastname, user_phone):
        """
           param : [token, page, count, user_phone]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
             # Admin can see all users
            if AdminsSerializer.admin_check_permission(admin_id, 'Joker'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    queryset = Users.objects.filter(user_phone__icontains=user_phone).order_by(
                        '-user_create_date')[offset:offset + limit]
                    response = Users.objects.serialize(queryset=queryset)
                    for res in response:
                        user_id = res['user_id']
                        user_meters = WaterMeters.objects.filter(water_meter_user=user_id).count()
                        res['All_water_meter_with_this_user_id'] = user_meters
                    return True, response
                else:
                    return field_result

            elif AdminsSerializer.admin_check_permission(admin_id, 'ViewUser'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    middel_admin_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                    user_id_list = WaterMeters.objects.filter(
                        water_meter_project__water_meter_project_id__in=middel_admin_projects).values_list(
                        'water_meter_user')
                    filters = {
                        "user_id__in": user_id_list,
                        "user_phone__icontains": user_phone
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    queryset = Users.objects.filter(Q(**filters) | Q(admin__admin_id=admin_id) & Q(
                        user_id__in=user_id_list)).order_by(
                        '-user_create_date')[offset:offset + limit]
                    response = Users.objects.serialize(queryset=queryset)
                    for res in response:
                        user_id = res['user_id']
                        user_meters = WaterMeters.objects.filter(water_meter_user=user_id).count()
                        res['All_water_meter_with_this_user_id'] = user_meters
                    return True, response
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_user_serializer(token, other_user_id, user_phone):
        """
           param : [token, other_user_id, user_phone]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'User'):
                try:
                    if user_phone == None:
                        queryset = Users.objects.get(user_id=other_user_id)
                    else:
                        queryset = Users.objects.get(user_phone=user_phone)
                    response = Users.objects.serialize(queryset=queryset)
                    for res in response:
                        user_id = res['user_id']
                        # count user water_meters
                        user_water_meters = WaterMeters.objects.filter(water_meter_user=user_id)
                        res['user_water_meters'] = user_water_meters.count()
                        # count user project
                        res['user_projects'] = user_water_meters.values('water_meter_project').distinct().count()
                        # count user consumptions
                        res['user_consumptions'] = WaterMetersConsumptions.objects.filter(
                            water_meters__in=user_water_meters).count()
                        res['user_tag_info'] = []
                    return True, response
                except:
                    wrong_data_result["farsi_message"] = "user_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong user_id"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_change_user_profile(token, other_user_id, user_name, user_lastname, user_phone, user_password,
                                  user_sms_code, user_profile, other_information, filepath):
        """
           param : [token, other_user_id, user_name, user_lastname, user_phone, user_password,
                                  user_sms_code, user_profile, other_information, filepath]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            password_hashing = Hashing()
            password_hashing = password_hashing.get_password_string(user_password)
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'User'):
                try:
                    user = Users.objects.get(user_id=other_user_id)
                    first_device_state_dict = {
                        "user_name": user.user_name,
                        "user_lastname": user.user_lastname,
                        "user_phone": user.user_phone,
                        "user_password": user.user_password,
                        "user_sms_code": user.user_sms_code,
                        "user_profile": user.user_profile,
                        "other_information": user.other_information,
                    }
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است،user_id"
                    wrong_data_result["english_message"] = "Wrong user_id"
                    return False, wrong_data_result
                fields = {
                    'user_name': (user_name, str),
                    "user_lastname": (user_lastname, str),
                    "user_phone": (user_phone, str),
                    "user_password": (user_password, str),
                    "user_sms_code": (user_sms_code, str),
                    "user_profile": (user_profile, dict),
                    "other_information": (other_information, dict)
                }
                result = wrong_result(fields)
                if result == None:
                    user_phone_file_path = user.user_phone
                    if filepath != "":
                        folder_name = str(user_phone_file_path)
                        file_manager = FileManager()
                        file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                       owner_name='User')
                        other_information.update(file_result)
                    user.user_name = user_name
                    user.user_lastname = user_lastname
                    user.user_phone = user_phone
                    user.user_password = password_hashing
                    user.user_sms_code = user_sms_code
                    user.user_profile = user_profile
                    user.other_information = other_information
                    user.save()
                    publish_message_to_client(phone_number=user_phone, from_where='edit_user')
                    second_device_state = Users.objects.get(user_id=other_user_id)
                    second_device_state_dict = {"user_name": second_device_state.user_name,
                                                "user_lastname": second_device_state.user_lastname,
                                                "user_phone": second_device_state.user_phone,
                                                "user_password": second_device_state.user_password,
                                                "user_sms_code": second_device_state.user_sms_code,
                                                "user_profile": second_device_state.user_profile,
                                                "other_information": second_device_state.other_information, }

                    changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                      first_device_state_dict if
                                      first_device_state_dict[key] != second_device_state_dict[key]}
                    system_log_message = ''
                    for key, values in changed_fields.items():
                        system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                    admin_obj = Admins.objects.get(admin_id=admin_id)
                    LogSerializers().system_log_create_serializer(token=token, system_log_admin=admin_obj,
                                                                  system_log_user=None,
                                                                  system_log_object_action_on=other_user_id,
                                                                  system_log_action='Edit',
                                                                  system_log_action_table='Users',
                                                                  system_log_message=system_log_message,
                                                                  system_log_field_changes=changed_fields)
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def guest_login_serializer(guest_phone, guest_password):
        """
           param : [guest_phone, guest_password]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        try:
            fields = {
                'guest_phone': (guest_phone, str),
                'guest_password': (guest_password, str)
            }
            password_hashing = Hashing()
            password_hashing = password_hashing.get_password_string(guest_password)
            guest = Users.objects.get(user_phone=guest_phone, user_password=password_hashing)
            guest_id = str(guest.user_id)
            user_pass_change = str(guest.user_password_changed)
            base_time = guest.as_dict()['user_sms_code_start_time']
            if base_time is not None:
                utc_time = base_time.replace(tzinfo=timezone.utc)
            else:
                utc_time = 0
            user_sms_code_start_time = guest.as_dict()['user_sms_code_start_time']

            if user_sms_code_start_time is not None:
                user_sms_code_start_time = int(user_sms_code_start_time.timestamp())
            else:
                user_sms_code_start_time = 0
            token = user_id_to_token(guest_id, True, token_level="User")
            now = datetime.datetime.now()
            dt = now.astimezone(pytz.UTC)
            result = {
                "token": token,
                "user_pass_change": user_pass_change,
                "user_sms_code_start_time": user_sms_code_start_time,
                "base_time": base_time,
                "utc_time": utc_time,
                "dt": dt,
                "now": now,
            }
            return True, result
        except:
            wrong_data_result["farsi_message"] = f" اشتباه است{fields}"
            wrong_data_result["english_message"] = f"{fields}Wrong "
            return False, wrong_data_result

    @staticmethod
    def admin_create_new_user_serializer(token, user_name, user_phone, user_lastname, user_password, user_sms_code,
                                         user_profile, other_information, filepath):
        """
           param : [token, user_name, user_phone, user_lastname, user_password, user_sms_code,
                                         user_profile, other_information, filepath]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'CRUDUser'):
                try:
                    admin = Admins.objects.get(admin_id=admin_id)
                except:
                    wrong_data_result["farsi_message"] = "admin_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                fields = {
                    "user_phone": (user_phone, str),
                }
                result = wrong_result(fields)
                data = {}
                if result == None:
                    if len(user_phone) > 11 or len(user_phone) < 11:
                        wrong_data_result["farsi_message"] = "لطفا یازده رقم وارد کنید "
                        wrong_data_result["english_message"] = "Please enter eleven digits"
                        return False, wrong_data_result
                    if len(user_phone) == 11:
                        x = bool(re.search("^(\\+98|0)?9\\d{9}$", user_phone))
                        if x:
                            password_hashing = Hashing()
                            password_hashing = password_hashing.get_password_string(user_password)
                            try:
                                user = Users()
                                user.admin = admin
                                user.user_name = user_name
                                user.user_lastname = user_lastname
                                user.user_phone = user_phone
                                user.user_password = password_hashing
                                user.user_sms_code = user_sms_code
                                user.user_profile = user_profile
                                user.other_information = other_information
                                user.save()
                                user_id = user.user_id
                                data = {
                                    'userID': user_id
                                }
                                if filepath != "":
                                    folder_name = str(user_phone)
                                    file_manager = FileManager()
                                    file_result = file_manager.File_upload_handler(file=filepath,
                                                                                   folder_name=folder_name,
                                                                                   owner_name='User')
                                    other_information.update({
                                        'file_result': file_result
                                    })
                                    user.other_information = other_information
                                    user.save()
                                # update user number in utils table
                                utils_object = Utils.objects.filter(name='all_record_count_in_system')
                                information = list(utils_object.values())[0].get('information')
                                information['all_users'] = information['all_users'] + 1
                                utils_object.update(information=information)
                                admin_object = Admins.objects.get(admin_id=admin_id)
                                LogSerializers().system_log_create_serializer(
                                    token=token, system_log_admin=admin_object, system_log_action='Add',
                                    system_log_user=None,
                                    system_log_field_changes=None, system_log_message=None,
                                    system_log_object_action_on=user_name,
                                    system_log_action_table='Users')
                            except:
                                wrong_data_result["farsi_message"] = "شماره همراه در سیستم وجود د ارد . "
                                wrong_data_result[
                                    "english_message"] = "phone number already exist."
                                return False, wrong_data_result
                            return True, data
                        else:
                            wrong_data_result["farsi_message"] = "شماره موبایل صحیح نیست "
                            wrong_data_result["english_message"] = "phone number not valid."
                            return False, wrong_data_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def user_get_profile_serializer(token):
        """
           param : [token]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            queryset = Users.objects.get(user_id=user_id)
            response = Users.objects.serialize(queryset=queryset)
            for res in response:
                res.pop('admin')
                res.pop('user_id')
                res.pop('all users')
                res.pop('user_sms_code')
            return True, response
        else:
            return False, wrong_token_result

    @staticmethod
    def user_edit_profile(token, user_name, user_lastname, user_profile, other_information, filepath):
        """
           param : [token, user_name, user_lastname, user_profile, other_information, filepath]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                'user_name': (user_name, str),
                "user_lastname": (user_lastname, str),
                "user_profile": (user_profile, dict),
                "other_information": (other_information, dict)
            }
            result = wrong_result(fields)
            if result == None:
                try:
                    user_object = Users.objects.get(user_id=user_id)
                    first_device_state_dict = {
                        "user_name": user_object.user_name,
                        "user_lastname": user_object.user_lastname,
                        "user_profile": user_object.user_profile,
                        "other_information": user_object.other_information,
                    }
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است،user_id"
                    wrong_data_result["english_message"] = "Wrong user_id"
                    return False, wrong_data_result
                user_object.user_name = user_name
                user_object.user_lastname = user_lastname
                user_object.user_profile = user_profile
                user_object.other_information = other_information
                user_object.save()

                if filepath != "":
                    uploader_class = UploadSerializer()
                    file_result = uploader_class.upload(file=filepath)[1]
                    print(file_result)
                    user = Users.objects.get(user_id=user_id)
                    # folder_name = str(user.user_phone)
                    # file_manager = FileManager()
                    # file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                    #                                                owner_name='User')
                    # Count the number of occurrences of the word in the URL
                    count = len(re.findall('/media', file_result['fileurl']))

                    # If the word appears more than once, delete the first occurrence
                    if count > 1:
                        file_result['fileurl'] = re.sub('/media', '', file_result['fileurl'], count=1)
                    user.user_images = [file_result.get('fileurl')]
                    user.save()
                publish_message_to_client(phone_number=user.user_phone, from_where='edit_user')
                second_device_state = Users.objects.get(user_id=user_id)
                second_device_state_dict = {
                    "user_name": second_device_state.user_name,
                    "user_lastname": second_device_state.user_lastname,
                    "user_profile": second_device_state.user_profile,
                    "other_information": second_device_state.other_information, }

                changed_fields = {key: (first_device_state_dict[key], second_device_state_dict[key]) for key in
                                  first_device_state_dict if
                                  first_device_state_dict[key] != second_device_state_dict[key]}
                system_log_message = ''
                for key, values in changed_fields.items():
                    system_log_message += f"Field '{key}' changed from '{values[0]}' to '{values[1]}'\n"
                LogSerializers().system_log_create_serializer(token=token, system_log_admin=None,
                                                              system_log_user=user_id,
                                                              system_log_object_action_on=user_name,
                                                              system_log_action='Edit',
                                                              system_log_action_table='Users',
                                                              system_log_message=system_log_message,
                                                              system_log_field_changes=changed_fields)

                return True, status_success_result

            else:
                return result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_change_password(token, user_new_password):
        """
           param : [token, user_new_password]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                'user_new_password': (user_new_password, str),
            }
            result = wrong_result(fields)
            user_first_pass = Users.objects.get(user_id=user_id)
            user_first_pass = str(user_first_pass.user_password)
            second_password = Hashing()
            second_password = second_password.get_password_string(user_new_password)
            if user_first_pass != second_password:
                if result == None:
                    user_updated = Users.objects.filter(user_id=user_id).update(user_password=second_password,
                                                                                user_password_changed=1)
                    if user_updated == 1:
                        return True, status_success_result
                    else:
                        wrong_data_result["farsi_message"] = "اشتباه است،user_id"
                        wrong_data_result["english_message"] = "Wrong user_id"
                        return False, wrong_data_result
                else:
                    return result
            else:
                wrong_data_result["farsi_message"] = "لطفا رمز جدید وارد کنید"
                wrong_data_result["english_message"] = "please enter new password"
                return False, wrong_data_result

        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_user_serializer(token, user_id):
        """
           param : [token, user_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'CRUDUser'):
                try:
                    user = Users.objects.get(user_id=user_id)
                except:
                    wrong_data_result["farsi_message"] = "user_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong user_id"
                    return False, wrong_data_result
                user_phone = user.user_phone
                try:
                    base_dir = os.getcwd()
                    media_dir = os.path.join(base_dir, 'media')
                    user_dir = os.path.join(media_dir, 'User')
                    directory_dir = os.path.join(user_dir, user_phone)
                    shutil.rmtree(directory_dir)
                except:
                    pass
                publish_message_to_client(phone_number=user_phone, from_where='delete_user')
                user.delete()
                admin_object = Admins.objects.get(admin_id=admin_id)
                LogSerializers().system_log_create_serializer(
                    token=token, system_log_admin=admin_object, system_log_action='Delete', system_log_user=None,
                    system_log_field_changes=None, system_log_message=None,
                    system_log_object_action_on=user_phone, system_log_action_table='Users')
                # update user number in utils table
                try:
                    utils_object = Utils.objects.filter(name='all_record_count_in_system')
                    information = list(utils_object.values())[0].get('information')
                    information['all_users'] = information['all_users'] - 1
                    utils_object.update(information=information)
                except:
                    pass
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_check_phone_number_validation_serializer(phone, sms_code, send_sms, password, hash_code):
        """
           param : [phone, sms_code, send_sms, password, hash_code]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        fields = {
            'user_phone': (phone, str),
        }
        result = wrong_result(fields)
        if result == None:

            try:
                user = Users.objects.get(user_phone=phone)
            except:
                wrong_data_result["farsi_message"] = "کاربری با این شماره در سیستم ثبت نشده است"
                wrong_data_result["english_message"] = "User with this number is not registered"
                return False, wrong_data_result
            user_phone_number_validation = user.user_phone_number_validation
            current_time = datetime.datetime.utcnow()
            if sms_code == None and send_sms == None and password == None:
                if user_phone_number_validation == 0:
                    result = {
                        "user_phone": user.user_phone,
                        "user_phone_number_validation": user_phone_number_validation,
                        "message": "The phone number is not active"
                    }
                    return True, result
                else:
                    result = {
                        "user_phone": user.user_phone,
                        "user_phone_number_validation": user_phone_number_validation,
                        "message": "The phone number is active"
                    }
                    return True, result
            elif sms_code == None and send_sms == 1:
                sms_code_api_result = str(random.randint(1000, 9999))
                UsersSerializer.send_verification_sms(phone_number=phone, sms_code=sms_code_api_result,
                                                      hash_code=hash_code)
                user.user_sms_code = sms_code_api_result
                user.user_sms_code_start_time = current_time
                user.save()

                def delete_sms_code():
                    time_after_2_minutes = current_time + timedelta(minutes=2)
                    for time_reminder in range(0, 122):
                        time.sleep(1)
                        time_checker = current_time + timedelta(seconds=time_reminder)
                        if time_checker >= time_after_2_minutes:
                            user.user_sms_code = None
                            user.user_sms_code_start_time = None
                            user.save()

                t1 = Thread(target=delete_sms_code)
                t1.start()
                result = {
                    "sms_code": sms_code_api_result
                }
                return True, result
            elif sms_code != None and send_sms == None:
                if sms_code == user.user_sms_code:
                    user.user_phone_number_validation = 1
                    user.save()
                    return True, status_success_result
                else:
                    wrong_data_result["farsi_message"] = "لطفا اس ام اس را صحیح وارد کنید."
                    wrong_data_result["english_message"] = "Please enter the correct SMS."
                    return False, wrong_data_result
            elif password != None and user.user_phone_number_validation == 1:
                password_hashing = Hashing()
                password_hashing = password_hashing.get_password_string(password)
                user.user_password = password_hashing
                user.save()
                result = {
                    "user_phone": phone,
                    "user_password": "Password changed successfully"
                }
                return True, result
            else:
                wrong_data_result["farsi_message"] = "ابتدا شماره موبایل را فعال کنید"
                wrong_data_result["english_message"] = "Please activate phone number first"
                return False, wrong_data_result
        else:
            return result

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
                        "name": "HASH",
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
    def user_add_app_serializer(token, filepath, app_version_code, app_name):
        """
           param : [token, filepath, app_version_code, app_name]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            if filepath != "":
                # Check for duplicate version
                app_count = App.objects.filter(app_version_code=app_version_code).count()
                if app_count != 0:
                    wrong_data_result["farsi_message"] = "ورژن تکراری"
                    wrong_data_result["english_message"] = "Duplicate version"
                    wrong_data_result["code"] = 409
                    return False, wrong_data_result
                folder_name = app_name
                file_manager = FileManager()
                file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                               owner_name='App')
                download_url = f"http://217.144.106.32:6565{file_result['fileurl']}"
                app_obj = App()
                app_obj.app_path = file_result['file_location']
                app_obj.app_version_code = app_version_code
                app_obj.app_name = app_name
                app_obj.app_url = download_url
                app_obj.save()
            return True, status_success_result
        else:
            wrong_token_result['code'] = 403
            return False, wrong_token_result
