from django.contrib import admin
from .models import Employee, Department, Holiday

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Holiday)

admin.site.site_header = "Employee Management System"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Employee Management System"  