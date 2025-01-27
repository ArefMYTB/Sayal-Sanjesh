from Authorization.TokenManager import token_to_user_id
from SayalSanjesh.Serializers import wrong_token_result, status_success_result, wrong_data_result, wrong_result
from SayalSanjesh.models import  Notice, NoticeReplayAdmin, NoticeCategories, NoticeReplayUser
from Authorization.models.Users import Users
from Authorization.models.Admins import Admins
from Authorization.Serializers.AdminsSerializer import AdminsSerializer
from General.FileUploadHandler import FileManager


class NoticeSerializer:
    @staticmethod
    def admin_get_one_notice(token, notice_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Notice'):
                try:
                    notices = Notice.objects.get(notice_id=notice_id)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است notice_id"
                    wrong_data_result["english_message"] = "Wrong notice_id"
                    return False, wrong_data_result
                user_replays = NoticeReplayUser.objects.filter(
                    notice=notice_id)
                admin_replays = NoticeReplayAdmin.objects.filter(
                    notice=notice_id)
                all_replays = []
                for replay in user_replays:
                    replay = replay.as_dict()
                    replay.pop('notice_info')
                    replay.update({
                        'user_info': replay['user_info']['user_id']
                    })
                    all_replays.append(replay)
                for replay in admin_replays:
                    replay = replay.as_dict()
                    replay.pop('notice_info')
                    replay.update({
                        'admin_info': replay['admin_info']['admin_id']
                    })
                    all_replays.append(replay)
                all_replays = sorted(
                    all_replays, key=lambda message: message['create_time'], reverse=True)
                notice_info = notices.as_dict()
                notice_category_info = {
                    'category_id': notice_info['notice_category_info']['category_id'],
                    'category_name': notice_info['notice_category_info']['category_name']
                }
                result = {
                    "notice_category_info": notice_category_info,
                    "notice_id": notices.notice_id,
                    "title": notices.title,
                    "message": notices.message,
                    "create_date": notices.create_date,
                    "attachment": notices.attachment,
                    "all_replays": all_replays,
                }
                return True, result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_notice_serializer(token, page, count, title, message, create_date, attachment):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Notice'):
                fields = {
                    "page": (page, int),
                    "count": (count, int)
                }
                field_result = wrong_result(fields)
                if field_result == None:
                    offset = int((page - 1) * count)
                    limit = int(count)
                    all_notices = Notice.objects.filter(title__contains=title, message__contains=message,
                                                        create_date__contains=create_date,
                                                        attachment__contains=attachment).order_by(
                        '-create_date')[offset:offset + limit]
                    tableCount = (Notice.objects.count())
                    noticeResult = []
                    all_replays = []
                    user_replays = NoticeReplayUser.objects.filter(notice__in=all_notices)
                    admin_replays = NoticeReplayAdmin.objects.filter(notice__in=all_notices)
                    if len(user_replays) != 0:
                        for replay in user_replays:
                            replay = replay.as_dict()
                            replay.pop('notice_info')
                            replay.update({
                                'user_info': replay['user_info']['user_id']
                            })
                            all_replays.append(replay)
                    if len(admin_replays) != 0:
                        for replay in admin_replays:
                            replay = replay.as_dict()
                            replay.pop('notice_info')
                            replay.update({
                                'admin_info': replay['admin_info']['admin_id']
                            })
                            all_replays.append(replay)
                    if len(all_replays) != 0:
                        all_replays = sorted(
                            all_replays, key=lambda message: message['create_time'], reverse=True)
                    for notice in all_notices:
                        notice_result = {
                            "notice_id": notice.notice_id,
                            "title": notice.title,
                            "message": notice.message,
                            "create_date": notice.create_date,
                            "attachment": notice.attachment,
                            "notice_files": notice.notice_files,
                            "notice_category_info": {
                                "category_id": notice.notice_category.category_id,
                                "category_name": notice.notice_category.category_name,
                                "category_index": notice.notice_category.category_index,
                                "create_date": notice.notice_category.create_date,

                            },
                            "notice_user_info": {
                                "user_id": notice.user.user_id,
                                "user_name": notice.user.user_name,
                                "user_phone": notice.user.user_phone,
                            },
                            "replays": all_replays,
                            "all_notices": tableCount
                        }
                        noticeResult.append(notice_result)

                    return True, noticeResult
                else:
                    return field_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_my_notice(token):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Notice'):
                all_notices = NoticeReplayAdmin.objects.filter(
                    admin_id=admin_id)
                results = [notice.as_dict() for notice in all_notices]
                for result in results:
                    notice_info = {
                        'notice_title': result['notice_info']['title'],
                        'notice_message': result['notice_info']['message']
                    }
                    admin_info = {
                        'admin_name': result['admin_info']['admin_name'],
                        'admin_lastname': result['admin_info']['admin_lastname']
                    }
                    result['notice_info'] = notice_info
                    result['admin_info'] = admin_info
                return True, results
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_replay_notice(token, notice, message):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminsSerializer.admin_check_permission(admin_id, 'Notice'):
                replay = NoticeReplayAdmin()
                try:
                    notice = Notice.objects.get(notice_id=notice)
                except:
                    wrong_data_result["farsi_message"] = "اشتباه است،notice_id"
                    wrong_data_result["english_message"] = "Wrong notice_id"
                    return False, wrong_data_result
                admin = Admins.objects.get(admin_id=admin_id)
                fields = {
                    "message": (message, str)
                }
                result = wrong_result(fields)
                if result == None:
                    replay.message = message
                    replay.notice = notice
                    replay.admin = admin
                    replay.save()
                    return True, status_success_result
                else:
                    return result
            else:
                return False, wrong_token_result

    @staticmethod
    def user_create_notice(token, notice_category, title, message, attachment, filepath):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            notice = Notice()
            user = Users.objects.get(user_id=user_id)
            try:
                category = NoticeCategories.objects.get(
                    category_id=notice_category)
            except:
                wrong_data_result["farsi_message"] = "category_id اشتباه است"
                wrong_data_result["english_message"] = "Wrong category_id"
                return False, wrong_data_result
            fields = {
                "title": (title, str),
                "message": (message, str),
            }
            result = wrong_result(fields)
            if result == None:
                notice.notice_category = category
                notice.title = title
                notice.message = message
                notice.user = user
                notice.attachment = attachment
                if filepath != "":
                    # folder_name = str(water_meter_project.water_meter_project_id)
                    # file_manager = FileManager()
                    # file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                    #                                                owner_name='Project')
                    # water_meter_project.water_meter_project_files.append(file_result)
                    folder_name = str(user.user_phone)
                    file_manager = FileManager()
                    file_result = file_manager.File_upload_handler(file=filepath, folder_name=folder_name,
                                                                   owner_name='Notice')

                    notice.notice_files.append(file_result)
                    notice.save()
                notice.save()
                return True, status_success_result
            else:
                return result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_replay_notice(token, notice, message):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            replay = NoticeReplayUser()
            user = Users.objects.get(user_id=user_id)
            try:
                notice = Notice.objects.get(notice_id=notice)
            except:
                wrong_data_result["farsi_message"] = "notice_id اشتباه است"
                wrong_data_result["english_message"] = "Wrong notice_id"
                return False, wrong_data_result
            fields = {
                "message": (message, str)
            }
            result = wrong_result(fields)
            if result == None:
                replay.notice = notice
                replay.user = user
                replay.message = message
                replay.save()
                return True, status_success_result
            else:
                return result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_my_notice(token):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            all_replays = NoticeReplayUser.objects.filter(
                user=user_id)
            results = [replay.as_dict() for replay in all_replays]
            for result in results:
                notice_info = {
                    'notice_title': result['notice_info']['title'],
                    'notice_message': result['notice_info']['message'],
                }
                user_info = {
                    'user_name': result['user_info']['user_name'],
                    'user_phone': result['user_info']['user_phone']
                }
                result['notice_info'] = notice_info
                result['user_info'] = user_info
            return True, results
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_notice(token, notice_id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            try:
                notices = Notice.objects.get(notice_id=notice_id)
            except:
                wrong_data_result["farsi_message"] = "notice_id اشتباه است"
                wrong_data_result["english_message"] = "Wrong notice_id"
                return False, wrong_data_result
            user_replays = NoticeReplayUser.objects.filter(notice=notice_id)

            admin_replays = NoticeReplayAdmin.objects.filter(notice=notice_id)
            all_replays = []
            for replay in user_replays:
                replay = replay.as_dict()
                replay.pop('notice_info')
                replay.update({
                    'user_info': replay['user_info']['user_id']
                })
                all_replays.append(replay)
            for replay in admin_replays:
                replay = replay.as_dict()
                replay.pop('notice_info')
                replay.update({
                    'admin_info': replay['admin_info']['admin_id']
                })
                all_replays.append(replay)
            all_replays = sorted(
                all_replays, key=lambda message: message['create_time'], reverse=True)
            notice_info = notices.as_dict()
            notice_category_info = {
                'category_id': notice_info['notice_category_info']['category_id'],
                'category_name': notice_info['notice_category_info']['category_name']
            }
            user_info = {
                'user_id': notice_info['user_info']['user_id'],
                'user_name': notice_info['user_info']['user_name']
            }
            result = {
                "notice_category_info": notice_category_info,
                "user_info": user_info,
                "notice_id": notices.notice_id,
                "title": notices.title,
                "message": notices.message,
                "create_date": notices.create_date,
                "attachment": notices.attachment,
                "replays": all_replays
            }
            return True, result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_notice_serializer(token, page, count, title, message, create_date, attachment):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            fields = {
                "page": (page, int),
                "count": (count, int)
            }
            field_result = wrong_result(fields)
            if field_result == None:
                offset = int((page - 1) * count)
                limit = int(count)
                all_notices = Notice.objects.filter(user_id=user_id, title__contains=title, message__contains=message,
                                                    create_date__contains=create_date,
                                                    attachment__contains=attachment)
                all_notices_pagination = all_notices.order_by('-create_date')[offset:offset + limit]
                tableCount = all_notices.count()
                noticeResult = []
                all_replays = []
                user_replays = NoticeReplayUser.objects.filter(notice__in=all_notices_pagination)
                admin_replays = NoticeReplayAdmin.objects.filter(notice__in=all_notices_pagination)
                if len(user_replays) != 0:
                    for replay in user_replays:
                        replay = replay.as_dict()
                        replay.pop('notice_info')
                        replay.update({
                            'user_info': replay['user_info']['user_id']
                        })
                        all_replays.append(replay)
                if len(admin_replays) != 0:
                    for replay in admin_replays:
                        replay = replay.as_dict()
                        replay.pop('notice_info')
                        replay.update({
                            'admin_info': replay['admin_info']['admin_id']
                        })
                        all_replays.append(replay)
                if len(all_replays) != 0:
                    all_replays = sorted(
                        all_replays, key=lambda message: message['create_time'], reverse=True)
                for notice in all_notices_pagination:
                    notice_result = {
                        "notice_id": notice.notice_id,
                        "title": notice.title,
                        "message": notice.message,
                        "create_date": notice.create_date,
                        "attachment": notice.attachment,
                        "notice_files": notice.notice_files,
                        "notice_category_info": {
                            "category_id": notice.notice_category.category_id,
                            "category_name": notice.notice_category.category_name,
                            "category_index": notice.notice_category.category_index,
                            "create_date": notice.notice_category.create_date,

                        },
                        "notice_user_info": {
                            "user_id": notice.user.user_id,
                            "user_name": notice.user.user_name,
                            "user_phone": notice.user.user_phone,
                        },
                        "replays": all_replays,
                        "all_notices": tableCount
                    }
                    noticeResult.append(notice_result)
                return True, noticeResult
            else:
                return field_result
        else:
            return False, wrong_token_result
