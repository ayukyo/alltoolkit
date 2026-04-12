# UUID Utilities - AllToolkit

**零依赖 UUID 生成与操作工具 - 生产就绪**

---

## 📦 功能特性

- ✅ **UUID v1 生成** - 基于时间的 UUID（可排序）
- ✅ **UUID v3 生成** - 基于 MD5 命名空间（确定性）
- ✅ **UUID v4 生成** - 随机 UUID（最常用）
- ✅ **UUID v5 生成** - 基于 SHA-1 命名空间（推荐用于确定性 UUID）
- ✅ **UUID 验证** - 支持多种格式（标准/带括号/URN/无连字符）
- ✅ **格式转换** - 字符串/字节/整数互相转换
- ✅ **UUID 比较** - 排序、比较、去重
- ✅ **时间戳提取** - 从 v1 UUID 提取创建时间
- ✅ **节点提取** - 从 v1 UUID 提取 MAC 地址
- ✅ **批量生成** - 一次性生成多个 UUID
- ✅ **自定义哈希 UUID** - 使用任意数据生成确定性 UUID
- ✅ **Nil UUID** - 全零 UUID 处理

---

## 🚀 快速开始

### 基本使用

```python
from mod import UUIDUtils, generate_v4, is_valid, parse

# 生成随机 UUID (v4)
uuid_obj = generate_v4()
print(uuid_obj)  # e.g., 550e8400-e29b-41d4-a716-446655440000

# 验证 UUID 字符串
is_valid('550e8400-e29b-41d4-a716-446655440000')  # True
is_valid('not-a-uuid')  # False

# 解析 UUID 字符串
uuid_obj = parse('550e8400-e29b-41d4-a716-446655440000')
```

### 生成不同类型的 UUID

```python
from mod import generate_v1, generate_v3, generate_v4, generate_v5
from mod import UUIDUtils

# v1 - 基于时间（可排序，揭示创建顺序）
u1 = generate_v1()
print(f"v1: {u1}, 版本：{u1.version}")

# v3 - 基于 MD5 命名空间（确定性）
u3 = generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
print(f"v3: {u3}")

# v4 - 随机（最常用）
u4 = generate_v4()
print(f"v4: {u4}")

# v5 - 基于 SHA-1 命名空间（推荐用于确定性 UUID）
u5 = generate_v5(UUIDUtils.NAMESPACE_DNS, 'example.com')
print(f"v5: {u5}")

# 验证确定性：相同输入产生相同输出
u3_again = generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
assert u3 == u3_again  # True!
```

---

## 📖 API 参考

### 生成函数

#### `generate_v1()` → `uuid.UUID`
生成基于时间的 UUID v1。

```python
u = generate_v1()
timestamp = UUIDUtils.get_timestamp(u)  # 可提取时间戳
```

#### `generate_v3(namespace, name)` → `uuid.UUID`
生成基于 MD5 命名空间的 UUID v3。

```python
# 使用预定义命名空间
u = generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')

# 或使用字符串别名
u = generate_v3('dns', 'example.com')
u = generate_v3('url', 'https://example.com')
u = generate_v3('oid', '1.2.3.4')
u = generate_v3('x500', 'CN=John Doe')
```

#### `generate_v4()` → `uuid.UUID`
生成随机 UUID v4。

```python
u = generate_v4()
# 碰撞概率：约 1/(2^122) ≈ 1/5.3×10^36
```

#### `generate_v5(namespace, name)` → `uuid.UUID`
生成基于 SHA-1 命名空间的 UUID v5。

```python
# 推荐用于需要确定性 UUID 的场景
u = generate_v5(UUIDUtils.NAMESPACE_URL, 'https://example.com/user/123')
```

#### `generate_batch(count, version)` → `List[uuid.UUID]`
批量生成 UUID。

```python
uuids = generate_batch(100, version=4)  # 生成 100 个 v4 UUID
```

#### `hash_to_uuid(data, algorithm)` → `uuid.UUID`
从任意数据生成确定性 UUID。

```python
# 使用用户 ID 生成唯一 UUID
user_uuid = hash_to_uuid('user_12345', 'sha256')

# 支持多种哈希算法
uuid_md5 = hash_to_uuid('data', 'md5')
uuid_sha1 = hash_to_uuid('data', 'sha1')
uuid_sha256 = hash_to_uuid('data', 'sha256')
uuid_sha512 = hash_to_uuid('data', 'sha512')
```

---

### 验证与解析

#### `is_valid(uuid_string)` → `bool`
验证字符串是否为有效 UUID。

```python
is_valid('550e8400-e29b-41d4-a716-446655440000')  # True
is_valid('{550e8400-e29b-41d4-a716-446655440000}')  # True (带括号)
is_valid('urn:uuid:550e8400-e29b-41d4-a716-446655440000')  # True (URN)
is_valid('550e8400e29b41d4a716446655440000')  # True (无连字符)
is_valid('invalid')  # False
```

#### `is_valid_fast(uuid_string)` → `bool`
快速验证（使用正则，不验证版本/变体）。

```python
# 比 is_valid() 快约 10 倍，适合批量验证
is_valid_fast('550e8400-e29b-41d4-a716-446655440000')  # True
```

#### `parse(uuid_string)` → `uuid.UUID`
解析 UUID 字符串。

```python
u = parse('550e8400-e29b-41d4-a716-446655440000')
```

---

### 转换函数

#### `to_string(uuid_obj, format)` → `str`
转换为不同格式的字符串。

