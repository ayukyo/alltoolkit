--[[
TOTP Utils 测试套件
运行方式: lua totp_utils_test.lua
]]

local totp_utils = require("mod")

local function assert_eq(actual, expected, msg)
    if actual ~= expected then
        error(msg .. ": 期望 " .. tostring(expected) .. ", 实际 " .. tostring(actual))
    end
end

local function assert_true(condition, msg)
    if not condition then
        error(msg .. ": 期望 true, 实际 " .. tostring(condition))
    end
end

local function assert_false(condition, msg)
    if condition then
        error(msg .. ": 期望 false, 实际 " .. tostring(condition))
    end
end

print("开始 TOTP Utils 测试...")
print()

-- 测试 Base32 编解码
print("=== 测试 Base32 编解码 ===")
local test_pairs = {
    {"", ""},
    {"f", "MY======"},
    {"fo", "MZXQ===="},
    {"foo", "MZXW6==="},
    {"foob", "MZXW6YQ="},
    {"fooba", "MZXW6YTB"},
    {"foobar", "MZXW6YTBOI======"},
}

for _, pair in ipairs(test_pairs) do
    local input, expected = pair[1], pair[2]
    local encoded = totp_utils.base32_encode(input)
    assert_eq(encoded, expected, "编码 " .. input)
    local decoded = totp_utils.base32_decode(expected)
    assert_eq(decoded, input, "解码 " .. expected)
end
print("Base32 编解码测试通过!")
print()

-- 测试 RFC 6238 标准向量
print("=== 测试 RFC 6238 标准向量 ===")

-- 注意: RFC 6238 使用的标准测试密钥是 "12345678901234567890" (20字节)
-- 对应的 Base32 编码是 "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ" (40个字符)
local sha1_tests = {
    {secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ", timestamp = 59, expected = "94287082"},  -- counter=1
    {secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ", timestamp = 1111111109, expected = "07081804"},
    {secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ", timestamp = 1234567890, expected = "89005924"},
    {secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ", timestamp = 2000000000, expected = "69279037"},
    {secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ", timestamp = 20000000000, expected = "65353130"},
}

for _, test in ipairs(sha1_tests) do
    local totp = totp_utils.new_totp(test.secret, 8, 30, "sha1")
    local code = totp:generate(test.timestamp)
    assert_eq(code, test.expected, "SHA1 timestamp=" .. test.timestamp)
end
print("SHA1 TOTP 测试通过!")

-- 测试 6 位验证码
local totp6 = totp_utils.new_totp("GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ", 6, 30, "sha1")
local code6 = totp6:generate(59)
print("6位验证码 (timestamp=59): " .. code6)
assert_eq(#code6, 6, "验证码应为6位")
print("6位验证码测试通过!")
print()

-- 测试验证功能
print("=== 测试验证功能 ===")
local secret = totp_utils.generate_secret()
local totp = totp_utils.new_totp(secret, 6, 30, "sha1")
local code = totp:generate()
print("生成的验证码: " .. code)
assert_true(totp:verify(code), "当前验证码应验证通过")
assert_false(totp:verify("000000"), "错误验证码应验证失败")
print("验证功能测试通过!")
print()

-- 测试时间容差
print("=== 测试时间容差 ===")
local now = os.time()
local future_code = totp_utils.new_totp(secret):generate(now + 60)
assert_true(totp_utils.new_totp(secret):verify(future_code, now + 60, 1), "60秒后验证码应可验证")
print("时间容差测试通过!")
print()

-- 测试密钥生成
print("=== 测试密钥生成 ===")
local gen_secret = totp_utils.generate_secret()
print("生成的密钥: " .. gen_secret)
assert_true(totp_utils.validate_secret(gen_secret), "生成的密钥应有效")
assert_true(#gen_secret >= 16, "密钥长度应足够")
print("密钥生成测试通过!")
print()

-- 测试 QR URL 生成
print("=== 测试 QR URL 生成 ===")
local qr_url = totp:generate_qr_url("test@example.com", "MyService")
print("QR URL: " .. qr_url)
assert_true(qr_url:match("otpauth://totp/"), "URL 应包含 otpauth://")
assert_true(qr_url:match("secret="), "URL 应包含 secret 参数")
print("QR URL 生成测试通过!")
print()

-- 测试剩余秒数
print("=== 测试剩余秒数 ===")
local remaining = totp:get_remaining_seconds()
print("当前步长剩余秒数: " .. remaining)
assert_true(remaining >= 0 and remaining <= 30, "剩余秒数应在 0-30 之间")
print("剩余秒数测试通过!")
print()

print("========================================")
print("所有测试通过!")
print("========================================")