#!/usr/bin/env python3
"""
Example usage of Gantt Chart Utilities.

This script demonstrates various ways to use the GanttChart class
for project management visualization.
"""

from datetime import datetime, timedelta
from mod import GanttChart, create_sample_chart


def example_basic():
    """Basic example with simple tasks."""
    print("=" * 60)
    print("Example 1: Basic Gantt Chart")
    print("=" * 60)
    
    chart = GanttChart("Website Redesign")
    
    # Add tasks with different progress levels
    chart.add_task("Research", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
    chart.add_task("Wireframes", datetime(2024, 1, 3), datetime(2024, 1, 8), progress=1.0)
    chart.add_task("Design", datetime(2024, 1, 6), datetime(2024, 1, 15), progress=0.7)
    chart.add_task("Development", datetime(2024, 1, 10), datetime(2024, 1, 25), progress=0.3)
    chart.add_task("Testing", datetime(2024, 1, 20), datetime(2024, 1, 28), progress=0.0)
    chart.add_task("Launch", datetime(2024, 1, 28), datetime(2024, 1, 30), progress=0.0)
    
    # Set current date marker
    chart.set_current_date(datetime(2024, 1, 12))
    
    # Add milestone
    chart.add_milestone("Design Approval", datetime(2024, 1, 15))
    chart.add_milestone("Go Live", datetime(2024, 1, 30))
    
    print(chart.render())
    print()


def example_table_view():
    """Example showing table view."""
    print("=" * 60)
    print("Example 2: Table View")
    print("=" * 60)
    
    chart = GanttChart("Mobile App Development")
    
    chart.add_task("Planning", datetime(2024, 2, 1), datetime(2024, 2, 7), progress=1.0)
    chart.add_task("UI Design", datetime(2024, 2, 5), datetime(2024, 2, 14), progress=0.9)
    chart.add_task("Backend Dev", datetime(2024, 2, 8), datetime(2024, 2, 25), progress=0.6)
    chart.add_task("iOS App", datetime(2024, 2, 15), datetime(2024, 3, 5), progress=0.3)
    chart.add_task("Android App", datetime(2024, 2, 15), datetime(2024, 3, 5), progress=0.2)
    chart.add_task("QA Testing", datetime(2024, 3, 1), datetime(2024, 3, 10), progress=0.0)
    chart.add_task("App Store Review", datetime(2024, 3, 8), datetime(2024, 3, 15), progress=0.0)
    
    print(chart.render_table())
    print()


def example_timeline_view():
    """Example showing timeline view."""
    print("=" * 60)
    print("Example 3: Timeline View")
    print("=" * 60)
    
    chart = GanttChart("Marketing Campaign")
    
    chart.add_task("Market Research", datetime(2024, 3, 1), datetime(2024, 3, 5), progress=1.0)
    chart.add_task("Content Creation", datetime(2024, 3, 3), datetime(2024, 3, 10), progress=0.8)
    chart.add_task("Social Media", datetime(2024, 3, 6), datetime(2024, 3, 20), progress=0.4)
    chart.add_task("Email Campaign", datetime(2024, 3, 10), datetime(2024, 3, 15), progress=0.0)
    chart.add_task("Analytics Review", datetime(2024, 3, 18), datetime(2024, 3, 22), progress=0.0)
    
    print(chart.render_timeline())
    print()


def example_compact_mode():
    """Example showing compact mode for longer projects."""
    print("=" * 60)
    print("Example 4: Compact Mode (Long Project)")
    print("=" * 60)
    
    chart = GanttChart("Year-long Project")
    
    # Q1
    chart.add_task("Phase 1: Planning", datetime(2024, 1, 1), datetime(2024, 1, 31), progress=1.0)
    chart.add_task("Phase 2: Design", datetime(2024, 2, 1), datetime(2024, 3, 31), progress=0.9)
    
    # Q2
    chart.add_task("Phase 3: Dev Sprint 1", datetime(2024, 4, 1), datetime(2024, 4, 30), progress=0.7)
    chart.add_task("Phase 4: Dev Sprint 2", datetime(2024, 5, 1), datetime(2024, 5, 31), progress=0.4)
    chart.add_task("Phase 5: Dev Sprint 3", datetime(2024, 6, 1), datetime(2024, 6, 30), progress=0.1)
    
    # Q3
    chart.add_task("Phase 6: Testing", datetime(2024, 7, 1), datetime(2024, 8, 31), progress=0.0)
    chart.add_task("Phase 7: Bug Fixes", datetime(2024, 9, 1), datetime(2024, 9, 30), progress=0.0)
    
    # Q4
    chart.add_task("Phase 8: Staging", datetime(2024, 10, 1), datetime(2024, 10, 31), progress=0.0)
    chart.add_task("Phase 9: Launch Prep", datetime(2024, 11, 1), datetime(2024, 11, 30), progress=0.0)
    chart.add_task("Phase 10: Launch", datetime(2024, 12, 1), datetime(2024, 12, 15), progress=0.0)
    
    # Set current date
    chart.set_current_date(datetime(2024, 5, 15))
    
    # Add milestones
    chart.add_milestone("Q1 Review", datetime(2024, 3, 31))
    chart.add_milestone("Beta Release", datetime(2024, 6, 30))
    chart.add_milestone("Final Release", datetime(2024, 12, 15))
    
    print(chart.render(compact=True))
    print()


def example_statistics():
    """Example showing project statistics."""
    print("=" * 60)
    print("Example 5: Project Statistics")
    print("=" * 60)
    
    chart = create_sample_chart()
    stats = chart.get_statistics()
    
    print(f"Project: {chart.title}")
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Completed Tasks: {stats['completed_tasks']}")
    print(f"Total Days: {stats['total_days']}")
    print(f"Overall Progress: {stats['overall_progress'] * 100:.1f}%")
    print(f"Completion Rate: {stats['completion_rate']}%")
    print()


def example_export_data():
    """Example showing data export."""
    print("=" * 60)
    print("Example 6: Export to Dictionary (JSON-ready)")
    print("=" * 60)
    
    chart = GanttChart("API Development")
    chart.add_task("API Design", datetime(2024, 4, 1), datetime(2024, 4, 5), progress=1.0)
    chart.add_task("Implementation", datetime(2024, 4, 6), datetime(2024, 4, 20), progress=0.5)
    chart.add_milestone("API v1.0", datetime(2024, 4, 20))
    
    import json
    data = chart.to_dict()
    print(json.dumps(data, indent=2))
    print()


def example_sprint_planning():
    """Example showing sprint planning use case."""
    print("=" * 60)
    print("Example 7: Sprint Planning (2 Week Sprint)")
    print("=" * 60)
    
    sprint = GanttChart("Sprint 23 - User Authentication")
    
    # Week 1
    sprint.add_task("US-101: Login Page", datetime(2024, 5, 6), datetime(2024, 5, 7), progress=1.0)
    sprint.add_task("US-102: Register Form", datetime(2024, 5, 7), datetime(2024, 5, 9), progress=0.8)
    sprint.add_task("US-103: Password Reset", datetime(2024, 5, 8), datetime(2024, 5, 10), progress=0.5)
    sprint.add_task("US-104: OAuth Integration", datetime(2024, 5, 9), datetime(2024, 5, 13), progress=0.2)
    
    # Week 2
    sprint.add_task("US-105: Session Management", datetime(2024, 5, 13), datetime(2024, 5, 15), progress=0.0)
    sprint.add_task("US-106: Unit Tests", datetime(2024, 5, 14), datetime(2024, 5, 16), progress=0.0)
    sprint.add_task("US-107: Code Review", datetime(2024, 5, 16), datetime(2024, 5, 17), progress=0.0)
    
    # Milestones
    sprint.add_milestone("Sprint Midpoint", datetime(2024, 5, 10))
    sprint.add_milestone("Sprint End", datetime(2024, 5, 17))
    
    # Current day
    sprint.set_current_date(datetime(2024, 5, 9))
    
    print(sprint.render())
    
    stats = sprint.get_statistics()
    print(f"\nSprint Progress: {stats['overall_progress'] * 100:.1f}%")
    print(f"Tasks Completed: {stats['completed_tasks']}/{stats['total_tasks']}")
    print()


def example_parallel_tasks():
    """Example showing parallel task execution."""
    print("=" * 60)
    print("Example 8: Parallel Tasks (Team-Based)")
    print("=" * 60)
    
    project = GanttChart("E-commerce Platform")
    
    # Frontend team
    project.add_task("FE: Homepage", datetime(2024, 6, 1), datetime(2024, 6, 5), progress=1.0)
    project.add_task("FE: Product List", datetime(2024, 6, 3), datetime(2024, 6, 8), progress=0.7)
    project.add_task("FE: Cart", datetime(2024, 6, 6), datetime(2024, 6, 12), progress=0.3)
    project.add_task("FE: Checkout", datetime(2024, 6, 10), datetime(2024, 6, 15), progress=0.0)
    
    # Backend team (parallel)
    project.add_task("BE: Product API", datetime(2024, 6, 1), datetime(2024, 6, 7), progress=0.9)
    project.add_task("BE: Cart API", datetime(2024, 6, 5), datetime(2024, 6, 10), progress=0.5)
    project.add_task("BE: Order API", datetime(2024, 6, 8), datetime(2024, 6, 14), progress=0.0)
    project.add_task("BE: Payment Integration", datetime(2024, 6, 12), datetime(2024, 6, 18), progress=0.0)
    
    # DevOps team (parallel)
    project.add_task("DO: CI/CD Setup", datetime(2024, 6, 1), datetime(2024, 6, 3), progress=1.0)
    project.add_task("DO: Staging Env", datetime(2024, 6, 4), datetime(2024, 6, 6), progress=1.0)
    project.add_task("DO: Prod Env", datetime(2024, 6, 15), datetime(2024, 6, 17), progress=0.0)
    
    project.set_current_date(datetime(2024, 6, 8))
    
    print(project.render())
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("GANTT CHART UTILITIES - EXAMPLES")
    print("=" * 60 + "\n")
    
    example_basic()
    example_table_view()
    example_timeline_view()
    example_compact_mode()
    example_statistics()
    example_export_data()
    example_sprint_planning()
    example_parallel_tasks()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()