#!/usr/bin/env lua
---
-- String Utilities Examples
-- 字符串工具函数使用示例
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local StringUtils = dofile(path .. "../mod.lua")

print("📝 String Utilities Examples")
print(string.rep("=", 50))

-------------------------------------------------------------------------------
-- 示例 1: 空白处理
-------------------------------------------------------------------------------
print("\n1️⃣ 空白处理")
print("-" .. string.rep("-", 49))

local input = "  Hello, World!  "
print("原始：'" .. input .. "'")
print("trim: '" .. StringUtils.trim(input) .. "'")
print("is_empty(''): " .. tostring(StringUtils.is_empty("")))
print("is_blank('   '): " .. tostring(StringUtils.is_blank("   ")))

-------------------------------------------------------------------------------
-- 示例 2: 大小写转换
-------------------------------------------------------------------------------
print("\n2️⃣ 大小写转换")
print("-" .. string.rep("-", 49))

local camelCase = "myVariableName"
print("camelCase: " .. camelCase)
print("→ snake_case: " .. StringUtils.to_snake_case(camelCase))
print("→ PascalCase: " .. StringUtils.to_pascal_case(camelCase))

local snake_case = "my_variable_name"
print("\nsnake_case: " .. snake_case)
print("→ camelCase: " .. StringUtils.to_camel_case(snake_case))
print("→ PascalCase: " .. StringUtils.to_pascal_case(snake_case))

-------------------------------------------------------------------------------
-- 示例 3: 字符串查找
-------------------------------------------------------------------------------
print("\n3️⃣ 字符串查找")
print("-" .. string.rep("-", 49))

local text = "The quick brown fox jumps over the lazy dog"
print("文本：" .. text)
print("contains 'fox': " .. tostring(StringUtils.contains(text, "fox")))
print("starts_with 'The': " .. tostring(StringUtils.starts_with(text, "The")))
print("ends_with 'dog': " .. tostring(StringUtils.ends_with(text, "dog")))

local positions = StringUtils.find_all(text, "the")
print("所有 'the' 的位置：" .. table.concat(positions, ", "))

-------------------------------------------------------------------------------
-- 示例 4: 字符串替换
-------------------------------------------------------------------------------
print("\n4️⃣ 字符串替换")
print("-" .. string.rep("-", 49))

local sentence = "I like cats. Cats are cute. I love cats!"
print("原始：" .. sentence)
print("replace_first: " .. StringUtils.replace_first(sentence, "cats", "dogs"))
print("replace_last: " .. StringUtils.replace_last(sentence, "cats", "dogs"))
print("replace_all: " .. StringUtils.replace_all(sentence, "cats", "dogs"))

-------------------------------------------------------------------------------
-- 示例 5: 分割与连接
-------------------------------------------------------------------------------
print("\n5️⃣ 分割与连接")
print("-" .. string.rep("-", 49))

local csv = "apple,banana,cherry,date"
local items = StringUtils.split(csv, ",")
print("CSV: " .. csv)
print("分割后：" .. table.concat(items, " | "))

local joined = StringUtils.join(items, " + ")
print("连接后：" .. joined)

-------------------------------------------------------------------------------
-- 示例 6: 填充与截断
-------------------------------------------------------------------------------
print("\n6️⃣ 填充与截断")
print("-" .. string.rep("-", 49))

print("数字格式化:")
for i = 1, 5 do
    local num = tostring(i)
    print(string.format("  %s → %s", num, StringUtils.pad_left(num, 3, "0")))
end

local long_text = "This is a very long title that needs to be truncated for display"
print("\n长文本截断:")
print("原始：" .. long_text)
print("truncate(30): " .. StringUtils.truncate(long_text, 30))
print("truncate_words(30): " .. StringUtils.truncate_words(long_text, 30))

-------------------------------------------------------------------------------
-- 示例 7: 验证函数
-------------------------------------------------------------------------------
print("\n7️⃣ 验证函数")
print("-" .. string.rep("-", 49))

