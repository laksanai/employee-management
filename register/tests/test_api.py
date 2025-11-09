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

    def test_successful_registration(self):
        """
        ทดสอบการลงทะเบียนผู้ใช้ใหม่ที่สำเร็จ
        """
        url = reverse('register') # 'register' คือ name ใน urlpatterns
        data = {
            'username': 'newuser123',
            'password': 'securepassword789',
        }
        
        # ทำ POST request ไปยัง RegisterView
        response = self.client.post(url, data, format='json')
        
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
        
        url = reverse('register')
        data = {
            'username': 'duplicateuser', # username ซ้ำ
            'password': 'anotherpassword',
        }
        
        # ทำ POST request ครั้งที่สอง
        response = self.client.post(url, data, format='json')
        
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
        url = reverse('register')
        data = {
            'username': 'missingpass',
            # 'password' หายไป
        }
        
        response = self.client.post(url, data, format='json')
        
        # ตรวจสอบสถานะ response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # ตรวจสอบว่า user ไม่ถูกสร้าง
        self.assertEqual(User.objects.count(), 0)
        
        # ตรวจสอบ error message
        self.assertIn('password', response.data)