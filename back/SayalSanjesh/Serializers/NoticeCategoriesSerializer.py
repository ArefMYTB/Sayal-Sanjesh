from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import NoticeCategories
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class NoticeCategoriesSerializer:

    @staticmethod
    def add_notice_category(token, category_name, category_index):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Category'):
                admin = Admins.objects.get(admin_id=admin_id)
                category = NoticeCategories()
                fields = {
                    "category_name": (category_name, str),
                    "category_index": (category_index, int),
                }

                result = wrong_result(fields)
                if result == None:
                    category.admin = admin
                    category.category_name = category_name
                    category.category_index = category_index
                    category.save()
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def edit_notice_category(token, category_id, category_name, category_index):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Category'):
                admin = Admins.objects.get(admin_id=admin_id)
                try:
                    category = NoticeCategories.objects.get(
                        category_id=category_id)
                except:
                    wrong_data_result["farsi_message"] = "category_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong category_id"
                    return False, wrong_data_result
                fields = {
                    "category_name": (category_name, str),
                    "category_index": (category_index, int),
                }

                result = wrong_result(fields)
                if result == None:
                    category.admin = admin
                    category.category_name = category_name
                    category.category_index = category_index
                    category.save()
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def delete_notice_category(token, category_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Category'):
                try:
                    category = NoticeCategories.objects.get(
                        category_id=category_id)
                except:
                    wrong_data_result["farsi_message"] = "category_id اشتباه است"
                    wrong_data_result["english_message"] = "Wrong category_id"
                    return False, wrong_data_result
                category.delete()
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_notice_categories(token, category_name, category_index, page, count):
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
                all_categories = NoticeCategories.objects.filter(
                    category_name__contains=category_name, category_index__contains=category_index).order_by(
                    '-create_date')[offset:offset + limit]
                tableCount = (NoticeCategories.objects.count())
                user_result = []
                for category in all_categories:
                    category = category.as_dict()
                    category.pop('admin_info')
                    user_result.append(category)
                return True, user_result
            else:
                return field_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_notice_category(token, category_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                category = NoticeCategories.objects.get(category_id=category_id)
            except:
                wrong_data_result["farsi_message"] = "category_id اشتباه است"
                wrong_data_result["english_message"] = "Wrong category_id"
                return False, wrong_data_result
            result = category.as_dict()
            result.pop('admin_info')
            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_notice_categoties(token, category_name, category_index, create_date, page, count):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Category'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    all_categories = NoticeCategories.objects.filter(category_name__contains=category_name,
                                                                     category_index__contains=category_index,
                                                                     create_date__contains=create_date).order_by(
                        '-create_date')[offset:offset + limit]
                    tableCount = (NoticeCategories.objects.count())
                    results = []
                    for category in all_categories:
                        category = category.as_dict()
                        category.update({
                            "all_categories": tableCount
                        })
                        results.append(category)
                    return True, results
                else:
                    return field_result
            else:
                return False, wrong_token_result
