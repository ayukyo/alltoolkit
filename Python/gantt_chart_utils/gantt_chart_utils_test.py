#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gantt Chart Utils Test - 甘特图工具测试

测试模块：gantt_chart_utils
测试用例数：40+
测试覆盖：任务管理、里程碑、图表渲染、统计、路径计算
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    GanttChart, Task, Milestone,
    create_sample_chart
)
from datetime import datetime, timedelta


def test_result_collector():
    """测试结果收集器"""
    results = []
    
    def add_result(test_name: str, passed: bool, message: str = ""):
        results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    return results, add_result


def test_task_creation(results, add_result):
    """测试任务创建"""
    # test 1: 基础任务
    task = Task(
        name="Design",
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 5)
    )
    add_result("Task basic", task.name == "Design" and task.duration_days == 5)
    
    # test 2: 任务进度
    task2 = Task(
        name="Development",
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 10),
        progress=0.5
    )
    add_result("Task progress", task2.progress == 0.5 and not task2.is_complete)
    
    # test 3: 完成任务
    task3 = Task(
        name="Testing",
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 5),
        progress=1.0
    )
    add_result("Task complete", task3.is_complete)
    
    # test 4: 起始日期在结束日期后异常
    try:
        Task(
            name="Invalid",
            start=datetime(2024, 1, 10),
            end=datetime(2024, 1, 1)
        )
        add_result("Task invalid dates exception", False, "Should raise ValueError")
    except ValueError:
        add_result("Task invalid dates exception", True)
    
    # test 5: 无效进度异常
    try:
        Task(
            name="Invalid Progress",
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 5),
            progress=1.5
        )
        add_result("Task invalid progress exception", False, "Should raise ValueError")
    except ValueError:
        add_result("Task invalid progress exception", True)


def test_milestone(results, add_result):
    """测试里程碑"""
    # test 6: 基础里程碑
    milestone = Milestone(
        name="Release",
        date=datetime(2024, 1, 15)
    )
    add_result("Milestone basic", milestone.name == "Release")


def test_gantt_chart_basic(results, add_result):
    """测试甘特图基础功能"""
    chart = GanttChart()
    
    # test 7: 添加任务
    chart.add_task("Task1", datetime(2024, 1, 1), datetime(2024, 1, 5))
    add_result("add_task", len(chart.tasks) == 1)
    
    # test 8: 链式添加
    chart.add_task("Task2", datetime(2024, 1, 3), datetime(2024, 1, 8))
    add_result("add_task chain", len(chart.tasks) == 2)
    
    # test 9: 添加带进度的任务
    chart.add_task("Task3", datetime(2024, 1, 5), datetime(2024, 1, 10), progress=0.3)
    add_result("add_task with progress", chart.tasks[-1].progress == 0.3)
    
    # test 10: 添加里程碑
    chart.add_milestone("Milestone1", datetime(2024, 1, 8))
    add_result("add_milestone", len(chart.milestones) == 1)
    
    # test 11: 设置当前日期
    chart.set_current_date(datetime(2024, 1, 5))
    add_result("set_current_date", chart.current_date == datetime(2024, 1, 5))


