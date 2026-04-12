# AllToolkit - Python Encryption Utils 🔐

**零依赖加密与安全工具 - 生产就绪**

---

## 📖 概述

`encryption_utils` 提供功能完整的加密和安全工具集，包括哈希、HMAC 签名、加密解密、安全随机数生成等。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **哈希函数** - SHA256/SHA512/MD5/BLAKE2 等多种算法
- **文件哈希** - 高效分块读取大文件
- **密码哈希** - PBKDF2 安全密码存储
- **HMAC 签名** - 消息认证码
- **XOR 加密** - 简单对称加密（教育用途）
- **替换密码** - 经典密码学教学
- **Base64 编码** - 标准及 URL 安全编码
- **令牌生成** - API 密钥、会话 ID、安全令牌
- **校验和** - CRC32/Adler32
- **一次一密** - 理论不可破解的 OTP
- **密钥派生** - PBKDF2 密钥生成
- **安全比较** - 防时序攻击比较
- **哈希链** - 数据完整性验证

---

## 🚀 快速开始

### 基础哈希

```python
from mod import hash_data, verify_hash, HashAlgorithm

# SHA256 哈希
result = hash_data("hello world")
print(result.hex_digest)

# 带盐哈希
result = hash_data("password", salt="random_salt")

# 验证哈希
is_valid = verify_hash("hello world", result.hex_digest)
```

### 文件哈希

```python
from mod import hash_file

result = hash_file("large_file.zip")
print(f"SHA256: {result.hex_digest}")
print(f"文件大小：{result.input_length} bytes")
```

### 密码哈希

```python
from mod import hash_password, verify_password

# 哈希密码
hashed = hash_password("my_secure_password")
# 返回：{'algorithm': 'pbkdf2_sha256', 'iterations': '100000', 'salt': '...', 'hash': '...'}

# 验证密码
is_valid = verify_password("my_secure_password", hashed)
```

### HMAC 签名

```python
from mod import compute_hmac, verify_hmac

# 计算签名
message = "Important message"
key = "secret_key"
signature = compute_hmac(message, key)

# 验证签名
is_valid = verify_hmac(message, signature, key)
```

### 令牌生成

```python
from mod import generate_token, generate_api_key, generate_session_id

# 安全令牌
token = generate_token(length=32)

# URL 安全令牌
token = generate_token(url_safe=True)

# API 密钥
api_key = generate_api_key(prefix="sk")  # sk_xxxxxxxxx

# 会话 ID
session_id = generate_session_id()
```

---

## 📚 API 参考

### 哈希函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `hash_data(data, algorithm, salt)` | 哈希数据 | `HashResult` |
| `hash_file(filepath, algorithm)` | 哈希文件 | `HashResult` |
| `verify_hash(data, expected, algorithm, salt)` | 验证哈希 | `bool` |
| `hash_password(password, salt, iterations)` | 哈希密码 | `Dict` |
| `verify_password(password, stored_hash)` | 验证密码 | `bool` |

### HashResult 类

| 属性 | 描述 |
|------|------|
| `algorithm` | 使用的算法 |
| `hex_digest` | 十六进制哈希值 |
| `bytes_digest` | 字节哈希值 |
| `input_length` | 输入数据长度 |
| `timestamp` | 哈希时间戳 |

| 方法 | 描述 |
|------|------|
| `verify(data)` | 验证数据是否匹配 |
| `to_dict()` | 导出为字典 |

### HMAC 函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `compute_hmac(data, key, algorithm)` | 计算 HMAC | `str` |
| `verify_hmac(data, signature, key, algorithm)` | 验证 HMAC | `bool` |

### 加密函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `xor_encrypt(data, key)` | XOR 加密 | `bytes` |
| `xor_decrypt(encrypted, key)` | XOR 解密 | `bytes` |
| `otp_encrypt(data, otp)` | OTP 加密 | `bytes` |
| `otp_decrypt(encrypted, otp)` | OTP 解密 | `bytes` |
| `generate_otp(length)` | 生成 OTP | `bytes` |

### Base64 函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `base64_encode(data)` | Base64 编码 | `str` |
| `base64_decode(encoded)` | Base64 解码 | `bytes` |
| `url_safe_encode(data)` | URL 安全编码 | `str` |
| `url_safe_decode(encoded)` | URL 安全解码 | `bytes` |

