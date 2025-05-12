import random
import time
from dotenv import load_dotenv
load_dotenv()

import os
import ssl
import paho.mqtt.client as mqttClient
from Handler import Handler

from Crypto.Cipher import AES
import base64
import json

key = bytes.fromhex(os.getenv("AES_KEY"))

def decrypt_payload(encrypted_payload_str, key):
    try:
        encrypted_payload = json.loads(encrypted_payload_str)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return None

    nonce = base64.b64decode(encrypted_payload['nonce'])
    tag = base64.b64decode(encrypted_payload['tag'])
    ciphertext = base64.b64decode(encrypted_payload['ciphertext'])
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    return json.loads(decrypted_data.decode())

handler_object = Handler()
Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
        # Subscribe to multiple topics here
        client.subscribe("/meters/data")
        client.subscribe("/meters/events")
        client.subscribe("/meters/commandsResponse")
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    try:
        # Attempt to decode the message
        try:
            decoded_message = message.payload.decode("utf-8", errors="replace")  # or "ignore"
        except UnicodeDecodeError:
            decoded_message = None
            print("Failed to decode message in UTF-8. Skipping this message.")

        # Attempt to decrypt the message
        try:
            decrypted_message = decrypt_payload(decoded_message, key)
        except UnicodeDecodeError:
            decrypted_message = None
            print("Failed to decrypt message. Skipping this message.")

        # Proceed only if decrypting was successful
        if decrypted_message:
            print("decrypted_message: ", decrypted_message)
            handler_object.get_message(message=decrypted_message, topic=message.topic)
        else:
            print("Message could not be processed due to decoding issues.")

    except Exception as e:
        # General exception handling to ensure no crashes
        print("An unexpected error occurred while handling the message:", e)



broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))

client_id = f'python-mqtt-{random.randint(0, 1000)}'

client = mqttClient.Client(client_id=client_id)
# Use TLS
client.tls_set(
    ca_certs="certs/ca.crt",
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers="ECDHE-RSA-AES256-GCM-SHA384"
)

user = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASS")

client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
