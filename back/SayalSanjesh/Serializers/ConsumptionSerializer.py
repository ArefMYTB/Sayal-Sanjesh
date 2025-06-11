import os
import csv
import pytz
from datetime import datetime, timedelta
from jalali_date import datetime2jalali
from persiantools.jdatetime import JalaliDate
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import WaterMeters, WaterMetersConsumptions, WaterMetersProjects, WaterMetersTags
from Authorization.models.Users import Users
from Authorization.models.Admins import Admins
from Authorization.models.MiddleAdmins import MiddleAdmins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from Authorization.Serializers.StaticTokenSerializer import StaticTokenSerializer
from MQQTReceiver.publisher import publish_message_to_client
from General.models import MqttLoger
from .jalali import jalali_to_gregorian
from persiantools.jdatetime import JalaliDateTime
from django.db.models import Sum, Max, Min, Q, F, Case, When, Value, IntegerField, Subquery, OuterRef, Count
from SayalSanjesh.models.Meters import Bills
# -----------------
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Aggregate
from django.db.models import CharField
from django.db.models.functions import TruncDate
from django.utils import timezone

class Concat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)


# ------------------
class ConsumptionSerializer:
    # ------------------------------------------------- AdminSerializers ----------------------------------------------
    @staticmethod
    def admin_get_all_consumptions_serializer(token, page, count, water_meters, water_meter_user, water_meter_project,
                                              water_meter_type, start_time, end_time):
        """
            param : [token, page, count, water_meters, water_meter_user, water_meter_project,
                                      water_meter_type, start_time, end_time]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            def consumption_results(all_consumption, all_consumption_count):
                consumptions_result = []
                for consumption in all_consumption:
                    if (consumption.log_id != None):
                        print(MqttLoger.objects.get(log_id=consumption.log_id))
                    if consumption.from_previous_record == None:
                        from_previous_record = ""
                    else:
                        from_previous_record = consumption.from_previous_record
                    if consumption.to_current_record == None:
                        to_current_record = ""
                    else:
                        to_current_record = consumption.to_current_record
                    consumption_info = {
                        "consumption_id": consumption.consumption_id,
                        "value": consumption.value,
                        "device_value": consumption.device_value,
                        "cumulative_value": consumption.cumulative_value  + (consumption.water_meters.initial_value or 0.0),
                        "create_time": str(consumption.create_time),
                        "information": consumption.information,
                        "counter": consumption.counter,
                        "value_type": consumption.value_type,
                        "flow_instantaneous": consumption.flow_instantaneous,
                        "flow_Type": consumption.flow_Type,
                        "flow_Value": consumption.flow_Value,
                        # Read from log
                        "log_time": str(MqttLoger.objects.filter(log_id=consumption.log_id).values_list('create_date', flat=True).first()) or "",
                        "log_message": str(MqttLoger.objects.filter(log_id=consumption.log_id).values_list('message', flat=True).first()) or "",

                        "from_previous_record": str(from_previous_record),
                        "to_current_record":str(to_current_record),
                        "bill_created": consumption.bill_created,
                        "water_meters_info": {
                            "water_meter_serial": consumption.water_meters.water_meter_serial,
                            "water_meter_name": consumption.water_meters.water_meter_name,
                            "water_meter_condition": consumption.water_meters.water_meter_condition,
                            "water_meter_validation": consumption.water_meters.water_meter_validation,
                            "water_meter_activation": consumption.water_meters.water_meter_activation,
                            "water_meter_create_date": str(consumption.water_meters.water_meter_create_date),
                            "other_information": consumption.water_meters.other_information,
                        },

                        "type_info": {
                            "water_meter_type_id": consumption.water_meters.water_meter_type.water_meter_type_id,
                            "water_meter_type_name": consumption.water_meters.water_meter_type.water_meter_type_name,
                            "water_meter_type_create_date": str(consumption.water_meters.water_meter_type.water_meter_type_create_date),
                        },
                        "tag_info": {
                            "water_meter_tag_id": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_id,
                            "water_meter_tag_name": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_name,
                            "water_meter_tag_create_date": str(consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_create_date),
                        },
                        "all_consumptions": all_consumption_count,
                    }

                    if consumption.water_meters.water_meter_user != None:
                        consumption_info['user_info'] = {
                            "user_name": consumption.water_meters.water_meter_user.user_name,
                            "user_lastname": consumption.water_meters.water_meter_user.user_lastname,
                            "user_phone": consumption.water_meters.water_meter_user.user_phone,
                            "user_id": consumption.water_meters.water_meter_user.user_id,
                        }
                    else:
                        consumption_info['user_info'] = "user is null"
                    if consumption.water_meters.water_meter_project != None:
                        consumption_info['project_info'] = {
                            "water_meter_project_id": consumption.water_meters.water_meter_project.water_meter_project_id,
                            "water_meter_project_name": consumption.water_meters.water_meter_project.water_meter_project_name,
                            "water_meter_project_title": consumption.water_meters.water_meter_project.water_meter_project_title,
                            "water_meter_project_create_date": str(consumption.water_meters.water_meter_project.water_meter_project_create_date),
                        }
                    else:
                        consumption_info['project_info'] = "project is null"
                    consumptions_result.append(consumption_info)
                return consumptions_result

            if AdminsSerializer.admin_check_permission(admin_id, ['ViewDevice']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        'water_meters': water_meters,
                        'water_meters__water_meter_user': water_meter_user,
                        'water_meters__water_meter_project': water_meter_project,
                        'water_meters__water_meter_type': water_meter_type,
                        'create_time__gte': start_time,
                        'create_time__lte': end_time,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    all_consumption = WaterMetersConsumptions.objects.filter(**filters)
                    all_consumption_paginated = all_consumption.order_by('-create_time')[
                                                offset:offset + limit]
                    all_consumption_count = all_consumption.count()
                    cons_results = consumption_results(all_consumption=all_consumption_paginated,
                                                       all_consumption_count=all_consumption_count)
                    return True, cons_results
                else:
                    return field_result
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_projects_list = middle_admin.project_ids
                middle_admin_water_meters_values = WaterMeters.objects.filter(
                    water_meter_project__in=middle_admin_projects_list).values(
                    'water_meter_serial')
                middle_admin_water_meter = []
                for water_serial in middle_admin_water_meters_values:
                    middle_admin_water_meter.append(water_serial['water_meter_serial'])

                water_meter_final = []
                if water_meters != None:
                    if water_meters in middle_admin_water_meter:
                        water_meter_final.append(water_meters)
                    else:
                        wrong_data_result["farsi_message"] = "کنتور را به ادمین اضافه کنید"
                        wrong_data_result["english_message"] = "Add the meter to the admin"
                        return False, wrong_data_result
                else:
                    water_meter_final = middle_admin_water_meter
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)

                    filters = {
                        'water_meters__in': water_meter_final,
                        'water_meters__water_meter_user': water_meter_user,
                        'water_meters__water_meter_project': water_meter_project,
                        'water_meters__water_meter_type': water_meter_type,
                        'create_time__gte': start_time,
                        'create_time__lte': end_time,
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    all_consumption = WaterMetersConsumptions.objects.filter(**filters)
                    all_consumption_paginated = all_consumption.order_by('-create_time')[
                                                offset:offset + limit]
                    all_consumption_count = all_consumption.count()
                    cons_results = consumption_results(all_consumption=all_consumption_paginated,
                                                       all_consumption_count=all_consumption_count)

                    return True, cons_results
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_consumption_serializer(token, consumption_id):
        """
            param : [token, consumption_id]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, 'ViewDevice'):
                try:
                    consumption = WaterMetersConsumptions.objects.get(consumption_id=consumption_id)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است consumption_id"
                    wrong_data_result["english_message"] = "Wrong consumption_id"
                    return False, wrong_data_result
                if consumption.from_previous_record == None:
                    from_previous_record = ""
                else:
                    from_previous_record = consumption.from_previous_record
                if consumption.to_current_record == None:
                    to_current_record = ""
                else:
                    to_current_record = consumption.to_current_record
                consumption_result = {
                    "consumption_id": consumption.consumption_id,
                    "create_time": consumption.create_time,
                    "value": consumption.value,
                    "information": consumption.information,
                    "from_previous_record": from_previous_record,
                    "to_current_record": to_current_record,
                    "bill_created": consumption.bill_created,
                    "water_meters": consumption.water_meters.water_meter_serial,
                    "water_meter_info": {
                        "water_meter_name": consumption.water_meters.water_meter_name,
                        "water_meter_activation": consumption.water_meters.water_meter_activation,
                        "water_meter_validation": consumption.water_meters.water_meter_validation,
                        "water_meter_condition": consumption.water_meters.water_meter_condition,
                        "other_information": consumption.water_meters.other_information,
                        "water_meter_create_date": consumption.water_meters.water_meter_create_date,
                    },
                    "type_info": {
                        "water_meter_type_id": consumption.water_meters.water_meter_type.water_meter_type_id,
                        "water_meter_type_name": consumption.water_meters.water_meter_type.water_meter_type_name,
                        "water_meter_type_create_date": consumption.water_meters.water_meter_type.water_meter_type_create_date,
                    },
                    "tag_info": {
                        "water_meter_tag_name": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_name,
                        "water_meter_tag_id": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_id,
                        "water_meter_tag_create_date": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_create_date,
                    },
                }
                if consumption.water_meters.water_meter_user != None:
                    consumption_result["user_info"] = {
                        "user_id": consumption.water_meters.water_meter_user.user_id,
                        "user_phone": consumption.water_meters.water_meter_user.user_phone,
                        "user_name": consumption.water_meters.water_meter_user.user_name,
                        "user_lastname": consumption.water_meters.water_meter_user.user_lastname,
                        "user_create_date": consumption.water_meters.water_meter_user.user_create_date,
                    }
                else:
                    consumption_result["user_info"] = {
                        "user_id": "",
                        "user_phone": "",
                        "user_name": "",
                        "user_lastname": "",
                        "user_create_date": "",
                    }
                if consumption.water_meters.water_meter_project != None:
                    consumption_result["project_info"] = {
                        "water_meter_project_id": consumption.water_meters.water_meter_project.water_meter_project_id,
                        "water_meter_project_name": consumption.water_meters.water_meter_project.water_meter_project_name,
                        "water_meter_project_title": consumption.water_meters.water_meter_project.water_meter_project_title,
                        "water_meter_project_create_date": consumption.water_meters.water_meter_project.water_meter_project_create_date,
                    }
                else:
                    consumption_result["project_info"] = {
                        "water_meter_project_id": "",
                        "water_meter_project_name": "",
                        "water_meter_project_title": "",
                        "water_meter_project_create_date": "",
                    }
                return True, consumption_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_remove_consumption_serializer(token, consumption_id, water_meter_serial, mode, time):
        """
            param : [token, consumption_id, water_meter_serial, mode, time]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ['Joker', 'ClearDeviceData']):
                # check for deleting consumptions
                valid_mode = ['all', 'single_consumption', 'time']
                if mode not in valid_mode:
                    wrong_data_result["farsi_message"] = f"پارامتر های مجاز برای mode  : {valid_mode}"
                    wrong_data_result["english_message"] = f"Authorized parameters for the mod : {valid_mode}"
                    return False, wrong_data_result
                # get meter object and check for meter serial is valid or not .
                try:
                    meter_object = WaterMeters.objects.get(water_meter_serial=water_meter_serial)
                except:
                    wrong_data_result["farsi_message"] = "شمازه سریال کنتور اشتباه است ."
                    wrong_data_result["english_message"] = "The serial number of the meter is wrong."
                    return False, wrong_data_result
                if mode == 'single_consumption':
                    try:
                        consumption_object = WaterMetersConsumptions.objects.get(
                            consumption_id=consumption_id, water_meters=meter_object)
                        consumption_object.delete()
                        return True, status_success_result
                    except:
                        wrong_data_result["farsi_message"] = "ای دی مقدار مصرف اشتباه وارد شده است . "
                        wrong_data_result["english_message"] = "The consumption ID was entered incorrectly."
                        return False, wrong_data_result
                elif mode == 'all':
                    consumptions = WaterMetersConsumptions.objects.filter(water_meters=meter_object)
                    consumptions.delete()
                    return True, status_success_result
                elif mode == 'time':
                    # check  dictionary items
                    if 'date_type' and 'create_time' not in time:
                        wrong_data_result["farsi_message"] = f"لطفا مقدار های Date_type و create_time را وارد کنید . "
                        wrong_data_result["english_message"] = "Please enter  date_type and create_time values."
                        return False, wrong_data_result
                    # check for valid value for data_type field.
                    valid_data_type = ['jalali', 'utc']
                    if time['date_type'] not in valid_data_type:
                        wrong_data_result["farsi_message"] = f"پارامتر های مجاز برای date_type  : {valid_data_type}"
                        wrong_data_result[
                            "english_message"] = f"Authorized parameters for the Date_type : {valid_data_type}"
                        return False, wrong_data_result
                    if time['date_type'] == 'jalali':
                        # convert time to utc if date_type is jalali
                        jalali_time = time['create_time'].split('-')
                        jalali_time = list(map(lambda x: int(x), jalali_time))
                        utc_time = JalaliDate(jalali_time[0], jalali_time[1], jalali_time[2]).to_gregorian()
                    else:
                        split_time = time['create_time'].split(' ')
                        date = split_time[0].split('-')
                        time_split = split_time[1].split(':')
                        print(f"this is split_time : {split_time}")
                        print(f"this is date : {date}")
                        print(f"this is time_split : {time_split}")
                        utc_time = datetime(int(date[0]), int(date[1]), int(date[2]), int(time_split[0]),
                                            int(time_split[1]),
                                            int(time_split[2]))
                    consumptions = WaterMetersConsumptions.objects.filter(
                        water_meters=meter_object, create_time__lte=utc_time).order_by('-create_time')
                    consumptions.delete()
                    test_ar = []
                    for cons in consumptions:
                        ts = {
                            "time": cons.create_time,
                            "value": cons.value
                        }
                        test_ar.append(ts)
                    res = {

                        "message": test_ar
                    }
                return True, res
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_consumption_serializer(token, consumption_id, value, information, create_time, from_previous_record,
                                          to_current_record):
        """
            param : [token, consumption_id, value, information, create_time, from_previous_record,
                                          to_current_record]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Joker'):
                fields = {
                    "value": (value, str),
                    "information": (information, dict)
                }
                result = wrong_result(fields)
                if result == None:
                    try:
                        if create_time == None or from_previous_record == None or to_current_record == None:
                            consumption_edit = WaterMetersConsumptions.objects.filter(
                                consumption_id=consumption_id).update(
                                value=value,
                                information=information)
                        else:
                            consumption_edit = WaterMetersConsumptions.objects.filter(
                                consumption_id=consumption_id).update(
                                value=value, create_time=create_time, from_previous_record=from_previous_record,
                                to_current_record=to_current_record,
                                information=information)
                    except:
                        wrong_data_result["farsi_message"] = "اشتباه است consumption_id"
                        wrong_data_result["english_message"] = "Wrong consumption_id"
                        return False, wrong_data_result
                    if consumption_edit == 1:
                        consumption = WaterMetersConsumptions.objects.get(consumption_id=consumption_id)
                        phone_number = consumption.water_meters.water_meter_user.user_phone
                        publish_message_to_client(phone_number=phone_number, from_where='edit_consumption')
                        project_obj = consumption.water_meters.water_meter_project
                        if project_obj is not None:
                            admin_obj = Admins.objects.get(admin_id=admin_id)
                            middle_admin_publish_data = {
                                'admin_phone_number': admin_obj.admin_phone,
                                'meter_serial': consumption.water_meters.water_meter_serial,
                                'from_where': 'edit_consumption'
                            }
                            publish_message_to_client(publish_func='middle_admin', data=middle_admin_publish_data)
                        return True, status_success_result
                    else:
                        wrong_data_result["farsi_message"] = "اشتباه است،user_id"
                        wrong_data_result["english_message"] = "Wrong user_id"
                        return False, wrong_data_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def admin_get_cumulative_consumptions_serializer(token, page, count, user_id, project_id, water_meter_serial,
                                                     water_meter_tag, sort_value, input_reverse):
        """
            param : [token, page, count, user_id, project_id, water_meter_serial,water_meter_tag, sort_value,
                        input_reverse]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            # water_meters_consumptions_dict = {}
            cumulative_result_dict = {}
            cumulative_result_list = []
            test_result_dict = {}

            # calculate cumulative value from consumption table .
            def _calculate_cumulative_and_get_last_consumption(all_water_meters):
                current_time = datetime.now()
                # get current time to jalali date .
                jalali_join = datetime2jalali(current_time).strftime('%y/%m/%d')
                jalali_join_split = jalali_join.split('/')
                if jalali_join_split[0] == '01':
                    jalali_join_split[0] = '1401'
                if jalali_join_split[0] == '02':
                    jalali_join_split[0] = '1402'
                if jalali_join_split[0] == '03':
                    jalali_join_split[0] = '1403'
                # get first day and last day of month in jalali date
                if int(jalali_join_split[1]) <= 6:
                    last_day_month = 31
                elif int(jalali_join_split[1]) > 6:
                    last_day_month = 30
                # jalaliToGeorgian_currentTime
                j2g = jalali_to_gregorian(jy=int(jalali_join_split[0]),
                                          jm=int(jalali_join_split[1]),
                                          jd=int(jalali_join_split[2]))
                j2g_str = f'{j2g[0]}-{j2g[1]}-{j2g[2]}'

                # Month
                # GeorgianFirstDayMonth
                g_first_day = jalali_to_gregorian(jy=int(jalali_join_split[0]),
                                                  jm=int(jalali_join_split[1]),
                                                  jd=1)
                # g_first_day too str
                if g_first_day[1] <= 9:
                    g_first_day[1] = f'0{g_first_day[1]}'
                if g_first_day[2] <= 9:
                    g_first_day[2] = f'0{g_first_day[2]}'
                g_first_day_2_str = f'{g_first_day[0]}-{g_first_day[1]}-{g_first_day[2]}'

                # GeorgianLastDayMonth
                g_last_day = jalali_to_gregorian(jy=int(jalali_join_split[0]),
                                                 jm=int(jalali_join_split[1]),
                                                 jd=last_day_month)
                # g_last_day too str
                if g_last_day[1] <= 9:
                    g_last_day[1] = f'0{g_last_day[1]}'
                if g_last_day[2] <= 9:
                    g_last_day[2] = f'0{g_last_day[2]}'
                g_last_day_2_str = f'{g_last_day[0]}-{g_last_day[1]}-{g_last_day[2]} 03:29:00'
                # End Month

                # Year
                # GeorgianFirstDayYear
                g_first_day_y = jalali_to_gregorian(jy=int(jalali_join_split[0]), jm=1, jd=1)
                # g_first_year too str
                if g_first_day_y[1] <= 9:
                    g_first_day_y[1] = f'0{g_first_day_y[1]}'
                if g_first_day_y[2] <= 9:
                    g_first_day_y[2] = f'0{g_first_day_y[2]}'
                g_first_day_y_2_str = f'{g_first_day_y[0]}-{g_first_day_y[1]}-{g_first_day_y[2]}'

                # GeorgianLastDayYear
                g_last_day_y = jalali_to_gregorian(jy=int(jalali_join_split[0]), jm=12, jd=29)
                # g_last_year too str
                if g_last_day_y[1] <= 9:
                    g_last_day_y[1] = f'0{g_last_day_y[1]}'
                if g_last_day_y[2] <= 9:
                    g_last_day_y[2] = f'0{g_last_day_y[2]}'
                g_last_day_y_2_str = f'{g_last_day_y[0]}-{g_last_day_y[1]}-{g_last_day_y[2]}'
                # End Year

                for water_meter_obj in all_water_meters:
                    serial = water_meter_obj.water_meter_serial
                    if serial not in cumulative_result_dict:
                        cumulative_result_dict[serial] = {
                            # 'water_meter_serial': serial,
                            'cumulative_consumptions': {},
                            'last_consumption': {},

                        }
                        consumptions_objects = WaterMetersConsumptions.objects.filter(water_meters=serial)
                        # sum all consumption
                        total_value = consumptions_objects.aggregate(Sum('value'))['value__sum']

                        # get last record
                        last_consumption = consumptions_objects.order_by(
                            'create_time').last()
                        if last_consumption is not None:
                            last_consumption = last_consumption.as_dict()
                            last_consumption.pop('water_meters')
                            last_consumption['timestamp'] = int(round(last_consumption['create_time'].timestamp()))
                            cumulative_value = last_consumption['cumulative_value']
                            if cumulative_value is not None:
                                difference = abs(total_value - cumulative_value)
                                if difference > 0 and difference < 10:
                                    final_total = cumulative_value
                                else:
                                    final_total = total_value
                            else:
                                final_total = total_value
                        else:
                            final_total = total_value
                        cumulative_result_dict[serial]['total_value'] = final_total
                        cumulative_result_dict[serial]['last_consumption'] = last_consumption
                        # end get last record

                        # year
                        cumulative_year_objects = consumptions_objects.filter(create_time__gte=g_first_day_y_2_str,
                                                                              create_time__lte=g_last_day_y_2_str)
                        cumulative_year_sum = cumulative_year_objects.aggregate(Sum('value'))
                        final_year_value = cumulative_year_sum["value__sum"]
                        if final_year_value is None:
                            final_year_value = 0
                        cumulative_result_dict[serial]['cumulative_consumptions']['year'] = (
                            jalali_join_split[0], final_year_value)
                        # month
                        cumulative_month_objects = consumptions_objects.filter(
                            create_time__gte=g_first_day_2_str,
                            create_time__lte=g_last_day_2_str)
                        cumulative_month_sum = cumulative_month_objects.aggregate(Sum('value'))
                        final_month_value = cumulative_month_sum["value__sum"]
                        if final_month_value is None:
                            final_month_value = 0
                        cumulative_result_dict[serial]['cumulative_consumptions']['month'] = (
                            jalali_join_split[1], final_month_value)

                        # day
                        cumulative_day_objects = consumptions_objects.filter(
                            create_time__startswith=current_time.date())
                        cumulative_day_sum = cumulative_day_objects.aggregate(Sum('value'))
                        final_day_value = cumulative_day_sum["value__sum"]
                        if final_day_value is None:
                            final_day_value = 0
                        cumulative_result_dict[serial]['cumulative_consumptions']['day'] = (
                            jalali_join_split[2], final_day_value)

                    # cumulative_result_list.append(cumulative_result)
                # end calculate cumulative value from consumption table .

            def _sort_value(sort_value, input_reverse):

                if input_reverse is None:
                    input_reverse = True

                if sort_value == 'last_consumption':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['last_consumption']['value'] if
                                         x[1]['last_consumption'] is not None else 0, reverse=input_reverse)

                    return True, sorted_list

                elif sort_value == 'month':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['cumulative_consumptions']['month'] if
                                         x[1]['cumulative_consumptions']['month'] is not None else 0,
                                         reverse=input_reverse)

                    return True, sorted_list
                elif sort_value == 'year':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['cumulative_consumptions']['year'] if
                                         x[1]['cumulative_consumptions']['year'] is not None else 0,
                                         reverse=input_reverse)
                    return True, sorted_list
                elif sort_value == 'day':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['cumulative_consumptions']['day'] if
                                         x[1]['cumulative_consumptions']['day'] is not None else 0,
                                         reverse=input_reverse)
                    return True, sorted_list

                elif sort_value == 'consumption_create_time':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['last_consumption']['timestamp'] if
                                         x[1]['last_consumption'] is not None else 0,
                                         reverse=input_reverse)
                    return True, sorted_list
                else:
                    return True, []

            if AdminsSerializer.admin_check_permission(admin_id, ''):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)

                    filters = {
                        'water_meter_serial': water_meter_serial,
                        'water_meter_user__user_id': user_id,
                        'water_meter_project__water_meter_project_id': project_id,
                        'water_meter_type__water_meter_tag__water_meter_tag_id': water_meter_tag
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    # try:
                    all_water_meter_query = WaterMeters.objects.filter(**filters)

                    # if input_reverse is not None and input_reverse == True:
                    #     all_water_meter_pagination = all_water_meter_query.order_by(
                    #         'water_meter_create_date')[offset:offset + limit]
                    # else:
                    #     all_water_meter_pagination = all_water_meter_query.order_by(
                    #         '-water_meter_create_date')[offset:offset + limit]
                    all_water_meter_pagination = all_water_meter_query.order_by(
                        'water_meter_create_date')[offset:offset + limit]
                    _calculate_cumulative_and_get_last_consumption(all_water_meters=all_water_meter_pagination)
                    # cumulative_result_list = [cumulative_result_dict[cumulative_result] for cumulative_result in
                    #                           cumulative_result_dict]
                    if input_reverse is not None and sort_value is None:
                        sort_value = 'consumption_create_time'
                    if water_meter_tag is not None:
                        if sort_value is not None:
                            return _sort_value(sort_value=sort_value, input_reverse=input_reverse)
                        else:
                            cumulative_result_list = [(k, v) for k, v in cumulative_result_dict.items()]
                            return True, cumulative_result_list
                    else:
                        cumulative_result_list = [(k, v) for k, v in cumulative_result_dict.items()]
                        return True, cumulative_result_list

                else:
                    return field_result

            elif AdminsSerializer.admin_check_permission(admin_id, ['Middle']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                # middle_admin_water_meters = middle_admin.water_meter_ids
                middle_admin_projects = middle_admin.project_ids
                middle_admin_water_meters = WaterMeters.objects.filter(
                    water_meter_project__in=middle_admin_projects).values('water_meter_serial')
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)

                    filters = {
                        'water_meter_user__user_id': user_id,
                    }
                    if project_id is None:
                        filters['water_meter_project__in'] = middle_admin_projects
                    else:
                        filters['water_meter_project__water_meter_project_id'] = project_id
                    filters = {k: v for k, v in filters.items() if v is not None}
                    try:
                        all_water_meters_query = WaterMeters.objects.filter(**filters)
                        if input_reverse is not None and input_reverse == True:
                            all_water_meter_pagination = all_water_meters_query.order_by(
                                'water_meter_create_date')[offset:offset + limit]
                        else:
                            all_water_meter_pagination = all_water_meters_query.order_by(
                                '-water_meter_create_date')[offset:offset + limit]
                        _calculate_cumulative_and_get_last_consumption(all_water_meters=all_water_meter_pagination)
                        # cumulative_result_list = [cumulative_result_dict[cumulative_result] for cumulative_result in
                        #                           cumulative_result_dict]
                        if water_meter_tag is not None:
                            if sort_value is not None:
                                return _sort_value(sort_value=sort_value, input_reverse=input_reverse)
                            else:
                                cumulative_result_list = [(k, v) for k, v in cumulative_result_dict.items()]
                                return True, cumulative_result_list
                        else:
                            cumulative_result_list = [(k, v) for k, v in cumulative_result_dict.items()]
                            return True, cumulative_result_list
                    except:
                        cumulative_result_list = []
                    return True, cumulative_result_list
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_cumulative_consumptions_per_tag_serializer(token, user_id, project_id,
                                                             water_meter_serial):
        """
            param : [token, user_id, project_id,water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, ''):

                current_time = datetime.now()
                one_day_before = current_time - timedelta(days=1)
                print(f"this is current_time: {current_time} -  one_day_before:{one_day_before}")
                # get current time to jalali date .
                jalali_join = datetime2jalali(one_day_before).strftime('%y/%m/%d')
                jalali_join_split = jalali_join.split('/')
                if jalali_join_split[0] == '01':
                    jalali_join_split[0] = '1401'
                elif jalali_join_split[0] == '02':
                    jalali_join_split[0] = '1402'
                elif jalali_join_split[0] == '03':
                    jalali_join_split[0] = '1403'
                jalali_to_str = f'{jalali_join_split[0]}-{jalali_join_split[1]}-{jalali_join_split[2]}'

                result_dict = {}
                filters = {
                    'water_meters__water_meter_serial__icontains': water_meter_serial,
                    'water_meters__water_meter_user__user_id': user_id,
                    'water_meters__water_meter_project__water_meter_project_id': project_id,
                    # 'create_time__startswith': one_day_before.date(),
                    'create_time__year': one_day_before.date().year,
                    'create_time__month': one_day_before.date().month,
                    'create_time__day': one_day_before.date().day,
                }
                if project_id is None:
                    """
                    get all tag in system and filter on it . 
                    """
                    all_system_tag = WaterMetersTags.objects.all()
                    for tag_obj in all_system_tag:
                        filters[
                            'water_meters__water_meter_type__water_meter_tag__water_meter_tag_id'] = tag_obj.water_meter_tag_id
                        filters = {k: v for k, v in filters.items() if v is not None}
                        tag_sum_cumulative = WaterMetersConsumptions.objects.filter(**filters).aggregate(
                            Sum('value'))
                        result_dict[tag_obj.water_meter_tag_name] = {
                            # 'tag_id': tag_obj.water_meter_tag_id,
                            'time': (one_day_before.date(), jalali_to_str),
                            'cumulative_consumption': tag_sum_cumulative['value__sum']
                        }
                else:
                    """
                    get project tag . 
                    """
                    try:
                        project_obj = WaterMetersProjects.objects.get(water_meter_project_id=project_id)
                    except:
                        wrong_data_result["farsi_message"] = "project_id اشتباه است"
                        wrong_data_result["english_message"] = "Wrong project_id"
                        return False, wrong_data_result
                    project_obj_types = project_obj.water_meter_types.all().distinct()
                    project_obj_tags = project_obj_types.values('water_meter_tag__water_meter_tag_id',
                                                                'water_meter_tag__water_meter_tag_name').distinct()
                    for tag_obj in project_obj_tags:
                        filters['water_meters__water_meter_type__water_meter_tag__water_meter_tag_id'] = tag_obj[
                            'water_meter_tag__water_meter_tag_id']
                        filters = {k: v for k, v in filters.items() if v is not None}
                        consumption_objects = WaterMetersConsumptions.objects.filter(**filters)
                        tag_sum_cumulative = consumption_objects.aggregate(
                            Sum('value'))
                        result_dict[tag_obj['water_meter_tag__water_meter_tag_name']] = {
                            # 'meter_name':consumption_objects.values('water_meters'),
                            'cumulative_consumption': {
                                'time': (one_day_before.date(), jalali_to_str),
                                'value': tag_sum_cumulative['value__sum']
                            }
                        }
                return True, result_dict

            elif AdminsSerializer.admin_check_permission(admin_id, ['Middle']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                # middle_admin_water_meters = middle_admin.water_meter_ids
                middle_admin_projects = middle_admin.project_ids
                middle_admin_water_meters = WaterMeters.objects.filter(
                    water_meter_project__in=middle_admin_projects).values('water_meter_serial')

                current_time = datetime.now()
                # get current time to jalali date .
                jalali_join = datetime2jalali(current_time).strftime('%y/%m/%d')
                jalali_join_split = jalali_join.split('/')
                if jalali_join_split[0] == '01':
                    jalali_join_split[0] = '1401'
                elif jalali_join_split[0] == '02':
                    jalali_join_split[0] = '1402'
                elif jalali_join_split[0] == '03':
                    jalali_join_split[0] = '1403'
                jalali_to_str = f'{jalali_join_split[0]}-{jalali_join_split[1]}-{jalali_join_split[2]}'

                result_dict = {}
                filters = {
                    'water_meters__water_meter_serial__icontains': water_meter_serial,
                    'water_meters__water_meter_user__user_id': user_id,
                    'water_meters__water_meter_project__water_meter_project_id': project_id,
                    'create_time__startswith': current_time.date()
                }
                if project_id is None:
                    """
                    get all tag in system and filter on it . 
                    """
                    filters.pop('water_meters__water_meter_project__water_meter_project_id')
                    filters['water_meters__water_meter_project__water_meter_project_id__in'] = middle_admin_projects
                    all_system_tag = WaterMetersTags.objects.all()
                    for tag_obj in all_system_tag:
                        filters[
                            'water_meters__water_meter_type__water_meter_tag__water_meter_tag_id'] = tag_obj.water_meter_tag_id
                        filters = {k: v for k, v in filters.items() if v is not None}
                        tag_sum_cumulative = WaterMetersConsumptions.objects.filter(**filters).aggregate(
                            Sum('value'))
                        result_dict[tag_obj.water_meter_tag_name] = {
                            # 'tag_id': tag_obj.water_meter_tag_id,
                            'time': (current_time.date(), jalali_to_str),
                            'cumulative_consumption': tag_sum_cumulative['value__sum']
                        }
                else:
                    """
                    get project tag . 
                    """
                    if project_id in middle_admin_projects:
                        project_obj = WaterMetersProjects.objects.get(water_meter_project_id=project_id)
                        project_obj_types = project_obj.water_meter_types.all().distinct()
                        project_obj_tags = project_obj_types.values('water_meter_tag__water_meter_tag_id',
                                                                    'water_meter_tag__water_meter_tag_name').distinct()
                        for tag_obj in project_obj_tags:
                            filters['water_meters__water_meter_type__water_meter_tag__water_meter_tag_id'] = tag_obj[
                                'water_meter_tag__water_meter_tag_id']
                            filters = {k: v for k, v in filters.items() if v is not None}
                            consumption_objects = WaterMetersConsumptions.objects.filter(**filters)
                            tag_sum_cumulative = consumption_objects.aggregate(
                                Sum('value'))
                            result_dict[tag_obj['water_meter_tag__water_meter_tag_name']] = {
                                # 'meter_name':consumption_objects.values('water_meters'),
                                'cumulative_consumption': {
                                    'time': (current_time.date(), jalali_to_str),
                                    'value': tag_sum_cumulative['value__sum']
                                }
                            }
                    elif project_id not in middle_admin_projects:
                        wrong_data_result["farsi_message"] = "project_id اشتباه است"
                        wrong_data_result["english_message"] = "Wrong project_id"
                        return False, wrong_data_result
                return True, result_dict

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_last_consumption_data_by_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ViewDevice'):
                try:
                    consumption = WaterMetersConsumptions.objects.filter(water_meters=water_meter_serial).order_by(
                        'create_time').last()
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result
                consumption = consumption.as_dict()
                consumption.update({
                    'water_meters': consumption['water_meters']['water_meter_serial']
                })
                return True, consumption
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_all_water_meter_consumption(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ViewDevice'):
                all_consumption_values = WaterMetersConsumptions.objects.all().values('value')
                all_values = {}
                number = 0
                for value in all_consumption_values:
                    value = value['value']
                    all_values.update({
                        f'value_{number}': value,
                    })
                    number += 1
                sum_all_values = sum(all_values.values())
                test = {
                    "sum_all_values": sum_all_values
                }
                return True, test
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_consumptions_by_date_serializer(token, page, count, water_meters, start_time, end_time, user_id,
                                                      tag_id, project_id, type_id):
        """
            param : [token, page, count, water_meters, start_time, end_time, user_id,
                                                      tag_id, project_id, type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, 'Admin'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)

                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        'water_meters': water_meters,
                        'water_meters__water_meter_user': user_id,
                        'water_meters__water_meter_type': type_id,
                        'water_meters__water_meter_type__water_meter_tag': tag_id,
                        'water_meters__water_meter_project': project_id,
                    }
                    date_sum_value = {}

                    # all consumptions per date
                    try:                        
                        filters['create_time__gte'] = start_time
                        filters['create_time__lte'] = end_time
                        all_consumption_filters = {k: v for k, v in filters.items() if v is not None}
                        all_consumption = (
                            WaterMetersConsumptions.objects
                            .filter(**all_consumption_filters)
                            .annotate(date=TruncDate('create_time'))
                            .values('date')
                            .annotate(sum=Sum('value'))
                            .order_by('-date')[offset:offset + limit]
                        )

                        filters.pop('create_time__gte')
                        filters.pop('create_time__lte')

                        # Cumulative consumptions until start date
                        filters['create_time__lte'] = start_time
                        cumulative_filters = {k: v for k, v in filters.items() if v is not None}

                        cumulative_consumptions = (
                            WaterMetersConsumptions.objects
                            .filter(**cumulative_filters)
                            .aggregate(Sum('value'))
                        )
                        date_sum_value['cumulative_consumptions'] = cumulative_consumptions['value__sum']

                        if not all_consumption:
                            return True, []

                        count_check = 0
                        total_value = 0.0
                        for cons in all_consumption:
                            count_check += 1
                            date_sum_value[str(cons['date'])] = cons['sum']
                            total_value += cons['sum']

                        date_sum_value['total'] = total_value
                        date_sum_value['average'] = "{:.2f}".format(total_value / len(all_consumption))

                    except:
                        wrong_data_result["farsi_message"] = ""
                        wrong_data_result["english_message"] = "water_meter_serial or time input Error"
                    return True, date_sum_value
                else:
                    return field_result

            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                # middle_admin_water_meters = middle_admin.water_meter_ids
                middle_admin_project_ids = middle_admin.project_ids
                middle_admin_projects_list = middle_admin.project_ids
                middle_admin_water_meters_values = WaterMeters.objects.filter(
                    water_meter_project__in=middle_admin_projects_list).values(
                    'water_meter_serial')
                middle_admin_water_meter = []
                for water_serial in middle_admin_water_meters_values:
                    middle_admin_water_meter.append(water_serial['water_meter_serial'])
                if water_meters is not None:
                    if water_meters not in middle_admin_water_meter:
                        wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                        wrong_data_result["english_message"] = "Wrong water_meter_serial"
                        return False, wrong_data_result

                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        # 'water_meters': water_meters,
                        'water_meters__water_meter_user': user_id,
                        'water_meters__water_meter_type': type_id,
                        'water_meters__water_meter_type__water_meter_tag': tag_id,
                        'water_meters__water_meter_project': project_id,
                    }
                    if water_meters is not None:
                        filters['water_meters'] = water_meters
                    else:
                        filters['water_meters__in'] = middle_admin_water_meter
                    date_sum_value = {}
                    try:
                        # all consumptions per date
                        filters['create_time__gte'] = start_time
                        filters['create_time__lte'] = end_time
                        all_consumption_filters = {k: v for k, v in filters.items() if v is not None}
                        all_consumption = (
                            WaterMetersConsumptions.objects
                            .filter(**all_consumption_filters)
                            .annotate(date=TruncDate('create_time'))
                            .values('date')
                            .annotate(sum=Sum('value'))
                            .order_by('-date')[offset:offset + limit]
                        )
                        filters.pop('create_time__gte')
                        filters.pop('create_time__lte')
                        # cumulative consumptions until start date .
                        filters['create_time__lte'] = start_time
                        cumulative_filters = {k: v for k, v in filters.items() if v is not None}
                        cumulative_consumptions = WaterMetersConsumptions.objects.filter(
                            **cumulative_filters).aggregate(
                            Sum('value'))
                        date_sum_value['cumulative_consumptions'] = cumulative_consumptions['value__sum']
                        if len(all_consumption) == 0:
                            all_consumption = []
                            return True, all_consumption
                        count_check = 0
                        total_value = 0.0
                        for cons in all_consumption:
                            count_check += 1
                            date_sum_value[str(cons['date'])] = cons['sum']
                            total_value += cons['sum']
                        date_sum_value['total'] = total_value
                        date_sum_value['average'] = "{:.2f}".format(total_value / all_consumption.count())
                    except:
                        wrong_data_result["farsi_message"] = ""
                        wrong_data_result["english_message"] = "water_meter_serial or time input Error"
                    return True, date_sum_value
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_consumptions_by_date_for_chart_serializer(token, water_meters, start_time, end_time, user_id,
                                                                tag_id, project_id, type_id):
        """
            param : [token, water_meters, start_time, end_time, user_id,
                                                    tag_id, project_id, type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results. It returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            def consumption_results(all_consumption):
                consumptions_result = []
                for consumption in all_consumption:
                    consumption_info = {
                        "value": consumption.value,
                        "create_time": str(consumption.create_time),
                    }
                    consumptions_result.append(consumption_info)
                return consumptions_result

            if AdminsSerializer.admin_check_permission(admin_id, ['ViewProject', 'ViewDevice']):
                filters = {
                    'water_meters': water_meters,
                    'water_meters__water_meter_user': user_id,
                    'water_meters__water_meter_type': type_id,
                    'water_meters__water_meter_type__water_meter_tag': tag_id,
                    'water_meters__water_meter_project': project_id,
                    'create_time__gte': start_time,
                    'create_time__lte': end_time,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                all_consumption = WaterMetersConsumptions.objects.filter(**filters)
                all_consumption_paginated = all_consumption.order_by('-create_time')
                cons_results = consumption_results(all_consumption=all_consumption_paginated)
                return True, cons_results
            
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_projects_list = middle_admin.project_ids
                middle_admin_water_meters_values = WaterMeters.objects.filter(
                    water_meter_project__in=middle_admin_projects_list).values(
                    'water_meter_serial')
                middle_admin_water_meter = [wm['water_meter_serial'] for wm in middle_admin_water_meters_values]

                if water_meters is not None and water_meters not in middle_admin_water_meter:
                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                    wrong_data_result["english_message"] = "Wrong water_meter_serial"
                    return False, wrong_data_result

                filters = {
                    'water_meters__water_meter_user': user_id,
                    'water_meters__water_meter_type': type_id,
                    'water_meters__water_meter_type__water_meter_tag': tag_id,
                    'water_meters__water_meter_project': project_id,
                    'create_time__gte': start_time,
                    'create_time__lte': end_time,
                }

                if water_meters is not None:
                    filters['water_meters'] = water_meters
                else:
                    filters['water_meters__in'] = middle_admin_water_meter

                filters = {k: v for k, v in filters.items() if v is not None}
                all_consumption = WaterMetersConsumptions.objects.filter(**filters)
                all_consumption_paginated = all_consumption.order_by('-create_time')
                cons_results = consumption_results(all_consumption=all_consumption_paginated)
                return True, cons_results

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result


    @staticmethod
    def admin_get_all_consumptions_by_date__per_meter_serializer(token, water_meters_list, start_time,
                                                                 end_time):
        """
            param : [token, water_meters_list, start_time, end_time]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results. Returns false status along with an error message.
            """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, ['Reports']):
                result_data = {}
                for meter_id in water_meters_list:
                    filters = {
                        'water_meters__water_meter_serial': meter_id,
                        'create_time__gte': start_time,
                        'create_time__lte': end_time
                    }
                    try:
                        consumption_data = WaterMetersConsumptions.objects.filter(**filters).values(
                            'create_time__date').annotate(sum=Sum('value')).order_by('-create_time__date')
                        meter_consumption = {str(cons['create_time__date']): cons['sum'] for cons in consumption_data}
                        result_data[meter_id] = meter_consumption
                    except:
                        # Handle any exceptions here
                        result_data[meter_id] = {}
                return True, result_data
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_consumption_total_statistics_serializer(token):
        """
            param : [token]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Reports'):
                all_consumption = WaterMetersConsumptions.objects.all()
                # .annotate(Sum('price'))
                # .aggregate(Sum('price'))
                result = {
                    "all_consumptions": all_consumption.count()
                }
                all_tags = WaterMetersTags.objects.all()
                for tag in all_tags:
                    tag_consumptions = all_consumption.filter(
                        water_meters__water_meter_type__water_meter_tag_id=tag.water_meter_tag_id)
                    tag_count = tag_consumptions.count()
                    sum_of_all_tag_consumption = tag_consumptions.aggregate(Sum('value'))
                    result[tag.water_meter_tag_name] = {
                        "tag_count": tag_count,
                        "sum_of_all_tag_consumption": sum_of_all_tag_consumption['value__sum']

                    }
                return True, result
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager', 'Consumption']):
                middle_admin_projects = MiddleAdmins.objects.get(middle_admin_id=admin_id).project_ids
                all_consumption = WaterMetersConsumptions.objects.filter(
                    water_meters__water_meter_project__water_meter_project_id__in=middle_admin_projects)
                # all_consumption = WaterMetersConsumptions.f
                # .annotate(Sum('price'))
                # .aggregate(Sum('price'))
                result = {
                    "all_consumptions": all_consumption.count()
                }
                all_tags = WaterMetersTags.objects.all()
                for tag in all_tags:
                    tag_consumptions = all_consumption.filter(
                        water_meters__water_meter_type__water_meter_tag_id=tag.water_meter_tag_id)
                    tag_count = tag_consumptions.count()
                    sum_of_all_tag_consumption = tag_consumptions.aggregate(Sum('value'))
                    result[tag.water_meter_tag_name] = {
                        "tag_count": tag_count,
                        "sum_of_all_tag_consumption": sum_of_all_tag_consumption['value__sum']

                    }
                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_create_csv_file_overall_serializer(token, water_meter_project, water_meter_tag_id):
        """
            param : [token, water_meter_project, water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                # get water_meters
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_project=water_meter_project,
                                                              water_meter_type__water_meter_tag__water_meter_tag_id=water_meter_tag_id)
                except:
                    wrong_data_result["farsi_message"] = "داده های ورودی را چک کنید"
                    wrong_data_result["english_message"] = "Check the input data"
                    return False, wrong_data_result
                headers = ['پروژه', 'دسته بندی', 'شماره سریال', 'نام کنتور', 'بیشترین مقدار مصرف',
                           'تاریخ بیشترین مقدار مصرف', 'کمترین مقدار مصرف', 'تاریخ کمترین مقدار مصرف']
                prepared_data_list = []
                project_name = None
                tag_name = None
                for water_meter_obj in water_meters:
                    water_meter_as_dict = water_meter_obj.as_dict()
                    project_name = water_meter_as_dict['water_meter_project_info'][
                        'water_meter_project_name']
                    tag_name = water_meter_as_dict['water_meter_type_info']['water_meter_tag'][
                        'water_meter_tag_name']
                    # get consumptions
                    consumptions = WaterMetersConsumptions.objects.filter(
                        water_meters__water_meter_serial=water_meter_as_dict['water_meter_serial'])
                    # min and max in all time
                    total_max_value = consumptions.aggregate(Max('value'))
                    total_max_value_obj = consumptions.filter(value=total_max_value['value__max'])
                    total_max_value_obj = [max_cons.as_dict() for max_cons in total_max_value_obj][0]
                    total_max_value_time = total_max_value_obj['create_time']
                    # total_max_value_time_jalali
                    gregorian_max_value_time = total_max_value_time.date()
                    max_value_jalali_date = JalaliDate.to_jalali(gregorian_max_value_time.year,
                                                                 gregorian_max_value_time.month,
                                                                 gregorian_max_value_time.day)
                    # --- end max value ---
                    # min value
                    total_min_value = consumptions.aggregate(Min('value'))
                    total_min_value_obj = consumptions.filter(value=total_min_value['value__min'])
                    total_min_value_obj = [min_cons.as_dict() for min_cons in total_min_value_obj][0]
                    total_min_value_time = total_min_value_obj['create_time']
                    # total_min_value_time_jalali
                    gregorian_min_value_time = total_min_value_time.date()
                    min_value_jalali_date = JalaliDate.to_jalali(gregorian_min_value_time.year,
                                                                 gregorian_min_value_time.month,
                                                                 gregorian_min_value_time.day)
                    # ---end min value ---

                    # --- end min and max in all time ---

                    prepared_data = {
                        "پروژه": project_name,
                        "دسته بندی": tag_name,
                        "شماره سریال": water_meter_as_dict['water_meter_serial'],
                        "نام کنتور": water_meter_as_dict['water_meter_name'],
                        "بیشترین مقدار مصرف": total_max_value['value__max'],
                        "تاریخ بیشترین مقدار مصرف": max_value_jalali_date,
                        "کمترین مقدار مصرف": total_min_value['value__min'],
                        "تاریخ کمترین مقدار مصرف": min_value_jalali_date,
                    }
                    prepared_data_list.append(prepared_data)
                # create csv file directory
                # check for csv directory
                csv_files = os.path.exists(os.path.join(os.getcwd(), 'csv_files'))
                if csv_files is False:
                    os.mkdir(os.path.join(os.getcwd(), 'csv_files'))
                csv_files_path = os.path.join(os.getcwd(), 'csv_files')

                # get current time
                current_time = datetime.now()
                # current time to jalali
                current_time_jalali = JalaliDate.to_jalali(current_time.date().year, current_time.date().month,
                                                           current_time.date().day)
                csv_file_name = f"{current_time_jalali} -- {tag_name} -- {project_name}.csv"

                final_file_path = os.path.join(csv_files_path, csv_file_name)
                # create to scv file .
                with open(final_file_path, 'w', encoding="utf-8-sig") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(prepared_data_list)

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_create_csv_file_single_serializer(token, water_meter_project, water_meter_tag_id):
        """
            param : [token, water_meter_project, water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                # get water_meters
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_project=water_meter_project,
                                                              water_meter_type__water_meter_tag__water_meter_tag_id=water_meter_tag_id)
                except:
                    wrong_data_result["farsi_message"] = "داده های ورودی را چک کنید"
                    wrong_data_result["english_message"] = "Check the input data"
                    return False, wrong_data_result
                prepared_data_list = []
                headers = ['پروژه', 'دسته بندی', 'شماره سریال', 'نام کنتور', 'بیشترین مقدار مصرف روز جاری',
                           'کمترین مقدار مصرف روز جاری',
                           'بیشترین مقدار مصرف هفته جاری', 'کمترین مقدار مصرف هفته جاری', 'بیشترین مقدار مصرف ماه جاری',
                           'کمترین مقدار مصرف ماه جاری', 'بیشترین مقدار مصرف سال جاری', 'کمترین مقدار مصرف سال جاری']

                project_name = ""
                tag_name = ""

                # get time
                jalali_today = JalaliDate.today()

                # Jalali to Gregorian
                today_gregorian = JalaliDate(jalali_today).to_gregorian()

                # las week consumptions
                last_week_jalali_time = jalali_today - timedelta(days=7)
                last_week_gregorian_time = JalaliDate(last_week_jalali_time).to_gregorian()

                # first day of month time
                first_day_month = JalaliDate(jalali_today.year, jalali_today.month, 1).to_gregorian()
                # last day of month time
                if jalali_today.month <= 6:
                    last_day = 31
                else:
                    last_day = 30
                last_day_month = JalaliDate(jalali_today.year, jalali_today.month, last_day).to_gregorian()

                # first day of year
                first_day_year = JalaliDate(jalali_today.year, 1, 1).to_gregorian()

                # last day of year
                last_day_year = JalaliDate(jalali_today.year, 12, 29).to_gregorian()
                for water_meter_obj in water_meters:
                    water_meter_as_dict = water_meter_obj.as_dict()
                    water_meter_serial = water_meter_as_dict['water_meter_serial']

                    project_name = water_meter_as_dict['water_meter_project_info'][
                        'water_meter_project_name']
                    tag_name = water_meter_as_dict['water_meter_type_info']['water_meter_tag'][
                        'water_meter_tag_name']

                    # get all meter consumptions
                    consumptions = WaterMetersConsumptions.objects.filter(
                        water_meters__water_meter_serial=water_meter_serial)
                    # today consumptions
                    today_consumptions = consumptions.filter(create_time__day=today_gregorian.day,
                                                             create_time__month=today_gregorian.month,
                                                             create_time__year=today_gregorian.year)

                    max_today_value = today_consumptions.aggregate(Max('value'))
                    min_today_value = today_consumptions.aggregate(Min('value'))

                    # week consumptions
                    week_consumptions = consumptions.filter(create_time__gte=last_week_gregorian_time,
                                                            create_time__lte=today_gregorian)
                    max_week_value = week_consumptions.aggregate(Max('value'))
                    min_week_value = week_consumptions.aggregate(Min('value'))

                    # month consumptions
                    month_consumptions = consumptions.filter(create_time__gte=first_day_month,
                                                             create_time__lte=last_day_month)

                    month_max_value = month_consumptions.aggregate(Max('value'))
                    month_min_value = month_consumptions.aggregate(Min('value'))

                    # year consumptions
                    year_consumptions = consumptions.filter(create_time__gte=first_day_year,
                                                            create_time__lte=last_day_year)
                    year_max_value = year_consumptions.aggregate(Max('value'))
                    year_min_value = year_consumptions.aggregate(Min('value'))

                    prepared_data = {
                        "پروژه": project_name,
                        "دسته بندی": tag_name,
                        "شماره سریال": water_meter_as_dict['water_meter_serial'],
                        "نام کنتور": water_meter_as_dict['water_meter_name'],
                        "بیشترین مقدار مصرف روز جاری": max_today_value['value__max'],
                        "کمترین مقدار مصرف روز جاری": min_today_value['value__min'],
                        "بیشترین مقدار مصرف هفته جاری": max_week_value['value__max'],
                        "کمترین مقدار مصرف هفته جاری": min_week_value['value__min'],
                        "بیشترین مقدار مصرف ماه جاری": month_max_value['value__max'],
                        "کمترین مقدار مصرف ماه جاری": month_min_value['value__min'],
                        "بیشترین مقدار مصرف سال جاری": year_max_value['value__max'],
                        "کمترین مقدار مصرف سال جاری": year_min_value['value__min'],

                    }
                    prepared_data_list.append(prepared_data)
                # check for csv directory
                csv_files = os.path.exists(os.path.join(os.getcwd(), 'csv_files'))
                if csv_files is False:
                    os.mkdir(os.path.join(os.getcwd(), 'csv_files'))
                csv_files_path = os.path.join(os.getcwd(), 'csv_files')
                csv_file_single = os.path.exists(os.path.join(csv_files_path, 'csv_file_single'))
                if csv_file_single is False:
                    os.mkdir(os.path.join(csv_files_path, 'csv_file_single'))
                csv_files_path = os.path.join(os.getcwd(), 'csv_files', 'csv_file_single')
                csv_file_name = f"{jalali_today} -- {tag_name} -- {project_name}.csv"
                final_file_path = os.path.join(csv_files_path, csv_file_name)
                # create to csv file .
                with open(final_file_path, 'w', encoding="utf-8-sig") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(prepared_data_list)
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_create_csv_file_all_serializer(token, water_meter_project, water_meter_tag_id):
        """
            param : [token, water_meter_project, water_meter_tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            # TODO: Check again
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                # get water_meters
                try:
                    filters = {
                        "water_meter_project": water_meter_project,
                        "water_meter_type__water_meter_tag__water_meter_tag_id": water_meter_tag_id
                    }
                    filters = {k: v for k, v in filters.items() if v is not None}
                    water_meters = WaterMeters.objects.filter(**filters)
                except:
                    wrong_data_result["farsi_message"] = "داده های ورودی را چک کنید"
                    wrong_data_result["english_message"] = "Check the input data"
                    return False, wrong_data_result
                #
                # get project and tag name
                project_name = water_meters[0].water_meter_project.water_meter_project_name
                tag_name = water_meters[0].water_meter_type.water_meter_tag.water_meter_tag_name

                # # get jalali today
                jalali_today = JalaliDate.today()

                # get all consumptions
                consumptions = WaterMetersConsumptions.objects.filter(water_meters__in=water_meters) \
                    .order_by('water_meters', '-value')

                consumptions_values = consumptions.values(
                    دسته=F('water_meters__water_meter_type__water_meter_tag__water_meter_tag_name'),
                    سریال=F('water_meters__water_meter_serial'), نام=F('water_meters__water_meter_name'),
                    مصرف=F('value'), روز=F('create_time__day'), ماه=F('create_time__month')
                    , سال=F('create_time__year'))

                headers = ['دسته', 'سریال', 'نام', 'مصرف', 'روز', 'ماه', 'سال']
                # check for csv directory
                csv_files = os.path.exists(os.path.join(os.getcwd(), 'csv_files'))
                if csv_files is False:
                    os.mkdir(os.path.join(os.getcwd(), 'csv_files'))
                csv_files_path = os.path.join(os.getcwd(), 'csv_files')
                csv_file_all = os.path.exists(os.path.join(csv_files_path, 'csv_file_all'))
                if csv_file_all is False:
                    os.mkdir(os.path.join(csv_files_path, 'csv_file_all'))
                csv_files_path = os.path.join(os.getcwd(), 'csv_files', 'csv_file_all')
                if water_meter_tag_id is None:
                    tag_name = 'جامع'
                csv_file_name = f"{jalali_today} -- {tag_name} -- {project_name}.csv"
                final_file_path = os.path.join(csv_files_path, csv_file_name)
                # create to csv file .
                with open(final_file_path, 'w', encoding="utf-8-sig") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(consumptions_values)

                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_csv_file_serializer(token, water_meter_serial, start_time, end_time):
        """
            param : [token, water_meter_serial, start_time, end_time]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'ViewDevice'):
                # consumptions
                filters = {
                    "water_meters": water_meter_serial,
                    "create_time__gte": start_time,
                    "create_time__lte": end_time
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                consumption_objects = WaterMetersConsumptions.objects.filter(**filters)
                consumption_objects_count = consumption_objects.count()
                if consumption_objects_count == 0:
                    wrong_data_result["farsi_message"] = "هیچ مقدار مصرفی در بازه ی مورد نظر وجود ندارد"
                    wrong_data_result["english_message"] = "There is no consumption amount in the desired range"
                    return False, wrong_data_result

                prepared_data_list = []
                headers = ['شماره سریال', 'تاریخ', 'ساعت', 'مقدار مصرف','مقدار مصرف تجمعی']

                base_dir = os.getcwd()
                csv_file_root = os.path.join(base_dir, 'media', 'csv', 'detail')

                for cons_obj in consumption_objects:
                    value = cons_obj.value
                    create_time = cons_obj.create_time
                    cumulative_value = cons_obj.cumulative_value
                    jalali_time = JalaliDateTime.fromtimestamp(create_time.timestamp(), pytz.timezone("Asia/Tehran"))
                    jalali_time_split = str(jalali_time).split(' ')
                    jalali_date = jalali_time_split[0]
                    jalali_time = jalali_time_split[1].split('.')[0]
                    # create csv file
                    prepared_data = {
                        "شماره سریال": water_meter_serial,

                        "تاریخ": jalali_date,
                        "ساعت": jalali_time,
                        "مقدار مصرف": value,
                        "مقدار مصرف تجمعی": cumulative_value
                    }

                    csv_file_path = os.path.join(csv_file_root, f'{water_meter_serial}.csv')
                    # check file exist
                    csv_checker = os.path.exists(csv_file_path)
                    if csv_checker is True:
                        os.remove(csv_file_path)

                    prepared_data_list.append(prepared_data)
                    # create to csv file .
                    with open(csv_file_path, 'w', encoding="utf-8-sig") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=headers)
                        writer.writeheader()
                        writer.writerows(prepared_data_list)
                download_link = f'/media/csv/detail/{water_meter_serial}.csv'
                result = {
                    "fileurl": download_link
                }
            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_update_sum_value_serializer(token, meter_list):
        """
            param : [token, meter_list]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, ''):
                # check for each meter serial in list .
                meter_not_valid = []
                res_dict = {}
                for meter_serial in meter_list:
                    try:
                        meter_object = WaterMeters.objects.get(water_meter_serial=meter_serial)
                        # get meter consumption
                        consumption_object = WaterMetersConsumptions.objects.filter(water_meters=meter_object)
                        consumption_object_sort = consumption_object.order_by('create_time')
                        get_last = consumption_object_sort.last()
                        meter_sum_value = get_last.sum_all_value
                        cumulative = get_last.cumulative_value
                        new_sum_value = consumption_object.aggregate(Sum('value'))
                        new_sum_value = new_sum_value['value__sum']
                        # comparison
                        if cumulative != new_sum_value:
                            if cumulative > new_sum_value:
                                difference = cumulative - new_sum_value
                            elif cumulative < new_sum_value:
                                difference = new_sum_value - cumulative
                            # first consumption
                            first_consumption = consumption_object_sort.first()
                            first_consumption_value = first_consumption.value
                            new_first_value = first_consumption_value + difference
                            WaterMetersConsumptions.objects.filter(
                                consumption_id=first_consumption.consumption_id,
                                water_meters=first_consumption.water_meters).update(value=new_first_value)
                            # update sum_value
                            final_sum_value = new_sum_value + difference
                            WaterMetersConsumptions.objects.filter(water_meters=meter_object).update(
                                sum_all_value=final_sum_value)

                    except:
                        meter_not_valid.append(meter_serial)
                if len(meter_not_valid) != 0:
                    wrong_data_result["farsi_message"] = f"مقادیر موجود در لیست یافت نشد : {meter_not_valid}"
                    wrong_data_result["english_message"] = f"The values in the list were not found : {meter_not_valid}"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_consumptions_by_date_app_serializer(token, page, count, water_meters, start_time, end_time,
                                                          user_id,
                                                          tag_id, project_id, type_id):
        """
            param : [token, page, count, water_meters, start_time, end_time,user_id,tag_id, project_id, type_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, 'ViewDevice'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)

                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        'water_meters': water_meters,
                        'water_meters__water_meter_user': user_id,
                        'water_meters__water_meter_type': type_id,
                        'water_meters__water_meter_type__water_meter_tag': tag_id,
                        'water_meters__water_meter_project': project_id,
                    }
                    date_sum_value = {}

                    # all consumptions per date
                    try:
                        filters['create_time__gte'] = start_time
                        filters['create_time__lte'] = end_time
                        all_consumption_filters = {k: v for k, v in filters.items() if v is not None}
                        all_consumption = WaterMetersConsumptions.objects.filter(**all_consumption_filters).values(
                            'create_time__date').annotate(
                            sum=Sum('value')).order_by(
                            '-create_time__date')[
                                          offset:offset + limit]
                        filters.pop('create_time__gte')
                        filters.pop('create_time__lte')
                        # cumulative consumptions until start date .
                        filters['create_time__lte'] = start_time
                        cumulative_filters = {k: v for k, v in filters.items() if v is not None}
                        cumulative_consumptions = WaterMetersConsumptions.objects.filter(
                            **cumulative_filters).aggregate(
                            Sum('value'))
                        date_sum_value['cumulative_consumptions'] = cumulative_consumptions['value__sum']

                        if len(all_consumption) == 0:
                            all_consumption = {}
                            return True, all_consumption
                        count_check = 0
                        total_value = 0.0
                        for cons in all_consumption:
                            count_check += 1
                            date_sum_value[str(cons['create_time__date'])] = cons['sum']
                            total_value += cons['sum']
                        date_sum_value['total'] = total_value
                        date_sum_value['average'] = "{:.2f}".format(total_value / all_consumption.count())
                        response = {}
                        date_list = []
                        for value in date_sum_value:
                            res = {"date": "", "value": ""}
                            if value != 'cumulative_consumptions' and value != 'total' and value != 'average':
                                res['date'] = value
                                res['value'] = date_sum_value[value]
                                date_list.append(res)
                        response['cumulative_consumptions'] = date_sum_value['cumulative_consumptions']
                        response['total'] = date_sum_value['total']
                        response['average'] = date_sum_value['average']
                        response['consumption_list'] = date_list

                    except:
                        wrong_data_result["farsi_message"] = ""
                        wrong_data_result["english_message"] = "water_meter_serial or time input Error"
                    return True, response
                else:
                    return field_result
            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['Middle', 'Consumption']):
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                # middle_admin_water_meters = middle_admin.water_meter_ids
                middle_admin_project_ids = middle_admin.project_ids
                middle_admin_projects_list = middle_admin.project_ids
                middle_admin_water_meters_values = WaterMeters.objects.filter(
                    water_meter_project__in=middle_admin_projects_list).values(
                    'water_meter_serial')
                middle_admin_water_meter = []
                for water_serial in middle_admin_water_meters_values:
                    middle_admin_water_meter.append(water_serial['water_meter_serial'])
                if water_meters is not None:
                    if water_meters not in middle_admin_water_meter:
                        wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                        wrong_data_result["english_message"] = "Wrong water_meter_serial"
                        return False, wrong_data_result

                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters = {
                        # 'water_meters': water_meters,
                        'water_meters__water_meter_user': user_id,
                        'water_meters__water_meter_type': type_id,
                        'water_meters__water_meter_type__water_meter_tag': tag_id,
                        'water_meters__water_meter_project': project_id,
                    }
                    if water_meters is not None:
                        filters['water_meters'] = water_meters
                    else:
                        filters['water_meters__in'] = middle_admin_water_meter
                    date_sum_value = {}
                    try:
                        # all consumptions per date
                        filters['create_time__gte'] = start_time
                        filters['create_time__lte'] = end_time
                        all_consumption_filters = {k: v for k, v in filters.items() if v is not None}
                        all_consumption = WaterMetersConsumptions.objects.filter(**all_consumption_filters).values(
                            'create_time__date').annotate(
                            sum=Sum('value')).order_by(
                            '-create_time__date')[
                                          offset:offset + limit]
                        filters.pop('create_time__gte')
                        filters.pop('create_time__lte')
                        # cumulative consumptions until start date .
                        filters['create_time__lte'] = start_time
                        cumulative_filters = {k: v for k, v in filters.items() if v is not None}
                        cumulative_consumptions = WaterMetersConsumptions.objects.filter(
                            **cumulative_filters).aggregate(
                            Sum('value'))
                        date_sum_value['cumulative_consumptions'] = cumulative_consumptions['value__sum']
                        if len(all_consumption) == 0:
                            all_consumption = {}
                            return True, all_consumption
                        count_check = 0
                        total_value = 0.0
                        for cons in all_consumption:
                            count_check += 1
                            date_sum_value[str(cons['create_time__date'])] = cons['sum']
                            total_value += cons['sum']
                        date_sum_value['total'] = total_value
                        date_sum_value['average'] = "{:.2f}".format(total_value / all_consumption.count())
                        response = {}
                        date_list = []
                        for value in date_sum_value:
                            res = {"date": "", "value": ""}
                            if value != 'cumulative_consumptions' and value != 'total' and value != 'average':
                                res['date'] = value
                                res['value'] = date_sum_value[value]
                                date_list.append(res)
                        response['cumulative_consumptions'] = date_sum_value['cumulative_consumptions']
                        response['total'] = date_sum_value['total']
                        response['average'] = date_sum_value['average']
                        response['consumption_list'] = date_list
                    except:
                        wrong_data_result["farsi_message"] = ""
                        wrong_data_result["english_message"] = "water_meter_serial or time input Error"

                    return True, response
                else:
                    return field_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def v2_admin_get_cumulative_consumptions_serializer(token, page, count, user_id, project_id, water_meter_serial,
                                                        water_meter_tag, sort_value, input_reverse):
        """
            param : [token, page, count, user_id, project_id, water_meter_serial,water_meter_tag, sort_value,
                        input_reverse]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            def _sorting_records(sort_value, water_meters, input_reverse):
                consumption_records = WaterMetersConsumptions.objects.filter(water_meters__in=water_meters)
                # meter_ids = consumption_records.values_list('water_meters__water_meter_serial').distinct()
                meter_ids = all_water_meter_query.values_list('water_meter_serial').distinct()
                current_time_jalali = JalaliDate.today()
                j_2_g = str(current_time_jalali).split('-')
                jalali_to_gregorian = JalaliDate(int(j_2_g[0]), int(j_2_g[1]), int(j_2_g[2])).to_gregorian()
                first_day_in_month = JalaliDate(int(j_2_g[0]), int(j_2_g[1]), 1).to_gregorian()
                last_day_in_month = JalaliDate(int(j_2_g[0]), int(j_2_g[1]), 29).to_gregorian()
                first_day_year = JalaliDate(int(j_2_g[0]), 1, 1).to_gregorian()
                last_day_year = JalaliDate(int(j_2_g[0]), 12, 29).to_gregorian()
                day_cons = consumption_records.filter(create_time=jalali_to_gregorian)
                month_cons = consumption_records.filter(create_time__gte=first_day_in_month,
                                                        create_time__lte=last_day_in_month)
                year_cons = consumption_records.filter(create_time__gte=first_day_year,
                                                       create_time__lte=last_day_year)
                structure = {}
                for meter_id in meter_ids:
                    meter_id = meter_id[0]
                    if meter_id not in structure.keys():
                        last_query = consumption_records.filter(water_meters__water_meter_serial=meter_id).order_by(
                            'create_time').last()

                        # last_query_serialize = WaterMetersConsumptions.objects.serialize(queryset=last_query)
                        year = year_cons.filter(water_meters__water_meter_serial=meter_id).aggregate(
                            Sum('value'))['value__sum']
                        month = month_cons.filter(water_meters__water_meter_serial=meter_id).aggregate(
                            Sum('value'))['value__sum']
                        day = day_cons.filter(water_meters__water_meter_serial=meter_id).aggregate(
                            Sum('value'))['value__sum']
                        structure[meter_id] = {
                            'cumulative_consumptions': {
                                "year": [year, j_2_g[0]],
                                "month": [month, j_2_g[1]],
                                "day": [day, j_2_g[2]],
                            }}
                        if last_query is not None:
                            last_bill_created_time = Bills.objects.filter(
                                bill_water_meter=last_query.water_meters).order_by(
                                'bill_create_date').last()
                            structure[meter_id]['last_consumption'] = {
                                "consumption_id": last_query.consumption_id,
                                "create_time": last_query.create_time,
                                "value": last_query.value,
                                "cumulative_value": last_query.cumulative_value,
                                "sum_all_value": last_query.sum_all_value,
                                "information": last_query.information,
                                "from_previous_record": last_query.from_previous_record,
                                "to_current_record": last_query.to_current_record,
                                "bill_created": last_query.bill_created,
                            }
                            if last_bill_created_time is not None:
                                structure[meter_id]['last_consumption'][
                                    'last_bill_created_time'] = last_bill_created_time.bill_create_date
                            else:
                                structure[meter_id]['last_consumption']['last_bill_created_time'] = None


                        elif last_query is None:
                            structure[meter_id]['last_consumption'] = None

                if sort_value == 'year':
                    if input_reverse:
                        result = list(map(list, sorted(structure.items(),
                                                       key=lambda x: x[1]['cumulative_consumptions']['year'][0] if
                                                       x[1]['cumulative_consumptions']['year'][
                                                           0] is not None else float(
                                                           'inf'), reverse=True)))
                    else:
                        result = list(map(list, sorted(structure.items(),
                                                       key=lambda x: x[1]['cumulative_consumptions']['year'][0] if
                                                       x[1]['cumulative_consumptions']['year'][
                                                           0] is not None else float(
                                                           'inf'), reverse=False)))

                elif sort_value == 'month':
                    if input_reverse:
                        result = list(map(list, sorted(structure.items(),
                                                       key=lambda x: x[1]['cumulative_consumptions']['month'][0] if
                                                       x[1]['cumulative_consumptions']['month'][
                                                           0] is not None else float(
                                                           'inf'), reverse=True)))
                    else:
                        result = list(map(list, sorted(structure.items(),
                                                       key=lambda x: x[1]['cumulative_consumptions']['month'][0] if
                                                       x[1]['cumulative_consumptions']['month'][
                                                           0] is not None else float(
                                                           'inf'), reverse=False)))
                elif sort_value == 'day':
                    if input_reverse:
                        result = list(map(list, sorted(structure.items(),
                                                       key=lambda x: x[1]['cumulative_consumptions']['day'][1] if
                                                       x[1]['cumulative_consumptions']['day'][0] is not None else float(
                                                           'inf'), reverse=True)))
                    else:
                        result = list(map(list, sorted(structure.items(),
                                                       key=lambda x: x[1]['cumulative_consumptions']['day'][1] if
                                                       x[1]['cumulative_consumptions']['day'][0] is not None else float(
                                                           'inf'), reverse=False)))
                elif sort_value == 'last_consumption_value':
                    if input_reverse:
                        result = list(
                            map(list, sorted(structure.items(), key=lambda x: x[1]['last_consumption']['value']
                            if x[1]['last_consumption'] is not None else float('inf'), reverse=True)))
                    else:
                        result = list(
                            map(list, sorted(structure.items(), key=lambda x: x[1]['last_consumption']['value']
                            if x[1]['last_consumption'] is not None else float('inf'), reverse=False)))

                elif sort_value == 'last_cons_object_create_time':
                    if input_reverse:
                        result = list(
                            map(list, sorted(structure.items(), key=lambda x: x[1]['last_consumption']['create_time']
                            if x[1]['last_consumption'] is not None else datetime.max.replace(tzinfo=pytz.utc),
                                             reverse=True)))
                    else:
                        result = list(
                            map(list, sorted(structure.items(), key=lambda x: x[1]['last_consumption']['create_time']
                            if x[1]['last_consumption'] is not None else datetime.max.replace(tzinfo=pytz.utc),
                                             reverse=False)))

                for itm in result:
                    if itm[1]['last_consumption'] is not None:
                        itm[1]['last_consumption']['create_time'] = str(itm[1]['last_consumption']['create_time'])
                        itm[1]['last_consumption']['last_bill_created_time'] = str(
                            itm[1]['last_consumption']['last_bill_created_time'])

                return result

            if AdminsSerializer.admin_check_permission(admin_id, 'ViewProject'):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    filters_test = {
                        'water_meter_serial': water_meter_serial,
                        'water_meter_user__user_id': user_id,
                        'water_meter_project__water_meter_project_id': project_id,
                        'water_meter_type__water_meter_tag__water_meter_tag_id': water_meter_tag
                    }
                    filters = {k: v for k, v in filters_test.items() if v is not None}
                    all_water_meter_query = WaterMeters.objects.filter(**filters)
                    result = _sorting_records(input_reverse=input_reverse, sort_value=sort_value,
                                              water_meters=all_water_meter_query)[
                             offset:offset + limit]
                    return True, result
                else:
                    return field_result

            # TODO: Remove This Section
            elif AdminsSerializer.admin_check_permission(admin_id, ['ProjectManager']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                middle_admin = MiddleAdmins.objects.get(middle_admin_id=admin_id)
                middle_admin_projects = middle_admin.project_ids
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)

                    filters = {
                        'water_meter_user__user_id': user_id,
                        'water_meter_type__water_meter_tag__water_meter_tag_id': water_meter_tag
                    }

                    if project_id is None:
                        filters['water_meter_project__in'] = middle_admin_projects
                    elif project_id is not None and project_id not in middle_admin_projects:
                        wrong_data_result["farsi_message"] = "project_id در میان ای دی ‌های پروژه مدیریت نیست"
                        wrong_data_result["english_message"] = "project_id it is not among the admin project IDs"
                        return False, wrong_data_result
                    else:
                        filters['water_meter_project__water_meter_project_id'] = project_id
                    filters = {k: v for k, v in filters.items() if v is not None}
                    filters = {k: v for k, v in filters.items() if v is not None}
                    all_water_meter_query = WaterMeters.objects.filter(**filters)
                    result = _sorting_records(input_reverse=input_reverse, sort_value=sort_value,
                                              water_meters=all_water_meter_query)[
                             offset:offset + limit]
                    return True, result
                else:
                    return field_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    # -----------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------- UserSerializers -----------------------------------------------
    @staticmethod
    def user_get_all_consumptions_serializer(token, page, count, water_meters, water_meter_project, water_meter_type,
                                             start_time, end_time):
        """
            param : [token, page, count, water_meters, water_meter_project, water_meter_type,
                                     start_time, end_time]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                "page": (page, int),
                "count": (count, int),
            }
            field_result = wrong_result(fields)

            def consumption_results(all_consumption):
                consumptions_result = []
                for consumption in all_consumption:
                    if consumption.from_previous_record == None:
                        from_previous_record = ""
                    else:
                        from_previous_record = consumption.from_previous_record
                    if consumption.to_current_record == None:
                        to_current_record = ""
                    else:
                        to_current_record = consumption.to_current_record
                    consumption_info = {
                        "consumption_id": consumption.consumption_id,
                        "value": consumption.value,
                        "create_time": consumption.create_time,
                        "information": consumption.information,
                        "from_previous_record": from_previous_record,
                        "to_current_record": to_current_record,
                        "bill_created": consumption.bill_created,
                        "water_meters_info": {
                            "water_meter_serial": consumption.water_meters.water_meter_serial,
                            "water_meter_name": consumption.water_meters.water_meter_name,
                            "water_meter_condition": consumption.water_meters.water_meter_condition,
                            "water_meter_validation": consumption.water_meters.water_meter_validation,
                            "water_meter_activation": consumption.water_meters.water_meter_activation,
                            "water_meter_create_date": consumption.water_meters.water_meter_create_date,
                            "other_information": consumption.water_meters.other_information,
                        },
                        # "user_info": {
                        #     "user_name": consumption.water_meters.water_meter_user.user_name,
                        #     "user_lastname": consumption.water_meters.water_meter_user.user_lastname,
                        #     "user_phone": consumption.water_meters.water_meter_user.user_phone,
                        #     "user_id": consumption.water_meters.water_meter_user.user_id,
                        # },
                        # "project_info": {
                        #     "water_meter_project_id": consumption.water_meters.water_meter_project.water_meter_project_id,
                        #     "water_meter_project_name": consumption.water_meters.water_meter_project.water_meter_project_name,
                        #     "water_meter_project_title": consumption.water_meters.water_meter_project.water_meter_project_title,
                        #     "water_meter_project_create_date": consumption.water_meters.water_meter_project.water_meter_project_create_date,
                        # },
                        "type_info": {
                            "water_meter_type_id": consumption.water_meters.water_meter_type.water_meter_type_id,
                            "water_meter_type_name": consumption.water_meters.water_meter_type.water_meter_type_name,
                            "water_meter_type_create_date": consumption.water_meters.water_meter_type.water_meter_type_create_date,
                        },
                        "tag_info": {
                            "water_meter_tag_id": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_id,
                            "water_meter_tag_name": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_name,
                            "water_meter_tag_create_date": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_create_date,
                        },
                        "all_consumptions": len(all_consumption),
                    }
                    if consumption.water_meters.water_meter_user != None:
                        consumption_info['user_info'] = {
                            "user_name": consumption.water_meters.water_meter_user.user_name,
                            "user_lastname": consumption.water_meters.water_meter_user.user_lastname,
                            "user_phone": consumption.water_meters.water_meter_user.user_phone,
                            "user_id": consumption.water_meters.water_meter_user.user_id,
                        }
                    else:
                        consumption_info['user_info'] = "user is null"
                    if consumption.water_meters.water_meter_project != None:
                        consumption_info['project_info'] = {
                            "water_meter_project_id": consumption.water_meters.water_meter_project.water_meter_project_id,
                            "water_meter_project_name": consumption.water_meters.water_meter_project.water_meter_project_name,
                            "water_meter_project_title": consumption.water_meters.water_meter_project.water_meter_project_title,
                            "water_meter_project_create_date": consumption.water_meters.water_meter_project.water_meter_project_create_date,
                        }
                    else:
                        consumption_info['project_info'] = "project is null"
                    consumptions_result.append(consumption_info)
                return consumptions_result

            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                try:
                    user = Users.objects.get(user_id=user_id)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است user_id"
                    wrong_data_result["english_message"] = "Wrong user_id"
                    return False, wrong_data_result
                search_list = [water_meters, water_meter_project, water_meter_type]
                counter = 0
                for param in search_list:
                    counter += 1
                    if param != None:
                        index_param = search_list.index(param)
                        if index_param == 0:
                            if start_time == None and end_time == None:
                                all_consumption = WaterMetersConsumptions.objects.filter(
                                    water_meters__water_meter_user=user_id,
                                    water_meters=search_list[index_param]).order_by('-create_time')[
                                                  offset:offset + limit]
                            else:
                                all_consumption = WaterMetersConsumptions.objects.filter(
                                    water_meters__water_meter_user=user_id,
                                    water_meters=search_list[index_param]).filter(
                                    create_time__gte=start_time, create_time__lte=end_time).order_by(
                                    '-create_time')[
                                                  offset:offset + limit]
                            if len(all_consumption) == 0:
                                all_consumption = []
                                return True, all_consumption
                            cons_results = consumption_results(all_consumption=all_consumption)
                            return True, cons_results
                        elif index_param == 1:
                            if start_time == None and end_time == None:
                                try:
                                    all_consumption = WaterMetersConsumptions.objects.filter(
                                        water_meters__water_meter_user=user_id,
                                        water_meters__water_meter_project=search_list[index_param]).order_by(
                                        '-create_time')[
                                                      offset:offset + limit]
                                    if len(all_consumption) == 0:
                                        all_consumption = []
                                        return True, all_consumption
                                except:
                                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_project"
                                    wrong_data_result["english_message"] = "Wrong water_meter_project"
                                    return False, wrong_data_result
                            else:
                                try:
                                    all_consumption = WaterMetersConsumptions.objects.filter(
                                        water_meters__water_meter_user=user_id,
                                        water_meters__water_meter_project=search_list[index_param]).filter(
                                        create_time__gte=start_time, create_time__lte=end_time
                                    ).order_by(
                                        '-create_time')[
                                                      offset:offset + limit]
                                    if len(all_consumption) == 0:
                                        all_consumption = []
                                        return True, all_consumption
                                except:
                                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_project"
                                    wrong_data_result["english_message"] = "Wrong water_meter_project"
                                    return False, wrong_data_result
                            cons_results = consumption_results(all_consumption=all_consumption)
                            return True, cons_results
                        elif index_param == 2:
                            if start_time == None and end_time == None:
                                try:
                                    all_consumption = WaterMetersConsumptions.objects.filter(
                                        water_meters__water_meter_user=user_id,
                                        water_meters__water_meter_type=search_list[index_param]).order_by(
                                        '-create_time')[
                                                      offset:offset + limit]
                                    if len(all_consumption) == 0:
                                        all_consumption = []
                                        return True, all_consumption
                                except:
                                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_type"
                                    wrong_data_result["english_message"] = "Wrong water_meter_type"
                                    return False, wrong_data_result
                            else:
                                try:
                                    all_consumption = WaterMetersConsumptions.objects.filter(
                                        water_meters__water_meter_user=user_id,
                                        water_meters__water_meter_type=search_list[index_param]).filter(
                                        create_time__gte=start_time, create_time__lte=end_time
                                    ).order_by(
                                        '-create_time')[
                                                      offset:offset + limit]
                                    if len(all_consumption) == 0:
                                        all_consumption = []
                                        return True, all_consumption
                                except:
                                    wrong_data_result["farsi_message"] = "اشتباه است water_meter_type"
                                    wrong_data_result["english_message"] = "Wrong water_meter_type"
                                    return False, wrong_data_result
                            cons_results = consumption_results(all_consumption=all_consumption)
                            return True, cons_results
                    elif param == None and counter == 3:
                        if start_time == None and end_time == None:
                            all_consumption = WaterMetersConsumptions.objects.filter(
                                water_meters__water_meter_user=user_id).order_by('-create_time')[
                                              offset:offset + limit]

                            if len(all_consumption) == 0:
                                all_consumption = []
                                return True, all_consumption
                        else:
                            try:
                                all_consumption = WaterMetersConsumptions.objects.filter(
                                    water_meters__water_meter_user=user_id,
                                    create_time__gte=start_time, create_time__lte=end_time).order_by(
                                    '-create_time')[
                                                  offset:offset + limit]
                                if len(all_consumption) == 0:
                                    all_consumption = []
                                    return True, all_consumption
                            except:
                                wrong_data_result["farsi_message"] = "فرمت تایم ارسالی اشتباه است"
                                wrong_data_result["english_message"] = "The time format sent is wrong"
                                return False, wrong_data_result

                        cons_results = consumption_results(all_consumption=all_consumption)
                        return True, cons_results
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_consumptions_by_date_serializer(token, page, count, water_meters, start_time, end_time,
                                                     project_id, type_id, tag_id):
        """
            param : [token, page, count, water_meters, start_time, end_time,
                                                     project_id, type_id, tag_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                "page": (page, int),
                "count": (count, int),
            }
            field_result = wrong_result(fields)

            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    'water_meters': water_meters,
                    'water_meters__water_meter_user': user_id,
                    'water_meters__water_meter_type': type_id,
                    'water_meters__water_meter_type__water_meter_tag': tag_id,
                    'water_meters__water_meter_project': project_id,
                    'create_time__gte': start_time,
                    'create_time__lte': end_time,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                date_sum_value = {}
                try:
                    # all consumptions per date
                    filters['create_time__gte'] = start_time
                    filters['create_time__lte'] = end_time
                    all_consumption_filters = {k: v for k, v in filters.items() if v is not None}
                    all_consumption = WaterMetersConsumptions.objects.filter(**all_consumption_filters).values(
                        'create_time__date').annotate(
                        sum=Sum('value')).order_by(
                        '-create_time__date')[
                                      offset:offset + limit]
                    filters.pop('create_time__gte')
                    filters.pop('create_time__lte')
                    # cumulative consumptions until start date .
                    filters['create_time__lte'] = start_time
                    cumulative_filters = {k: v for k, v in filters.items() if v is not None}
                    cumulative_consumptions = WaterMetersConsumptions.objects.filter(
                        **cumulative_filters).aggregate(
                        Sum('value'))
                    date_sum_value['cumulative_consumptions'] = cumulative_consumptions['value__sum']
                    if len(all_consumption) == 0:
                        all_consumption = {}
                        return True, all_consumption
                    count_check = 0
                    total_value = 0.0
                    for cons in all_consumption:
                        count_check += 1
                        date_sum_value[str(cons['create_time__date'])] = cons['sum']
                        total_value += cons['sum']
                    date_sum_value['total'] = total_value
                    date_sum_value['average'] = "{:.2f}".format(total_value / all_consumption.count())
                    response = {}
                    date_list = []
                    for value in date_sum_value:
                        res = {"date": "", "value": ""}
                        if value != 'cumulative_consumptions' and value != 'total' and value != 'average':
                            res['date'] = value
                            res['value'] = date_sum_value[value]
                            date_list.append(res)
                    response['cumulative_consumptions'] = date_sum_value['cumulative_consumptions']
                    response['total'] = date_sum_value['total']
                    response['average'] = date_sum_value['average']
                    response['consumption_list'] = date_list
                except:
                    wrong_data_result["farsi_message"] = ""
                    wrong_data_result["english_message"] = "water_meter_serial or time input Error"
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_last_consumption_data_by_water_meter_serializer(token, water_meter_serial):
        """
            param : [token, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            try:
                water_meter = WaterMeters.objects.filter(water_meter_serial=water_meter_serial,
                                                         water_meter_user=user_id)
                waterMeter = [w.as_dict() for w in water_meter]
                consumption = WaterMetersConsumptions.objects.filter(
                    water_meters=waterMeter[0]['water_meter_serial']).order_by(
                    'create_time').last()
            except:
                wrong_data_result["farsi_message"] = "اشتباه است water_meter_serial"
                wrong_data_result["english_message"] = "Wrong water_meter_serial"
                return False, wrong_data_result
            consumption = consumption.as_dict()
            consumption.update({
                'water_meters': consumption['water_meters']['water_meter_serial']
            })
            consumption.pop('consumption_id')
            test = {
                "Message": "Test"
            }
            return True, consumption
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_consumptions_view_serializer(token, consumption_id):
        """
            param : [token, consumption_id]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                consumption = WaterMetersConsumptions.objects.get(consumption_id=consumption_id)
            except:
                wrong_data_result["farsi_message"] = "اشتباه است consumption_id"
                wrong_data_result["english_message"] = "Wrong consumption_id"
                return False, wrong_data_result
            if consumption.from_previous_record == None:
                from_previous_record = ""
            else:
                from_previous_record = consumption.from_previous_record
            if consumption.to_current_record == None:
                to_current_record = ""
            else:
                to_current_record = consumption.to_current_record
            consumption_result = {
                "consumption_id": consumption.consumption_id,
                "create_time": consumption.create_time,
                "value": consumption.value,
                "information": consumption.value,
                "from_previous_record": from_previous_record,
                "to_current_record": to_current_record,
                "bill_created": consumption.bill_created,
                "water_meters": consumption.water_meters.water_meter_serial,
                "water_meter_info": {
                    "water_meter_name": consumption.water_meters.water_meter_name,
                    "water_meter_activation": consumption.water_meters.water_meter_activation,
                    "water_meter_validation": consumption.water_meters.water_meter_validation,
                    "water_meter_condition": consumption.water_meters.water_meter_condition,
                    "other_information": consumption.water_meters.other_information,
                    "water_meter_create_date": consumption.water_meters.water_meter_create_date,
                },
                "type_info": {
                    "water_meter_type_id": consumption.water_meters.water_meter_type.water_meter_type_id,
                    "water_meter_type_name": consumption.water_meters.water_meter_type.water_meter_type_name,
                    "water_meter_type_create_date": consumption.water_meters.water_meter_type.water_meter_type_create_date,
                },
                "tag_info": {
                    "water_meter_tag_name": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_name,
                    "water_meter_tag_id": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_id,
                    "water_meter_tag_create_date": consumption.water_meters.water_meter_type.water_meter_tag.water_meter_tag_create_date,
                },
            }
            if consumption.water_meters.water_meter_user != None:
                consumption_result["user_info"] = {
                    "user_id": consumption.water_meters.water_meter_user.user_id,
                    "user_phone": consumption.water_meters.water_meter_user.user_phone,
                    "user_name": consumption.water_meters.water_meter_user.user_name,
                    "user_lastname": consumption.water_meters.water_meter_user.user_lastname,
                    "user_create_date": consumption.water_meters.water_meter_user.user_create_date,
                }
            else:
                consumption_result["user_info"] = {
                    "user_id": "",
                    "user_phone": "",
                    "user_name": "",
                    "user_lastname": "",
                    "user_create_date": "",
                }
            if consumption.water_meters.water_meter_project != None:
                consumption_result["project_info"] = {
                    "water_meter_project_id": consumption.water_meters.water_meter_project.water_meter_project_id,
                    "water_meter_project_name": consumption.water_meters.water_meter_project.water_meter_project_name,
                    "water_meter_project_title": consumption.water_meters.water_meter_project.water_meter_project_title,
                    "water_meter_project_create_date": consumption.water_meters.water_meter_project.water_meter_project_create_date,
                }
            else:
                consumption_result["project_info"] = {
                    "water_meter_project_id": "",
                    "water_meter_project_name": "",
                    "water_meter_project_title": "",
                    "water_meter_project_create_date": "",
                }
            return True, consumption_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_cumulative_consumptions_serializer(token, page, count, water_meter_serial, water_meter_tag, sort_value,
                                                    input_reverse):
        """
            param : [token, page, count, water_meter_serial, water_meter_tag, sort_value,
                                            input_reverse]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]

            cumulative_result_dict = {}

            # calculate cumulative value from consumption table .
            def _calculate_cumulative_and_get_last_consumption(all_water_meters):
                current_time = datetime.now()
                # get current time to jalali date .
                jalali_join = datetime2jalali(current_time).strftime('%y/%m/%d')
                jalali_join_split = jalali_join.split('/')
                if jalali_join_split[0] == '01':
                    jalali_join_split[0] = '1401'
                if jalali_join_split[0] == '02':
                    jalali_join_split[0] = '1402'
                if jalali_join_split[0] == '03':
                    jalali_join_split[0] = '1403'
                # get first day and last day of month in jalali date
                if int(jalali_join_split[1]) <= 6:
                    last_day_month = 31
                elif int(jalali_join_split[1]) > 6:
                    last_day_month = 30
                # jalaliToGeorgian_currentTime
                j2g = jalali_to_gregorian(jy=int(jalali_join_split[0]),
                                          jm=int(jalali_join_split[1]),
                                          jd=int(jalali_join_split[2]))
                j2g_str = f'{j2g[0]}-{j2g[1]}-{j2g[2]}'

                # Month
                # GeorgianFirstDayMonth
                g_first_day = jalali_to_gregorian(jy=int(jalali_join_split[0]),
                                                  jm=int(jalali_join_split[1]),
                                                  jd=1)
                # g_first_day too str
                if g_first_day[1] <= 9:
                    g_first_day[1] = f'0{g_first_day[1]}'
                if g_first_day[2] <= 9:
                    g_first_day[2] = f'0{g_first_day[2]}'
                g_first_day_2_str = f'{g_first_day[0]}-{g_first_day[1]}-{g_first_day[2]}'

                # GeorgianLastDayMonth
                g_last_day = jalali_to_gregorian(jy=int(jalali_join_split[0]),
                                                 jm=int(jalali_join_split[1]),
                                                 jd=last_day_month)
                # g_last_day too str
                if g_last_day[1] <= 9:
                    g_last_day[1] = f'0{g_last_day[1]}'
                if g_last_day[2] <= 9:
                    g_last_day[2] = f'0{g_last_day[2]}'
                g_last_day_2_str = f'{g_last_day[0]}-{g_last_day[1]}-{g_last_day[2]} 03:29:00'
                # End Month

                # Year
                # GeorgianFirstDayYear
                g_first_day_y = jalali_to_gregorian(jy=int(jalali_join_split[0]), jm=1, jd=1)
                # g_first_year too str
                if g_first_day_y[1] <= 9:
                    g_first_day_y[1] = f'0{g_first_day_y[1]}'
                if g_first_day_y[2] <= 9:
                    g_first_day_y[2] = f'0{g_first_day_y[2]}'
                g_first_day_y_2_str = f'{g_first_day_y[0]}-{g_first_day_y[1]}-{g_first_day_y[2]}'

                # GeorgianLastDayYear
                g_last_day_y = jalali_to_gregorian(jy=int(jalali_join_split[0]), jm=12, jd=29)
                # g_last_year too str
                if g_last_day_y[1] <= 9:
                    g_last_day_y[1] = f'0{g_last_day_y[1]}'
                if g_last_day_y[2] <= 9:
                    g_last_day_y[2] = f'0{g_last_day_y[2]}'
                g_last_day_y_2_str = f'{g_last_day_y[0]}-{g_last_day_y[1]}-{g_last_day_y[2]}'
                # End Year

                for water_meter_obj in all_water_meters:
                    serial = water_meter_obj.water_meter_serial
                    if serial not in cumulative_result_dict:
                        cumulative_result_dict[serial] = {
                            # 'water_meter_serial': serial,
                            'cumulative_consumptions': {},
                            'last_consumption': {},

                        }
                        consumptions_objects = WaterMetersConsumptions.objects.filter(water_meters=serial)
                        # sum all consumption
                        total_value = consumptions_objects.aggregate(Sum('value'))['value__sum']

                        # get last record
                        last_consumption = consumptions_objects.order_by(
                            'create_time').last()
                        if last_consumption is not None:
                            last_consumption = last_consumption.as_dict()
                            last_consumption.pop('water_meters')
                            last_consumption['timestamp'] = int(round(last_consumption['create_time'].timestamp()))
                            cumulative_value = last_consumption['cumulative_value']
                            if cumulative_value is not None:
                                difference = abs(total_value - cumulative_value)
                                if difference > 0 and difference < 10:
                                    final_total = cumulative_value
                                else:
                                    final_total = total_value
                            else:
                                final_total = total_value
                        else:
                            final_total = total_value
                        cumulative_result_dict[serial]['total_value'] = final_total
                        cumulative_result_dict[serial]['last_consumption'] = last_consumption
                        # end get last record

                        # year
                        cumulative_year_objects = consumptions_objects.filter(create_time__gte=g_first_day_y_2_str,
                                                                              create_time__lte=g_last_day_y_2_str)
                        cumulative_year_sum = cumulative_year_objects.aggregate(Sum('value'))
                        final_year_value = cumulative_year_sum["value__sum"]
                        if final_year_value is None:
                            final_year_value = 0
                        cumulative_result_dict[serial]['cumulative_consumptions']['year'] = (
                            jalali_join_split[0], final_year_value)
                        # month
                        cumulative_month_objects = consumptions_objects.filter(
                            create_time__gte=g_first_day_2_str,
                            create_time__lte=g_last_day_2_str)
                        cumulative_month_sum = cumulative_month_objects.aggregate(Sum('value'))
                        final_month_value = cumulative_month_sum["value__sum"]
                        if final_month_value is None:
                            final_month_value = 0
                        cumulative_result_dict[serial]['cumulative_consumptions']['month'] = (
                            jalali_join_split[1], final_month_value)

                        # day
                        cumulative_day_objects = consumptions_objects.filter(
                            create_time__startswith=current_time.date())
                        cumulative_day_sum = cumulative_day_objects.aggregate(Sum('value'))
                        final_day_value = cumulative_day_sum["value__sum"]
                        if final_day_value is None:
                            final_day_value = 0
                        cumulative_result_dict[serial]['cumulative_consumptions']['day'] = (
                            jalali_join_split[2], final_day_value)

                    # cumulative_result_list.append(cumulative_result)
                # end calculate cumulative value from consumption table .

            def _sort_value(sort_value, input_reverse):

                if input_reverse is None:
                    input_reverse = True

                if sort_value == 'last_consumption':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['last_consumption']['value'] if
                                         x[1]['last_consumption']['value'] is not None else 0, reverse=input_reverse)

                    return True, sorted_list

                elif sort_value == 'month':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['cumulative_consumptions']['month'] if
                                         x[1]['cumulative_consumptions']['month'] is not None else 0,
                                         reverse=input_reverse)

                    return True, sorted_list

                elif sort_value == 'year':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['cumulative_consumptions']['year'] if
                                         x[1]['cumulative_consumptions']['year'] is not None else 0,
                                         reverse=input_reverse)
                    return True, sorted_list

                elif sort_value == 'day':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['cumulative_consumptions']['day'] if
                                         x[1]['cumulative_consumptions']['day'] is not None else 0,
                                         reverse=input_reverse)

                    return True, sorted_list

                elif sort_value == 'consumption_create_time':
                    sorted_list = sorted(cumulative_result_dict.items(),
                                         key=lambda x: x[1]['last_consumption']['timestamp'] if
                                         x[1]['last_consumption'] is not None else 0,
                                         reverse=input_reverse)

                    return True, sorted_list

                else:
                    return True, []

            fields = {
                "page": (page, int),
                "count": (count, int),
            }
            field_result = wrong_result(fields)
            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)

                filters = {
                    'water_meter_serial': water_meter_serial,
                    'water_meter_user__user_id': user_id,
                    'water_meter_type__water_meter_tag__water_meter_tag_id': water_meter_tag
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                all_water_meter_query = WaterMeters.objects.filter(**filters)

                all_water_meter_pagination = all_water_meter_query.order_by(
                    'water_meter_create_date')[offset:offset + limit]
                _calculate_cumulative_and_get_last_consumption(all_water_meters=all_water_meter_pagination)

                if input_reverse is not None and sort_value is None:
                    sort_value = 'consumption_create_time'
                if water_meter_tag is not None:
                    if sort_value is not None:
                        return _sort_value(sort_value=sort_value, input_reverse=input_reverse)
                    else:
                        cumulative_result_list = [(k, v) for k, v in cumulative_result_dict.items()]
                        return True, cumulative_result_list
                else:
                    cumulative_result_list = [(k, v) for k, v in cumulative_result_dict.items()]
                    return True, cumulative_result_list
            else:
                return field_result
        else:
            return False, wrong_token_result

    # -----------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------- AddSerializers -----------------------------------------------
    @staticmethod
    def calculate_all_consumptions_value(water_meter_serial):
        """
            param : [water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        try:
            sum_values = WaterMetersConsumptions.objects.filter(water_meters=water_meter_serial).aggregate(
                Sum('value'))
            sum_final_value = sum_values['value__sum']
            sum_all_values = float('{:.2f}'.format(sum_final_value))
            WaterMetersConsumptions.objects.filter(water_meters=water_meter_serial).update(sum_all_value=sum_all_values)
        except:
            pass

    @staticmethod
    def add_consumptions_water_meter_serializer(token, value, water_meters, information, module_code,
                                                from_previous_record_input, to_current_record_input,
                                                create_time_input, cumulative_value):
        """
            param : [token, value, water_meters, information, module_code,
                                        from_previous_record_input, to_current_record_input,
                                        create_time_input, cumulative_value]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:
            fields = {
                "value": (value, float),
                "information": (information, dict)
            }
            result = wrong_result(fields)

            if water_meters != None and module_code == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "سربال کنتور اشتباه است."
                    wrong_data_result["english_message"] = "The meter_serial is wrong."
                    return False, wrong_data_result
                if water_meters.water_meter_module is None:
                    wrong_data_result["farsi_message"] = "کنتور هیچ ماژولی ندارد"
                    wrong_data_result["english_message"] = "The meter has no modules"
                    return False, wrong_data_result
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code != None and water_meters == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_module__water_meter_module_code=module_code)
                except:
                    wrong_data_result["farsi_message"] = "ماژول به هیچ کنتوری اضافه نشده یا ای دی کاژول اشتباه است."
                    wrong_data_result[
                        "english_message"] = "The module has not been added to any meter! or module id is wrong"
                    return False, wrong_data_result

                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code != None and water_meters != None:
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_module__water_meter_module_code=module_code,
                                                              water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "کد اشتباه است"
                    wrong_data_result["english_message"] = "Code is wrong."
                    return False, wrong_data_result
                water_meters = [water_meter for water_meter in water_meters][0]
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code == None and water_meters == None:

                wrong_data_result["farsi_message"] = "لطفا شماره سریال را وارد کنید"
                wrong_data_result["english_message"] = "please enter code."
                return False, wrong_data_result
            consumption_records = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
            last_consumption_record = consumption_records.order_by('create_time').last()
            # Check for dont save repetitive data
            save_data_checker = False
            if create_time_input is not None and to_current_record_input is not None and \
                    from_previous_record_input is not None:
                save_data_checker = WaterMetersConsumptions.objects.filter(water_meters=water_meters,
                                                                           water_meters__water_meter_module__water_meter_module_code=module_code,
                                                                           value=value,
                                                                           create_time=create_time_input,
                                                                           from_previous_record=from_previous_record_input,
                                                                           to_current_record=to_current_record_input).exists()
            # check for same with different value
            # note : bigger value is currect
            upsert_check = WaterMetersConsumptions.objects.filter(
                water_meters=water_meters, water_meters__water_meter_module__water_meter_module_code=module_code,
                create_time=create_time_input, from_previous_record=from_previous_record_input,
                to_current_record=to_current_record_input)

            if len(upsert_check) > 0:
                upsert_check_value = upsert_check.values('value')
                print(f"upsert_check_value : {upsert_check_value} - meter : {water_meters} time = {create_time_input}")
                # if upsert_check_value > value : dont save new data
                if upsert_check_value[0]['value'] > value:
                    save_data_checker = True
                # if upsert_check_value < value : edit upsert_check and dont save value .
                elif upsert_check_value[0]['value'] < value:
                    upsert_check.update(value=value)
                    save_data_checker = True
            consumption = WaterMetersConsumptions()
            if last_consumption_record == None:
                from_previous_record = datetime.now()
            else:
                from_previous_record = last_consumption_record.create_time

            if result == None:
                consumption.value = value
                consumption.water_meters = water_meters
                consumption.information = information
                consumption.cumulative_value = cumulative_value
                if from_previous_record_input is not None and to_current_record_input is not None and create_time_input is not None:
                    consumption.to_current_record = to_current_record_input
                    consumption.from_previous_record = from_previous_record_input
                    consumption.create_time = create_time_input
                elif from_previous_record_input is None and to_current_record_input is \
                        None and create_time_input is None:
                    consumption.to_current_record = datetime.now()
                    consumption.from_previous_record = from_previous_record

                if save_data_checker is False:
                    print("saved")
                    consumption.save()

                return True, status_success_result
            else:
                return result
        else:
            return False, wrong_token_result

    @staticmethod
    def v1_add_consumptions_water_meter_serializer(token, value, water_meters, information, module_code,
                                                   cumulative_value):
        """
            param : [token, value, water_meters, information, module_code,cumulative_value]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:
            fields = {
                "value": (value, float),
                "information": (information, dict)
            }
            result = wrong_result(fields)
            # check section for valid meter .
            if water_meters != None and module_code == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "سربال کنتور اشتباه است."
                    wrong_data_result["english_message"] = "The meter_serial is wrong."
                    return False, wrong_data_result
                if water_meters.water_meter_module is None:
                    wrong_data_result["farsi_message"] = "کنتور هیچ ماژولی ندارد"
                    wrong_data_result["english_message"] = "The meter has no modules"
                    return False, wrong_data_result
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code != None and water_meters == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_module__water_meter_module_code=module_code)
                except:
                    wrong_data_result["farsi_message"] = "ماژول به هیچ کنتوری اضافه نشده یا ای دی کاژول اشتباه است."
                    wrong_data_result[
                        "english_message"] = "The module has not been added to any meter! or module id is wrong"
                    return False, wrong_data_result

                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code != None and water_meters != None:
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_module__water_meter_module_code=module_code,
                                                              water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "کد اشتباه است"
                    wrong_data_result["english_message"] = "Code is wrong."
                    return False, wrong_data_result
                water_meters = [water_meter for water_meter in water_meters][0]
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code == None and water_meters == None:
                wrong_data_result["farsi_message"] = "لطفا شماره سریال را وارد کنید"
                wrong_data_result["english_message"] = "please enter code."
                return False, wrong_data_result
            consumption_records = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
            last_consumption_record = consumption_records.order_by('create_time').last()
            # get current time
            current_time = datetime.now()
            current_time_utc = datetime.now(tz=pytz.utc)
            # Check for dont save repetitive data
            save_data_checker = True
            # get difference
            # iran : 2:30 am -- 23:00 utc
            # iran : 3:00 am -- 23:30 utc
            if last_consumption_record is not None:
                # get current time hour :
                time_check = current_time_utc.time()
                time_valid = datetime.strptime('23:00:00', '%H:%M:%S').time()
                time_valid_les = datetime.strptime('23:30:00', '%H:%M:%S').time()
                if time_check > time_valid and time_valid < time_valid_les:
                    # create time for filter
                    date_filter = current_time_utc.date()
                    time_filter = datetime.strptime('23:00:00', '%H:%M:%S').time()
                    date_time_filter = f'{date_filter} {time_filter}'
                    date_time_filter = datetime.strptime(date_time_filter, '%Y-%m-%d %H:%M:%S')
                    # time_delta = date_time_filter + timedelta(hours=1)
                    time_delta = date_time_filter + timedelta(minutes=60)
                    ls_frame_utc = last_consumption_record.create_time

                    ls_str_frame_utc = ls_frame_utc.strftime("%Y-%m-%d %H:%M:%S")
                    ls_datetime_object = datetime.strptime(ls_str_frame_utc, '%Y-%m-%d %H:%M:%S')
                    # change teh to utc
                    local = pytz.timezone("Asia/Tehran")
                    local_dt = local.localize(ls_datetime_object, is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt_str_frame = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                    ls_utc_datetime_object_teh = datetime.strptime(utc_dt_str_frame, '%Y-%m-%d %H:%M:%S')
                    # end change teh to utc

                    # change europe to utc
                    local = pytz.timezone("CET")
                    local_dt_europe = local.localize(ls_datetime_object, is_dst=None)
                    utc_dt_er = local_dt_europe.astimezone(pytz.utc)
                    utc_dt_str_frame_er = utc_dt_er.strftime("%Y-%m-%d %H:%M:%S")
                    ls_utc_datetime_object_er = datetime.strptime(utc_dt_str_frame_er, '%Y-%m-%d %H:%M:%S')
                    # end change europe to utc

                    if ls_utc_datetime_object_teh > date_time_filter and ls_utc_datetime_object_teh < time_delta:
                        save_data_checker = False

                    elif ls_utc_datetime_object_er > date_time_filter and ls_utc_datetime_object_er < time_delta:
                        save_data_checker = False

            consumption = WaterMetersConsumptions()
            if last_consumption_record == None:
                from_previous_record = current_time
            else:
                from_previous_record = last_consumption_record.create_time
            # check for missing day value
            if last_consumption_record is not None:
                last_cons_day = last_consumption_record.create_time.date()
                last_cons_day_utc = last_consumption_record.create_time.astimezone(pytz.UTC).date()
                # if last_consumption_record.create_time.time() > '00:01' and last_consumption_record.create_time.time() < '00:59':
                #     last_cons_day_utc = last_cons_day_utc + timedelta(days=1)
                # current_day = current_time.date()
                current_day_utc = current_time.astimezone(pytz.UTC).date()
                # date_difference = current_day - last_cons_day
                date_difference = current_day_utc - last_cons_day_utc
                date_difference_int = int(date_difference.days)
                if date_difference_int > 1:
                    try:
                        last_cons_cumulative = last_consumption_record.cumulative_value
                        for day in reversed(range(date_difference_int)):
                            last_cons_obj = WaterMetersConsumptions()
                            if day == 0:
                                break
                            lost_day = current_time - timedelta(days=day)
                            difference_with_lost_day = lost_day.date() - last_cons_day
                            difference_with_lost_day = int(difference_with_lost_day.days)
                            # update consumption table in lost_days
                            # lost_value = ((current_value + last_cons_cumulative) - current_cumulative) % date_difference_int
                            lost_value = (cumulative_value - (value + last_cons_cumulative)) / (date_difference_int - 1)
                            lost_cumulative = (lost_value * difference_with_lost_day) + last_cons_cumulative
                            # should create consumption object with this date
                            last_cons_obj.value = float('{:.2f}'.format(lost_value))
                            last_cons_obj.water_meters = water_meters
                            last_cons_obj.information = last_consumption_record.information
                            last_cons_obj.create_time = lost_day
                            last_cons_obj.to_current_record = lost_day
                            last_cons_obj.from_previous_record = last_consumption_record.create_time
                            last_cons_obj.cumulative_value = float('{:.2f}'.format(lost_cumulative))
                            if lost_value >= 0:
                                last_cons_obj.save()
                            else:
                                pass
                    except:
                        pass
                last_cons_cumulative = last_consumption_record.cumulative_value
                # difference
                if date_difference_int <= 1:
                    if last_cons_cumulative is not None and cumulative_value is not None:
                        difference_cumulative = cumulative_value - last_cons_cumulative
                        if difference_cumulative >= 0:
                            if difference_cumulative == value:
                                final_value = value
                            elif difference_cumulative > value:
                                final_value = difference_cumulative
                            elif difference_cumulative < value and difference_cumulative != 0:
                                final_value = difference_cumulative
                            elif difference_cumulative == 0 and value != 0:
                                save_data_checker = False
                                final_value = value
                            else:
                                final_value = value
                        else:
                            final_value = value
                    else:
                        final_value = value
                else:
                    last_cons_update = WaterMetersConsumptions.objects.filter(water_meters=water_meters).order_by(
                        'create_time').last()
                    last_cons_cumulative_update = last_cons_update.cumulative_value
                    if last_cons_cumulative_update is not None and cumulative_value is not None:
                        difference_cumulative = cumulative_value - last_cons_cumulative_update
                        if difference_cumulative >= 0:
                            if difference_cumulative == value:
                                final_value = value
                            elif difference_cumulative > value:
                                final_value = difference_cumulative
                            elif difference_cumulative < value and difference_cumulative != 0:
                                final_value = difference_cumulative
                            # or difference_cumulative < value
                            elif difference_cumulative == 0 and value != 0:
                                save_data_checker = False
                                final_value = value
                            else:
                                final_value = value
                        else:
                            final_value = value
                    else:
                        final_value = value
            else:
                final_value = value
            if final_value < 0:
                save_data_checker = False
            if result == None:
                consumption.value = float('{:.2f}'.format(final_value))
                consumption.water_meters = water_meters
                consumption.information = information
                consumption.to_current_record = datetime.now()
                consumption.from_previous_record = from_previous_record
                consumption.cumulative_value = float('{:.2f}'.format(cumulative_value))
                if save_data_checker is True:
                    consumption.save()
                    try:
                        consumptions = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
                        sum_all_consumptions = consumptions.aggregate(Sum('value'))
                        sum_all_consumptions = sum_all_consumptions['value__sum']
                        sum_all_values = float('{:.2f}'.format(sum_all_consumptions))
                        sum_difference = abs(sum_all_values - cumulative_value)
                        if sum_difference > 0 and sum_difference < 10:
                            consumptions.update(sum_all_value=float('{:.2f}'.format(cumulative_value)))
                        else:
                            consumptions.update(sum_all_value=sum_all_values)
                    except:
                        pass
                # if water_meters.water_meter_user is not None and save_data_checker is True:
                #     phone_number = water_meters.water_meter_user.user_phone
                #     publish_message_to_client(phone_number=phone_number, from_where='add_consumption')
                # if water_meters.water_meter_project is not None and save_data_checker is True:
                #     project_id = water_meters.water_meter_project.water_meter_project_id
                #     middle_admin_publish_data = {
                #         'project_id': project_id,
                #         'meter_serial': water_meters.water_meter_serial,
                #         'from_where': 'add_consumption'
                #     }
                #     publish_message_to_client(publish_func='middle_admin', data=middle_admin_publish_data)
                return True, status_success_result
            else:
                return result
        else:
            return False, wrong_token_result

    # version two serialize
    @staticmethod
    def v2_add_consumptions_water_meter_serializer(token, value, water_meters, information, module_code,
                                                   from_previous_record_input, to_current_record_input,
                                                   create_time_input, cumulative_value):
        """
            param : [token, value, water_meters, information, module_code,
                                           from_previous_record_input, to_current_record_input,
                                           create_time_input, cumulative_value]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:
            fields = {
                "value": (value, float),
                "information": (information, dict)
            }
            result = wrong_result(fields)

            if water_meters != None and module_code == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "سربال کنتور اشتباه است."
                    wrong_data_result["english_message"] = "The meter_serial is wrong."
                    return False, wrong_data_result
                if water_meters.water_meter_module is None:
                    wrong_data_result["farsi_message"] = "کنتور هیچ ماژولی ندارد"
                    wrong_data_result["english_message"] = "The meter has no modules"
                    return False, wrong_data_result
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code != None and water_meters == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_module__water_meter_module_code=module_code)
                except:
                    wrong_data_result["farsi_message"] = "ماژول به هیچ کنتوری اضافه نشده یا ای دی کاژول اشتباه است."
                    wrong_data_result[
                        "english_message"] = "The module has not been added to any meter! or module id is wrong"
                    return False, wrong_data_result

                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code != None and water_meters != None:
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_module__water_meter_module_code=module_code,
                                                              water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "کد اشتباه است"
                    wrong_data_result["english_message"] = "Code is wrong."
                    return False, wrong_data_result
                water_meters = [water_meter for water_meter in water_meters][0]
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code == None and water_meters == None:

                wrong_data_result["farsi_message"] = "لطفا شماره سریال را وارد کنید"
                wrong_data_result["english_message"] = "please enter code."
                return False, wrong_data_result
            consumption_records = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
            last_consumption_record = consumption_records.order_by('create_time').last()
            # Check for dont save repetitive data
            save_data_checker = False
            if create_time_input is not None and to_current_record_input is not None and \
                    from_previous_record_input is not None:
                save_data_checker = WaterMetersConsumptions.objects.filter(create_time=create_time_input,
                                                                           water_meters=water_meters,
                                                                           from_previous_record=from_previous_record_input,
                                                                           value=value,
                                                                           to_current_record=to_current_record_input).exists()

            # value comparison
            value_comparison = WaterMetersConsumptions.objects.filter(create_time=create_time_input,
                                                                      water_meters=water_meters,
                                                                      from_previous_record=from_previous_record_input,
                                                                      to_current_record=to_current_record_input)
            if value_comparison is not None:
                for value_obj in value_comparison:
                    value_exists = value_obj.value
                    if value > value_exists:
                        value_comparison.update(value=value)
                        save_data_checker = True
                    elif value < value_exists:
                        save_data_checker = True

            consumption = WaterMetersConsumptions()
            if last_consumption_record == None:
                from_previous_record = datetime.now()

            else:
                from_previous_record = last_consumption_record.create_time

            if result == None:
                consumption.value = value
                consumption.water_meters = water_meters
                consumption.information = information
                consumption.cumulative_value = cumulative_value
                if from_previous_record_input is not None and to_current_record_input is not None and create_time_input is not None:
                    consumption.to_current_record = to_current_record_input
                    consumption.from_previous_record = from_previous_record_input
                    consumption.create_time = create_time_input
                elif from_previous_record_input is None and to_current_record_input is \
                        None and create_time_input is None:
                    consumption.to_current_record = datetime.now()
                    consumption.from_previous_record = from_previous_record
                if save_data_checker is False:
                    consumption.save()
                return True, status_success_result
            else:
                return result
        else:
            return False, wrong_token_result

    @staticmethod
    def v3_add_consumptions_water_meter_serializer(token, value, water_meters, information, module_code,
                                                   cumulative_value, inpput_create_time=None):
        """
            param : [token, value, water_meters, information, module_code,
                                                   cumulative_value, inpput_create_time]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:
            # check section for valid meter .
            if water_meters != None and module_code == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "سربال کنتور اشتباه است."
                    wrong_data_result["english_message"] = "The meter_serial is wrong."
                    return False, wrong_data_result
                if water_meters.water_meter_module is None:
                    wrong_data_result["farsi_message"] = "کنتور هیچ ماژولی ندارد"
                    wrong_data_result["english_message"] = "The meter has no modules"
                    return False, wrong_data_result
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code != None and water_meters == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_module__water_meter_module_code=module_code)
                except:
                    wrong_data_result["farsi_message"] = "ماژول به هیچ کنتوری اضافه نشده یا ای دی کاژول اشتباه است."
                    wrong_data_result[
                        "english_message"] = "The module has not been added to any meter! or module id is wrong"
                    return False, wrong_data_result

                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code != None and water_meters != None:
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_module__water_meter_module_code=module_code,
                                                              water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "کد اشتباه است"
                    wrong_data_result["english_message"] = "Code is wrong."
                    return False, wrong_data_result
                water_meters = [water_meter for water_meter in water_meters][0]
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code == None and water_meters == None:
                wrong_data_result["farsi_message"] = "لطفا شماره سریال را وارد کنید"
                wrong_data_result["english_message"] = "please enter code."
                return False, wrong_data_result
            if inpput_create_time is not None:
                current_time = inpput_create_time
            else:
                current_time = datetime.now()
            consumption_records = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
            last_consumption_record = consumption_records.order_by('create_time').last()
            if last_consumption_record is not None:
                last_consumption_record_time = last_consumption_record.create_time
                # Convert last_consumption_record_time to UTC time zone
                # last_consumption_record_time_utc = pytz.utc.localize(last_consumption_record_time)
                # Convert current_time to UTC time zone
                current_time_utc = pytz.utc.localize(current_time)

                # Calculate the difference
                time_difference = current_time_utc - last_consumption_record_time

                # Extract the days, hours, and minutes from the timedelta object
                # days = time_difference.days
                # hours, remainder = divmod(time_difference.seconds, 3600)
                # minutes, _ = divmod(remainder, 60)
                last_consumption_record_cumulative_value = last_consumption_record.cumulative_value
                if last_consumption_record_cumulative_value is not None:
                    cumulative_difference = cumulative_value - last_consumption_record_cumulative_value
                    if cumulative_difference > 0:
                        prepared_data_to_add = {
                            'value': cumulative_difference,
                            'water_meters': water_meters,
                            'information': information,
                            'cumulative_value': cumulative_value,
                        }
                        if inpput_create_time is not None:
                            prepared_data_to_add['create_time'] = inpput_create_time
                        WaterMetersConsumptions.objects.create(**prepared_data_to_add)
                        try:
                            consumptions = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
                            sum_all_consumptions = consumptions.aggregate(Sum('value'))
                            sum_all_consumptions = sum_all_consumptions['value__sum']
                            sum_all_values = float('{:.2f}'.format(sum_all_consumptions))
                            sum_difference = abs(sum_all_values - cumulative_value)
                            if sum_difference > 0 and sum_difference < 10:
                                consumptions.update(sum_all_value=float('{:.2f}'.format(cumulative_value)))
                            else:
                                consumptions.update(sum_all_value=sum_all_values)
                        except:
                            pass
                        return True, status_success_result
                    if cumulative_difference == 0:
                        # Define a timedelta of 15 minutes
                        fifteen_minutes = timedelta(minutes=15)
                        # Compare the difference with 15 minutes
                        if time_difference > fifteen_minutes:
                            prepared_data_to_add = {
                                'value': cumulative_difference,
                                'water_meters': water_meters,
                                'information': {},
                                'cumulative_value': cumulative_value,
                            }
                            if inpput_create_time is not None:
                                prepared_data_to_add['create_time'] = inpput_create_time
                            WaterMetersConsumptions.objects.create(**prepared_data_to_add)
                            try:
                                consumptions = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
                                sum_all_consumptions = consumptions.aggregate(Sum('value'))
                                sum_all_consumptions = sum_all_consumptions['value__sum']
                                sum_all_values = float('{:.2f}'.format(sum_all_consumptions))
                                sum_difference = abs(sum_all_values - cumulative_value)
                                if sum_difference > 0 and sum_difference < 10:
                                    consumptions.update(sum_all_value=float('{:.2f}'.format(cumulative_value)))
                                else:
                                    consumptions.update(sum_all_value=sum_all_values)
                            except:
                                pass
                            return True, status_success_result
            else:
                prepared_data_to_add = {
                    'value': value,
                    'water_meters': water_meters,
                    'information': information,
                    'cumulative_value': cumulative_value,
                }
                if inpput_create_time is not None:
                    prepared_data_to_add['create_time'] = inpput_create_time
                WaterMetersConsumptions.objects.create(**prepared_data_to_add)
                try:
                    consumptions = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
                    sum_all_consumptions = consumptions.aggregate(Sum('value'))
                    sum_all_consumptions = sum_all_consumptions['value__sum']
                    sum_all_values = float('{:.2f}'.format(sum_all_consumptions))
                    sum_difference = abs(sum_all_values - cumulative_value)
                    if sum_difference > 0 and sum_difference < 10:
                        consumptions.update(sum_all_value=float('{:.2f}'.format(cumulative_value)))
                    else:
                        consumptions.update(sum_all_value=sum_all_values)
                except:
                    pass
                return True, status_success_result
        else:
            return False, wrong_token_result

    @staticmethod
    def add_level_gauge_consumptions_water_meter_serializer(token, value, water_meters, information, module_code,
                                                            cumulative_value):
        """
            param : [token, value, water_meters, information, module_code,
                                                    cumulative_value]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:
            fields = {
                "value": (value, float),
                "information": (information, dict)
            }
            result = wrong_result(fields)
            # check section for valid meter .
            if water_meters != None and module_code == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "سربال کنتور اشتباه است."
                    wrong_data_result["english_message"] = "The meter_serial is wrong."
                    return False, wrong_data_result
                if water_meters.water_meter_module is None:
                    wrong_data_result["farsi_message"] = "کنتور هیچ ماژولی ندارد"
                    wrong_data_result["english_message"] = "The meter has no modules"
                    return False, wrong_data_result
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result

            elif module_code != None and water_meters == None:
                try:
                    water_meters = WaterMeters.objects.get(water_meter_module__water_meter_module_code=module_code)
                except:
                    wrong_data_result["farsi_message"] = "ماژول به هیچ کنتوری اضافه نشده یا ای دی کاژول اشتباه است."
                    wrong_data_result[
                        "english_message"] = "The module has not been added to any meter! or module id is wrong"
                    return False, wrong_data_result

                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code != None and water_meters != None:
                try:
                    water_meters = WaterMeters.objects.filter(water_meter_module__water_meter_module_code=module_code,
                                                              water_meter_serial=water_meters)
                except:
                    wrong_data_result["farsi_message"] = "کد اشتباه است"
                    wrong_data_result["english_message"] = "Code is wrong."
                    return False, wrong_data_result
                water_meters = [water_meter for water_meter in water_meters][0]
                if water_meters.water_meter_activation != 1 and water_meters.water_meter_validation != 1:
                    wrong_data_result["farsi_message"] = "کنتور فعال نیست"
                    wrong_data_result["english_message"] = "meter not active or valid"
                    return False, wrong_data_result
            elif module_code == None and water_meters == None:
                wrong_data_result["farsi_message"] = "لطفا شماره سریال را وارد کنید"
                wrong_data_result["english_message"] = "please enter code."
                return False, wrong_data_result
            consumption_records = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
            last_consumption_record = consumption_records.order_by('create_time').last()
            # get current time
            current_time = datetime.now()

            consumption = WaterMetersConsumptions()
            if last_consumption_record is None:
                from_previous_record = current_time
            else:
                from_previous_record = last_consumption_record.create_time

            if result == None:
                consumption.value = float('{:.2f}'.format(value))
                consumption.water_meters = water_meters
                consumption.information = information
                consumption.to_current_record = None
                consumption.from_previous_record = None
                if cumulative_value is not None:
                    consumption.cumulative_value = float('{:.2f}'.format(cumulative_value))
                consumption.save()
                try:
                    consumptions = WaterMetersConsumptions.objects.filter(water_meters=water_meters)
                    sum_all_consumptions = consumptions.aggregate(Sum('value'))
                    sum_all_consumptions = sum_all_consumptions['value__sum']
                    sum_all_values = float('{:.2f}'.format(sum_all_consumptions))
                    consumptions.update(sum_all_value=sum_all_values)
                except:
                    pass
                if water_meters.water_meter_user is not None:
                    phone_number = water_meters.water_meter_user.user_phone
                    publish_message_to_client(phone_number=phone_number, from_where='add_consumption')
                if water_meters.water_meter_project is not None:
                    project_id = water_meters.water_meter_project.water_meter_project_id
                    middle_admin_publish_data = {
                        'project_id': project_id,
                        'meter_serial': water_meters.water_meter_serial,
                        'from_where': 'add_consumption'
                    }
                    publish_message_to_client(publish_func='middle_admin', data=middle_admin_publish_data)
                return True, status_success_result
            else:
                return result
        else:
            return False, wrong_token_result

    @staticmethod
    def add_consumptions_from_mqtt_broker(token, value, water_meters, information,
                                        cumulative_value, create_time, counter, value_type, flow_instantaneous,
                                        flow_type, flow_value, log_id):
        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result is None:
            # Parse the create_time string to datetime object
            time_string = create_time
            date_time_obj = datetime.strptime(time_string, "%m/%d/%Y-%H:%M:%S")
            # Get the meter object from the water_meter_serial
            meter_object = WaterMeters.objects.get(water_meter_serial=water_meters)
            
            try:
                # Check if the record already exists
                WaterMetersConsumptions.objects.get(water_meters=meter_object, create_time=date_time_obj)
                return False, wrong_data_result
            except WaterMetersConsumptions.DoesNotExist:
                # Get the last consumption entry for the water meter
                last_consumption = WaterMetersConsumptions.objects.filter(water_meters=meter_object,
                                                                          create_time__lte=date_time_obj).order_by(
                    'create_time').last()
                
                # Get the first consumption after this consumption so we can update it when missed data comes back
                first_later_consumption = WaterMetersConsumptions.objects.filter(water_meters=meter_object,
                                                                        create_time__gte=date_time_obj).order_by(
                    'create_time').first()
                
                if first_later_consumption is not None:
                    first_later_consumption.value = first_later_consumption.cumulative_value - cumulative_value
                    first_later_consumption.from_previous_record = date_time_obj
                    first_later_consumption.save()
                    
                device_value = value
                
                if last_consumption is not None:
                    last_cumulative_value = last_consumption.cumulative_value
                    difference_cumulative = cumulative_value - last_cumulative_value
                    
                    # Handle the case where cumulative difference is negative or positive, no restriction
                    # This will treat both positive and negative values equally
                    if value is None:
                        value = cumulative_value - last_consumption.cumulative_value
                    if value is not None and last_consumption is not None:
                        if value != difference_cumulative:
                            value = difference_cumulative
                            
                if last_consumption is None:
                    from_previous_record = datetime.now()
                else:
                    from_previous_record = last_consumption.create_time

                if water_meters in {"SWMM-02511102", "SWMM-02511103"}:
                    device_value *= 10

                # Create and save the consumption object
                consumption_object = WaterMetersConsumptions()
                consumption_object.water_meters = meter_object
                consumption_object.value = value
                consumption_object.device_value = device_value
                consumption_object.information = information
                consumption_object.cumulative_value = cumulative_value
                consumption_object.create_time = date_time_obj
                consumption_object.counter = counter
                consumption_object.value_type = value_type
                consumption_object.flow_instantaneous = flow_instantaneous
                consumption_object.flow_type = flow_type
                consumption_object.flow_value = flow_value
                consumption_object.log_id = log_id
                consumption_object.from_previous_record = from_previous_record
                consumption_object.to_current_record = datetime.now()
                consumption_object.save()
                
                return True, status_success_result
            
        else:
            return False, wrong_token_result


    @staticmethod
    def get_last_consumptions_(token, water_meters):

        token_result = StaticTokenSerializer()
        token_result = token_result.token_checker(token)
        if token_result == None:
            # if value none get last cumulative and do minus

            meter_object = WaterMeters.objects.get(water_meter_serial=water_meters)
            last_consumption = WaterMetersConsumptions.objects.filter(water_meters=meter_object).order_by(
                'create_time').last()
            if last_consumption is not None:
                return True, last_consumption.counter
            else:
                return False, wrong_data_result
        else:
            return False, wrong_token_result

    # -----------------------------------------------------------------------------------------------------------------
