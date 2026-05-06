# UUIDv7 Utils

UUIDv7 生成和操作工具模块 - RFC 9562 标准实现

## 简介

UUIDv7 是一种基于时间戳的 UUID 格式，在 RFC 9562 中定义。与传统 UUIDv4 相比，UUIDv7 具有以下优势：

- **自然排序**：按创建时间排序，无需额外字段
- **数据库友好**：作为主键时索引效率更高
- **分布式系统**：无需协调即可生成唯一 ID
- **时间查询**：可直接从 UUID 提取时间戳进行过滤

## 格式结构（128 位）

| 位范围 | 内容 | 描述 |
|--------|------|------|
| 0-47 | 时间戳 | Unix 毫秒时间戳 |
| 48-51 | 版本 | 固定为 7 |
| 52-63 | rand_a | 12 位随机/计数器 |
| 64-65 | 变体 | RFC 4122 变体 (10) |
| 66-127 | rand_b | 62 位随机 |

## 快速开始

```python
from uuidv7_utils import generate

# 生成 UUIDv7
uuid = generate()
print(uuid)  # 018f3b6a-1b2c-7d3e-8f4a-5b6c7d8e9f0a

# 提取时间信息
print(uuid.timestamp)   # Unix 毫秒时间戳
print(uuid.datetime)    # datetime 对象
```

## 主要功能

### 1. 基本 UUID 生成

```python
from uuidv7_utils import UUIDv7

# 生成随机 UUIDv7
uuid = UUIDv7.generate()

# 属性访问
uuid.version       # 7
uuid.variant       # 2 (RFC 4122)
uuid.timestamp     # Unix 毫秒时间戳
uuid.datetime      # datetime 对象
uuid.hex           # 32 字符十六进制
uuid.bytes         # 16 字节
uuid.int           # 128 位整数
```

### 2. 单调递增生成

```python
from uuidv7_utils import UUIDv7Generator

gen = UUIDv7Generator()

# 保证同一毫秒内 UUID 递增
uuid1 = gen.generate()
uuid2 = gen.generate()
assert uuid1 < uuid2  # 总是成立
```

### 3. 批量生成

```python
from uuidv7_utils import generate_batch

# 生成 100 个单调递增的 UUID
uuids = generate_batch(100, monotonic=True)

# 验证顺序
assert uuids == sorted(uuids)
```

### 4. 从时间戳创建

```python
from uuidv7_utils import from_datetime, from_timestamp
from datetime import datetime, timezone

# 从 datetime 创建
dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
uuid = from_datetime(dt)

# 从时间戳创建
uuid = from_timestamp(1704067200000)
```

### 5. 解析和验证

```python
from uuidv7_utils import parse, is_uuidv7, UUIDv7Validator

# 解析多种格式
uuid = parse("018f3b6a-1b2c-7d3e-8f4a-5b6c7d8e9f0a")
uuid = parse("018f3b6a1b2c7d3e8f4a5b6c7d8e9f0a")  # 无分隔符
uuid = parse(uuid_bytes)  # 16 字节

# 验证
if is_uuidv7(uuid_string):
    uuid = UUIDv7Validator.validate(uuid_string)
```

### 6. UUID 集合操作

```python
from uuidv7_utils import UUIDv7Set

# 创建集合
uuid_set = UUIDv7Set([uuid1, uuid2, uuid3])

# 操作
uuid_set.add(uuid4)
uuid_set.remove(uuid1)
if uuid2 in uuid_set:
    print("存在")

# 转换
hex_list = uuid_set.to_hex_list()
uuid_list = uuid_set.to_list()
```

### 7. 时间范围过滤

```python
from uuidv7_utils import UUIDv7Range

# 最近 24 小时范围
range_24h = UUIDv7Range.last_hours(24)

# 检查 UUID 是否在范围内
if uuid in range_24h:
    print("最近 24 小时创建")

# 自定义时间范围
start = datetime(2024, 1, 1, tzinfo=timezone.utc)
end = datetime(2024, 12, 31, tzinfo=timezone.utc)
year_2024 = UUIDv7Range.from_datetime_range(start, end)
```

### 8. 分布式系统

