#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Job Scheduler Utilities Tests
"""

import sys
import os
import time
import tempfile
import threading
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mod import (
    Job, JobStatus, JobPriority, ScheduleType, JobResult,
    JobScheduler, JobBuilder,
    schedule, schedule_interval, scheduled, periodic, run_in_thread
)


def test_job_creation():
    """Test basic job creation."""
    job = Job(
        id="test_1",
        name="test_job",
        args=(1, 2),
        kwargs={"x": 3},
    )
    
    assert job.id == "test_1"
    assert job.name == "test_job"
    assert job.status == JobStatus.PENDING
    assert job.priority == JobPriority.NORMAL
    assert job.args == (1, 2)
    assert job.kwargs == {"x": 3}
    assert job.max_retries == 0
    print("✓ Job creation test passed")


def test_job_ready_check():
    """Test job readiness check."""
    now = time.time()
    
    # Job ready now
    job1 = Job(id="test_1", name="job1", scheduled_time=now - 1)
    assert job1.is_ready() is True
    
    # Job scheduled in future
    job2 = Job(id="test_2", name="job2", scheduled_time=now + 100)
    assert job2.is_ready() is False
    
    # Job already running
    job3 = Job(id="test_3", name="job3", status=JobStatus.RUNNING)
    assert job3.is_ready() is False
    
    print("✓ Job ready check test passed")


def test_job_serialization():
    """Test job to_dict and from_dict."""
    job = Job(
        id="test_1",
        name="test_job",
        args=(1, 2),
        kwargs={"x": 3},
        status=JobStatus.COMPLETED,
        priority=JobPriority.HIGH,
        scheduled_time=12345.0,
        interval=60.0,
        max_retries=3,
        retry_delay=2.0,
        tags=["important"],
        metadata={"key": "value"},
        result=JobResult(success=True, value=42, execution_time=1.5),
    )
    
    data = job.to_dict()
    assert data['id'] == "test_1"
    assert data['name'] == "test_job"
    assert data['status'] == "completed"
    assert data['priority'] == 75
    assert data['scheduled_time'] == 12345.0
    assert data['interval'] == 60.0
    assert data['tags'] == ["important"]
    assert data['result']['success'] is True
    assert data['result']['value'] == 42
    
    # Reconstruct
    job2 = Job.from_dict(data)
    assert job2.id == job.id
    assert job2.name == job.name
    assert job2.status == job.status
    assert job2.priority == job.priority
    assert job2.scheduled_time == job.scheduled_time
    assert job2.interval == job.interval
    
    print("✓ Job serialization test passed")


def test_scheduler_basic():
    """Test basic scheduler functionality."""
    scheduler = JobScheduler()
    
    # Schedule a simple job
    results = []
    
    def simple_task():
        results.append("executed")
        return 42
    
    job_id = scheduler.schedule_once(
        func=simple_task,
        name="simple_task",
        delay_seconds=0,
    )
    
    assert job_id.startswith("job_")
    assert scheduler.get_job(job_id) is not None
    
    # Start scheduler and wait
    scheduler.start()
    time.sleep(0.5)
    scheduler.stop()
    
    assert "executed" in results
    job = scheduler.get_job(job_id)
    assert job.status == JobStatus.COMPLETED
    assert job.result.success is True
    assert job.result.value == 42
    
    print("✓ Basic scheduler test passed")


def test_scheduler_delayed():
    """Test delayed job execution."""
    scheduler = JobScheduler()
    
    execution_time = []
    
    def delayed_task():
        execution_time.append(time.time())
        return "done"
    
    start = time.time()
    job_id = scheduler.schedule_delayed(
        func=delayed_task,
        delay_seconds=0.3,
    )
    
    scheduler.start()
    time.sleep(0.6)
    scheduler.stop()
    
    assert len(execution_time) == 1
    delay = execution_time[0] - start
    assert delay >= 0.25  # Allow some tolerance
    
    print("✓ Delayed job test passed")


def test_scheduler_interval():
    """Test periodic job execution."""
    scheduler = JobScheduler()
    
    counter = [0]
    
    def periodic_task():
        counter[0] += 1
        return counter[0]
    
    job_id = scheduler.schedule_interval(
        func=periodic_task,
        interval_seconds=0.3,
        delay_seconds=0,
    )
    
    scheduler.start()
    time.sleep(1.2)
    scheduler.stop()
    
    # Should have run at least 2 times
    assert counter[0] >= 2
    
    print(f"✓ Interval job test passed (ran {counter[0]} times)")


def test_scheduler_priority():
    """Test job priority ordering."""
    scheduler = JobScheduler()
    
    execution_order = []
    
    def low_task():
        execution_order.append("low")
    
    def high_task():
        execution_order.append("high")
    
    def normal_task():
        execution_order.append("normal")
    
    # Schedule with different priorities
    scheduler.schedule_once(func=low_task, priority=JobPriority.LOW, delay_seconds=0)
    scheduler.schedule_once(func=high_task, priority=JobPriority.HIGH, delay_seconds=0)
    scheduler.schedule_once(func=normal_task, priority=JobPriority.NORMAL, delay_seconds=0)
    
    scheduler.start()
    time.sleep(0.3)
    scheduler.stop()
    
    # High should run first
    assert execution_order[0] == "high"
    
    print("✓ Priority test passed")


def test_scheduler_retry():
    """Test job retry functionality."""
    scheduler = JobScheduler()
    
    attempts = [0]
    
    def failing_task():
        attempts[0] += 1
        if attempts[0] < 3:
            raise ValueError("Simulated failure")
        return "success"
    
    job_id = scheduler.schedule_once(
        func=failing_task,
        delay_seconds=0,
        max_retries=3,
        retry_delay=0.3,
    )
    
    scheduler.start()
    time.sleep(3.0)  # Enough time for 3 attempts with retry delay
    scheduler.stop()
    
    job = scheduler.get_job(job_id)
    assert job.status == JobStatus.COMPLETED
    assert job.result.success is True
    assert attempts[0] == 3
    
    print("✓ Retry test passed")


def test_scheduler_retry_exhausted():
    """Test job retry exhaustion."""
    scheduler = JobScheduler()
    
    attempts = [0]
    
    def always_failing():
        attempts[0] += 1
        raise ValueError("Always fails")
    
    job_id = scheduler.schedule_once(
        func=always_failing,
        delay_seconds=0,
        max_retries=2,
        retry_delay=0.3,
    )
    
    scheduler.start()
    time.sleep(2.0)  # Enough time for 3 attempts
    scheduler.stop()
    
    job = scheduler.get_job(job_id)
    assert job.status == JobStatus.FAILED
    assert job.result.success is False
    assert "Always fails" in job.result.error
    
    print("✓ Retry exhaustion test passed")


def test_scheduler_cancellation():
    """Test job cancellation."""
    scheduler = JobScheduler()
    
    executed = [False]
    
    def slow_task():
        time.sleep(1)
        executed[0] = True
    
    # Schedule with delay so we can cancel before it runs
    job_id = scheduler.schedule_once(
        func=slow_task,
        delay_seconds=5.0,  # Large delay so we can definitely cancel
    )
    
    # Cancel without starting scheduler (pending job)
    assert scheduler.cancel_job(job_id) is True
    
    job = scheduler.get_job(job_id)
    assert job.status == JobStatus.CANCELLED
    
    # Can't cancel again
    assert scheduler.cancel_job(job_id) is False
    
    # Start scheduler to ensure cancelled job doesn't execute
    scheduler.start()
    time.sleep(0.5)
    scheduler.stop()
    
    assert executed[0] is False
    
    print("✓ Cancellation test passed")


def test_scheduler_dependencies():
    """Test job dependencies."""
    scheduler = JobScheduler()
    
    execution_order = []
    
    def first_task():
        execution_order.append("first")
        return "first_result"
    
    def second_task():
        execution_order.append("second")
        return "second_result"
    
    # First job
    first_id = scheduler.schedule_once(
        func=first_task,
        delay_seconds=0,
    )
    
    # Second job depends on first
    second_id = scheduler.schedule_once(
        func=second_task,
        delay_seconds=0,
        dependencies=[first_id],
    )
    
    scheduler.start()
    time.sleep(0.3)
    scheduler.stop()
    
    # First should run before second
    assert execution_order == ["first", "second"]
    
    print("✓ Dependencies test passed")


def test_scheduler_context_manager():
    """Test scheduler as context manager."""
    results = []
    
    def task():
        results.append("executed")
    
    with JobScheduler() as scheduler:
        scheduler.schedule_once(func=task, delay_seconds=0)
        time.sleep(0.3)
    
    assert "executed" in results
    
    print("✓ Context manager test passed")


def test_scheduler_stats():
    """Test scheduler statistics."""
    scheduler = JobScheduler()
    
    def task():
        pass
    
    def failing():
        raise ValueError("fail")
    
    job1 = scheduler.schedule_once(func=task, delay_seconds=0)
    job2 = scheduler.schedule_once(func=failing, delay_seconds=0, max_retries=0)
    job3 = scheduler.schedule_once(func=task, delay_seconds=100)
    scheduler.cancel_job(job3)
    
    scheduler.start()
    time.sleep(0.3)
    scheduler.stop()
    
    stats = scheduler.get_stats()
    assert stats['total_scheduled'] >= 3
    assert stats['total_completed'] >= 1
    assert stats['total_failed'] >= 1
    assert stats['total_cancelled'] >= 1
    
    print("✓ Stats test passed")


def test_scheduler_persistence():
    """Test scheduler persistence."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Create and save
        scheduler1 = JobScheduler(persistence_path=temp_path)
        
        def task():
            return 42
        
        job_id = scheduler1.schedule_once(
            func=task,
            name="test_job",
            delay_seconds=100,  # Far future so it doesn't run
            tags=["test"],
        )
        
        scheduler1.persist()
        
        # Load in new scheduler
        scheduler2 = JobScheduler(persistence_path=temp_path)
        
        # Job should be loaded (without function)
        job = scheduler2.get_job(job_id)
        assert job is not None
        assert job.name == "test_job"
        assert job.status == JobStatus.PENDING
        assert "test" in job.tags
        
    finally:
        os.unlink(temp_path)
    
    print("✓ Persistence test passed")


