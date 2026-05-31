# TOTP Utils - Lua 实现的 TOTP 工具库

零外部依赖，纯 Lua 实现，遵循 RFC 6238 标准。

## 功能

- 生成和验证 TOTP 代码（如 Google Authenticator）
- 支持 SHA1 哈希算法
- 生成 otpauth:// URI（用于二维码）
- 密钥生成和验证
- 支持 6 位和 8 位验证码

## 使用方法

```lua
local totp_utils = require("mod")

-- 创建 TOTP 实例
local totp = totp_utils.new_totp("YOUR_BASE32_SECRET", 6, 30, "sha1")

-- 生成当前验证码
local code = totp:generate()
print("当前验证码: " .. code)

-- 验证验证码
local valid = totp:verify("123456")
print("验证结果: " .. tostring(valid))

-- 生成 QR 码 URL
local qr_url = totp:generate_qr_url("user@example.com", "MyApp")
print("QR URL: " .. qr_url)

-- 生成新密钥
local new_secret = totp_utils.generate_secret()
print("新密钥: " .. new_secret)
```

## API

### totp_utils.new_totp(secret, digits, interval, algorithm)

创建 TOTP 实例。

- `secret`: Base32 编码的密钥
- `digits`: 验证码位数（默认 6）
- `interval`: 时间步长秒数（默认 30）
- `algorithm`: 哈希算法（默认 "sha1"）

### totp:generate(timestamp)

生成 TOTP 验证码。

- `timestamp`: Unix 时间戳（可选，默认当前时间）
- 返回格式化后的验证码字符串

### totp:verify(token, timestamp, tolerance)

验证 TOTP 验证码。

- `token`: 用户输入的验证码
- `timestamp`: 验证时的时间戳（可选，默认当前时间）
- `tolerance`: 允许的前后时间步数（默认 1）
- 返回布尔值

### totp:get_remaining_seconds()

获取当前步长剩余秒数。

### totp:get_current_code()

获取当前验证码和剩余秒数。

### totp:generate_qr_url(account_name, issuer)

生成 otpauth:// URI。

- `account_name`: 账户名称
- `issuer`: 服务名称（可选）
- 返回 otpauth:// URI 字符串

### totp_utils.generate_secret(length)

生成随机 Base32 密钥。

- `length`: 密钥字节长度（默认 20）
- 返回 Base32 编码的密钥字符串

### totp_utils.validate_secret(secret)

验证 Base32 密钥格式。

- `secret`: 要验证的密钥
- 返回布尔值

### totp_utils.base32_encode(data)

Base32 编码。

### totp_utils.base32_decode(encoded)

Base32 解码。

## 运行测试

```bash
lua totp_utils_test.lua
```

## 运行示例

```bash
lua examples/usage_examples.lua
```

## 依赖

- Lua 5.3+（使用原生位运算符）