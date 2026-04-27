# Job Scheduler Utils


AllToolkit - Python Job Scheduler Utilities

A zero-dependency, production-ready job scheduling module.
Supports delayed jobs, periodic jobs, job prioritization, dependencies,
cancellation, retry, and simple persistence.

Author: AllToolkit
License: MIT


## 功能

### 类

- **JobStatus**: Job status enumeration
- **JobPriority**: Job priority levels
- **ScheduleType**: Schedule type enumeration
- **JobResult**: Result of a job execution
  方法: to_dict
- **Job**: Represents a scheduled job
  方法: is_ready, is_periodic, to_dict, from_dict
- **JobScheduler**: A thread-safe job scheduler supporting delayed, periodic, and dependent jobs
  方法: register_function, unregister_function, schedule_once, schedule_interval, schedule_delayed ... (20 个方法)
- **JobBuilder**: Fluent interface for building and scheduling jobs
  方法: with_name, with_args, with_delay, at_time, at_datetime ... (13 个方法)

### 函数

- **schedule(func, delay_seconds, scheduled_time**) - Schedule a function to run.
- **schedule_interval(func, interval_seconds**) - Schedule a function to run periodically.
- **run_in_thread(func**) - Run a function in a background thread immediately.
- **scheduled(delay_seconds, scheduled_time**) - Decorator to schedule a function.
- **periodic(interval_seconds**) - Decorator to schedule a function to run periodically.
- **to_dict(self**)
- **is_ready(self, now**) - Check if the job is ready to run.
- **is_periodic(self**) - Check if this is a periodic job.
- **to_dict(self, include_func**) - Convert job to dictionary for serialization.
- **from_dict(cls, data**) - Create a Job from dictionary (without function).

... 共 47 个函数

## 使用示例

```python
from mod import schedule

# 使用 schedule
result = schedule()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
