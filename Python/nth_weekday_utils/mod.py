"""
AllToolkit - Python Nth Weekday Utilities

A zero-dependency utility module for calculating the nth occurrence of a weekday
within a month or year. Useful for holiday calculations (e.g., Thanksgiving is the
4th Thursday of November), scheduling, and date manipulations.

Author: AllToolkit
License: MIT
"""

from datetime import date, datetime, timedelta
from typing import Optional, List, Tuple, Union
from enum import IntEnum


def _parse_date(date_input: Union[date, str]) -> date:
    """Parse date input, handling both date objects and ISO format strings."""
    if isinstance(date_input, date):
        return date_input
    if isinstance(date_input, str):
        # Try ISO format first (YYYY-MM-DD)
        try:
            return datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            raise NthWeekdayError(f"Invalid date format: {date_input}. Use YYYY-MM-DD.")
    raise NthWeekdayError(f"Invalid date input: {date_input}")


class Weekday(IntEnum):
    """Weekday enumeration (Monday=0, Sunday=6)"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class NthWeekdayError(Exception):
    """Exception raised for nth weekday calculation errors."""
    pass


class NthWeekdayUtils:
    """
    Utility class for calculating nth weekday occurrences within months/years.
    
    Provides functions for:
    - Finding the nth occurrence of a weekday in a month
    - Finding the last occurrence of a weekday in a month
    - Finding all occurrences of a weekday in a month
    - Calculating common holidays (Thanksgiving, Labor Day, etc.)
    - Counting weekdays between dates
    """
    
    # Common holiday definitions (month, nth, weekday)
    HOLIDAYS = {
        # US Holidays
        'thanksgiving': (11, 4, Weekday.THURSDAY),  # 4th Thursday of November
        'labor_day': (9, 1, Weekday.MONDAY),  # 1st Monday of September
        'memorial_day': (5, -1, Weekday.MONDAY),  # Last Monday of May
        'columbus_day': (10, 2, Weekday.MONDAY),  # 2nd Monday of October
        'presidents_day': (2, 3, Weekday.MONDAY),  # 3rd Monday of February
        'martin_luther_king_day': (1, 3, Weekday.MONDAY),  # 3rd Monday of January
        'mothers_day': (5, 2, Weekday.SUNDAY),  # 2nd Sunday of May
        'fathers_day': (6, 3, Weekday.SUNDAY),  # 3rd Sunday of June
        # UK Holidays
        'early_may_bank_holiday': (5, 1, Weekday.MONDAY),  # 1st Monday of May
        'spring_bank_holiday': (5, -1, Weekday.MONDAY),  # Last Monday of May
        'summer_bank_holiday': (8, -1, Weekday.MONDAY),  # Last Monday of August
        # Canada Holidays
        'thanksgiving_canada': (10, 2, Weekday.MONDAY),  # 2nd Monday of October
        'victoria_day': (5, 3, Weekday.MONDAY),  # Monday before May 25 (approximation)
        # Australia
        'anzac_day': (4, 25, None),  # Fixed date (April 25)
    }
    
    @staticmethod
    def nth_weekday(year: int, month: int, nth: int, weekday: Union[int, Weekday]) -> date:
        """
        Find the nth occurrence of a weekday in a given month.
        
        Args:
            year: The year
            month: The month (1-12)
            nth: Which occurrence (1=first, 2=second, ..., -1=last, -2=second to last)
            weekday: The weekday (0=Monday, 6=Sunday, or use Weekday enum)
        
        Returns:
            date object for the calculated day
        
        Raises:
            NthWeekdayError: If nth is out of range or invalid parameters
        
        Example:
            >>> # Find Thanksgiving 2024 (4th Thursday of November)
            >>> NthWeekdayUtils.nth_weekday(2024, 11, 4, Weekday.THURSDAY)
            datetime.date(2024, 11, 28)
            
            >>> # Find last Monday of May 2024
            >>> NthWeekdayUtils.nth_weekday(2024, 5, -1, Weekday.MONDAY)
            datetime.date(2024, 5, 27)
        """
        if not 1 <= month <= 12:
            raise NthWeekdayError(f"Invalid month: {month}. Must be 1-12.")
        
        if not 0 <= weekday <= 6:
            raise NthWeekdayError(f"Invalid weekday: {weekday}. Must be 0-6 (Monday=0).")
        
        weekday = int(weekday)
        
        # Get all occurrences of the weekday in the month
        occurrences = NthWeekdayUtils.all_weekdays_in_month(year, month, weekday)
        
        if not occurrences:
            raise NthWeekdayError(f"No occurrences of weekday {weekday} in {year}-{month}.")
        
        # Handle negative nth (from end)
        if nth < 0:
            idx = nth
            if abs(nth) > len(occurrences):
                raise NthWeekdayError(
                    f"Invalid nth: {nth}. Only {len(occurrences)} occurrences in month."
                )
        else:
            idx = nth - 1  # Convert 1-indexed to 0-indexed
            if idx >= len(occurrences):
                raise NthWeekdayError(
                    f"Invalid nth: {nth}. Only {len(occurrences)} occurrences in month."
                )
            if nth < 1:
                raise NthWeekdayError(f"Invalid nth: {nth}. Must be >= 1 or negative for last.")
        
        return occurrences[idx]
    
    @staticmethod
    def last_weekday(year: int, month: int, weekday: Union[int, Weekday]) -> date:
        """
        Find the last occurrence of a weekday in a given month.
        
        Args:
            year: The year
            month: The month (1-12)
            weekday: The weekday (0=Monday, 6=Sunday, or use Weekday enum)
        
        Returns:
            date object for the last occurrence
        
        Example:
            >>> NthWeekdayUtils.last_weekday(2024, 5, Weekday.MONDAY)
            datetime.date(2024, 5, 27)
        """
        return NthWeekdayUtils.nth_weekday(year, month, -1, weekday)
    
    @staticmethod
    def first_weekday(year: int, month: int, weekday: Union[int, Weekday]) -> date:
        """
        Find the first occurrence of a weekday in a given month.
        
        Args:
            year: The year
            month: The month (1-12)
            weekday: The weekday (0=Monday, 6=Sunday, or use Weekday enum)
        
        Returns:
            date object for the first occurrence
        
        Example:
            >>> NthWeekdayUtils.first_weekday(2024, 11, Weekday.THURSDAY)
            datetime.date(2024, 11, 7)
        """
        return NthWeekdayUtils.nth_weekday(year, month, 1, weekday)
    
    @staticmethod
    def all_weekdays_in_month(year: int, month: int, 
                               weekday: Union[int, Weekday, None] = None) -> List[date]:
        """
        Find all occurrences of a weekday (or all weekdays) in a given month.
        
        Args:
            year: The year
            month: The month (1-12)
            weekday: The weekday filter (0=Monday, 6=Sunday, or None for all days)
        
        Returns:
            List of date objects in chronological order
        
        Example:
            >>> # All Thursdays in November 2024
            >>> NthWeekdayUtils.all_weekdays_in_month(2024, 11, Weekday.THURSDAY)
            [datetime.date(2024, 11, 7), datetime.date(2024, 11, 14), 
             datetime.date(2024, 11, 21), datetime.date(2024, 11, 28)]
        """
        if not 1 <= month <= 12:
            raise NthWeekdayError(f"Invalid month: {month}. Must be 1-12.")
        
        # Get first day of month and number of days
        first_day = date(year, month, 1)
        
        # Calculate number of days in month
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        days_in_month = last_day.day
        
        if weekday is not None:
            weekday = int(weekday)
            if not 0 <= weekday <= 6:
                raise NthWeekdayError(f"Invalid weekday: {weekday}. Must be 0-6.")
            
            # Calculate days until first occurrence of weekday
            days_until = (weekday - first_day.weekday()) % 7
            
            # Generate all occurrences
            result = []
            current = first_day + timedelta(days=days_until)
            while current.month == month:
                result.append(current)
                current += timedelta(days=7)
            
            return result
        else:
            # Return all days in month
            return [date(year, month, day) for day in range(1, days_in_month + 1)]
    
    @staticmethod
    def count_weekdays_in_month(year: int, month: int, weekday: Union[int, Weekday]) -> int:
        """
        Count the occurrences of a weekday in a given month.
        
        Args:
            year: The year
            month: The month (1-12)
            weekday: The weekday (0=Monday, 6=Sunday, or use Weekday enum)
        
        Returns:
            Number of occurrences (typically 4 or 5)
        
        Example:
            >>> NthWeekdayUtils.count_weekdays_in_month(2024, 11, Weekday.THURSDAY)
            4
        """
        return len(NthWeekdayUtils.all_weekdays_in_month(year, month, weekday))
    
    @staticmethod
    def which_nth_weekday(check_date: Union[date, str]) -> Tuple[int, int, int]:
        """
        Determine which nth occurrence of weekday a date is in its month.
        
        Args:
            check_date: The date to check (date object or ISO format string)
        
        Returns:
            Tuple of (year, month, nth) where nth is 1-indexed (1=first, 2=second, etc.)
        
        Example:
            >>> NthWeekdayUtils.which_nth_weekday(date(2024, 11, 28))
            (2024, 11, 4)  # 4th Thursday of November 2024
        """
        if isinstance(check_date, str):
            check_date = datetime.strptime(check_date, '%Y-%m-%d').date()
        
        year = check_date.year
        month = check_date.month
        weekday = check_date.weekday()
        
        # Find all occurrences
        all_occurrences = NthWeekdayUtils.all_weekdays_in_month(year, month, weekday)
        
        # Find position
        for i, d in enumerate(all_occurrences, 1):
            if d == check_date:
                return (year, month, i)
        
        raise NthWeekdayError(f"Date {check_date} not found in its own month.")
    
    @staticmethod
    def holiday(holiday_name: str, year: int) -> Optional[date]:
        """
        Calculate a named holiday for a given year.
        
        Args:
            holiday_name: Name of the holiday (case-insensitive, underscores or spaces)
            year: The year
        
        Returns:
            date object for the holiday, or None if holiday not recognized
        
        Example:
            >>> NthWeekdayUtils.holiday('thanksgiving', 2024)
            datetime.date(2024, 11, 28)
            
            >>> NthWeekdayUtils.holiday('labor_day', 2024)
            datetime.date(2024, 9, 2)
        """
        # Normalize holiday name
        key = holiday_name.lower().replace(' ', '_')
        
        if key not in NthWeekdayUtils.HOLIDAYS:
            return None
        
        month, nth, weekday = NthWeekdayUtils.HOLIDAYS[key]
        
        if weekday is None:
            # Fixed date holiday (like ANZAC Day)
            return date(year, month, nth)
        
        return NthWeekdayUtils.nth_weekday(year, month, nth, weekday)
    
    @staticmethod
    def list_holidays(year: int, country: str = 'us') -> List[Tuple[str, date]]:
        """
        List all nth-weekday-based holidays for a given year and country.
        
        Args:
            year: The year
            country: Country code ('us', 'uk', 'ca', 'au')
        
        Returns:
            List of (holiday_name, date) tuples sorted by date
        
        Example:
            >>> holidays = NthWeekdayUtils.list_holidays(2024, 'us')
            >>> for name, d in holidays[:3]:
            ...     print(f"{name}: {d}")
            martin_luther_king_day: 2024-01-15
            presidents_day: 2024-02-19
            memorial_day: 2024-05-27
        """
        # Country-specific holiday sets
        country_holidays = {
            'us': ['martin_luther_king_day', 'presidents_day', 'memorial_day',
                   'labor_day', 'columbus_day', 'thanksgiving', 'mothers_day', 'fathers_day'],
            'uk': ['early_may_bank_holiday', 'spring_bank_holiday', 'summer_bank_holiday'],
            'ca': ['victoria_day', 'thanksgiving_canada'],
            'au': ['anzac_day'],
        }
        
        holiday_names = country_holidays.get(country.lower(), country_holidays['us'])
        
        result = []
        for name in holiday_names:
            d = NthWeekdayUtils.holiday(name, year)
            if d:
                name_display = name.replace('_', ' ').title()
                result.append((name_display, d))
        
        return sorted(result, key=lambda x: x[1])
    
    @staticmethod
    def weekdays_between(start_date: Union[date, str], end_date: Union[date, str],
                         weekday: Union[int, Weekday]) -> List[date]:
        """
        Find all occurrences of a weekday between two dates (inclusive).
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            weekday: The weekday to find (0=Monday, 6=Sunday)
        
        Returns:
            List of date objects in chronological order
        
        Example:
            >>> # All Fridays in January 2024
            >>> NthWeekdayUtils.weekdays_between('2024-01-01', '2024-01-31', Weekday.FRIDAY)
            [datetime.date(2024, 1, 5), datetime.date(2024, 1, 12),
             datetime.date(2024, 1, 19), datetime.date(2024, 1, 26)]
        """
        start_date = _parse_date(start_date)
        end_date = _parse_date(end_date)
        
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        weekday = int(weekday)
        
        # Find first occurrence on or after start_date
        days_until = (weekday - start_date.weekday()) % 7
        current = start_date + timedelta(days=days_until)
        
        result = []
        while current <= end_date:
            result.append(current)
            current += timedelta(days=7)
        
        return result
    
    @staticmethod
    def count_weekdays_between(start_date: Union[date, str], end_date: Union[date, str],
                               weekday: Union[int, Weekday, None] = None) -> int:
        """
        Count occurrences of a weekday (or all weekdays) between two dates.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            weekday: The weekday to count, or None to count all days
        
        Returns:
            Number of occurrences
        
        Example:
            >>> # Count all Mondays in January 2024
            >>> NthWeekdayUtils.count_weekdays_between('2024-01-01', '2024-01-31', Weekday.MONDAY)
            5
        """
        if weekday is not None:
            return len(NthWeekdayUtils.weekdays_between(start_date, end_date, weekday))
        
        start_date = _parse_date(start_date)
        end_date = _parse_date(end_date)
        
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        return (end_date - start_date).days + 1
    
    @staticmethod
    def next_weekday_after(start_date: Union[date, str], weekday: Union[int, Weekday],
                           inclusive: bool = False) -> date:
        """
        Find the next occurrence of a weekday after (or on) a given date.
        
        Args:
            start_date: The starting date
            weekday: The target weekday (0=Monday, 6=Sunday)
            inclusive: If True, return start_date if it's already the target weekday
        
        Returns:
            date object for the next occurrence
        
        Example:
            >>> # Next Monday after 2024-11-27 (Wednesday)
            >>> NthWeekdayUtils.next_weekday_after('2024-11-27', Weekday.MONDAY)
            datetime.date(2024, 12, 2)
        """
        start_date = _parse_date(start_date)
        
        weekday = int(weekday)
        
        if inclusive and start_date.weekday() == weekday:
            return start_date
        
        days_until = (weekday - start_date.weekday()) % 7
        if days_until == 0:
            days_until = 7
        
        return start_date + timedelta(days=days_until)
    
    @staticmethod
    def previous_weekday_before(start_date: Union[date, str], weekday: Union[int, Weekday],
                                inclusive: bool = False) -> date:
        """
        Find the previous occurrence of a weekday before (or on) a given date.
        
        Args:
            start_date: The starting date
            weekday: The target weekday (0=Monday, 6=Sunday)
            inclusive: If True, return start_date if it's already the target weekday
        
        Returns:
            date object for the previous occurrence
        
        Example:
            >>> # Previous Monday before 2024-11-27 (Wednesday)
            >>> NthWeekdayUtils.previous_weekday_before('2024-11-27', Weekday.MONDAY)
            datetime.date(2024, 11, 25)
        """
        start_date = _parse_date(start_date)
        
        weekday = int(weekday)
        
        if inclusive and start_date.weekday() == weekday:
            return start_date
        
        days_since = (start_date.weekday() - weekday) % 7
        if days_since == 0:
            days_since = 7
        
        return start_date - timedelta(days=days_since)
    
    @staticmethod
    def weekday_name(weekday: Union[int, Weekday], lang: str = 'en') -> str:
        """
        Get the name of a weekday.
        
        Args:
            weekday: The weekday (0=Monday, 6=Sunday)
            lang: Language code ('en', 'zh', 'es', 'fr', 'de', 'ja')
        
        Returns:
            Weekday name string
        
        Example:
            >>> NthWeekdayUtils.weekday_name(Weekday.MONDAY, 'en')
            'Monday'
            >>> NthWeekdayUtils.weekday_name(Weekday.MONDAY, 'zh')
            '星期一'
        """
        weekday = int(weekday)
        
        names = {
            'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'zh': ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'],
            'es': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
            'fr': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
            'de': ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'],
            'ja': ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'],
        }
        
        lang = lang.lower()
        if lang not in names:
            lang = 'en'
        
        return names[lang][weekday]
    
    @staticmethod
    def month_name(month: int, lang: str = 'en') -> str:
        """
        Get the name of a month.
        
        Args:
            month: The month (1-12)
            lang: Language code ('en', 'zh', 'es', 'fr', 'de', 'ja')
        
        Returns:
            Month name string
        
        Example:
            >>> NthWeekdayUtils.month_name(11, 'en')
            'November'
            >>> NthWeekdayUtils.month_name(11, 'zh')
            '十一月'
        """
        if not 1 <= month <= 12:
            raise NthWeekdayError(f"Invalid month: {month}. Must be 1-12.")
        
        names = {
            'en': ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'],
            'zh': ['一月', '二月', '三月', '四月', '五月', '六月',
                   '七月', '八月', '九月', '十月', '十一月', '十二月'],
            'es': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            'fr': ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                   'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
            'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                   'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
            'ja': ['1月', '2月', '3月', '4月', '5月', '6月',
                   '7月', '8月', '9月', '10月', '11月', '12月'],
        }
        
        lang = lang.lower()
        if lang not in names:
            lang = 'en'
        
        return names[lang][month - 1]


# Convenience functions for direct import

def nth_weekday(year: int, month: int, nth: int, weekday: Union[int, Weekday]) -> date:
    """Find the nth occurrence of a weekday in a month."""
    return NthWeekdayUtils.nth_weekday(year, month, nth, weekday)


def last_weekday(year: int, month: int, weekday: Union[int, Weekday]) -> date:
    """Find the last occurrence of a weekday in a month."""
    return NthWeekdayUtils.last_weekday(year, month, weekday)


def first_weekday(year: int, month: int, weekday: Union[int, Weekday]) -> date:
    """Find the first occurrence of a weekday in a month."""
    return NthWeekdayUtils.first_weekday(year, month, weekday)


def all_weekdays_in_month(year: int, month: int, 
                          weekday: Union[int, Weekday, None] = None) -> List[date]:
    """Find all occurrences of a weekday in a month."""
    return NthWeekdayUtils.all_weekdays_in_month(year, month, weekday)


def count_weekdays_in_month(year: int, month: int, weekday: Union[int, Weekday]) -> int:
    """Count occurrences of a weekday in a month."""
    return NthWeekdayUtils.count_weekdays_in_month(year, month, weekday)


def which_nth_weekday(check_date: Union[date, str]) -> Tuple[int, int, int]:
    """Determine which nth occurrence a date is in its month."""
    return NthWeekdayUtils.which_nth_weekday(check_date)


def holiday(holiday_name: str, year: int) -> Optional[date]:
    """Calculate a named holiday for a given year."""
    return NthWeekdayUtils.holiday(holiday_name, year)


def list_holidays(year: int, country: str = 'us') -> List[Tuple[str, date]]:
    """List all nth-weekday-based holidays for a year."""
    return NthWeekdayUtils.list_holidays(year, country)


def weekdays_between(start_date: Union[date, str], end_date: Union[date, str],
                    weekday: Union[int, Weekday]) -> List[date]:
    """Find all occurrences of a weekday between two dates."""
    return NthWeekdayUtils.weekdays_between(start_date, end_date, weekday)


def count_weekdays_between(start_date: Union[date, str], end_date: Union[date, str],
                           weekday: Union[int, Weekday, None] = None) -> int:
    """Count occurrences of a weekday between two dates."""
    return NthWeekdayUtils.count_weekdays_between(start_date, end_date, weekday)


def next_weekday_after(start_date: Union[date, str], weekday: Union[int, Weekday],
                       inclusive: bool = False) -> date:
    """Find the next occurrence of a weekday after a date."""
    return NthWeekdayUtils.next_weekday_after(start_date, weekday, inclusive)


def previous_weekday_before(start_date: Union[date, str], weekday: Union[int, Weekday],
                            inclusive: bool = False) -> date:
    """Find the previous occurrence of a weekday before a date."""
    return NthWeekdayUtils.previous_weekday_before(start_date, weekday, inclusive)


def weekday_name(weekday: Union[int, Weekday], lang: str = 'en') -> str:
    """Get the name of a weekday."""
    return NthWeekdayUtils.weekday_name(weekday, lang)


def month_name(month: int, lang: str = 'en') -> str:
    """Get the name of a month."""
    return NthWeekdayUtils.month_name(month, lang)