import json
import datetime
import uuid
import base64
from django.http import JsonResponse
from AutomationSayalSanjesh import settings
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode


# Function to encrypt data

def encrypt_string2(clear_str, key):
    encrypted_str = ""
    try:
        cipher = Blowfish.new(key.encode(), Blowfish.MODE_ECB)
        encrypted_bytes = cipher.encrypt(pad(clear_str.encode(), Blowfish.block_size))
        encrypted_str = b64encode(encrypted_bytes).decode()
    except Exception as e:
        print(e)
    return encrypted_str


def blowfish_encrypt(key, plaintext):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    iv = cipher.iv
    padded_data = pad(plaintext.encode(), Blowfish.block_size)
    ciphertext = cipher.encrypt(padded_data)
    # Combine IV and ciphertext and encode as base64
    encoded_ciphertext = base64.b64encode(iv + ciphertext).decode('utf-8')
    return encoded_ciphertext


def blowfish_decrypt(key, encoded_ciphertext):
    # Decode from base64 to get the raw bytes
    ciphertext = base64.b64decode(encoded_ciphertext)
    iv = ciphertext[:Blowfish.block_size]
    actual_ciphertext = ciphertext[Blowfish.block_size:]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_padded_data = cipher.decrypt(actual_ciphertext)
    decrypted_data = unpad(decrypted_padded_data, Blowfish.block_size)
    return decrypted_data.decode('utf-8')


def custom_serializer(obj):
    if isinstance(obj, datetime) and isinstance(obj, uuid):
        return str(obj)
    raise TypeError("Type not serializable")


def result_creator(status="ok", code=200, data=None, farsi_message="با موفقیت انجام شد.",
                   english_message="successfully done."):
    key = b'f675e6d9e84f419ba71b87a1fb57dfd5'
    result = {
        "status": status,
        "code": code,
        "data": data,
        "farsi_message": farsi_message,
        "english_message": english_message
    }

    if settings.ENCODE_DATA:
        if type(result['data']) == dict:
            json_response = JsonResponse(result['data'])
            response_data = json.loads(json_response.content)
            # result['data'] = blowfish_encrypt(plaintext=f"{response_data}", key=key)
            result['data'] = blowfish_encrypt(plaintext=f"{custom_serializer(obj=result['data'])}", key=key)
            print(blowfish_decrypt(key=key, encoded_ciphertext=result['data']))

        if type(result['data']) == list:
            result['data'] = blowfish_encrypt(plaintext=f"{custom_serializer(obj = result['data'])}", key=key)
    response = JsonResponse(result, status=result["code"], safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response
