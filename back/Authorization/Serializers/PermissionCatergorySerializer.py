from Authorization.TokenManager import user_id_to_token, token_to_user_id
from SayalSanjesh.Serializers import status_success_result, wrong_token_result, wrong_data_result, wrong_result
from Authorization.models.PermissionCategory import PermissionCategory
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class PermissionCategorySerializers:
    @staticmethod
    def admin_create_permission_category_serializer(token, permission_category_persian_name,
                                                    permission_category_english_name,
                                                    permission_category_description, permissions):
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
            if AdminsSerializer.admin_check_permission(admin_id, 'Permission'):
                try:
                    admin = Admins.objects.get(admin_id=admin_id)
                except:
                    wrong_data_result["farsi_message"] = "admin_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                fields = {
                    "permission_category_english_name": (permission_category_english_name, str),
                }
                result = wrong_result(fields)
                if result == None:
                    # try:
                    category = PermissionCategory.objects.create(admin=admin,
                                                                 permission_category_persian_name=permission_category_persian_name,
                                                                 permission_category_english_name=permission_category_english_name,
                                                                 permission_category_description=permission_category_description)
                    category.permissions.set(permissions)
                    # except:
                    #     wrong_data_result["farsi_message"] = "دسترسی انتخاب شده موجود است"
                    #     wrong_data_result["english_message"] = "permission name already exist"
                    #     return False, wrong_data_result
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_edit_permission_category_serializer(token, permission_category_id, permission_category_english_name,
                                                  permission_category_persian_name,
                                                  permission_category_description, permissions):
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
            if AdminsSerializer.admin_check_permission(admin_id, 'Permission'):
                try:
                    admin = Admins.objects.get(admin_id=admin_id)
                except:
                    wrong_data_result["farsi_message"] = "admin_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong admin_id"
                    return False, wrong_data_result
                try:
                    filters = {
                        "admin": admin,
                        "permission_category_english_name": permission_category_english_name,
                        "permission_category_persian_name": permission_category_persian_name,
                        "permission_category_description": permission_category_description,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    PermissionCategory.objects.filter(permission_category_id=permission_category_id).update(**filters)
                    if permissions is not None:
                        permission_category = PermissionCategory.objects.get(
                            permission_category_id=permission_category_id)
                        permission_category.permissions.set(permissions)
                except:
                    wrong_data_result["farsi_message"] = "داده نامعتبر"
                    wrong_data_result["english_message"] = "Invalid data"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_delete_permission_serializer(token, permission_category_id):
        """
           param : [token, permission_id]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'PermissionCategory'):
                try:
                    permission_category = PermissionCategory.objects.get(permission_category_id=permission_category_id)
                    permission_category.delete()
                except:
                    wrong_data_result["farsi_message"] = "permission_category_id اشتباه است"
                    wrong_data_result["english_message"] = "invalid permission_category_id"
                    return False, wrong_data_result

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_permission_category_serializer(token, page, count, permission_category_english_name):
        """
           param : [token, page, count, permission_english_name]

           return :
           A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
           results.  it returns a false status along with an error message.
       """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'PermissionCategory'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    queryset = PermissionCategory.objects.filter(
                        permission_category_english_name__icontains=permission_category_english_name).order_by(
                        '-permission_category_create_date')[offset:offset + limit]
                    response = PermissionCategory.objects.serialize(queryset=queryset)
                    return True, response
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
