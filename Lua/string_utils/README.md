# String Utilities 📝

字符串处理工具函数库 - 零依赖，生产就绪

## 📖 简介

`string_utils` 提供全面的字符串处理功能，仅使用 Lua 标准库，无需任何外部依赖。

### 核心功能

| 功能分类 | 说明 |
|----------|------|
| 空白处理 | trim、is_empty、is_blank |
| 大小写转换 | lower、upper、capitalize、title、snake_case、camelCase、PascalCase |
| 字符串查找 | contains、starts_with、ends_with、find_all |
| 字符串替换 | replace_first、replace_last、replace_all、replace_n |
| 分割连接 | split、lines、join |
| 填充截断 | pad_left、pad_right、pad_center、truncate |
| 验证函数 | is_alpha、is_digit、is_email、is_url、is_ipv4 |
| 格式化 | format_number、format_bytes、format_time、format_datetime |
| 编码解码 | URL、HTML、Base64 |
| 相似度 | Levenshtein 距离、相似度计算 |
| 工具函数 | random、uuid、builder、template、interpolate |

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.lua` 到你的项目即可使用。

```bash
cp AllToolkit/Lua/string_utils/mod.lua your_project/string_utils.lua
```

### 基础示例

```lua
local StringUtils = require("string_utils")

-- 空白处理
print(StringUtils.trim("  hello  "))        --> "hello"
print(StringUtils.is_empty(""))             --> true

-- 大小写转换
print(StringUtils.upper("hello"))           --> "HELLO"
print(StringUtils.to_snake_case("camelCase")) --> "camel_case"

-- 字符串查找
print(StringUtils.contains("hello world", "world"))  --> true
print(StringUtils.starts_with("hello", "he"))        --> true

-- 字符串替换
print(StringUtils.replace_all("a b a", "a", "x"))    --> "x b x"

-- 分割连接
local parts = StringUtils.split("a,b,c", ",")
print(parts[1])                                      --> "a"

-- 验证
print(StringUtils.is_email("test@example.com"))      --> true
print(StringUtils.is_ipv4("192.168.1.1"))            --> true

-- 格式化
print(StringUtils.format_number(1234567))            --> "1,234,567"
print(StringUtils.format_bytes(1536))                --> "1.50 KB"

