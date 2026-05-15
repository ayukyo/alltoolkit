"""
Cron Expression Utilities

A comprehensive tool for parsing, validating, and computing cron expressions.
Supports standard 5-field and 6-field (with seconds) cron formats.

Features:
- Parse cron expressions into structured format
- Validate cron expressions
- Calculate next execution times
- Support for special characters: * , - /
- No external dependencies

Author: AllToolkit
Date: 2025-05-15
"""

import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict, Any
from calendar import monthrange


class CronParseError(Exception):
    """Exception raised when cron expression parsing fails."""
    pass


class CronExpression:
    """
    Represents a parsed cron expression with methods for computing execution times.
    
    Supported format (5-field):
        ┌───────────── minute (0-59)
        │ ┌───────────── hour (0-23)
        │ │ ┌───────────── day of month (1-31)
        │ │ │ ┌───────────── month (1-12)
        │ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
        │ │ │ │ │
        * * * * *
    
    Supported format (6-field with seconds):
        ┌───────────── second (0-59)
        │ ┌───────────── minute (0-59)
        │ │ ┌───────────── hour (0-23)
        │ │ │ ┌───────────── day of month (1-31)
        │ │ │ │ ┌───────────── month (1-12)
        │ │ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
        │ │ │ │ │ │
        * * * * * *
    
    Special characters:
        * - any value
        , - value list separator
        - - range
        / - step values
    """
    
    # Field definitions: (name, min, max)
    FIELD_DEFS_5 = [
        ('minute', 0, 59),
        ('hour', 0, 23),
        ('day_of_month', 1, 31),
        ('month', 1, 12),
        ('day_of_week', 0, 6),
    ]
    
    FIELD_DEFS_6 = [
        ('second', 0, 59),
        ('minute', 0, 59),
        ('hour', 0, 23),
        ('day_of_month', 1, 31),
        ('month', 1, 12),
        ('day_of_week', 0, 6),
    ]
    
    # Month name mappings
    MONTH_NAMES = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    }
    
    # Day of week name mappings
    DOW_NAMES = {
        'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6,
    }
    
    def __init__(self, expression: str):
        """
        Initialize a CronExpression from a string.
        
        Args:
            expression: Cron expression string (5 or 6 fields)
        """
        self.original = expression.strip()
        self.has_seconds = False
        self.fields: Dict[str, List[int]] = {}
        self._parse()
    
    def _parse(self) -> None:
        """Parse the cron expression into field sets."""
        parts = self.original.split()
        
        if len(parts) == 5:
            field_defs = self.FIELD_DEFS_5
            self.has_seconds = False
        elif len(parts) == 6:
            field_defs = self.FIELD_DEFS_6
            self.has_seconds = True
        else:
            raise CronParseError(
                f"Invalid cron expression: expected 5 or 6 fields, got {len(parts)}"
            )
        
        for i, (name, min_val, max_val) in enumerate(field_defs):
            self.fields[name] = self._parse_field(
                parts[i], min_val, max_val, name
            )
    
    def _parse_field(
        self, 
        field: str, 
        min_val: int, 
        max_val: int, 
        name: str
    ) -> List[int]:
        """
        Parse a single cron field into a list of valid values.
        
        Args:
            field: Field string (e.g., "*/5", "1,3,5", "1-10/2")
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            name: Field name for error messages
            
        Returns:
            Sorted list of valid integer values
        """
        # Handle special names for month and day of week
        field_lower = field.lower()
        if name == 'month':
            for month_name, month_num in self.MONTH_NAMES.items():
                field_lower = field_lower.replace(month_name, str(month_num))
        elif name == 'day_of_week':
            for dow_name, dow_num in self.DOW_NAMES.items():
                field_lower = field_lower.replace(dow_name, str(dow_num))
        field = field_lower
        
        values: List[int] = []
        
        # Split by comma for multiple parts
        for part in field.split(','):
            part = part.strip()
            if not part:
                continue
            
            # Check for step notation
            step = 1
            if '/' in part:
                range_part, step_part = part.split('/', 1)
                try:
                    step = int(step_part)
                    if step <= 0:
                        raise CronParseError(f"Step must be positive: {step_part}")
                except ValueError:
                    raise CronParseError(f"Invalid step value: {step_part}")
                part = range_part
            
            # Determine range
            if part == '*':
                start, end = min_val, max_val
            elif '-' in part:
                try:
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str)
                    end = int(end_str)
                except ValueError:
                    raise CronParseError(f"Invalid range: {part}")
            else:
                try:
                    start = end = int(part)
                except ValueError:
                    raise CronParseError(f"Invalid value: {part}")
            
            # Validate range
            if start < min_val or start > max_val:
                raise CronParseError(
                    f"Value {start} out of range [{min_val}-{max_val}] for {name}"
                )
            if end < min_val or end > max_val:
                raise CronParseError(
                    f"Value {end} out of range [{min_val}-{max_val}] for {name}"
                )
            
            # Generate values with step
            for v in range(start, end + 1, step):
                if v not in values:
                    values.append(v)
        
        return sorted(values)
    
    def get_next_run(self, from_time: Optional[datetime] = None) -> datetime:
        """
        Calculate the next execution time after the given datetime.
        
        Args:
            from_time: Starting datetime (defaults to current time)
            
        Returns:
            Next execution datetime
            
        Raises:
            ValueError: If no valid next run time can be found within 5 years
        """
        if from_time is None:
            from_time = datetime.now()
        
        # Start from the next second
        current = from_time.replace(microsecond=0)
        if self.has_seconds:
            current += timedelta(seconds=1)
        else:
            current += timedelta(minutes=1)
            current = current.replace(second=0)
        
        # Maximum search: 5 years
        max_date = from_time + timedelta(days=5*365)
        
        while current <= max_date:
            if self._matches(current):
                return current
            current = self._increment(current)
        
        raise ValueError("Could not find next run time within 5 years")
    
    def get_next_runs(
        self, 
        from_time: Optional[datetime] = None, 
        count: int = 5
    ) -> List[datetime]:
        """
        Calculate the next N execution times.
        
        Args:
            from_time: Starting datetime (defaults to current time)
            count: Number of future times to return
            
        Returns:
            List of next execution datetimes
        """
        if from_time is None:
            from_time = datetime.now()
        
        runs: List[datetime] = []
        current = from_time
        
        for _ in range(count):
            next_run = self.get_next_run(current)
            runs.append(next_run)
            current = next_run
        
        return runs
    
    def _matches(self, dt: datetime) -> bool:
        """Check if a datetime matches the cron expression."""
        # Check each field
        if dt.minute not in self.fields['minute']:
            return False
        if dt.hour not in self.fields['hour']:
            return False
        if dt.month not in self.fields['month']:
            return False
        
        # Day matching is special - both day of month and day of week must match
        # if both are restricted (not *), OR logic applies
        dom_restricted = self.fields['day_of_month'] != list(range(1, 32))
        dow_restricted = self.fields['day_of_week'] != list(range(0, 7))
        
        dom_matches = dt.day in self.fields['day_of_month']
        dow_matches = dt.weekday() in [d - 1 if d > 0 else 6 for d in self.fields['day_of_week']]
        # Convert Python weekday (0=Monday) to cron weekday (0=Sunday)
        cron_dow = (dt.weekday() + 1) % 7
        dow_matches = cron_dow in self.fields['day_of_week']
        
        if dom_restricted and dow_restricted:
            # Both restricted - OR logic
            if not (dom_matches or dow_matches):
                return False
        elif dom_restricted:
            if not dom_matches:
                return False
        elif dow_restricted:
            if not dow_matches:
                return False
        
        # Check seconds if 6-field format
        if self.has_seconds and dt.second not in self.fields['second']:
            return False
        
        return True
    
    def _increment(self, dt: datetime) -> datetime:
        """Increment datetime to the next potential match."""
        if self.has_seconds:
            return dt + timedelta(seconds=1)
        return dt + timedelta(minutes=1)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the cron expression to a dictionary representation."""
        return {
            'original': self.original,
            'has_seconds': self.has_seconds,
            'fields': {k: v for k, v in self.fields.items()},
        }
    
    def __str__(self) -> str:
        return f"CronExpression('{self.original}')"
    
    def __repr__(self) -> str:
        return self.__str__()


def parse_cron(expression: str) -> CronExpression:
    """
    Parse a cron expression string.
    
    Args:
        expression: Cron expression string (5 or 6 fields)
        
    Returns:
        CronExpression object
        
    Raises:
        CronParseError: If the expression is invalid
    """
    return CronExpression(expression)


def validate_cron(expression: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a cron expression.
    
    Args:
        expression: Cron expression string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        CronExpression(expression)
        return True, None
    except CronParseError as e:
        return False, str(e)


def get_next_run(
    expression: str, 
    from_time: Optional[datetime] = None
) -> datetime:
    """
    Get the next run time for a cron expression.
    
    Args:
        expression: Cron expression string
        from_time: Starting datetime (defaults to current time)
        
    Returns:
        Next execution datetime
    """
    cron = CronExpression(expression)
    return cron.get_next_run(from_time)


def get_next_runs(
    expression: str, 
    from_time: Optional[datetime] = None, 
    count: int = 5
) -> List[datetime]:
    """
    Get the next N run times for a cron expression.
    
    Args:
        expression: Cron expression string
        from_time: Starting datetime (defaults to current time)
        count: Number of future times to return
        
    Returns:
        List of next execution datetimes
    """
    cron = CronExpression(expression)
    return cron.get_next_runs(from_time, count)


def cron_to_human_readable(expression: str) -> str:
    """
    Convert a cron expression to a human-readable description.
    
    Args:
        expression: Cron expression string
        
    Returns:
        Human-readable description
    """
    cron = CronExpression(expression)
    
    parts = []
    
    # Seconds
    if cron.has_seconds:
        seconds = cron.fields['second']
        if seconds == list(range(60)):
            parts.append("every second")
        elif len(seconds) == 1:
            parts.append(f"at second {seconds[0]}")
        else:
            parts.append(f"at seconds {', '.join(map(str, seconds))}")
    
    # Minutes
    minutes = cron.fields['minute']
    if minutes == list(range(60)):
        if cron.has_seconds:
            pass  # Already said "every second"
        else:
            parts.append("every minute")
    elif len(minutes) == 1:
        parts.append(f"at minute {minutes[0]}")
    else:
        parts.append(f"at minutes {', '.join(map(str, minutes))}")
    
    # Hours
    hours = cron.fields['hour']
    if hours != list(range(24)):
        if len(hours) == 1:
            parts.append(f"of hour {hours[0]}")
        else:
            parts.append(f"of hours {', '.join(map(str, hours))}")
    
    # Days of month
    dom = cron.fields['day_of_month']
    dom_restricted = dom != list(range(1, 32))
    
    # Days of week
    dow = cron.fields['day_of_week']
    dow_restricted = dow != list(range(7))
    dow_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    if dom_restricted and dow_restricted:
        parts.append(f"on day {', '.join(map(str, dom))} of month or on {', '.join(dow_names[d] for d in dow)}")
    elif dom_restricted:
        if len(dom) == 1:
            parts.append(f"on day {dom[0]} of month")
        else:
            parts.append(f"on days {', '.join(map(str, dom))} of month")
    elif dow_restricted:
        parts.append(f"on {', '.join(dow_names[d] for d in dow)}")
    
    # Months
    months = cron.fields['month']
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    if months != list(range(1, 13)):
        parts.append(f"in {', '.join(month_names[m-1] for m in months)}")
    
    return " ".join(parts) if parts else "every second"


# Common cron presets
CRON_PRESETS = {
    'every_minute': '* * * * *',
    'every_hour': '0 * * * *',
    'every_day': '0 0 * * *',
    'every_week': '0 0 * * 0',
    'every_month': '0 0 1 * *',
    'every_year': '0 0 1 1 *',
    'every_5_minutes': '*/5 * * * *',
    'every_15_minutes': '*/15 * * * *',
    'every_30_minutes': '*/30 * * * *',
    'every_6_hours': '0 */6 * * *',
    'every_12_hours': '0 */12 * * *',
    'every_weekday': '0 0 * * 1-5',
    'every_weekend': '0 0 * * 0,6',
}


def get_preset(preset_name: str) -> Optional[str]:
    """
    Get a cron expression by preset name.
    
    Args:
        preset_name: Name of the preset (e.g., 'every_hour')
        
    Returns:
        Cron expression string or None if preset not found
    """
    return CRON_PRESETS.get(preset_name.lower())


def list_presets() -> Dict[str, str]:
    """
    List all available cron presets.
    
    Returns:
        Dictionary of preset names to cron expressions
    """
    return dict(CRON_PRESETS)


# Export public API
__all__ = [
    'CronExpression',
    'CronParseError',
    'parse_cron',
    'validate_cron',
    'get_next_run',
    'get_next_runs',
    'cron_to_human_readable',
    'get_preset',
    'list_presets',
    'CRON_PRESETS',
]