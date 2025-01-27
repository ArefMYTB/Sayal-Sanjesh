import os
import sys
import django
from pathlib import Path

# ------------------------------------define django setting to access project model-------------------------------------
base_dir = os.getcwd()
project_path = Path(base_dir).parent
sys.path.append(f"{project_path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutomationSayalSanjesh.settings")
django.setup()
# ----------------------------------------------------------------------------------------------------------------------
from SayalSanjesh.models import WaterMetersConsumptions, WaterMeters, WaterMetersProjects
from django.db.models import Count
from django.db.models import F, Subquery, OuterRef, Max
from django.db.models.functions import Length
import datetime


# ----------------------------------------------- delete data manager --------------------------------------------------
class delete_data_from_database:
    def delete_duplicate_value(self):
        # projectId : ae01a22c-7b20-43bc-be4b-eba7f6bbb3ba , tagId : 07d00e58-a3a4-4963-9f25-d22d4a5befbd
        all_power_meter_id = WaterMeters.objects.filter(
            water_meter_type__water_meter_tag_id='07d00e58-a3a4-4963-9f25-d22d4a5befbd',
            water_meter_project_id='ae01a22c-7b20-43bc-be4b-eba7f6bbb3ba').values('water_meter_serial')
        print(f"all_power_meter_id_count  : {len(all_power_meter_id)}")

        for meter_serial in all_power_meter_id:
            print(meter_serial)
            consumptions = WaterMetersConsumptions.objects.filter(
                water_meters=meter_serial['water_meter_serial']).values(
                'create_time').annotate(count=Count('consumption_id'))

            duplicates = WaterMetersConsumptions.objects.filter(water_meters=meter_serial['water_meter_serial']).values(
                'create_time').annotate(count=Count('consumption_id')).filter(
                count__gt=1)
            # for duplicate in duplicates:
            #     records = WaterMetersConsumptions.objects.filter(water_meters=meter_serial['water_meter_serial'],
            #                                                      create_time=duplicate['create_time']).order_by('value')
            # #     # Delete all records except the one with the highest b value
            #     delete_status = records.exclude(consumption_id=records.last().consumption_id).delete()
            #     print(delete_status)

    def delete_consumption_v2(self):
        for num in range(12, 29):
            dt_obj = datetime.datetime(2023, 11, num)
            consumption_objects = WaterMetersConsumptions.objects.filter(water_meters_id='SEMK-02311132',
                                                                         create_time__day=dt_obj.day,
                                                                         create_time__month=dt_obj.month,
                                                                         create_time__year=dt_obj.year)
            if len(consumption_objects) >= 2:
                cons_ids = consumption_objects.values('consumption_id', 'value', 'create_time')
                print(cons_ids)
                # for cons in consumption_objects:
                #     print(dt_obj, cons.water_meters.water_meter_serial, cons.value, cons.create_time)

    def delete_data_in_range(self):
        print("start")
        dt = datetime.datetime(2023, 11, 11)
        dt = datetime.datetime(2023, 11, 28)
        valid_cons_serial = ['SEMK-02311120']
        for serial in valid_cons_serial:
            for num in range(11, 29):
                dt = datetime.datetime(2023, 11, num)
                cons_obj = WaterMetersConsumptions.objects.filter(water_meters_id=serial, create_time__day=dt.day,
                                                                  create_time__month=dt.month,
                                                                  create_time__year=dt.year)
                if len(cons_obj) == 1:
                    cons_obj = list(cons_obj)[0]
                    cons_id = cons_obj.consumption_id
                    cons_del = WaterMetersConsumptions.objects.get(consumption_id=cons_id).delete()
                    print(cons_del)


# ----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------read from txt and add to data base ------------------------------------------
def read_from_txt_file():
    base_root = os.getcwd()
    file_path = os.path.join(base_root, 'sample')
    # Using readlines()
    file1 = open(file_path, 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    for line in Lines:
        packet_string = line.strip()
        packet_split = packet_string.split(' ')
        date = packet_split[0]
        time = packet_split[2]
        meter_detail = packet_split[-1].split(',')
        module_code = meter_detail[0].split(':')[1]
        meter_serial = meter_detail[1].split(':')[1]
        cv_value = meter_detail[2].split(':')[1]
        ccv_value = meter_detail[-1].split(':')[1].split('$')[0]
        print(date, time, module_code, meter_serial, cv_value, ccv_value)
        # get_meter_value =


# ----------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------ edit project id -----------------------------------------------------
def edit_project_id():
    project_meter = WaterMeters.objects.filter(
        water_meter_project__water_meter_project_id='ae01a22c-7b20-43bc-be4b-eba7f6bbb3ba')
    meter_edited = []
    for project_object in project_meter:
        if project_object.water_meter_name.find('(شرقی)') != -1:
            meter_serial = project_object.water_meter_serial
            meter_edited.append(meter_serial)
            # WaterMeters.objects.filter(water_meter_serial=meter_serial).update(
            #     water_meter_project__water_meter_project_id='526c7265-9c90-47a4-bf1a-8ac28f112b73')
            meter_object = WaterMeters.objects.filter(water_meter_serial=meter_serial)
            project_object = WaterMetersProjects.objects.get(water_meter_project_id='526c7265-9c90-47a4-bf1a-8ac28f112b73')
            meter_object.update(water_meter_project=project_object)
            print(f"meter_object : {meter_object} , project_object : {project_object}")
    print(meter_edited)


# ----------------------------------------------------------------------------------------------------------------------
