--[[
TOTP Utils 使用示例
]]

local totp_utils = require("mod")

print("=== TOTP Utils 使用示例 ===")
print()

-- 示例 1: 基本使用
print("1. 基本使用")
local secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  -- "12345678901234567890" 的 Base32 编码
local totp = totp_utils.new_totp(secret, 6, 30, "sha1")
local code, remaining = totp:get_current_code()
print("   密钥: " .. secret)
print("   当前验证码: " .. code)
print("   剩余 " .. remaining .. " 秒")
print()

-- 示例 2: 生成新密钥
print("2. 生成新密钥")
local new_secret = totp_utils.generate_secret(20)
print("   新生成的密钥: " .. new_secret)
local new_totp = totp_utils.new_totp(new_secret)
print("   当前验证码: " .. new_totp:generate())
print()

-- 示例 3: 验证验证码
print("3. 验证验证码")
local verify_totp = totp_utils.new_totp(new_secret)
local current_code = verify_totp:generate()
print("   当前验证码: " .. current_code)
print("   验证结果: " .. tostring(verify_totp:verify(current_code)))
print("   错误验证码验证: " .. tostring(verify_totp:verify("123456")))
print()

-- 示例 4: 生成 QR 码 URL
print("4. 生成 QR 码 URL")
local qr_url = verify_totp:generate_qr_url("user@example.com", "MyApp")
print("   账户: user@example.com")
print("   服务: MyApp")
print("   URL: " .. qr_url)
print()

-- 示例 5: 8 位验证码
print("5. 使用 8 位验证码")
local totp8 = totp_utils.new_totp(secret, 8, 30, "sha1")
print("   8位验证码: " .. totp8:generate(59))
print()

-- 示例 6: 时间容差验证
print("6. 时间容差验证")
local now = os.time()
local future_totp = totp_utils.new_totp(new_secret)
local future_code = future_totp:generate(now + 60)
print("   60秒后的验证码: " .. future_code)
print("   当前时间验证 (容差=0): " .. tostring(future_totp:verify(future_code, now, 0)))
print("   60秒后验证 (容差=2): " .. tostring(future_totp:verify(future_code, now + 60, 2)))
print()

-- 示例 7: 密钥验证
print("7. 密钥验证")
print("   有效密钥: " .. tostring(totp_utils.validate_secret(new_secret)))
print("   无效密钥: " .. tostring(totp_utils.validate_secret("invalid!@#")))
print()

print("=== 示例结束 ===")