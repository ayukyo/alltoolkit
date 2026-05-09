# TOTP Utils

TOTP (Time-based One-Time Password) 和 HOTP (HMAC-based One-Time Password) 工具集。

完整实现 RFC 6238 (TOTP) 和 RFC 4226 (HOTP) 标准，零外部依赖。

## 功能特性

- ✅ **TOTP 生成** - 生成基于时间的一次性密码
- ✅ **TOTP 验证** - 验证 TOTP 代码，支持时间漂移容忍
- ✅ **HOTP 生成** - 生成基于计数器的一次性密码
- ✅ **多种算法** - 支持 SHA1、SHA256、SHA512
- ✅ **QR 码 URL** - 生成 otpauth:// URL 和 QR 码图片链接
- ✅ **密钥管理** - 生成和验证 Base32 密钥
- ✅ **备份码** - 生成恢复/备用码
- ✅ **多账户管理** - TOTPManager 类管理多个账户

## 快速开始

```python
from mod import TOTPUtils, generate_secret

# 生成密钥
secret = generate_secret()
print(f"密钥: {secret}")

# 创建 TOTP 实例
totp = TOTPUtils(secret)

# 生成当前代码
code = totp.generate()
print(f"当前代码: {code}")
print(f"剩余秒数: {totp.get_remaining_seconds()}秒")

# 验证代码
is_valid = totp.verify(code)
print(f"验证结果: {is_valid}")
```

## 使用示例

### 1. 设置新账户

```python
from mod import TOTPUtils, generate_secret, generate_backup_codes

# 生成密钥
secret = generate_secret(20)

# 创建 TOTP 实例
totp = TOTPUtils(secret)

# 获取 QR 码 URL（用户扫码绑定）
qr_url = totp.get_qr_code_url("MyApp", "user@example.com")
print(f"QR码: {qr_url}")

# 生成备份码
backup_codes = generate_backup_codes(10, 8)
print(f"备份码: {backup_codes}")
```

### 2. 验证登录

```python
from mod import TOTPUtils

secret = "用户保存的密钥"
totp = TOTPUtils(secret)

# 验证用户输入的代码（允许±1个时间窗口的漂移）
if totp.verify(user_input_code, tolerance=1):
    print("验证成功!")
else:
    print("验证失败!")
```

### 3. 多账户管理

```python
from mod import TOTPManager, generate_secret

manager = TOTPManager()

# 添加账户
manager.add_account("GitHub", generate_secret(), "GitHub")
manager.add_account("Google", generate_secret(), "Google")

# 获取所有代码
codes = manager.get_all_codes()
for name, info in codes.items():
    print(f"{name}: {info['code']} ({info['remaining']}s)")
```

### 4. HOTP (计数器模式)

```python
from mod import HOTPUtils, generate_secret

secret = generate_secret()
hotp = HOTPUtils(secret)

# 生成代码
for counter in range(5):
    code = hotp.generate(counter)
    print(f"Counter {counter}: {code}")

# 验证
if hotp.verify(user_code, expected_counter):
    print("验证成功!")
```

## API 参考

### TOTPUtils

| 方法 | 说明 |
|------|------|
| `generate(timestamp)` | 生成 TOTP 代码 |
| `verify(code, timestamp, tolerance)` | 验证代码 |
| `get_remaining_seconds(timestamp)` | 获取剩余有效时间 |
| `get_otpauth_url(issuer, account)` | 获取 otpauth:// URL |
| `get_qr_code_url(issuer, account, service)` | 获取 QR 码图片 URL |

### HOTPUtils

| 方法 | 说明 |
|------|------|
| `generate(counter)` | 生成 HOTP 代码 |
| `verify(code, counter)` | 验证代码 |

### 便捷函数

```python
# 生成密钥
secret = generate_secret(length=20)

# 验证密钥格式
is_valid = is_valid_secret(secret)

# 快捷生成 TOTP
code = generate_totp(secret, digits=6, interval=30)

# 快捷验证 TOTP
is_valid = verify_totp(code, secret, tolerance=1)

# 快捷生成 HOTP
code = generate_hotp(secret, counter=0)

# 生成备份码
codes = generate_backup_codes(count=10, length=8)
```

## 测试

```bash
# 运行测试
python totp_utils_test.py

# 或使用 pytest
python -m pytest totp_utils_test.py -v
```

## 示例

```bash
# 认证流程演示
python examples/auth_demo.py

# 多账户管理演示
python examples/manager_demo.py

# HOTP 演示
python examples/hotp_demo.py
```

## 安全建议

1. **密钥存储** - 密钥应加密存储，不要明文保存
2. **备份码** - 建议生成并安全存储备份码
3. **时间同步** - 确保服务器时间准确（使用 NTP）
4. **失败限制** - 实现验证失败次数限制，防止暴力破解
5. **HTTPS** - 通过 HTTPS 传输验证码

## 标准

- [RFC 4226](https://tools.ietf.org/html/rfc4226) - HOTP: An HMAC-Based One-Time Password Algorithm
- [RFC 6238](https://tools.ietf.org/html/rfc6238) - TOTP: Time-Based One-Time Password Algorithm

## 依赖

仅使用 Python 标准库，无外部依赖：

- `hashlib` - HMAC 和哈希算法
- `hmac` - HMAC 实现
- `base64` - Base32 编解码
- `struct` - 二进制数据打包
- `secrets` - 安全随机数
- `time` - 时间戳
- `urllib.parse` - URL 编码