import json
import pytz
import random
import time
import threading
import os
import sys
import django
import paho.mqtt.client as mqttClient
from pathlib import Path
from datetime import datetime
from MQQTReceiver.publisher import ResponsePublisher

# ------------------------------------define django setting to access project model-------------------------------------
base_dir = os.getcwd()
project_path = Path(base_dir).parent
sys.path.append(f"{project_path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomationSayalSanjesh.settings")
django.setup()
# ----------------------------------------------------------------------------------------------------------------------
from Authorization.models import StaticToken
from SayalSanjesh.Serializers.ConsumptionSerializer import ConsumptionSerializer
from SayalSanjesh.Serializers.EventSerializer import EventSerializer
from SayalSanjesh.models.Events import EventType
from SayalSanjesh.models.Orders import OrderType, OrderGroups, Order
from SayalSanjesh.models.Meters import WaterMeters
from General.models.Log import MqttLoger


# ----------------------------------------------------------------------------------------------------------------------


class DataBaseConnection:
    def __init__(self):
        self.meter_related_class = ConsumptionSerializer()
        self.event_related_class = EventSerializer()
        self.publisher_class = ResponsePublisher()
        self.static_token = StaticToken.objects.all()[0].token

    def add_meter_data(self, data):
        data['token'] = self.static_token
        response = self.meter_related_class.add_consumptions_from_mqtt_broker(**data)
        print("this is response  : ", response)
        meter_serial = data.get('water_meters')
        try:
            last_counter = self.meter_related_class.get_last_consumptions_(
                token=self.static_token, water_meters=meter_serial
            )
            if last_counter[0] is not True:
                publish_message = f'serial : {meter_serial} , {None}'
            else:
                publish_message = f'serial : {meter_serial} ,  last_counter : {last_counter[1]}'
        except:
            publish_message = f'serial : {meter_serial} , {None}'

        self.publisher_class.add_data_response(topic_name=f'/meters/dataResponse/{meter_serial}',
                                               message=publish_message)

    def add_events(self, data):
        meter_serial = data.get('meter_serial')
        response = self.event_related_class.create_event_serializer(**data)
        # publish response
        try:
            event_create_time = data.get('event_create_time')
            last_counter = self.event_related_class.get_last_event_counter(self.static_token, meter_serial=meter_serial,
                                                                           event_create_time=event_create_time)
            # print("last_counter : ", last_counter)
            if last_counter[0] is True and last_counter[1]['SendResponse'] is True:
                publish_message = f'serial : {meter_serial} ,  last_counter : {last_counter[1]["event_counter"]}'
                self.publisher_class.add_event_response(topic_name=f'/meters/eventResponse/{meter_serial}',
                                                        message=publish_message)
            elif last_counter[0] is True and last_counter[1]['SendResponse'] is False:
                publish_message = f'serial : {meter_serial} ,  last_counter : {last_counter[1]["event_counter"]} ,' \
                                  f'repetitive_response : {True}'
                self.publisher_class.add_event_response(topic_name=f'/meters/eventResponse/{meter_serial}',
                                                        message=publish_message)
        except:
            print("add_events,except")
            publish_message = f'serial : {meter_serial} , {None}'
            self.publisher_class.add_event_response(topic_name=f'/meters/eventResponse/{meter_serial}',
                                                    message=publish_message)

    def command_response(self, data):
        print("command_response")
        current_time = datetime.now(pytz.utc)
        order_meter = data.get('order_meter')
        order_meter_obj = WaterMeters.objects.get(water_meter_serial=order_meter)
        order_type_obj = OrderType.objects.get(order_type_code=data.get('order_type'))
        Order.objects.filter(order_meter=order_meter_obj, order_type=order_type_obj,
                             order_counter=data.get('order_counter')).update(
            order_status=data.get('order_status'), order_status_time=current_time)
        check_orders = Order.objects.filter(order_meter=order_meter_obj, order_status=-1)
        publish_retain = {
            "DevInfo": {
                "SerialNum": order_meter
            }
        }
        if len(check_orders) > 0:
            for obj in check_orders:
                publish_retain[f"{obj.order_type.order_type_code}"] = {
                    'Counter': obj.order_counter,
                    'Status': -1
                }
        else:
            publish_retain = {}
        self.publisher_class.send_commands(topic_name=f'/meters/commands/{order_meter}',
                                           message=json.dumps(publish_retain))