-- 编码
print(StringUtils.url_encode("hello world"))         --> "hello+world"
print(StringUtils.base64_encode("Hello"))            --> "SGVsbG8="
```

---

## 📚 API 参考

### 空白处理

#### `is_empty(s)`

检查是否为 nil 或空字符串。

```lua
StringUtils.is_empty(nil)     --> true
StringUtils.is_empty("")      --> true
StringUtils.is_empty(" ")     --> false
```

#### `is_blank(s)`

检查是否为 nil、空字符串或只包含空白。

```lua
StringUtils.is_blank("   ")   --> true
StringUtils.is_blank(" a ")   --> false
```

#### `trim(s)` / `trim_left(s)` / `trim_right(s)`

去除空白字符。

```lua
StringUtils.trim("  hello  ")     --> "hello"
StringUtils.trim_left("  hello")  --> "hello"
StringUtils.trim_right("hello  ") --> "hello"
```

---

### 大小写转换

#### `lower(s)` / `upper(s)`

大小写转换。

```lua
StringUtils.lower("HELLO")  --> "hello"
StringUtils.upper("hello")  --> "HELLO"
```

#### `capitalize(s)`

首字母大写。

```lua
StringUtils.capitalize("hello")  --> "Hello"
```

#### `title(s)`

每个单词首字母大写。

```lua
StringUtils.title("hello world")  --> "Hello World"
```

#### `to_snake_case(s)` / `to_camel_case(s)` / `to_pascal_case(s)`

命名格式转换。

```lua
StringUtils.to_snake_case("camelCase")    --> "camel_case"
StringUtils.to_camel_case("snake_case")   --> "snakeCase"
StringUtils.to_pascal_case("snake_case")  --> "SnakeCase"
```

---

### 字符串查找

#### `contains(s, substring)`

检查是否包含子串。

```lua
StringUtils.contains("hello world", "world")  --> true
```

#### `starts_with(s, prefix)` / `ends_with(s, suffix)`

检查前缀/后缀。

```lua
StringUtils.starts_with("hello", "he")   --> true
StringUtils.ends_with("hello", "lo")     --> true
```

#### `find_all(s, substring)`

查找所有匹配位置。

```lua
StringUtils.find_all("abcabc", "abc")  --> {1, 4}
```

---

### 字符串替换

#### `replace_first(s, old, new)` / `replace_last(s, old, new)`

替换第一次/最后一次出现。

```lua
StringUtils.replace_first("a b a", "a", "x")  --> "x b a"
StringUtils.replace_last("a b a", "a", "x")   --> "a b x"
```

#### `replace_all(s, old, new)`

替换所有出现。

```lua
StringUtils.replace_all("a b a", "a", "x")  --> "x b x"
```

#### `replace_n(s, old, new, count)`

替换前 n 次出现。

```lua
StringUtils.replace_n("a b a b a", "a", "x", 2)  --> "x b x b a"
```

---

### 分割与连接

#### `split(s, delimiter)`

分割字符串。

```lua
StringUtils.split("a,b,c", ",")  --> {"a", "b", "c"}
```

#### `lines(s)`

按行分割。

```lua
StringUtils.lines("a\nb\nc")  --> {"a", "b", "c"}
```

#### `join(tbl, separator)`

连接字符串数组。

```lua
StringUtils.join({"a", "b", "c"}, "-")  --> "a-b-c"
```

---

### 填充与截断

#### `pad_left(s, length, char)` / `pad_right(s, length, char)` / `pad_center(s, length, char)`

填充字符串。

```lua
StringUtils.pad_left("42", 5, "0")   --> "00042"
StringUtils.pad_right("42", 5, "0")  --> "42000"
StringUtils.pad_center("42", 7)      --> "  42   "
```

#### `truncate(s, length, suffix)` / `truncate_words(s, length, suffix)`

截断字符串。

```lua
StringUtils.truncate("hello world", 8)        --> "hello..."
StringUtils.truncate_words("hello world", 8)  --> "hello..."
```

---

### 验证函数

#### `is_alpha(s)` / `is_digit(s)` / `is_alphanumeric(s)`

字符类型验证。

```lua
StringUtils.is_alpha("abc")       --> true
StringUtils.is_digit("123")       --> true
StringUtils.is_alphanumeric("abc123")  --> true
```

#### `is_email(s)`

邮箱格式验证。

```lua
StringUtils.is_email("test@example.com")  --> true
```

#### `is_url(s)`

URL 格式验证。

```lua
StringUtils.is_url("https://example.com")  --> true
```

#### `is_ipv4(s)`

IPv4 地址验证。

```lua
StringUtils.is_ipv4("192.168.1.1")  --> true
```

---

### 格式化函数

#### `format_number(num, separator)`

千分位格式化。

```lua
StringUtils.format_number(1234567)       --> "1,234,567"
StringUtils.format_number(1234567, ".")  --> "1.234.567"
```

#### `format_bytes(bytes, precision)`

字节数格式化。

```lua
StringUtils.format_bytes(1536)     --> "1.50 KB"
StringUtils.format_bytes(1048576)  --> "1.00 MB"
```

#### `format_time(seconds)`

时间格式化。

```lua
StringUtils.format_time(3661)  --> "1:01:01"
StringUtils.format_time(61)    --> "1:01"
```

#### `format_datetime(timestamp, format)`

日期时间格式化。

```lua
StringUtils.format_datetime()  --> "2026-04-11 01:00:00"
```

---

### 编码解码

#### `url_encode(s)` / `url_decode(s)`

URL 编码解码。

```lua
StringUtils.url_encode("hello world")   --> "hello+world"
StringUtils.url_decode("hello+world")   --> "hello world"
```

#### `html_encode(s)` / `html_decode(s)`

HTML 实体编码解码。

```lua
StringUtils.html_encode("<script>")     --> "&lt;script&gt;"
StringUtils.html_decode("&lt;script&gt;") --> "<script>"
```

#### `base64_encode(s)` / `base64_decode(s)`

Base64 编码解码。

```lua
local encoded = StringUtils.base64_encode("Hello")
local decoded = StringUtils.base64_decode(encoded)
```

---

### 相似度计算

#### `levenshtein(s1, s2)`

计算编辑距离。

```lua
StringUtils.levenshtein("kitten", "sitting")  --> 3
```

#### `similarity(s1, s2)`

计算相似度 (0-1)。

```lua
StringUtils.similarity("hello", "hello")   --> 1.0
StringUtils.similarity("hello", "hallo")   --> 0.8
```

---

### 工具函数

#### `random(length, charset)`

生成随机字符串。

```lua
StringUtils.random(10)                    --> "aB3xY9kL2m"
StringUtils.random(6, "0123456789")       --> "482916"
```

#### `uuid()`

生成 UUID v4。

```lua
StringUtils.uuid()  --> "550e8400-e29b-41d4-a716-446655440000"
```

#### `builder()`

创建字符串构建器。

```lua
local b = StringUtils.builder()
b:append("Hello"):append(" "):append("World")
print(b:to_string())  --> "Hello World"
```

#### `template(template, data)`

模板替换。

```lua
StringUtils.template("Hello, {name}!", { name = "World" })
--> "Hello, World!"
```

#### `interpolate(s, env)`

字符串插值。

```lua
StringUtils.interpolate("${2 + 2}", {})  --> "4"
```

---

## 💡 实用示例

### 1. 表单验证

```lua
local StringUtils = require("string_utils")

