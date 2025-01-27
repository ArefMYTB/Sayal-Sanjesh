from itertools import count
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.NoticeCategoriesSerializer import NoticeCategoriesSerializer
from SayalSanjesh.models import NoticeCategories


class NoticeCategoriesView():

    @csrf_exempt
    def admin_add_notice_category(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["category_name", "category_index"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        category_name = input_data['category_name']
        category_index = input_data['category_index']
        result, data = NoticeCategoriesSerializer.add_notice_category(
            token=token, category_name=category_name, category_index=category_index)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_notice_category(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["category_name", "category_index", "category_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        category_name = input_data['category_name']
        category_index = input_data['category_index']
        category_id = input_data['category_id']
        result, data = NoticeCategoriesSerializer.edit_notice_category(
            token=token, category_id=category_id, category_name=category_name, category_index=category_index)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_notice_category(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'category_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است category_id",
                                  english_message="category_id is Null.")
        category_id = input_data['category_id']
        result, data = NoticeCategoriesSerializer.delete_notice_category(
            token=token, category_id=category_id)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_notice_categories(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["category_name", "category_index", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        category_name = input_data['category_name']
        category_index = input_data['category_index']
        page = input_data['page']
        count = input_data['count']
        result, data = NoticeCategoriesSerializer.user_get_all_notice_categories(
            token=token, category_name=category_name, category_index=category_index, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_notice_category_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'category_id' in input_data:
            category_id = input_data['category_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است category_id",
                                  english_message="category_id is Null.")
        result, data = NoticeCategoriesSerializer.user_get_one_notice_category(
            token=token, category_id=category_id)
        if result:
            result = {
                "category": data
            }
            return result_creator(result)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_notice_categories(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["category_name", "category_index", "create_date", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        category_name = input_data['category_name']
        category_index = input_data['category_index']
        create_date = input_data['create_date']
        page = input_data['page']
        count = input_data['count']
        result, data = NoticeCategoriesSerializer.admin_get_all_notice_categoties(
            token=token, category_name=category_name, category_index=category_index,
            create_date=create_date, page=page, count=count)
        if result:
            return result_creator(data=data)

        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
