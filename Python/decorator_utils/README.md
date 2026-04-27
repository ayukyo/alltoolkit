# Decorator Utils


decorator_utils - Python Decorator Utilities
============================================

A collection of commonly used decorators for Python development.
Zero external dependencies - uses only Python standard library.

Features:
- @timer - Measure execution time
- @retry - Auto-retry on failure with configurable backoff
- @memoize - Cache function results
- @singleton - Ensure only one instance exists
- @deprecated - Mark functions as deprecated
- @validate_types - Runtime type checking
- @rate_limit - Limit function call frequency
- @log_calls - Log function calls with arguments
- @timeout - Timeout for long-running functions
- @count_calls - Count function invocations

Author: AllToolkit
Date: 2026-04-17


## 功能

### 函数

- **timer(func**) - Decorator to measure and print function execution time.
- **timer_verbose(include_args**) - Decorator factory for timer with options.
- **retry(max_attempts, delay, backoff**, ...) - Decorator to retry a function on failure with exponential backoff.
- **memoize(maxsize, typed, ttl**) - Decorator to cache function results with optional TTL.
- **singleton(cls**) - Class decorator to ensure only one instance exists.
- **deprecated(reason, version, replacement**) - Decorator to mark a function as deprecated.
- **validate_types(**) - Decorator for runtime type checking of function arguments.
- **rate_limit(calls, period, raise_on_limit**) - Decorator to limit function call frequency.
- **log_calls(logger, include_result, include_time**) - Decorator to log function calls with arguments.
- **timeout(seconds**) - Decorator to limit function execution time.

... 共 45 个函数

## 使用示例

```python
from mod import timer

# 使用 timer
result = timer()
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
