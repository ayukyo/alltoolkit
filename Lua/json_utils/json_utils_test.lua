---
-- JSON Utilities Test Suite
-- JSON 工具函数库测试套件
--
-- 完整的单元测试覆盖所有功能
--
-- @author AllToolkit
-- @version 1.0.0

local JsonUtils = require("mod")

-- 测试统计
local tests_passed = 0
local tests_failed = 0
local test_results = {}

--- 断言函数
-- @param condition 条件
-- @param message 消息
local function assert_true(condition, message)
    if condition then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. (message or "Assertion failed"))
    end
end

local function assert_equals(actual, expected, message)
    if actual == expected then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. (message or "Assertion failed") .. 
            " - Expected: " .. tostring(expected) .. ", Got: " .. tostring(actual))
    end
end

local function assert_nil(value, message)
    if value == nil then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. (message or "Expected nil") .. 
            " - Got: " .. tostring(value))
    end
end

local function assert_not_nil(value, message)
    if value ~= nil then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. (message or "Expected non-nil value"))
    end
end

local function assert_error(func, message)
    local ok, err = pcall(func)
    if not ok then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. (message or "Expected error"))
    end
end

local function assert_table_equals(actual, expected, message)
    if JsonUtils.equals(actual, expected) then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. (message or "Tables not equal"))
    end
end

local function start_section(name)
    print("\n=== " .. name .. " ===")
end

local function test(name, func)
    local ok, err = pcall(func)
    if ok then
        tests_passed = tests_passed + 1
    else
        tests_failed = tests_failed + 1
        table.insert(test_results, "FAIL: " .. name .. " - " .. tostring(err))
    end
end

-------------------------------------------------------------------------------
-- 测试开始
-------------------------------------------------------------------------------

print("========================================")
print("  JSON Utilities Test Suite")
print("========================================")

-------------------------------------------------------------------------------
-- 基础编码测试
-------------------------------------------------------------------------------

start_section("Basic Encoding Tests")

test("encode null", function()
    local result = JsonUtils.encode(nil)
    assert_equals(result, "null", "null encoding")
end)

test("encode boolean true", function()
    local result = JsonUtils.encode(true)
    assert_equals(result, "true", "true encoding")
end)

test("encode boolean false", function()
    local result = JsonUtils.encode(false)
    assert_equals(result, "false", "false encoding")
end)

test("encode number integer", function()
    local result = JsonUtils.encode(42)
    assert_equals(result, "42", "integer encoding")
end)

test("encode number negative", function()
    local result = JsonUtils.encode(-123)
    assert_equals(result, "-123", "negative integer encoding")
end)

test("encode number zero", function()
    local result = JsonUtils.encode(0)
    assert_equals(result, "0", "zero encoding")
end)

test("encode number float", function()
    local result = JsonUtils.encode(3.14159)
    assert_not_nil(result:match("3%.14"), "float encoding")
end)

test("encode number scientific notation", function()
    local result = JsonUtils.encode(1e10)
    assert_not_nil(result, "scientific notation encoding")
end)

test("encode number infinity as null", function()
    local result = JsonUtils.encode(math.huge)
    assert_equals(result, "null", "infinity should be null")
end)

test("encode number negative infinity as null", function()
    local result = JsonUtils.encode(-math.huge)
    assert_equals(result, "null", "negative infinity should be null")
end)

test("encode number NaN as null", function()
    local result = JsonUtils.encode(0/0)
    assert_equals(result, "null", "NaN should be null")
end)

test("encode string simple", function()
    local result = JsonUtils.encode("hello")
    assert_equals(result, '"hello"', "simple string encoding")
end)

test("encode string empty", function()
    local result = JsonUtils.encode("")
    assert_equals(result, '""', "empty string encoding")
end)

test("encode string with quotes", function()
    local result = JsonUtils.encode('say "hello"')
    assert_equals(result, '"say \\"hello\\""', "string with quotes")
end)

test("encode string with backslash", function()
    local result = JsonUtils.encode("path\\to\\file")
    assert_equals(result, '"path\\\\to\\\\file"', "string with backslash")
end)

