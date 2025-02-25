import datetime
import random
import json
import time
import os
import sys
import django
import paho.mqtt.client as mqttClient
from pathlib import Path

# ------------------------------------define django setting to access project model-------------------------------------
base_dir = os.getcwd()
project_path = Path(base_dir).parent
sys.path.append(f"{project_path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomationSayalSanjesh.settings")
django.setup()
# ----------------------------------------------------------------------------------------------------------------------
from SayalSanjesh.models import WaterMeters
from MQQTReceiver.Handler import Handler

# ------------------------------------------------get meters serial-----------------------------------------------------
meter_object = WaterMeters.objects.all().values('water_meter_serial')
meter_object = list(map(lambda x: x['water_meter_serial'], meter_object))
meter_topics = list(map(lambda x: (f'/meters/{x}', 0), meter_object))
# ----------------------------------------------------------------------------------------------------------------------
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


print("path : ", os.getcwd())


def write_to_file(text):
    # Get the directory from the file path
    current_time = datetime.datetime.now()
    base_dir = os.getcwd()

    # Check if the directory exists, if not, create it
    if not os.path.exists(os.path.join(base_dir, "Log")):
        os.makedirs(os.path.join(base_dir, "Log"))
    log_dir = os.path.join(base_dir, "Log")
    pure_log = os.path.join(log_dir, "pure_log.txt")
    # Open the file in append mode, which creates the file if it doesn't exist
    with open(pure_log, 'a') as file:
        # Write the text followed by a newline character
        message = f"{current_time}  , {str(text)} \n"
        file.write(message)
    
    test_log = os.path.join(log_dir, "test_log.txt")
    with open(test_log, 'a') as file:
        file.write("Aref Edit")


def on_message(client, userdata, message):
    try:
        print("message : ", message.payload)
        write_to_file(text=message.payload)

        # Attempt to decode the message
        try:
            decoded_message = message.payload.decode("utf-8", errors="replace")  # or "ignore"
        except UnicodeDecodeError:
            decoded_message = None
            print("Failed to decode message in UTF-8. Skipping this message.")

        # Proceed only if decoding was successful
        if decoded_message:
            print("Message received: " + decoded_message)
            handler_object.get_message(message=decoded_message, topic=message.topic)
        else:
            print("Message could not be processed due to decoding issues.")

    except Exception as e:
        # General exception handling to ensure no crashes
        print("An unexpected error occurred while handling the message:", e)



broker = '217.144.106.32'
port = 1883
# topic = "/Meters/Data"
# topic = meter_topics

client_id = f'python-mqtt-{random.randint(0, 1000)}'
# user = "test"
# password = "sayal@mqtt"

user = "meters"
password = "S@yal1402"
# user = "server"
# password = "S@sV02"

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

# client.subscribe(topic)
# client.subscribe('#')

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
