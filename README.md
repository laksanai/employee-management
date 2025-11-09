# Employees management
CRUD RESTful API โดยใช้ Django ในการจัดการ employees

## การติดตั้ง
```bash
git clone https://github.com/laksanai/employee-management.git
cd ./employee-management
pip install -r requirements.txt
```

## การตั้งค่าฐานข้อมูล
```bash
python manage.py makemigrations emp_app register
python manage.py migrate
```

## การรัน Development Server
```bash
python manage.py runserver
```

## ทำการเพิ่ม User
ไปที่ http://127.0.0.1:8000/register/ เพื่อทำการเพิ่ม user

## ให้ทำการเพิ่มข้อมูลใน Model
- position     ที่  http://127.0.0.1:8000/api/positions/
- department   ที่  http://127.0.0.1:8000/api/departments/
- status       ที่  http://127.0.0.1:8000/api/statuses/
- employee     ที่  http://127.0.0.1:8000/api/employees/

## สามารถทำการ DELETE UPDATE จาก
- position     ที่  http://127.0.0.1:8000/api/positions/<id>
- department   ที่  http://127.0.0.1:8000/api/departments/<id>
- status       ที่  http://127.0.0.1:8000/api/statuses/<id>
- employee     ที่  http://127.0.0.1:8000/api/employees/<id>

## รัน unit tests and integration tests
```bash
python manage.py test
```