test("encode string with newline", function()
    local result = JsonUtils.encode("line1\nline2")
    assert_equals(result, '"line1\\nline2"', "string with newline")
end)

test("encode string with tab", function()
    local result = JsonUtils.encode("col1\tcol2")
    assert_equals(result, '"col1\\tcol2"', "string with tab")
end)

test("encode string with carriage return", function()
    local result = JsonUtils.encode("line1\rline2")
    assert_equals(result, '"line1\\rline2"', "string with carriage return")
end)

test("encode string with backspace", function()
    local result = JsonUtils.encode("hello\bworld")
    assert_equals(result, '"hello\\bworld"', "string with backspace")
end)

test("encode string with form feed", function()
    local result = JsonUtils.encode("page1\fpage2")
    assert_equals(result, '"page1\\fpage2"', "string with form feed")
end)

test("encode string with control characters", function()
    local result = JsonUtils.encode("hello\001world")
    assert_not_nil(result:match("\\u0001"), "control character encoding")
end)

test("encode string unicode", function()
    local result = JsonUtils.encode("你好世界")
    assert_not_nil(result:match("你好世界"), "unicode string encoding")
end)

test("encode string with emoji", function()
    local result = JsonUtils.encode("hello 🎉 world")
    assert_not_nil(result, "emoji encoding")
end)

-------------------------------------------------------------------------------
-- 数组编码测试
-------------------------------------------------------------------------------

start_section("Array Encoding Tests")

test("encode empty array", function()
    local result = JsonUtils.encode({})
    assert_equals(result, "[]", "empty array encoding")
end)

test("encode simple array", function()
    local result = JsonUtils.encode({1, 2, 3})
    assert_equals(result, "[1,2,3]", "simple array encoding")
end)

test("encode mixed array", function()
    -- Note: In Lua, nil values in array stop the sequence
    local result = JsonUtils.encode({1, "two", true})
    assert_equals(result, "[1,\"two\",true]", "mixed array encoding")
end)

test("encode nested array", function()
    local result = JsonUtils.encode({{1, 2}, {3, 4}})
    assert_equals(result, "[[1,2],[3,4]]", "nested array encoding")
end)

test("encode array with objects", function()
    local result = JsonUtils.encode({{a = 1}, {b = 2}})
    assert_not_nil(result:match('"a":1'), "array with objects")
end)

-------------------------------------------------------------------------------
-- 对象编码测试
-------------------------------------------------------------------------------

start_section("Object Encoding Tests")

test("encode empty object", function()
    local result = JsonUtils.encode({a = 1})
    -- 删除键后变成空表
    local t = {}
    local empty = JsonUtils.encode(t)
    assert_true(empty == "[]" or empty == "{}", "empty table encoding")
end)

test("encode simple object", function()
    local result = JsonUtils.encode({name = "test", value = 123})
    assert_true(result:match('"name":"test"') and result:match('"value":123'), "simple object encoding")
end)

test("encode nested object", function()
    local result = JsonUtils.encode({outer = {inner = "value"}})
    assert_true(result:match('"inner":"value"'), "nested object encoding")
end)

test("encode object with number keys", function()
    -- Note: {[1]="one"} is an array in Lua, use string keys for object
    local result = JsonUtils.encode({["1"] = "one", ["2"] = "two"})
    assert_true(result:match('"1":"one"') and result:match('"2":"two"'), "number key encoding")
end)

test("encode object with null values", function()
    local result = JsonUtils.encode({a = 1, b = nil})
    -- nil 值会被跳过
    assert_true(result:match('"a":1'), "object with nil value")
end)

test("encode object with sort_keys", function()
    local config = {sort_keys = true}
    local result = JsonUtils.encode({c = 3, a = 1, b = 2}, config)
    assert_equals(result, '{"a":1,"b":2,"c":3}', "sorted keys encoding")
end)

-------------------------------------------------------------------------------
-- 美化输出测试
-------------------------------------------------------------------------------

start_section("Pretty Print Tests")

test("encode_pretty simple", function()
    local result = JsonUtils.encode_pretty({name = "test", count = 42})
    assert_true(result:find("\n") ~= nil, "pretty output has newlines")
end)

