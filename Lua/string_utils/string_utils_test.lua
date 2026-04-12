#!/usr/bin/env lua
---
-- String Utilities Test Suite
-- 字符串工具函数测试套件
--
-- 覆盖场景:
-- - 空白处理 (trim, is_empty, is_blank)
-- - 大小写转换 (lower, upper, capitalize, title, case conversion)
-- - 字符串查找 (contains, starts_with, ends_with, find_all)
-- - 字符串替换 (replace_first, replace_last, replace_all, replace_n)
-- - 字符串分割 (split, lines, join)
-- - 字符串填充 (pad_left, pad_right, pad_center)
-- - 字符串截断 (truncate, truncate_words)
-- - 验证函数 (is_alpha, is_digit, is_email, is_url, is_ipv4)
-- - 格式化函数 (format_number, format_bytes, format_time)
-- - 编码解码 (url_encode/decode, html_encode/decode, base64_encode/decode)
-- - 相似度计算 (levenshtein, similarity)
-- - 工具函数 (random, uuid, builder)
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local mod_path = path .. "mod.lua"

-- 加载模块
local StringUtils = dofile(mod_path)

-- 测试统计
local tests_run = 0
local tests_passed = 0
local tests_failed = 0
local failures = {}

--- 断言函数
local function assert_eq(actual, expected, message)
    tests_run = tests_run + 1
    if actual == expected then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or ("Expected %s, got %s"):format(tostring(expected), tostring(actual))
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言真值
local function assert_true(condition, message)
    tests_run = tests_run + 1
    if condition then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected true"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言假值
local function assert_false(condition, message)
    tests_run = tests_run + 1
    if not condition then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected false"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 打印测试组标题
local function test_group(name)
    print("\n📋 " .. name)
    print(string.rep("-", 50))
end

-------------------------------------------------------------------------------
-- 测试：空白处理
-------------------------------------------------------------------------------
test_group("空白处理 (Whitespace Handling)")

assert_eq(StringUtils.trim("  hello  "), "hello", "trim 两端空白")
assert_eq(StringUtils.trim("hello"), "hello", "trim 无空白")
assert_eq(StringUtils.trim("  "), "", "trim 全空白")
assert_true(StringUtils.is_empty(nil), "is_empty(nil)")
assert_true(StringUtils.is_empty(""), "is_empty(\"\")")
assert_false(StringUtils.is_empty(" "), "is_empty(\" \")")
assert_true(StringUtils.is_blank(nil), "is_blank(nil)")
assert_true(StringUtils.is_blank(""), "is_blank(\"\")")
assert_true(StringUtils.is_blank("   "), "is_blank(\"   \")")
assert_false(StringUtils.is_blank(" a "), "is_blank(\" a \")")
assert_eq(StringUtils.trim_left("  hello  "), "hello  ", "trim_left")
assert_eq(StringUtils.trim_right("  hello  "), "  hello", "trim_right")

-------------------------------------------------------------------------------
-- 测试：大小写转换
-------------------------------------------------------------------------------
test_group("大小写转换 (Case Conversion)")

assert_eq(StringUtils.lower("HELLO"), "hello", "lower")
assert_eq(StringUtils.upper("hello"), "HELLO", "upper")
assert_eq(StringUtils.capitalize("hello"), "Hello", "capitalize")
assert_eq(StringUtils.capitalize("HELLO"), "Hello", "capitalize 全大写")
assert_eq(StringUtils.title("hello world"), "Hello World", "title")
assert_eq(StringUtils.to_snake_case("camelCase"), "camel_case", "to_snake_case")
assert_eq(StringUtils.to_snake_case("PascalCase"), "pascal_case", "to_snake_case PascalCase")
assert_eq(StringUtils.to_camel_case("snake_case"), "snakeCase", "to_camel_case")
assert_eq(StringUtils.to_pascal_case("snake_case"), "SnakeCase", "to_pascal_case")

-------------------------------------------------------------------------------
-- 测试：字符串查找
-------------------------------------------------------------------------------
test_group("字符串查找 (String Search)")

