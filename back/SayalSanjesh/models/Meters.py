import uuid
from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
# from .Users import Users
from Authorization.models.Admins import Admins
from Authorization.models.Users import Users
from Authorization.models.MiddleAdmins import MiddleAdmins
from SayalSanjesh.models.Tags import WaterMetersTags
# from SayalSanjesh.models.Patterns import Pattern


# -----------------------------------------------Consumption model------------------------------------------------------

class CustomConsumptionsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
        serialized_data = []
        for obj in queryset:
            # count_info = self.get_count_info(type_id=obj.water_meter_type_id)
            serialized_obj = {
                "consumption_id": obj.consumption_id,
                "create_time": obj.create_time,
                "value": obj.value,
                "cumulative_value": obj.cumulative_value,
                "water_meters": obj.water_meters.as_dict(),
                "sum_all_value": obj.sum_all_value,
                "information": obj.information,
                "from_previous_record": obj.from_previous_record,
                "to_current_record": obj.to_current_record,
                "bill_created": obj.bill_created,
                "value_type": obj.value_type,
                "flow_instantaneous": obj.flow_instantaneous,
                "flow_Type": obj.flow_Type,
                "flow_Value": obj.flow_Value,
            }
            serialized_data.append(serialized_obj)
        return serialized_data

    def get_count_info(self, type_id):
        All_counter_with_this_type = WaterMeters.objects.filter(
            water_meter_type=type_id).count()
        All_project_with_this_type = WaterMetersProjects.objects.filter(
            water_meter_types=type_id).count()
        return {
            "All_counter_with_this_type": All_counter_with_this_type,
            "All_project_with_this_type": All_project_with_this_type,
        }


class WaterMetersConsumptions(models.Model):
    consumption_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(default=datetime.now, blank=True)
    value = models.FloatField()
    device_value = models.FloatField(null=True)
    cumulative_value = models.FloatField(null=True, blank=True)
    water_meters = models.ForeignKey('WaterMeters', on_delete=CASCADE)
    information = models.JSONField()
    sum_all_value = models.FloatField(null=True, blank=True)
    from_previous_record = models.DateTimeField(null=True, blank=True)
    to_current_record = models.DateTimeField(null=True, blank=True)
    bill_created = models.BooleanField(default=False)
    counter = models.IntegerField(null=True)
    value_type = models.CharField(max_length=200, null=True)
    flow_instantaneous = models.FloatField(null=True)
    flow_Type = models.CharField(max_length=200, null=True)
    flow_Value = models.FloatField(null=True)
    log = models.ForeignKey('General.MqttLoger', on_delete=models.SET_NULL, null=True, blank=True)  # Link to log entry
    objects = CustomConsumptionsManager()

    class Meta:
        db_table = 'WaterMetersConsumptions'
        indexes = [
            models.Index(fields=['water_meters', 'create_time']),  # Composite index for efficient filtering by date
        ]

    def __str__(self):
        return f"{0} , {self.create_time} : {self.value}"

    def as_dict(self):
        if self.from_previous_record == None:
            from_previous_record = ""
        else:
            from_previous_record = self.from_previous_record
        if self.to_current_record == None:
            to_current_record = ""
        else:
            to_current_record = self.to_current_record
        return {
            "consumption_id": self.consumption_id,
            "create_time": self.create_time,
            "value": self.value,
            "cumulative_value": self.cumulative_value,
            "water_meters": self.water_meters.as_dict(),
            "sum_all_value": self.sum_all_value,
            "information": self.information,
            "from_previous_record": from_previous_record,
            "to_current_record": to_current_record,
            "bill_created": self.bill_created,
            "log_id": self.log.log_id if self.log else None,  # Include log_id
        }


# ----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------Types model-----------------------------------------------------------

class CustomTypeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            count_info = self.get_count_info(type_id=obj.water_meter_type_id)
            serialized_obj = {
                # Add any other custom fields you want to include in the response
                "admin_info": obj.admin.as_dict()['admin_id'],
                "water_meter_type_id": obj.water_meter_type_id,
                "water_meter_type_name": obj.water_meter_type_name,
                "water_meter_type_create_date": str(obj.water_meter_type_create_date),
                "water_meter_type_other_information": obj.water_meter_type_other_information,
                "water_meter_tag": {
                    "water_meter_tag_id": obj.water_meter_tag.water_meter_tag_id,
                    "water_meter_tag_name": obj.water_meter_tag.water_meter_tag_name,
                    "water_meter_tag_create_date": str(obj.water_meter_tag.water_meter_tag_create_date),
                },
                "water_meter_type_files": obj.water_meter_type_files,
                "All_counter_with_this_type": count_info['All_counter_with_this_type'],
                "All_project_with_this_type": count_info['All_project_with_this_type'],

            }
            serialized_data.append(serialized_obj)
        return serialized_data

    def get_count_info(self, type_id):
        All_counter_with_this_type = WaterMeters.objects.filter(
            water_meter_type=type_id).count()
        All_project_with_this_type = WaterMetersProjects.objects.filter(
            water_meter_types=type_id).count()
        return {
            "All_counter_with_this_type": All_counter_with_this_type,
            "All_project_with_this_type": All_project_with_this_type,
        }


