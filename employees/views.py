from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Attendance, Department, Holiday
from .forms import EmployeeForm, AttendanceForm
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime, timedelta, date
import calendar
from django.db.models import Q, Count

# Create your views here.

def employee_list(request):
    employees = Employee.objects.all().select_related('department').order_by('first_name', 'last_name')
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee.objects.select_related('department'), pk=pk)
    # Get employee attendance history
    attendances = Attendance.objects.filter(employee=employee).order_by('-date')[:10]
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'attendances': attendances,
    })

def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.first_name} {employee.last_name} has been created successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.first_name} {employee.last_name} has been updated successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'employee': employee})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee_name = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        messages.success(request, f'Employee {employee_name} has been deleted successfully.')
        return redirect('employee_list')
    # For GET requests, redirect to employee list (or show confirmation page)
    return redirect('employee_list')

def is_weekend(date_obj):
    """Check if date is Saturday (5) or Sunday (6)"""
    return date_obj.weekday() >= 5  # 5 = Saturday, 6 = Sunday

def is_holiday(date_obj):
    """Check if date is a holiday"""
    # Check for exact date match
    if Holiday.objects.filter(date=date_obj).exists():
        return True
    # Check for recurring holidays (same month and day, different year)
    if Holiday.objects.filter(is_recurring=True, date__month=date_obj.month, date__day=date_obj.day).exists():
        return True
    return False

def is_working_day(date_obj):
    """Check if date is a working day (not weekend or holiday)"""
    return not is_weekend(date_obj) and not is_holiday(date_obj)
    
