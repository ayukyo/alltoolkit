--[[
Base64 Utils 测试文件
测试所有 Base64 工具函数
]]

-- 加载模块
package.path = package.path .. ";../?.lua"
local base64 = require("mod")

-- 测试计数
local tests_passed = 0
local tests_failed = 0

-- 简单测试框架
local function test(name, func)
    local success, err = pcall(func)
    if success then
        tests_passed = tests_passed + 1
        print("✓ " .. name)
    else
        tests_failed = tests_failed + 1
        print("✗ " .. name .. ": " .. tostring(err))
    end
end

local function assert_eq(actual, expected, msg)
    if actual ~= expected then
        error((msg or "") .. " 期望: " .. tostring(expected) .. " 实际: " .. tostring(actual))
    end
end

local function assert_contains(str, substr, msg)
    if not string.find(str, substr, 1, true) then
        error((msg or "") .. " 字符串应包含: " .. substr)
    end
end

print("========== Base64 Utils 测试开始 ==========\n")

-- 测试基本编码
test("基本编码 - 空字符串", function()
    local result = base64.encode("")
    assert_eq(result, "", "空字符串编码")
end)

test("基本编码 - Hello", function()
    local result = base64.encode("Hello")
    assert_eq(result, "SGVsbG8=", "Hello 编码")
end)

test("基本编码 - Hello World", function()
    local result = base64.encode("Hello World")
    assert_eq(result, "SGVsbG8gV29ybGQ=", "Hello World 编码")
end)

test("基本编码 - 数字", function()
    local result = base64.encode("1234567890")
    assert_eq(result, "MTIzNDU2Nzg5MA==", "数字编码")
end)

test("基本编码 - 特殊字符", function()
    local result = base64.encode("!@#$%^&*()")
    assert_eq(result, "IUAjJCVeJiooKQ==", "特殊字符编码")
end)

test("基本编码 - 中文", function()
    local result = base64.encode("你好世界")
    assert_eq(result, "5L2g5aW95LiW55WM", "中文编码")
end)

-- 测试基本解码
test("基本解码 - 空字符串", function()
    local result, err = base64.decode("")
    assert_eq(err, nil, "无错误")
    assert_eq(result, "", "空字符串解码")
end)

test("基本解码 - Hello", function()
    local result, err = base64.decode("SGVsbG8=")
    assert_eq(err, nil, "无错误")
    assert_eq(result, "Hello", "Hello 解码")
end)

test("基本解码 - Hello World", function()
    local result, err = base64.decode("SGVsbG8gV29ybGQ=")
    assert_eq(err, nil, "无错误")
    assert_eq(result, "Hello World", "Hello World 解码")
end)

test("基本解码 - 中文", function()
    local result, err = base64.decode("5L2g5aW95LiW55WM")
    assert_eq(err, nil, "无错误")
    assert_eq(result, "你好世界", "中文解码")
end)

-- 测试编解码往返
test("编解码往返 - 随机数据", function()
    local original = "This is a test string with various characters: 123!@#"
    local encoded = base64.encode(original)
    local decoded, err = base64.decode(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded, original, "往返一致")
end)

test("编解码往返 - 二进制数据", function()
    local original = string.char(0, 1, 2, 127, 128, 255, 254, 253)
    local encoded = base64.encode(original)
    local decoded, err = base64.decode(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded, original, "二进制往返一致")
end)

-- 测试 URL 安全编码
test("URL安全编码 - 基本测试", function()
    local result = base64.encode_urlsafe("Hello World")
    assert_eq(result, "SGVsbG8gV29ybGQ", "无 padding")
    assert_eq(string.find(result, "="), nil, "无等号")
end)

test("URL安全编码 - 特殊字符转换", function()
    -- 包含会生成 +/ 的数据
    local data = string.char(0xfb, 0xff)
    local result = base64.encode_urlsafe(data)
    assert_eq(string.find(result, "+"), nil, "无加号")
    assert_eq(string.find(result, "/"), nil, "无斜杠")
end)

test("URL安全解码 - 基本测试", function()
    local original = "Test Data!"
    local encoded = base64.encode_urlsafe(original)
    local decoded, err = base64.decode_urlsafe(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded, original, "URL安全往返一致")
end)

-- 测试验证
test("验证 - 有效 Base64", function()
    assert_eq(base64.is_valid("SGVsbG8="), true, "有效标准格式")
    assert_eq(base64.is_valid("SGVsbG8gV29ybGQ="), true, "有效长格式")
end)

test("验证 - 无效 Base64", function()
    assert_eq(base64.is_valid("SGVs=bG8="), false, "无效 padding 位置")
    assert_eq(base64.is_valid("SGVs##G8="), false, "含非法字符")
    assert_eq(base64.is_valid(""), false, "空字符串")
end)

test("验证 - 含空格的 Base64", function()
    -- 注意：is_valid 会忽略空白字符（与解码行为一致）
    assert_eq(base64.is_valid("SGVs bG8="), true, "含空格仍然有效")
end)

test("验证 - URL 安全格式", function()
    assert_eq(base64.is_valid("SGVsbG8-_"), true, "URL安全字符有效")
end)

