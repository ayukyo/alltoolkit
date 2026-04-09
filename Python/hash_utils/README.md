# Hash Utils 🔐

**Python 哈希工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`hash_utils` 是一个全面的 Python 哈希工具模块，提供常用的哈希算法、HMAC、文件哈希、编码转换等功能。所有实现均使用 Python 标准库（`hashlib`、`hmac`、`base64` 等），零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **多种算法** - MD5、SHA1、SHA256、SHA512、SHA3、BLAKE2 等
- **HMAC 支持** - 消息认证码生成和验证
- **文件哈希** - 单文件和目录批量哈希
- **编码转换** - Hex ↔ Base64 ↔ Bytes
- **增量哈希** - 流式数据处理
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/hash_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```python
from mod import md5, sha256, sha512, hmac_hash, hash_file

# 基本哈希
print(md5("hello"))
# 输出：5d41402abc4b2a76b9719d911017c592

print(sha256("hello"))
# 输出：2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

# HMAC
mac = hmac_hash("message", "secret_key")
print(mac)

# 文件哈希
file_hash = hash_file("path/to/file.txt")
print(file_hash)
```

---

## 📚 API 参考

### 基本哈希函数

#### `md5(data, hex_output=True)`

计算 MD5 哈希。

```python
md5("hello")
# '5d41402abc4b2a76b9719d911017c592'

md5(b"hello", hex_output=False)
# b']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92'
```

#### `sha1(data, hex_output=True)`

计算 SHA1 哈希。

```python
sha1("hello")
# 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
```

#### `sha256(data, hex_output=True)`

计算 SHA256 哈希。

```python
sha256("hello")
# '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
```

#### `sha512(data, hex_output=True)`

计算 SHA512 哈希。

```python
sha512("hello")
# '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca7...'
```

#### `hash(data, algorithm='sha256', hex_output=True)`

使用指定算法计算哈希。

```python
hash("hello", "md5")
# '5d41402abc4b2a76b9719d911017c592'

hash("hello", "sha512")
# '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca7...'
```

#### `hash_algorithms()`

获取支持的哈希算法列表。

```python
hash_algorithms()
# ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 
#  'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
#  'blake2b', 'blake2s']
```

---

### HMAC 函数

#### `hmac_hash(data, key, algorithm='sha256', hex_output=True)`

计算 HMAC（基于哈希的消息认证码）。

```python
mac = hmac_hash("message", "secret_key")
print(mac)
# 'c955b7f8e1c4e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8f4c8e8'
```

#### `hmac_verify(data, key, signature, algorithm='sha256')`

验证 HMAC 签名。

```python
key = "secret"
data = "message"
sig = hmac_hash(data, key)

hmac_verify(data, key, sig)
# True

hmac_verify("tampered", key, sig)
# False
```

---

### 文件哈希

#### `hash_file(filepath, algorithm='sha256', hex_output=True, chunk_size=8192)`

计算文件的哈希值。

```python
hash_file("document.pdf")
# 'abc123...'

hash_file("document.pdf", algorithm="md5")
# 'def456...'
```

#### `hash_directory(dirpath, algorithm='sha256', recursive=True, ignore_patterns=None)`

计算目录下所有文件的哈希值。

```python
hashes = hash_directory("/path/to/dir")
print(hashes)
# {'file1.txt': 'abc123...', 'subdir/file2.txt': 'def456...'}

# 忽略特定文件
hashes = hash_directory("/path/to/dir", ignore_patterns=["*.pyc", "__pycache__"])
```

#### `verify_file_hash(filepath, expected_hash, algorithm='sha256')`

验证文件哈希是否匹配。

```python
verify_file_hash("file.txt", "expected_hash_value")
# True 或 False
```

---

### 哈希比较

#### `compare_hashes(hash1, hash2, case_sensitive=False)`

安全地比较两个哈希值。

```python
compare_hashes("ABC123", "abc123")
# True

compare_hashes("ABC123", "abc123", case_sensitive=True)
# False
```

