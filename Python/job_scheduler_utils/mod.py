"""
AllToolkit - Python Job Scheduler Utilities

A zero-dependency, production-ready job scheduling module.
Supports delayed jobs, periodic jobs, job prioritization, dependencies,
cancellation, retry, and simple persistence.

Author: AllToolkit
License: MIT
"""

import time
import threading
import json
import hashlib
from typing import (
    Callable, Optional, Dict, List, Any, Set, Tuple,
    TypeVar, Generic, Union, Coroutine
)
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps
from collections import deque
import asyncio
from concurrent.futures import ThreadPoolExecutor, Future
import logging
from pathlib import Path
import inspect

logger = logging.getLogger(__name__)

T = TypeVar('T')


class JobStatus(Enum):
    """Job status enumeration."""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRY = "retry"


class JobPriority(Enum):
    """Job priority levels."""
    LOW = 10
    NORMAL = 50
    HIGH = 75
    CRITICAL = 100


class ScheduleType(Enum):
    """Schedule type enumeration."""
    ONCE = "once"          # Run once at specified time
    INTERVAL = "interval"  # Run at fixed intervals
    CRON = "cron"          # Cron-style scheduling (simplified)
    DELAY = "delay"        # Run after a delay


@dataclass
class JobResult:
    """Result of a job execution."""
    success: bool
    value: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    attempts: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'value': self.value,
            'error': self.error,
            'execution_time': self.execution_time,
            'attempts': self.attempts,
        }


@dataclass
class Job:
    """
    Represents a scheduled job.
    
    Attributes:
        id: Unique job identifier
        name: Human-readable job name
        func: The function to execute (can be sync or async)
        args: Positional arguments for the function
        kwargs: Keyword arguments for the function
        status: Current job status
        priority: Job priority level
        schedule_type: Type of scheduling
        scheduled_time: When the job should run (timestamp)
        interval: Interval in seconds for periodic jobs
        max_retries: Maximum retry attempts on failure
        retry_delay: Delay between retries in seconds
        retry_count: Current retry count
        dependencies: List of job IDs that must complete first
        timeout: Maximum execution time in seconds
        created_at: Job creation timestamp
        started_at: Job start timestamp
        completed_at: Job completion timestamp
        result: Job execution result
        tags: User-defined tags for filtering
        metadata: Additional user metadata
    """
    id: str
    name: str
    func: Optional[Callable] = None
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    priority: JobPriority = JobPriority.NORMAL
    schedule_type: ScheduleType = ScheduleType.ONCE
    scheduled_time: Optional[float] = None
    interval: Optional[float] = None
    max_retries: int = 0
    retry_delay: float = 1.0
    retry_count: int = 0
    dependencies: List[str] = field(default_factory=list)
    timeout: Optional[float] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[JobResult] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def __lt__(self, other: 'Job') -> bool:
        """Compare jobs for priority queue ordering."""
        # Higher priority first, then earlier scheduled time
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        return (self.scheduled_time or 0) < (other.scheduled_time or 0)
    
    def __post_init__(self):
        if self.args is None:
            self.args = ()
        if self.kwargs is None:
            self.kwargs = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
    
    def is_ready(self, now: Optional[float] = None) -> bool:
        """Check if the job is ready to run."""
        now = now or time.time()
        if self.status not in (JobStatus.PENDING, JobStatus.RETRY):
            return False
        if self.scheduled_time and now < self.scheduled_time:
            return False
        return True
    
    def is_periodic(self) -> bool:
        """Check if this is a periodic job."""
        return self.schedule_type == ScheduleType.INTERVAL
    
    def to_dict(self, include_func: bool = False) -> Dict[str, Any]:
        """Convert job to dictionary for serialization."""
        data = {
            'id': self.id,
            'name': self.name,
            'status': self.status.value,
            'priority': self.priority.value,
            'schedule_type': self.schedule_type.value,
            'scheduled_time': self.scheduled_time,
            'interval': self.interval,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'retry_count': self.retry_count,
            'dependencies': self.dependencies,
            'timeout': self.timeout,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'args': self.args,
            'kwargs': self.kwargs,
            'tags': self.tags,
            'metadata': self.metadata,
        }
        if self.result:
            data['result'] = self.result.to_dict()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Job':
        """Create a Job from dictionary (without function)."""
        return cls(
            id=data['id'],
            name=data['name'],
            func=None,  # Function needs to be registered separately
            args=tuple(data.get('args', ())),
            kwargs=data.get('kwargs', {}),
            status=JobStatus(data['status']),
            priority=JobPriority(data['priority']),
            schedule_type=ScheduleType(data['schedule_type']),
            scheduled_time=data.get('scheduled_time'),
            interval=data.get('interval'),
            max_retries=data.get('max_retries', 0),
            retry_delay=data.get('retry_delay', 1.0),
            retry_count=data.get('retry_count', 0),
            dependencies=data.get('dependencies', []),
            timeout=data.get('timeout'),
            created_at=data.get('created_at', time.time()),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at'),
            result=JobResult(**data['result']) if data.get('result') else None,
            tags=data.get('tags', []),
            metadata=data.get('metadata', {}),
        )