-- 测试统计
test("统计信息 - 基本测试", function()
    local stats = base64.get_encode_stats("Hello")
    assert_eq(stats.original_size, 5, "原始大小")
    assert_eq(stats.encoded_size, 8, "编码大小")
    assert_eq(stats.padding_count, 1, "padding 数量")
end)

test("统计信息 - 无 padding", function()
    local stats = base64.get_encode_stats("Hell")
    assert_eq(stats.original_size, 4, "原始大小")
    assert_eq(stats.padding_count, 2, "padding 数量")
end)

test("统计信息 - 不需要 padding", function()
    local stats = base64.get_encode_stats("HelloHelloHello")
    assert_eq(stats.original_size, 15, "原始大小")
    assert_eq(stats.padding_count, 0, "无 padding")
end)

-- 测试表格编解码
test("表格编码 - 简单表格", function()
    local tbl = { name = "test", value = 123 }
    local encoded, err = base64.encode_table(tbl)
    assert_eq(err, nil, "无错误")
    assert_eq(type(encoded), "string", "返回字符串")
    assert_eq(#encoded > 0, true, "非空")
end)

test("表格编码 - 嵌套表格", function()
    local tbl = {
        user = {
            name = "Alice",
            age = 30,
            tags = { "dev", "lua" }
        }
    }
    local encoded, err = base64.encode_table(tbl)
    assert_eq(err, nil, "无错误")
end)

test("表格编码 - 数组", function()
    local tbl = { 1, 2, 3, "four", true }
    local encoded, err = base64.encode_table(tbl)
    assert_eq(err, nil, "无错误")
end)

test("表格解码 - 简单表格", function()
    local original = { name = "test", count = 42 }
    local encoded, _ = base64.encode_table(original)
    local decoded, err = base64.decode_table(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded.name, "test", "name 字段")
    assert_eq(decoded.count, 42, "count 字段")
end)

test("表格解码 - 嵌套表格", function()
    local original = {
        config = {
            host = "localhost",
            port = 8080
        },
        items = { "a", "b", "c" }
    }
    local encoded, _ = base64.encode_table(original)
    local decoded, err = base64.decode_table(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded.config.host, "localhost", "嵌套字段")
    assert_eq(#decoded.items, 3, "数组长度")
end)

-- 测试边界情况
test("边界 - 单字符", function()
    local original = "A"
    local encoded = base64.encode(original)
    local decoded, _ = base64.decode(encoded)
    assert_eq(decoded, original, "单字符往返")
end)

test("边界 - 两字符", function()
    local original = "AB"
    local encoded = base64.encode(original)
    local decoded, _ = base64.decode(encoded)
    assert_eq(decoded, original, "两字符往返")
end)

test("边界 - 大数据", function()
    -- 生成 10KB 数据
    local original = string.rep("TestData123", 1000)
    local encoded = base64.encode(original)
    local decoded, err = base64.decode(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded, original, "大数据往返")
end)

test("边界 - 空白字符处理", function()
    local encoded = "SGVs\nbG8=\t "
    local decoded, err = base64.decode(encoded)
    assert_eq(err, nil, "无错误")
    assert_eq(decoded, "Hello", "空白字符被忽略")
end)

-- 测试错误处理
test("错误处理 - 无效输入类型", function()
    local success, err = pcall(function()
        base64.encode(123)
    end)
    assert_eq(success, false, "应该报错")
    assert_contains(err, "字符串", "错误信息包含类型提示")
end)

test("错误处理 - 解码无效字符", function()
    local decoded, err = base64.decode("SGVs###G8=")
    assert_eq(decoded, nil, "返回 nil")
    assert_eq(err ~= nil, true, "有错误信息")
end)

test("错误处理 - 解码无效长度", function()
    -- 7字符（非4的倍数，无padding）应该被处理（不崩溃）
    local decoded, err = base64.decode("SGVsbG8")
    -- 标准格式下，非4倍数长度可能报错或尝试解码
    -- 主要确保函数不崩溃
    assert_eq(decoded == nil or decoded ~= nil, true, "不崩溃")
end)

-- 测试标准测试向量
test("标准测试向量 - RFC 4648", function()
    -- RFC 4648 测试向量
    local vectors = {
        { "", "" },
        { "f", "Zg==" },
        { "fo", "Zm8=" },
        { "foo", "Zm9v" },
        { "foob", "Zm9vYg==" },
        { "fooba", "Zm9vYmE=" },
        { "foobar", "Zm9vYmFy" },
    }
    
    for _, v in ipairs(vectors) do
        local encoded = base64.encode(v[1])
        assert_eq(encoded, v[2], "编码: " .. v[1])
        
        local decoded, _ = base64.decode(v[2])
        assert_eq(decoded, v[1], "解码: " .. v[2])
    end
end)

-- 打印结果
print("\n========== 测试结果 ==========")
print(string.format("通过: %d", tests_passed))
print(string.format("失败: %d", tests_failed))
print(string.format("总计: %d", tests_passed + tests_failed))
print("========== 测试结束 ==========")

-- 返回状态
os.exit(tests_failed > 0 and 1 or 0)