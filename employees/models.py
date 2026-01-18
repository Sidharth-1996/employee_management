from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateField()
    
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Holiday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(unique=True)
    is_recurring = models.BooleanField(default=False, help_text="If checked, this holiday repeats every year on the same date")
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Holidays'
    
    def __str__(self):
        return f"{self.name} - {self.date}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-date', 'employee__first_name']
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_date')
        ]
        verbose_name_plural = 'Attendances'
    
    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"