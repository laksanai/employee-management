from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from emp_app.models import Status, Position, Department, Employee
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


class EmployeeAPITest(APITestCase):
    def create_dummy_image(self):
        """Helper function เพื่อสร้าง SimpleUploadedFile ใหม่ทุกครั้งที่เรียกใช้"""
        image = Image.new('RGB', (100, 100), color='red')
        byte_io = BytesIO()
        image.save(byte_io, format='JPEG')
        byte_io.seek(0)
        return SimpleUploadedFile("test.jpg", byte_io.read(), content_type="image/jpeg")
    
    def setUp(self):
        # 1. สร้างผู้ใช้และรับ Token สำหรับการทดสอบ (Authentication)
        self.user = User.objects.create_user(username='apitest', password='testpassword')
        response = self.client.post('/api/auth/token/', {'username': 'apitest', 'password': 'testpassword'}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token) # ตั้งค่า Header สำหรับทุกคำขอ
        
        # 2. สร้างข้อมูลพื้นฐาน
        self.status = Status.objects.create(name='Active')
        self.position = Position.objects.create(name='Analyst', salary=60000.00)
        self.department = Department.objects.create(name='HR', manager=None)
        
        # 3. สร้าง Employee สำหรับการทดสอบ
        self.employee_data = {
            'name': 'Alice', 
            'address': '456 Test', 
            'position': self.position, 
            'department': self.department, 
            'status': self.status,
            'image': self.create_dummy_image()
        }
        Employee.objects.create(**self.employee_data)
        self.list_url = '/api/employees/'

    def test_create_employee_success(self):
        """ทดสอบ POST (Create) Employee"""
        payload = {
            'name': 'Alice',
            'address': '456 Test',
            'status_id': self.status.id,
            'position_id': self.position.id,
            'department_id': self.department.id,
            'image': self.create_dummy_image()
        }
        response = self.client.post(self.list_url, payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_list_employees_success(self):
        """ทดสอบ GET (Read) Employee List"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_employee_by_position(self):
        """ทดสอบ Advanced Query (Filtering)"""
        # สร้าง Employee คนที่สองที่มี Position ต่างกัน
        position_dev = Position.objects.create(name='Dev', salary=70000.00)
        emp_data2 = self.employee_data.copy()
        emp_data2['position'] = position_dev
        Employee.objects.create(
            **emp_data2
        )
        
        # กรองเฉพาะ Analyst (ID เดิม)
        response = self.client.get(f'{self.list_url}?position={self.position.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['position']['id'], self.position.id)