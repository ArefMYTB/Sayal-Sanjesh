import uuid
import os
from django.core.files.storage import FileSystemStorage
from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
# from SayalSanjesh.Serializers.AdminsSerializer import AdminsSerializer
from Authorization.models.Admins import Admins
from General.FileUploadHandler import FileManager
from django.conf import settings


class UploadSerializer:
    """
            This class is responsible for serializing data in our Django app
    """
    @staticmethod
    def upload(file):
        """
            param : [file]

            return :
            A tuple containing a boolean indicating the success or failure of the operation, and a list of serialized data
            results.
        """
        # generate uuid for dont save repetitive file .
        uuid_key = uuid.uuid4()

        # save file in media folder .
        file_name = file.name
        file_name = file_name.split('.')
        unique_file_name = f"{uuid_key}_{file_name[0]}.{file_name[1]}"
        media_path = settings.MEDIA_ROOT
        file_path = os.path.join(media_path, unique_file_name)

        fs = FileSystemStorage(location=media_path)
        file_save = fs.save(unique_file_name, file)
        fileurl = fs.url(file_save)

        result = {
            'file_location': file_path,
            'fileurl': fileurl
        }

        # get link and create result .

        return True, result

    @staticmethod
    def admin_upload_file_serializer(token, file):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            # generate uuid for dont save repetitive file .
            uuid_key = uuid.uuid4()

            # save file in media folder .
            file_name = file.name
            file_name = file_name.split('.')
            unique_file_name = f"{uuid_key}_{file_name[0]}.{file_name[1]}"
            media_path = settings.MEDIA_ROOT
            file_path = os.path.join(media_path, unique_file_name)

            fs = FileSystemStorage(location=media_path)
            file_save = fs.save(unique_file_name, file)
            fileurl = fs.url(file_save)

            result = {
                'file_location': file_path,
                'fileurl': fileurl
            }

            # get link and create result .

            return True, result

        else:
            return False, wrong_token_result
        # else:
        #     return False, wrong_token_result