### 令牌生成

| 函数 | 描述 | 返回 |
|------|------|------|
| `generate_token(length, url_safe, include_timestamp)` | 生成令牌 | `str` |
| `generate_api_key(prefix)` | 生成 API 密钥 | `str` |
| `generate_session_id()` | 生成会话 ID | `str` |

### 校验和

| 函数 | 描述 | 返回 |
|------|------|------|
| `compute_checksum(data, algorithm)` | 计算校验和 | `int` |
| `verify_checksum(data, expected, algorithm)` | 验证校验和 | `bool` |

### 密钥派生

| 函数 | 描述 | 返回 |
|------|------|------|
| `derive_key(password, salt, length, algorithm, iterations)` | 派生密钥 | `Tuple[bytes, bytes]` |

### 安全比较

| 函数 | 描述 | 返回 |
|------|------|------|
| `secure_compare(a, b)` | 防时序攻击比较 | `bool` |

### 工具类

#### SubstitutionCipher

```python
cipher = SubstitutionCipher(key="mykey")
encrypted = cipher.encrypt("hello")
decrypted = cipher.decrypt(encrypted)
```

#### SecureString

```python
with SecureString("secret") as ss:
    value = ss.get()
# 自动清除
```

#### HashChain

```python
chain = HashChain()
chain.add("doc1").add("doc2").add("doc3")
final_hash = chain.get_chain_hash()
is_valid = chain.verify(["doc1", "doc2", "doc3"], final_hash)
```

---

## 🎯 使用场景

### 1. 用户认证系统

```python
from mod import hash_password, verify_password, generate_session_id

class AuthService:
    def __init__(self):
        self.sessions = {}
    
    def register(self, username, password):
        # 哈希密码存储
        hashed = hash_password(password)
        # 存储 username -> hashed
    
    def login(self, username, password, stored_hash):
        if verify_password(password, stored_hash):
            session_id = generate_session_id()
            self.sessions[session_id] = username
            return session_id
        return None
    
    def logout(self, session_id):
        self.sessions.pop(session_id, None)
```

### 2. API 请求签名

```python
from mod import compute_hmac, verify_hmac, generate_api_key

class APISecurity:
    def __init__(self):
        self.api_keys = {}  # key_id -> secret
    
    def create_key(self, user_id):
        key_id = generate_api_key(prefix="ak")
        secret = generate_token()
        self.api_keys[key_id] = secret
        return key_id, secret
    
    def sign_request(self, method, path, body, secret):
        message = f"{method}:{path}:{body}"
        return compute_hmac(message, secret)
    
    def verify_request(self, method, path, body, key_id, signature):
        secret = self.api_keys.get(key_id)
        if not secret:
            return False
        message = f"{method}:{path}:{body}"
        return verify_hmac(message, signature, secret)
```

### 3. 文件完整性验证

```python
from mod import hash_file, verify_hash, HashChain

class FileIntegrity:
    def __init__(self):
        self.hashes = {}
    
    def register_file(self, filepath, name):
        result = hash_file(filepath)
        self.hashes[name] = result.hex_digest
        return result.hex_digest
    
    def verify_file(self, filepath, expected_hash):
        result = hash_file(filepath)
        return verify_hash(result.bytes_digest, expected_hash)
    
    def create_manifest(self, files):
        """创建文件清单哈希链"""
        chain = HashChain()
        for filepath in files:
            h = hash_file(filepath)
            chain.add(h.hex_digest)
        return chain.get_chain_hash()
```

### 4. 安全令牌服务

```python
from mod import generate_token, generate_session_id, url_safe_encode
import time
import struct

class TokenService:
    def generate_refresh_token(self, user_id):
        """生成刷新令牌"""
        timestamp = struct.pack('>Q', int(time.time() * 1000))
        user_bytes = str(user_id).encode()
        random = generate_token(length=24, url_safe=True).encode()
        
        token_data = timestamp + user_bytes + random
        return url_safe_encode(token_data)
    
    def generate_csrf_token(self):
        """生成 CSRF 令牌"""
        return generate_token(url_safe=True)
    
    def generate_verification_code(self, length=6):
        """生成验证码"""
        import secrets
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
```

### 5. 数据完整性链