local test_cases = {
    { value = "test@example.com", fn = "is_email", expected = true },
    { value = "invalid-email", fn = "is_email", expected = false },
    { value = "https://example.com", fn = "is_url", expected = true },
    { value = "192.168.1.1", fn = "is_ipv4", expected = true },
    { value = "256.1.1.1", fn = "is_ipv4", expected = false },
    { value = "abc123", fn = "is_alphanumeric", expected = true },
}

for _, test in ipairs(test_cases) do
    local result = StringUtils[test.fn](test.value)
    local status = result == test.expected and "✅" or "❌"
    print(string.format("%s %s('%s') = %s", status, test.fn, test.value, tostring(result)))
end

-------------------------------------------------------------------------------
-- 示例 8: 格式化函数
-------------------------------------------------------------------------------
print("\n8️⃣ 格式化函数")
print("-" .. string.rep("-", 49))

print("数字格式化:")
print("  1234567 → " .. StringUtils.format_number(1234567))
print("  -1234567 → " .. StringUtils.format_number(-1234567))

print("\n字节格式化:")
local sizes = { 512, 1536, 1048576, 1073741824 }
for _, bytes in ipairs(sizes) do
    print("  " .. bytes .. " → " .. StringUtils.format_bytes(bytes))
end

print("\n时间格式化:")
print("  61 秒 → " .. StringUtils.format_time(61))
print("  3661 秒 → " .. StringUtils.format_time(3661))
print("  90061 秒 → " .. StringUtils.format_time(90061))

-------------------------------------------------------------------------------
-- 示例 9: 编码解码
-------------------------------------------------------------------------------
print("\n9️⃣ 编码解码")
print("-" .. string.rep("-", 49))

local original = "Hello, 世界!"
print("原始：" .. original)

local url_encoded = StringUtils.url_encode(original)
print("URL 编码：" .. url_encoded)
print("URL 解码：" .. StringUtils.url_decode(url_encoded))

local html = "<script>alert('XSS')</script>"
print("\nHTML 编码:")
print("原始：" .. html)
print("编码：" .. StringUtils.html_encode(html))

local base64_text = "AllToolkit String Utils"
print("\nBase64:")
print("原始：" .. base64_text)
local encoded = StringUtils.base64_encode(base64_text)
print("编码：" .. encoded)
print("解码：" .. StringUtils.base64_decode(encoded))

-------------------------------------------------------------------------------
-- 示例 10: 相似度计算
-------------------------------------------------------------------------------
print("\n🔟 相似度计算")
print("-" .. string.rep("-", 49))

local pairs_to_compare = {
    { "kitten", "sitting" },
    { "hello", "hello" },
    { "hello", "hallo" },
    { "abc", "xyz" },
}

for _, pair in ipairs(pairs_to_compare) do
    local s1, s2 = pair[1], pair[2]
    local distance = StringUtils.levenshtein(s1, s2)
    local similarity = StringUtils.similarity(s1, s2)
    print(string.format("'%s' vs '%s': 距离=%d, 相似度=%.2f", s1, s2, distance, similarity))
end

-------------------------------------------------------------------------------
-- 示例 11: 工具函数
-------------------------------------------------------------------------------
print("\n1️⃣1️⃣ 工具函数")
print("-" .. string.rep("-", 49))

print("随机字符串:")
print("  10 位：" .. StringUtils.random(10))
print("  6 位数字：" .. StringUtils.random(6, "0123456789"))
print("  UUID: " .. StringUtils.uuid())

print("\n字符串构建器:")
local builder = StringUtils.builder()
builder:append("function ")
builder:append("calculate")
builder:append("(")
builder:append("x, y")
builder:append(")")
print("  结果：" .. builder:to_string())

-------------------------------------------------------------------------------
-- 示例 12: 模板与插值
-------------------------------------------------------------------------------
print("\n1️⃣2️⃣ 模板与插值")
print("-" .. string.rep("-", 49))

local template = "Hello, {name}! You are {age} years old."
local data = { name = "Alice", age = 25 }
print("模板：" .. template)
print("数据：" .. table.concat({ "name=" .. data.name, "age=" .. data.age }, ", "))
print("结果：" .. StringUtils.template(template, data))

