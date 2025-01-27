from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Authorization.Serializers.StaticTokenSerializer import StaticTokenSerializer
from SayalSanjesh.Views import result_creator


@csrf_exempt
class StaticTokenView:
    @csrf_exempt
    def add_static_token_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if 'token_name' not in input_data:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است token_name",
                                  english_message="token_name is Null.")
        token_name = input_data["token_name"]
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = StaticTokenSerializer.admin_creat_static_token(token_name=token_name, token=token)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message="توکن نامعتبر است",
                                  english_message="Token is wrong.")
