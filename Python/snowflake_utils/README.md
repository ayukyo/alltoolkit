# Snowflake Utils


Snowflake ID Generator - 分布式唯一ID生成器

Snowflake ID 是 Twitter 开发的分布式唯一ID生成算法，生成64位整数ID。
特点：
- 时间有序：ID按时间递增，便于索引
- 分布式：支持多节点同时生成不冲突
- 高性能：单节点每毫秒可生成4096个ID
- 无需协调：不依赖数据库或中心化服务

ID结构（64位）:
| 1位 | 41位时间戳 | 10位机器ID | 12位序列号 |
|-----|-----------|-----------|-----------|
|  0  | 毫秒级时间 | 数据中心+工作节点 | 毫秒内序列 |

常用场景：
- 数据库主键
- 分布式系统唯一标识
- 订单号、消息ID
- 追踪ID


## 功能

### 类

- **SnowflakeConfig**: Snowflake 配置类
- **SnowflakeGenerator**: Snowflake ID 生成器

线程安全的分布式唯一ID生成器。

示例:
    >>> generator = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    >>> snowflake_id = generator
  方法: datacenter_id, worker_id, epoch, epoch_datetime, generate ... (14 个方法)
- **DiscordSnowflake**: Discord Snowflake ID 生成器

Discord的Snowflake使用2015-01-01 00:00:00 UTC作为起始时间。
Discord ID是公开的，通常以字符串形式使用。

示例:
    >>> gen = DiscordSnowflake(worker_id=1)
    >>> discord_id = gen
  方法: generate_str, get_creation_time
- **TwitterSnowflake**: Twitter Snowflake ID 生成器

Twitter原始Snowflake使用2010-11-04 01:42:54 UTC作为起始时间。

示例:
    >>> gen = TwitterSnowflake(datacenter_id=1, worker_id=1)
    >>> tweet_id = gen
  方法: get_creation_time

### 函数

- **get_default_generator(**) - 获取默认的全局生成器
- **generate_id(**) - 使用默认生成器生成Snowflake ID
- **generate_batch(count**) - 使用默认生成器批量生成Snowflake ID
- **decompose_id(snowflake_id, epoch**) - 解析Snowflake ID
- **extract_timestamp(snowflake_id, epoch**) - 从Snowflake ID提取时间戳
- **extract_datetime(snowflake_id, epoch**) - 从Snowflake ID提取datetime对象
- **create_generator(datacenter_id, worker_id, epoch**) - 创建Snowflake生成器
- **datacenter_id(self**) - 获取数据中心ID
- **worker_id(self**) - 获取工作节点ID
- **epoch(self**) - 获取起始时间戳

... 共 24 个函数

## 使用示例

```python
from mod import get_default_generator

# 使用 get_default_generator
result = get_default_generator()
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
