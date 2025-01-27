import time
import uuid
import paho.mqtt.client as mqtt
from termcolor import colored
import json
import time


class Publisher:

    def __init__(self, client_id=None, name='MQTT publisher client'):
        self.client_id = client_id
        self.name = name
        self.username = None
        self.password = None
        self.host = ''
        self.port = 1883
        self.connected = False

        if client_id is None:
            self.client_id = uuid.uuid1()

        self.client = mqtt.Client(client_id=str(self.client_id))
        self.client.on_connect = self.on_connect

    def set_username_password(self, username, password):
        self.username = username
        self.password = password

    def on_connect(self, client, user_data, flags, rc):
        if rc == 0:
            print(colored('connected OK', 'green'))
            self.connected = True
        else:
            self.connected = False
            if rc == 1:
                error = 'Connection refused – incorrect protocol version'
            elif rc == 2:
                error = 'Connection refused – invalid client identifier'
            elif rc == 3:
                error = 'Connection refused – server unavailable'
            elif rc == 4:
                error = 'Connection refused – bad username or password'
            elif rc == 5:
                error = 'Connection refused – not authorised'
            else:
                error = 'Currently unused'
            print(colored("connection failure with code {}: {}"
                          .format(rc, error), 'red'))

    def on_disconnect(self, client, user_data, rc):
        self.connected = False
        print(colored("disconnected with result code {0}".format(str(rc)), 'red'))
        # self.connect(host=self.host, port=self.port)

    def connect(self, host, port=1883, keep_alive=60):
        self.host = host
        self.port = port
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.connect(host=host, port=port, keepalive=keep_alive)
        self.client.loop_start()
        time.sleep(1)

    def publish(self, topic, message, qos=0, retain=False):
        # print(self.client.is_connected())
        if self.connected:
            print(colored('publishing message "{}" on topic "{}"'
                          .format(message, topic)))
            self.client.publish(topic=topic, payload=message, qos=qos, retain=retain)
        else:
            print(colored('client not connected to broker. can not publish the message!', 'red'))


host = "217.144.106.32"
port = 1883
username = "test"
password = "sayal@mqtt"

p = Publisher()
p.set_username_password(username=username, password=password)
p.connect(host=host, port=port)


def user_publish_message(phone_number, from_where="edit_user"):
    '''
    phone_number: user phone number
    from_where - options:
                        1- edit_user
                        2- delete_user
                        3- add_device
                        4- edit_device
                        5- delete_device
                        6- add_consumption
                        7- edit_consumption
                        8- bill_created
    '''

    topic = "updateService/user/{}".format(phone_number)
    data = {
        'user_edited': False,
        'user_deleted': False,
        'device_changed': False,
        'consumption_changed': False,
        'bill_created': False
    }
    if from_where == "edit_user":
        data['user_edited'] = True
    elif from_where == "delete_user":
        data["user_deleted"] = True
    elif from_where == 'add_device' or from_where == 'edit_device' or from_where == 'delete_device':
        data['device_changed'] = True
    elif from_where == 'add_consumption' or from_where == 'edit_consumption':
        data['consumption_changed'] = True
    elif from_where == 'bill_created':
        data['bill_created'] = True
    message = json.dumps(data)
    p.publish(topic=topic, message=message)
    time.sleep(0.01)


def admin_user_publish_message(meter_serial=None, admin_phone_number=None, project_id=None, from_where='edit_user'):
    """
    project_id :  meter project id
    meter_serial : meter serial
    """
    data = {
        'user_edited': False,
        'user_deleted': False,
        'device_changed': False,
        'consumption_changed': False,
        'bill_created': False
    }
    if meter_serial is not None:
        data['meter_serial'] = meter_serial
    if from_where == "edit_user":
        data['user_edited'] = True
    elif from_where == "delete_user":
        data["user_deleted"] = True
    elif from_where == 'add_device' or from_where == 'edit_device' or from_where == 'delete_device':
        data['device_changed'] = True
    elif from_where == 'add_consumption' or from_where == 'edit_consumption':
        data['consumption_changed'] = True
    elif from_where == 'bill_created':
        data['bill_created'] = True
    # topic = 'meters/admin/{}'.format(project_id)
    if project_id is not None and admin_phone_number is None:
        topic = 'updateService/admin/project/{}'.format(project_id)
    elif admin_phone_number is not None and project_id is None:
        topic = 'updateService/admin/{}'.format(admin_phone_number)
    message = json.dumps(data)
    p.publish(topic=topic, message=message)
    time.sleep(0.01)


def publish_message_to_client(publish_func=None, data=None, phone_number=None, from_where=None):
    """
    use this function to choose which function to call to publish the message
    """
    if publish_func is None and data is None:
        from_where = {'from_where': from_where,
                      'phone_number': phone_number}
        from_where = {k: v for k, v in from_where.items() if v is not None}
        user_publish_message(**from_where)
    elif publish_func == 'middle_admin':
        admin_user_publish_message(**data)


def meters_publisher(topic_name, message):
    # message = json.dumps(message)
    p.publish(topic=topic_name, message=message)


class ResponsePublisher:
    def add_data_response(self, topic_name, message):
        p.publish(topic=topic_name, message=message)

    def add_event_response(self, topic_name, message):
        p.publish(topic=topic_name, message=message)

    def send_commands(self, topic_name, message):
        p.publish(topic=topic_name, message=message, retain=True)
