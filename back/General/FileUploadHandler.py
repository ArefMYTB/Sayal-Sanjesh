import os
import uuid
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import FileResponse


class FileManager:

    def File_upload_handler(self, file, folder_name, owner_name):
        base_dir = os.getcwd()
        # system_base_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        media_path = os.path.join(base_dir, 'media')
        if owner_name == 'Admin':
            base_url_path = os.path.join('media')
            # base_url_path = os.path.join(base_url_path, 'Admin')
            # base_url_path = os.path.join(base_url_path, folder_name)
            # base_url_path = os.path.join(base_url_path, file.name)
            # admin_path = os.path.join(media_path, 'Admin')
            uuid_key = uuid.uuid4()

            # save file in media folder .
            file_name = file.name
            file_name = file_name.split('.')
            unique_file_name = f"{uuid_key}_{file_name[0]}.{file_name[1]}"
            # file_path = os.path.join(base_url_path, unique_file_name)

            fs = FileSystemStorage(location=media_path)
            file_save = fs.save(unique_file_name, file)
            fileurl = fs.url(file_save)

            result = {
                # 'file_location': file_path,
                'fileurl': fileurl
            }
            return result

        elif owner_name == 'User':
            admin_path = os.path.join(media_path, 'User')
            path = os.path.join(admin_path, folder_name)
            base_url_path = os.path.join('media')
            base_url_path = os.path.join(base_url_path, 'User')
            uuid_key = uuid.uuid4()

            # save file in media folder .
            file_name = file.name
            file_name = file_name.split('.')
            unique_file_name = f"{uuid_key}_{file_name[0]}.{file_name[1]}"
            file_path = os.path.join(base_url_path, unique_file_name)

            fs = FileSystemStorage(location=media_path)
            file_save = fs.save(unique_file_name, file)
            fileurl = fs.url(file_save)

            result = {
                'file_location': file_path,
                'fileurl': fileurl
            }
            return result
            # base_url_path = os.path.join(base_url_path, folder_name)
            # base_url_path = os.path.join(base_url_path, file.name)
            # fs = FileSystemStorage(location=path)
            # old_file_path = os.path.join(path, file.name)
            # old_file_exists = os.path.exists(old_file_path)
            # if old_file_exists:
            #     # os.remove(old_file_path)
            #     filez = fs.save(file.name, file)
            # else:
            #     filez = fs.save(file.name, file)
            # fileurl = fs.url(base_url_path)
            # final_file_path = os.path.join(path, file.name)
            # result = {
            #     'file_location': final_file_path,
            #     'fileurl': fileurl
            # }
            # return result

        elif owner_name == 'Project':
            project_path = os.path.join(media_path, 'Project')
            path = os.path.join(project_path, folder_name)
            base_url_path = os.path.join('media')
            base_url_path = os.path.join(base_url_path, 'Project')
            base_url_path = os.path.join(base_url_path, folder_name)
            base_url_path = os.path.join(base_url_path, file.name)
            fs = FileSystemStorage(location=path)
            old_file_path = os.path.join(path, file.name)
            old_file_exists = os.path.exists(old_file_path)
            if old_file_exists:
                os.remove(old_file_path)
                filez = fs.save(file.name, file)
            else:
                filez = fs.save(file.name, file)
            fileurl = fs.url(base_url_path)
            final_file_path = os.path.join(path, file.name)
            result = {
                'file_location': final_file_path,
                'fileurl': fileurl
            }
            return result

        elif owner_name == 'Type':
            project_path = os.path.join(media_path, 'Type')
            path = os.path.join(project_path, folder_name)
            base_url_path = os.path.join('media')
            base_url_path = os.path.join(base_url_path, 'Type')
            base_url_path = os.path.join(base_url_path, folder_name)
            base_url_path = os.path.join(base_url_path, file.name)
            fs = FileSystemStorage(location=path)
            old_file_path = os.path.join(path, file.name)
            old_file_exists = os.path.exists(old_file_path)
            if old_file_exists:
                os.remove(old_file_path)
                filez = fs.save(file.name, file)
            else:
                filez = fs.save(file.name, file)
            fileurl = fs.url(base_url_path)
            final_file_path = os.path.join(path, file.name)
            result = {
                'file_location': final_file_path,
                'fileurl': fileurl
            }
            return result

        elif owner_name == 'Tag':
            project_path = os.path.join(media_path, 'Tag')
            path = os.path.join(project_path, folder_name)
            base_url_path = os.path.join('media')
            base_url_path = os.path.join(base_url_path, 'Tag')
            base_url_path = os.path.join(base_url_path, folder_name)
            base_url_path = os.path.join(base_url_path, file.name)
            fs = FileSystemStorage(location=path)
            old_file_path = os.path.join(path, file.name)
            old_file_exists = os.path.exists(old_file_path)
            if old_file_exists:
                os.remove(old_file_path)
                filez = fs.save(file.name, file)
            else:
                filez = fs.save(file.name, file)
            fileurl = fs.url(base_url_path)
            final_file_path = os.path.join(path, file.name)
            result = {
                'file_location': final_file_path,
                'fileurl': fileurl
            }
            return result

        elif owner_name == 'Notice':
            user_path = os.path.join(media_path, 'User')
            path = os.path.join(user_path, folder_name)
            base_url_path = os.path.join('media')
            base_url_path = os.path.join(base_url_path, 'User')
            base_url_path = os.path.join(base_url_path, folder_name)
            base_url_path = os.path.join(base_url_path, 'NoticesFile')
            base_url_path = os.path.join(base_url_path, file.name)
            fs = FileSystemStorage(location=path)
            old_file_path = os.path.join(path, file.name)
            old_file_exists = os.path.exists(old_file_path)
            if old_file_exists:
                os.remove(old_file_path)
                filez = fs.save(file.name, file)
            else:
                filez = fs.save(file.name, file)
            fileurl = fs.url(base_url_path)
            final_file_path = os.path.join(path, file.name)
            result = {
                'file_location': final_file_path,
                'fileurl': fileurl
            }
            return result

        elif owner_name == 'App':
            app_path = os.path.join(media_path, 'App')
            path = os.path.join(app_path, folder_name)
            base_url_path = os.path.join('media')
            base_url_path = os.path.join(base_url_path, 'App')
            base_url_path = os.path.join(base_url_path, folder_name)
            fs = FileSystemStorage(location=path)
            old_file_path = os.path.join(path, file.name)
            old_file_exists = os.path.exists(old_file_path)
            if old_file_exists:
                os.remove(old_file_path)
                filez = fs.save(file.name, file)
            else:
                filez = fs.save(file.name, file)
            final_url = os.path.join(base_url_path,file.name)
            # app = 'App'
            # app_path = os.path.join(app,folder_name)
            # final_app_path = os.path.join(app_path,file.name)
            fileurl = fs.url(final_url)
            final_file_path = os.path.join(path, file.name)
            result = {
                'file_location': final_file_path,
                'fileurl': fileurl
            }
            return result
