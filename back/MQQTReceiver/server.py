import random
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

# ------------------------------------------------get meters serial-----------------------------------------------------
meter_object = WaterMeters.objects.all().values('water_meter_serial')
meter_object = list(map(lambda x: x['water_meter_serial'], meter_object))
meter_topics = list(map(lambda x: (f'/meters/{x}', 0), meter_object))
# ----------------------------------------------------------------------------------------------------------------------

Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    print(f"{message.topic}")
    print("Message received: " + message.payload.decode("utf-8"))


broker = '217.144.106.32'
port = 1883
topic = "/Meters/4575"
# topic = meter_topics

client_id = f'python-mqtt-{random.randint(0, 1000)}'
# user = "test"
# password = "sayal@mqtt"

user = "meters"
password = "S@yal1402"

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

client.subscribe(topic)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
