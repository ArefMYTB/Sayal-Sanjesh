import os
import shutil
import random
import string
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.models.Apps import App
from General.FileUploadHandler import FileManager
from Authorization.TokenManager import token_to_user_id
from Authorization.Serializers.StaticTokenSerializer import StaticTokenSerializer
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result


class AppSerializers:
    """
        This class is responsible for serializing data in our Django app
    """

    @staticmethod
    def get_app_serializer(token):
        """
            param : [token]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        print(token_result)
        if token_result is None:
            try:
                app_obj = App.objects.order_by('app_create_date').last()
                result = {
                    "app_version_code": app_obj.app_version_code,
                    "app_version_name": app_obj.app_version_name,
                    "app_url": app_obj.app_url
                }
                return True, result
            except:
                wrong_data_result["farsi_message"] = "هیچ فایلی برای دانلود وجود ندارد"
                wrong_data_result["english_message"] = "There are no files to download"
                wrong_data_result["code"] = 404
                return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_app_serializer(token):
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
                    app_obj = App.objects.order_by('app_create_date').last()
                    result = {
                        "app_version_code": app_obj.app_version_code,
                        "app_version_name": app_obj.app_version_name,
                        "app_url": app_obj.app_url
                    }
                    return True, result
                except:
                    wrong_data_result["farsi_message"] = "هیچ فایلی برای دانلود وجود ندارد"
                    wrong_data_result["english_message"] = "There are no files to download"
                    wrong_data_result["code"] = 404
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_app_serializer(token, app_version_code):
        """
            param : [token, app_version_code]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'User'):
                # get all app versions
                all_apps = App.objects.all()
                all_app_versions = list(map(lambda itm: itm['app_version_code'], all_apps.values('app_version_code')))
                if app_version_code in all_app_versions:
                    base_root = os.getcwd()
                    app_root = os.path.join(base_root, 'media', 'App')
                    if os.path.exists(os.path.join(app_root, str(app_version_code))):
                        version_root = os.path.join(app_root, str(app_version_code))
                        shutil.rmtree(version_root)
                        App.objects.get(app_version_code=app_version_code).delete()
                    else:
                        App.objects.get(app_version_code=app_version_code).delete()
                else:
                    wrong_data_result["farsi_message"] = "ورژن اشتباه وارد شده است"
                    wrong_data_result["english_message"] = "The wrong version has been entered."
                    wrong_data_result["code"] = 404
                    return False, wrong_data_result
                return True, status_success_result
            else:
                wrong_token_result['code'] = 403
                return False, wrong_token_result
        else:
            wrong_token_result['code'] = 403
            return False, wrong_token_result

    @staticmethod
    def admin_add_app_serializer(token, filepath, app_version_code, app_version_name):
        """
            param : [token, filepath, app_version_code, app_version_name]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'User'):
                if filepath != "":
                    # Check for duplicate version
                    app_count = App.objects.filter(app_version_code=app_version_code).count()
                    if app_count != 0:
                        wrong_data_result["farsi_message"] = "ورژن تکراری"
                        wrong_data_result["english_message"] = "Duplicate version"
                        wrong_data_result["code"] = 409
                        return False, wrong_data_result
                    folder_name = str(app_version_code)
                    file_manager = FileManager()
                    file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                   owner_name='App')
                    S = 50  # number of characters in the string.
                    # call random.choices() string module to find the string in Uppercase + numeric data.
                    ran_character = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
                    download_url = f"{file_result['fileurl']}/{ran_character}"
                    url_list = list(reversed(download_url.split('/')))
                    app_obj = App()
                    app_obj.app_path = file_result['file_location']
                    app_obj.app_version_code = app_version_code
                    app_obj.app_version_name = app_version_name
                    app_obj.app_url = url_list
                    app_obj.save()
                return True, status_success_result
            else:
                wrong_token_result['code'] = 403
                return False, wrong_token_result
        else:
            wrong_token_result['code'] = 403
            return False, wrong_token_result

    @staticmethod
    def user_get_app_serializer(token):
        """
            param : [token]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            # get obj from db
            try:
                app_obj = App.objects.order_by('app_create_date').last()
                result = {
                    "app_version_code": app_obj.app_version_code,
                    "app_version_name": app_obj.app_version_name,
                    "app_url": app_obj.app_url
                }
                return True, result
            except:
                wrong_data_result["farsi_message"] = "هیچ فایلی برای دانلود وجود ندارد"
                wrong_data_result["english_message"] = "There are no files to download"
                wrong_data_result["code"] = 404
                return False, wrong_data_result
        else:
            wrong_token_result['code'] = 403
            return False, wrong_token_result
