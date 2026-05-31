# Eisenhower Matrix Utilities

Priority task management using the Eisenhower Method.

## Overview

Two-dimensional priority matrix with four quadrants:
- **Q1 (Do First)**: Urgent + Important
- **Q2 (Schedule)**: Important, Not Urgent
- **Q3 (Delegate)**: Urgent, Not Important
- **Q4 (Eliminate)**: Not Urgent, Not Important

## Installation

```bash
pip install alltoolkit
```

## Usage

```python
from alltoolkit import EisenhowerMatrix

m = EisenhowerMatrix()
m.add_task("Fix critical bug", urgent=True, important=True)
m.add_task("Plan architecture redesign", urgent=False, important=True)
m.add_task("Reply to routine emails", urgent=True, important=False)
m.add_task("Browse social media", urgent=False, important=False)

# Classify tasks
print(m.classify())
# {'Q1': ['Fix critical bug'], 'Q2': ['Plan architecture redesign'],
#  'Q3': ['Reply routine emails'], 'Q4': ['Browse social media']}

# Get statistics
print(m.stats())
# {'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1, 'total': 4, 'efficiency': 0.5}

# Priority order
print(m.tasks_by_priority())
# ['Fix critical bug', 'Plan architecture redesign', 'Reply routine emails', 'Browse social media']
```

## API Reference

### EisenhowerMatrix

Main class for managing priority tasks.

#### Methods

- `add_task(name, urgent, important)` - Register a task
- `remove_task(name)` - Remove a task by name
- `reclassify(name, urgent, important)` - Update task priority
- `classify()` - Group tasks into quadrants
- `stats()` - Get per-quadrant counts and efficiency
- `tasks_by_priority()` - Tasks ordered by Q1→Q4
- `clear()` - Remove all tasks

### Factory Functions

```python
from alltoolkit import from_dicts, from_tuples

# From list of dicts
tasks = [
    {"name": "Task 1", "urgent": True, "important": True},
    {"name": "Task 2", "urgent": False, "important": True},
]
m = from_dicts(tasks)

# From tuples
tasks = [
    ("Task 1", True, True),
    ("Task 2", False, True),
]
m = from_tuples(tasks)
```

## Algorithm

The Eisenhower Matrix classifies tasks based on two dimensions:

1. **Urgency** - Time-sensitive tasks
2. **Importance** - Tasks with significant impact

The efficiency ratio is calculated as: `(Q1 + Q2) / total`

A well-prioritized task list should have high efficiency (>0.5), meaning most tasks are important (either urgent or not).
