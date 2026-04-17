#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Job Scheduler Utilities Examples

演示任务调度器的各种使用场景。
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from job_scheduler_utils.mod import (
    Job, JobStatus, JobPriority, ScheduleType,
    JobScheduler, JobBuilder,
    schedule, schedule_interval, scheduled, periodic,
)


def example_basic_scheduling():
    """基本任务调度示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基本任务调度")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    # 定义任务
    def send_email(to: str, subject: str):
        print(f"[{datetime.now()}] 发送邮件给 {to}: {subject}")
        return f"邮件已发送到 {to}"
    
    # 调度一次性任务
    job_id = scheduler.schedule_once(
        func=send_email,
        name="send_welcome_email",
        args=("user@example.com", "欢迎加入!"),
        delay_seconds=1,
    )
    
    print(f"任务已调度, ID: {job_id}")
    
    # 启动调度器
    scheduler.start()
    time.sleep(2)
    scheduler.stop()
    
    # 检查结果
    job = scheduler.get_job(job_id)
    print(f"任务状态: {job.status.value}")
    print(f"执行结果: {job.result.value if job.result else 'N/A'}")


def example_periodic_tasks():
    """周期性任务示例"""
    print("\n" + "=" * 60)
    print("示例 2: 周期性任务")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    # 心跳任务
    def heartbeat():
        print(f"[{datetime.now()}] 心跳检测...")
    
    # 每 2 秒执行一次
    job_id = scheduler.schedule_interval(
        func=heartbeat,
        interval_seconds=2,
        name="heartbeat",
    )
    
    print("启动心跳任务 (每 2 秒)...")
    scheduler.start()
    time.sleep(7)
    scheduler.stop()
    
    print("心跳任务已停止")


def example_priority_tasks():
    """任务优先级示例"""
    print("\n" + "=" * 60)
    print("示例 3: 任务优先级")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    execution_order = []
    
    def low_priority():
        execution_order.append("low")
        print("执行低优先级任务")
    
    def normal_priority():
        execution_order.append("normal")
        print("执行普通优先级任务")
    
    def high_priority():
        execution_order.append("high")
        print("执行高优先级任务")
    
    def critical():
        execution_order.append("critical")
        print("执行紧急任务")
    
    # 同时调度多个任务
    scheduler.schedule_once(func=low_priority, delay_seconds=0, 
                           priority=JobPriority.LOW)
    scheduler.schedule_once(func=normal_priority, delay_seconds=0,
                           priority=JobPriority.NORMAL)
    scheduler.schedule_once(func=high_priority, delay_seconds=0,
                           priority=JobPriority.HIGH)
    scheduler.schedule_once(func=critical, delay_seconds=0,
                           priority=JobPriority.CRITICAL)
    
    scheduler.start()
    time.sleep(0.5)
    scheduler.stop()
    
    print(f"\n执行顺序: {execution_order}")
    print("注意: 高优先级任务优先执行")


def example_retry_mechanism():
    """任务重试机制示例"""
    print("\n" + "=" * 60)
    print("示例 4: 任务重试机制")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    attempts = [0]
    
    def unreliable_task():
        attempts[0] += 1
        print(f"尝试 #{attempts[0]}...")
        
        if attempts[0] < 3:
            raise ConnectionError("连接失败")
        
        print("任务成功!")
        return "success"
    
    job_id = scheduler.schedule_once(
        func=unreliable_task,
        delay_seconds=0,
        max_retries=5,
        retry_delay=0.5,
    )
    
    scheduler.start()
    time.sleep(2)
    scheduler.stop()
    
    job = scheduler.get_job(job_id)
    print(f"\n最终状态: {job.status.value}")
    print(f"尝试次数: {job.result.attempts if job.result else 0}")


def example_job_dependencies():
    """任务依赖示例"""
    print("\n" + "=" * 60)
    print("示例 5: 任务依赖")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    def fetch_data():
        print("1. 获取数据...")
        time.sleep(0.3)
        return {"users": ["Alice", "Bob"]}
    
    def process_data():
        print("2. 处理数据...")
        time.sleep(0.3)
        return "处理完成"
    
    def save_results():
        print("3. 保存结果...")
        time.sleep(0.3)
        return "保存完成"
    
    # 调度有依赖关系的任务
    fetch_id = scheduler.schedule_once(
        func=fetch_data,
        name="fetch_data",
        delay_seconds=0,
    )
    
    process_id = scheduler.schedule_once(
        func=process_data,
        name="process_data",
        delay_seconds=0,
        dependencies=[fetch_id],
    )
    
    save_id = scheduler.schedule_once(
        func=save_results,
        name="save_results",
        delay_seconds=0,
        dependencies=[process_id],
    )
    
    scheduler.start()
    time.sleep(1.5)
    scheduler.stop()
    
    print("\n所有任务按依赖顺序执行完成!")


def example_job_cancellation():
    """任务取消示例"""
    print("\n" + "=" * 60)
    print("示例 6: 任务取消")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    def long_task():
        print("开始长时间任务...")
        time.sleep(10)
        print("任务完成!")
    
    job_id = scheduler.schedule_once(
        func=long_task,
        delay_seconds=2,
        name="long_task",
    )
    
    print(f"任务已调度: {job_id}")
    print("任务将在 2 秒后执行...")
    
    scheduler.start()
    time.sleep(0.5)
    
    # 取消任务
    print("取消任务...")
    if scheduler.cancel_job(job_id):
        print("任务已取消!")
    
    job = scheduler.get_job(job_id)
    print(f"任务状态: {job.status.value}")
    
    scheduler.stop()


def example_job_builder():
    """Job Builder 流式 API 示例"""
    print("\n" + "=" * 60)
    print("示例 7: Job Builder 流式 API")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    def report_task(report_type: str, format: str):
        print(f"生成 {report_type} 报告 ({format})...")
        return f"{report_type}_report.{format}"
    
    # 使用 Builder 模式创建任务
    job_id = (JobBuilder(report_task)
        .with_name("daily_report")
        .with_args("销售", format="pdf")
        .with_delay(1)
        .with_priority(JobPriority.HIGH)
        .with_retry(3, 0.5)
        .with_tags("report", "daily", "important")
        .with_metadata(department="sales", created_by="admin")
        .schedule(scheduler))
    
    print(f"任务已通过 Builder 创建: {job_id}")
    
    job = scheduler.get_job(job_id)
    print(f"任务名称: {job.name}")
    print(f"任务标签: {job.tags}")
    print(f"任务元数据: {job.metadata}")
    
    scheduler.start()
    time.sleep(2)
    scheduler.stop()


def example_persistence():
    """持久化示例"""
    print("\n" + "=" * 60)
    print("示例 7: 任务持久化")
    print("=" * 60)
    
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # 创建调度器并添加任务
        scheduler = JobScheduler(
            persistence_path=temp_path,
            auto_persist=True,
        )
        
        def important_task():
            print("执行重要任务...")
        
        job_id = scheduler.schedule_once(
            func=important_task,
            name="important_task",
            delay_seconds=3600,  # 1 小时后执行
            tags=["important"],
        )
        
        print(f"任务已创建: {job_id}")
        
        # 手动持久化
        scheduler.persist()
        print(f"状态已保存到: {temp_path}")
        
        # 加载到新调度器
        scheduler2 = JobScheduler(persistence_path=temp_path)
        job = scheduler2.get_job(job_id)
        
        if job:
            print(f"从文件加载任务: {job.name}")
            print(f"任务状态: {job.status.value}")
            print(f"任务标签: {job.tags}")
        
    finally:
        os.unlink(temp_path)


def example_daily_scheduling():
    """每日定时任务示例"""
    print("\n" + "=" * 60)
    print("示例 8: 每日定时任务")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    def daily_backup():
        print(f"[{datetime.now()}] 执行每日备份...")
    
    # 每天在指定时间执行
    # 注意: 这里演示用法，实际运行需要等待到指定时间
    job_id = scheduler.schedule_daily(
        func=daily_backup,
        hour=2,    # 凌晨 2 点
        minute=0,
        name="daily_backup",
    )
    
    job = scheduler.get_job(job_id)
    print(f"每日备份任务已调度")
    print(f"下次执行时间: {datetime.fromtimestamp(job.scheduled_time)}")
    
    scheduler.stop()


def example_context_manager():
    """上下文管理器示例"""
    print("\n" + "=" * 60)
    print("示例 9: 上下文管理器")
    print("=" * 60)
    
    def quick_task(n: int):
        print(f"执行任务 {n}...")
    
    # 使用 with 语句自动管理调度器生命周期
    with JobScheduler() as scheduler:
        for i in range(3):
            scheduler.schedule_once(func=quick_task, args=(i+1,), delay_seconds=0)
        
        time.sleep(0.5)
    
    print("调度器已自动停止")


def example_statistics():
    """统计信息示例"""
    print("\n" + "=" * 60)
    print("示例 10: 调度器统计")
    print("=" * 60)
    
    scheduler = JobScheduler()
    
    def task():
        pass
    
    def failing_task():
        raise ValueError("失败")
    
    # 添加多个任务
    scheduler.schedule_once(func=task, delay_seconds=0)
    scheduler.schedule_once(func=task, delay_seconds=0)
    scheduler.schedule_once(func=task, delay_seconds=0)
    scheduler.schedule_once(func=failing_task, delay_seconds=0, max_retries=0)
    
    to_cancel = scheduler.schedule_once(func=task, delay_seconds=100)
    scheduler.cancel_job(to_cancel)
    
    scheduler.start()
    time.sleep(0.5)
    scheduler.stop()
    
    stats = scheduler.get_stats()
    print(f"总调度任务数: {stats['total_scheduled']}")
    print(f"已完成: {stats['total_completed']}")
    print(f"失败: {stats['total_failed']}")
    print(f"已取消: {stats['total_cancelled']}")
    print(f"当前等待中: {stats['pending_count']}")
    print(f"当前运行中: {stats['running_count']}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 70)
    print("  AllToolkit Job Scheduler - 使用示例")
    print("=" * 70)
    
    examples = [
        example_basic_scheduling,
        example_periodic_tasks,
        example_priority_tasks,
        example_retry_mechanism,
        example_job_dependencies,
        example_job_cancellation,
        example_job_builder,
        example_persistence,
        example_daily_scheduling,
        example_context_manager,
        example_statistics,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"示例 {example.__name__} 出错: {e}")
    
    print("\n" + "=" * 70)
    print("  所有示例执行完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()