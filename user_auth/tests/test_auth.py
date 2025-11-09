from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthAPITest(APITestCase):
    def test_user_registration_success(self):
        """ทดสอบการลงทะเบียนผู้ใช้ใหม่ที่ถูกต้อง"""
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'securepwd',
            'password2': 'securepwd'
        }
        response = self.client.post('/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login_success(self):
        """ทดสอบการเข้าสู่ระบบที่ถูกต้อง"""
        User.objects.create_user(username='loginuser', password='loginpwd')
        data = {'username': 'loginuser', 'password': 'loginpwd'}
        response = self.client.post('/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_user_login_fail(self):
        """ทดสอบการเข้าสู่ระบบด้วยรหัสผ่านที่ไม่ถูกต้อง"""
        User.objects.create_user(username='failuser', password='correctpwd')
        data = {'username': 'failuser', 'password': 'wrongpwd'}
        response = self.client.post('/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)