```python
u = parse('550e8400-e29b-41d4-a716-446655440000')

to_string(u, 'standard')   # '550e8400-e29b-41d4-a716-446655440000'
to_string(u, 'braced')     # '{550e8400-e29b-41d4-a716-446655440000}'
to_string(u, 'urn')        # 'urn:uuid:550e8400-e29b-41d4-a716-446655440000'
to_string(u, 'no-hyphen')  # '550e8400e29b41d4a716446655440000'
to_string(u, 'upper')      # '550E8400-E29B-41D4-A716-446655440000'
```

#### `to_bytes(uuid_obj)` → `bytes`
转换为 16 字节。

```python
b = to_bytes(u)  # b'U\x0e\x84\x00\xe2\x9bA\xd4\xa7\x16DfUD\x00'
```

#### `from_bytes(data)` → `uuid.UUID`
从 16 字节创建 UUID。

```python
u = from_bytes(b'U\x0e\x84\x00\xe2\x9bA\xd4\xa7\x16DfUD\x00')
```

#### `to_int(uuid_obj)` → `int`
转换为 128 位整数。

```python
i = to_int(u)  # 113487710670637795159710968403718799360
```

#### `from_int(value)` → `uuid.UUID`
从整数创建 UUID。

```python
u = from_int(113487710670637795159710968403718799360)
```

---

### 比较与排序

#### `compare(uuid1, uuid2)` → `int`
比较两个 UUID。

```python
compare(u1, u2)  # -1 (u1 < u2), 0 (相等), 1 (u1 > u2)
```

#### `equal(uuid1, uuid2)` → `bool`
检查是否相等。

```python
equal(u1, u2)  # True/False
```

#### `sort(uuid_list, reverse)` → `List[uuid.UUID]`
排序 UUID 列表。

```python
uuids = ['0001...', '0000...', '0002...']
sorted_uuids = sort(uuids)  # 升序
sorted_uuids = sort(uuids, reverse=True)  # 降序
```

---

### UUID v1 专用

#### `get_timestamp(uuid_obj)` → `datetime`
从 v1 UUID 提取时间戳。

```python
u = generate_v1()
ts = get_timestamp(u)
print(f"创建时间：{ts}")
```

#### `get_node(uuid_obj)` → `int`
从 v1 UUID 提取节点（MAC 地址）。

```python
u = generate_v1()
node = get_node(u)
print(f"节点 ID: {node:012x}")  # 格式化为 MAC 地址
```

---

### 其他工具

#### `get_version(uuid_obj)` → `int`
获取 UUID 版本。

```python
get_version(generate_v4())  # 4
```

#### `get_variant(uuid_obj)` → `str`
获取 UUID 变体。

```python
get_variant(generate_v4())  # 'RFC 4122'
```

#### `nil()` → `uuid.UUID`
获取全零 UUID。

```python
nil_uuid = nil()  # 00000000-0000-0000-0000-000000000000
is_nil(nil_uuid)  # True
```

---

## 💡 使用场景

### 1. 数据库主键

```python
# 使用 v4 作为随机主键
user_id = generate_v4()

# 或使用 v1 保持插入顺序
order_id = generate_v1()
```

### 2. 分布式 ID 生成

```python
# 使用 v1 UUID，不同节点生成的 ID 可排序
request_id = generate_v1()
```

### 3. 确定性 ID（缓存键、分片键）

```python
# 相同用户总是得到相同 UUID
user_uuid = generate_v5(UUIDUtils.NAMESPACE_DNS, f'user:{user_id}')

# 用于一致性哈希分片
shard_key = hash_to_uuid(f'shard:{user_id}')
```

### 4. URL 安全标识符

```python
# 生成无连字符的 UUID
short_id = to_string(generate_v4(), 'no-hyphen')
# 用于短链接：example.com/s/550e8400e29b41d4a716446655440000
```

### 5. 批量数据导入

```python
# 为 10000 条记录生成唯一 ID
ids = generate_batch(10000, version=4)
```

### 6. API 令牌生成

```python
# 使用用户信息生成确定性 API 令牌
api_token = hash_to_uuid(f'{user_id}:{secret}', 'sha256')
```

---

## 🧪 运行测试

```bash
cd uuid_utils
python uuid_utils_test.py
```

测试覆盖：
- ✅ UUID v1/v3/v4/v5 生成
- ✅ 确定性验证（相同输入=相同输出）
- ✅ 多格式解析与验证
- ✅ 字符串/字节/整数转换
- ✅ 比较与排序
- ✅ v1 时间戳和节点提取
- ✅ 批量生成
- ✅ Nil UUID 处理
- ✅ 哈希到 UUID 转换
- ✅ 边界情况和错误处理

---

## 📊 性能提示

1. **批量验证**：使用 `is_valid_fast()` 比 `is_valid()` 快约 10 倍
2. **v4 vs v1**：v4 生成略快于 v1（无需获取 MAC 地址和时间）
3. **确定性 UUID**：v5 比 v3 更安全（SHA-1 vs MD5），性能差异可忽略
4. **批量生成**：`generate_batch()` 比循环调用单个生成函数略快

---

## 🔒 安全注意事项

1. **v4 UUID**：使用系统随机数生成器，适合安全敏感场景
2. **v1 UUID**：可能泄露 MAC 地址和时间信息，隐私敏感场景慎用
3. **确定性 UUID**：v3/v5 适合公开数据，但输入应具有足够熵
4. **自定义哈希**：`hash_to_uuid()` 使用 SHA-256 默认，适合密钥派生

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
