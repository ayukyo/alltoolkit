"""
Eisenhower Matrix Priority Task Manager
https://en.wikipedia.org/wiki/Time_management#The_Eisenhower_Method

Two-dimensional priority matrix with four quadrants:
  - Urgent + Important  → Q1: Do First
  - Important, Not Urgent → Q2: Schedule
  - Urgent, Not Important → Q3: Delegate
  - Not Urgent, Not Important → Q4: Eliminate

Example
    >>> m = EisenhowerMatrix()
    >>> m.add_task("Fix critical bug", urgent=True, important=True)
    >>> m.add_task("Plan architecture redesign", urgent=False, important=True)
    >>> m.add_task("Reply to routine emails", urgent=True, important=False)
    >>> m.add_task("Browse social media", urgent=False, important=False)
    >>> m.classify()
    {'Q1': ['Fix critical bug'], 'Q2': ['Plan architecture redesign'],
     'Q3': ['Reply routine emails'], 'Q4': ['Browse social media']}
    >>> m.stats()
    {'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1, 'total': 4, 'efficiency': 0.5}
"""

__version__ = "1.0.0"

from enum import Enum


class Quadrant(Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class Task(object):
    """Lightweight task record."""
    __slots__ = ("name", "urgent", "important")

    def __init__(self, name, urgent, important):
        self.name = name
        self.urgent = urgent
        self.important = important

    def __repr__(self):
        return "Task(%r, urgent=%s, important=%s)" % (
            self.name, self.urgent, self.important,
        )


class EisenhowerMatrix(object):
    """
    Manages tasks classified by urgency and importance.

    Methods
    -------
    add_task(name, urgent, important)
        Register a task with urgency/importance flags.
    remove_task(name)
        Remove a task by exact name match.
    reclassify(name, urgent, important)
        Update urgency/importance of an existing task.
    classify() -> dict
        Group all tasks into quadrants.
    stats() -> dict
        Return per-quadrant counts and efficiency ratio.
    clear()
        Remove all tasks.
    """

    def __init__(self):
        self._tasks = []

    # -- mutators -----------------------------------------------------------

    def add_task(self, name, urgent, important):
        """Register a new task."""
        if not name:
            raise ValueError("task name must not be empty")
        self._tasks.append(Task(name=name.strip(), urgent=urgent, important=important))

    def remove_task(self, name):
        """Remove first exact-match task. Returns True if removed."""
        for i, t in enumerate(self._tasks):
            if t.name == name:
                del self._tasks[i]
                return True
        return False

    def reclassify(self, name, urgent, important):
        """Update urgency/importance of first matching task. Returns True if found."""
        for i, t in enumerate(self._tasks):
            if t.name == name:
                self._tasks[i] = Task(name=t.name, urgent=urgent, important=important)
                return True
        return False

    def clear(self):
        """Remove all tasks."""
        del self._tasks[:]

    # -- queries ------------------------------------------------------------

    def classify(self):
        """Return a dict mapping each quadrant key to its task names."""
        result = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
        for t in self._tasks:
            if t.urgent and t.important:
                result["Q1"].append(t.name)
            elif t.important:
                result["Q2"].append(t.name)
            elif t.urgent:
                result["Q3"].append(t.name)
            else:
                result["Q4"].append(t.name)
        return result

    def stats(self):
        """Return counts and efficiency ratio (Q1+Q2 tasks / total)."""
        q1 = q2 = q3 = q4 = 0
        for t in self._tasks:
            if t.urgent and t.important:
                q1 += 1
            elif t.important:
                q2 += 1
            elif t.urgent:
                q3 += 1
            else:
                q4 += 1
        total = len(self._tasks)
        efficiency = round((q1 + q2) / float(total), 2) if total else 0.0
        return {
            "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4,
            "total": total, "efficiency": efficiency,
        }

    def tasks_by_priority(self):
        """
        Return all task names ordered by priority:
        Q1 → Q2 → Q3 → Q4.
        """
        c = self.classify()
        ordered = []
        for key in ("Q1", "Q2", "Q3", "Q4"):
            ordered.extend(c[key])
        return ordered


# ---------------------------------------------------------------------------
# Convenience factory functions
# ---------------------------------------------------------------------------

def from_dicts(tasks):
    """
    Build an EisenhowerMatrix from a list of dicts.

    Each dict must contain ``name`` and optionally ``urgent``/``important``.
    Defaults to not urgent, not important.
    """
    m = EisenhowerMatrix()
    for t in tasks:
        m.add_task(
            t["name"],
            urgent=bool(t.get("urgent", False)),
            important=bool(t.get("important", False)),
        )
    return m


def from_tuples(tasks):
    """
    Build an EisenhowerMatrix from (name, urgent, important) tuples.
    """
    m = EisenhowerMatrix()
    for name, urgent, important in tasks:
        m.add_task(name, urgent=urgent, important=important)
    return m