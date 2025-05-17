# define django setting to access project model .
import os
import sys
import django
from pathlib import Path

base_dir = os.getcwd()
project_path = Path(base_dir).parent
sys.path.append(f"{project_path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomationSayalSanjesh.settings")
django.setup()
# --------------------------------------------------------------------------------------------------------------------
import socket
import threading
from time import sleep
import os
import datetime
import collections
from SayalSanjesh.models import EventType, StaticToken, Order
from SayalSanjesh.Serializers.WaterMeterSerializer import WaterMeterSerializer
from SayalSanjesh.Serializers.EventSerializer import EventSerializer

# get static_token from database .
static_token = StaticToken.objects.all().values('token')[0]
token = static_token['token']
# ---------------------------------------------------------------------------------------------------------------------

# get event types from database .
event_types = EventType.objects.all().values('event_type_code', 'event_type_id')

event_types = list(map(lambda x: (str(x['event_type_id']), str(x['event_type_code'])), event_types))
valid_events_dict = {}

# ---------------------------------------------------------------------------------------------------------------------
HOST = "217.144.106.32"  # or use a specific IP address

# note : the port 43256 is used for version one tcp connection that name in linux system is : smart_tcp_server.service
# if you want use  43256 port you should shout down smart_tcp_server service .
PORT = 43256  # choose a port number above 1024


class FileManager:

    def __init__(self, file_path):
        self.file_path = file_path
        self.f = None
        self.open()

    def open(self):
        if self.f is None:
            self.f = open(self.file_path, 'a')
        elif self.f.closed:
            self.f = open(self.file_path, 'a')

    def close(self):
        try:
            self.f.close()
        except:
            return

    def prepare_datetime(self):
        dt = datetime.datetime.now()
        dt_str = '{}-{}-{}  {}:{}:{}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        return dt_str

    def write(self, message):
        dt = self.prepare_datetime()
        self.open()
        self.f.write('{} - {}\n'.format(dt, message))
        self.close()