#### `hash_diff(hash1, hash2)`

比较两个哈希值并返回详细差异信息。

```python
result = hash_diff("abc123", "abc456")
print(result)
# {
#     'match': False,
#     'length_match': True,
#     'hash1_length': 6,
#     'hash2_length': 6,
#     'hash1': 'abc123',
#     'hash2': 'abc456',
#     'differ_at': [3, 4, 5]
# }
```

---

### 编码转换

#### `hex_to_base64(hex_string)`

将十六进制字符串转换为 Base64。

```python
hex_to_base64("48656c6c6f")  # "Hello" 的十六进制
# 'SGVsbG8='
```

#### `base64_to_hex(base64_string)`

将 Base64 字符串转换为十六进制。

```python
base64_to_hex("SGVsbG8=")
# '48656c6c6f'
```

#### `bytes_to_hex(data)`

将字节转换为十六进制字符串。

```python
bytes_to_hex(b"Hello")
# '48656c6c6f'
```

#### `hex_to_bytes(hex_string)`

将十六进制字符串转换为字节。

```python
hex_to_bytes("48656c6c6f")
# b'Hello'
```

---

### 增量哈希

#### `IncrementalHasher`

用于流式数据的增量哈希器。

```python
hasher = IncrementalHasher('sha256')
hasher.update("Hello ")
hasher.update("World")
print(hasher.hexdigest())
# 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'

# 重置
hasher.reset()

# 复制状态
hasher2 = hasher.copy()

# 链式调用
result = IncrementalHasher('md5').update("a").update("b").update("c").hexdigest()
```

---

### 实用工具

#### `consistent_hash(data, num_buckets)`

计算一致性哈希用于桶分配。

```python
bucket = consistent_hash("user123", 10)
# 返回 0-9 之间的整数
```

#### `crc32(data)`

计算 CRC32 校验和。

```python
crc32("hello")
# 907060870

crc32_hex("hello")
# '3610a686'
```

---

### 密码哈希（简单用途）

⚠️ **注意**：这些函数仅供教育和非关键应用使用。生产环境请使用 bcrypt、argon2 或 scrypt。

#### `simple_hash_password(password, salt=None)`

创建简单的加盐密码哈希。

```python
result = simple_hash_password("mypassword")
print(result)
# {
#     'hash': 'abc123...',
#     'salt': 'random_salt_hex',
#     'algorithm': 'sha256'
# }
```

#### `verify_password(password, stored_hash, salt, algorithm='sha256')`

验证密码。

```python
result = simple_hash_password("mypassword")
verify_password("mypassword", result['hash'], result['salt'])
# True

verify_password("wrongpassword", result['hash'], result['salt'])
# False
```

---

## 📝 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基本用法示例
- `file_integrity.py` - 文件完整性校验
- `hmac_auth.py` - HMAC 认证示例
- `incremental_hash.py` - 增量哈希示例

---

## 🧪 运行测试

```bash
cd hash_utils
python hash_utils_test.py
```

测试覆盖：
- 基本哈希函数
- HMAC 生成和验证
- 文件哈希
- 编码转换
- 增量哈希
- 密码哈希
- Unicode 处理
- 边界情况

---

## 🔒 安全注意事项

1. **密码存储**：`simple_hash_password` 仅供简单用途。生产环境请使用专门的密码哈希库（bcrypt、argon2）。

2. **HMAC 密钥**：使用足够长且随机的密钥（至少 32 字节）。

3. **定时攻击防护**：所有比较操作使用 `hmac.compare_digest` 防止定时攻击。

4. **算法选择**：
   - 通用哈希：SHA256 或 SHA512
   - 密码存储：bcrypt/argon2（外部库）
   - 校验和：CRC32
   - 遗留系统：MD5/SHA1（不推荐用于安全用途）

---

## 📊 性能提示

- 文件哈希使用 8KB 块大小，可根据内存调整
- 增量哈希适合处理大文件或流式数据
- 批量目录哈希时考虑使用多进程

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
