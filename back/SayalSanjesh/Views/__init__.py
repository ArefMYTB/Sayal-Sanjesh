import json
import base64
from django.http import JsonResponse


# def hash_sha256(data):
#     if type(data) == dict:
#         data = json.dumps(data)
#     elif type(data) == list:
#         data = str(data)
#     has_str = data + ''
#     sha256_hash = hashlib.sha256()
#     sha256_hash.update(has_str.encode('utf-8'))
#     return sha256_hash.hexdigest()

def encode_base64(data):
    return data
    # if data is not None :
    #     if type(data) == dict:
    #         data = json.dumps(data)
    #     elif type(data) == list:
    #         data = str(data)
    #     has_str = data + ''
    #     byte_string = has_str.encode('utf-8')
    #     encoded_string = base64.b64encode(byte_string)
    #     return encoded_string.decode('utf-8')
    # else:
    #     return data
def result_creator(status="ok", code=200, data=None, farsi_message="با موفقیت انجام شد.",
                   english_message="successfully done."):
    result = {
        "status": status,
        "code": code,
        "data": data,
        "farsi_message": farsi_message,
        "english_message": english_message
    }
    result['data'] = encode_base64(data=result['data'])

    response = JsonResponse(result, status=result["code"], safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response
