import uuid, os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, wrong_result
from SayalSanjesh.models.SnapShots import Snapshots
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from datetime import datetime
import jdatetime

class SnapShotSerializer:

    @staticmethod
    def admin_create_snap_shot_serializer(token, input_data):
        token_result = token_to_user_id(token)
        if token_result["status"] != "OK":
            return False, wrong_token_result

        admin_id = token_result["data"]["user_id"]

        if not AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
            return False, wrong_token_result

        # Date & Time
        create_date_str = input_data["create_date"]  # e.g., "2025-05-05"
        create_time_str = input_data["create_time"]  # e.g., "09:39"
        # Combine them into a datetime object
        combined_datetime_str = f"{create_date_str} {create_time_str}"
        combined_datetime = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")

        # Numeric Values
        mechanic_value = input_data.get("mechanic_value")
        cumulative_value = input_data.get("cumulative_value")
        # Handle empty strings or None by converting them to 0.0
        mechanic_value = float(mechanic_value) if mechanic_value not in [None, ""] else 0.0
        cumulative_value = float(cumulative_value) if cumulative_value not in [None, ""] else 0.0

        try:
            snapshot = Snapshots.objects.create(
                snapshot_watermeter_id=input_data["watermeter_id"],
                snapshot_create_time=combined_datetime,
                snapshot_admin_id=admin_id,
                snapshot_mechanic_value=mechanic_value,
                snapshot_cumulative_value=cumulative_value,
                snapshot_image=input_data.get("image", []),
                snapshot_text=input_data.get("text", "")
            )
            return True, {"snapshot_id": str(snapshot.snapshot_id)}
        except Exception as e:
            return False, {"farsi_message": "خطا در ایجاد برداشت", "english_message": f"Error in snapshot creation: {e}"}


    @staticmethod
    def admin_edit_snap_shot_serializer(token, input_data):
        token_result = token_to_user_id(token)
        if token_result["status"] != "OK":
            return False, wrong_token_result

        admin_id = token_result["data"]["user_id"]

        if not AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
            return False, wrong_token_result

        try:
            # Date & Time
            create_date_str = input_data["create_date"]  # e.g., "2025-05-05"
            create_time_str = input_data["create_time"]  # e.g., "09:39"
            # Combine them into a datetime object
            combined_datetime_str = f"{create_date_str} {create_time_str}"
            combined_datetime = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
            
            # Find the snapshot
            snapshot = Snapshots.objects.filter(
                snapshot_watermeter_id=input_data["watermeter_id"],
                snapshot_create_time=combined_datetime
            ).first()

            if not snapshot:
                return False, {"farsi_message": "برداشت یافت نشد", "english_message": "Snapshot not found"}
            
            # Update fields if provided
            if "mechanic_value" in input_data:
                snapshot.snapshot_mechanic_value = input_data["mechanic_value"]
            if "text" in input_data:
                snapshot.snapshot_text = input_data["text"]

            snapshot.save()
            return True, {"farsi_message": "با موفقیت ویرایش شد", "english_message": "Snapshot updated successfully"}

        except Exception as e:
            return False, {"farsi_message": "خطا در ویرایش", "english_message": f"Error during update: {e}"}


    @staticmethod
    def admin_remove_snap_shot_serializer(token, input_data):

        token_result = token_to_user_id(token)
        if token_result["status"] != "OK":
            return False, wrong_token_result

        admin_id = token_result["data"]["user_id"]

        if not AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
            return False, wrong_token_result

        # Get watermeter ID and datetime from input
        watermeter_id = input_data["watermeter_id"]
        create_date_str = input_data["create_date"] # e.g., "2025-05-05"
        create_time_str = input_data["create_time"]  # e.g., "09:39"

        if not watermeter_id or not create_date_str or not create_time_str:
            return False, {"farsi_message": "اطلاعات ناقص است", "english_message": "Missing data for deletion"}
        
        try:
            # convert Jalali date string to Gregorian datetime
            j_date = jdatetime.datetime.strptime(create_date_str, "%Y/%m/%d")
            g_date = j_date.togregorian()
            combined_datetime_str = f"{g_date.strftime('%Y-%m-%d')} {create_time_str}"
            combined_datetime = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M:%S")

            snapshot = Snapshots.objects.filter(
                snapshot_watermeter_id=watermeter_id,
                snapshot_create_time=combined_datetime
            ).first()

            if not snapshot:
                return False, {"farsi_message": "یافت نشد", "english_message": "Snapshot not found"}

            snapshot.delete()
            return True, {"farsi_message": "با موفقیت حذف شد", "english_message": "Snapshot deleted successfully"}
        except Exception as e:
            return False, {"farsi_message": "خطا در حذف", "english_message": f"Error in deletion: {e}"}



    @staticmethod
    def admin_get_all_snap_shots_serializer(request, token, page, count, user_id, water_meter_serial):
        """
            param : [token, page, count, user_id, water_meter_serial]
            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of
            serialized data results.  it returns a false status along with an error message.
        """
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin', 'MeterList']):
                fields = {
                    "page": (page, int),
                    "count": (count, int),
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    
                    response = {}
                    response['snapshots'] = []
                    try:
                        filters = {
                            'snapshot_watermeter__water_meter_serial': water_meter_serial,
                        }
                        queryset = Snapshots.objects.filter(**filters).order_by('-snapshot_create_time')[offset:offset + limit]
                        
                        for item in queryset:
                            response['snapshots'].append({
                                'admin': f'{item.snapshot_admin.admin_name} {item.snapshot_admin.admin_lastname}',
                                'create_time': item.snapshot_create_time,
                                'mechanic_value': item.snapshot_mechanic_value,
                                'cumulative_value': item.snapshot_cumulative_value,
                                'image': [
                                    request.build_absolute_uri(settings.MEDIA_URL + img_path.replace('/media/', '')) 
                                    for img_path in item.snapshot_image if img_path
                                ] if item.snapshot_image else None,
                                'text': item.snapshot_text,
                            })

                        else:
                            response['admin'] = None 

                    except Exception as e:
                        print(f"Error: {e}") 
                        response = []

                    return True, response
                else:
                    return field_result

            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_upload_snap_shot_serializer(token, file):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]

            
            print("uploading")
            if AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
                # generate uuid for dont save repetitive file .
                uuid_key = uuid.uuid4()

                # save file in media folder .
                file_name = file.name
                file_name = file_name.split('.')
                unique_file_name = f"{uuid_key}_{file_name[0]}.{file_name[1]}"
                media_path = os.path.join(settings.MEDIA_ROOT, "Snapshots")
                file_path = os.path.join(media_path, unique_file_name)
                fs = FileSystemStorage(location=media_path)
                file_save = fs.save(unique_file_name, file)
                # fileurl = fs.url(file_save)
                fileurl = f"/media/Snapshots/{file_save}"

                result = {
                    'file_location': file_path,
                    'fileurl': fileurl
                }
                print("uploaded: ", file_path, " -- ", fileurl)

                # get link and create result .

                return True, result

        else:
            return False, wrong_token_result