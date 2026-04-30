--[[
Base64 Utils 使用示例
演示各种 Base64 编码/解码场景
]]

-- 加载模块
package.path = package.path .. ";../?.lua"
local base64 = require("mod")

local function separator()
    print(string.rep("─", 40))
end

print("========== Base64 Utils 使用示例 ==========\n")

-- 1. 基本编码解码
print("1. 基本编码解码")
separator()

local text = "Hello, 世界!"
local encoded = base64.encode(text)
local decoded, _ = base64.decode(encoded)

print(string.format("原文: %s", text))
print(string.format("编码: %s", encoded))
print(string.format("解码: %s", decoded))
print()

-- 2. URL 安全编码
print("2. URL 安全编码")
separator()

local url_data = "user@example.com:password123"
local url_encoded = base64.encode_urlsafe(url_data)
local url_decoded, _ = base64.decode_urlsafe(url_encoded)

print(string.format("原文: %s", url_data))
print(string.format("URL安全编码: %s", url_encoded))
print(string.format("解码: %s", url_decoded))
print("注意: URL安全编码无 padding，+ 替换为 -，/ 替换为 _")
print()

-- 3. 二进制数据编码
print("3. 二进制数据编码")
separator()

local binary = string.char(0x00, 0xFF, 0x7F, 0x80, 0x01, 0xFE)
local bin_encoded = base64.encode(binary)
local bin_decoded, _ = base64.decode(bin_encoded)

print(string.format("二进制数据长度: %d 字节", #binary))
print(string.format("编码后长度: %d 字节", #bin_encoded))
print(string.format("解码后匹配: %s", binary == bin_decoded and "是" or "否"))
print()

-- 4. 统计信息
print("4. 编码统计信息")
separator()

local sample = "这是一段测试文本，用于演示编码统计功能。"
local stats = base64.get_encode_stats(sample)

print(string.format("原始大小: %d 字节", stats.original_size))
print(string.format("编码大小: %d 字节", stats.encoded_size))
print(string.format("开销: %d 字节 (%.1f%%)", stats.overhead_bytes, stats.overhead_percent))
print(string.format("Padding: %d 个", stats.padding_count))
print()

-- 5. 验证
print("5. Base64 验证")
separator()

local valid_b64 = "SGVsbG8gV29ybGQ="
local invalid_b64 = "SGVs###G8="
local urlsafe_b64 = "SGVsbG8-_"

print(string.format("'%s' 有效: %s", valid_b64, base64.is_valid(valid_b64) and "是" or "否"))
print(string.format("'%s' 有效: %s", invalid_b64, base64.is_valid(invalid_b64) and "是" or "否"))
print(string.format("'%s' 有效: %s", urlsafe_b64, base64.is_valid(urlsafe_b64) and "是" or "否"))
print()

-- 6. 表格编码
print("6. 表格编码（Base64 JSON）")
separator()

local config = {
    app_name = "MyApp",
    version = "1.0.0",
    settings = {
        debug = true,
        port = 8080,
        hosts = { "localhost", "127.0.0.1" }
    }
}

local tbl_encoded, _ = base64.encode_table(config)
print("原始表格:")
for k, v in pairs(config) do
    print(string.format("  %s: %s", k, type(v) == "table" and "[表格]" or tostring(v)))
end
print(string.format("\nBase64 编码: %s", tbl_encoded))

local tbl_decoded, _ = base64.decode_table(tbl_encoded)
print("\n解码后表格:")
print(string.format("  app_name: %s", tbl_decoded.app_name))
print(string.format("  version: %s", tbl_decoded.version))
print(string.format("  settings.debug: %s", tostring(tbl_decoded.settings.debug)))
print(string.format("  settings.port: %s", tbl_decoded.settings.port))
print()

-- 7. 实用示例：简单 Token 生成
print("7. 实用示例：简单 Token")
separator()

local function generate_token(user_id, timestamp, secret)
    local data = {
        user = user_id,
        time = timestamp,
        secret = secret
    }
    return base64.encode_table(data)
end

local function verify_token(token, secret)
    local data, err = base64.decode_table(token)
    if err then return false, err end
    return data.secret == secret, data
end

local token = generate_token("user123", os.time(), "my_secret_key")
print(string.format("生成的 Token: %s", token))

local valid, payload = verify_token(token, "my_secret_key")
print(string.format("Token 验证: %s", valid and "通过" or "失败"))
print(string.format("用户ID: %s", payload.user))
print()

-- 8. RFC 4648 标准测试向量验证
print("8. RFC 4648 标准测试向量")
separator()

local rfc_vectors = {
    { input = "", expected = "" },
    { input = "f", expected = "Zg==" },
    { input = "fo", expected = "Zm8=" },
    { input = "foo", expected = "Zm9v" },
    { input = "foob", expected = "Zm9vYg==" },
    { input = "fooba", expected = "Zm9vYmE=" },
    { input = "foobar", expected = "Zm9vYmFy" },
}

local all_pass = true
for _, v in ipairs(rfc_vectors) do
    local result = base64.encode(v.input)
    local pass = result == v.expected
    all_pass = all_pass and pass
    print(string.format("'%s' → '%s' %s", 
        #v.input > 0 and v.input or "(空)", 
        result, 
        pass and "✓" or "✗ 期望: " .. v.expected))
end
print(string.format("\n所有测试向量: %s", all_pass and "通过" or "有失败"))
print()

print("========== 示例演示结束 ==========")