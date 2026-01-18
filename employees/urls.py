from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/new/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('delete_attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]