function validate_user(email, phone)
    local errors = {}
    
    if not StringUtils.is_email(email) then
        table.insert(errors, "Invalid email")
    end
    
    if not StringUtils.is_phone_cn(phone) then
        table.insert(errors, "Invalid phone")
    end
    
    return #errors == 0, errors
end
```

### 2. 日志格式化

```lua
local function format_log(level, message, data)
    local timestamp = StringUtils.format_datetime()
    local formatted_msg = StringUtils.template(message, data)
    return string.format("[%s] [%s] %s", timestamp, level, formatted_msg)
end

print(format_log("INFO", "User {name} logged in", { name = "Alice" }))
```

### 3. 文本截断显示

```lua
local function display_title(title, max_length)
    return StringUtils.truncate_words(title, max_length)
end

print(display_title("This is a very long article title", 20))
--> "This is a very..."
```

### 4. 生成邀请码

```lua
local function generate_invite_code()
    return "INV-" .. StringUtils.random(8, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
end

print(generate_invite_code())  --> "INV-A3X9K2M7"
```

### 5. 模糊搜索

```lua
local function search_items(query, items)
    local results = {}
    for _, item in ipairs(items) do
        local score = StringUtils.similarity(query:lower(), item:lower())
        if score > 0.5 then
            table.insert(results, { item = item, score = score })
        end
    end
    table.sort(results, function(a, b) return a.score > b.score end)
    return results
end
```

### 6. 数据序列化

```lua
local function serialize_simple(data)
    local builder = StringUtils.builder()
    builder:append("{")
    local first = true
    for k, v in pairs(data) do
        if not first then builder:append(",") end
        builder:append('"'):append(k):append('":')
        if type(v) == "string" then
            builder:append('"'):append(StringUtils.html_encode(v)):append('"')
        else
            builder:append(tostring(v))
        end
        first = false
    end
    builder:append("}")
    return builder:to_string()
end
```

---

## 🧪 测试

运行测试套件：

```bash
cd AllToolkit/Lua/string_utils
lua string_utils_test.lua
```

测试覆盖：
- ✅ 空白处理
- ✅ 大小写转换
- ✅ 字符串查找
- ✅ 字符串替换
- ✅ 分割连接
- ✅ 填充截断
- ✅ 验证函数
- ✅ 格式化函数
- ✅ 编码解码
- ✅ 相似度计算
- ✅ 工具函数
- ✅ 边界情况处理

---

## ⚠️ 注意事项

### Lua 版本

- 兼容 Lua 5.1+
- 在 Lua 5.2/5.3/5.4 和 LuaJIT 上测试通过

### 性能考虑

- 大字符串处理时，某些操作会创建新字符串
- 对于频繁拼接，建议使用 `builder()`

### 模式匹配

- `split()` 默认支持 Lua 模式
- 使用 `split_by()` 进行纯文本分割

### 编码限制

- Base64 实现仅支持 ASCII 字符串
- 处理 UTF-8 多字节字符时，长度计算按字节而非字符

---

## 📝 版本历史

- **1.0.0** (2026-04-11) - 初始版本
  - 50+ 核心函数
  - 完整测试套件
  - 详细文档和示例

---

## 📄 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 报告 Bug
- 请求新功能
- 改进文档
- 添加新工具函数

---

**Author:** AllToolkit  
**Version:** 1.0.0  
**Last Updated:** 2026-04-11
