# Token Bucket Rate Limiter Utils

令牌桶限流器工具集，提供多种限流算法实现。

## 功能特性

- **TokenBucket**: 基础令牌桶实现
- **ThreadSafeTokenBucket**: 线程安全版本，支持阻塞等待
- **HierarchicalTokenBucket**: 分层级联限流（全局+用户级）
- **SlidingWindowBucket**: 滑动窗口混合实现

## 安装使用

```python
from token_bucket_utils import TokenBucket, ThreadSafeTokenBucket

# 创建桶：容量10，每秒补充2个令牌
bucket = TokenBucket(capacity=10, refill_rate=2)

# 消费令牌
if bucket.consume(1):
    # 执行操作
    pass
else:
    # 被限流
    wait_time = bucket.wait_time(1)
```

## 算法说明

### 令牌桶算法
- 令牌以固定速率放入桶中
- 桶有最大容量（突发上限）
- 每次请求消耗令牌
- 令牌不足时拒绝请求

### 应用场景
- API 限流
- 网络流量控制
- 数据库访问限制
- Web 爬虫速率控制

## 测试

```bash
python -m pytest test_token_bucket.py -v
```

## 示例

```bash
python examples.py
```

## 文件结构

```
token_bucket_utils/
├── __init__.py           # 模块导出
├── token_bucket.py       # 基础实现
├── thread_safe_bucket.py # 线程安全版本
├── hierarchical_bucket.py# 分层限流
├── sliding_bucket.py     # 滑动窗口版本
├── test_token_bucket.py  # 单元测试
├── examples.py           # 使用示例
└── README.md             # 说明文档
```

## 依赖

零外部依赖，仅使用 Python 标准库。