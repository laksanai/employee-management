from .base import *

DEBUG = False 
ALLOWED_HOSTS = ['your-domain.com', 'your-ip-address'] 

# SECRET_KEY ต้องถูกดึงมาจาก Environment Variable เพื่อความปลอดภัย
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') # ต้องมี os.environ.get() และการจัดการ Error
SECRET_KEY = 'MySecretKeys'

# ฐานข้อมูล (มักใช้ PostgreSQL หรือ MySQL)
DATABASES = {
    'default': {
        # ... ตั้งค่า Engine และ Credentials สำหรับ Production Database
    }
}
# การตั้งค่าสำหรับ Static/Media files
# STATIC_ROOT = os.path.join(BASE_DIR, 'static_root') 
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')