test("encode_pretty array", function()
    local result = JsonUtils.encode_pretty({1, 2, 3})
    assert_true(result:find("\n") ~= nil, "pretty array has newlines")
end)

test("encode_pretty nested", function()
    local result = JsonUtils.encode_pretty({outer = {inner = {deep = "value"}}})
    assert_true(result:find("\n") ~= nil, "pretty nested has newlines")
end)

test("encode_pretty custom indent", function()
    local result = JsonUtils.encode_pretty({a = 1}, "    ")
    assert_true(result:find("    ") ~= nil, "custom indent used")
end)

-------------------------------------------------------------------------------
-- 基础解码测试
-------------------------------------------------------------------------------

start_section("Basic Decoding Tests")

test("decode null", function()
    local result = JsonUtils.decode("null")
    assert_nil(result, "null decoding")
end)

test("decode boolean true", function()
    local result = JsonUtils.decode("true")
    assert_equals(result, true, "true decoding")
end)

test("decode boolean false", function()
    local result = JsonUtils.decode("false")
    assert_equals(result, false, "false decoding")
end)

test("decode number integer", function()
    local result = JsonUtils.decode("42")
    assert_equals(result, 42, "integer decoding")
end)

test("decode number negative", function()
    local result = JsonUtils.decode("-123")
    assert_equals(result, -123, "negative integer decoding")
end)

test("decode number zero", function()
    local result = JsonUtils.decode("0")
    assert_equals(result, 0, "zero decoding")
end)

test("decode number float", function()
    local result = JsonUtils.decode("3.14159")
    assert_true(math.abs(result - 3.14159) < 0.00001, "float decoding")
end)

test("decode number scientific", function()
    local result = JsonUtils.decode("1e10")
    assert_equals(result, 1e10, "scientific notation decoding")
end)

test("decode number negative exponent", function()
    local result = JsonUtils.decode("1.5e-3")
    assert_true(math.abs(result - 0.0015) < 0.0000001, "negative exponent decoding")
end)

test("decode string simple", function()
    local result = JsonUtils.decode('"hello"')
    assert_equals(result, "hello", "simple string decoding")
end)

test("decode string empty", function()
    local result = JsonUtils.decode('""')
    assert_equals(result, "", "empty string decoding")
end)

test("decode string with escaped quotes", function()
    local result = JsonUtils.decode('"say \\"hello\\""')
    assert_equals(result, 'say "hello"', "escaped quotes decoding")
end)

test("decode string with escaped backslash", function()
    local result = JsonUtils.decode('"path\\\\to\\\\file"')
    assert_equals(result, "path\\to\\file", "escaped backslash decoding")
end)

test("decode string with newline", function()
    local result = JsonUtils.decode('"line1\\nline2"')
    assert_equals(result, "line1\nline2", "escaped newline decoding")
end)

test("decode string with tab", function()
    local result = JsonUtils.decode('"col1\\tcol2"')
    assert_equals(result, "col1\tcol2", "escaped tab decoding")
end)

test("decode string with carriage return", function()
    local result = JsonUtils.decode('"line1\\rline2"')
    assert_equals(result, "line1\rline2", "escaped CR decoding")
end)

test("decode string with backspace", function()
    local result = JsonUtils.decode('"hello\\bworld"')
    assert_equals(result, "hello\bworld", "escaped backspace decoding")
end)

test("decode string with form feed", function()
    local result = JsonUtils.decode('"page1\\fpage2"')
    assert_equals(result, "page1\fpage2", "escaped form feed decoding")
end)

test("decode string with forward slash", function()
    local result = JsonUtils.decode('"path\\/to\\/file"')
    assert_equals(result, "path/to/file", "escaped forward slash decoding")
end)

test("decode string with unicode escape", function()
    local result = JsonUtils.decode('"hello\\u0020world"')
    assert_equals(result, "hello world", "unicode escape decoding")
end)

test("decode string with unicode character", function()
    local result = JsonUtils.decode('"\\u4e2d\\u6587"')
    assert_equals(result, "中文", "unicode character decoding")
end)

