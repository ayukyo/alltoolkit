# Rate Limiter Utils


rate_limiter_utils - 速率限制器工具集

提供多种速率限制算法的实现，支持：
- 滑动窗口计数器 (Sliding Window Counter)
- 令牌桶 (Token Bucket)
- 漏桶 (Leaky Bucket)
- 固定窗口计数器 (Fixed Window Counter)

所有实现均为零外部依赖，纯 Python 标准库实现。

作者: AllToolkit
日期: 2026-04-19


## 功能

### 类

- **RateLimitResult**: 速率限制检查结果
  方法: to_dict
- **RateLimiterBase**: 速率限制器基类
  方法: try_acquire, get_state, reset
- **FixedWindowRateLimiter**: 固定窗口计数器算法

特点：
- 实现简单，内存占用小
- 存在边界突发问题（两个窗口交界处可能突破限制）
- 适合对精度要求不高的场景
  方法: try_acquire, get_state, reset
- **SlidingWindowRateLimiter**: 滑动窗口计数器算法

特点：
- 精确控制速率，无边界突发问题
- 使用时间戳队列记录请求
- 适合需要精确控制的场景
  方法: try_acquire, get_state, reset
- **TokenBucketRateLimiter**: 令牌桶算法

特点：
- 支持突发流量（令牌可累积）
- 平滑限流
- 适合需要处理突发流量的场景

参数：
    max_requests: 桶的最大容量
    window_seconds: 填满桶所需的时间
  方法: try_acquire, get_state, reset
- **LeakyBucketRateLimiter**: 漏桶算法

特点：
- 以恒定速率处理请求
- 无突发流量，严格限流
- 适合需要严格控制流出速率的场景
  方法: try_acquire, get_state, reset
- **RateLimiterRegistry**: 速率限制器注册表

管理多个命名限制器，支持按 key（如用户ID、IP等）进行限制
  方法: try_acquire, get_state, reset, reset_all, cleanup
- **RateLimitExceeded**: 速率限制异常

### 函数

- **rate_limit(limiter, on_reject**) - 装饰器：为函数添加速率限制
- **create_limiter(algorithm, max_requests, window_seconds**) - 创建速率限制器的便捷函数
- **to_dict(self**) - 转换为字典
- **try_acquire(self, tokens**) - 尝试获取许可
- **get_state(self**) - 获取当前状态（用于监控/调试）
- **reset(self**) - 重置限制器状态
- **try_acquire(self, tokens**)
- **get_state(self**)
- **reset(self**)
- **try_acquire(self, tokens**)

... 共 25 个函数

## 使用示例

```python
from mod import rate_limit

# 使用 rate_limit
result = rate_limit()
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