class DataParser:
    def __init__(self, name="data parser"):
        self.name = name
        self.neccessary_events = ['E1', 'E2', 'E3', 'E4', 'E5']
        self.required_fields = ['MC']
        self.non_required_fields = ['SN', 'CV', 'CCV', 'FL', 'EVS', 'ST', 'OR', 'ORS', 'ORN', 'ORID', 'DV']
        self.valid_events = None  # set valid events if evs in data packet .

    def convert_to_dict(self, seperated_data=[]):
        results = {}
        for str_data in seperated_data:
            splited_data = str_data.split(":")
            if len(splited_data) != 2:
                return
            results[splited_data[0]] = splited_data[1]
        return results

    def check_required_fields(self, data):
        for rf in self.required_fields:
            if rf not in data.keys():
                return False
        return True

    def check_data_format(self, data):
        if len(data) < 2:  # validated data must be contain more than 2 character
            return
        data = data[1:len(data) - 1]  # remove start and end characters
        seperated_data = data.split(",")  # split data
        print(f"seperated_data : {seperated_data}")
        data = self.convert_to_dict(seperated_data=seperated_data)
        print("dict data is: {}".format(data))
        if data is None:
            return
        for field in list(data.keys()):
            if field != 'MC' and field not in self.non_required_fields:
                return
        # --------------------------------------------------------------
        rf_check = self.check_required_fields(data=data)
        if not rf_check:
            return
        # --------------------------------------------------------------
        # verify module code
        module_code = data.get('MC', None)
        if module_code is None:
            return
        if len(module_code) == 0:
            return
        # ---------------------------------------------------------------
        # verify serial number
        serial_number = data.get('SN', None)
        if serial_number is None:
            serial_number = '0'
        else:
            if len(serial_number) == 0:
                return
        # ---------------------------------------------------------------
        # verify consumption value
        consumption_value = data.get('CV', None)
        if consumption_value is not None:
            try:
                consumption_value = float(consumption_value)
                if consumption_value < 0:
                    return
            except:
                return
        # --------------------------------------------------------------
        # verify cumulative consumption value
        cumulative_consumption_value = data.get('CCV', None)
        if cumulative_consumption_value is not None:
            try:
                cumulative_consumption_value = float(cumulative_consumption_value)
                if cumulative_consumption_value < 0:
                    return
            except:
                return
        # -----------------------------------------------------------------
        # verify flow
        flow = data.get('FL', None)
        if flow is not None:
            try:
                flow = float(flow)
                if flow < 0:
                    return
            except:
                return
        # -------------------------------------------------------------------

        # verify level gauge position
        state = data.get('ST', None)
        # -------------------------------------------------------------------

        # verify device mode
        device_mode = data.get('DV', None)
        # -------------------------------------------------------------------

        # verify device orders detail
        device_order = data.get('OR', None)
        device_order_number = data.get('ORN', None)
        device_order_status = data.get('ORS', None)
        device_order_id = data.get('ORID', None)
        # -------------------------------------------------------------------

        # verify events
        events_string = data.get('EVS', None)
        events = {}
        if events_string is not None:
            for valid_item in event_types:
                valid_events_dict[valid_item[1]] = valid_item[0]
            valid_events_dict_sorted = dict(collections.OrderedDict(sorted(valid_events_dict.items())))
            self.valid_events = valid_events_dict_sorted
            # event_list = events_string[1:-1].split('.')
            event_number = ""
            event_value = ""
            get_event_number = False
            for chr in events_string:
                if chr == "E":
                    get_event_number = True
                    if len(event_number) > 0 and len(event_value) > 0:
                        try:
                            event_number = int(event_number)
                        except:
                            continue
                        key = '{:03d}'.format(event_number)
                        exist = events.get(key, None)
                        if exist is not None:
                            return
                        events[key] = event_value
                    event_value = ""
                    event_number = ""
                    continue
                if chr == "_":
                    get_event_number = False
                    continue
                if get_event_number:
                    event_number += chr
                else:
                    event_value += chr
            if len(event_number) > 0 and len(event_value) > 0:
                try:
                    event_number = int(event_number)
                except:
                    return
                key = '{:03d}'.format(event_number)
                exist = events.get(key, None)
                if exist is not None:
                    return
                events[key] = event_value

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        cr_status = None
        or_status = None
        if device_order is not None or device_order_number is not None or device_order_status \
                is not None or device_order_id is not None:
            order_detail_dict = {
                "device_order": data.get('OR'),
                "device_order_number": data.get('ORN'),
                "device_order_status": data.get('ORS'),
                "device_order_id": data.get('ORID')
            }
            or_status = self.send_order_to_device(module_code=module_code, serial_number=serial_number,
                                                  **order_detail_dict)

        if consumption_value is not None:
            validated_data = {
                'module_code': module_code,
                'serial_number': None if serial_number == "0" else serial_number,
                'consumption_value': consumption_value,
                'cumulative_consumption_value': cumulative_consumption_value,
                'flow': flow,
                'state': state
            }
            if device_mode is None and state is None or device_mode == '01' and state is None:
                cr_status = self.register_consumption_record(validated_data=validated_data)
            elif device_mode == '02' or state is not None:
                cr_status = self.register_level_gauge_consumption_record(validated_data=validated_data)
        print("events: {}".format(events))
        er_status = None
        if len(events.keys()) > 0:
            er_status = self.register_events_records(module_code=module_code, events=events)
        if consumption_value is None and or_status is not None:
            return or_status
        if consumption_value is None and len(events.keys()) == 0 and or_status is None:
            return 'OK'
        if cr_status is None and er_status is None:
            return
        elif cr_status is None:
            return er_status
        elif er_status is None:
            return cr_status
        else:
            return er_status

    def register_events_records(self, module_code, events):
        valid_events = {}
        for key, value in events.items():
            if key in self.valid_events.keys():
                valid_events[key] = value

        for key, value in valid_events.items():
            # call event add function from event serializer.
            try:
                event_class = EventSerializer()
                event_class.create_event_serializer(token=token, event_type_code=key,
                                                          event_module_code=module_code,
                                                          event_value=value, event_information={})
            except:
                continue
        return 'OK'

    def register_consumption_record(self, validated_data):
        prepared_data = {
            'token': token,
            'value': validated_data.get('consumption_value'),
            'water_meters': validated_data.get('serial_number'),
            'information': {},
            'module_code': validated_data.get('module_code'),
            'cumulative_value': validated_data.get('cumulative_consumption_value'),

        }
        if validated_data.get('flow', None) is not None: prepared_data['information'] = {
            'flow': validated_data.get('flow')}
        water_meter_class = WaterMeterSerializer()
        # try:
        print(f"prepared_data :{prepared_data}")
        res = water_meter_class.v3_add_consumptions_water_meter_serializer(**prepared_data)
        if res[0] is True:
            return "Ok"
        else:
            return "Unknown_Error"
        # except:
        #     return "Unknown_Error"
    def register_level_gauge_consumption_record(self, validated_data):
        prepared_data = {
            'token': token,
            'value': validated_data.get('consumption_value'),
            'water_meters': validated_data.get('serial_number'),
            'information': {},
            'module_code': validated_data.get('module_code'),
            'cumulative_value': None,
        }
        if validated_data.get('state', None) is not None: prepared_data['information'] = {
            'level_gauge': validated_data.get('state')
        }
        water_meter_class = WaterMeterSerializer()
        try:
            water_meter_class.add_level_gauge_consumptions_water_meter_serializer(**prepared_data)
            response = "Ok"
        except:
            response = "Unknown_Error"
        return response

    def send_order_to_device(self, module_code, serial_number, **order_details):
        # get last device order
        order_detail_dict = {k: v for k, v in order_details.items() if v is not None}
        order_type = list(order_detail_dict.keys())
        if 'device_order' in order_type:
            if len(order_type) > 1:
                return 'Invalid_Format'
            try:
                if module_code is not None and serial_number is None:
                    device_order = Order.objects.filter(
                        order_meter__water_meter_module__water_meter_module_code=module_code,
                        order_status=False).order_by(
                        'order_create_time').last()
                else:
                    device_order = Order.objects.filter(order_meter=serial_number, order_status=False).order_by(
                        'order_create_time').last()
                order_type_code = device_order.as_dict()['order_type']['order_type_code']
                # order_time = device_order.order_create_time.strftime(("%Y-%m-%d %H:%M:%S"))
                order_id = device_order.order_id
                return f"OR:{order_type_code} , ORID:{order_id}"
            except:
                return 'Unknown_Error'
        elif 'device_order_number' in order_type:
            if len(order_type) > 1:
                return 'Invalid_Format'
            if module_code is not None and serial_number is None:
                device_order = Order.objects.filter(
                    order_meter__water_meter_module__water_meter_module_code=module_code, order_status=False)
            else:
                device_order = Order.objects.filter(order_meter=serial_number, order_status=False).order_by(
                    'order_create_time')
            order_number = device_order.count()
            return f"ORN:{order_number}"
        elif 'device_order_status' in order_type and 'device_order_id' in order_type:
            order_id = order_details.get('device_order_id')
            order_status = True if order_details.get('device_order_status') == '1' else False
            try:
                if module_code is not None and serial_number is None:
                    device_order = Order.objects.filter(
                        order_meter__water_meter_module__water_meter_module_code=module_code, order_id=order_id)
                else:
                    device_order = Order.objects.filter(order_meter=serial_number, order_id=order_id)
                device_order.update(order_status=order_status, order_status_time=datetime.datetime.now())
                return 'Ok'
            except:
                'Invalid_Format'
        else:
            return 'Invalid_Format'


dp = DataParser()
base_dir = os.getcwd()
file_path = os.path.join(base_dir, 'log.txt')
fm = FileManager(file_path=file_path)


def handle_client(conn, addr):
    data = conn.recv(1024).decode()
    if not data:
        print("closing connection by client...")
        conn.close()
        return

    print("recieved data from {}: {}".format(addr, data))
    fm.write(message='RCV: {}:{} => {}'.format(addr[0], addr[1], data))
    response = dp.check_data_format(data=data)
    print(response)
    if response is None:
        response = 'Invalid_Format'
        sleep(0.25)
        conn.send(response.encode())
        conn.close()
        return
    else:
        sleep(0.25)
        conn.send(response.encode())
        conn.close()
        return


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("socket binded to port", PORT)
    s.listen()
    print("socket is listening")
    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr[0]}:{addr[1]}")
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
