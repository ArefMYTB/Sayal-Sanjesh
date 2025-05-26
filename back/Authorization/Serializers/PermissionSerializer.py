from Authorization.TokenManager import user_id_to_token, token_to_user_id
from SayalSanjesh.Serializers import status_success_result, wrong_token_result, wrong_data_result, wrong_result
from Authorization.models.Permissions import Permissions
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class PermissionSerializers:
    @staticmethod
    def admin_create_permission_serializer(token, permission_english_name, permission_persian_name,
                                           permission_description):
        """
           param : [token, permission_english_name, permission_persian_name,
                                           permission_description]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                try:
                    admin = Admins.objects.get(admin_id=admin_id)
                except:
                    wrong_data_result["farsi_message"] = "admin_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                fields = {
                    "permission_english_name": (permission_english_name, str),
                    "permission_persian_name": (permission_persian_name, str),
                    "permission_description": (permission_description, str),
                }
                result = wrong_result(fields)
                if result == None:
                    try:
                        Permissions.objects.create(admin=admin,
                                                   permission_english_name=permission_english_name,
                                                   permission_persian_name=permission_persian_name,
                                                   permission_description=permission_description)
                    except:
                        wrong_data_result["farsi_message"] = "دسترسی انتخاب شده موجود است"
                        wrong_data_result["english_message"] = "permission name already exist"
                        return False, wrong_data_result
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_edit_permission_serializer(token, permission_id, permission_english_name, permission_persian_name,
                                         permission_description):
        """
           param : [token, permission_english_name, permission_persian_name,
                                           permission_description]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                try:
                    admin = Admins.objects.get(admin_id=admin_id)
                except:
                    wrong_data_result["farsi_message"] = "admin_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                try:
                    filters = {
                        "admin": admin,
                        "permission_english_name": permission_english_name,
                        "permission_persian_name": permission_persian_name,
                        "permission_description": permission_description,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    Permissions.objects.filter(permission_id=permission_id).update(**filters)
                except:
                    wrong_data_result["farsi_message"] = "دسترسی انتخاب شده موجود است"
                    wrong_data_result["english_message"] = "permission name already exist"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_permission_serializer(token, permission_id):
        """
           param : [token, permission_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                try:
                    permission = Permissions.objects.get(permission_id=permission_id)
                    permission.delete()
                except:
                    wrong_data_result["farsi_message"] = "permission_id اشتباه است"
                    wrong_data_result["english_message"] = "invalid permission_id"
                    return False, wrong_data_result

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_permission_serializer(token, page, count, permission_english_name):
        """
           param : [token, page, count, permission_english_name]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Settings'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    queryset = Permissions.objects.filter(
                        permission_english_name__icontains=permission_english_name).order_by(
                        'permission_english_name')[offset:offset + limit]
                    response = Permissions.objects.serialize(queryset=queryset)
                    return True, response
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