class Logger:
    def __init__(self, status, message, topic=None):
        self.status = status
        self.message = message
        self.topic = topic
        self.log_dir = os.path.join(os.getcwd(), 'Log')
        if self.status == 'receive':
            self.__receive_logs()
        if self.status == 'error':
            self.__error_logs()
        if self.status == 'response':
            self.__response_logs()

    def __receive_logs(self):
        current_time = datetime.now()
        log_message = f"Message received :\n Time : {current_time}\n Topic :{self.topic}\n Content :\n {self.message}\n\n\n"
        receive_root = os.path.join(self.log_dir, 'ReceiveLogs.txt')
        with open(receive_root, 'a') as file:
            # Write text to the file
            file.write(log_message)
        # add log to data base
        MqttLoger.objects.create(topic_name=self.topic, message=self.message, state='Receive')

    def __error_logs(self):
        current_time = datetime.now()
        log_message = f"Message received :\n Time : {current_time}\n Topic :{self.topic}\n Content :\n {self.message}\n\n\n"
        receive_root = os.path.join(self.log_dir, 'ErrorLogs.txt')
        with open(receive_root, 'a') as file:
            # Write text to the file
            file.write(log_message)
        # add log to data base
        MqttLoger.objects.create(topic_name=self.topic, message=self.message, state='Error')

    def __response_logs(self):
        current_time = datetime.now()
        log_message = f"Message received :\n Time : {current_time}\n Topic :{self.topic}\n Content :\n {self.message}\n\n\n"
        receive_root = os.path.join(self.log_dir, 'ResponseLogs.txt')
        with open(receive_root, 'a') as file:
            # Write text to the file
            file.write(log_message)


class Validation(DataBaseConnection):
    def __init__(self):
        super().__init__()

    def data_validation(self, message, topic):
        # write every message t logger file
        Logger(status='receive', message=message, topic=topic)

        try:
            data = json.loads(message)
            prepared_data = {
                "water_meters": data.get('DevInfo').get('SerialNum'),
                "create_time": data.get('DevInfo').get('DateTime'),
                "counter": data.get('DevInfo').get('DataCounter'),
                "value": None,
                "cumulative_value": data.get('Volume').get('Cumulative'),
                "value_type": None,
                "flow_instantaneous": None,
                "flow_type": None,
                "flow_value": None,
                'information': {}
            }
            if 'Value' in data.get('Volume').keys():
                prepared_data['value'] = data.get('Volume').get('Value')
            if 'Type' in data.get('Volume').keys():
                prepared_data['value_type'] = data.get('Volume').get('Type')
            flow_detail = data.get('Flow', None)
            if flow_detail is not None and flow_detail != {}:
                prepared_data['flow_instantaneous'] = data.get('Flow').get('Instantaneous')
                prepared_data['flow_type'] = data.get('Flow').get('Type')
                prepared_data['flow_value'] = data.get('Flow').get('Value')
            non_required_device_info = ['SignalQuality', 'DeviceOnTime', 'RelayStatus', 'FirmwareVersion']
            for field in non_required_device_info:
                if field in data.get('DevInfo').keys():
                    prepared_data['information'][field] = data.get('DevInfo').get(field)
            voltage_detail = data.get('Voltage', None)
            if voltage_detail is not None and voltage_detail != {}:
                prepared_data['information']['voltage_detail'] = voltage_detail
            temperature_detail = data.get('Temperature', None)
            if temperature_detail is not None and temperature_detail != {}:
                prepared_data['information']['temperature_detail'] = temperature_detail
            # send prepared_data to add to database
            self.add_meter_data(data=prepared_data)
            # t = threading.Thread(target=self.add_meter_data, args=(prepared_data,))
            # t.start()
        except:
            # write every message t logger file
            Logger(status='error', message=message, topic=topic)

    def event_validation(self, message, topic):
        system_event_types = EventType.objects.values_list('event_type_code', flat=True)
        # write every message t logger file
        Logger(status='receive', message=message, topic=topic)

        try:
            data = json.loads(message)
            for key in data.keys():
                if key != 'DevInfo' and key in system_event_types:
                    prepared_data = {
                        'token': self.static_token,
                        "meter_serial": data.get('DevInfo').get('SerialNum'),
                        "event_counter": data.get('DevInfo').get('EventCounter'),
                        "event_type_code": key,
                        "event_count": data.get(key).get('Count'),
                        "event_last_occurrence": data.get(key).get('LastOccurence'),
                        'event_create_time': data.get('DevInfo').get('DateTime'),
                        "event_information": {}
                    }
                    self.add_events(prepared_data)
        except:
            print("event_validation,except")
            # write every message t logger file
            Logger(status='error', message=message, topic=topic)

    def command_validation(self, message, topic):
        # write every message t logger file
        Logger(status='receive', message=message, topic=topic)
        system_order_types = OrderType.objects.values_list('order_type_code', flat=True)
        try:
            data = json.loads(message)
            for key in data.keys():
                if key != 'DevInfo' and key in system_order_types:
                    prepared_data = {
                        "order_meter": data.get('DevInfo').get('SerialNum'),
                        "order_type": key,
                        "order_counter": data.get(key).get('Counter'),
                        "order_status": data.get(key).get('Status'),
                    }
                    # send prepared_data to add to database
                    self.command_response(data=prepared_data)
        except:
            # write every message t logger file
            Logger(status='error', message=message, topic=topic)


class Handler(Validation):
    def __init__(self):
        super().__init__()

    def get_message(self, message, topic):
        print("topic : ", topic)
        if topic == '/meters/data':
            # validate message
            t = threading.Thread(target=self.data_validation, args=(message, topic,))
            t.start()
            # self.data_validation(message, topic)
        if topic == '/meters/events':
            t = threading.Thread(target=self.event_validation, args=(message, topic,))
            t.start()
            # self.event_validation(message=message , topic=topic)
        if topic == '/meters/commandsResponse':
            t = threading.Thread(target=self.command_validation, args=(message, topic))
            t.start()
