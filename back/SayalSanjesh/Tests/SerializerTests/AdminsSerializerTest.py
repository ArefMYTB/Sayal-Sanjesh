from django.test import TestCase
from SayalSanjesh.Serializers.AdminsSerializer import AdminsSerializer
from SayalSanjesh.TokenManager import user_id_to_token, token_to_user_id
from SayalSanjesh.models import Admins


class TestAdminSerializer(TestCase):

    def test_admin_check_permission(self):
        Admins.objects.create(admin_id='a22292ea-5f3e-4315-8d0b-8e2c7b0bb8a6', admin_name='AdminTest',
                              admin_phone='09356165600', admin_permissions=['Self', 'Admin'], admin_password='1234',
                              admin_lastname='Admin', admin_sms_code='1234', other_information={})
        admin = AdminsSerializer()
        function = admin.admin_check_permission(admin_id='a22292ea-5f3e-4315-8d0b-8e2c7b0bb8a6', permission='Self')
        expected = True
        self.assertEqual(function, expected)

    def test_admin_login_serializer(self):
        Admins.objects.create(admin_id='a22292ea-5f3e-4315-8d0b-8e2c7b0bb8a6', admin_name='AdminTest',
                              admin_phone='09356165600', admin_permissions=['Self', 'Admin'], admin_password='1234',
                              admin_lastname='Admin', admin_sms_code='1234', other_information={})
        token = user_id_to_token('a22292ea-5f3e-4315-8d0b-8e2c7b0bb8a6', True, token_level="Admin")
        admin = AdminsSerializer()
        function = admin.admin_login_serializer(admin_phone='09356165600', admin_password='1234')
        test_result = {
            "permissions": ['Self', 'Admin'],
            "token": token
        }
        expected = (True, test_result)
        self.assertEqual(function, expected)
