import uuid, os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, wrong_result
from SayalSanjesh.models.SnapShots import Snapshots
from Authorization.Serializers.AdminsSerializer import AdminsSerializer

class SnapShotSerializer:

    @staticmethod
    def admin_create_snap_shot_serializer(token, input_data):
        token_result = token_to_user_id(token)
        if token_result["status"] != "OK":
            return False, wrong_token_result

        admin_id = token_result["data"]["user_id"]

        if not AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
            return False, wrong_token_result
        
        try:
            snapshot = Snapshots.objects.create(
                snapshot_watermeter_id=input_data["watermeter_id"],
                snapshot_admin_id=admin_id,
                snapshot_mechanic_value=input_data.get("mechanic_value", 0.0),
                snapshot_cumulative_value=input_data.get("cumulative_value", 0.0),
                snapshot_image=input_data.get("image", []),
                snapshot_text=input_data.get("text", "")
            )
            return True, {"snapshot_id": str(snapshot.snapshot_id)}
        except Exception as e:
            return False, {"farsi_message": "خطا در ایجاد عکس‌برداری", "english_message": f"Error in snapshot creation: {e}"}


    @staticmethod
    def admin_edit_snap_shot_serializer(token, input_data):
        token_result = token_to_user_id(token)
        if token_result["status"] != "OK":
            return False, wrong_token_result

        admin_id = token_result["data"]["user_id"]

        if not AdminsSerializer.admin_check_permission(admin_id, ['SuperAdmin']):
            return False, wrong_token_result

        try:
            snapshot = Snapshots.objects.get(snapshot_id=input_data["snapshot_id"])
            snapshot.snapshot_mechanic_value = input_data.get("mechanic_value", snapshot.snapshot_mechanic_value)
            snapshot.snapshot_cumulative_value = input_data.get("cumulative_value", snapshot.snapshot_cumulative_value)
            snapshot.snapshot_image = input_data.get("image", snapshot.snapshot_image)
            snapshot.snapshot_text = input_data.get("text", snapshot.snapshot_text)
            snapshot.save()

            return True, {"snapshot_id": str(snapshot.snapshot_id)}
        except Snapshots.DoesNotExist:
            return False, {"farsi_message": "عکس‌برداری یافت نشد", "english_message": "Snapshot not found"}
        except Exception as e:
            return False, {"farsi_message": "خطا در ویرایش", "english_message": f"Error in editing: {e}"}


    @staticmethod
    def admin_get_all_snap_shots_serializer(token, page, count, user_id, water_meter_serial):
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
                                'image': item.snapshot_image if item.snapshot_image else None,
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