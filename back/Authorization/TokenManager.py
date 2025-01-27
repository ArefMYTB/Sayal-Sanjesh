import jwt
from datetime import datetime, timedelta
from Authorization.models.Token import Token


def user_id_to_token(user_id, activation, token_level="User"):
    try:
        token_object = Token.objects.get(owner_id=user_id)
        return token_object.token
    except Token.DoesNotExist:
        JWT_SECRET = "This is my secret key in this project."
        JWT_ALGORITHM = "HS256"
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        token_version = 1.0
        JWT_EXP_DELTA_SECONDS = 30
        JWT_EXP_DELTA_MINUTES = 1
        JWT_EXP_DELTA_hours = 24
        JWT_EXP_DELTA_days = 1
        payload = {
            'activation': activation,
            'user_id': user_id,
            'identifier': now_datetime,
            'token_version': token_version,
            'token_creator': "System",
            'token_level': token_level,
            'token_owner': "Rojcast",
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXP_DELTA_hours)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        token = jwt_token
        Token.objects.create(owner_id=user_id, token=token)
        return token


def token_to_user_id(token):
    JWT_SECRET = "This is my secret key in this project."
    JWT_ALGORITHM = "HS256"
    try:
        if Token.objects.get(token=token):
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception as e:
                try:
                    token_obj = Token.objects.get(token=token)
                    token_obj.delete()
                except:
                    pass
                return result_sender(401, "توکن نامعتبر است.", "wrong token.")
            return result_sender(0, data=payload)
    except Token.DoesNotExist:
        return result_sender(401, "توکن نامعتبر است.", "wrong token.")


def result_sender(code, farsi_message="", english_message="", data=None):
    if code == 0:
        status = "OK"
    else:
        status = "failure"
    result = {
        "status": status,
        "code": code,
        "farsi_message": farsi_message,
        "english_message": english_message,
        "data": data
    }
    return result
