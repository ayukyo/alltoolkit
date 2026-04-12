"""
AllToolkit - Python Cron Utilities

A zero-dependency cron expression parser and scheduler utility module.
Supports standard cron syntax, validation, next execution time calculation,
and simple in-memory task scheduling.

Author: AllToolkit
License: MIT
"""

import time
import threading
from typing import Optional, List, Set, Callable, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re


class CronField(Enum):
    """Cron field types with their valid ranges."""
    MINUTE = (0, 59)
    HOUR = (0, 23)
    DAY_OF_MONTH = (1, 31)
    MONTH = (1, 12)
    DAY_OF_WEEK = (0, 6)  # 0 = Sunday
    
    def __init__(self, min_val: int, max_val: int):
        self.min = min_val
        self.max = max_val


@dataclass
class CronExpression:
    """Parsed cron expression with field sets."""
    minutes: Set[int]
    hours: Set[int]
    days_of_month: Set[int]
    months: Set[int]
    days_of_week: Set[int]
    original: str
    
    def __str__(self) -> str:
        return self.original


@dataclass
class CronSchedule:
    """Represents a parsed cron schedule."""
    expression: CronExpression
    next_execution: Optional[datetime] = None
    last_execution: Optional[datetime] = None
    is_active: bool = True


@dataclass
class ScheduledTask:
    """Represents a scheduled task."""
    id: str
    name: str
    cron_expr: str
    callback: Callable[[], Any]
    schedule: CronSchedule
    created_at: datetime = field(default_factory=datetime.now)
    run_count: int = 0
    last_error: Optional[str] = None
    is_active: bool = True


class CronParseError(Exception):
    """Exception raised when cron expression parsing fails."""
    pass


