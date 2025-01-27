from json.decoder import JSONDecodeError
from django.views.decorators.csrf import csrf_exempt
import json
from SayalSanjesh.Views import result_creator
from SayalSanjesh.Serializers.NoticeSerializer import NoticeSerializer


# from SayalSanjesh.models import Notice


class NoticeView():

    @csrf_exempt
    def admin_get_one_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        if 'notice_id' in input_data:
            notice_id = input_data['notice_id']
        else:
            return result_creator(status="failure", code=406, farsi_message=".وارد نشده است notice_id",
                                  english_message="notice_id is Null.")
        result, data = NoticeSerializer.admin_get_one_notice(token=token,
                                                             notice_id=notice_id)
        if result:
            data = {
                "notice": data
            }
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_all_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "title",
                  "message", "create_date", "attachment"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data['page']
        count = input_data['count']
        title = input_data['title']
        message = input_data['message']
        create_date = input_data['create_date']
        attachment = input_data['attachment']
        result, data = NoticeSerializer.admin_get_all_notice_serializer(
            token, page, count, title, message, create_date, attachment)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_get_my_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = NoticeSerializer.admin_get_my_notice(
            token=token)
        if result:

            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def admin_replay_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["message", "notice"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        message = input_data['message']
        notice = input_data['notice']
        result, data = NoticeSerializer.admin_replay_notice(
            token=token, message=message, notice=notice)
        if result:
            data = {
                "notice": data
            }
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_create_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            data = request.POST['data']
            filepath = request.FILES['file'] if 'file' in request.FILES else False
            if filepath != False:
                filepath = filepath
            else:
                filepath = ""
            input_data = json.loads(data)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["attachment", "title", "message", "notice_category"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        notice_category = input_data['notice_category']
        title = input_data['title']
        message = input_data['message']
        attachment = input_data['attachment']
        result, data = NoticeSerializer.user_create_notice(
            token=token, notice_category=notice_category, title=title,
            message=message, attachment=attachment, filepath=filepath)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_replay_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["message", "notice"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        message = input_data['message']
        notice = input_data['notice']
        result, data = NoticeSerializer.user_replay_notice(
            token=token, message=message, notice=notice)
        if result:
            data = {
                "notice": data
            }
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=data["code"], farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_my_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        result, data = NoticeSerializer.user_get_my_notice(
            token=token)
        if result:
            data = {
                "notice": data
            }
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_one_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["notice_id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        notice_id = input_data['notice_id']
        result, data = NoticeSerializer.user_get_one_notice(token=token,
                                                            notice_id=notice_id)
        if result:
            data = {
                "notice": data
            }
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])

    @csrf_exempt
    def user_get_all_notice(self, request):
        if request.method.lower() == "options":
            return result_creator()
        try:
            input_data = json.loads(request.body)
        except:
            return result_creator(status="failure", code=406, farsi_message="وارد نشده است json",
                                  english_message="invalid JSON error")

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["page", "count", "title",
                  "message", "create_date", "attachment"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, farsi_message=f".وارد نشده است {field}",
                                      english_message=f"{field} is Null.")
        page = input_data['page']
        count = input_data['count']
        title = input_data['title']
        message = input_data['message']
        create_date = input_data['create_date']
        attachment = input_data['attachment']
        result, data = NoticeSerializer.user_get_all_notice_serializer(
            token, page, count, title, message, create_date, attachment)
        if result:
                return result_creator(data=data)
        else:
            return result_creator(status="failure", code=406, farsi_message=data["farsi_message"],
                                  english_message=data["english_message"])
