# Secrets Utilities Module

安全密钥管理工具函数库，提供密码生成、API 密钥、TOTP 等完整功能。

## 功能特性

- 🔐 **密码生成** - 可定制复杂度的安全密码
- 📝 **短语生成** - 易记的安全 passphrase
- 🔑 **API 密钥** - 带前缀的 API key 和 bearer token
- 💪 **强度评估** - 密码强度评分和建议
- 🔒 **安全哈希** - PBKDF2 密钥哈希和验证
- ⏱️ **TOTP** - 双因素认证验证码生成
- 🎲 **安全随机** - 加密级随机数生成
- 🛡️ **工具函数** - 密钥掩码、常量比较等

## 快速开始

### 生成密码

```python
from secrets_utils.mod import generate_password, generate_passphrase

# 生成 16 位强密码
password = generate_password(length=16)
# 输出示例：Kx9#mP2$nQ7@wL5!

# 生成易记短语
passphrase = generate_passphrase(word_count=4)
# 输出示例：correct-horse-battery-staple

# 排除易混淆字符
password = generate_password(exclude_ambiguous=True)
# 不包含 l, 1, I, O, 0 等
```

### API 密钥生成

```python
from secrets_utils.mod import generate_api_key, generate_bearer_token, generate_session_id

# API 密钥
api_key = generate_api_key(prefix='ak')
# 输出：ak_7Fz9Kx2mPq5Nw8Rt3Yv6Bc1Df4Gh7Jk0

# Secret Key
secret_key = generate_api_key(prefix='sk', length=24)

# Bearer Token
token = generate_bearer_token()

# Session ID
session_id = generate_session_id(prefix='sess')
```

### 密码强度评估

```python
from secrets_utils.mod import evaluate_password_strength, is_password_strong

# 评估密码强度
score, strength, suggestions = evaluate_password_strength("MyStr0ng!Pass")
print(f"Score: {score}/100")      # Score: 85/100
print(f"Strength: {strength}")    # Strength: Strong
print(f"Suggestions: {suggestions}")

# 快速判断
is_password_strong("weak")        # False
is_password_strong("Str0ng!Pass#2024")  # True
```

### 密钥哈希与验证

```python
from secrets_utils.mod import hash_secret, verify_secret

# 哈希密码
hashed = hash_secret("my_password")
# 输出：sha256:100000:abc123...:xyz789...

# 验证密码
verify_secret("my_password", hashed)    # True
verify_secret("wrong", hashed)          # False

# 使用 SHA512
hashed = hash_secret("password", algorithm='sha512')

# 自定义迭代次数
hashed = hash_secret("password", iterations=200000)
```

### TOTP 双因素认证

```python
from secrets_utils.mod import generate_totp_secret, generate_totp, verify_totp

# 生成新密钥
secret = generate_totp_secret()
# 输出：JBSWY3DPEHPK3PXP (Base32 编码)

# 生成验证码
code = generate_totp(secret)
# 输出：123456

# 验证验证码
verify_totp(secret, code)       # True
verify_totp(secret, "000000")   # False

# 带时间窗口验证（允许前后 1 个时间步）
verify_totp(secret, code, window=1)
```

### 安全随机工具

```python
from secrets_utils.mod import (
    secure_random_int,
    secure_random_bytes,
    secure_random_hex,
    secure_shuffle,
    secure_choice,
)

# 随机整数
num = secure_random_int(1, 100)

# 随机字节
data = secure_random_bytes(32)

# 随机十六进制
hex_str = secure_random_hex(64)

# 安全打乱
shuffled = secure_shuffle([1, 2, 3, 4, 5])

# 安全选择
item = secure_choice(['red', 'green', 'blue'])
```

### 工具函数

```python
from secrets_utils.mod import mask_secret, compare_secrets, is_secure_string

# 掩码显示（用于日志）
mask_secret("sk-1234567890abcdef")
# 输出：sk-1************cdef

# 常量时间比较（防时序攻击）
compare_secrets("secret1", "secret1")  # True
compare_secrets("secret1", "secret2")  # False

# 检查字符串安全性
is_secure_string("Abc123Def")   # True
is_secure_string("weak")        # False
```

## CLI 使用

```bash
# 生成密码
python mod.py --password --length 20

# 生成短语
python mod.py --passphrase --words 5

# 生成 API 密钥
python mod.py --api-key

# 生成 TOTP 密钥
python mod.py --totp-secret

# 哈希密码
python mod.py --hash "my_password"

# 验证密码
python mod.py --verify "my_password" "sha256:100000:salt:hash"

# 评估强度
python mod.py --strength "MyPassword123!"
```

## API 参考

### 密码生成

| 函数 | 描述 |
|------|------|
| `generate_password(length=16, ...)` | 生成指定长度的安全密码 |
| `generate_passphrase(word_count=4, ...)` | 生成易记的单词短语 |

### API 密钥

| 函数 | 描述 |
|------|------|
| `generate_api_key(prefix='ak', length=32)` | 生成带前缀的 API 密钥 |
| `generate_bearer_token(length=64)` | 生成 bearer token |
| `generate_session_id(prefix='sess')` | 生成 session ID |

### 密码强度

| 函数 | 描述 |
|------|------|
| `evaluate_password_strength(password)` | 评估密码强度 (0-100 分) |
| `is_password_strong(password, min_score=70)` | 判断是否达到强度要求 |

### 哈希验证

| 函数 | 描述 |
|------|------|
| `hash_secret(secret, algorithm='sha256', ...)` | PBKDF2 哈希 |
| `verify_secret(secret, hashed)` | 验证密钥 |

### TOTP

| 函数 | 描述 |
|------|------|
| `generate_totp_secret()` | 生成 TOTP 密钥 |
| `generate_totp(secret, digits=6)` | 生成验证码 |
| `verify_totp(secret, code, window=1)` | 验证验证码 |

### 安全随机

| 函数 | 描述 |
|------|------|
| `secure_random_int(min, max)` | 范围内随机整数 |
| `secure_random_bytes(length)` | 随机字节 |
| `secure_random_hex(length)` | 随机十六进制 |
| `secure_shuffle(items)` | 安全打乱列表 |
| `secure_choice(items)` | 安全选择 |

### 工具

| 函数 | 描述 |
|------|------|
| `mask_secret(secret, visible_chars=4)` | 掩码显示 |
| `compare_secrets(a, b)` | 常量时间比较 |
| `is_secure_string(s, min_length=8)` | 检查安全性 |
| `store_secret_env(name, value)` | 存入环境变量 |
| `get_secret_env(name, default)` | 从环境变量获取 |

## 安全建议

1. **密码长度**: 至少 12 位，推荐 16 位以上
2. **字符多样性**: 包含大小写、数字、特殊字符
3. **避免模式**: 不使用常见单词、日期、序列
4. **定期更换**: 重要账户定期更新密码
5. **使用短语**: 长 passphrase 比短密码更安全易记
6. **启用 2FA**: 重要账户开启双因素认证
7. **安全存储**: 使用密码管理器，不要明文存储

## 测试

```bash
cd /home/admin/.openclaw/workspace/AllToolkit/Python/secrets_utils
python secrets_utils_test.py
```

## 依赖

- Python 3.7+
- 零外部依赖（仅使用标准库）

## 许可证

MIT License