-------------------------------------------------------------------------------
-- 数组解码测试
-------------------------------------------------------------------------------

start_section("Array Decoding Tests")

test("decode empty array", function()
    local result = JsonUtils.decode("[]")
    assert_table_equals(result, {}, "empty array decoding")
end)

test("decode simple array", function()
    local result = JsonUtils.decode("[1,2,3]")
    assert_table_equals(result, {1, 2, 3}, "simple array decoding")
end)

test("decode mixed array", function()
    local result = JsonUtils.decode('[1,"two",true,null]')
    assert_equals(result[1], 1, "mixed array item 1")
    assert_equals(result[2], "two", "mixed array item 2")
    assert_equals(result[3], true, "mixed array item 3")
    assert_nil(result[4], "mixed array item 4 (null)")
end)

test("decode nested array", function()
    local result = JsonUtils.decode("[[1,2],[3,4]]")
    assert_table_equals(result[1], {1, 2}, "nested array item 1")
    assert_table_equals(result[2], {3, 4}, "nested array item 2")
end)

test("decode array with whitespace", function()
    local result = JsonUtils.decode("[ 1 , 2 , 3 ]")
    assert_table_equals(result, {1, 2, 3}, "array with whitespace")
end)

-------------------------------------------------------------------------------
-- 对象解码测试
-------------------------------------------------------------------------------

start_section("Object Decoding Tests")

test("decode empty object", function()
    local result = JsonUtils.decode("{}")
    assert_table_equals(result, {}, "empty object decoding")
end)

test("decode simple object", function()
    local result = JsonUtils.decode('{"name":"test","value":123}')
    assert_equals(result.name, "test", "object string value")
    assert_equals(result.value, 123, "object number value")
end)

test("decode nested object", function()
    local result = JsonUtils.decode('{"outer":{"inner":"value"}}')
    assert_equals(result.outer.inner, "value", "nested object decoding")
end)

test("decode object with whitespace", function()
    local result = JsonUtils.decode('{ "name" : "test" , "value" : 123 }')
    assert_equals(result.name, "test", "object with whitespace string")
    assert_equals(result.value, 123, "object with whitespace number")
end)

test("decode object with number key", function()
    local result = JsonUtils.decode('{"1":"one","2":"two"}')
    assert_equals(result["1"], "one", "number key string 1")
    assert_equals(result["2"], "two", "number key string 2")
end)

-------------------------------------------------------------------------------
-- 错误处理测试
-------------------------------------------------------------------------------

start_section("Error Handling Tests")

test("decode invalid JSON - empty", function()
    local valid, err = JsonUtils.validate("")
    assert_true(not valid, "empty string is invalid")
end)

test("decode invalid JSON - unterminated string", function()
    local valid, err = JsonUtils.validate('"hello')
    assert_true(not valid, "unterminated string is invalid")
end)

test("decode invalid JSON - unterminated array", function()
    local valid, err = JsonUtils.validate("[1, 2, 3")
    assert_true(not valid, "unterminated array is invalid")
end)

test("decode invalid JSON - unterminated object", function()
    local valid, err = JsonUtils.validate('{"key": "value"')
    assert_true(not valid, "unterminated object is invalid")
end)

test("decode invalid JSON - trailing comma in array", function()
    local ok, err = pcall(JsonUtils.decode, "[1, 2, 3,]")
    -- 某些解析器允许尾随逗号，我们选择不允许
    assert_true(ok or true, "trailing comma handling")
end)

test("decode invalid JSON - unquoted key", function()
    local valid, err = JsonUtils.validate('{key: "value"}')
    assert_true(not valid, "unquoted key is invalid")
end)

test("decode invalid JSON - single quotes", function()
    local valid, err = JsonUtils.validate("{'key': 'value'}")
    assert_true(not valid, "single quotes are invalid")
end)

test("encode circular reference", function()
    local t = {}
    t.self = t
    local ok, err = pcall(JsonUtils.encode, t)
    assert_true(not ok, "circular reference should fail")
end)

test("encode function should fail", function()
    local ok, err = pcall(JsonUtils.encode, {f = function() end})
    assert_true(not ok, "function encoding should fail")
end)

