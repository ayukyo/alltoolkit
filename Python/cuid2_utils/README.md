# CUID2 Utils

安全、现代的唯一 ID 生成工具。

## 简介

CUID2 是一个现代化的、安全的唯一 ID 生成方案，设计用于替代 UUID 和其他传统 ID 格式。相比 UUID 和 NanoID，CUID2 具有更好的抗预测性和碰撞抵抗性。

### 特点

- ✅ **零外部依赖** - 仅使用 Python 标准库
- ✅ **安全可靠** - 使用 SHA3-256 哈希确保不可预测性
- ✅ **线程安全** - 支持多线程并发生成
- ✅ **可配置长度** - 支持 2-32 字符长度
- ✅ **多种变体** - 基础版、安全版、带前缀版
- ✅ **完整验证** - 支持 ID 格式验证和解析

### 与其他方案对比

| 特性 | CUID2 | UUID v4 | NanoID |
|------|--------|---------|--------|
| 安全性 | ✅ SHA3 哈希 | ❌ 随机 | ✅ 随机 |
| 抗预测 | ✅ 高 | ❌ 低 | ✅ 中 |
| 默认长度 | 24 | 36 | 21 |
| 碰撞抵抗 | ✅ 极高 | ✅ 高 | ✅ 高 |
| 线程安全 | ✅ | ✅ | ✅ |

## 安装

```python
# 无需安装，直接导入
from cuid2_utils import Cuid2, create_id
```

## 快速开始

### 基本 ID 生成

```python
from cuid2_utils import Cuid2

# 创建生成器
cuid = Cuid2()

# 生成 ID（默认 24 字符）
id1 = cuid.generate()
print(id1)  # 如: clh3am8ji0000358uht4dbq8c

# 自定义长度
id_short = cuid.generate(length=8)
id_long = cuid.generate(length=32)
```

### 快捷函数

```python
from cuid2_utils import create_id, create_id_batch, is_cuid2

# 快速生成
my_id = create_id()

# 批量生成
ids = create_id_batch(100)

# 验证
is_cuid2("clh3am8ji0000358uht4dbq8c")  # True
```

## API 文档

### Cuid2 类

主要 ID 生成器。

```python
Cuid2(length=24, fingerprint=None)
```

**参数：**
- `length`: ID 长度，范围 2-32，默认 24
- `fingerprint`: 可选的自定义指纹

**方法：**

| 方法 | 说明 |
|------|------|
| `generate(length=None)` | 生成单个 ID |
| `generate_batch(count, length=None)` | 批量生成 |
| `is_valid(id)` | 验证 ID 格式 |
| `get_info(id)` | 获取 ID 信息 |
| `fingerprint` | 获取/设置指纹 |

### SecureCuid2 类

更安全的变体，最小长度 16，默认 32。

```python
from cuid2_utils import SecureCuid2

secure = SecureCuid2()
secure_id = secure.generate()  # 32 字符
```

### PrefixedCuid2 类

带前缀的 ID 生成器。

```python
from cuid2_utils import PrefixedCuid2

user_gen = PrefixedCuid2(prefix="user")
user_id = user_gen.generate()  # user_clh3am8ji0000358uht4dbq8c

# 方法
user_gen.is_valid(user_id)      # True
user_gen.extract_prefix(user_id) # "user"
user_gen.extract_cuid(user_id)   # "clh3am8ji0000358uht4dbq8c"
```

### 快捷函数

| 函数 | 说明 |
|------|------|
| `create_id(length=24)` | 生成单个 ID |
| `create_id_batch(count, length=24)` | 批量生成 |
| `create_prefixed_id(prefix, length=24)` | 生成带前缀 ID |
| `is_cuid2(id)` | 验证 ID 格式 |

## 使用场景

### 数据库主键

```python
from cuid2_utils import PrefixedCuid2

user_gen = PrefixedCuid2(prefix="user")
order_gen = PrefixedCuid2(prefix="order")

# 创建用户记录
user = {
    "id": user_gen.generate(),
    "name": "张三",
    "email": "zhangsan@example.com"
}

# 创建订单记录
order = {
    "id": order_gen.generate(),
    "user_id": user["id"],
    "total": 99.99
}
```

### 分布式系统

```python
from cuid2_utils import Cuid2

# 每个服务器实例使用不同指纹
server_1 = Cuid2(fingerprint="server_1")
server_2 = Cuid2(fingerprint="server_2")

# 生成的 ID 包含实例标识
id1 = server_1.generate()
id2 = server_2.generate()
```

### 会话管理

```python
from cuid2_utils import create_prefixed_id

# 创建会话
session_id = create_prefixed_id("session")

# 创建令牌
token_id = create_prefixed_id("token")

# 创建追踪 ID
trace_id = create_prefixed_id("trace")
```

### URL 短链接

```python
from cuid2_utils import Cuid2

# 使用较短长度
cuid = Cuid2(length=8)
short_url_code = cuid.generate()  # 如: clh3am8j

# 组合成短链接
short_url = f"https://example.com/{short_url_code}"
```

## 性能

- 单次生成：~0.0001ms
- 批量生成 10000 个：< 5s
- 线程安全：支持多线程并发
- 碰撞概率：极低（安全哈希 + 时间戳 + 计数器）

## 测试

```bash
python Python/cuid2_utils/cuid2_utils_test.py
```

测试覆盖：
- ID 生成（单次、批量）
- 格式验证
- 唯一性保证
- 线程安全
- 边界值测试
- 性能测试

## 实现原理

CUID2 生成过程：

1. **时间戳** - 毫秒级时间戳，确保时序性
2. **计数器** - 同一毫秒内的序列号，确保唯一性
3. **随机数** - 8 字节随机数据，增加熵
4. **指纹** - 系统特征标识，区分不同实例
5. **SHA3 哈希** - 组合所有组件并哈希，确保不可预测性
6. **Base36 编码** - 输出为紧凑的 Base36 字符串

```
输入: timestamp + counter + random + fingerprint
输出: SHA3-256(输入) → Base36 → 截取指定长度
```

## 常见问题

### Q: CUID2 和 UUID 有什么区别？

A: CUID2 更短（默认 24 字符 vs UUID 的 36），更安全（SHA3 哈希），且更不易碰撞。

### Q: 可以从 CUID2 还原时间信息吗？

A: 不可以。CUID2 是哈希后的结果，无法还原原始时间戳。如果需要时间信息，请使用 UUIDv7。

### Q: 多线程环境下安全吗？

A: 是的。Cuid2 使用线程锁确保计数器的原子性操作。

## 许可证

MIT License

## 相关模块

- `uuid_utils` - UUID 生成
- `ulid_utils` - ULID 生成
- `nanoid_utils` - NanoID 生成
- `xid_utils` - XID 生成
- `snowflake_utils` - Snowflake ID 生成