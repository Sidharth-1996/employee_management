"""
DateRangeService for handling predefined date ranges and validation.
Provides reusable logic for filtering attendance records by date range.
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import Tuple, Optional


class DateRangeService:
    """Service for handling date range calculations and validations."""
    
    @staticmethod
    def get_today() -> date:
        """Get today's date."""
        return date.today()
    
    @staticmethod
    def get_predefined_range(range_type: str) -> Tuple[date, date]:
        """
        Get a predefined date range based on the range type.
        
        Args:
            range_type: One of 'today', 'yesterday', 'last7days', 'last30days',
                       'thisweek', 'lastweek', 'thismonth', 'lastmonth',
                       'thisyear', 'lastyear'
        
        Returns:
            Tuple of (start_date, end_date)
        """
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
            # Monday of this week
            start = today - timedelta(days=today.weekday())
            return start, today
        
        elif range_type == 'lastweek':
            # Previous week (Monday to Sunday)
            days_since_monday = today.weekday()
            sunday_last_week = today - timedelta(days=days_since_monday + 1)
            monday_last_week = sunday_last_week - timedelta(days=6)
            return monday_last_week, sunday_last_week
        
        elif range_type == 'thismonth':
            start = today.replace(day=1)
            return start, today
        
        elif range_type == 'lastmonth':
            # First day of last month
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
            # Default: last 7 days
            start = today - timedelta(days=6)
            return start, today
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> Tuple[bool, Optional[str]]:
        """
        Validate that the date range is valid.
        
        Args:
            start_date: The start date
            end_date: The end date
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        today = date.today()
        
        # Check if start_date is after end_date
        if start_date > end_date:
            return False, "Start date cannot be after end date."
        
        # Check if end_date is in the future
        if end_date > today:
            return False, f"End date cannot be in the future. Today is {today}."
        
        # Check if range is too large (e.g., more than 2 years)
        days_diff = (end_date - start_date).days
        if days_diff > 730:  # 2 years
            return False, "Date range cannot exceed 2 years."
        
        return True, None
    
    @staticmethod
    def get_month_range(month: int, year: int) -> Tuple[date, date]:
        """
        Get the first and last day of a given month.
        
        Args:
            month: Month number (1-12)
            year: Year
        
        Returns:
            Tuple of (first_day, last_day)
        """
        first_day = date(year, month, 1)
        # Get last day by going to next month and subtracting 1 day
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return first_day, last_day
    
    @staticmethod
    def generate_calendar_months(center_month: int, center_year: int, months_count: int = 6) -> list:
        """
        Generate a list of months centered around the given month.
        
        Args:
            center_month: Month number (1-12)
            center_year: Year
            months_count: Total number of months to generate (default 6)
        
        Returns:
            List of (month, year) tuples
        """
        months = []
        offset = -(months_count // 2)  # Start from months before center
        
        for i in range(months_count):
            new_date = date(center_year, center_month, 1) + relativedelta(months=offset + i)
            months.append((new_date.month, new_date.year))
        
        return months