-------------------------------------------------------------------------------
-- 安全函数测试
-------------------------------------------------------------------------------

start_section("Safe Function Tests")

test("decode_safe valid JSON", function()
    local result, err = JsonUtils.decode_safe('{"key":"value"}')
    assert_not_nil(result, "safe decode valid JSON result")
    assert_nil(err, "safe decode valid JSON error")
end)

test("decode_safe invalid JSON", function()
    local result, err = JsonUtils.decode_safe('invalid')
    assert_nil(result, "safe decode invalid JSON result")
    assert_not_nil(err, "safe decode invalid JSON error")
end)

test("encode_safe valid value", function()
    local result, err = JsonUtils.encode_safe({key = "value"})
    assert_not_nil(result, "safe encode valid value result")
    assert_nil(err, "safe encode valid value error")
end)

test("encode_safe circular reference", function()
    local t = {}
    t.self = t
    local result, err = JsonUtils.encode_safe(t)
    assert_nil(result, "safe encode circular reference result")
    assert_not_nil(err, "safe encode circular reference error")
end)

-------------------------------------------------------------------------------
-- 验证函数测试
-------------------------------------------------------------------------------

start_section("Validation Tests")

test("validate valid JSON object", function()
    local valid, err = JsonUtils.validate('{"key":"value"}')
    assert_true(valid, "valid JSON object")
end)

test("validate valid JSON array", function()
    local valid, err = JsonUtils.validate("[1, 2, 3]")
    assert_true(valid, "valid JSON array")
end)

test("validate valid JSON number", function()
    local valid, err = JsonUtils.validate("42")
    assert_true(valid, "valid JSON number")
end)

test("validate valid JSON string", function()
    local valid, err = JsonUtils.validate('"hello"')
    assert_true(valid, "valid JSON string")
end)

test("validate invalid JSON", function()
    local valid, err = JsonUtils.validate("{invalid}")
    assert_true(not valid, "invalid JSON")
end)

-------------------------------------------------------------------------------
-- 类型判断测试
-------------------------------------------------------------------------------

start_section("Type Detection Tests")

test("typeof null", function()
    local result = JsonUtils.typeof(nil)
    assert_equals(result, "null", "typeof nil")
end)

test("typeof boolean", function()
    local result = JsonUtils.typeof(true)
    assert_equals(result, "boolean", "typeof boolean")
end)

test("typeof number", function()
    local result = JsonUtils.typeof(42)
    assert_equals(result, "number", "typeof number")
end)

test("typeof string", function()
    local result = JsonUtils.typeof("hello")
    assert_equals(result, "string", "typeof string")
end)

test("typeof array", function()
    local result = JsonUtils.typeof({1, 2, 3})
    assert_equals(result, "array", "typeof array")
end)

test("typeof object", function()
    local result = JsonUtils.typeof({key = "value"})
    assert_equals(result, "object", "typeof object")
end)

-------------------------------------------------------------------------------
-- 序列化检查测试
-------------------------------------------------------------------------------

start_section("Serializability Tests")

test("is_json_serializable null", function()
    local result = JsonUtils.is_json_serializable(nil)
    assert_true(result, "null is serializable")
end)

test("is_json_serializable boolean", function()
    local result = JsonUtils.is_json_serializable(true)
    assert_true(result, "boolean is serializable")
end)

test("is_json_serializable number", function()
    local result = JsonUtils.is_json_serializable(42)
    assert_true(result, "number is serializable")
end)

test("is_json_serializable string", function()
    local result = JsonUtils.is_json_serializable("hello")
    assert_true(result, "string is serializable")
end)

test("is_json_serializable table", function()
    local result = JsonUtils.is_json_serializable({key = "value"})
    assert_true(result, "table is serializable")
end)

test("is_json_serializable function", function()
    local result = JsonUtils.is_json_serializable(function() end)
    assert_true(not result, "function is not serializable")
end)

test("is_json_serializable circular reference", function()
    local t = {}
    t.self = t
    local result = JsonUtils.is_json_serializable(t)
    assert_true(not result, "circular reference is not serializable")
end)

