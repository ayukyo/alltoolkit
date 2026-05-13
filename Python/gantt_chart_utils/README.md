# Gantt Chart Utilities

Zero-dependency ASCII Gantt chart generator for Python. Perfect for CLI tools,
terminal-based project management, and visualizing project timelines in text format.

## Features

- 📊 **ASCII Gantt Charts** - Beautiful terminal-friendly visualization
- 📋 **Multiple Views** - Chart, table, and timeline views
- 📈 **Progress Tracking** - Visual progress bars for each task
- 🎯 **Milestones** - Mark important project milestones
- 📅 **Date Handling** - Automatic date range calculation
- 📤 **Data Export** - Export to JSON-ready dictionary
- 📊 **Statistics** - Project progress statistics
- 🚀 **Zero Dependencies** - Pure Python stdlib

## Installation

Simply copy `mod.py` to your project. No external dependencies required!

## Quick Start

```python
from datetime import datetime
from mod import GanttChart

# Create a chart
chart = GanttChart("My Project")

# Add tasks with progress (0.0 to 1.0)
chart.add_task("Design", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.8)
chart.add_task("Development", datetime(2024, 1, 3), datetime(2024, 1, 10), progress=0.3)
chart.add_task("Testing", datetime(2024, 1, 8), datetime(2024, 1, 12), progress=0.0)

# Add a milestone
chart.add_milestone("Beta Release", datetime(2024, 1, 10))

# Set current date marker
chart.set_current_date(datetime(2024, 1, 5))

# Render the chart
print(chart.render())
```

## Output Example

```
══════════════════════════════════════════════════════════════
                         My Project                         
══════════════════════════════════════════════════════════════

                    │     Jan 2024        
                    │01020304050607080910111213
                    │MTWTFMTWTFMTWTFMTWTFM
────────────────────┼─────────────────────────────
Today               │             ▼              
Design              │████████▒▒░░░░░░░░░░░░ 80%
Development         │░░░░██████████▒▒▒▒▒▒▒▒ 30%
Testing             │░░░░░░░░░░░░░████████████ 0%

────────────────────┼─────────────────────────────
Milestones          │
Beta Release        │         ◆                  

Legend:
  █ Completed  ▒ Remaining  ░ Not started  ◆ Milestone  ▼ Today
```

## Views

### Chart View (Default)

```python
print(chart.render())
```

### Table View

```python
print(chart.render_table())
```

Output:
```
Task                           Start        End          Days   Progress    
──────────────────────────────────────────────────────────────────────
Design                         2024-01-01   2024-01-05   5      ████████░░ 80%
Development                    2024-01-03   2024-01-10   8      ███░░░░░░░ 30%
Testing                        2024-01-08   2024-01-12   5      ░░░░░░░░░░ 0%
```

### Timeline View

```python
print(chart.render_timeline())
```

Output:
```
Timeline View
────────────────────────────────────────

📅 2024-01-01
  ○ Design (5d)
  ○ Development (8d)

📅 2024-01-08
  ○ Testing (5d)
```

## API Reference

### GanttChart

Main class for creating Gantt charts.

#### Constructor

```python
GanttChart(title: str = "Project Timeline")
```

#### Methods

| Method | Description |
|--------|-------------|
| `add_task(name, start, end, progress=0.0)` | Add a task |
| `add_milestone(name, date)` | Add a milestone |
| `set_current_date(date)` | Set today's marker |
| `render()` | Render ASCII chart |
| `render_table()` | Render table view |
| `render_timeline()` | Render timeline view |
| `to_dict()` | Export to dictionary |
| `get_statistics()` | Get project statistics |
| `calculate_critical_path()` | Get critical path tasks |

### Task

Data class representing a task.

```python
Task(
    name: str,
    start: datetime,
    end: datetime,
    progress: float = 0.0,  # 0.0 to 1.0
    dependencies: List[str] = []
)
```

### Milestone

Data class representing a milestone.

```python
Milestone(
    name: str,
    date: datetime
)
```

## Statistics

```python
stats = chart.get_statistics()
print(stats)
# {
#   'total_tasks': 5,
#   'completed_tasks': 2,
#   'total_days': 25,
#   'overall_progress': 0.42,
#   'completion_rate': 40.0
# }
```

## Data Export

```python
import json

data = chart.to_dict()
json_string = json.dumps(data, indent=2)
```

## Compact Mode

For longer projects, use compact mode:

```python
print(chart.render(compact=True))
```

This uses fewer characters per day, suitable for month-long or year-long projects.

## Testing

Run the test suite:

```bash
python test.py
```

## Examples

See `example.py` for comprehensive usage examples:

- Basic Gantt chart
- Table view
- Timeline view
- Compact mode for long projects
- Statistics display
- Data export
- Sprint planning
- Parallel team tasks

```bash
python example.py
```

## License

MIT License - Free to use in any project.

## Contributing

Contributions welcome! Feel free to:
- Add new rendering styles
- Improve date handling
- Add color support
- Add dependency visualization