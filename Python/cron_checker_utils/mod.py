"""
Cron Checker Utils - Validate and check cron expression execution times

This module provides utilities for:
- Validating cron expressions
- Getting next/last execution times
- Checking if a cron expression matches a specific time
- Converting cron expressions to human-readable descriptions
- Getting the execution history within a time range
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple


class CronChecker:
    """
    Validate and check cron expression execution times.
    
    Supports standard 5-field cron format: minute, hour, day of month,
    month, day of week. Also supports special strings: @yearly, @monthly,
    @weekly, @daily, @hourly, @annually, @midnight, @noon.
    """
    
    # Special cron expressions
    SPECIAL_EXPRESSIONS = {
        '@yearly': '0 0 1 1 *',
        '@annually': '0 0 1 1 *',
        '@monthly': '0 0 1 * *',
        '@weekly': '0 0 * * 0',
        '@daily': '0 0 * * *',
        '@midnight': '0 0 * * *',
        '@noon': '0 12 * * *',
        '@hourly': '0 * * * *',
    }
    
    # Month names mapping
    MONTH_MAP = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    # Day of week names mapping
    DOW_MAP = {
        'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3,
        'thu': 4, 'fri': 5, 'sat': 6
    }
    
    def __init__(self, expression: str):
        """
        Initialize with a cron expression.
        
        Args:
            expression: Cron expression string (e.g., '0 0 * * *' or '@daily')
        
        Raises:
            ValueError: If the expression format is invalid
        """
        self.raw_expression = expression.strip()
        self.expression = self._expand_special(expression.strip())
        self.fields = self.expression.split()
        
        if len(self.fields) != 5:
            raise ValueError(
                f"Cron expression must have 5 fields, got {len(self.fields)}: {expression}"
            )
        
        self._minute, self._hour, self._day, self._month, self._dow = self.fields
        self._validate_fields()
    
    def _expand_special(self, expr: str) -> str:
        """Expand special cron strings to standard format."""
        expr_lower = expr.lower().strip()
        if expr_lower in self.SPECIAL_EXPRESSIONS:
            return self.SPECIAL_EXPRESSIONS[expr_lower]
        return expr
    
    def _validate_fields(self) -> None:
        """Validate each field of the cron expression."""
        self._validate_field(self._minute, 0, 59, 'minute')
        self._validate_field(self._hour, 0, 23, 'hour')
        self._validate_field(self._day, 1, 31, 'day of month')
        self._validate_field(self._month, 1, 12, 'month')
        self._validate_field(self._dow, 0, 6, 'day of week')
    
    def _validate_field(self, field: str, min_val: int, max_val: int, name: str) -> None:
        """Validate a single cron field."""
        if field == '*':
            return
        
        for part in field.split(','):
            if '/' in part:
                base, step = part.split('/')
                base = base.strip() if base.strip() else '*'
                step_val = int(step)
                if step_val <= 0:
                    raise ValueError(f"Invalid step value {step_val} in {name} field")
                if base != '*':
                    try:
                        base_val = self._parse_value(base, min_val, max_val)
                    except ValueError:
                        raise ValueError(f"Invalid base value '{base}' in {name} field")
            elif '-' in part:
                start, end = part.split('-')
                try:
                    start_val = self._parse_value(start.strip(), min_val, max_val)
                    end_val = self._parse_value(end.strip(), min_val, max_val)
                except ValueError:
                    raise ValueError(f"Invalid range '{part}' in {name} field")
                if start_val > end_val:
                    raise ValueError(f"Invalid range: start ({start_val}) > end ({end_val}) in {name} field")
            else:
                try:
                    self._parse_value(part.strip(), min_val, max_val)
                except ValueError:
                    raise ValueError(f"Invalid value '{part}' in {name} field")
    
    def _parse_value(self, value: str, min_val: int, max_val: int) -> int:
        """Parse a single value (number or name) to integer."""
        value_lower = value.lower()
        if value_lower in self.MONTH_MAP and max_val == 12:
            return self.MONTH_MAP[value_lower]
        if value_lower in self.DOW_MAP and max_val == 6:
            return self.DOW_MAP[value_lower]
        try:
            num = int(value)
            if num < min_val or num > max_val:
                raise ValueError(f"Value {num} out of range [{min_val}, {max_val}]")
            return num
        except ValueError:
            raise ValueError(f"Invalid value: {value}")
    
    def _expand_field(self, field: str, min_val: int, max_val: int) -> List[int]:
        """
        Expand a cron field to a list of matching values.
        
        Returns all values that match the field pattern.
        """
        if field == '*':
            return list(range(min_val, max_val + 1))
        
        result = set()
        
        for part in field.split(','):
            if '/' in part:
                base, step = part.split('/')
                base = base.strip() if base.strip() else '*'
                step_val = int(step)
                
                if base == '*':
                    base_values = list(range(min_val, max_val + 1))
                elif '-' in base:
                    start, end = base.split('-')
                    start_val = self._parse_value(start.strip(), min_val, max_val)
                    end_val = self._parse_value(end.strip(), min_val, max_val)
                    base_values = list(range(start_val, end_val + 1))
                else:
                    base_values = [self._parse_value(base.strip(), min_val, max_val)]
                
                for i, val in enumerate(base_values):
                    if i % step_val == 0:
                        result.add(val)
            elif '-' in part:
                start, end = part.split('-')
                start_val = self._parse_value(start.strip(), min_val, max_val)
                end_val = self._parse_value(end.strip(), min_val, max_val)
                result.update(range(start_val, end_val + 1))
            else:
                result.add(self._parse_value(part.strip(), min_val, max_val))
        
        return sorted(result)
    
    def _field_matches(self, field: str, value: int, min_val: int, max_val: int) -> bool:
        """Check if a field matches a specific value."""
        if field == '*':
            return True
        
        matches = self._expand_field(field, min_val, max_val)
        return value in matches
    
    def matches(self, dt: datetime) -> bool:
        """
        Check if the cron expression matches a specific datetime.
        
        Args:
            dt: Datetime to check
            
        Returns:
            True if the cron expression matches the given datetime
        """
        # Check month
        if not self._field_matches(self._month, dt.month, 1, 12):
            return False
        
        # Check day of month (1-31)
        if not self._field_matches(self._day, dt.day, 1, 31):
            return False
        
        # Check day of week (0-6, 0=Sunday)
        if not self._field_matches(self._dow, dt.weekday(), 0, 6):
            return False
        
        # Check hour
        if not self._field_matches(self._hour, dt.hour, 0, 23):
            return False
        
        # Check minute
        if not self._field_matches(self._minute, dt.minute, 0, 59):
            return False
        
        return True
    
    def _days_in_month(self, year: int, month: int) -> int:
        """Get the number of days in a month."""
        from calendar import monthrange
        return monthrange(year, month)[1]
    
    def get_next_run(self, after: Optional[datetime] = None) -> datetime:
        """
        Get the next execution time after a given datetime.
        
        Args:
            after: Starting datetime (defaults to now)
            
        Returns:
            Next execution datetime
        """
        if after is None:
            after = datetime.now()
        
        current = after.replace(second=0, microsecond=0)
        if current.minute == 0 and current.second == 0 and current.microsecond == 0:
            current = current - timedelta(minutes=1)
        
        # Simple iterative approach - iterate forward minute by minute
        # Maximum 2 years worth of iterations
        max_minutes = 365 * 2 * 24 * 60
        
        for _ in range(max_minutes):
            current = current + timedelta(minutes=1)
            if self.matches(current):
                return current
        
        raise RuntimeError("Could not find next run time within 2 years")
    
    def get_last_run(self, before: Optional[datetime] = None) -> datetime:
        """
        Get the last execution time before a given datetime.
        
        Args:
            before: Ending datetime (defaults to now)
            
        Returns:
            Last execution datetime
        """
        if before is None:
            before = datetime.now()
        
        current = before.replace(second=0, microsecond=0)
        
        # Iterate backwards (max 2 years)
        max_minutes = 365 * 2 * 24 * 60
        
        for _ in range(max_minutes):
            if self.matches(current):
                return current
            current = current - timedelta(minutes=1)
        
        raise RuntimeError("Could not find last run time")
    
    def get_run_times(self, start: datetime, end: datetime) -> List[datetime]:
        """
        Get all execution times within a date range.
        
        Args:
            start: Start datetime (inclusive)
            end: End datetime (inclusive)
            
        Returns:
            List of execution datetimes
        """
        results = []
        current = self.get_next_run(self._sub_minute(start))
        
        while current <= end:
            results.append(current)
            current = self.get_next_run(current)
        
        return results
    
    def _sub_minute(self, dt: datetime) -> datetime:
        """Subtract one minute from datetime."""
        return dt - timedelta(minutes=1)
    
    def describe(self) -> str:
        """
        Get a human-readable description of the cron expression.
        
        Returns:
            Human-readable description string
        """
        minute = self._minute
        hour = self._hour
        day = self._day
        month = self._month
        dow = self._dow
        
        # Special patterns
        if self.expression == '0 0 1 1 *':
            return 'At 00:00 on January 1st'
        if self.expression == '0 0 1 * *':
            return 'At 00:00 on day 1 of every month'
        if self.expression == '0 0 * * 0':
            return 'At 00:00 every Sunday'
        if self.expression == '0 0 * * *':
            return 'At 00:00 every day'
        if self.expression == '0 12 * * *':
            return 'At 12:00 every day'
        if self.expression == '0 * * * *':
            return 'Every hour'
        
        parts = []
        
        # Time description
        if minute == '*' and hour == '*':
            time_desc = 'Every minute'
        elif minute == '*':
            time_desc = f'Every minute during hour {hour}'
        elif hour == '*':
            if minute == '0':
                time_desc = 'Every hour'
            else:
                time_desc = f'Every hour at minute {minute}'
        else:
            time_desc = f'At {hour}:{minute.zfill(2) if len(minute) < 2 else minute}'
        parts.append(time_desc)
        
        # Day of month
        if day != '*':
            parts.append(f'on day {day} of the month')
        
        # Month
        if month != '*':
            month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            if ',' in month or '-' in month:
                parts.append(f'in months {month}')
            else:
                month_num = int(month) if month.isdigit() else self.MONTH_MAP.get(month.lower(), int(month))
                parts.append(f'in {month_names[month_num - 1]}')
        
        # Day of week
        dow_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if dow != '*':
            if ',' in dow:
                dows = [dow_names[self.DOW_MAP.get(d.strip(), int(d))] for d in dow.split(',')]
                parts.append(f'on {" and ".join(dows)}')
            elif '-' in dow:
                parts.append(f'on weekdays {dow}')
            else:
                dow_num = int(dow) if dow.isdigit() else self.DOW_MAP.get(dow.lower(), int(dow))
                parts.append(f'on {dow_names[dow_num]}')
        
        return ' '.join(parts)
    
    def to_dict(self) -> dict:
        """
        Get the cron expression as a dictionary of its components.
        
        Returns:
            Dictionary with minute, hour, day, month, dow keys
        """
        return {
            'expression': self.expression,
            'minute': self._minute,
            'hour': self._hour,
            'day': self._day,
            'month': self._month,
            'dow': self._dow,
            'description': self.describe()
        }


def validate(expression: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a cron expression.
    
    Args:
        expression: Cron expression string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        CronChecker(expression)
        return True, None
    except ValueError as e:
        return False, str(e)


def get_next_run(expression: str, after: Optional[datetime] = None) -> datetime:
    """
    Get the next execution time for a cron expression.
    
    Args:
        expression: Cron expression string
        after: Starting datetime (defaults to now)
        
    Returns:
        Next execution datetime
    """
    return CronChecker(expression).get_next_run(after)


def get_last_run(expression: str, before: Optional[datetime] = None) -> datetime:
    """
    Get the last execution time for a cron expression.
    
    Args:
        expression: Cron expression string
        before: Ending datetime (defaults to now)
        
    Returns:
        Last execution datetime
    """
    return CronChecker(expression).get_last_run(before)


def get_run_times(expression: str, start: datetime, end: datetime) -> List[datetime]:
    """
    Get all execution times for a cron expression within a range.
    
    Args:
        expression: Cron expression string
        start: Start datetime (inclusive)
        end: End datetime (inclusive)
        
    Returns:
        List of execution datetimes
    """
    return CronChecker(expression).get_run_times(start, end)


def matches(expression: str, dt: datetime) -> bool:
    """
    Check if a cron expression matches a specific datetime.
    
    Args:
        expression: Cron expression string
        dt: Datetime to check
        
    Returns:
        True if the expression matches the datetime
    """
    return CronChecker(expression).matches(dt)


def describe(expression: str) -> str:
    """
    Get a human-readable description of a cron expression.
    
    Args:
        expression: Cron expression string
        
    Returns:
        Human-readable description
    """
    return CronChecker(expression).describe()