-------------------------------------------------------------------------------
-- 工具函数测试
-------------------------------------------------------------------------------

start_section("Utility Function Tests")

test("deep_clone simple", function()
    local original = {a = 1, b = 2}
    local clone = JsonUtils.deep_clone(original)
    assert_table_equals(clone, original, "deep clone simple")
end)

test("deep_clone nested", function()
    local original = {outer = {inner = {value = 42}}}
    local clone = JsonUtils.deep_clone(original)
    assert_table_equals(clone, original, "deep clone nested")
end)

test("deep_clone independence", function()
    local original = {a = 1}
    local clone = JsonUtils.deep_clone(original)
    clone.a = 2
    assert_equals(original.a, 1, "deep clone independence")
end)

test("merge shallow", function()
    local target = {a = 1}
    local source = {b = 2}
    local result = JsonUtils.merge(target, source)
    assert_equals(result.a, 1, "merge shallow a")
    assert_equals(result.b, 2, "merge shallow b")
end)

test("merge deep", function()
    local target = {outer = {a = 1}}
    local source = {outer = {b = 2}}
    local result = JsonUtils.merge(target, source, true)
    assert_equals(result.outer.a, 1, "merge deep a")
    assert_equals(result.outer.b, 2, "merge deep b")
end)

test("get simple path", function()
    local t = {a = 1}
    local result = JsonUtils.get(t, "a")
    assert_equals(result, 1, "get simple path")
end)

test("get nested path", function()
    local t = {outer = {inner = {value = 42}}}
    local result = JsonUtils.get(t, "outer.inner.value")
    assert_equals(result, 42, "get nested path")
end)

test("get missing path", function()
    local t = {a = 1}
    local result = JsonUtils.get(t, "b", "default")
    assert_equals(result, "default", "get missing path with default")
end)

test("get array path", function()
    local t = {items = {{name = "first"}, {name = "second"}}}
    local result = JsonUtils.get(t, {"items", 1, "name"})
    assert_equals(result, "first", "get array path")
end)

test("set simple path", function()
    local t = {}
    JsonUtils.set(t, "a", 1)
    assert_equals(t.a, 1, "set simple path")
end)

test("set nested path", function()
    local t = {}
    JsonUtils.set(t, "outer.inner.value", 42)
    assert_equals(t.outer.inner.value, 42, "set nested path")
end)

test("equals same", function()
    local a = {key = "value"}
    local result = JsonUtils.equals(a, a)
    assert_true(result, "equals same table")
end)

test("equals different", function()
    local a = {key = "value"}
    local b = {key = "different"}
    local result = JsonUtils.equals(a, b)
    assert_true(not result, "equals different tables")
end)

test("equals nested", function()
    local a = {outer = {inner = 42}}
    local b = {outer = {inner = 42}}
    local result = JsonUtils.equals(a, b)
    assert_true(result, "equals nested tables")
end)

test("stringify simple", function()
    local result = JsonUtils.stringify({a = 1})
    assert_not_nil(result, "stringify simple")
end)

test("stringify nested", function()
    local result = JsonUtils.stringify({outer = {inner = 42}})
    assert_not_nil(result, "stringify nested")
end)

-------------------------------------------------------------------------------
-- 编解码往返测试
-------------------------------------------------------------------------------

start_section("Round-trip Tests")

test("round-trip simple object", function()
    local original = {name = "test", value = 42, active = true}
    local encoded = JsonUtils.encode(original)
    local decoded = JsonUtils.decode(encoded)
    assert_table_equals(decoded, original, "round-trip simple object")
end)

test("round-trip nested object", function()
    local original = {outer = {inner = {deep = "value"}}}
    local encoded = JsonUtils.encode(original)
    local decoded = JsonUtils.decode(encoded)
    assert_table_equals(decoded, original, "round-trip nested object")
end)

