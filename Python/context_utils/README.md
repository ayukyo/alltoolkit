# Context Utils


AllToolkit - Python Context Utilities

A zero-dependency, production-ready context management utility module.
Provides thread-safe scoped context storage, request context management,
context propagation across call chains, and nested scope support.

Author: AllToolkit
License: MIT


## 功能

### 类

- **ContextError**: Base exception for context operations
- **ContextNotFoundError**: Raised when a context variable is not found
- **ScopeNotFoundError**: Raised when a scope is not found
- **InvalidScopeError**: Raised when scope operation is invalid
- **Scope**: Represents a single scope in the context hierarchy
  方法: get, get_local, set, delete, has ... (12 个方法)
- **ScopedContext**: Thread-safe scoped context manager
  方法: current_scope, root_scope, scope_depth, get, get_local ... (18 个方法)
- **RequestContext**: Request-scoped context manager
  方法: active, request_id, elapsed, start, end ... (11 个方法)
- **ContextVar**: A context variable that can have different values in different contexts
  方法: get, set, reset, clear, is_set ... (7 个方法)
- **ContextPropagator**: Propagate context across boundaries (threads, tasks, etc
  方法: capture, apply, captured_items, age, propagate

### 函数

- **get_context(**) - Get the global scoped context.
- **get_request_context(**) - Get the global request context.
- **ctx_get(key, default**) - Get a value from the global context.
- **ctx_set(key, value**) - Set a value in the global context.
- **ctx_has(key**) - Check if key exists in global context.
- **ctx_delete(key**) - Delete a key from global context.
- **ctx_scope(name, readonly**) - Create a new scope in the global context.
- **ctx_snapshot(**) - Take a snapshot of the global context.
- **ctx_restore(snapshot**) - Restore global context from a snapshot.
- **with_context(**) - Decorator to set context values for a function.

... 共 70 个函数

## 使用示例

```python
from mod import get_context

# 使用 get_context
result = get_context()
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
