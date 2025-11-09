from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from auth_app.serializers import RegisterSerializer

User = get_user_model()

# --- Unit Test สำหรับ Serializer ---
class RegisterSerializerTest(APITestCase):
    """
    ทดสอบการทำงานของ RegisterSerializer
    """

    def test_valid_data(self):
        """
        ตรวจสอบว่า serializer สามารถสร้าง user ได้ถูกต้องเมื่อข้อมูลถูกต้อง
        """
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        # สร้าง instance ของ Serializer
        serializer = RegisterSerializer(data=data)
        
        # ตรวจสอบความถูกต้องของข้อมูล
        self.assertTrue(serializer.is_valid())
        
        # บันทึกข้อมูล (ซึ่งจะเรียก method create())
        user = serializer.save()
        
        # ตรวจสอบว่า user ถูกสร้างในฐานข้อมูลแล้ว
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, data['username'])
        
        # ตรวจสอบว่ารหัสผ่านถูกแฮชอย่างถูกต้อง (ไม่เก็บเป็น plain text)
        self.assertTrue(user.check_password(data['password']))
        
    def test_invalid_missing_username(self):
        """
        ตรวจสอบการจัดการเมื่อขาดฟิลด์ username
        """
        data = {
            'password': 'testpassword123',
        }
        serializer = RegisterSerializer(data=data)
        
        # ข้อมูลควรไม่ถูกต้อง
        self.assertFalse(serializer.is_valid())
        
        # ตรวจสอบว่ามี error message สำหรับ 'username'
        self.assertIn('username', serializer.errors)
        
    def test_invalid_duplicate_username(self):
        """
        ตรวจสอบการจัดการเมื่อ username ซ้ำกัน
        """
        # สร้าง user แรก
        User.objects.create_user(username='existinguser', password='password123')
        
        # ข้อมูลสำหรับ user ที่สองที่มี username ซ้ำ
        data = {
            'username': 'existinguser',
            'password': 'newpassword456',
        }
        serializer = RegisterSerializer(data=data)
        
        # ข้อมูลควรไม่ถูกต้อง
        self.assertFalse(serializer.is_valid())
        
        # ตรวจสอบว่ามี error message สำหรับ 'username'
        self.assertIn('username', serializer.errors)
        # ตรวจสอบข้อความ error ที่เกี่ยวข้องกับการซ้ำ
        self.assertIn('already exists', str(serializer.errors['username']))