def attendance_list(request):
    # Get date range from query parameters or use defaults
    today = timezone.now().date()
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # Default to first day of current month
            start_date = today.replace(day=1)
    else:
        # Default to first day of current month
        start_date = today.replace(day=1)
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # Default to today
            end_date = today
    else:
        # Default to today
        end_date = today
    
    # Ensure start_date is before or equal to end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Filter attendances by date range
    attendances = Attendance.objects.filter(
        date__gte=start_date, 
        date__lte=end_date
    ).select_related('employee').order_by('-date', 'employee__first_name', 'employee__last_name')
    
    # Generate a list of dates for the header
    delta = end_date - start_date
    dates = []
    for i in range(delta.days + 1):
        current_date = start_date + timedelta(days=i)
        is_weekend_day = is_weekend(current_date)
        is_holiday_day = is_holiday(current_date)
        
        dates.append({
            'date': current_date,
            'weekday': current_date.strftime('%A'),
            'is_today': current_date == today,
            'is_weekend': is_weekend_day,
            'is_holiday': is_holiday_day,
            'is_non_working': is_weekend_day or is_holiday_day,
        })
    
    # Create an attendance matrix
    employees = Employee.objects.all().select_related('department').order_by('first_name', 'last_name')
    employees_list = list(employees)  # Convert to list to check count
    attendance_matrix = []
    for employee in employees_list:
        employee_daily_attendance = []
        for d_info in dates:
            att = next((a for a in attendances if a.employee == employee and a.date == d_info['date']), None)
            employee_daily_attendance.append({
                'date': d_info['date'],
                'attendance': att,
                'is_non_working': d_info['is_non_working'],
                'is_locked': False,  # Can be enhanced later
            })
        attendance_matrix.append({
            'employee': employee,
            'daily_attendance': employee_daily_attendance,
        })
    
    # Calculate daily statistics
    daily_stats = []
    for d_info in dates:
        day_attendances = [a for a in attendances if a.date == d_info['date']]
        day_total = len(day_attendances)
        day_present = len([a for a in day_attendances if a.status == 'present'])
        day_absent = len([a for a in day_attendances if a.status == 'absent'])
        daily_stats.append({
            'date': d_info['date'],
            'weekday': d_info['weekday'],
            'total': day_total,
            'present': day_present,
            'absent': day_absent,
            'is_non_working': d_info['is_non_working'],
        })
    
    # Generate calendar dates for the date range picker modal
    # Show the month containing end_date and the previous month
    end_month = end_date.replace(day=1)
    # Calculate previous month
    if end_month.month == 1:
        prev_month = end_month.replace(year=end_month.year - 1, month=12)
    else:
        prev_month = end_month.replace(month=end_month.month - 1)
    
    calendar_dates = []
    
    # Generate 2 months for calendar display (previous month and end_date month)
    months_to_show = [prev_month, end_month]
    for month_date in months_to_show:
        
        # Calculate the month's calendar
        month = month_date.month
        year = month_date.year
        month_name = calendar.month_name[month]
        
        # Get first day of month and number of days
        first_day = date(year, month, 1)
        last_day = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year + 1, 1, 1) - timedelta(days=1)
        days_in_month = last_day.day
        starting_day_of_week = first_day.weekday()  # 0=Monday, 6=Sunday
        
        # Build weeks
        weeks = []
        current_week = []
        
        # Add empty cells for days before month starts
        for _ in range(starting_day_of_week):
            current_week.append(None)
        
        # Add days of the month
        for day in range(1, days_in_month + 1):
            current_date = date(year, month, day)
            current_week.append(current_date)
            
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        
        # Add remaining days to complete the last week
        if current_week:
            while len(current_week) < 7:
                current_week.append(None)
            weeks.append(current_week)
        
        calendar_dates.append({
            'month': month,
            'year': year,
            'month_name': month_name,
            'weeks': weeks,
        })
    
    # Define preset date ranges
    presets = [
        {'value': 'today', 'label': 'Today', 'icon': '📅'},
        {'value': 'yesterday', 'label': 'Yesterday', 'icon': '⬅️'},
        {'value': 'last7days', 'label': 'Last 7 Days', 'icon': '📊'},
        {'value': 'last30days', 'label': 'Last 30 Days', 'icon': '📈'},
        {'value': 'last90days', 'label': 'Last 90 Days', 'icon': '📉'},
        {'value': 'thisweek', 'label': 'This Week', 'icon': '📆'},
        {'value': 'lastweek', 'label': 'Last Week', 'icon': '⏮️'},
        {'value': 'thismonth', 'label': 'This Month', 'icon': '🗓️'},
        {'value': 'lastmonth', 'label': 'Last Month', 'icon': '◀️'},
    ]
    
    # Determine selected preset based on current date range
    selected_preset = None
    month_start = today.replace(day=1)
    last_month_end = month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    
    days_since_monday = today.weekday()
    this_week_start = today - timedelta(days=days_since_monday)
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)
    
    # Calculate date ranges for presets
    last_7_days_start = today - timedelta(days=6)
    last_30_days_start = today - timedelta(days=29)
    last_90_days_start = today - timedelta(days=89)
    
    if start_date == today and end_date == today:
        selected_preset = 'today'
    elif start_date == today - timedelta(days=1) and end_date == today - timedelta(days=1):
        selected_preset = 'yesterday'
    elif start_date == last_7_days_start and end_date == today:
        selected_preset = 'last7days'
    elif start_date == last_30_days_start and end_date == today:
        selected_preset = 'last30days'
    elif start_date == last_90_days_start and end_date == today:
        selected_preset = 'last90days'
    elif start_date == this_week_start and end_date == today:
        selected_preset = 'thisweek'
    elif start_date == last_week_start and end_date == last_week_end:
        selected_preset = 'lastweek'
    elif start_date == month_start and end_date == today:
        selected_preset = 'thismonth'
    elif start_date == last_month_start and end_date == last_month_end:
        selected_preset = 'lastmonth'
    
    context = {
        'attendances': attendances,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
        'dates': dates,
        'attendance_matrix': attendance_matrix,
        'daily_stats': daily_stats,
        'calendar_dates': calendar_dates,
        'presets': presets,
        'selected_preset': selected_preset,
        'has_employees': len(employees_list) > 0,  # Explicit flag for template
    }
    
    return render(request, 'attendance_list.html', context)

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, f'Attendance for {attendance.employee} on {attendance.date} has been added successfully.')
            return redirect('attendance_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AttendanceForm()
    return render(request, 'add_attendance.html', {'form': form})

def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == "POST":
        employee_name = str(attendance.employee)
        date_str = attendance.date.strftime('%B %d, %Y')
        attendance.delete()
        messages.success(request, f'Attendance for {employee_name} on {date_str} has been deleted successfully.')
        return redirect('attendance_list')  
    return redirect('attendance_list')

def dashboard(request):
    today = timezone.now().date()
    
    # Total employees
    total_employees = Employee.objects.count()
    
    # Today's attendance
    today_attendances = Attendance.objects.filter(date=today)
    today_total = today_attendances.count()
    today_present = today_attendances.filter(status='present').count()
    today_absent = today_attendances.filter(status='absent').count()
    today_percentage = round((today_present / today_total * 100) if today_total > 0 else 0, 1)
    
    # Recent attendance count (this week)
    week_start = today - timedelta(days=today.weekday())
    recent_attendance_count = Attendance.objects.filter(date__gte=week_start).count()
    
    # Department statistics
    departments = Department.objects.all()
    department_stats = []
    for dept in departments:
        dept_employees = Employee.objects.filter(department=dept)
        dept_employee_count = dept_employees.count()
        # Get today's attendance for employees in this department
        dept_employee_ids = dept_employees.values_list('id', flat=True)
        dept_today_attendances = today_attendances.filter(employee_id__in=dept_employee_ids)
        dept_today_present = dept_today_attendances.filter(status='present').count()
        department_stats.append({
            'name': dept.name,
            'employee_count': dept_employee_count,
            'today_present': dept_today_present,
        })
    
    # Weekly attendance trend (last 7 days)
    week_attendance = []
    for i in range(6, -1, -1):  # Last 7 days including today
        date = today - timedelta(days=i)
        day_attendances = Attendance.objects.filter(date=date)
        day_total = day_attendances.count()
        day_present = day_attendances.filter(status='present').count()
        day_absent = day_attendances.filter(status='absent').count()
        week_attendance.append({
            'date': date,
            'total': day_total,
            'present': day_present,
            'absent': day_absent,
        })
    
    context = {
        'total_employees': total_employees,
        'today_present': today_present,
        'today_absent': today_absent,
        'today_total': today_total,
        'today_percentage': today_percentage,
        'recent_attendance_count': recent_attendance_count,
        'department_stats': department_stats,
        'week_attendance': week_attendance,
        'today': today,
    }
    
    return render(request, 'dashboard.html', context)

def mark_attendance(request):
    # Check if there's a specific date parameter
    selected_date = request.GET.get('date', None)
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    employees = Employee.objects.all().select_related('department').order_by('first_name', 'last_name')
    today = timezone.now().date()
    
    if request.method == 'POST':
        # Process attendance marking
        selected_date_str = request.POST.get('selected_date')
        if selected_date_str:
            try:
                selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                selected_date = timezone.now().date()
        
        # Validate that the date is a working day
        if is_weekend(selected_date):
            day_name = selected_date.strftime('%A')
            messages.error(request, f'Attendance cannot be marked on {day_name}s (weekends). Please select a working day.')
            return redirect('mark_attendance')
        
        if is_holiday(selected_date):
            holiday = Holiday.objects.filter(
                Q(date=selected_date) | 
                Q(is_recurring=True, date__month=selected_date.month, date__day=selected_date.day)
            ).first()
            holiday_name = holiday.name if holiday else 'a holiday'
            messages.error(request, f'Attendance cannot be marked on {holiday_name}. Please select a working day.')
            return redirect('mark_attendance')
        
        # Get attendance status for each employee
        saved_count = 0
        for employee in employees:
            status_key = f'status_{employee.id}'
            if status_key in request.POST:
                status = request.POST[status_key]
                # Delete existing attendance for this date if exists
                Attendance.objects.filter(employee=employee, date=selected_date).delete()
                # Create new attendance record
                Attendance.objects.create(
                    employee=employee,
                    date=selected_date,
                    status=status,
                )
                saved_count += 1
        
        if saved_count > 0:
            date_str = selected_date.strftime('%B %d, %Y')
            messages.success(request, f'Attendance for {saved_count} employee(s) on {date_str} has been saved successfully.')
        else:
            messages.warning(request, 'No attendance records were saved. Please select at least one employee.')
        
        return redirect('attendance_list')
    
    # Get existing attendance for the selected date
    attendances_dict = {}
    if selected_date:
        attendances = Attendance.objects.filter(date=selected_date).select_related('employee')
        for att in attendances:
            attendances_dict[att.employee.id] = att
    
    # Build employees_data list
    employees_data = []
    # Check if selected date is a working day (not weekend or holiday)
    is_selected_date_working = is_working_day(selected_date)
    
    for employee in employees:
        # Check if employee is new (hired within last 30 days)
        is_new = (today - employee.hire_date).days <= 30 if employee.hire_date else False
        # Date should not be locked if it's a working day and today or in the past
        # Only lock if it's a weekend/holiday or future date
        is_locked = not is_selected_date_working or selected_date > today
        
        employees_data.append({
            'employee': employee,
            'attendance': attendances_dict.get(employee.id),
            'is_new': is_new,
            'is_locked': is_locked,
        })
    
    # Generate calendar for the current week only
    
    # Get the start of the current week (Monday)
    # weekday() returns 0 for Monday, 1 for Tuesday, etc.
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)
    
    # Generate the 7 days of the current week with metadata
    week_dates = []
    for i in range(7):
        week_date = week_start + timedelta(days=i)
        is_weekend_day = is_weekend(week_date)
        is_holiday_day = is_holiday(week_date)
        is_working = is_working_day(week_date)
        
        # Get holiday name if it's a holiday
        holiday_name = None
        if is_holiday_day:
            holiday = Holiday.objects.filter(
                Q(date=week_date) | 
                Q(is_recurring=True, date__month=week_date.month, date__day=week_date.day)
            ).first()
            if holiday:
                holiday_name = holiday.name
        
        week_dates.append({
            'date': week_date,
            'day': week_date.day,  # Day number (1-31)
            'is_today': week_date == today,
            'is_selected': week_date == selected_date,
            'is_future': week_date > today,
            'is_weekend': is_weekend_day,
            'is_holiday': is_holiday_day,
            'is_working': is_working,
            'holiday_name': holiday_name,
            'date_str': week_date.strftime('%Y-%m-%d'),
        })
    
    # Get month name and year (use the most common month in the week)
    month_days = {}
    for d in week_dates:
        date_obj = d['date']
        month_key = (date_obj.year, date_obj.month)
        month_days[month_key] = month_days.get(month_key, 0) + 1
    
    # Get the month with most days in the week
    main_month = max(month_days.items(), key=lambda x: x[1])[0]
    month_name = calendar.month_name[main_month[1]]
    cal_year = main_month[0]
    
    calendar_dates = [{
        'month_name': month_name,
        'year': cal_year,
        'week_dates': week_dates,  # Just the 7 days of the week with metadata
    }]
    
    context = {
        'employees_data': employees_data,
        'selected_date': selected_date,
        'today': today,
        'calendar_dates': calendar_dates,
    }
    
    return render(request, 'mark_attendance.html', context)

def logout_view(request):
    """Custom logout view that accepts GET requests and redirects to login"""
    logout(request)
    return redirect('login') 