```python
from mod import HashChain

class AuditLog:
    def __init__(self):
        self.chain = HashChain()
    
    def log(self, event):
        """添加审计日志"""
        self.chain.add(event)
    
    def get_fingerprint(self):
        """获取当前指纹"""
        return self.chain.get_chain_hash()
    
    def verify_integrity(self, events, expected_fingerprint):
        """验证日志完整性"""
        return self.chain.verify(events, expected_fingerprint)
```

### 6. 安全配置存储

```python
from mod import SecureString, derive_key, xor_encrypt, base64_encode

class SecureConfig:
    def __init__(self, master_password):
        key, _ = derive_key(master_password)
        self._key = key
    
    def encrypt_value(self, value):
        """加密配置值"""
        with SecureString(value) as vs:
            encrypted = xor_encrypt(vs.get(), self._key)
            return base64_encode(encrypted)
    
    def decrypt_value(self, encrypted, key):
        """解密配置值"""
        from mod import base64_decode, xor_decrypt
        data = base64_decode(encrypted)
        return xor_decrypt(data, key)
```

---

## 🧪 运行测试

```bash
cd encryption_utils
python encryption_utils_test.py -v
```

### 测试覆盖

- ✅ 哈希函数（多算法）
- ✅ 文件哈希
- ✅ 密码哈希与验证
- ✅ HMAC 签名与验证
- ✅ XOR 加密解密
- ✅ 替换密码
- ✅ Base64 编码解码
- ✅ URL 安全编码
- ✅ 令牌生成
- ✅ API 密钥生成
- ✅ 会话 ID 生成
- ✅ 校验和（CRC32/Adler32）
- ✅ OTP 加密
- ✅ 安全比较
- ✅ 密钥派生
- ✅ SecureString
- ✅ HashChain
- ✅ 边界情况
- ✅ 集成测试

---

## ⚠️ 安全注意事项

### ⚠️ 生产环境建议

1. **XOR 加密仅用于教育** - 不适用于生产环境的安全需求
2. **替换密码仅用于教学** - 容易被频率分析破解
3. **密码存储** - 使用 `hash_password`（PBKDF2）而非简单哈希
4. **密钥管理** - 安全存储密钥，不要硬编码
5. **传输安全** - 始终使用 HTTPS 传输敏感数据

### ✅ 推荐用于生产

- ✅ SHA256/SHA512 哈希
- ✅ PBKDF2 密码哈希
- ✅ HMAC 消息认证
- ✅ 安全令牌生成
- ✅ 安全比较（防时序攻击）
- ✅ 密钥派生

### ❌ 仅用于学习

- ❌ XOR 加密（无安全性）
- ❌ 替换密码（易破解）

对于生产加密，建议使用 `cryptography` 库的 Fernet 或 AES。

---

## 🔧 配置选项

### 哈希算法

```python
from mod import HashAlgorithm

algorithms = [
    HashAlgorithm.MD5,        # 128 位（不推荐用于安全）
    HashAlgorithm.SHA1,       # 160 位（不推荐用于安全）
    HashAlgorithm.SHA256,     # 256 位（推荐）
    HashAlgorithm.SHA384,     # 384 位
    HashAlgorithm.SHA512,     # 512 位
    HashAlgorithm.SHA3_256,   # SHA3 256 位
    HashAlgorithm.SHA3_512,   # SHA3 512 位
    HashAlgorithm.BLAKE2B,    # BLAKE2b
    HashAlgorithm.BLAKE2S,    # BLAKE2s
]
```

### 密码哈希参数

```python
# 增加迭代次数提高安全性（但更慢）
hashed = hash_password("password", iterations=200000)

# 自定义盐
import secrets
salt = secrets.token_bytes(32)
hashed = hash_password("password", salt=salt)
```

---

## 📊 性能提示

### 大文件哈希

```python
# 调整块大小优化性能
result = hash_file("large_file.iso", chunk_size=1048576)  # 1MB 块
```

### 批量操作

```python
# 使用 HashChain 比单独哈希更高效
chain = HashChain()
for item in items:
    chain.add(item)
```

---

## 📁 文件结构

```
encryption_utils/
├── mod.py                          # 主要实现
├── encryption_utils_test.py        # 测试套件 (80+ 测试用例)
├── README.md                       # 本文档
└── examples/
    ├── basic_usage.py              # 基础使用示例
    └── advanced_example.py         # 高级使用示例
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
