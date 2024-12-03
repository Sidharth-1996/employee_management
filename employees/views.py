from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Attendance
from .forms import EmployeeForm, AttendanceForm
from django.http import HttpResponse

# Create your views here.

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})


def employee_delete(request, pk):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect('employee_list')
    
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'attendances': attendances})

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'add_attendance.html', {'form': form})

def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == "POST":
        attendance.delete()
        return redirect('attendance_list')  
    return redirect('attendance_list')  