print("\n字符串插值:")
local expr = "Price: ${100 * 1.1} (with 10% tax)"
print("表达式：" .. expr)
print("结果：" .. StringUtils.interpolate(expr, {}))

-------------------------------------------------------------------------------
-- 示例 13: 综合应用 - 用户注册验证
-------------------------------------------------------------------------------
print("\n1️⃣3️⃣ 综合应用：用户注册验证")
print("-" .. string.rep("-", 49))

local function validate_registration(username, email, password)
    local errors = {}
    
    -- 用户名验证
    if StringUtils.is_blank(username) then
        table.insert(errors, "Username cannot be empty")
    elseif #username < 3 then
        table.insert(errors, "Username must be at least 3 characters")
    elseif not StringUtils.is_alphanumeric(username) then
        table.insert(errors, "Username must be alphanumeric")
    end
    
    -- 邮箱验证
    if not StringUtils.is_email(email) then
        table.insert(errors, "Invalid email format")
    end
    
    -- 密码验证
    if #password < 8 then
        table.insert(errors, "Password must be at least 8 characters")
    end
    
    return #errors == 0, errors
end

local test_users = {
    { "ab", "invalid", "123" },
    { "alice", "alice@example.com", "securepass123" },
    { "bob!", "bob@example", "password" },
}

for i, user in ipairs(test_users) do
    local valid, errors = validate_registration(user[1], user[2], user[3])
    print(string.format("\n用户 %d:", i))
    print("  用户名：" .. user[1])
    print("  邮箱：" .. user[2])
    print("  验证：" .. (valid and "✅ 通过" or "❌ 失败"))
    if not valid then
        print("  错误：" .. table.concat(errors, ", "))
    end
end

-------------------------------------------------------------------------------
-- 示例 14: 综合应用 - 日志格式化
-------------------------------------------------------------------------------
print("\n1️⃣4️⃣ 综合应用：日志格式化")
print("-" .. string.rep("-", 49))

local function format_log_entry(level, message, context)
    local timestamp = StringUtils.format_datetime(nil, "%Y-%m-%d %H:%M:%S")
    local formatted_msg = StringUtils.template(message, context or {})
    local level_padded = StringUtils.pad_right(level, 7)
    return string.format("[%s] [%s] %s", timestamp, level_padded, formatted_msg)
end

local log_entries = {
    { "INFO", "User {user} logged in from {ip}", { user = "Alice", ip = "192.168.1.100" } },
    { "WARN", "Failed login attempt for {user}", { user = "Bob" } },
    { "ERROR", "Database connection failed: {error}", { error = "timeout" } },
}

for _, entry in ipairs(log_entries) do
    print(format_log_entry(entry[1], entry[2], entry[3]))
end

-------------------------------------------------------------------------------
-- 示例 15: 综合应用 - 模糊搜索
-------------------------------------------------------------------------------
print("\n1️⃣5️⃣ 综合应用：模糊搜索")
print("-" .. string.rep("-", 49))

local function fuzzy_search(query, items, threshold)
    threshold = threshold or 0.5
    local results = {}
    
    query = StringUtils.lower(StringUtils.trim(query))
    
    for _, item in ipairs(items) do
        local item_lower = StringUtils.lower(item)
        local score = StringUtils.similarity(query, item_lower)
        
        if score >= threshold then
            table.insert(results, {
                item = item,
                score = score,
            })
        end
    end
    
    -- 按相似度排序
    table.sort(results, function(a, b) return a.score > b.score end)
    
    return results
end

local fruits = { "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew" }
local search_queries = { "appel", "banan", "grape" }

print("水果列表：" .. table.concat(fruits, ", "))
print()

for _, query in ipairs(search_queries) do
    print(string.format("搜索 '%s':", query))
    local results = fuzzy_search(query, fruits)
    if #results > 0 then
        for _, result in ipairs(results) do
            print(string.format("  - %s (相似度：%.2f)", result.item, result.score))
        end
    else
        print("  无匹配结果")
    end
    print()
end

-------------------------------------------------------------------------------
print("\n" .. string.rep("=", 50))
print("✅ 所有示例执行完成!")
print(string.rep("=", 50))
