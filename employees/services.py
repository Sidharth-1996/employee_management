from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import Tuple, Optional


class DateRangeService:
    
    @staticmethod
    def get_today() -> date:
        return date.today()
    
    @staticmethod
    def get_predefined_range(range_type: str) -> Tuple[date, date]:
        today = date.today()
        
        if range_type == 'today':
            return today, today
        elif range_type == 'yesterday':
            yesterday = today - timedelta(days=1)
            return yesterday, yesterday
        elif range_type == 'last7days':
            start = today - timedelta(days=6)
            return start, today
        elif range_type == 'last30days':
            start = today - timedelta(days=29)
            return start, today
        elif range_type == 'last90days':
            start = today - timedelta(days=89)
            return start, today
        elif range_type == 'thisweek':
            start = today - timedelta(days=today.weekday())
            return start, today
        elif range_type == 'lastweek':
            days_since_monday = today.weekday()
            sunday_last_week = today - timedelta(days=days_since_monday + 1)
            monday_last_week = sunday_last_week - timedelta(days=6)
            return monday_last_week, sunday_last_week
        elif range_type == 'thismonth':
            start = today.replace(day=1)
            return start, today
        elif range_type == 'lastmonth':
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            return first_day_last_month, last_day_last_month
        elif range_type == 'thisyear':
            start = today.replace(month=1, day=1)
            return start, today
        elif range_type == 'lastyear':
            start = today.replace(year=today.year - 1, month=1, day=1)
            end = today.replace(year=today.year - 1, month=12, day=31)
            return start, end
        else:
            start = today - timedelta(days=6)
            return start, today
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> Tuple[bool, Optional[str]]:
        today = date.today()
        
        if start_date > end_date:
            return False, "Start date cannot be after end date."
        
        if end_date > today:
            return False, f"End date cannot be in the future. Today is {today}."
        
        days_diff = (end_date - start_date).days
        if days_diff > 730:
            return False, "Date range cannot exceed 2 years."
        
        return True, None
    
    @staticmethod
    def get_month_range(month: int, year: int) -> Tuple[date, date]:
        first_day = date(year, month, 1)
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return first_day, last_day
    
    @staticmethod
    def generate_calendar_months(center_month: int, center_year: int, months_count: int = 6) -> list:
        months = []
        offset = -(months_count // 2)
        
        for i in range(months_count):
            new_date = date(center_year, center_month, 1) + relativedelta(months=offset + i)
            months.append((new_date.month, new_date.year))
        
        return months
