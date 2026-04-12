# Password Utils 🔐

**Python 密码安全工具库**

零依赖、生产就绪的密码生成、强度分析、验证和安全哈希工具。

---

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **安全生成** - 使用 `secrets` 模块进行密码学安全随机数生成
- **强度分析** - 计算熵值、字符多样性、检测常见模式
- **全面验证** - 检查长度、字符类型、常见密码、序列模式
- **安全哈希** - PBKDF2 密钥派生，支持多种算法
- **泄露检测** - 本地常见密码库检测
- **破解时间估算** - 基于熵值估算暴力破解时间
- **助记符短语** - 生成易记的安全密码短语

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Python/password_utils
```

---

## 🚀 快速开始

### 基本使用

```python
from password_utils.mod import (
    generate_password,
    generate_passphrase,
    analyze,
    validate,
    hash_password,
    verify_password,
)

# 生成密码
pwd = generate_password(length=16)
print(pwd)  # 例如：K9#mP2$xL7@nQ5!w

# 生成助记符短语
phrase = generate_passphrase(word_count=4)
print(phrase)  # 例如：Dragon-Sunset-Crystal-Wisdom

# 分析强度
strength = analyze("MyPassword123!")
print(strength.level.value)  # strong
print(strength.score)        # 75/100
print(strength.entropy_bits) # 65.2 bits

# 验证密码
result = validate("Test123!")
print(result.is_valid)  # True

# 哈希密码
pwd_hash, salt = hash_password("MySecurePassword!")
print(f"Hash: {pwd_hash}")
print(f"Salt: {salt}")

# 验证密码
is_correct = verify_password("MySecurePassword!", pwd_hash, salt)
print(is_correct)  # True
```

---

## 📖 API 文档

### 密码生成

#### `generate_password(length=16, ...)`

生成密码学安全的随机密码。

**参数:**
- `length` (int): 密码长度，默认 16
- `use_lowercase` (bool): 包含小写字母，默认 True
- `use_uppercase` (bool): 包含大写字母，默认 True
- `use_digits` (bool): 包含数字，默认 True
- `use_special` (bool): 包含特殊字符，默认 True
- `exclude_ambiguous` (bool): 排除易混淆字符 (0,O,l,I,1)，默认 False

**返回:** `str` - 生成的密码

**示例:**
```python
# 标准密码
pwd = generate_password()

# 更长、更安全的密码
pwd = generate_password(length=32)

# 不含特殊字符（某些系统要求）
pwd = generate_password(use_special=False)

# 不含易混淆字符
pwd = generate_password(exclude_ambiguous=True)
```

#### `generate_passphrase(word_count=4, ...)`

生成易记的密码短语。

**参数:**
- `word_count` (int): 单词数量，默认 4
- `separator` (str): 分隔符，默认 "-"
- `use_capitalization` (bool): 首字母大写，默认 True
- `add_number` (bool): 添加数字，默认 False
- `add_symbol` (bool): 添加符号，默认 False

**返回:** `str` - 生成的短语

**示例:**
```python
# 标准短语
phrase = generate_passphrase()  # Dragon-Sunset-Crystal-Wisdom

# 更长短语
phrase = generate_passphrase(word_count=6)

# 带数字增强
phrase = generate_passphrase(add_number=True)  # Dragon-Sunset-Crystal-Wisdom42

# 自定义分隔符
phrase = generate_passphrase(separator="_")  # Dragon_Sunset_Crystal_Wisdom
```

---

### 强度分析

#### `analyze(password)`

分析密码强度。

**参数:**
- `password` (str): 要分析的密码

**返回:** `PasswordStrength` 对象

**PasswordStrength 属性:**
- `level` (StrengthLevel): 强度级别 (very_weak/weak/fair/strong/very_strong)
- `score` (int): 强度分数 (0-100)
- `entropy_bits` (float): 熵值（比特）
- `length` (int): 密码长度
- `has_lowercase` (bool): 是否包含小写字母
- `has_uppercase` (bool): 是否包含大写字母
- `has_digits` (bool): 是否包含数字
- `has_special` (bool): 是否包含特殊字符
- `character_diversity` (float): 字符多样性 (0-1)
- `issues` (List[str]): 发现的问题列表
- `suggestions` (List[str]): 改进建议列表

**示例:**
```python
strength = analyze("MyPassword123!")

print(f"强度：{strength.level.value}")      # strong
print(f"分数：{strength.score}/100")        # 75
print(f"熵值：{strength.entropy_bits} bits") # 65.2

# 检查问题
if strength.issues:
    for issue in strength.issues:
        print(f"问题：{issue}")

# 获取建议
if strength.suggestions:
    for tip in strength.suggestions:
        print(f"建议：{tip}")

# 转换为字典
data = strength.to_dict()
```

---

### 密码验证

#### `validate(password, ...)`

根据安全策略验证密码。

**参数:**
- `password` (str): 要验证的密码
- `require_uppercase` (bool): 要求大写字母，默认 True
- `require_lowercase` (bool): 要求小写字母，默认 True
- `require_digit` (bool): 要求数字，默认 True
- `require_special` (bool): 要求特殊字符，默认 False
- `check_common` (bool): 检查常见密码，默认 True
- `check_sequential` (bool): 检查序列模式，默认 True
- `username` (str): 用户名（检查是否包含），可选
- `email` (str): 邮箱（检查是否包含），可选

**返回:** `ValidationResult` 对象

**ValidationResult 属性:**
- `is_valid` (bool): 是否通过验证
- `errors` (List[ValidationError]): 错误类型列表
- `error_messages` (List[str]): 错误消息列表

**示例:**
```python
# 基本验证
result = validate("Test123!")
print(result.is_valid)  # True

