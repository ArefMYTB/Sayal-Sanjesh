from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, wrong_result
from SayalSanjesh.models.SnapShots import Snapshots
from Authorization.Serializers.AdminsSerializer import AdminsSerializer

class SnapShotSerializer:

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
                    try:
                        filters = {
                            'snapshot_watermeter__water_meter_serial': water_meter_serial,
                        }
                        queryset = Snapshots.objects.filter(**filters).order_by('-snapshot_create_time')[offset:offset + limit]
                        print("queryset: ", queryset)
                        
                        if queryset:
                            response['admin'] = f'{queryset[0].snapshot_admin.admin_name} {queryset[0].snapshot_admin.admin_lastname}'
                            response['create_time'] = queryset[0].snapshot_create_time
                            response['mechanic_value'] = queryset[0].snapshot_mechanic_value
                            response['cumulative_value'] = queryset[0].snapshot_cumulative_value
                            
                        else:
                            response['admin'] = None 

                        print(response)


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