class JobScheduler:
    """
    A thread-safe job scheduler supporting delayed, periodic, and dependent jobs.
    
    Features:
        - Schedule jobs to run at specific times
        - Schedule recurring jobs with intervals
        - Job prioritization
        - Job dependencies (run after other jobs complete)
        - Automatic retry on failure
        - Job cancellation
        - Simple JSON persistence
        - Thread-safe operations
        - Support for both sync and async functions
    
    Example:
        >>> scheduler = JobScheduler()
        >>> 
        >>> # Schedule a one-time job
        >>> job_id = scheduler.schedule_once(
        ...     func=my_task,
        ...     name="my_job",
        ...     delay_seconds=60
        ... )
        >>> 
        >>> # Schedule a periodic job
        >>> job_id = scheduler.schedule_interval(
        ...     func=cleanup_task,
        ...     name="cleanup",
        ...     interval_seconds=3600
        ... )
        >>> 
        >>> # Start the scheduler
        >>> scheduler.start()
    """
    
    def __init__(
        self,
        max_workers: int = 4,
        persistence_path: Optional[str] = None,
        auto_persist: bool = False,
        persist_interval: float = 30.0,
    ):
        """
        Initialize the job scheduler.
        
        Args:
            max_workers: Maximum number of worker threads
            persistence_path: Path for JSON persistence file
            auto_persist: Automatically persist changes
            persist_interval: Interval for auto-persistence in seconds
        """
        self._jobs: Dict[str, Job] = {}
        self._pending: List[Job] = []
        self._running: Set[str] = set()
        self._completed: Dict[str, Job] = {}
        self._func_registry: Dict[str, Callable] = {}
        
        self._lock = threading.RLock()
        self._condition = threading.Condition(self._lock)
        self._running_flag = False
        self._scheduler_thread: Optional[threading.Thread] = None
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        
        self._persistence_path = persistence_path
        self._auto_persist = auto_persist
        self._persist_interval = persist_interval
        self._last_persist = time.time()
        
        self._counter = 0
        self._stats = {
            'total_scheduled': 0,
            'total_completed': 0,
            'total_failed': 0,
            'total_cancelled': 0,
        }
        
        if persistence_path and Path(persistence_path).exists():
            self._load_from_file()
    
    def _generate_id(self) -> str:
        """Generate a unique job ID."""
        self._counter += 1
        timestamp = int(time.time() * 1000)
        random_suffix = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        return f"job_{timestamp}_{self._counter}_{random_suffix}"
    
    def register_function(self, name: str, func: Callable) -> None:
        """
        Register a function for later reference by name.
        Useful for persistence and deserialization.
        
        Args:
            name: Function name
            func: The function to register
        """
        self._func_registry[name] = func
    
    def unregister_function(self, name: str) -> bool:
        """Unregister a function by name."""
        return self._func_registry.pop(name, None) is not None
    
    def schedule_once(
        self,
        func: Callable,
        name: Optional[str] = None,
        args: Tuple = (),
        kwargs: Optional[Dict] = None,
        delay_seconds: Optional[float] = None,
        scheduled_time: Optional[float] = None,
        priority: JobPriority = JobPriority.NORMAL,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        dependencies: Optional[List[str]] = None,
        timeout: Optional[float] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> str:
        """
        Schedule a job to run once.
        
        Args:
            func: The function to execute
            name: Human-readable job name
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            delay_seconds: Delay before execution (in seconds)
            scheduled_time: Specific timestamp to run at
            priority: Job priority
            max_retries: Maximum retry attempts on failure
            retry_delay: Delay between retries in seconds
            dependencies: List of job IDs that must complete first
            timeout: Maximum execution time in seconds
            tags: User-defined tags
            metadata: Additional user metadata
            
        Returns:
            Job ID
        """
        with self._lock:
            now = time.time()
            
            if scheduled_time is None:
                scheduled_time = now + (delay_seconds or 0)
            
            job = Job(
                id=self._generate_id(),
                name=name or func.__name__,
                func=func,
                args=args,
                kwargs=kwargs or {},
                status=JobStatus.PENDING,
                priority=priority,
                schedule_type=ScheduleType.ONCE,
                scheduled_time=scheduled_time,
                max_retries=max_retries,
                retry_delay=retry_delay,
                dependencies=dependencies or [],
                timeout=timeout,
                tags=tags or [],
                metadata=metadata or {},
            )
            
            self._jobs[job.id] = job
            self._pending.append(job)
            self._pending.sort()
            self._stats['total_scheduled'] += 1
            
            self._condition.notify_all()
            
            if self._auto_persist:
                self._maybe_persist()
            
            return job.id
    
    def schedule_interval(
        self,
        func: Callable,
        interval_seconds: float,
        name: Optional[str] = None,
        args: Tuple = (),
        kwargs: Optional[Dict] = None,
        delay_seconds: Optional[float] = None,
        scheduled_time: Optional[float] = None,
        priority: JobPriority = JobPriority.NORMAL,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> str:
        """
        Schedule a job to run periodically.
        
        Args:
            func: The function to execute
            interval_seconds: Interval between executions in seconds
            name: Human-readable job name
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            delay_seconds: Delay before first execution
            scheduled_time: Specific timestamp for first execution
            priority: Job priority
            max_retries: Maximum retry attempts on failure
            retry_delay: Delay between retries in seconds
            tags: User-defined tags
            metadata: Additional user metadata
            
        Returns:
            Job ID
        """
        with self._lock:
            now = time.time()
            
            if scheduled_time is None:
                scheduled_time = now + (delay_seconds or 0)
            
            job = Job(
                id=self._generate_id(),
                name=name or func.__name__,
                func=func,
                args=args,
                kwargs=kwargs or {},
                status=JobStatus.PENDING,
                priority=priority,
                schedule_type=ScheduleType.INTERVAL,
                scheduled_time=scheduled_time,
                interval=interval_seconds,
                max_retries=max_retries,
                retry_delay=retry_delay,
                tags=tags or [],
                metadata=metadata or {},
            )
            
            self._jobs[job.id] = job
            self._pending.append(job)
            self._pending.sort()
            self._stats['total_scheduled'] += 1
            
            self._condition.notify_all()
            
            if self._auto_persist:
                self._maybe_persist()
            
            return job.id
    
    def schedule_delayed(
        self,
        func: Callable,
        delay_seconds: float,
        **kwargs
    ) -> str:
        """
        Schedule a job to run after a delay.
        Convenience method for schedule_once.
        
        Args:
            func: The function to execute
            delay_seconds: Delay before execution
            **kwargs: Additional arguments for schedule_once
            
        Returns:
            Job ID
        """
        return self.schedule_once(func, delay_seconds=delay_seconds, **kwargs)
    
    def schedule_daily(
        self,
        func: Callable,
        hour: int = 0,
        minute: int = 0,
        **kwargs
    ) -> str:
        """
        Schedule a job to run daily at a specific time.
        
        Args:
            func: The function to execute
            hour: Hour (0-23)
            minute: Minute (0-59)
            **kwargs: Additional arguments for schedule_interval
            
        Returns:
            Job ID
        """
        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if target <= now:
            target += timedelta(days=1)
        
        scheduled_time = target.timestamp()
        interval = 24 * 60 * 60  # 24 hours
        
        return self.schedule_interval(
            func,
            interval_seconds=interval,
            scheduled_time=scheduled_time,
            **kwargs
        )
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a scheduled job.
        
        Args:
            job_id: The job ID to cancel
            
        Returns:
            True if cancelled, False if not found or already running/completed/cancelled
        """
        with self._lock:
            if job_id not in self._jobs:
                return False
            
            job = self._jobs[job_id]
            
            # Can't cancel jobs that are running, completed, failed, or already cancelled
            if job.status in (JobStatus.RUNNING, JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED):
                return False
            
            job.status = JobStatus.CANCELLED
            self._pending = [j for j in self._pending if j.id != job_id]
            self._stats['total_cancelled'] += 1
            
            if self._auto_persist:
                self._maybe_persist()
            
            return True
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID."""
        with self._lock:
            return self._jobs.get(job_id)
    
    def get_jobs_by_status(self, status: JobStatus) -> List[Job]:
        """Get all jobs with a specific status."""
        with self._lock:
            return [job for job in self._jobs.values() if job.status == status]
    
    def get_jobs_by_tag(self, tag: str) -> List[Job]:
        """Get all jobs with a specific tag."""
        with self._lock:
            return [job for job in self._jobs.values() if tag in job.tags]
    
    def get_pending_jobs(self) -> List[Job]:
        """Get all pending jobs."""
        return self.get_jobs_by_status(JobStatus.PENDING)
    
    def get_running_jobs(self) -> List[Job]:
        """Get all running jobs."""
        return self.get_jobs_by_status(JobStatus.RUNNING)
    
    def get_completed_jobs(self) -> List[Job]:
        """Get all completed jobs."""
        return self.get_jobs_by_status(JobStatus.COMPLETED)
    
    def get_failed_jobs(self) -> List[Job]:
        """Get all failed jobs."""
        return self.get_jobs_by_status(JobStatus.FAILED)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        with self._lock:
            return {
                **self._stats,
                'pending_count': len(self._pending),
                'running_count': len(self._running),
                'total_jobs': len(self._jobs),
            }
    
    def _check_dependencies(self, job: Job) -> bool:
        """Check if all job dependencies are satisfied."""
        for dep_id in job.dependencies:
            if dep_id in self._jobs:
                dep_job = self._jobs[dep_id]
                if dep_job.status != JobStatus.COMPLETED:
                    return False
            else:
                # Dependency doesn't exist, consider it satisfied
                pass
        return True
    
    def _execute_job(self, job: Job) -> None:
        """Execute a job."""
        with self._lock:
            job.status = JobStatus.RUNNING
            job.started_at = time.time()
            self._running.add(job.id)
        
        start_time = time.time()
        success = False
        error = None
        value = None
        
        try:
            if job.func is None:
                raise ValueError(f"Job {job.id} has no function registered")
            
            result = job.func(*job.args, **job.kwargs)
            
            # Handle coroutine
            if asyncio.iscoroutine(result):
                loop = asyncio.new_event_loop()
                try:
                    value = loop.run_until_complete(result)
                finally:
                    loop.close()
            else:
                value = result
            
            success = True
            
        except Exception as e:
            error = str(e)
            logger.error(f"Job {job.id} failed: {e}")
        
        execution_time = time.time() - start_time
        
        with self._lock:
            self._running.discard(job.id)
            job.completed_at = time.time()
            
            if success:
                job.status = JobStatus.COMPLETED
                job.result = JobResult(
                    success=True,
                    value=value,
                    execution_time=execution_time,
                    attempts=job.retry_count + 1,
                )
                self._stats['total_completed'] += 1
                
                # For periodic jobs, reschedule
                if job.is_periodic() and job.interval:
                    job.status = JobStatus.PENDING
                    job.scheduled_time = time.time() + job.interval
                    job.started_at = None
                    job.completed_at = None
                    job.result = None
                    self._pending.append(job)
                    self._pending.sort()
            else:
                if job.retry_count < job.max_retries:
                    job.retry_count += 1
                    job.status = JobStatus.RETRY
                    job.scheduled_time = time.time() + job.retry_delay
                    job.started_at = None
                    job.completed_at = None
                    self._pending.append(job)
                    self._pending.sort()
                    logger.info(f"Job {job.id} scheduled for retry {job.retry_count}/{job.max_retries}")
                else:
                    job.status = JobStatus.FAILED
                    job.result = JobResult(
                        success=False,
                        error=error,
                        execution_time=execution_time,
                        attempts=job.retry_count + 1,
                    )
                    self._stats['total_failed'] += 1
            
            self._completed[job.id] = job
            
            if self._auto_persist:
                self._maybe_persist()
    
    def _scheduler_loop(self) -> None:
        """Main scheduler loop."""
        while self._running_flag:
            with self._lock:
                now = time.time()
                ready_jobs = []
                
                for job in self._pending[:]:
                    if job.is_ready(now) and self._check_dependencies(job):
                        ready_jobs.append(job)
                        self._pending.remove(job)
                
                for job in ready_jobs:
                    self._executor.submit(self._execute_job, job)
                
                # Wait for next job or timeout
                if self._pending:
                    next_job = min(self._pending, key=lambda j: j.scheduled_time or 0)
                    wait_time = max(0.1, (next_job.scheduled_time or 0) - time.time())
                    self._condition.wait(timeout=min(wait_time, 1.0))
                else:
                    self._condition.wait(timeout=1.0)
    
    def start(self) -> None:
        """Start the scheduler."""
        with self._lock:
            if self._running_flag:
                return
            
            self._running_flag = True
            self._scheduler_thread = threading.Thread(
                target=self._scheduler_loop,
                daemon=True,
                name="JobScheduler"
            )
            self._scheduler_thread.start()
    
    def stop(self, wait: bool = True, timeout: Optional[float] = None) -> None:
        """
        Stop the scheduler.
        
        Args:
            wait: Wait for running jobs to complete
            timeout: Maximum time to wait in seconds
        """
        with self._lock:
            self._running_flag = False
            self._condition.notify_all()
        
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=timeout)
            self._scheduler_thread = None
        
        if wait:
            self._executor.shutdown(wait=True)
    
    def clear(self, include_running: bool = False) -> int:
        """
        Clear all jobs.
        
        Args:
            include_running: Also clear running jobs (will not stop them)
            
        Returns:
            Number of jobs cleared
        """
        with self._lock:
            if include_running:
                count = len(self._jobs)
                self._jobs.clear()
                self._pending.clear()
                self._running.clear()
                self._completed.clear()
            else:
                count = len(self._jobs) - len(self._running)
                self._pending.clear()
                self._jobs = {jid: job for jid, job in self._jobs.items() 
                             if job.status == JobStatus.RUNNING}
                self._completed.clear()
            
            if self._auto_persist:
                self._maybe_persist()
            
            return count
    
    def _maybe_persist(self) -> None:
        """Persist if enough time has passed."""
        now = time.time()
        if now - self._last_persist >= self._persist_interval:
            self.persist()
    
    def persist(self, path: Optional[str] = None) -> bool:
        """
        Persist scheduler state to a JSON file.
        
        Args:
            path: Custom path (uses persistence_path if not provided)
            
        Returns:
            True if successful
        """
        path = path or self._persistence_path
        if not path:
            return False
        
        try:
            with self._lock:
                data = {
                    'jobs': [job.to_dict() for job in self._jobs.values()],
                    'stats': self._stats,
                    'timestamp': time.time(),
                }
            
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self._last_persist = time.time()
            return True
            
        except Exception as e:
            logger.error(f"Failed to persist scheduler state: {e}")
            return False
    
    def _load_from_file(self) -> int:
        """Load scheduler state from file."""
        if not self._persistence_path or not Path(self._persistence_path).exists():
            return 0
        
        try:
            with open(self._persistence_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with self._lock:
                for job_data in data.get('jobs', []):
                    job = Job.from_dict(job_data)
                    # Only load non-completed, non-failed, non-cancelled jobs
                    if job.status in (JobStatus.PENDING, JobStatus.RETRY):
                        job.status = JobStatus.PENDING
                        self._jobs[job.id] = job
                        self._pending.append(job)
                
                self._pending.sort()
                self._stats = data.get('stats', self._stats)
            
            return len(self._jobs)
            
        except Exception as e:
            logger.error(f"Failed to load scheduler state: {e}")
            return 0
    
    def load(self, path: str) -> int:
        """
        Load scheduler state from a specific file.
        
        Args:
            path: Path to load from
            
        Returns:
            Number of jobs loaded
        """
        self._persistence_path = path
        return self._load_from_file()
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
    
    def __len__(self) -> int:
        """Return the total number of jobs."""
        return len(self._jobs)
    
    def __contains__(self, job_id: str) -> bool:
        """Check if a job exists."""
        return job_id in self._jobs


# =============================================================================
# Convenience Functions
# =============================================================================

def schedule(
    func: Callable,
    delay_seconds: Optional[float] = None,
    scheduled_time: Optional[float] = None,
    **kwargs
) -> str:
    """
    Schedule a function to run.
    
    This creates a global scheduler instance for convenience.
    
    Args:
        func: The function to execute
        delay_seconds: Delay before execution
        scheduled_time: Specific timestamp to run at
        **kwargs: Additional job arguments
        
    Returns:
        Job ID
    """
    global _default_scheduler
    if '_default_scheduler' not in globals():
        _default_scheduler = JobScheduler()
        _default_scheduler.start()
    return _default_scheduler.schedule_once(
        func,
        delay_seconds=delay_seconds,
        scheduled_time=scheduled_time,
        **kwargs
    )


def schedule_interval(
    func: Callable,
    interval_seconds: float,
    **kwargs
) -> str:
    """
    Schedule a function to run periodically.
    
    This uses the global scheduler instance.
    
    Args:
        func: The function to execute
        interval_seconds: Interval between executions
        **kwargs: Additional job arguments
        
    Returns:
        Job ID
    """
    global _default_scheduler
    if '_default_scheduler' not in globals():
        _default_scheduler = JobScheduler()
        _default_scheduler.start()
    return _default_scheduler.schedule_interval(func, interval_seconds, **kwargs)


def run_in_thread(func: Callable, *args, **kwargs) -> Future:
    """
    Run a function in a background thread immediately.
    
    Args:
        func: The function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Future object
    """
    global _default_executor
    if '_default_executor' not in globals():
        _default_executor = ThreadPoolExecutor(max_workers=4)
    return _default_executor.submit(func, *args, **kwargs)


# =============================================================================
# Decorators
# =============================================================================

def scheduled(
    delay_seconds: Optional[float] = None,
    scheduled_time: Optional[float] = None,
    **kwargs
):
    """
    Decorator to schedule a function.
    
    Example:
        @scheduled(delay_seconds=60)
        def my_task():
            print("Running after 60 seconds")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        
        schedule(func, delay_seconds=delay_seconds, 
                scheduled_time=scheduled_time, **kwargs)
        return wrapper
    return decorator


def periodic(interval_seconds: float, **kwargs):
    """
    Decorator to schedule a function to run periodically.
    
    Example:
        @periodic(60)
        def heartbeat():
            print("Heartbeat every 60 seconds")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        
        schedule_interval(func, interval_seconds, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# Job Builder (Fluent Interface)
# =============================================================================

class JobBuilder:
    """
    Fluent interface for building and scheduling jobs.
    
    Example:
        job_id = (JobBuilder(my_func)
            .with_name("my_job")
            .with_priority(JobPriority.HIGH)
            .with_delay(60)
            .with_retry(3, 5.0)
            .with_tags("important", "cleanup")
            .schedule())
    """
    
    def __init__(self, func: Callable):
        self._func = func
        self._name: Optional[str] = None
        self._args: Tuple = ()
        self._kwargs: Dict = {}
        self._delay_seconds: Optional[float] = None
        self._scheduled_time: Optional[float] = None
        self._interval_seconds: Optional[float] = None
        self._priority: JobPriority = JobPriority.NORMAL
        self._max_retries: int = 0
        self._retry_delay: float = 1.0
        self._dependencies: List[str] = []
        self._timeout: Optional[float] = None
        self._tags: List[str] = []
        self._metadata: Dict = {}
    
    def with_name(self, name: str) -> 'JobBuilder':
        """Set job name."""
        self._name = name
        return self
    
    def with_args(self, *args, **kwargs) -> 'JobBuilder':
        """Set job arguments."""
        self._args = args
        self._kwargs = kwargs
        return self
    
    def with_delay(self, seconds: float) -> 'JobBuilder':
        """Set delay before execution."""
        self._delay_seconds = seconds
        return self
    
    def at_time(self, timestamp: float) -> 'JobBuilder':
        """Set specific execution time."""
        self._scheduled_time = timestamp
        return self
    
    def at_datetime(self, dt: datetime) -> 'JobBuilder':
        """Set specific execution datetime."""
        self._scheduled_time = dt.timestamp()
        return self
    
    def every(self, interval_seconds: float) -> 'JobBuilder':
        """Set periodic interval."""
        self._interval_seconds = interval_seconds
        return self
    
    def with_priority(self, priority: JobPriority) -> 'JobBuilder':
        """Set job priority."""
        self._priority = priority
        return self
    
    def with_retry(self, max_retries: int, delay: float = 1.0) -> 'JobBuilder':
        """Set retry configuration."""
        self._max_retries = max_retries
        self._retry_delay = delay
        return self
    
    def depends_on(self, *job_ids: str) -> 'JobBuilder':
        """Set job dependencies."""
        self._dependencies.extend(job_ids)
        return self
    
    def with_timeout(self, seconds: float) -> 'JobBuilder':
        """Set execution timeout."""
        self._timeout = seconds
        return self
    
    def with_tags(self, *tags: str) -> 'JobBuilder':
        """Set job tags."""
        self._tags.extend(tags)
        return self
    
    def with_metadata(self, **kwargs) -> 'JobBuilder':
        """Set job metadata."""
        self._metadata.update(kwargs)
        return self
    
    def schedule(self, scheduler: Optional[JobScheduler] = None) -> str:
        """
        Schedule the job.
        
        Args:
            scheduler: Custom scheduler (uses global if not provided)
            
        Returns:
            Job ID
        """
        if scheduler is None:
            global _default_scheduler
            if '_default_scheduler' not in globals():
                _default_scheduler = JobScheduler()
                _default_scheduler.start()
            scheduler = _default_scheduler
        
        if self._interval_seconds:
            return scheduler.schedule_interval(
                func=self._func,
                interval_seconds=self._interval_seconds,
                name=self._name,
                args=self._args,
                kwargs=self._kwargs,
                delay_seconds=self._delay_seconds,
                scheduled_time=self._scheduled_time,
                priority=self._priority,
                max_retries=self._max_retries,
                retry_delay=self._retry_delay,
                tags=self._tags,
                metadata=self._metadata,
            )
        else:
            return scheduler.schedule_once(
                func=self._func,
                name=self._name,
                args=self._args,
                kwargs=self._kwargs,
                delay_seconds=self._delay_seconds,
                scheduled_time=self._scheduled_time,
                priority=self._priority,
                max_retries=self._max_retries,
                retry_delay=self._retry_delay,
                dependencies=self._dependencies,
                timeout=self._timeout,
                tags=self._tags,
                metadata=self._metadata,
            )