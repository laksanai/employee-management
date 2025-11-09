from django.contrib import admin
from .models import Employee, Position, Department, Status

# 1. ลงทะเบียนโมเดลแบบง่ายที่สุด
admin.site.register(Status)
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(Employee)