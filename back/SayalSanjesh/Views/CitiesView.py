from json.decoder import JSONDecodeError
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.CitiesSerializer import citiesSerializer


class citiesView:
    """
       A view class for handling GET and POST requests.

       Methods:
       - get: Handles GET requests and returns a JSON response.
       - post: Handles POST requests and returns a JSON response.
   """
    @csrf_exempt
    def admin_create_city_view(self, request):
        if request.method.lower() == "options":
            return result_creator()

        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["city_name", "city_state"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        city_name = input_data['city_name']
        city_state = input_data['city_state']
        result, data = citiesSerializer.admin_create_city_serializer(
            token=token, city_name=city_name, city_state=city_state)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_edit_city_view(self, request):
        if request.method.lower() == "options":
            return result_creator()

        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["city_id", "city_name", "city_state"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        city_name = input_data['city_name']
        city_state = input_data['city_state']
        city_id = input_data['city_id']
        result, data = citiesSerializer.admin_edit_city_serializer(
            token=token, city_name=city_name, city_state=city_state, city_id=city_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_delete_city_view(self, request):
        if request.method.lower() == "options":
            return result_creator()

        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["city_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        city_id = input_data['city_id']
        result, data = citiesSerializer.admin_delete_city_serializer(
            token=token, city_id=city_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_cities_view(self, request):
        if request.method.lower() == "options":
            return result_creator()

        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "city_name", "city_state"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        city_name = input_data['city_name']
        city_state = input_data['city_state']
        page = input_data['page']
        count = input_data['count']
        result, data = citiesSerializer.admin_get_all_cities_serializer(
            page=page, count=count, token=token, city_name=city_name, city_state=city_state)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_one_city_view(self, request):
        if request.method.lower() == "options":
            return result_creator()

        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["city_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        city_id = input_data['city_id']
        result, data = citiesSerializer.admin_get_one_city_serializer(
            token=token, city_id=city_id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