class CronParser:
    """
    Parse and validate cron expressions.
    
    Supports standard 5-field cron syntax:
    ┌───────────── minute (0 - 59)
    │ ┌───────────── hour (0 - 23)
    │ │ ┌───────────── day of month (1 - 31)
    │ │ │ ┌───────────── month (1 - 12)
    │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday = 0)
    │ │ │ │ │
    * * * * *
    
    Special characters:
    - * : any value
    - , : value list separator
    - - : range
    - / : step values
    """
    
    # Month and day-of-week name mappings
    MONTH_NAMES = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    DOW_NAMES = {
        'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6
    }
    
    def __init__(self):
        self._cache: Dict[str, CronExpression] = {}
    
    def parse(self, expression: str) -> CronExpression:
        """
        Parse a cron expression string into a CronExpression object.
        
        Args:
            expression: A 5-field cron expression string
            
        Returns:
            CronExpression object with parsed field sets
            
        Raises:
            CronParseError: If the expression is invalid
        """
        # Check cache
        if expression in self._cache:
            return self._cache[expression]
        
        # Normalize whitespace
        expr = ' '.join(expression.split())
        
        # Split into fields
        fields = expr.split()
        if len(fields) != 5:
            raise CronParseError(
                f"Invalid cron expression: expected 5 fields, got {len(fields)}"
            )
        
        try:
            minutes = self._parse_field(fields[0], CronField.MINUTE)
            hours = self._parse_field(fields[1], CronField.HOUR)
            days_of_month = self._parse_field(fields[2], CronField.DAY_OF_MONTH)
            months = self._parse_field(fields[3], CronField.MONTH)
            days_of_week = self._parse_field(fields[4], CronField.DAY_OF_WEEK)
        except ValueError as e:
            raise CronParseError(f"Invalid cron expression: {e}")
        
        cron_expr = CronExpression(
            minutes=minutes,
            hours=hours,
            days_of_month=days_of_month,
            months=months,
            days_of_week=days_of_week,
            original=expr
        )
        
        self._cache[expr] = cron_expr
        return cron_expr
    
    def _parse_field(self, field: str, field_type: CronField) -> Set[int]:
        """
        Parse a single cron field into a set of valid values.
        
        Args:
            field: The field string (e.g., "*/5", "1-5", "1,3,5")
            field_type: The type of field being parsed
            
        Returns:
            Set of valid integer values for this field
        """
        values: Set[int] = set()
        
        # Handle list (comma-separated)
        for part in field.split(','):
            values.update(self._parse_part(part.strip(), field_type))
        
        if not values:
            raise ValueError(f"Empty field: {field}")
        
        return values
    
    def _parse_part(self, part: str, field_type: CronField) -> Set[int]:
        """
        Parse a single part of a cron field (handles *, ranges, steps).
        
        Args:
            part: The part string (e.g., "*/5", "1-5", "5")
            field_type: The type of field being parsed
            
        Returns:
            Set of valid integer values
        """
        values: Set[int] = set()
        min_val, max_val = field_type.min, field_type.max
        
        # Handle step values
        step = 1
        if '/' in part:
            range_part, step_str = part.split('/', 1)
            try:
                step = int(step_str)
            except ValueError:
                raise ValueError(f"Invalid step value: {step_str}")
            if step <= 0:
                raise ValueError(f"Step must be positive: {step}")
            part = range_part
        
        # Handle wildcard
        if part == '*':
            for i in range(min_val, max_val + 1, step):
                values.add(i)
            return values
        
        # Handle range
        if '-' in part:
            range_parts = part.split('-', 1)
            start = self._parse_value(range_parts[0], field_type)
            end = self._parse_value(range_parts[1], field_type)
            
            if start > end:
                raise ValueError(f"Invalid range: {start}-{end}")
            
            for i in range(start, end + 1, step):
                values.add(i)
            return values
        
        # Handle single value
        value = self._parse_value(part, field_type)
        values.add(value)
        return values
    
    def _parse_value(self, value: str, field_type: CronField) -> int:
        """
        Parse a single value (number or name).
        
        Args:
            value: The value string
            field_type: The type of field
            
        Returns:
            Integer value
        """
        value = value.lower()
        
        # Check for month names
        if field_type == CronField.MONTH and value in self.MONTH_NAMES:
            return self.MONTH_NAMES[value]
        
        # Check for day-of-week names
        if field_type == CronField.DAY_OF_WEEK and value in self.DOW_NAMES:
            return self.DOW_NAMES[value]
        
        # Parse as integer
        try:
            num = int(value)
        except ValueError:
            raise ValueError(f"Invalid value: {value}")
        
        min_val, max_val = field_type.min, field_type.max
        if num < min_val or num > max_val:
            raise ValueError(
                f"Value {num} out of range [{min_val}-{max_val}] for {field_type.name}"
            )
        
        return num
    
    def validate(self, expression: str) -> bool:
        """
        Validate a cron expression without raising exceptions.
        
        Args:
            expression: The cron expression to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.parse(expression)
            return True
        except CronParseError:
            return False
    
    def clear_cache(self) -> None:
        """Clear the expression cache."""
        self._cache.clear()


class CronMatcher:
    """
    Match datetime objects against cron expressions.
    """
    
    def __init__(self, parser: Optional[CronParser] = None):
        self.parser = parser or CronParser()
    
    def matches(self, expression: str, dt: datetime) -> bool:
        """
        Check if a datetime matches a cron expression.
        
        Args:
            expression: The cron expression
            dt: The datetime to check
            
        Returns:
            True if the datetime matches the expression
        """
        cron = self.parser.parse(expression)
        return self._matches_parsed(cron, dt)
    
    def _matches_parsed(self, cron: CronExpression, dt: datetime) -> bool:
        """Check if datetime matches parsed cron expression."""
        if dt.minute not in cron.minutes:
            return False
        if dt.hour not in cron.hours:
            return False
        if dt.day not in cron.days_of_month:
            return False
        if dt.month not in cron.months:
            return False
        if dt.weekday() not in self._convert_weekday(cron.days_of_week):
            return False
        return True
    
    def _convert_weekday(self, cron_dow: Set[int]) -> Set[int]:
        """
        Convert cron day-of-week (0=Sunday) to Python weekday (0=Monday).
        
        Args:
            cron_dow: Set of cron day-of-week values
            
        Returns:
            Set of Python weekday values
        """
        # Cron: 0=Sunday, 1=Monday, ..., 6=Saturday
        # Python: 0=Monday, 1=Tuesday, ..., 6=Sunday
        python_dow = set()
        for cron_day in cron_dow:
            if cron_day == 0:  # Sunday
                python_dow.add(6)
            else:
                python_dow.add(cron_day - 1)
        return python_dow
    
    def next_run(self, expression: str, after: Optional[datetime] = None,
                 max_iterations: int = 525600) -> Optional[datetime]:
        """
        Calculate the next execution time for a cron expression.
        
        Args:
            expression: The cron expression
            after: Start searching after this time (default: now)
            max_iterations: Maximum iterations to prevent infinite loops
                           (default: 525600 = 1 year of minutes)
            
        Returns:
            The next datetime when the cron should run, or None if not found
        """
        cron = self.parser.parse(expression)
        start = after or datetime.now()
        
        # Start from the next minute
        dt = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
        
        for _ in range(max_iterations):
            if self._matches_parsed(cron, dt):
                return dt
            dt += timedelta(minutes=1)
        
        return None
    
    def next_runs(self, expression: str, count: int = 5,
                  after: Optional[datetime] = None) -> List[datetime]:
        """
        Calculate the next N execution times for a cron expression.
        
        Args:
            expression: The cron expression
            count: Number of execution times to calculate
            after: Start searching after this time (default: now)
            
        Returns:
            List of upcoming execution datetimes
        """
        runs: List[datetime] = []
        current = after
        
        for _ in range(count):
            next_run = self.next_run(expression, after=current)
            if next_run is None:
                break
            runs.append(next_run)
            current = next_run
        
        return runs


class CronScheduler:
    """
    In-memory cron-based task scheduler.
    
    Note: This is a simple in-memory scheduler. For production use,
    consider using a more robust solution with persistence.
    """
    
    def __init__(self, parser: Optional[CronParser] = None):
        self.parser = parser or CronParser()
        self.matcher = CronMatcher(self.parser)
        self._tasks: Dict[str, ScheduledTask] = {}
        self._lock = threading.RLock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._check_interval = 10.0  # Check every 10 seconds
    
    def add_task(self, task_id: str, name: str, cron_expr: str,
                 callback: Callable[[], Any]) -> ScheduledTask:
        """
        Add a scheduled task.
        
        Args:
            task_id: Unique identifier for the task
            name: Human-readable name
            cron_expr: Cron expression for scheduling
            callback: Function to call when task runs
            
        Returns:
            The created ScheduledTask object
            
        Raises:
            CronParseError: If the cron expression is invalid
            ValueError: If task_id already exists
        """
        with self._lock:
            if task_id in self._tasks:
                raise ValueError(f"Task {task_id} already exists")
            
            # Validate and parse the expression
            schedule = CronSchedule(
                expression=self.parser.parse(cron_expr),
                next_execution=self.matcher.next_run(cron_expr)
            )
            
            task = ScheduledTask(
                id=task_id,
                name=name,
                cron_expr=cron_expr,
                callback=callback,
                schedule=schedule
            )
            
            self._tasks[task_id] = task
            return task
    
    def remove_task(self, task_id: str) -> bool:
        """
        Remove a scheduled task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            True if task was removed, False if not found
        """
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get a task by ID."""
        with self._lock:
            return self._tasks.get(task_id)
    
    def list_tasks(self) -> List[ScheduledTask]:
        """List all scheduled tasks."""
        with self._lock:
            return list(self._tasks.values())
    
    def enable_task(self, task_id: str) -> bool:
        """Enable a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.is_active = True
                task.schedule.is_active = True
                return True
            return False
    
    def disable_task(self, task_id: str) -> bool:
        """Disable a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.is_active = False
                task.schedule.is_active = False
                return True
            return False
    
    def start(self, check_interval: float = 10.0) -> None:
        """
        Start the scheduler background thread.
        
        Args:
            check_interval: How often to check for tasks to run (seconds)
        """
        with self._lock:
            if self._running:
                return
            
            self._running = True
            self._check_interval = check_interval
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
    
    def stop(self) -> None:
        """Stop the scheduler."""
        with self._lock:
            self._running = False
            if self._thread:
                self._thread.join(timeout=5.0)
                self._thread = None
    
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running
    
    def _run_loop(self) -> None:
        """Main scheduler loop."""
        while self._running:
            try:
                self._check_and_run()
            except Exception as e:
                # Log error but continue running
                pass
            time.sleep(self._check_interval)
    
    def _check_and_run(self) -> None:
        """Check all tasks and run those that are due."""
        now = datetime.now()
        
        with self._lock:
            for task in self._tasks.values():
                if not task.is_active:
                    continue
                
                next_exec = task.schedule.next_execution
                if next_exec and now >= next_exec:
                    self._run_task(task, now)
    
    def _run_task(self, task: ScheduledTask, run_time: datetime) -> None:
        """Execute a task and update its schedule."""
        task.schedule.last_execution = run_time
        task.run_count += 1
        
        try:
            task.callback()
        except Exception as e:
            task.last_error = str(e)
        
        # Calculate next execution time
        task.schedule.next_execution = self.matcher.next_run(
            task.cron_expr, after=run_time
        )
    
    def run_due_tasks(self) -> List[str]:
        """
        Manually check and run all due tasks (for testing).
        
        Returns:
            List of task IDs that were run
        """
        now = datetime.now()
        run_tasks: List[str] = []
        
        with self._lock:
            for task in self._tasks.values():
                if not task.is_active:
                    continue
                
                next_exec = task.schedule.next_execution
                if next_exec and now >= next_exec:
                    self._run_task(task, now)
                    run_tasks.append(task.id)
        
        return run_tasks


# Convenience functions
_default_parser = CronParser()
_default_matcher = CronMatcher(_default_parser)


def parse(expression: str) -> CronExpression:
    """Parse a cron expression."""
    return _default_parser.parse(expression)


def validate(expression: str) -> bool:
    """Validate a cron expression."""
    return _default_parser.validate(expression)


def matches(expression: str, dt: datetime) -> bool:
    """Check if a datetime matches a cron expression."""
    return _default_matcher.matches(expression, dt)


def next_run(expression: str, after: Optional[datetime] = None) -> Optional[datetime]:
    """Get the next execution time for a cron expression."""
    return _default_matcher.next_run(expression, after)


def next_runs(expression: str, count: int = 5,
              after: Optional[datetime] = None) -> List[datetime]:
    """Get the next N execution times for a cron expression."""
    return _default_matcher.next_runs(expression, count, after)


def create_scheduler() -> CronScheduler:
    """Create a new CronScheduler instance."""
    return CronScheduler()
