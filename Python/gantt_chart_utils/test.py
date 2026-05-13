"""
Unit tests for Gantt Chart Utilities.
"""

import unittest
from datetime import datetime, timedelta
from mod import GanttChart, Task, Milestone, create_sample_chart


class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task("Test Task", datetime(2024, 1, 1), datetime(2024, 1, 5))
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.progress, 0.0)
        self.assertEqual(task.duration_days, 5)
    
    def test_task_duration(self):
        """Test task duration calculation."""
        task = Task("Task", datetime(2024, 1, 1), datetime(2024, 1, 10))
        self.assertEqual(task.duration_days, 10)
    
    def test_task_progress(self):
        """Test task progress."""
        task = Task("Task", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.5)
        self.assertEqual(task.progress, 0.5)
        self.assertFalse(task.is_complete)
    
    def test_task_completion(self):
        """Test task completion check."""
        task = Task("Task", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
        self.assertTrue(task.is_complete)
    
    def test_invalid_dates(self):
        """Test that invalid dates raise error."""
        with self.assertRaises(ValueError):
            Task("Invalid", datetime(2024, 1, 10), datetime(2024, 1, 1))
    
    def test_invalid_progress(self):
        """Test that invalid progress raises error."""
        with self.assertRaises(ValueError):
            Task("Invalid", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.5)
        
        with self.assertRaises(ValueError):
            Task("Invalid", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=-0.1)


class TestMilestone(unittest.TestCase):
    """Test cases for Milestone class."""
    
    def test_milestone_creation(self):
        """Test basic milestone creation."""
        milestone = Milestone("Launch", datetime(2024, 1, 15))
        self.assertEqual(milestone.name, "Launch")
        self.assertEqual(milestone.date, datetime(2024, 1, 15))


class TestGanttChart(unittest.TestCase):
    """Test cases for GanttChart class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.chart = GanttChart("Test Project")
    
    def test_chart_creation(self):
        """Test chart creation."""
        self.assertEqual(self.chart.title, "Test Project")
        self.assertEqual(len(self.chart.tasks), 0)
        self.assertEqual(len(self.chart.milestones), 0)
    
    def test_add_task(self):
        """Test adding a task."""
        result = self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5))
        self.assertEqual(len(self.chart.tasks), 1)
        self.assertEqual(self.chart.tasks[0].name, "Task 1")
        self.assertEqual(result, self.chart)  # Test fluent interface
    
    def test_add_task_with_progress(self):
        """Test adding a task with progress."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.5)
        self.assertEqual(self.chart.tasks[0].progress, 0.5)
    
    def test_add_milestone(self):
        """Test adding a milestone."""
        result = self.chart.add_milestone("M1", datetime(2024, 1, 10))
        self.assertEqual(len(self.chart.milestones), 1)
        self.assertEqual(result, self.chart)  # Test fluent interface
    
    def test_set_current_date(self):
        """Test setting current date."""
        result = self.chart.set_current_date(datetime(2024, 1, 5))
        self.assertEqual(self.chart.current_date, datetime(2024, 1, 5))
        self.assertEqual(result, self.chart)  # Test fluent interface
    
    def test_render_empty_chart(self):
        """Test rendering empty chart."""
        result = self.chart.render()
        self.assertEqual(result, "No tasks or milestones to display.")
    
    def test_render_with_tasks(self):
        """Test rendering chart with tasks."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.5)
        result = self.chart.render()
        self.assertIn("Task 1", result)
        self.assertIn("Jan 2024", result)
    
    def test_render_table(self):
        """Test rendering table view."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.5)
        result = self.chart.render_table()
        self.assertIn("Task 1", result)
        self.assertIn("2024-01-01", result)
        self.assertIn("2024-01-05", result)
    
    def test_render_timeline(self):
        """Test rendering timeline view."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.5)
        result = self.chart.render_timeline()
        self.assertIn("Task 1", result)
        self.assertIn("2024-01-01", result)
    
    def test_to_dict(self):
        """Test exporting to dictionary."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.5)
        self.chart.add_milestone("M1", datetime(2024, 1, 10))
        
        result = self.chart.to_dict()
        
        self.assertEqual(result["title"], "Test Project")
        self.assertEqual(len(result["tasks"]), 1)
        self.assertEqual(len(result["milestones"]), 1)
        self.assertEqual(result["tasks"][0]["name"], "Task 1")
        self.assertEqual(result["tasks"][0]["progress"], 0.5)
    
    def test_get_statistics_empty(self):
        """Test statistics for empty chart."""
        result = self.chart.get_statistics()
        self.assertEqual(result["total_tasks"], 0)
        self.assertEqual(result["overall_progress"], 0.0)
    
    def test_get_statistics_with_tasks(self):
        """Test statistics with tasks."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
        self.chart.add_task("Task 2", datetime(2024, 1, 6), datetime(2024, 1, 10), progress=0.0)
        
        result = self.chart.get_statistics()
        
        self.assertEqual(result["total_tasks"], 2)
        self.assertEqual(result["completed_tasks"], 1)
        self.assertEqual(result["total_days"], 10)  # 5 + 5
        self.assertEqual(result["completion_rate"], 50.0)
    
    def test_calculate_critical_path(self):
        """Test critical path calculation."""
        self.chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 5))
        self.chart.add_task("Task 2", datetime(2024, 1, 6), datetime(2024, 1, 10))
        
        result = self.chart.calculate_critical_path()
        self.assertIsInstance(result, list)
    
    def test_sample_chart(self):
        """Test sample chart creation."""
        chart = create_sample_chart()
        self.assertEqual(chart.title, "Sample Project")
        self.assertGreater(len(chart.tasks), 0)
        self.assertGreater(len(chart.milestones), 0)
    
    def test_date_range_calculation(self):
        """Test date range calculation."""
        self.chart.add_task("Task", datetime(2024, 1, 5), datetime(2024, 1, 10))
        start, end = self.chart._get_date_range()
        
        # Should include padding
        self.assertLessEqual(start, datetime(2024, 1, 5))
        self.assertGreaterEqual(end, datetime(2024, 1, 10))
    
    def test_truncate_name(self):
        """Test name truncation."""
        long_name = "This is a very long task name that should be truncated"
        result = self.chart._truncate_name(long_name, 20)
        self.assertLessEqual(len(result), 20)
        self.assertTrue(result.endswith("..."))


class TestChartRendering(unittest.TestCase):
    """Test chart rendering features."""
    
    def setUp(self):
        """Set up test chart."""
        self.chart = GanttChart("Test Project")
        self.chart.add_task("Short", datetime(2024, 1, 1), datetime(2024, 1, 2))
        self.chart.add_task("Long Task", datetime(2024, 1, 1), datetime(2024, 1, 10), progress=0.3)
    
    def test_compact_render(self):
        """Test compact rendering mode."""
        result = self.chart.render(compact=True)
        self.assertIn("Short", result)
        self.assertIn("Long Task", result)
    
    def test_render_with_current_date(self):
        """Test rendering with current date marker."""
        self.chart.set_current_date(datetime(2024, 1, 5))
        result = self.chart.render()
        self.assertIn("Today", result)
    
    def test_render_with_milestones(self):
        """Test rendering with milestones."""
        self.chart.add_milestone("Milestone 1", datetime(2024, 1, 5))
        result = self.chart.render()
        self.assertIn("Milestones", result)
        self.assertIn("Milestone 1", result)
    
    def test_render_includes_legend(self):
        """Test that render includes legend."""
        result = self.chart.render()
        self.assertIn("Legend:", result)
        self.assertIn("Completed", result)
        self.assertIn("Remaining", result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_single_day_task(self):
        """Test task that starts and ends on same day."""
        chart = GanttChart()
        chart.add_task("Single Day", datetime(2024, 1, 1), datetime(2024, 1, 1))
        result = chart.render()
        self.assertIn("Single Day", result)
    
    def test_zero_progress(self):
        """Test task with zero progress."""
        task = Task("Zero Progress", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=0.0)
        self.assertEqual(task.progress, 0.0)
        self.assertFalse(task.is_complete)
    
    def test_full_progress(self):
        """Test task with 100% progress."""
        task = Task("Full Progress", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
        self.assertEqual(task.progress, 1.0)
        self.assertTrue(task.is_complete)
    
    def test_overlapping_tasks(self):
        """Test overlapping tasks."""
        chart = GanttChart()
        chart.add_task("Task 1", datetime(2024, 1, 1), datetime(2024, 1, 10))
        chart.add_task("Task 2", datetime(2024, 1, 5), datetime(2024, 1, 15))
        result = chart.render()
        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
    
    def test_long_task_name(self):
        """Test handling of long task names."""
        chart = GanttChart()
        long_name = "This is an extremely long task name that exceeds the normal display limit"
        chart.add_task(long_name, datetime(2024, 1, 1), datetime(2024, 1, 5))
        result = chart.render()
        # Should not crash and should show truncated name
        self.assertIn("...", result)


if __name__ == "__main__":
    unittest.main()