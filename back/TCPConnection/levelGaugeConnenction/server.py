# define django setting to access project model .
import os
import sys
import django
import uuid
from pathlib import Path

base_dir = os.getcwd()
project_path = Path(base_dir).parent.parent
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
from SayalSanjesh.models import EventType,StaticToken, Order
from SayalSanjesh.Serializers.WaterMeterSerializer import WaterMeterSerializer

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
PORT = 42422    # Port to listen on (non-privileged ports are > 1023)


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
        self.f.write('{} - {} \n'.format(dt, message))
        self.close()


class UserManager:

    def __init__(self, name='client manager for server socket'):
        self.name = name
        self.users = dict()

    def add_user(self, data):
        address = data.get('address')
        connection = data.get('connection')
        u_id = uuid.uuid4()
        self.users[u_id] = {'address': address, 'connection': connection}
        return u_id

    def remove_user(self, user_id):
        try:
            del self.users[user_id]
            return True
        except:
            return False


# API call info
# host = "http://smart.sayalsanjesh.com"
host = "http://217.144.106.32"
port = 6565
endpoint = "watermeters/add/levelGauge/consumption"


class DataParser:

    def __init__(self, name="data parser"):
        self.name = name
        self.required_fields = ['MC']
        self.non_required_fields = ['SN', 'CV']

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

        # return self.prepare_data(validated_data=validated_data)
        data = self.convert_to_dict(seperated_data=seperated_data)
        print("dict data is: {}".format(data))
        if data is None:
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
        # verify consumpton value
        consumption_value = data.get('CV', None)
        if consumption_value is not None:
            try:
                consumption_value = float(consumption_value)
                if consumption_value < 0:
                    return
            except:
                return
        # --------------------------------------------------------------
        # verify state consumption value
        state_value = data.get('ST', None)
        if state_value is None:
            return

        # --------------------------------------------------------------
        # verify cumulative consumption value

        # -----------------------------------------------------------------
        # verify flow

        # -------------------------------------------------------------------
        # verify events

        # ----------------------------------------------------------------------
        cr_status = None
        if consumption_value is not None:
            validated_data = {
                'module_code': module_code,
                'serial_number': None if serial_number == "0" else serial_number,
                'consumption_value': consumption_value,
                'information': {
                    "level_gauge": state_value
                }
            }
            cr_status = self.register_consumption_record(validated_data=validated_data)
        if consumption_value is None == 0:
            return 'OK'
        if cr_status is None:
            return
        else:
            return cr_status

    def register_consumption_record(self, validated_data):
        prepared_data = {
            'token': token,
            'value': validated_data.get('consumption_value'),
            'water_meters': validated_data.get('serial_number'),
            'module_code': validated_data.get('module_code'),
            'information': validated_data.get('information'),
            'cumulative_value': None

        }
        water_meter_class = WaterMeterSerializer()
        # check order
        order_object = Order.objects.filter(order_meter=prepared_data.get('water_meters'), order_status=False)
        if len(order_object) > 0:
            last_object = order_object.order_by('order_create_time').last()
            last_order_type_code = last_object.order_type.order_type_code
            order_structure = {
                '003': '*1111QQQQQQQQQQQQQQ/',
                '004': '*0111QQQQQQQQQQQQQQ/',
                '005': '*1000QQQQQQQQQQQQQQ/',
                '006': '*1100QQQQQQQQQQQQQQ/',
            }
            if last_order_type_code in list(order_structure.keys()):
                order_str = order_structure[last_order_type_code]
            else:
                order_str = None
        else:
            order_str = None
        try:
            water_meter_class.add_level_gauge_consumptions_water_meter_serializer(**prepared_data)
            # check if order exist for this device send order to response if order is not send ok
            if order_str is not None:
                response = order_str
                # update order after send it to device
                Order.objects.filter(order_meter=prepared_data.get('water_meters'),
                                     order_id=last_object.order_id) \
                    .update(order_status=True, order_status_time=datetime.datetime.now())
            else:
                response = "Ok"
        except:
            response = "Unknown_Error"
        return response


root_dir = os.getcwd()

# create log directory and log_file .
if not os.path.exists('log_dir'):
    # If it doesn't exist, create it
    os.makedirs('log_dir')
log_dir = os.path.join(root_dir, 'log_dir')
log_file = os.path.join(log_dir, 'log_file.txt')
if 'log_file.txt' not in log_dir:
    file = open(log_file, "+w")
    file.close()

# ----------------------------
user_manager = UserManager()
fm = FileManager(file_path=log_file)
dp = DataParser()


def handle_client(conn, addr):
    # user_data = {'address': addr, 'connection': conn}
    # user_id = user_manager.add_user(data=user_data)
    data = conn.recv(1024).decode()
    if not data:
        print("closing connection by client...")
        conn.close()
        return

    print("recieved data from {}: {}".format(addr, data))
    # response = ''
    fm.write(message='RCV: {}:{} => {}'.format(addr[0], addr[1], data))
    response = dp.check_data_format(data=data)
    if response is None:
        response = 'Invalid_Format'
        sleep(0.5)
        conn.send(response.encode())
        conn.close()
        return
    else:
        sleep(0.5)
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
