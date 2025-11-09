from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=128, unique=True, help_text="recuitment process, waiting for onboarding, in probation period, normal, resigned")

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    manager = models.ForeignKey(
        'Employee', related_name='managed_departments',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    manager = models.BooleanField(default=False) 
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

    def __str__(self):
        return self.name