# 严格验证
result = validate(
    "password",
    require_special=True,
    check_common=True,
)
print(result.is_valid)  # False
print(result.error_messages)
# ["Password must contain special characters", "This is a commonly used password"]

# 检查是否包含用户名
result = validate("JohnDoe123!", username="johndoe")
print(result.is_valid)  # False
```

---

### 密码哈希

#### `hash_password(password, salt=None, algorithm="sha256", iterations=100000)`

使用盐值哈希密码。

**参数:**
- `password` (str): 要哈希的密码
- `salt` (bytes): 盐值（可选，自动生成）
- `algorithm` (str): 哈希算法 (sha256/sha512/blake2b)，默认 "sha256"
- `iterations` (int): 迭代次数，默认 100000

**返回:** `Tuple[str, str]` - (哈希值 hex, 盐值 hex)

**示例:**
```python
# 基本哈希
pwd_hash, salt = hash_password("MySecurePassword!")
print(f"Hash: {pwd_hash}")
print(f"Salt: {salt}")

# 使用更强算法
pwd_hash, salt = hash_password(
    "MySecurePassword!",
    algorithm="sha512",
    iterations=200000,
)
```

#### `verify_password(password, stored_hash, salt_hex, ...)`

验证密码是否匹配存储的哈希。

**参数:**
- `password` (str): 要验证的密码
- `stored_hash` (str): 存储的哈希值 (hex)
- `salt_hex` (str): 存储的盐值 (hex)
- `algorithm` (str): 哈希算法，默认 "sha256"
- `iterations` (int): 迭代次数，默认 100000

**返回:** `bool` - 是否匹配

**示例:**
```python
# 存储（注册时）
pwd_hash, salt = hash_password("UserPassword123!")
# 将 pwd_hash 和 salt 存储到数据库

# 验证（登录时）
is_correct = verify_password(
    "UserPassword123!",
    stored_hash=pwd_hash,
    salt_hex=salt,
)
print(is_correct)  # True
```

---

### 其他工具函数

#### `is_weak(password)`

检查密码是否为弱密码。

```python
is_weak("123456")      # True
is_weak("abc")         # True
is_weak("K9#mP2$xL7@") # False
```

#### `is_strong(password)`

检查密码是否为强密码。

```python
is_strong("K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1") # True
is_strong("password123")                     # False
```

#### `estimate_crack_time(password, guesses_per_second=10_000_000_000)`

估算暴力破解时间。

**返回:** `Dict` 包含：
- `entropy_bits`: 熵值
- `combinations`: 总组合数
- `time_to_crack`: 破解时间（人类可读）
- `seconds`: 秒数

```python
info = estimate_crack_time("123456")
print(info["time_to_crack"])  # "instantly"

info = estimate_crack_time("K9#mP2$xL7@nQ5!wR8&vN3^tY6*uI1")
print(info["time_to_crack"])  # "centuries"
```

#### `is_breached(password)`

检查密码是否在常见泄露密码列表中。

```python
is_breached("password")  # True
is_breached("X9#kL2$mN") # False
```

---

## 🔒 安全特性

### 密码学安全随机数

使用 Python `secrets` 模块，提供密码学安全的随机数生成：

```python
import secrets

# 安全随机密码
pwd = "".join(secrets.choice(pool) for _ in range(16))
```

### PBKDF2 密钥派生

使用 PBKDF2-HMAC 进行密钥派生，防止彩虹表攻击：

```python
hashlib.pbkdf2_hmac(
    'sha256',
    password_bytes,
    salt,
    100000,  # 迭代次数
)
```

### 时序安全比较

使用 `hmac.compare_digest` 防止时序攻击：

```python
hmac.compare_digest(computed_hash, stored_hash)
```

---

## 📊 强度级别说明

| 级别 | 分数范围 | 描述 |
|------|----------|------|
| very_weak | 0-24 | 极易被破解，立即更换 |
| weak | 25-49 | 容易被破解，建议更换 |
| fair | 50-74 | 中等强度，可用于低风险场景 |
| strong | 75-89 | 强度高，推荐用于大多数场景 |
| very_strong | 90-100 | 非常高强度，用于高安全需求 |

---

## 🎯 最佳实践

### ✅ 推荐

1. **使用至少 16 个字符**
   ```python
   pwd = generate_password(length=16)
   ```

2. **使用密码短语**
   ```python
   phrase = generate_passphrase(word_count=5)
   ```

3. **始终加盐哈希**
   ```python
   pwd_hash, salt = hash_password(password)
   ```

4. **验证时使用常量时间比较**
   ```python
   verify_password(password, stored_hash, salt)
   ```

### ❌ 避免

1. **不要使用常见密码**
   ```python
   # 会被检测为弱密码
   validate("password123")  # ✗
   ```

2. **不要使用序列模式**
   ```python
   # 会被检测为弱密码
   analyze("abcdef123")  # ✗
   ```

3. **不要明文存储密码**
   ```python
   # 错误：明文存储
   db.store(password)  # ✗
   
   # 正确：哈希存储
   pwd_hash, salt = hash_password(password)
   db.store(pwd_hash, salt)  # ✓
   ```

---

## 🧪 运行测试

```bash
cd password_utils
python password_utils_test.py
```

## 📝 运行示例

```bash
cd password_utils
python examples/usage_examples.py
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**AllToolkit** - 一套工具，多种语言，统一标准。
