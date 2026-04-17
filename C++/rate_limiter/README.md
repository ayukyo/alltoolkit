# Rate Limiter - 速率限制器

线程安全的 C++17 速率限制工具库，零外部依赖。

## 算法实现

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| **TokenBucket** | 允许突发流量，平滑速率限制 | API 调用、流量整形 |
| **SlidingWindow** | 精确限制，无突发边界问题 | 登录限制、敏感操作 |
| **FixedWindow** | 简单高效，内存占用低 | 简单限流场景 |
| **LeakyBucket** | 恒定输出速率，削峰填谷 | 消息队列、流量平滑 |

## 快速开始

```cpp
#include "rate_limiter.hpp"
using namespace alltoolkit;

// 令牌桶：100 容量，10 tokens/秒
TokenBucket bucket(100, 10.0);

if (bucket.try_acquire()) {
    // 允许请求
} else {
    // 超过限制
}

// 阻塞式获取
bucket.acquire();  // 会等待直到获得令牌
```

## 使用示例

### 1. Token Bucket（令牌桶）

```cpp
// 容量 10，每秒补充 5 个令牌
TokenBucket bucket(10, 5.0);

// 突发请求
bucket.try_acquire(10);  // 一次获取 10 个

// 等待令牌补充
std::this_thread::sleep_for(std::chrono::milliseconds(400));
bucket.try_acquire();  // 现在有 2 个令牌
```

### 2. Sliding Window（滑动窗口）

```cpp
// 每秒最多 5 次请求
SlidingWindow window(5, 1000);

for (int i = 0; i < 6; i++) {
    if (window.try_acquire()) {
        std::cout << "请求 " << i << " 允许\n";
    } else {
        std::cout << "请求 " << i << " 拒绝\n";
    }
}
// 输出: 前 5 个允许，第 6 个拒绝
```

### 3. Fixed Window（固定窗口）

```cpp
// 每 500ms 最多 3 次请求
FixedWindow window(3, 500);

// 查询窗口剩余时间
int64_t remaining = window.remaining_window_time();
```

### 4. Leaky Bucket（漏桶）

```cpp
// 容量 10，每秒处理 3 个请求
LeakyBucket bucket(10, 3.0);

// 填入请求
bucket.try_acquire(5);

// 查看剩余容量
double available = bucket.available_permits();  // 5.0
```

### 5. 工厂预设

```cpp
// API 限流器：100 次/分钟
auto api = RateLimiterFactory::create_api_limiter();

// 登录限制器：5 次/分钟
auto login = RateLimiterFactory::create_login_limiter();

// 上传限制器：10 次/小时
auto upload = RateLimiterFactory::create_upload_limiter();

// 消息限制器：30 次/分钟
auto message = RateLimiterFactory::create_message_limiter();
```

### 6. 自定义创建

```cpp
// 创建任意类型的限流器
auto token = RateLimiterFactory::create("token", 50.0, 100);
auto sliding = RateLimiterFactory::create("sliding", 10.0, 10);
auto leaky = RateLimiterFactory::create("leaky", 5.0, 15);
auto fixed = RateLimiterFactory::create("fixed", 20.0, 20);
```

### 7. 等待时间估算

```cpp
TokenBucketWithEstimate bucket(5, 2.0);

bucket.try_acquire(5);  // 用完所有令牌

// 估算需要等待多久
int64_t wait_ms = bucket.estimate_wait_time();     // ~500ms
int64_t wait_4 = bucket.estimate_wait_time(4);      // ~2000ms
```

## 编译

```bash
# 编译测试
g++ -std=c++17 -o test_rate_limiter test_rate_limiter.cpp -pthread
./test_rate_limiter

# 编译示例
g++ -std=c++17 -o example_rate_limiter example_rate_limiter.cpp -pthread
./example_rate_limiter
```

## API 参考

### TokenBucket

| 方法 | 说明 |
|------|------|
| `TokenBucket(capacity, refill_rate)` | 构造函数 |
| `try_acquire()` | 尝试获取 1 个令牌 |
| `try_acquire(permits)` | 尝试获取多个令牌 |
| `acquire()` | 阻塞获取 1 个令牌 |
| `acquire(permits)` | 阻塞获取多个令牌 |
| `available_permits()` | 当前可用令牌数 |
| `capacity()` | 桶容量 |
| `refill_rate()` | 令牌补充速率 |

### SlidingWindow

| 方法 | 说明 |
|------|------|
| `SlidingWindow(max_requests, window_ms)` | 构造函数 |
| `try_acquire()` / `try_acquire(permits)` | 尝试获取许可 |
| `acquire()` | 阻塞获取 |
| `available_permits()` | 剩余许可数 |
| `max_requests()` | 窗口最大请求数 |
| `window_ms()` | 窗口大小（毫秒）|

### FixedWindow

| 方法 | 说明 |
|------|------|
| `FixedWindow(max_requests, window_ms)` | 构造函数 |
| `try_acquire()` / `try_acquire(permits)` | 尝试获取许可 |
| `acquire()` | 阻塞获取 |
| `available_permits()` | 剩余许可数 |
| `remaining_window_time()` | 窗口剩余时间 |

### LeakyBucket

| 方法 | 说明 |
|------|------|
| `LeakyBucket(capacity, leak_rate)` | 构造函数 |
| `try_acquire()` / `try_acquire(permits)` | 尝试添加请求 |
| `acquire()` | 阻塞添加 |
| `available_permits()` | 剩余容量 |
| `capacity()` | 桶容量 |
| `leak_rate()` | 漏出速率 |

## 线程安全

所有实现都是线程安全的，使用 `std::mutex` 保护内部状态。

```cpp
TokenBucket bucket(100, 10.0);

// 多线程安全使用
std::vector<std::thread> threads;
for (int i = 0; i < 10; i++) {
    threads.emplace_back([&bucket]() {
        for (int j = 0; j < 20; j++) {
            if (bucket.try_acquire()) {
                // 处理请求
            }
        }
    });
}
```

## 算法选择指南

| 场景 | 推荐算法 | 原因 |
|------|----------|------|
| API 调用限流 | TokenBucket | 允许突发，平滑流量 |
| 登录/密码尝试 | SlidingWindow | 精确控制，无边界突发 |
| 简单计数限流 | FixedWindow | 高效，低内存 |
| 消息发送 | LeakyBucket | 平滑输出，防止洪泛 |
| 文件上传 | FixedWindow | 按时间窗口统计 |

## License

MIT License