```python
from uuidv7_utils import UUIDv7Generator

# 不同节点使用不同的 node_id
node_1 = UUIDv7Generator(node_id=1)
node_2 = UUIDv7Generator(node_id=2)

# 每个节点独立生成 ID
id_1 = node_1.generate()
id_2 = node_2.generate()
```

## 数据库应用场景

### 主键设计

```python
# 使用单调生成器作为主键
gen = UUIDv7Generator()

# 插入记录
for i in range(1000):
    record_id = gen.generate()
    # INSERT INTO users (id, name) VALUES (record_id, ...)
```

**优势**：
- B-tree 索引效率高（顺序插入）
- 无需额外的 created_at 字段
- 分布式系统无需协调

### 时间范围查询

```python
# 查询最近 7 天的记录
range_7d = UUIDv7Range.last_days(7)

# WHERE id >= min_uuid AND id <= max_uuid
min_uuid = UUIDv7.from_timestamp(range_7d.start_ms)
max_uuid = UUIDv7.from_timestamp(range_7d.end_ms)
```

## 与其他 UUID 版本对比

| 特性 | UUIDv4 | UUIDv1 | UUIDv7 |
|------|--------|--------|--------|
| 排序能力 | ❌ | ⚠️ 部分 | ✅ 完全 |
| 数据库索引效率 | 低 | 中 | 高 |
| 时间戳提取 | ❌ | ✅ | ✅ |
| 分布式协调 | 不需要 | 需要 | 不需要 |
| 隐私性（无 MAC 地址） | ✅ | ❌ | ✅ |

## 性能特点

- **生成速度**：约 100,000 个/秒（单线程）
- **内存占用**：每个 UUID 16 字节
- **线程安全**：所有生成器都是线程安全的

## 零依赖

完全使用 Python 标准库实现，无需任何外部依赖：
- `time` - 时间戳
- `secrets` - 安全随机数
- `threading` - 线程安全
- `datetime` - 时间处理

## API 参考

### UUIDv7 类

| 方法 | 描述 |
|------|------|
| `generate()` | 生成随机 UUIDv7 |
| `generate_monotonic()` | 生成单调递增 UUIDv7 |
| `from_timestamp(ms)` | 从时间戳创建 |
| `from_datetime(dt)` | 从 datetime 创建 |

### 属性

| 属性 | 描述 |
|------|------|
| `timestamp` | Unix 毫秒时间戳 |
| `datetime` | datetime 对象 |
| `version` | UUID 版本（7） |
| `variant` | UUID 变体（2） |
| `hex` | 32 字符十六进制 |
| `bytes` | 16 字节 |
| `int` | 128 位整数 |

### UUIDv7Generator 类

| 方法 | 描述 |
|------|------|
| `generate()` | 生成单调递增 UUID |
| `generate_batch(n)` | 批量生成 n 个 UUID |

### UUIDv7Range 类

| 方法 | 描述 |
|------|------|
| `from_datetime_range(start, end)` | 从 datetime 创建范围 |
| `from_timestamp(ts, duration)` | 从时间戳创建范围 |
| `last_hours(n)` | 最近 n 小时范围 |
| `last_days(n)` | 最近 n 天范围 |

### 便捷函数

| 函数 | 描述 |
|------|------|
| `generate()` | 生成 UUIDv7 |
| `generate_monotonic()` | 生成单调 UUIDv7 |
| `generate_batch(n)` | 批量生成 |
| `parse(value)` | 解析 UUID |
| `is_uuidv7(value)` | 验证 UUIDv7 |
| `from_timestamp(ms)` | 从时间戳创建 |
| `from_datetime(dt)` | 从 datetime 创建 |

## 运行测试

```bash
python uuidv7_utils/test.py
```

## 运行示例

```bash
python uuidv7_utils/examples.py
```

## 版本历史

- **1.0.0** - 初始版本
  - UUIDv7 生成（随机、单调）
  - 时间戳提取和转换
  - UUID 集合和范围过滤
  - 分布式节点支持
  - 线程安全生成器

## 许可证

MIT License

## 参考

- [RFC 9562 - Universally Unique IDentifiers (UUIDs)](https://www.rfc-editor.org/rfc/rfc9562)
- [UUIDv7 Format Specification](https://www.rfc-editor.org/rfc/rfc9562#name-uuid-version-7)