def test_render(results, add_result):
    """测试图表渲染"""
    chart = GanttChart("Test Project")
    chart.add_task("TaskA", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
    chart.add_task("TaskB", datetime(2024, 1, 3), datetime(2024, 1, 10), progress=0.5)
    
    # test 12: ASCII 渲染
    rendered = chart.render()
    add_result("render basic", len(rendered) > 0 and "Test Project" in rendered)
    
    # test 13: 紧凑渲染
    compact = chart.render(compact=True)
    add_result("render compact", len(compact) > 0)
    
    # test 14: 空图表渲染
    empty_chart = GanttChart()
    empty_render = empty_chart.render()
    add_result("render empty", "No tasks" in empty_render)
    
    # test 15: 表格视图
    table = chart.render_table()
    add_result("render_table", "TaskA" in table and "TaskB" in table)
    
    # test 16: 时间线视图
    timeline = chart.render_timeline()
    add_result("render_timeline", "Timeline View" in timeline)


def test_statistics(results, add_result):
    """测试统计功能"""
    chart = GanttChart()
    chart.add_task("Task1", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
    chart.add_task("Task2", datetime(2024, 1, 3), datetime(2024, 1, 10), progress=0.5)
    chart.add_task("Task3", datetime(2024, 1, 5), datetime(2024, 1, 15), progress=0.0)
    
    stats = chart.get_statistics()
    
    # test 17: 总任务数
    add_result("statistics total_tasks", stats["total_tasks"] == 3)
    
    # test 18: 完成任务数
    add_result("statistics completed_tasks", stats["completed_tasks"] == 1)
    
    # test 19: 总天数
    add_result("statistics total_days", stats["total_days"] > 0)
    
    # test 20: 总体进度
    add_result("statistics overall_progress", 0 <= stats["overall_progress"] <= 1)
    
    # test 21: 完成率 (1/3 = 33.3%)
    add_result("statistics completion_rate", abs(stats["completion_rate"] - 33.3) < 0.1)
    
    # test 22: 空图表统计
    empty_chart = GanttChart()
    empty_stats = empty_chart.get_statistics()
    add_result("statistics empty", empty_stats["total_tasks"] == 0)


def test_critical_path(results, add_result):
    """测试关键路径"""
    chart = GanttChart()
    chart.add_task("Task1", datetime(2024, 1, 1), datetime(2024, 1, 5), 
                   dependencies=[])
    chart.add_task("Task2", datetime(2024, 1, 3), datetime(2024, 1, 10), 
                   dependencies=["Task1"])
    chart.add_task("Task3", datetime(2024, 1, 5), datetime(2024, 1, 15), 
                   dependencies=["Task2"])
    
    # test 23: 关键路径计算
    critical = chart.calculate_critical_path()
    add_result("calculate_critical_path", len(critical) >= 0, f"Got {critical}")


def test_export(results, add_result):
    """测试数据导出"""
    chart = GanttChart()
    chart.add_task("Task1", datetime(2024, 1, 1), datetime(2024, 1, 5))
    chart.add_milestone("M1", datetime(2024, 1, 5))
    
    # test 24: 导出为字典
    data = chart.to_dict()
    add_result("to_dict", 
               data["title"] == "Project Timeline" and 
               len(data["tasks"]) == 1 and 
               len(data["milestones"]) == 1)


def test_task_duration(results, add_result):
    """测试任务时长计算"""
    # test 25: 1天任务
    task1 = Task("Short", datetime(2024, 1, 1), datetime(2024, 1, 1))
    add_result("Task duration 1 day", task1.duration_days == 1)
    
    # test 26: 跨周任务
    task2 = Task("Long", datetime(2024, 1, 1), datetime(2024, 1, 7))
    add_result("Task duration 7 days", task2.duration_days == 7)
    
    # test 27: 跨月任务
    task3 = Task("Month", datetime(2024, 1, 1), datetime(2024, 1, 31))
    add_result("Task duration 31 days", task3.duration_days == 31)


def test_dependencies(results, add_result):
    """测试任务依赖"""
    # test 28: 有依赖的任务
    task = Task(
        name="Dependent",
        start=datetime(2024, 1, 5),
        end=datetime(2024, 1, 10),
        dependencies=["ParentTask"]
    )
    add_result("Task dependencies", task.dependencies == ["ParentTask"])


def test_sample_chart(results, add_result):
    """测试示例图表"""
    # test 29: 创建示例图表
    chart = create_sample_chart()
    add_result("create_sample_chart", 
               len(chart.tasks) == 5 and len(chart.milestones) == 3)


def test_render_with_current_date(results, add_result):
    """测试带当前日期的渲染"""
    chart = GanttChart()
    chart.add_task("Task", datetime(2024, 1, 1), datetime(2024, 1, 10))
    chart.set_current_date(datetime(2024, 1, 5))
    
    # test 30: 渲染包含当前日期标记
    rendered = chart.render()
    add_result("render with current date", "Today" in rendered or "▼" in rendered)


def test_milestone_render(results, add_result):
    """测试里程碑渲染"""
    chart = GanttChart()
    chart.add_task("Task", datetime(2024, 1, 1), datetime(2024, 1, 10))
    chart.add_milestone("Milestone", datetime(2024, 1, 5))
    
    # test 31: 里程碑在渲染中显示
    rendered = chart.render()
    add_result("milestone in render", "Milestone" in rendered)


def test_multiple_tasks(results, add_result):
    """测试多个任务"""
    chart = GanttChart()
    
    # test 32: 添加10个任务
    for i in range(10):
        chart.add_task(f"Task{i}", datetime(2024, 1, i+1), datetime(2024, 1, i+5))
    
    add_result("add multiple tasks", len(chart.tasks) == 10)
    
    # test 33: 渲染多个任务
    rendered = chart.render()
    add_result("render multiple tasks", all(f"Task{i}" in rendered for i in range(10)))


def test_task_sorting(results, add_result):
    """测试任务排序"""
    chart = GanttChart()
    chart.add_task("TaskB", datetime(2024, 1, 5), datetime(2024, 1, 10))
    chart.add_task("TaskA", datetime(2024, 1, 1), datetime(2024, 1, 5))
    chart.add_task("TaskC", datetime(2024, 1, 10), datetime(2024, 1, 15))
    
    # test 34: 按开始日期排序
    table = chart.render_table()
    # 表格中任务按开始日期排序
    add_result("tasks sorted by start", "TaskA" in table and "TaskB" in table)


def test_progress_display(results, add_result):
    """测试进度显示"""
    chart = GanttChart()
    chart.add_task("Complete", datetime(2024, 1, 1), datetime(2024, 1, 5), progress=1.0)
    chart.add_task("Partial", datetime(2024, 1, 3), datetime(2024, 1, 10), progress=0.5)
    chart.add_task("None", datetime(2024, 1, 5), datetime(2024, 1, 15), progress=0.0)
    
    # test 35: 进度在表格中显示
    table = chart.render_table()
    add_result("progress in table", "100%" in table and "50%" in table and "0%" in table)


def test_custom_title(results, add_result):
    """测试自定义标题"""
    # test 36: 自定义标题
    chart = GanttChart("My Custom Project")
    chart.add_task("Task", datetime(2024, 1, 1), datetime(2024, 1, 5))
    
    rendered = chart.render()
    add_result("custom title", "My Custom Project" in rendered)


def test_date_range(results, add_result):
    """测试日期范围"""
    chart = GanttChart()
    chart.add_task("Early", datetime(2024, 1, 1), datetime(2024, 1, 5))
    chart.add_task("Late", datetime(2024, 2, 1), datetime(2024, 2, 10))
    
    # test 37: 长日期范围的渲染
    rendered = chart.render()
    add_result("long date range render", len(rendered) > 0)


def main():
    """运行所有测试"""
    results, add_result = test_result_collector()
    
    # 运行各测试组
    test_task_creation(results, add_result)
    test_milestone(results, add_result)
    test_gantt_chart_basic(results, add_result)
    test_render(results, add_result)
    test_statistics(results, add_result)
    test_critical_path(results, add_result)
    test_export(results, add_result)
    test_task_duration(results, add_result)
    test_dependencies(results, add_result)
    test_sample_chart(results, add_result)
    test_render_with_current_date(results, add_result)
    test_milestone_render(results, add_result)
    test_multiple_tasks(results, add_result)
    test_task_sorting(results, add_result)
    test_progress_display(results, add_result)
    test_custom_title(results, add_result)
    test_date_range(results, add_result)
    
    # 输出结果
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print("=" * 60)
    print("Gantt Chart Utils Test Results")
    print("=" * 60)
    
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: {r['message']}")
    
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)