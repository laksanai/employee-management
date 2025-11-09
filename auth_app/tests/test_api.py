from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

# --- Integration Test สำหรับ View และ Endpoint ---
class RegisterViewTest(APITestCase):
    """
    ทดสอบการทำงานของ RegisterView ผ่าน HTTP request
    """
    def setUp(self):
        self.register_url = reverse('register') # ต้อง set name ไว้ใน urls
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_successful_registration(self):
        """
        ทดสอบการลงทะเบียนผู้ใช้ใหม่ที่สำเร็จ
        """

        data = {
            'username': 'newuser123',
            'password': 'securepassword789',
        }
        
        # ทำ POST request ไปยัง RegisterView
        response = self.client.post(self.register_url, data, format='json')
        
        # ตรวจสอบสถานะ response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # ตรวจสอบว่า user ถูกสร้างในฐานข้อมูลแล้ว
        self.assertEqual(User.objects.count(), 1)
        
        # ดึง user ที่สร้างขึ้นมาเพื่อตรวจสอบรายละเอียด
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))
        
        # ตรวจสอบว่า response มี username กลับมา (แต่ไม่ควรมี password)
        self.assertEqual(response.data['username'], data['username'])
        self.assertNotIn('password', response.data) # Password ไม่ควรอยู่ใน response
        
    def test_duplicate_registration_failure(self):
        """
        ทดสอบการลงทะเบียนซ้ำซ้อน
        """
        User.objects.create_user(username='duplicateuser', password='password123')
        
        data = {
            'username': 'duplicateuser', # username ซ้ำ
            'password': 'anotherpassword',
        }
        
        # ทำ POST request ครั้งที่สอง
        response = self.client.post(self.register_url, data, format='json')
        
        # ตรวจสอบสถานะ response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # ตรวจสอบว่า user ยังคงมีเพียง 1 คนเท่านั้น
        self.assertEqual(User.objects.count(), 1)
        
        # ตรวจสอบ error message
        self.assertIn('username', response.data)
        self.assertIn('already exists', str(response.data['username']))

    def test_missing_field_registration_failure(self):
        """
        ทดสอบเมื่อขาดข้อมูลที่จำเป็น (เช่น password)
        """

        data = {
            'username': 'missingpass',
            # 'password' หายไป
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        # ตรวจสอบสถานะ response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # ตรวจสอบว่า user ไม่ถูกสร้าง
        self.assertEqual(User.objects.count(), 0)
        
        # ตรวจสอบ error message
        self.assertIn('password', response.data)

    def test_login(self):

        User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)   # DRF Token auth

        self.token = response.data['token']

    def test_logout(self):

        User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # ทำการ Login
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        }, format='json')
        token = response.data['token']

        # ตั้ง header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #ทดสอบใช้ ยิ่งดูข้อมูลอีกครั้ง
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        