def test_job_builder():
    """Test fluent job builder."""
    scheduler = JobScheduler()
    
    results = []
    
    def task(x, y):
        results.append(x + y)
        return x + y
    
    job_id = (JobBuilder(task)
        .with_name("builder_job")
        .with_args(1, 2)
        .with_delay(0)
        .with_priority(JobPriority.HIGH)
        .with_retry(2, 0.1)
        .with_tags("test", "builder")
        .with_metadata(key="value")
        .schedule(scheduler))
    
    scheduler.start()
    time.sleep(0.3)
    scheduler.stop()
    
    assert results[0] == 3
    
    job = scheduler.get_job(job_id)
    assert job.name == "builder_job"
    assert "test" in job.tags
    assert "builder" in job.tags
    
    print("✓ Job builder test passed")


def test_get_jobs_methods():
    """Test various get_jobs methods."""
    scheduler = JobScheduler()
    
    def task():
        pass
    
    job1 = scheduler.schedule_once(func=task, delay_seconds=0, tags=["tag1"])
    job2 = scheduler.schedule_once(func=task, delay_seconds=100, tags=["tag1", "tag2"])
    job3 = scheduler.schedule_once(func=task, delay_seconds=100, tags=["tag2"])
    
    scheduler.start()
    time.sleep(0.3)
    scheduler.stop()
    
    # Get by status
    completed = scheduler.get_completed_jobs()
    pending = scheduler.get_pending_jobs()
    
    assert len(completed) >= 1
    assert len(pending) >= 2
    
    # Get by tag
    tag1_jobs = scheduler.get_jobs_by_tag("tag1")
    tag2_jobs = scheduler.get_jobs_by_tag("tag2")
    
    assert len(tag1_jobs) >= 2
    assert len(tag2_jobs) >= 2
    
    print("✓ Get jobs methods test passed")


