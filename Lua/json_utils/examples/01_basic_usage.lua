---
-- JSON Utilities - Basic Usage Examples
-- 基础使用示例
--
-- 展示 JSON 编码、解码、验证等基础功能
--

local JsonUtils = require("mod")

print("=== JSON Utilities Basic Usage ===\n")

-------------------------------------------------------------------------------
-- 1. 基础编码
-------------------------------------------------------------------------------

print("1. Basic Encoding")
print("-------------------")

-- 编码简单值
print("null:", JsonUtils.encode(nil))
print("true:", JsonUtils.encode(true))
print("false:", JsonUtils.encode(false))
print("number:", JsonUtils.encode(42))
print("string:", JsonUtils.encode("hello world"))

-- 编码数组
local arr = {1, 2, 3, "four", true}
print("array:", JsonUtils.encode(arr))

-- 编码对象
local obj = {
    name = "Alice",
    age = 30,
    active = true,
    email = "alice@example.com"
}
print("object:", JsonUtils.encode(obj))

print("")

-------------------------------------------------------------------------------
-- 2. 美化输出
-------------------------------------------------------------------------------

print("2. Pretty Output")
print("-----------------")

local data = {
    user = {
        name = "Bob",
        age = 25,
        contacts = {
            email = "bob@example.com",
            phone = "123-456-7890"
        },
        hobbies = {"reading", "coding", "music"}
    },
    metadata = {
        version = "1.0.0",
        created = "2024-01-01"
    }
}

print("Pretty JSON:")
print(JsonUtils.encode_pretty(data))

print("")

-------------------------------------------------------------------------------
-- 3. 基础解码
-------------------------------------------------------------------------------

print("3. Basic Decoding")
print("-----------------")

-- 解码简单值
print("null:", JsonUtils.decode("null"))
print("true:", JsonUtils.decode("true"))
print("false:", JsonUtils.decode("false"))
print("number:", JsonUtils.decode("42.5"))
print("string:", JsonUtils.decode('"hello"'))

-- 解码数组
local decodedArr = JsonUtils.decode("[1, 2, 3]")
print("array[1]:", decodedArr[1])
print("array[2]:", decodedArr[2])
print("array[3]:", decodedArr[3])

-- 解码对象
local decodedObj = JsonUtils.decode('{"name":"Alice","age":30}')
print("object.name:", decodedObj.name)
print("object.age:", decodedObj.age)

print("")

-------------------------------------------------------------------------------
-- 4. 安全解码
-------------------------------------------------------------------------------

print("4. Safe Decoding")
print("----------------")

-- 有效 JSON
local result, err = JsonUtils.decode_safe('{"key":"value"}')
if err then
    print("Error:", err)
else
    print("Result:", result.key)
end

-- 无效 JSON
local result2, err2 = JsonUtils.decode_safe('invalid json')
if err2 then
    print("Invalid JSON detected:", err2)
else
    print("Result:", result2)
end

print("")

-------------------------------------------------------------------------------
-- 5. 验证
-------------------------------------------------------------------------------

print("5. Validation")
print("-------------")

local valid1, err1 = JsonUtils.validate('{"name":"test"}')
print("Valid JSON object:", valid1)

local valid2, err2 = JsonUtils.validate("[1, 2, 3]")
print("Valid JSON array:", valid2)

local valid3, err3 = JsonUtils.validate("{invalid}")
print("Invalid JSON:", not valid3)
print("Error:", err3)

print("")

-------------------------------------------------------------------------------
-- 6. 类型判断
-------------------------------------------------------------------------------

print("6. Type Detection")
print("-----------------")

print("null:", JsonUtils.typeof(nil))
print("boolean:", JsonUtils.typeof(true))
print("number:", JsonUtils.typeof(42))
print("string:", JsonUtils.typeof("hello"))
print("array:", JsonUtils.typeof({1, 2, 3}))
print("object:", JsonUtils.typeof({key = "value"}))

print("")

-------------------------------------------------------------------------------
-- 7. 特殊字符处理
-------------------------------------------------------------------------------

print("7. Special Characters")
print("---------------------")

local special = {
    text = 'Line1\nLine2\tTabbed',
    path = "C:\\Users\\Documents",
    quote = 'He said "Hello"',
    mixed = "Newline\nTab\tQuote\"Backslash\\"
}

print("Encoded special characters:")
print(JsonUtils.encode(special))

-- 解码回来
local decoded = JsonUtils.decode(JsonUtils.encode(special))
print("\nDecoded back:")
print("text:", decoded.text)
print("path:", decoded.path)
print("quote:", decoded.quote)

print("")

-------------------------------------------------------------------------------
-- 8. Unicode 支持
-------------------------------------------------------------------------------

print("8. Unicode Support")
print("------------------")

local unicode = {
    greeting = "你好世界",
    emoji = "🎉🎊🎁",
    mixed = "Hello 世界 🌍",
    japanese = "こんにちは"
}

print("Unicode encoding:")
print(JsonUtils.encode(unicode))

print("\nPretty Unicode:")
print(JsonUtils.encode_pretty(unicode))

print("")

-------------------------------------------------------------------------------
-- 9. 配置选项
-------------------------------------------------------------------------------

print("9. Configuration Options")
print("------------------------")

-- 排序键
local unsorted = {c = 3, a = 1, b = 2}
print("Unsorted:", JsonUtils.encode(unsorted))

local sorted = JsonUtils.encode(unsorted, {sort_keys = true})
print("Sorted:", sorted)

-- 自定义缩进
local customIndent = JsonUtils.encode_pretty({a = 1, b = 2}, "    ")
print("Custom indent (4 spaces):")
print(customIndent)

print("")

-------------------------------------------------------------------------------
-- 10. 往返测试
-------------------------------------------------------------------------------

print("10. Round-trip Test")
print("-------------------")

local original = {
    name = "Test",
    values = {1, 2, 3},
    nested = {
        level1 = {
            level2 = {
                data = "deep"
            }
        }
    },
    active = true,
    count = 42
}

print("Original:")
print(JsonUtils.encode_pretty(original))

local encoded = JsonUtils.encode(original)
local decoded = JsonUtils.decode(encoded)

print("\nDecoded:")
print(JsonUtils.encode_pretty(decoded))

print("\nAre they equal?", JsonUtils.equals(original, decoded))

print("\n=== End of Basic Usage Examples ===")