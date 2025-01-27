from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.ModuleTypeSerializer import ModuleTypesSerializer


class ModuleTypesView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """

    @csrf_exempt
    def admin_add_module_type_view(self, request):
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
        fields = ["module_type_name", "module_other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        module_type_name = input_data['module_type_name']
        module_other_information = input_data['module_other_information']
        result, data = ModuleTypesSerializer.admin_add_module_type_serializer(
            token=token, module_type_name=module_type_name,
            module_other_information=module_other_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_module_type_view(self, request):
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
        fields = ["module_type_id", "module_type_name", "module_other_information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        module_type_id = input_data['module_type_id']
        module_type_name = input_data['module_type_name']
        module_other_information = input_data['module_other_information']
        result, data = ModuleTypesSerializer.admin_edit_module_type_serializer(
            token=token, module_type_id=module_type_id, module_type_name=module_type_name,
            module_other_information=module_other_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_module_type_view(self, request):
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
        if 'module_type_id' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_type_id",
                                  english_message="water_meter_type_id is Null.")
        module_type_id = input_data['module_type_id']
        result, data = ModuleTypesSerializer.admin_delete_module_type_serializer(
            token=token, module_type_id=module_type_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_module_type_view(self, request):
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
        fields = ["module_type_name", "page", "count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        module_type_name = input_data['module_type_name']
        page = input_data['page']
        count = input_data['count']
        result, data = ModuleTypesSerializer.admin_get_all_module_type_serializer(
            token=token, module_type_name=module_type_name, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_module_type_view(self, request):
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
        if 'module_type_id' in input_data:
            module_type_id = input_data['module_type_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است water_meter_type_id",
                                  english_message="water_meter_type_id is Null.")
        result, data = ModuleTypesSerializer.admin_get_one_module_type_serializer(
            token=token, module_type_id=module_type_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