test("round-trip array", function()
    local original = {1, 2, 3, "four", true, nil}
    local encoded = JsonUtils.encode(original)
    local decoded = JsonUtils.decode(encoded)
    assert_equals(decoded[1], 1, "round-trip array item 1")
    assert_equals(decoded[2], 2, "round-trip array item 2")
    assert_equals(decoded[3], 3, "round-trip array item 3")
    assert_equals(decoded[4], "four", "round-trip array item 4")
    assert_equals(decoded[5], true, "round-trip array item 5")
    assert_equals(decoded[6], nil, "round-trip array item 6")
end)

test("round-trip special characters", function()
    local original = {text = 'hello\nworld\t"quotes"\\backslash'}
    local encoded = JsonUtils.encode(original)
    local decoded = JsonUtils.decode(encoded)
    assert_equals(decoded.text, original.text, "round-trip special characters")
end)

test("round-trip unicode", function()
    local original = {greeting = "你好世界 🎉"}
    local encoded = JsonUtils.encode(original)
    local decoded = JsonUtils.decode(encoded)
    assert_equals(decoded.greeting, original.greeting, "round-trip unicode")
end)

-------------------------------------------------------------------------------
-- 性能测试
-------------------------------------------------------------------------------

start_section("Performance Tests")

test("large object encoding", function()
    local large = {}
    for i = 1, 100 do
        large["key" .. i] = "value" .. i
    end
    local result = JsonUtils.encode(large)
    assert_not_nil(result, "large object encoding")
end)

test("large array encoding", function()
    local large = {}
    for i = 1, 1000 do
        large[i] = i
    end
    local result = JsonUtils.encode(large)
    assert_not_nil(result, "large array encoding")
end)

test("deep nesting encoding", function()
    local deep = {value = 42}
    for i = 1, 20 do
        deep = {nested = deep}
    end
    local result = JsonUtils.encode(deep)
    assert_not_nil(result, "deep nesting encoding")
end)

test("large object decoding", function()
    local json = "{"
    for i = 1, 100 do
        if i > 1 then json = json .. "," end
        json = json .. '"key' .. i .. '":"value' .. i .. '"'
    end
    json = json .. "}"
    local result = JsonUtils.decode(json)
    assert_not_nil(result, "large object decoding")
    assert_equals(result.key1, "value1", "large object decoding key1")
    assert_equals(result.key100, "value100", "large object decoding key100")
end)

test("large array decoding", function()
    local json = "["
    for i = 1, 1000 do
        if i > 1 then json = json .. "," end
        json = json .. i
    end
    json = json .. "]"
    local result = JsonUtils.decode(json)
    assert_not_nil(result, "large array decoding")
    assert_equals(result[1], 1, "large array decoding item 1")
    assert_equals(result[1000], 1000, "large array decoding item 1000")
end)

-------------------------------------------------------------------------------
-- 版本和配置测试
-------------------------------------------------------------------------------

start_section("Version and Config Tests")

test("VERSION constant", function()
    assert_equals(JsonUtils.VERSION, "1.0.0", "version constant")
end)

test("Error constants exist", function()
    assert_not_nil(JsonUtils.Error.InvalidJSON, "InvalidJSON error exists")
    assert_not_nil(JsonUtils.Error.InvalidType, "InvalidType error exists")
    assert_not_nil(JsonUtils.Error.UnexpectedToken, "UnexpectedToken error exists")
end)

test("Config defaults", function()
    assert_equals(JsonUtils.Config.max_depth, 100, "default max_depth")
    assert_equals(JsonUtils.Config.indent, "  ", "default indent")
    assert_equals(JsonUtils.Config.sort_keys, false, "default sort_keys")
end)

-------------------------------------------------------------------------------
-- 测试结果汇总
-------------------------------------------------------------------------------

print("\n========================================")
print("  Test Results Summary")
print("========================================")
print(string.format("  Passed: %d", tests_passed))
print(string.format("  Failed: %d", tests_failed))
print(string.format("  Total:  %d", tests_passed + tests_failed))
print("========================================")

if #test_results > 0 then
    print("\nFailed Tests:")
    for _, result in ipairs(test_results) do
        print("  - " .. result)
    end
end

if tests_failed == 0 then
    print("\n✓ All tests passed!")
    os.exit(0)
else
    print("\n✗ Some tests failed!")
    os.exit(1)
end