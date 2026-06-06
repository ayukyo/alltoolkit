"""
Tests for eisenhower_matrix_utils
"""

import pytest
from eisenhower_matrix_utils import (
    EisenhowerMatrix,
    Quadrant,
    from_dicts,
    from_tuples,
)


class TestEisenhowerMatrix:
    # ------------------------------------------------------------------
    # add_task / classify
    # ------------------------------------------------------------------

    def test_q1_do_first(self):
        m = EisenhowerMatrix()
        m.add_task("Critical fix", urgent=True, important=True)
        c = m.classify()
        assert c == {
            "Q1": ["Critical fix"],
            "Q2": [],
            "Q3": [],
            "Q4": [],
        }

    def test_q2_schedule(self):
        m = EisenhowerMatrix()
        m.add_task("Architecture redesign", urgent=False, important=True)
        c = m.classify()
        assert c == {
            "Q1": [],
            "Q2": ["Architecture redesign"],
            "Q3": [],
            "Q4": [],
        }

    def test_q3_delegate(self):
        m = EisenhowerMatrix()
        m.add_task("Reply routine emails", urgent=True, important=False)
        c = m.classify()
        assert c == {
            "Q1": [],
            "Q2": [],
            "Q3": ["Reply routine emails"],
            "Q4": [],
        }

    def test_q4_eliminate(self):
        m = EisenhowerMatrix()
        m.add_task("Browse social media", urgent=False, important=False)
        c = m.classify()
        assert c == {
            "Q1": [],
            "Q2": [],
            "Q3": [],
            "Q4": ["Browse social media"],
        }

    def test_all_quadrants(self):
        m = EisenhowerMatrix()
        m.add_task("Q1 task", urgent=True, important=True)
        m.add_task("Q2 task", urgent=False, important=True)
        m.add_task("Q3 task", urgent=True, important=False)
        m.add_task("Q4 task", urgent=False, important=False)
        c = m.classify()
        assert c["Q1"] == ["Q1 task"]
        assert c["Q2"] == ["Q2 task"]
        assert c["Q3"] == ["Q3 task"]
        assert c["Q4"] == ["Q4 task"]

    # ------------------------------------------------------------------
    # remove_task
    # ------------------------------------------------------------------

    def test_remove_task_found(self):
        m = EisenhowerMatrix()
        m.add_task("Task A", urgent=True, important=True)
        m.add_task("Task B", urgent=False, important=True)
        assert m.remove_task("Task A") is True
        c = m.classify()
        assert c["Q1"] == []
        assert c["Q2"] == ["Task B"]

    def test_remove_task_not_found(self):
        m = EisenhowerMatrix()
        m.add_task("Task A", urgent=True, important=True)
        assert m.remove_task("Task B") is False

    def test_remove_task_first_match_only(self):
        m = EisenhowerMatrix()
        m.add_task("Task", urgent=True, important=True)
        m.add_task("Task", urgent=False, important=True)
        m.remove_task("Task")
        c = m.classify()
        assert c["Q1"] == []
        assert c["Q2"] == ["Task"]

    # ------------------------------------------------------------------
    # reclassify
    # ------------------------------------------------------------------

    def test_reclassify_found(self):
        m = EisenhowerMatrix()
        m.add_task("Task X", urgent=True, important=False)
        assert m.reclassify("Task X", urgent=True, important=True) is True
        assert m.classify()["Q1"] == ["Task X"]

    def test_reclassify_not_found(self):
        m = EisenhowerMatrix()
        assert m.reclassify("Ghost", urgent=True, important=True) is False

    # ------------------------------------------------------------------
    # stats
    # ------------------------------------------------------------------

    def test_stats_empty(self):
        m = EisenhowerMatrix()
        assert m.stats() == {
            "Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0, "total": 0, "efficiency": 0.0
        }

    def test_stats_all_q1(self):
        m = EisenhowerMatrix()
        m.add_task("A", urgent=True, important=True)
        m.add_task("B", urgent=True, important=True)
        s = m.stats()
        assert s["Q1"] == 2
        assert s["total"] == 2
        assert s["efficiency"] == 1.0

    def test_stats_mixed(self):
        m = EisenhowerMatrix()
        m.add_task("A", urgent=True, important=True)
        m.add_task("B", urgent=False, important=True)
        m.add_task("C", urgent=True, important=False)
        m.add_task("D", urgent=False, important=False)
        s = m.stats()
        assert s["Q1"] == 1
        assert s["Q2"] == 1
        assert s["Q3"] == 1
        assert s["Q4"] == 1
        assert s["total"] == 4
        assert s["efficiency"] == 0.5

    # ------------------------------------------------------------------
    # tasks_by_priority
    # ------------------------------------------------------------------

    def test_tasks_by_priority(self):
        m = EisenhowerMatrix()
        m.add_task("Z", urgent=False, important=False)
        m.add_task("A", urgent=True, important=True)
        m.add_task("M", urgent=False, important=True)
        m.add_task("R", urgent=True, important=False)
        assert m.tasks_by_priority() == ["A", "M", "R", "Z"]

    # ------------------------------------------------------------------
    # clear
    # ------------------------------------------------------------------

    def test_clear(self):
        m = EisenhowerMatrix()
        m.add_task("Task", urgent=True, important=True)
        m.clear()
        assert m.stats()["total"] == 0

    # ------------------------------------------------------------------
    # error handling
    # ------------------------------------------------------------------

    def test_add_task_empty_name_raises(self):
        m = EisenhowerMatrix()
        with pytest.raises(ValueError):
            m.add_task("", urgent=True, important=True)

    def test_add_task_strips_whitespace(self):
        m = EisenhowerMatrix()
        m.add_task("  Trim me  ", urgent=True, important=True)
        assert "Trim me" in m.classify()["Q1"]


class TestFactoryFunctions:
    def test_from_dicts(self):
        data = [
            {"name": "Q1", "urgent": True, "important": True},
            {"name": "Q2", "urgent": False, "important": True},
            {"name": "Q3", "urgent": True, "important": False},
            {"name": "Q4"},
        ]
        m = from_dicts(data)
        c = m.classify()
        assert c["Q1"] == ["Q1"]
        assert c["Q2"] == ["Q2"]
        assert c["Q3"] == ["Q3"]
        assert c["Q4"] == ["Q4"]

    def test_from_tuples(self):
        data = [("A", True, True), ("B", False, True)]
        m = from_tuples(data)
        assert m.classify()["Q1"] == ["A"]
        assert m.classify()["Q2"] == ["B"]


class TestQuadrantEnum:
    def test_values(self):
        assert Quadrant.Q1.value == "Q1"
        assert Quadrant.Q2.value == "Q2"
        assert Quadrant.Q3.value == "Q3"
        assert Quadrant.Q4.value == "Q4"

    def test_order(self):
        qs = list(Quadrant)
        assert [q.name for q in qs] == ["Q1", "Q2", "Q3", "Q4"]