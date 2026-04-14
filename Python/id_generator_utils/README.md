# ID Generator Utilities

分布式ID生成工具集，提供多种唯一标识符生成策略，零外部依赖。

## 功能特性

- **Snowflake ID** - Twitter雪花算法，分布式系统唯一ID
- **ULID** - 通用可排序词典ID
- **NanoID** - 小型、安全、URL友好的唯一字符串ID
- **ObjectId** - MongoDB风格的对象标识符
- **KSUID** - K-排序唯一标识符
- **CUID2** - 抗碰撞唯一标识符
- **TSID** - 时间排序ID
- **UUID** - UUID4和UUID7生成器
- **便捷函数** - 短ID、时间戳ID、序列ID等

## 快速开始

```python
from id_generator_utils import (
    SnowflakeGenerator,
    ULID,
    NanoID,
    ObjectId,
    short_id,
    timestamp_id,
    sequential_id,
)
```

### Snowflake ID

```python
from id_generator_utils import SnowflakeGenerator

# 创建生成器
gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)

# 生成ID
id1 = gen.generate()  # 1234567890123456789

# 批量生成
ids = gen.generate_batch(100)

# 解析ID
parsed = SnowflakeGenerator.parse(id1)
print(parsed['datetime'])  # 生成时间
print(parsed['worker_id'])  # 工作节点ID
```

### ULID

```python
from id_generator_utils import ULID

# 生成ULID
ulid = ULID.generate()  # '01ARZ3NDEKTSV4RRFFQ69G5FAV'

# 提取时间戳
timestamp = ULID.get_timestamp(ulid)

# 比较
ULID.compare(ulid1, ulid2)  # -1, 0, 1
```

### NanoID

```python
from id_generator_utils import NanoID

# 默认生成 (21字符)
id1 = NanoID.generate()  # 'V1StGXR8_Z5jdHi6B-myT'

# 自定义长度
id2 = NanoID.generate(length=10)

# 数字ID
num_id = NanoID.numeric(16)  # '4738924682123456'

# 无易混淆字符
safe_id = NanoID.no_lookalikes(20)  # 无 l1IO0

# URL安全
url_id = NanoID.url_safe(15)
```

### ObjectId

```python
from id_generator_utils import ObjectId

# 生成ObjectId
oid = ObjectId.generate()  # '507f1f77bcf86cd799439011'

# 验证
ObjectId.is_valid(oid)  # True

# 提取时间戳
timestamp = ObjectId.get_timestamp(oid)
```

### 便捷函数

```python
from id_generator_utils import short_id, timestamp_id, sequential_id

# 短ID
id1 = short_id(8)  # 'aB3x9KmP'

# 时间戳ID
id2 = timestamp_id('ORD')  # 'ORD1713076800000x7kP'

# 序列ID生成器
gen = sequential_id('ITEM', padding=6)
gen()  # 'ITEM000001'
gen()  # 'ITEM000002'
```

## 线程安全

所有生成器都是线程安全的，可在多线程环境中使用：

```python
import threading
from id_generator_utils import SnowflakeGenerator

gen = SnowflakeGenerator(worker_id=1)

def worker():
    for _ in range(1000):
        id = gen.generate()
        # 使用ID...

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
```

## 性能

典型性能（Python 3.x）：

| 生成器 | 速度 (ID/秒) |
|--------|-------------|
| SnowflakeGenerator | ~500,000+ |
| ULID | ~50,000+ |
| NanoID | ~100,000+ |
| ObjectId | ~50,000+ |

## API 参考

### SnowflakeGenerator

```python
SnowflakeGenerator(worker_id=0, datacenter_id=0, epoch=1704067200000)
.generate() -> int
.generate_batch(count) -> List[int]
.parse(id, epoch=None) -> dict
```

### ULID

```python
ULID.generate() -> str
ULID.get_timestamp(ulid) -> datetime
ULID.compare(ulid1, ulid2) -> int
```

### NanoID

```python
NanoID.generate(length=21, alphabet=None) -> str
NanoID.numeric(length=16) -> str
NanoID.lowercase(length=24) -> str
NanoID.no_lookalikes(length=24) -> str
NanoID.url_safe(length=21) -> str
```

### ObjectId

```python
ObjectId.generate() -> str
ObjectId.get_timestamp(oid) -> datetime
ObjectId.is_valid(oid) -> bool
```

### 其他函数

```python
short_id(length=8, alphabet=None) -> str
timestamp_id(prefix='', suffix='') -> str
sequential_id(prefix='', start=1, padding=0) -> Callable
prefixed_uuid(prefix, separator='_') -> str
ksuid(timestamp=None) -> str
cuid2(length=24) -> str
tsid(prefix='', node_id=0) -> str
analyze_id(id_string) -> dict
uuid4_str() -> str
uuid4_hex() -> str
uuid7_str() -> str
```

## 许可证

MIT License