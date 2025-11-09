from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from emp_app.models import Status, Position, Department, Employee

class EmployeeModelTest(TestCase):
    def setUp(self):
        # สร้างข้อมูลพื้นฐานที่จำเป็นสำหรับการทดสอบ Employee
        self.user = User.objects.create_user(username='manager', password='pwd')
        self.status = Status.objects.create(name='Permanent')
        self.position = Position.objects.create(name='Developer', salary=50000.00)
        self.department = Department.objects.create(name='IT', manager=None)
        self.image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        # สร้าง Employee
        self.employee = Employee.objects.create(
            name='John',
            address='Test Address',
            position=self.position,
            department=self.department,
            status=self.status,
            image = self.image,
        )

    # ทดสอบการสร้างโมเดล Status
    def test_status_creation(self):
        self.assertTrue(isinstance(self.status, Status))
        self.assertEqual(self.status.__str__(), 'Permanent')

    # ทดสอบการสร้างโมเดล Position
    def test_position_creation(self):
        self.assertTrue(isinstance(self.position, Position))
        self.assertEqual(self.position.salary, 50000.00)

    # ทดสอบการสร้างโมเดล Employee
    def test_employee_creation(self):
        self.assertTrue(isinstance(self.employee, Employee))
        self.assertEqual(self.employee.__str__(), 'John')
        self.assertEqual(self.employee.position.name, 'Developer')