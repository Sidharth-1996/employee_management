from django import forms
from django.core.exceptions import ValidationError
from .models import Employee, Attendance, Department, Holiday
from django.utils import timezone
from django.db.models import Q

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'department', 'hire_date']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter first name',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter last name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter email address',
                'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter phone number',
                'required': True,
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
            }),
            'hire_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'max': timezone.now().date().isoformat(),
            }),
        }
        help_texts = {
            'email': 'Enter a valid email address.',
            'hire_date': 'Select the date when the employee was hired.',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            queryset = Employee.objects.filter(email=email)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError('An employee with this email already exists.')
        return email
    
    def clean_hire_date(self):
        hire_date = self.cleaned_data.get('hire_date')
        if hire_date:
            today = timezone.now().date()
            if hire_date > today:
                raise ValidationError('Hire date cannot be in the future.')
        return hire_date


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status']
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'max': timezone.now().date().isoformat(),
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
        }
    
    def is_weekend(self, date_obj):
        return date_obj.weekday() >= 5
    
    def is_holiday(self, date_obj):
        if Holiday.objects.filter(date=date_obj).exists():
            return True
        if Holiday.objects.filter(is_recurring=True, date__month=date_obj.month, date__day=date_obj.day).exists():
            return True
        return False
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            today = timezone.now().date()
            if date > today:
                raise ValidationError('Attendance date cannot be in the future.')
            
            # Check if date is a weekend
            if self.is_weekend(date):
                day_name = date.strftime('%A')
                raise ValidationError(f'Attendance cannot be marked on {day_name}s (weekends). Please select a working day.')
            
            # Check if date is a holiday
            if self.is_holiday(date):
                holiday = Holiday.objects.filter(
                    Q(date=date) | 
                    Q(is_recurring=True, date__month=date.month, date__day=date.day)
                ).first()
                holiday_name = holiday.name if holiday else 'a holiday'
                raise ValidationError(f'Attendance cannot be marked on {holiday_name}. Please select a working day.')
        
        return date
    
    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        date = cleaned_data.get('date')
        
        if employee and date:
            queryset = Attendance.objects.filter(employee=employee, date=date)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError({
                    'date': f'Attendance for {employee} on {date} already exists.'
                })
        
        return cleaned_data
