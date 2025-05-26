import jwt
from datetime import datetime
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result
from Authorization.models import StaticToken
from Authorization.Serializers.AdminsSerializer import AdminsSerializer


class StaticTokenSerializer:
    @staticmethod
    def token_checker(token):
        try:
            a = StaticToken.objects.get(token=token)
            # print(a)
        except Exception as e:
            return 0

    @staticmethod
    def creat_static_token(token_name):
        JWT_SECRET = f"this ^ Secret % key ! for {token_name} in SayalSanjesh # Company !"
        JWT_ALGORITHM = "HS256"
        token_version = 1.0
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload = {
            'identifier': now_datetime,
            'token_version': token_version,
            'token_creator': "System",
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        token = jwt_token
        return token

    @staticmethod
    def admin_creat_static_token(token, token_name):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                static_token = StaticTokenSerializer()
                static_token = static_token.creat_static_token(token_name=token_name)
                StaticToken.objects.create(
                    token_name=token_name, token=static_token)
                result = {
                    f"static {token_name} token": static_token
                }
                # t = StaticTokenSerializer()
                # t = t.token_checker(
                #     token="ooooeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiMjAyMi0wOC0xNiAxNjo0NjozMyIsInRva2VuX3ZlcnNpb24iOjEuMCwidG9rZW5fY3JlYXRvciI6IlN5c3RlbSJ9.84yQXAfUORy7KNt8kGfd4dxyKjxEiGDlgURl3KIzfyI")
                # print(t)
                # result = {
                #     "message": "test"
                # }
                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