assert_true(StringUtils.contains("hello world", "world"), "contains 找到")
assert_false(StringUtils.contains("hello world", "foo"), "contains 未找到")
assert_true(StringUtils.starts_with("hello world", "hello"), "starts_with")
assert_false(StringUtils.starts_with("hello world", "world"), "starts_with false")
assert_true(StringUtils.ends_with("hello world", "world"), "ends_with")
assert_false(StringUtils.ends_with("hello world", "hello"), "ends_with false")

local positions = StringUtils.find_all("abcabcabc", "abc")
assert_eq(#positions, 3, "find_all 找到 3 个")
assert_eq(positions[1], 1, "find_all 位置 1")
assert_eq(positions[2], 4, "find_all 位置 2")
assert_eq(positions[3], 7, "find_all 位置 3")

-------------------------------------------------------------------------------
-- 测试：字符串替换
-------------------------------------------------------------------------------
test_group("字符串替换 (String Replacement)")

assert_eq(StringUtils.replace_first("hello world world", "world", "foo"), 
          "hello foo world", "replace_first")
assert_eq(StringUtils.replace_last("hello world world", "world", "foo"), 
          "hello world foo", "replace_last")
assert_eq(StringUtils.replace_all("hello world world", "world", "foo"), 
          "hello foo foo", "replace_all")
assert_eq(StringUtils.replace_n("a b a b a", "a", "x", 2), 
          "x b x b a", "replace_n")

-------------------------------------------------------------------------------
-- 测试：字符串分割与连接
-------------------------------------------------------------------------------
test_group("分割与连接 (Split & Join)")

local parts = StringUtils.split("a,b,c", ",")
assert_eq(#parts, 3, "split 数量")
assert_eq(parts[1], "a", "split[1]")
assert_eq(parts[2], "b", "split[2]")
assert_eq(parts[3], "c", "split[3]")

local lines = StringUtils.lines("line1\nline2\nline3")
assert_eq(#lines, 3, "lines 数量")

local joined = StringUtils.join({"a", "b", "c"}, "-")
assert_eq(joined, "a-b-c", "join")

-------------------------------------------------------------------------------
-- 测试：字符串填充
-------------------------------------------------------------------------------
test_group("字符串填充 (Padding)")

assert_eq(StringUtils.pad_left("42", 5, "0"), "00042", "pad_left")
assert_eq(StringUtils.pad_right("42", 5, "0"), "42000", "pad_right")
assert_eq(StringUtils.pad_center("42", 7, " "), "  42   ", "pad_center")
assert_eq(StringUtils.pad_center("42", 6, " "), "  42  ", "pad_center 偶数")

-------------------------------------------------------------------------------
-- 测试：字符串截断
-------------------------------------------------------------------------------
test_group("字符串截断 (Truncation)")

assert_eq(StringUtils.truncate("hello world", 8), "hello...", "truncate")
assert_eq(StringUtils.truncate("hi", 10), "hi", "truncate 不需要")
assert_eq(StringUtils.truncate_words("hello world foo bar", 15), "hello world...", "truncate_words")

-------------------------------------------------------------------------------
-- 测试：验证函数
-------------------------------------------------------------------------------
test_group("验证函数 (Validation)")

assert_true(StringUtils.is_alpha("abc"), "is_alpha")
assert_false(StringUtils.is_alpha("abc123"), "is_alpha 含数字")
assert_true(StringUtils.is_digit("123"), "is_digit")
assert_false(StringUtils.is_digit("123a"), "is_digit 含字母")
assert_true(StringUtils.is_alphanumeric("abc123"), "is_alphanumeric")
assert_true(StringUtils.is_email("test@example.com"), "is_email")
assert_false(StringUtils.is_email("invalid"), "is_email 无效")
assert_true(StringUtils.is_url("https://example.com"), "is_url")
assert_true(StringUtils.is_ipv4("192.168.1.1"), "is_ipv4")
assert_false(StringUtils.is_ipv4("256.1.1.1"), "is_ipv4 超限")

-------------------------------------------------------------------------------
-- 测试：格式化函数
-------------------------------------------------------------------------------
test_group("格式化函数 (Formatting)")

assert_eq(StringUtils.format_number(1234567), "1,234,567", "format_number")
assert_eq(StringUtils.format_number(-1234567), "-1,234,567", "format_number 负数")
assert_true(StringUtils.format_bytes(1536):match("^1.50 KB$"), "format_bytes")
assert_eq(StringUtils.format_time(3661), "1:01:01", "format_time")
assert_true(StringUtils.format_time(61):match("^1:01$"), "format_time 无小时")

-------------------------------------------------------------------------------
-- 测试：编码解码
-------------------------------------------------------------------------------
test_group("编码解码 (Encoding/Decoding)")

assert_eq(StringUtils.url_encode("hello world"), "hello+world", "url_encode")
assert_eq(StringUtils.url_decode("hello+world"), "hello world", "url_decode")
assert_eq(StringUtils.html_encode("<script>"), "&lt;script&gt;", "html_encode")
assert_eq(StringUtils.html_decode("&lt;script&gt;"), "<script>", "html_decode")

local encoded = StringUtils.base64_encode("Hello, World!")
local decoded = StringUtils.base64_decode(encoded)
assert_eq(decoded, "Hello, World!", "base64 encode/decode")

-------------------------------------------------------------------------------
-- 测试：相似度
-------------------------------------------------------------------------------
test_group("相似度 (Similarity)")

assert_eq(StringUtils.levenshtein("kitten", "sitting"), 3, "levenshtein")
assert_eq(StringUtils.levenshtein("", "abc"), 3, "levenshtein 空串")
assert_eq(StringUtils.similarity("hello", "hello"), 1.0, "similarity 相同")
assert_true(StringUtils.similarity("hello", "hallo") > 0.5, "similarity 相似")

-------------------------------------------------------------------------------
-- 测试：工具函数
-------------------------------------------------------------------------------
test_group("工具函数 (Utilities)")

local random_str = StringUtils.random(10)
assert_eq(#random_str, 10, "random 长度")

local uuid = StringUtils.uuid()
assert_true(uuid:match("^%x%x%x%x%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%x%x%x%x%x%x%x%x$"), "uuid 格式")

local builder = StringUtils.builder()
builder:append("Hello"):append(" "):append("World")
assert_eq(builder:to_string(), "Hello World", "builder")

-------------------------------------------------------------------------------
-- 测试：模板与插值
-------------------------------------------------------------------------------
test_group("模板与插值 (Template & Interpolation)")

local template_result = StringUtils.template("Hello, {name}!", { name = "World" })
assert_eq(template_result, "Hello, World!", "template")

local interp_result = StringUtils.interpolate("2 + 2 = ${2 + 2}", {})
assert_eq(interp_result, "2 + 2 = 4", "interpolate 表达式")

-------------------------------------------------------------------------------
-- 测试：边界情况
-------------------------------------------------------------------------------
test_group("边界情况 (Edge Cases)")

assert_true(StringUtils.is_empty(nil), "nil 处理")
assert_eq(StringUtils.trim(nil), nil, "trim nil")
assert_eq(StringUtils.contains(nil, "x"), false, "contains nil")
assert_eq(StringUtils.length(nil), 0, "length nil")
assert_eq(StringUtils.char_at(nil, 1), nil, "char_at nil")
assert_eq(StringUtils.substring(nil, 1, 2), nil, "substring nil")

-------------------------------------------------------------------------------
-- 打印测试结果
-------------------------------------------------------------------------------
print("\n" .. string.rep("=", 50))
print("📊 测试结果")
print(string.rep("=", 50))
print(string.format("总测试数：%d", tests_run))
print(string.format("✅ 通过：%d", tests_passed))
print(string.format("❌ 失败：%d", tests_failed))

if tests_failed > 0 then
    print("\n📝 失败详情:")
    for i, failure in ipairs(failures) do
        print(string.format("  %d. %s", i, failure))
    end
    os.exit(1)
else
    print("\n🎉 所有测试通过!")
    os.exit(0)
end
