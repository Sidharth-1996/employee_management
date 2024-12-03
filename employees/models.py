from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,default='Software Developer')
    hire_date = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Attendance(models.Model):
    DEPARTMENT_CHOICES = [
        ('Software Developer', 'Software Developer'),
        ('HR', 'HR'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Admin', 'Admin'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent')])
    department = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES, default='Software Developer')
    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"