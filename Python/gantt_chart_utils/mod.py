"""
Gantt Chart Utilities - Zero-dependency ASCII Gantt chart generator.

A lightweight library for creating ASCII/text Gantt charts for project
management visualization. Perfect for CLI tools and terminal-based
project tracking.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents a task in the Gantt chart."""
    name: str
    start: datetime
    end: datetime
    progress: float = 0.0  # 0.0 to 1.0
    color: str = ""  # For future color support
    dependencies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"Task '{self.name}': start date cannot be after end date")
        if not 0.0 <= self.progress <= 1.0:
            raise ValueError(f"Task '{self.name}': progress must be between 0.0 and 1.0")
    
    @property
    def duration_days(self) -> int:
        """Return duration in days (inclusive)."""
        return (self.end - self.start).days + 1
    
    @property
    def is_complete(self) -> bool:
        """Check if task is complete."""
        return self.progress >= 1.0


@dataclass
class Milestone:
    """Represents a milestone in the Gantt chart."""
    name: str
    date: datetime
    color: str = ""


class GanttChart:
    """
    ASCII Gantt chart generator.
    
    Example:
        >>> chart = GanttChart()
        >>> chart.add_task("Design", datetime(2024, 1, 1), datetime(2024, 1, 5))
        >>> chart.add_task("Development", datetime(2024, 1, 3), datetime(2024, 1, 10), progress=0.5)
        >>> print(chart.render())
    """
    
    # ASCII characters for drawing
    CHAR_EMPTY = "░"
    CHAR_PROGRESS = "█"
    CHAR_REMAINING = "▒"
    CHAR_MILESTONE = "◆"
    CHAR_CONNECTOR = "│"
    CHAR_ARROW_H = "─"
    CHAR_ARROW_HEAD = ">"
    CHAR_CURRENT = "▼"
    
    def __init__(self, title: str = "Project Timeline"):
        self.title = title
        self.tasks: List[Task] = []
        self.milestones: List[Milestone] = []
        self.current_date: Optional[datetime] = None
    
    def add_task(
        self,
        name: str,
        start: datetime,
        end: datetime,
        progress: float = 0.0,
        dependencies: Optional[List[str]] = None
    ) -> "GanttChart":
        """Add a task to the chart."""
        task = Task(
            name=name,
            start=start,
            end=end,
            progress=progress,
            dependencies=dependencies or []
        )
        self.tasks.append(task)
        return self
    
    def add_milestone(self, name: str, date: datetime) -> "GanttChart":
        """Add a milestone to the chart."""
        self.milestones.append(Milestone(name=name, date=date))
        return self
    
    def set_current_date(self, date: datetime) -> "GanttChart":
        """Set the current date marker."""
        self.current_date = date
        return self
    
    def _get_date_range(self) -> Tuple[datetime, datetime]:
        """Get the date range covering all tasks and milestones."""
        if not self.tasks and not self.milestones:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return today, today + timedelta(days=7)
        
        all_dates = []
        for task in self.tasks:
            all_dates.extend([task.start, task.end])
        for milestone in self.milestones:
            all_dates.append(milestone.date)
        
        min_date = min(all_dates)
        max_date = max(all_dates)
        
        # Add some padding
        min_date = min_date - timedelta(days=1)
        max_date = max_date + timedelta(days=1)
        
        return min_date, max_date
    
    def _date_to_position(self, date: datetime, start_date: datetime, scale: int = 1) -> int:
        """Convert date to chart position."""
        days = (date - start_date).days
        return max(0, days * scale)
    
    def _get_char_width(self, date_range: int) -> int:
        """Calculate character width per day."""
        if date_range <= 7:
            return 4  # 4 chars per day for short ranges
        elif date_range <= 30:
            return 2  # 2 chars per day for medium ranges
        else:
            return 1  # 1 char per day for long ranges
    
    def _truncate_name(self, name: str, max_len: int) -> str:
        """Truncate task name to fit column width."""
        if len(name) <= max_len:
            return name
        return name[:max_len - 3] + "..."
    
    def _render_date_header(self, start_date: datetime, end_date: datetime, width_per_day: int) -> List[str]:
        """Render the date header row(s)."""
        days = (end_date - start_date).days + 1
        name_width = 20
        
        # Month header
        months = {}
        for i in range(days):
            date = start_date + timedelta(days=i)
            month_key = date.strftime("%Y-%m")
            if month_key not in months:
                months[month_key] = {"start": i, "end": i, "name": date.strftime("%b %Y")}
            else:
                months[month_key]["end"] = i
        
        month_line = " " * name_width + "│"
        for month_data in months.values():
            month_width = (month_data["end"] - month_data["start"] + 1) * width_per_day
            month_str = month_data["name"].center(month_width)
            month_line += month_str
        
        # Day header
        day_line = " " * name_width + "│"
        date_line = " " * name_width + "│"
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            day_str = str(date.day).zfill(2)[:width_per_day].ljust(width_per_day)
            day_line += day_str
            
            # Weekday
            weekday = date.strftime("%a")[0]
            date_line += weekday.center(width_per_day)
        
        return [month_line, day_line, date_line]
    
    def _render_task(self, task: Task, start_date: datetime, width_per_day: int) -> str:
        """Render a single task row."""
        name_width = 20
        total_days = (self._get_date_range()[1] - start_date).days + 1
        
        # Build task bar
        bar = []
        for i in range(total_days):
            current_date = start_date + timedelta(days=i)
            
            if current_date < task.start or current_date > task.end:
                bar.append(self.CHAR_EMPTY * width_per_day)
            elif self._date_to_position(current_date, start_date) < self._date_to_position(task.start, start_date):
                bar.append(self.CHAR_EMPTY * width_per_day)
            else:
                # Calculate progress position
                task_duration = task.duration_days
                task_start_pos = self._date_to_position(task.start, start_date)
                current_pos = i
                
                # Check if this day is within progress
                progress_days = int(task_duration * task.progress)
                days_from_start = i - self._date_to_position(task.start, start_date)
                
                if days_from_start < progress_days:
                    bar.append(self.CHAR_PROGRESS * width_per_day)
                else:
                    bar.append(self.CHAR_REMAINING * width_per_day)
        
        task_name = self._truncate_name(task.name, name_width - 1)
        bar_str = "".join(bar)
        
        # Add progress percentage
        progress_str = f" {int(task.progress * 100)}%"
        
        return f"{task_name.ljust(name_width)}│{bar_str}{progress_str}"
    
    def _render_milestone(self, milestone: Milestone, start_date: datetime, width_per_day: int) -> str:
        """Render a milestone row."""
        name_width = 20
        total_days = (self._get_date_range()[1] - start_date).days + 1
        
        bar = []
        for i in range(total_days):
            current_date = start_date + timedelta(days=i)
            if current_date == milestone.date:
                bar.append(self.CHAR_MILESTONE.center(width_per_day))
            else:
                bar.append(self.CHAR_EMPTY * width_per_day)
        
        milestone_name = self._truncate_name(milestone.name, name_width - 1)
        bar_str = "".join(bar)
        
        return f"{milestone_name.ljust(name_width)}│{bar_str}"
    
    def _render_current_date_marker(self, start_date: datetime, width_per_day: int) -> str:
        """Render the current date marker row."""
        if not self.current_date:
            return ""
        
        name_width = 20
        total_days = (self._get_date_range()[1] - start_date).days + 1
        
        bar = []
        for i in range(total_days):
            current_date = start_date + timedelta(days=i)
            if current_date == self.current_date:
                bar.append(self.CHAR_CURRENT.center(width_per_day))
            else:
                bar.append(" " * width_per_day)
        
        return f"{'Today'.ljust(name_width)}│{''.join(bar)}"
    
    def render(
        self,
        show_progress: bool = True,
        show_weekends: bool = True,
        compact: bool = False
    ) -> str:
        """
        Render the Gantt chart as ASCII art.
        
        Args:
            show_progress: Whether to show task progress
            show_weekends: Whether to include weekends
            compact: Use compact output format
            
        Returns:
            ASCII Gantt chart string
        """
        if not self.tasks and not self.milestones:
            return "No tasks or milestones to display."
        
        start_date, end_date = self._get_date_range()
        date_range = (end_date - start_date).days + 1
        width_per_day = 1 if compact else self._get_char_width(date_range)
        name_width = 20
        
        lines = []
        
        # Title
        lines.append(f"{'═' * (name_width + date_range * width_per_day + 10)}")
        lines.append(f"{self.title.center(name_width + date_range * width_per_day + 10)}")
        lines.append(f"{'═' * (name_width + date_range * width_per_day + 10)}")
        lines.append("")
        
        # Date headers
        headers = self._render_date_header(start_date, end_date, width_per_day)
        lines.extend(headers)
        
        # Separator
        separator = "─" * name_width + "┼" + "─" * (date_range * width_per_day)
        lines.append(separator)
        
        # Current date marker
        if self.current_date:
            marker = self._render_current_date_marker(start_date, width_per_day)
            if marker:
                lines.append(marker)
        
        # Tasks
        for task in sorted(self.tasks, key=lambda t: t.start):
            lines.append(self._render_task(task, start_date, width_per_day))
        
        # Milestones
        if self.milestones:
            lines.append("")
            lines.append("─" * name_width + "┼" + "─" * (date_range * width_per_day))
            lines.append(f"{'Milestones'.ljust(name_width)}│")
            for milestone in sorted(self.milestones, key=lambda m: m.date):
                lines.append(self._render_milestone(milestone, start_date, width_per_day))
        
        # Legend
        lines.append("")
        lines.append("Legend:")
        lines.append(f"  {self.CHAR_PROGRESS} Completed  {self.CHAR_REMAINING} Remaining  {self.CHAR_EMPTY} Not started  {self.CHAR_MILESTONE} Milestone  {self.CHAR_CURRENT} Today")
        
        return "\n".join(lines)
    
    def render_table(self) -> str:
        """Render a simple table view of tasks."""
        if not self.tasks:
            return "No tasks to display."
        
        lines = []
        lines.append(f"{'Task':<30} {'Start':<12} {'End':<12} {'Days':<6} {'Progress':<10}")
        lines.append("─" * 70)
        
        for task in sorted(self.tasks, key=lambda t: t.start):
            progress_bar = "█" * int(task.progress * 10) + "░" * (10 - int(task.progress * 10))
            lines.append(
                f"{task.name[:28]:<30} "
                f"{task.start.strftime('%Y-%m-%d'):<12} "
                f"{task.end.strftime('%Y-%m-%d'):<12} "
                f"{task.duration_days:<6} "
                f"{progress_bar} {int(task.progress * 100)}%"
            )
        
        return "\n".join(lines)
    
    def render_timeline(self) -> str:
        """Render a simple timeline view."""
        if not self.tasks:
            return "No tasks to display."
        
        lines = ["Timeline View", "─" * 40]
        
        # Group tasks by start date
        date_groups: Dict[str, List[Task]] = {}
        for task in self.tasks:
            date_key = task.start.strftime("%Y-%m-%d")
            if date_key not in date_groups:
                date_groups[date_key] = []
            date_groups[date_key].append(task)
        
        # Sort dates
        for date_key in sorted(date_groups.keys()):
            lines.append(f"\n📅 {date_key}")
            for task in date_groups[date_key]:
                status = "✓" if task.is_complete else "○"
                duration = f"({task.duration_days}d)"
                lines.append(f"  {status} {task.name} {duration}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export chart data as dictionary."""
        return {
            "title": self.title,
            "tasks": [
                {
                    "name": t.name,
                    "start": t.start.isoformat(),
                    "end": t.end.isoformat(),
                    "progress": t.progress,
                    "duration_days": t.duration_days
                }
                for t in self.tasks
            ],
            "milestones": [
                {
                    "name": m.name,
                    "date": m.date.isoformat()
                }
                for m in self.milestones
            ]
        }
    
    def calculate_critical_path(self) -> List[str]:
        """
        Calculate the critical path (simplified version).
        Returns tasks that are on the critical path.
        
        Note: This is a simplified implementation that identifies
        tasks with dependencies.
        """
        # Build dependency graph
        task_map = {t.name: t for t in self.tasks}
        critical_tasks = []
        
        # Find tasks that have dependents
        dependents: Dict[str, List[str]] = {t.name: [] for t in self.tasks}
        for task in self.tasks:
            for dep in task.dependencies:
                if dep in dependents:
                    dependents[dep].append(task.name)
        
        # Tasks with no slack are on critical path
        # Simplified: tasks that have dependents are critical
        for task in self.tasks:
            if dependents[task.name]:
                critical_tasks.append(task.name)
        
        return critical_tasks
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the project."""
        if not self.tasks:
            return {
                "total_tasks": 0,
                "total_days": 0,
                "completed_tasks": 0,
                "overall_progress": 0.0
            }
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks if t.is_complete)
        total_days = sum(t.duration_days for t in self.tasks)
        
        # Calculate overall progress (weighted by duration)
        if total_days > 0:
            weighted_progress = sum(t.duration_days * t.progress for t in self.tasks)
            overall_progress = weighted_progress / total_days
        else:
            overall_progress = 0.0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_days": total_days,
            "overall_progress": round(overall_progress, 2),
            "completion_rate": round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0
        }


def create_sample_chart() -> GanttChart:
    """Create a sample Gantt chart for demonstration."""
    chart = GanttChart("Sample Project")
    
    # Add tasks
    chart.add_task(
        "Requirements",
        datetime(2024, 1, 1),
        datetime(2024, 1, 5),
        progress=1.0
    )
    chart.add_task(
        "Design",
        datetime(2024, 1, 3),
        datetime(2024, 1, 10),
        progress=0.8
    )
    chart.add_task(
        "Development",
        datetime(2024, 1, 8),
        datetime(2024, 1, 20),
        progress=0.5
    )
    chart.add_task(
        "Testing",
        datetime(2024, 1, 18),
        datetime(2024, 1, 25),
        progress=0.2
    )
    chart.add_task(
        "Deployment",
        datetime(2024, 1, 24),
        datetime(2024, 1, 28),
        progress=0.0
    )
    
    # Add milestones
    chart.add_milestone("Design Complete", datetime(2024, 1, 10))
    chart.add_milestone("Beta Release", datetime(2024, 1, 20))
    chart.add_milestone("Launch", datetime(2024, 1, 28))
    
    return chart


if __name__ == "__main__":
    # Demo
    chart = create_sample_chart()
    chart.set_current_date(datetime(2024, 1, 12))
    print(chart.render())
    print("\n")
    print(chart.render_table())
    print("\n")
    print(chart.render_timeline())
    print("\n")
    print("Statistics:", chart.get_statistics())