def test_scheduler_clear():
    """Test scheduler clear functionality."""
    scheduler = JobScheduler()
    
    def task():
        time.sleep(0.5)
    
    scheduler.schedule_once(func=task, delay_seconds=0)
    scheduler.schedule_once(func=task, delay_seconds=100)
    scheduler.schedule_once(func=task, delay_seconds=100)
    
    scheduler.start()
    time.sleep(0.1)  # Let one job start
    
    cleared = scheduler.clear(include_running=False)
    
    assert cleared >= 2
    
    # Running job should still be there
    assert len(scheduler.get_running_jobs()) >= 1
    
    scheduler.stop()
    
    print("✓ Clear test passed")


def test_async_function():
    """Test async function support."""
    scheduler = JobScheduler()
    
    results = []
    
    async def async_task():
        await asyncio.sleep(0.1)
        results.append("async_done")
        return 42
    
    import asyncio
    
    job_id = scheduler.schedule_once(func=async_task, delay_seconds=0)
    
    scheduler.start()
    time.sleep(0.5)
    scheduler.stop()
    
    assert "async_done" in results
    
    job = scheduler.get_job(job_id)
    assert job.status == JobStatus.COMPLETED
    assert job.result.value == 42
    
    print("✓ Async function test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Job Scheduler Utilities Tests")
    print("=" * 60)
    
    tests = [
        test_job_creation,
        test_job_ready_check,
        test_job_serialization,
        test_scheduler_basic,
        test_scheduler_delayed,
        test_scheduler_interval,
        test_scheduler_priority,
        test_scheduler_retry,
        test_scheduler_retry_exhausted,
        test_scheduler_cancellation,
        test_scheduler_dependencies,
        test_scheduler_context_manager,
        test_scheduler_stats,
        test_scheduler_persistence,
        test_job_builder,
        test_get_jobs_methods,
        test_scheduler_clear,
        test_async_function,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)