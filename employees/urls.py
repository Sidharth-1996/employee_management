from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/new/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('delete_attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
]