class WaterMetersTypes(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    water_meter_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    water_meter_type_name = models.CharField(max_length=200)
    water_meter_type_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    # water_meter_project = models.ForeignKey(WaterMetersProjects, on_delete=models.DO_NOTHING)
    water_meter_type_other_information = models.JSONField(default={"default": "default"})
    water_meter_tag = models.ForeignKey('WaterMetersTags', on_delete=models.CASCADE, default=None, null=True)
    water_meter_type_files = ArrayField(models.JSONField(blank=True), default=list)
    objects = CustomTypeManager()

    class Meta:
        db_table = 'WaterMetersTypes'
        indexes = [
            models.Index(fields=['water_meter_type_id', 'water_meter_tag'])]

    def as_dict(self):
        return {
            "admin_info": self.admin.as_dict(),
            "water_meter_type_id": self.water_meter_type_id,
            "water_meter_type_name": self.water_meter_type_name,
            "water_meter_type_create_date": self.water_meter_type_create_date,
            "water_meter_type_other_information": self.water_meter_type_other_information,
            "water_meter_tag": self.water_meter_tag.as_dict(),
            "water_meter_type_files": self.water_meter_type_files,
            # "water_meter_project_info": self.water_meter_project.as_dict()
        }


# ----------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------Project model----------------------------------------------------------

class CustomProjectManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset, modify_response=None, pop_item=[], is_middel=None, middel_id=None):
        detail = False
        if hasattr(queryset, '__iter__') is False:
            queryset = [queryset]
            detail = True
        serialized_data = []
        if is_middel is True and middel_id is not None:
            middel_projects = MiddleAdmins.objects.get(middle_admin_id=middel_id).project_ids
            middel_projects_count = WaterMetersProjects.objects.filter(
                water_meter_project_id__in=middel_projects).count()
        for obj in queryset:
            serialized_obj = {
                # Add any other custom fields you want to include in the response
                "admin_info": str(obj.admin_id),
                "water_meter_project_name": obj.water_meter_project_name,
                "water_meter_project_id": str(obj.water_meter_project_id),
                "water_meter_project_create_date": str(obj.water_meter_project_create_date),
                "water_meter_project_title": obj.water_meter_project_title,
                "water_meter_project_start_date": str(obj.water_meter_project_start_date),
                "water_meter_project_employer_description": obj.water_meter_project_employer_description,
                "water_meter_project_contract_number": obj.water_meter_project_contract_number,
                "water_meter_project_other_information": obj.water_meter_project_other_information,
                "water_meter_project_files": obj.water_meter_project_files,
                "water_meter_project_urls": obj.water_meter_project_urls,
                "water_meters_with_this_id": {
                    "All_water_meter_with_this_id": str(self.all_meter_info(obj=obj)['All_water_meter_with_this_id']),
                    "sum_off_all_water_meter": self.all_meter_info(obj=obj)['sum_off_all_water_meter'],
                },
                'types': self.project_types(obj=obj, detail=detail),
                # 'all_project_numbers': WaterMetersProjects.objects.count()
            }
            if is_middel is True:
                serialized_obj['all_project_numbers'] = middel_projects_count
            if is_middel is False or is_middel is None:
                serialized_obj['all_project_numbers'] = WaterMetersProjects.objects.count()
            if detail:
                serialized_obj['project_users'] = self.project_users(obj=obj)
                serialized_obj['project_meters_per_tag'] = self.project_meters_per_tag(obj=obj)
            if modify_response is not None:
                for itm in pop_item:
                    serialized_obj.pop(itm)
            serialized_data.append(serialized_obj)

        return serialized_data

    def project_types(self, obj, detail):
        project_types = obj.water_meter_types.all()
        type_info_list = []
        for project_type in project_types:
            type_info = {
                "admin_info": str(project_type.admin.admin_id),
                "water_meter_type_id": str(project_type.water_meter_type_id),
                "water_meter_type_name": project_type.water_meter_type_name,
                "water_meter_type_create_date": str(project_type.water_meter_type_create_date),
                "water_meter_type_other_information": project_type.water_meter_type_other_information,
                "water_meter_type_files": project_type.water_meter_type_files,
                "water_meter_tag": {
                    "water_meter_tag_name": project_type.water_meter_tag.water_meter_tag_name,
                    "water_meter_tag_id": str(project_type.water_meter_tag.water_meter_tag_id),
                    "water_meter_tag_create_date": str(project_type.water_meter_tag.water_meter_tag_create_date),
                }
            }
            type_info_list.append(type_info)
            if detail:
                type_info['meter_per_type'] = WaterMeters.objects.filter(
                    water_meter_project_id=obj.water_meter_project_id,
                    water_meter_type__water_meter_type_id=project_type.water_meter_type_id).count()
        return type_info_list

    def all_meter_info(self, obj):
        project_meters = WaterMeters.objects.filter(water_meter_project_id=obj.water_meter_project_id)
        all_users_in_project = project_meters.values('water_meter_user').distinct().count()
        project_meters_count = project_meters.count()
        # sum_all_water_meter = WaterMetersConsumptions.objects.filter(water_meters__in=project_meters).aggregate(
        #     Sum('value'))['value__sum']
        response = {
            "All_water_meter_with_this_id": project_meters_count,
            "sum_off_all_water_meter": '',
            "all_users_in_project": all_users_in_project
        }
        return response

    def project_users(self, obj):
        project_user_list = []
        unique_meter_users = WaterMeters.objects.filter(water_meter_project_id=obj.water_meter_project_id) \
            .exclude(water_meter_user=None) \
            .values_list('water_meter_user') \
            .distinct()
        for user_id in unique_meter_users:
            queryset = Users.objects.get(
                user_id=user_id[0])
            response = Users.objects.serialize(queryset=queryset)
            response = response[0]
            response.pop('admin')
            response.pop('user_sms_code')
            response.pop('user_profile')
            response.pop('other_information')
            response.pop('user_create_date')
            response.pop('user_phone_number_validation')
            response.pop('user_images')
            response.pop('user_sms_code_start_time')
            response.pop('all users')
            project_user_list.append(response)
        return project_user_list

    def project_meters_per_tag(self, obj):
        tag_response = []
        tags = WaterMeters.objects.filter(water_meter_project_id=obj.water_meter_project_id).values_list(
            'water_meter_type__water_meter_tag__water_meter_tag_id').distinct()
        for tag_id in tags:
            tag_id = str(tag_id[0])
            query = WaterMetersTags.objects.get(water_meter_tag_id=tag_id)
            response = WaterMetersTags.objects.serialize(queryset=query)
            tag_obj = response[0]
            tag_obj.pop('admin_info')
            tag_obj['meter_number_per_tag'] = WaterMeters.objects.filter(
                water_meter_project_id=obj.water_meter_project_id,
                water_meter_type__water_meter_tag__water_meter_tag_id=tag_id).count()
            tag_response.append(tag_obj)
        return tag_response


