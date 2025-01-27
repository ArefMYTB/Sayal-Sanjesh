import json
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
from SayalSanjesh.models import WaterMetersConsumptions, WaterMeters
from Authorization.models import StaticToken
from SayalSanjesh.Serializers.WaterMeterSerializer import WaterMeterSerializer
from publisher import meters_publisher

# ------------------------------------------------get meters serial-----------------------------------------------------
# meter_object = WaterMeters.objects.all().values('water_meter_serial')
# meter_object = list(map(lambda x: x['water_meter_serial'], meter_object))
# meter_topics = list(map(lambda x: (f'/meters/{x}', 0), meter_object))
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------get static token from database---------------------------------------------
static_token = StaticToken.objects.all()[0].token


# ----------------------------------------------------------------------------------------------------------------------

# ------------------------------------ get data from node and save it to database --------------------------------------
def save_data(dict_value):
    """
    dict_value = {
        'meter_serial': "",
        'meter_hourly_data': {
            # time : value
            '2023-01-01 13:05:40':'$4578',
        },
        'meter_daily_time': if you send data only daily without hourly value : null  elif : '2023-01-01 23:45:11'
        'meter_daily_data': $4575,
        'meter_cumulative_value': 4567.0,
        'meter_sd_card_status': '',
        'meter_battery_voltage': '',
    }
    """
    meter_serial = dict_value.get('MS', None)  # meter_serial
    meter_cumulative_value = dict_value.get('MCV', None)  # meter_cumulative_value
    meter_daily_data = dict_value.get('MDD', None)  # meter_daily_data
    if meter_daily_data is not None:
        if type(meter_daily_data) == str:
            meter_daily_data = int(meter_daily_data.split('$')[1])
        else:
            meter_daily_data = dict_value.get('MDD')
    meter_daily_time = dict_value.get('MDT', None)  # meter_daily_time
    information = {
        'meter_sd_card_status': dict_value.get('MSCS', None),  # meter_sd_card_status
        'meter_battery_voltage': dict_value.get('MBV', None),  # meter_battery_voltage
        'signal_power': dict_value.get('SP', None),  # signal_power
        'last_error_code': dict_value.get('LEC', None)  # last_error_code
    }
    # add to database
    # try:
    print("code in try")
    # if dict_value.get('meter_hourly_data') is not None:
    water_meter_object = WaterMeters.objects.get(water_meter_serial=meter_serial)
    if dict_value.get('meter_hourly_data') is not None:
        if len(dict_value.get('meter_hourly_data')) != 0:

            for time, value in dict_value.get('meter_hourly_data').items():
                value = int(value.split('$')[1])
                res = WaterMetersConsumptions.objects.create(water_meters=water_meter_object, value=value,
                                                             create_time=time,
                                                             cumulative_value=meter_cumulative_value,
                                                             information=information)
                print(f"res : {res}")
                res = str(res).split(',')
                if int(res[0]) == 0:
                    message = res[1]
                    meters_publisher(topic_name=f'/Meters/{meter_serial}', message=message)


    else:
        if meter_daily_time is not None:
            res = WaterMetersConsumptions.objects.create(water_meters=water_meter_object,
                                                         value=meter_daily_data,
                                                         create_time=meter_daily_time,
                                                         cumulative_value=meter_cumulative_value,
                                                         information=information)
            res = str(res).split(',')
            print(f"res : {res}")
            if int(res[0]) == 0:
                message = res[1]
                meters_publisher(topic_name=f'/Meters/{meter_serial}', message=message)

        else:
            print("in else block")
            res = WaterMetersConsumptions.objects.create(water_meters=water_meter_object,
                                                         value=meter_daily_data,
                                                         cumulative_value=meter_cumulative_value,
                                                         information=information)
            res = str(res).split(',')
            print(f"res : {res}")
            if int(res[0]) == 0:
                message = res[1]
                meters_publisher(topic_name=f'/Meters/{meter_serial}', message=message)
    # except:
    #     print("something is wrong")


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
    #  write to csv or add to database ?
    # try:
    dict_value = json.loads(message.payload.decode("utf-8"))
    save_data(dict_value=dict_value)
    # except:
    #     pass


broker = '217.144.106.32'
port = 1883
topic = "/Meters/data"

client_id = f'python-mqtt-{random.randint(0, 1000)}'

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