class WaterMetersProjects(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    water_meter_project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    water_meter_project_name = models.CharField(max_length=200, )
    water_meter_project_title = models.CharField(max_length=200, default="Title")
    water_meter_project_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    water_meter_project_start_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    water_meter_project_employer_description = models.JSONField(default={})
    water_meter_project_contract_number = models.CharField(max_length=200, default="")
    water_meter_project_other_information = models.JSONField(default={})
    water_meter_project_images = ArrayField(models.JSONField(blank=True), default=list, null=True)
    water_meter_project_files = ArrayField(models.JSONField(blank=True), default=list)
    water_meter_project_urls = models.JSONField(default={})
    water_meter_types = models.ManyToManyField('WaterMetersTypes')
    objects = CustomProjectManager()

    class Meta:
        db_table = 'WaterMetersProjects'

    def as_dict(self):
        return {
            "admin_info": self.admin.as_dict(),
            "water_meter_project_name": self.water_meter_project_name,
            "water_meter_project_id": self.water_meter_project_id,
            "water_meter_project_create_date": self.water_meter_project_create_date,
            "water_meter_project_title": self.water_meter_project_title,
            "water_meter_project_start_date": self.water_meter_project_start_date,
            "water_meter_project_employer_description": self.water_meter_project_employer_description,
            "water_meter_project_contract_number": self.water_meter_project_contract_number,
            "water_meter_project_other_information": self.water_meter_project_other_information,
            "water_meter_project_files": self.water_meter_project_files,
            "water_meter_types": self.water_meter_types,
            "water_meter_project_images": self.water_meter_project_images,
            "water_meter_project_urls": self.water_meter_project_urls
        }

    def all_meter_info(self):
        project_meters = WaterMeters.objects.filter(water_meter_project_id=self.water_meter_project_id)
        all_users_in_project = project_meters.values('water_meter_user').distinct().count()
        project_meters_count = project_meters.count()
        sum_all_water_meter = WaterMetersConsumptions.objects.filter(water_meters__in=project_meters).aggregate(
            Sum('value'))
        response = {
            "All_water_meter_with_this_id": project_meters_count,
            "sum_off_all_water_meter": sum_all_water_meter['value__sum'],
            "all_users_in_project": all_users_in_project
        }

        return response

    def project_types(self):
        project_types = self.water_meter_types.all()
        type_info_list = []
        for project_type in project_types:
            type_info = {
                "admin_info": str(project_type.admin.admin_id),
                "water_meter_type_id": str(project_type.water_meter_type_id),
                "water_meter_type_name": project_type.water_meter_type_name,
                "water_meter_type_create_date": str(project_type.water_meter_type_create_date),
                "water_meter_type_other_information": project_type.water_meter_type_other_information,
                "water_meter_type_files": project_type.water_meter_type_files,
                "water_meter_tag": {
                    "water_meter_tag_name": project_type.water_meter_tag.water_meter_tag_name,
                    "water_meter_tag_id": str(project_type.water_meter_tag.water_meter_tag_id),
                    "water_meter_tag_create_date": str(project_type.water_meter_tag.water_meter_tag_create_date),
                }
            }
            type_info_list.append(type_info)
        return type_info_list

    def as_dict_for_get_all(self):
        response = {
            "admin_info": str(self.admin_id),
            "water_meter_project_name": self.water_meter_project_name,
            "water_meter_project_id": str(self.water_meter_project_id),
            "water_meter_project_create_date": str(self.water_meter_project_create_date),
            "water_meter_project_title": self.water_meter_project_title,
            "water_meter_project_start_date": str(self.water_meter_project_start_date),
            "water_meter_project_employer_description": self.water_meter_project_employer_description,
            "water_meter_project_contract_number": self.water_meter_project_contract_number,
            "water_meter_project_other_information": self.water_meter_project_other_information,
            "water_meter_project_files": self.water_meter_project_files,
            "water_meters_with_this_id": {
                "All_water_meter_with_this_id": str(self.all_meter_info()['All_water_meter_with_this_id']),
                "sum_off_all_water_meter": self.all_meter_info()['sum_off_all_water_meter'],
            },
            "all_users_in_project": self.all_meter_info()['all_users_in_project'],
            'types': self.project_types()
        }
        return response


# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------Meter model-----------------------------------------------------------

class CustomMeterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        count = WaterMeters.objects.count()
        for obj in queryset:
            serialized_obj = {
                # Add any other custom fields you want to include in the response
                "water_meter_name": obj.water_meter_name,
                "water_meter_serial": obj.water_meter_serial,
                "water_meter_location": obj.water_meter_location,
                "water_meter_validation": obj.water_meter_validation,
                "water_meter_activation": obj.water_meter_activation,
                "water_meter_condition": obj.water_meter_condition,
                "other_information": obj.other_information,
                "water_meter_size": obj.water_meter_size,
                "water_meter_model": obj.water_meter_model,
                "water_meter_create_date": str(obj.water_meter_create_date),
                # "water_meter_status": self.check_records(water_meter_serial=obj.water_meter_serial),
                "water_meter_bill": obj.water_meter_bill,
                "water_meter_manual_number": obj.water_meter_manual_number,
                "water_meter_order_mode": obj.water_meter_order_mode,
                "water_meter_type_info": {
                    "water_meter_type_name": obj.water_meter_type.water_meter_type_name,
                    # "water_meter_type_id": obj.water_meter_type.water_meter_type_id,
                    # "water_meter_type_create_date": obj.water_meter_type.water_meter_type_create_date,
                },

                "water_meter_tag_info": {
                    "water_meter_tag_name": obj.water_meter_type.water_meter_tag.water_meter_tag_name,
                    "water_meter_tag_id": obj.water_meter_type.water_meter_tag.water_meter_tag_id,
                    "water_meter_tag_create_date": str(obj.water_meter_type.water_meter_tag.water_meter_tag_create_date)
                },
                # "water_meter_user_info": {},
                # "water_meter_project_info": {},
                # "water_meter_module_info": {},
                "all_water_meters": count,
            }
            # check for user
            if obj.water_meter_user is not None:
                # user_obj = obj.water_meter_user.as_dict()
                serialized_obj['water_meter_user_info'] = {
                    "user_id": obj.water_meter_user.user_id,
                    "user_name": obj.water_meter_user.user_name,
                    "user_lastname": obj.water_meter_user.user_lastname,
                    "user_phone": obj.water_meter_user.user_phone,
                    "other_information": obj.water_meter_user.other_information,
                }
            # end check
            elif obj.water_meter_user is None:
                serialized_obj['water_meter_user_info'] = {
                    "user": "User is None"
                }
            # end check for user

            # check for project
            if obj.water_meter_project is not None:
                serialized_obj['water_meter_project_info'] = {
                    "project_id": obj.water_meter_project.water_meter_project_id,
                    "project_name": obj.water_meter_project.water_meter_project_name,
                    "project_title": obj.water_meter_project.water_meter_project_title,
                    "project_create_date": str(obj.water_meter_project.water_meter_project_create_date),
                }
            elif obj.water_meter_project is None:
                serialized_obj['water_meter_project_info'] = {
                    "project": "Project is None"
                }
            # end check for project

            # check for module
            if obj.water_meter_module is not None:
                serialized_obj['water_meter_module_info'] = {
                    "water_meter_module_id": obj.water_meter_module.water_meter_module_id,
                    "water_meter_module_code": obj.water_meter_module.water_meter_module_code,
                    "water_meter_module_name": obj.water_meter_module.water_meter_module_name,
                    "water_meter_module_unit": obj.water_meter_module.water_meter_module_unit,
                    "water_meter_module_create_date": str(obj.water_meter_module.water_meter_module_create_date),
                    "water_meter_module_other_information": obj.water_meter_module.water_meter_module_other_information,
                }
            elif obj.water_meter_module is None:
                serialized_obj['water_meter_module_info'] = {
                    "module": "module is None"
                }
            serialized_data.append(serialized_obj)
        return serialized_data

    def check_records(self, water_meter_serial):
        consumption = WaterMetersConsumptions.objects.filter(water_meters=water_meter_serial).order_by(
            'create_time').last()
        current_time = datetime.now().date()
        result = {
            "status": (),
            "last_consumption_time": "",
            "current_time": current_time,
        }
        if consumption is not None:
            last_cons_time = consumption.create_time.date()
            delta_time = current_time - last_cons_time
            result['last_consumption_time'] = str(last_cons_time)
            if delta_time.days <= 1:
                result['status'] = ('Ok', delta_time.days)
            else:
                result['status'] = ('Not Ok', delta_time.days)
        elif consumption is None:
            result['status'] = ()
            result['last_consumption_time'] = None
        return result


class WaterMeters(models.Model):
    ORDER_MODE_CHOICE = [
        ('R', 'RealTime'),
        ('P', 'Periodic'),
    ]
    water_meter_admin = models.ForeignKey(Admins, on_delete=models.DO_NOTHING)
    water_meter_user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, default=None, null=True)
    water_meter_serial = models.CharField(primary_key=True, max_length=100)
    water_meter_location = models.JSONField()
    water_meter_validation = models.IntegerField(default=0)
    water_meter_activation = models.IntegerField(default=0)
    water_meter_condition = models.IntegerField(default=0)
    other_information = models.JSONField()
    water_meter_create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    water_meter_type = models.ForeignKey(WaterMetersTypes, on_delete=models.DO_NOTHING)
    water_meter_project = models.ForeignKey(WaterMetersProjects, on_delete=models.DO_NOTHING, default=None, null=True)
    water_meter_name = models.CharField(max_length=200, default='TestName')
    water_meter_module = models.OneToOneField('WaterMetersModules', null=True, on_delete=models.DO_NOTHING)
    water_meter_bill = models.BooleanField(default=True)
    water_meter_manual_number = models.FloatField(null=True)
    water_meter_order_mode = models.CharField(max_length=200, null=True, blank=True, choices=ORDER_MODE_CHOICE)
    water_meter_size = models.IntegerField(null=True)
    water_meter_model = models.CharField(max_length=200, null=True)
    objects = CustomMeterManager()

    class Meta:
        db_table = 'WaterMeters'
        indexes = [
            models.Index(fields=['water_meter_serial', 'water_meter_type', 'water_meter_project'])]

    # water_meter_tag = models.CharField(max_length=200, default='TagName')
    def get_last_bill_info(self):

        bill_object = Bills.objects.filter(bill_water_meter=self.water_meter_serial).last()
        if bill_object is not None:
            response = bill_object.as_dict()
            response.pop('bill_user_info')
            response.pop('bill_admin_info')
            response.pop('bill_water_meter')
        else:
            response = {}
        return response

    def check_records(self):
        consumption = WaterMetersConsumptions.objects.filter(water_meters=self.water_meter_serial).order_by(
            'create_time').last()
        current_time = datetime.now().date()
        result = {
            "status": (),
            "last_consumption_time": "",
            "current_time": current_time,
            # "cumulative_value": consumption.cumulative_value,
            # "sum_all_value": consumption.sum_all_value,
        }
        if consumption is not None:
            last_cons_time = consumption.create_time.date()
            delta_time = current_time - last_cons_time
            result['last_consumption_time'] = last_cons_time
            if delta_time.days <= 1:
                result['status'] = ('Ok', delta_time.days)
            else:
                result['status'] = ('Not Ok', delta_time.days)
        elif consumption is None:
            result['status'] = ()
            result['last_consumption_time'] = None
        return result

    def get_all_obj_count(self):
        all_water_meter_count = WaterMeters.objects.count()
        return all_water_meter_count

    def as_dict(self):
        water_meter_user = self.water_meter_user
        if water_meter_user != None:
            water_meter_user = self.water_meter_user.as_dict()
        else:
            water_meter_user = "User Is None"
        water_meter_project = self.water_meter_project
        if water_meter_project != None:
            water_meter_project = self.water_meter_project.as_dict()
        else:
            water_meter_project = "Project Is None"
        # module
        water_meter_module = self.water_meter_module
        if water_meter_module != None:
            water_meter_module = self.water_meter_module.as_dict()
        else:
            water_meter_module = "Module Is None"
        return {
            "admin": self.water_meter_admin.as_dict(),
            "user": water_meter_user,
            "water_meter_type_info": self.water_meter_type.as_dict(),
            "water_meter_project_info": water_meter_project,
            "water_meter_serial": self.water_meter_serial,
            "water_meter_location": self.water_meter_location,
            "water_meter_validation": self.water_meter_validation,
            "water_meter_activation": self.water_meter_activation,
            "water_meter_condition": self.water_meter_condition,
            "other_information": self.other_information,
            "water_meter_name": self.water_meter_name,
            'water_meter_create_date': self.water_meter_create_date,
            "water_meter_module_info": water_meter_module,
            "water_meter_bill": self.water_meter_bill,
            "water_meter_manual_number": self.water_meter_manual_number,
            "water_meter_order_mode": self.water_meter_order_mode,
        }

    def as_dict_customise(self):
        return {
            "admin": self.water_meter_admin.as_dict_customise(),
            "user": self.water_meter_user.as_dict_customise(),
            "water_meter_serial": self.water_meter_serial
        }

    def as_dict_for_get_all(self):
        water_meter_info = {
            "water_meter_name": self.water_meter_name,
            "water_meter_serial": self.water_meter_serial,
            "water_meter_location": self.water_meter_location,
            "water_meter_validation": self.water_meter_validation,
            "water_meter_activation": self.water_meter_activation,
            "water_meter_condition": self.water_meter_condition,
            "other_information": self.other_information,
            "water_meter_create_date": str(self.water_meter_create_date),
            "water_meter_status": self.check_records(),
            "water_meter_bill": self.water_meter_bill,
            # "water_meter_last_bill_info": self.get_last_bill_info(),
            "water_meter_manual_number": self.water_meter_manual_number,
            "water_meter_order_mode": self.water_meter_order_mode,
            "water_meter_type_info": {
                "water_meter_type_name": self.water_meter_type.water_meter_type_name,
                "water_meter_type_id": self.water_meter_type.water_meter_type_id,
                "water_meter_type_create_date": str(self.water_meter_type.water_meter_type_create_date),
            },

            "water_meter_tag_info": {
                "water_meter_tag_name": self.water_meter_type.water_meter_tag.water_meter_tag_name,
                "water_meter_tag_id": self.water_meter_type.water_meter_tag.water_meter_tag_id,
                "water_meter_tag_create_date": str(self.water_meter_type.water_meter_tag.water_meter_tag_create_date)
            },
            "water_meter_user_info": {},
            "water_meter_project_info": {},
            "water_meter_module_info": {},
            "all_water_meters": self.get_all_obj_count(),
        }
        # check for user
        if self.water_meter_user is not None:

            water_meter_info['water_meter_user_info'] = {
                "user_id": self.water_meter_user.user_id,
                "user_name": self.water_meter_user.user_name,
                "user_lastname": self.water_meter_user.user_lastname,
                "user_phone": self.water_meter_user.user_phone,
                "other_information": self.water_meter_user.other_information,
            }
        elif self.water_meter_user is None:
            water_meter_info['water_meter_user_info'] = {
                "user": "User is None"
            }
        # end check for user

        # check for project
        if self.water_meter_project is not None:
            water_meter_info['water_meter_project_info'] = {
                "project_id": self.water_meter_project.water_meter_project_id,
                "project_name": self.water_meter_project.water_meter_project_name,
                "project_title": self.water_meter_project.water_meter_project_title,
                "project_create_date": str(self.water_meter_project.water_meter_project_create_date),
            }
        elif self.water_meter_project is None:
            water_meter_info['water_meter_project_info'] = {
                "project": "Project is None"
            }
        # end check for project

        # check for module
        if self.water_meter_module is not None:
            water_meter_info['water_meter_module_info'] = {
                "water_meter_module_id": self.water_meter_module.water_meter_module_id,
                "water_meter_module_code": self.water_meter_module.water_meter_module_code,
                "water_meter_module_name": self.water_meter_module.water_meter_module_name,
                "water_meter_module_unit": self.water_meter_module.water_meter_module_unit,
                "water_meter_module_create_date": str(self.water_meter_module.water_meter_module_create_date),
                "water_meter_module_other_information": self.water_meter_module.water_meter_module_other_information,
            }
        elif self.water_meter_module is None:
            water_meter_info['water_meter_module_info'] = {
                "module": "module is None"
            }
        # end check for module
        # self.check_records(water_meter_serial=self.water_meter_serial)
        return water_meter_info

    # def __str__(self):
    #     # json.dumps(self.data)
    #     return json.dumps(self.as_dict_for_get_all())


# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------Bills model-----------------------------------------------------------

class Bills(models.Model):
    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    bill_admin = models.ForeignKey(Admins, on_delete=models.DO_NOTHING)
    bill_water_meter = models.ForeignKey(WaterMeters, on_delete=models.DO_NOTHING)
    bill_serial = models.CharField(unique=True, null=True, max_length=200)
    bill_start_date = models.DateField(null=True)
    bill_end_date = models.DateField(null=True)
    payment_dead_line = models.DateField(null=True)
    bill_create_date = models.DateField(auto_now_add=True, blank=True)
    consumptions = models.FloatField()
    bill_price = models.FloatField(null=True, blank=True)
    other_information = models.JSONField()
    bill_link = models.CharField(max_length=255, null=True)
    bill_link_validation = models.BooleanField(default=False)

    class Meta:
        db_table = 'Bills'

    def as_dict(self):
        bill_user_info = {
            "user_id": self.bill_user.user_id,
            "user_name": self.bill_user.user_name,
            "user_lastname": self.bill_user.user_lastname,
            "user_phone": self.bill_user.user_phone
        }
        bill_admin_info = {
            "admin_id": self.bill_admin.admin_id,
            "admin_name": self.bill_admin.admin_name,
            "admin_lastname": self.bill_admin.admin_lastname
        }
        if self.bill_water_meter.water_meter_project is not None:

            water_meter_project_info = {
                "water_meter_project_id": self.bill_water_meter.water_meter_project.water_meter_project_id,
                "water_meter_project_name": self.bill_water_meter.water_meter_project.water_meter_project_name,
                "water_meter_project_title": self.bill_water_meter.water_meter_project.water_meter_project_title,
                "water_meter_project_files": self.bill_water_meter.water_meter_project.water_meter_project_files,
                "water_meter_project_start_date": str(
                    self.bill_water_meter.water_meter_project.water_meter_project_start_date),
                "water_meter_project_employer_description": self.bill_water_meter.water_meter_project.water_meter_project_employer_description,
                "water_meter_project_contract_number": self.bill_water_meter.water_meter_project.water_meter_project_contract_number,
                "water_meter_project_images": self.bill_water_meter.water_meter_project.water_meter_project_images,
                "water_meter_project_urls": self.bill_water_meter.water_meter_project.water_meter_project_urls,
            }
            # pattern_object = Pattern.objects.filter(
            #     pattern_project=self.bill_water_meter.water_meter_project.water_meter_project_id)
            # pattern_list = [pattern.pattern_list for pattern in pattern_object][0]
            # bill_pattern_info = {
            #     "pattern_list": pattern_list
            # }
        else:
            # water_meter_project_info = None
            bill_pattern_info = None
        if self.bill_water_meter.water_meter_type is not None:
            water_meter_type_info = {
                "water_meter_type_id": self.bill_water_meter.water_meter_type.water_meter_type_id,
                "water_meter_type_name": self.bill_water_meter.water_meter_type.water_meter_type_name,
                "water_meter_tag_info": {
                    "water_meter_tag_name": self.bill_water_meter.water_meter_type.water_meter_tag.water_meter_tag_name,
                    "water_meter_tag_id": self.bill_water_meter.water_meter_type.water_meter_tag.water_meter_tag_id,
                },
            }
        else:
            water_meter_type_info = None
        if self.bill_water_meter.water_meter_module is not None:
            water_meter_module_info = {
                "water_meter_module_id": self.bill_water_meter.water_meter_module.water_meter_module_id,
                "water_meter_module_code": self.bill_water_meter.water_meter_module.water_meter_module_code,
                "water_meter_module_name": self.bill_water_meter.water_meter_module.water_meter_module_name,
            }
        else:
            water_meter_module_info = None
        bill_water_meter_info = {
            "water_meter_serial": self.bill_water_meter.water_meter_serial,
            "water_meter_name": self.bill_water_meter.water_meter_name,
            "water_meter_activation": self.bill_water_meter.water_meter_activation,
            "water_meter_validation": self.bill_water_meter.water_meter_validation,
            "water_meter_condition": self.bill_water_meter.water_meter_condition,
            "water_meter_location": self.bill_water_meter.water_meter_location,
            "water_meter_create_date": str(self.bill_water_meter.water_meter_create_date),
            "other_information": self.bill_water_meter.other_information,
            "water_meter_project_info": water_meter_project_info,
            "water_meter_type_info": water_meter_type_info,
            "water_meter_module_info": water_meter_module_info
        }

        return {
            "bill_user_info": bill_user_info,
            "bill_admin_info": bill_admin_info,
            "bill_id": self.bill_id,
            "bill_serial": self.bill_serial,
            "bill_start_date": str(self.bill_start_date),
            "bill_end_date": str(self.bill_end_date),
            "payment_dead_line": str(self.payment_dead_line),
            "bill_create_date": str(self.bill_create_date),
            "consumptions": self.consumptions,
            "bill_price": self.bill_price,
            "other_information": self.other_information,
            "bill_water_meter": bill_water_meter_info,
            "bill_link": self.bill_link,
            "bill_link_validation": self.bill_link_validation,
            # "bill_pattern_info": bill_pattern_info,
        }

# ----------------------------------------------------------------------------------------------------------------------
