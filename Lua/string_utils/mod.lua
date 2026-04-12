---
-- String Utilities Module
-- 字符串处理工具函数库
--
-- 提供常用的字符串处理功能，包括格式化、转换、验证、解析等。
-- 仅使用 Lua 标准库，零依赖。
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local StringUtils = {}
local StringUtilsMT = { __index = StringUtils }

--- 版本号
StringUtils.VERSION = "1.0.0"

--- 错误处理
StringUtils.Error = {
    InvalidArgument = "Invalid argument",
    PatternNotFound = "Pattern not found",
    InvalidFormat = "Invalid format",
    OutOfRange = "Index out of range",
}

-------------------------------------------------------------------------------
-- 基础工具函数
-------------------------------------------------------------------------------

--- 检查值是否为 nil 或空字符串
-- @param s 要检查的字符串
-- @return boolean 如果是 nil 或空字符串返回 true
function StringUtils.is_empty(s)
    return s == nil or s == ""
end

--- 检查值是否为 nil、空字符串或只包含空白字符
-- @param s 要检查的字符串
-- @return boolean 如果是空白字符串返回 true
function StringUtils.is_blank(s)
    if s == nil then return true end
    return s:match("^%s*$") ~= nil
end

--- 去除字符串两端的空白字符
-- @param s 输入字符串
-- @return string 修剪后的字符串
function StringUtils.trim(s)
    if s == nil then return nil end
    return (s:gsub("^%s*(.-)%s*$", "%1"))
end

--- 只去除左侧空白字符
-- @param s 输入字符串
-- @return string 修剪后的字符串
function StringUtils.trim_left(s)
    if s == nil then return nil end
    return (s:gsub("^%s*", ""))
end

--- 只去除右侧空白字符
-- @param s 输入字符串
-- @return string 修剪后的字符串
function StringUtils.trim_right(s)
    if s == nil then return nil end
    return (s:gsub("%s*$", ""))
end

-------------------------------------------------------------------------------
-- 大小写转换
-------------------------------------------------------------------------------

--- 转换为小写（安全处理 nil）
-- @param s 输入字符串
-- @return string 小写字符串
function StringUtils.lower(s)
    if s == nil then return nil end
    return s:lower()
end

--- 转换为大写（安全处理 nil）
-- @param s 输入字符串
-- @return string 大写字符串
function StringUtils.upper(s)
    if s == nil then return nil end
    return s:upper()
end

--- 首字母大写
-- @param s 输入字符串
-- @return string 首字母大写的字符串
function StringUtils.capitalize(s)
    if s == nil then return nil end
    if #s == 0 then return s end
    return s:sub(1, 1):upper() .. s:sub(2):lower()
end

--- 每个单词首字母大写（标题格式）
-- @param s 输入字符串
-- @return string 标题格式的字符串
function StringUtils.title(s)
    if s == nil then return nil end
    return (s:gsub("(%w+)", function(word)
        return word:sub(1, 1):upper() .. word:sub(2):lower()
    end))
end

--- 转换为蛇形命名（snake_case）
-- @param s 输入字符串（支持 camelCase 或 PascalCase）
-- @return string 蛇形命名格式的字符串
function StringUtils.to_snake_case(s)
    if s == nil then return nil end
    -- 在大写字母前插入下划线，然后转小写
    local result = s:gsub("([a-z])([A-Z])", "%1_%2")
                     :gsub("([A-Z]+)([A-Z][a-z])", "%1_%2")
    return result:lower()
end

--- 转换为驼峰命名（camelCase）
-- @param s 输入字符串（支持 snake_case 或 PascalCase）
-- @return string 驼峰命名格式的字符串
function StringUtils.to_camel_case(s)
    if s == nil then return nil end
    -- 先处理 snake_case
    local result = s:gsub("_([a-z])", function(match)
        return match:upper()
    end)
    -- 确保首字母小写
    if #result > 0 then
        result = result:sub(1, 1):lower() .. result:sub(2)
    end
    return result
end

--- 转换为帕斯卡命名（PascalCase）
-- @param s 输入字符串（支持 snake_case 或 camelCase）
-- @return string 帕斯卡命名格式的字符串
function StringUtils.to_pascal_case(s)
    if s == nil then return nil end
    -- 先处理 snake_case
    local result = s:gsub("_([a-z])", function(match)
        return match:upper()
    end)
    -- 确保首字母大写
    if #result > 0 then
        result = result:sub(1, 1):upper() .. result:sub(2)
    end
    return result
end

-------------------------------------------------------------------------------
-- 字符串查找与匹配
-------------------------------------------------------------------------------

--- 检查字符串是否包含子串
-- @param s 输入字符串
-- @param substring 要查找的子串
-- @return boolean 如果包含返回 true
function StringUtils.contains(s, substring)
    if s == nil or substring == nil then return false end
    return s:find(substring, 1, true) ~= nil
end

--- 检查字符串是否以指定前缀开始
-- @param s 输入字符串
-- @param prefix 前缀字符串
-- @return boolean 如果以前缀开始返回 true
function StringUtils.starts_with(s, prefix)
    if s == nil or prefix == nil then return false end
    if #prefix == 0 then return true end
    if #prefix > #s then return false end
    return s:sub(1, #prefix) == prefix
end

--- 检查字符串是否以指定后缀结束
-- @param s 输入字符串
-- @param suffix 后缀字符串
-- @return boolean 如果以后缀结束返回 true
function StringUtils.ends_with(s, suffix)
    if s == nil or suffix == nil then return false end
    if #suffix == 0 then return true end
    if #suffix > #s then return false end
    return s:sub(-#suffix) == suffix
end

--- 查找子串在字符串中的位置（返回所有匹配位置）
-- @param s 输入字符串
-- @param substring 要查找的子串
-- @param plain 是否使用纯文本匹配（默认 true）
-- @return table 位置数组
function StringUtils.find_all(s, substring, plain)
    if s == nil or substring == nil then return {} end
    plain = plain ~= false
    
    local positions = {}
    local start = 1
    while true do
        local pos = s:find(substring, start, plain)
        if pos == nil then break end
        table.insert(positions, pos)
        start = pos + #substring
    end
    return positions
end

--- 使用模式匹配提取内容
-- @param s 输入字符串
-- @param pattern Lua 模式字符串
-- @return table 匹配结果数组
function StringUtils.match_all(s, pattern)
    if s == nil or pattern == nil then return {} end
    
    local results = {}
    for match in s:gmatch(pattern) do
        if type(match) == "table" then
            table.insert(results, { table.unpack(match) })
        else
            table.insert(results, match)
        end
    end
    return results
end

-------------------------------------------------------------------------------
-- 字符串替换
-------------------------------------------------------------------------------

--- 替换第一次出现的子串
-- @param s 输入字符串
-- @param old 要替换的子串
-- @param new 新的子串
-- @return string 替换后的字符串
function StringUtils.replace_first(s, old, new)
    if s == nil or old == nil then return s end
    if new == nil then new = "" end
    
    local start, finish = s:find(old, 1, true)
    if start == nil then return s end
    
    return s:sub(1, start - 1) .. new .. s:sub(finish + 1)
end

--- 替换最后一次出现的子串
-- @param s 输入字符串
-- @param old 要替换的子串
-- @param new 新的子串
-- @return string 替换后的字符串
function StringUtils.replace_last(s, old, new)
    if s == nil or old == nil then return s end
    if new == nil then new = "" end
    
    local start, finish = s:find(old, 1, true)
    local last_start, last_finish = start, finish
    
    while start ~= nil do
        last_start, last_finish = start, finish
        start, finish = s:find(old, finish + 1, true)
    end
    
    if last_start == nil then return s end
    
    return s:sub(1, last_start - 1) .. new .. s:sub(last_finish + 1)
end

--- 替换所有出现的子串
-- @param s 输入字符串
-- @param old 要替换的子串
-- @param new 新的子串
-- @return string 替换后的字符串
function StringUtils.replace_all(s, old, new)
    if s == nil or old == nil then return s end
    if new == nil then new = "" end
    if #old == 0 then return s end
    
    local result = {}
    local start = 1
    local old_start, old_finish = s:find(old, 1, true)
    
    while old_start ~= nil do
        table.insert(result, s:sub(start, old_start - 1))
        table.insert(result, new)
        start = old_finish + 1
        old_start, old_finish = s:find(old, start, true)
    end
    
    table.insert(result, s:sub(start))
    return table.concat(result)
end

--- 替换前 n 次出现的子串
-- @param s 输入字符串
-- @param old 要替换的子串
-- @param new 新的子串
-- @param count 替换次数
-- @return string 替换后的字符串
function StringUtils.replace_n(s, old, new, count)
    if s == nil or old == nil or count == nil or count <= 0 then return s end
    if new == nil then new = "" end
    if #old == 0 then return s end
    
    local result = {}
    local start = 1
    local replaced = 0
    
    while replaced < count do
        local old_start, old_finish = s:find(old, start, true)
        if old_start == nil then break end
        
        table.insert(result, s:sub(start, old_start - 1))
        table.insert(result, new)
        start = old_finish + 1
        replaced = replaced + 1
    end
    
    table.insert(result, s:sub(start))
    return table.concat(result)
end

-------------------------------------------------------------------------------
-- 字符串分割与连接
-------------------------------------------------------------------------------

--- 分割字符串
-- @param s 输入字符串
-- @param delimiter 分隔符（支持 Lua 模式）
-- @param plain 是否使用纯文本匹配（默认 false，即支持模式）
-- @return table 分割后的字符串数组
function StringUtils.split(s, delimiter, plain)
    if s == nil then return {} end
    if delimiter == nil or delimiter == "" then
        -- 按字符分割
        local result = {}
        for i = 1, #s do
            table.insert(result, s:sub(i, i))
        end
        return result
    end
    
    plain = plain or false
    local result = {}
    local start = 1
    local delim_start, delim_finish = s:find(delimiter, start, not plain)
    
    while delim_start ~= nil do
        table.insert(result, s:sub(start, delim_start - 1))
        start = delim_finish + 1
        delim_start, delim_finish = s:find(delimiter, start, not plain)
    end
    
    table.insert(result, s:sub(start))
    return result
end

--- 使用纯文本分隔符分割（不支持模式）
-- @param s 输入字符串
-- @param delimiter 分隔符
-- @return table 分割后的字符串数组
function StringUtils.split_by(s, delimiter)
    return StringUtils.split(s, delimiter, true)
end

--- 按行分割字符串
-- @param s 输入字符串
-- @return table 行数组
function StringUtils.lines(s)
    if s == nil then return {} end
    local result = {}
    for line in s:gmatch("[^\r\n]*") do
        table.insert(result, line)
    end
    return result
end

--- 连接字符串数组
-- @param tbl 字符串数组
-- @param separator 分隔符（默认空字符串）
-- @return string 连接后的字符串
function StringUtils.join(tbl, separator)
    if tbl == nil then return nil end
    separator = separator or ""
    return table.concat(tbl, separator)
end

-------------------------------------------------------------------------------
-- 字符串填充与截断
-------------------------------------------------------------------------------

--- 左侧填充字符串
-- @param s 输入字符串
-- @param length 目标长度
-- @param char 填充字符（默认空格）
-- @return string 填充后的字符串
function StringUtils.pad_left(s, length, char)
    if s == nil then return nil end
    char = char or " "
    if #s >= length then return s end
    return char:rep(length - #s) .. s
end

--- 右侧填充字符串
-- @param s 输入字符串
-- @param length 目标长度
-- @param char 填充字符（默认空格）
-- @return string 填充后的字符串
function StringUtils.pad_right(s, length, char)
    if s == nil then return nil end
    char = char or " "
    if #s >= length then return s end
    return s .. char:rep(length - #s)
end

--- 居中填充字符串
-- @param s 输入字符串
-- @param length 目标长度
-- @param char 填充字符（默认空格）
-- @return string 填充后的字符串
function StringUtils.pad_center(s, length, char)
    if s == nil then return nil end
    char = char or " "
    if #s >= length then return s end
    
    local total_padding = length - #s
    local left_padding = math.floor(total_padding / 2)
    local right_padding = total_padding - left_padding
    
    return char:rep(left_padding) .. s .. char:rep(right_padding)
end

--- 截断字符串到指定长度
-- @param s 输入字符串
-- @param length 最大长度
-- @param suffix 截断后缀（默认 "..."）
-- @return string 截断后的字符串
function StringUtils.truncate(s, length, suffix)
    if s == nil then return nil end
    suffix = suffix or "..."
    if #s <= length then return s end
    
    local max_len = length - #suffix
    if max_len < 0 then
        return suffix:sub(1, length)
    end
    
    return s:sub(1, max_len) .. suffix
end

--- 截断单词边界
-- @param s 输入字符串
-- @param length 最大长度
-- @param suffix 截断后缀（默认 "..."）
-- @return string 截断后的字符串
function StringUtils.truncate_words(s, length, suffix)
    if s == nil then return nil end
    suffix = suffix or "..."
    if #s <= length then return s end
    
    local truncated = s:sub(1, length - #suffix)
    -- 找到最后一个空格
    local last_space = truncated:match("^(.*[ ])")
    if last_space then
        return last_space:sub(1, -2) .. suffix
    end
    
    return truncated .. suffix
end

-------------------------------------------------------------------------------
-- 字符串重复与反转
-------------------------------------------------------------------------------

--- 重复字符串
-- @param s 输入字符串
-- @param count 重复次数
-- @param separator 分隔符（可选）
-- @return string 重复后的字符串
function StringUtils.repeat_str(s, count, separator)
    if s == nil or count == nil or count <= 0 then return "" end
    if separator then
        local result = {}
        for i = 1, count do
            table.insert(result, s)
        end
        return table.concat(result, separator)
    else
        return s:rep(count)
    end
end

--- 反转字符串
-- @param s 输入字符串
-- @return string 反转后的字符串
function StringUtils.reverse(s)
    if s == nil then return nil end
    return s:reverse()
end

-------------------------------------------------------------------------------
-- 字符与字节操作
-------------------------------------------------------------------------------

--- 获取字符串长度（安全处理 nil）
-- @param s 输入字符串
-- @return number 长度，nil 返回 0
function StringUtils.length(s)
    if s == nil then return 0 end
    return #s
end

--- 获取指定位置的字符
-- @param s 输入字符串
-- @param index 位置（1-based，负数表示从后往前）
-- @return string 字符，越界返回 nil
function StringUtils.char_at(s, index)
    if s == nil then return nil end
    local len = #s
    if index < 0 then
        index = len + index + 1
    end
    if index < 1 or index > len then
        return nil
    end
    return s:sub(index, index)
end

--- 提取子串（安全处理边界）
-- @param s 输入字符串
-- @param start 起始位置（1-based，负数表示从后往前）
-- @param finish 结束位置（可选，默认到末尾）
-- @return string 子串
function StringUtils.substring(s, start, finish)
    if s == nil then return nil end
    return s:sub(start, finish)
end

-------------------------------------------------------------------------------
-- 验证函数
-------------------------------------------------------------------------------

--- 检查字符串是否只包含字母
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_alpha(s)
    if s == nil or #s == 0 then return false end
    return s:match("^%a+$") ~= nil
end

--- 检查字符串是否只包含数字
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_digit(s)
    if s == nil or #s == 0 then return false end
    return s:match("^%d+$") ~= nil
end

--- 检查字符串是否只包含字母和数字
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_alphanumeric(s)
    if s == nil or #s == 0 then return false end
    return s:match("^%w+$") ~= nil
end

--- 检查是否是有效的邮箱地址（基础验证）
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_email(s)
    if s == nil then return false end
    -- 基础邮箱格式验证
    local pattern = "^[%w%.%-]+@[%w%.%-]+%.[%w]+$"
    return s:match(pattern) ~= nil
end

--- 检查是否是有效的 URL（基础验证）
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_url(s)
    if s == nil then return false end
    local pattern = "^https?://[%w%.%-%_]+[%.%w%.%-%_]+[%w%.%-%_%.%?%=%&%/]*$"
    return s:match(pattern) ~= nil
end

--- 检查是否是有效的 IPv4 地址
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_ipv4(s)
    if s == nil then return false end
    local pattern = "^(%d%d?%d?)%.(%d%d?%d?)%.(%d%d?%d?)%.(%d%d?%d?)$"
    local a, b, c, d = s:match(pattern)
    if a == nil then return false end
    a, b, c, d = tonumber(a), tonumber(b), tonumber(c), tonumber(d)
    return a <= 255 and b <= 255 and c <= 255 and d <= 255
end

--- 检查是否是有效的电话号码（中国大陆）
-- @param s 输入字符串
-- @return boolean
function StringUtils.is_phone_cn(s)
    if s == nil then return false end
    -- 支持多种格式：13800138000, 138-0013-8000, 138 0013 8000, +8613800138000
    local cleaned = s:gsub("[%s%-%+]", "")
    return cleaned:match("^%d+%d{10}$") ~= nil
end

-------------------------------------------------------------------------------
-- 格式化函数
-------------------------------------------------------------------------------

--- 格式化数字为千分位字符串
-- @param num 数字
-- @param separator 千分位分隔符（默认 ","）
-- @return string 格式化后的字符串
function StringUtils.format_number(num, separator)
    if num == nil then return nil end
    separator = separator or ","
    
    local str = tostring(num)
    local is_negative = str:sub(1, 1) == "-"
    if is_negative then
        str = str:sub(2)
    end
    
    -- 处理小数部分
    local dot_pos = str:find(".", 1, true)  -- 纯文本匹配，使用 "." 而不是 "%."
    local integer_part, decimal_part
    if dot_pos then
        integer_part = str:sub(1, dot_pos - 1)
        decimal_part = str:sub(dot_pos)
    else
        integer_part = str
        decimal_part = nil
    end
    
    if #integer_part == 0 then return str end
    
    -- 添加千分位（兼容 Lua 5.1）
    local result = {}
    local len = #integer_part
    local remainder = len % 3
    
    -- 处理第一组（可能少于 3 位）
    if remainder > 0 then
        table.insert(result, integer_part:sub(1, remainder))
    end
    
    -- 处理剩余的 3 位组
    for i = remainder + 1, len, 3 do
        if #result > 0 then
            table.insert(result, separator)
        end
        table.insert(result, integer_part:sub(i, i + 2))
    end
    
    result = table.concat(result)
    
    if decimal_part then
        result = result .. decimal_part
    end
    
    return is_negative and "-" .. result or result
end

--- 格式化字节数为人类可读格式
-- @param bytes 字节数
-- @param precision 小数位数（默认 2）
-- @return string 格式化后的字符串（如 "1.5 MB"）
function StringUtils.format_bytes(bytes, precision)
    if bytes == nil then return nil end
    precision = precision or 2
    
    local units = { "B", "KB", "MB", "GB", "TB", "PB" }
    local unit_index = 1
    local size = tonumber(bytes)
    
    while size >= 1024 and unit_index < #units do
        size = size / 1024
        unit_index = unit_index + 1
    end
    
    return string.format("%." .. precision .. "f %s", size, units[unit_index])
end

--- 格式化字节数为人类可读格式
-- @param bytes 字节数
-- @param precision 小数位数（默认 2）
-- @return string 格式化后的字符串（如 "1.5 MB"）
function StringUtils.format_bytes(bytes, precision)
    if bytes == nil then return nil end
    precision = precision or 2
    
    local units = { "B", "KB", "MB", "GB", "TB", "PB" }
    local unit_index = 1
    local size = tonumber(bytes)
    
    while size >= 1024 and unit_index < #units do
        size = size / 1024
        unit_index = unit_index + 1
    end
    
    return string.format("%." .. precision .. "f %s", size, units[unit_index])
end

--- 格式化时间为 HH:MM:SS
-- @param seconds 秒数
-- @return string 格式化后的时间字符串
function StringUtils.format_time(seconds)
    if seconds == nil then return nil end
    seconds = math.floor(tonumber(seconds))
    
    local h = math.floor(seconds / 3600)
    local m = math.floor((seconds % 3600) / 60)
    local s = seconds % 60
    
    if h > 0 then
        return string.format("%d:%02d:%02d", h, m, s)
    else
        return string.format("%d:%02d", m, s)
    end
end

--- 格式化日期时间
-- @param timestamp Unix 时间戳（可选，默认当前时间）
-- @param format 格式字符串（默认 "%Y-%m-%d %H:%M:%S"）
-- @return string 格式化后的日期时间字符串
function StringUtils.format_datetime(timestamp, format)
    format = format or "%Y-%m-%d %H:%M:%S"
    timestamp = timestamp or os.time()
    return os.date(format, timestamp)
end

-------------------------------------------------------------------------------
-- 模板与插值
-------------------------------------------------------------------------------

--- 简单的模板替换
-- @param template 模板字符串，使用 {name} 作为占位符
-- @param data 数据表
-- @return string 替换后的字符串
function StringUtils.template(template, data)
    if template == nil or data == nil then return template end
    
    return (template:gsub("{([%w_]+)}", function(key)
        local value = data[key]
        if value ~= nil then
            return tostring(value)
        end
        return "{" .. key .. "}"  -- 保持原样
    end))
end

--- 字符串插值（类似 Python f-string）
-- 使用 ${expression} 语法，支持简单的 Lua 表达式
-- @param s 包含插值表达式的字符串
-- @param env 环境表（用于查找变量）
-- @return string 插值后的字符串
function StringUtils.interpolate(s, env)
    if s == nil then return nil end
    env = env or {}
    
    return (s:gsub("%$({([^}]+)})", function(_, expr)
        -- 尝试作为表达式执行
        local func, err = load("return " .. expr, "interpolate", "t", env)
        if func then
            local success, result = pcall(func)
            if success then
                return tostring(result)
            end
        end
        -- 如果失败，尝试直接作为变量名
        local value = env[expr]
        if value ~= nil then
            return tostring(value)
        end
        return "${" .. expr .. "}"  -- 保持原样
    end))
end

-------------------------------------------------------------------------------
-- 编码与解码
-------------------------------------------------------------------------------

--- URL 编码
-- @param s 输入字符串
-- @return string 编码后的字符串
function StringUtils.url_encode(s)
    if s == nil then return nil end
    return (s:gsub("([^%w%.%-_%~ ])", function(c)
        return string.format("%%%02X", c:byte())
    end):gsub(" ", "+"))
end

--- URL 解码
-- @param s 输入字符串
-- @return string 解码后的字符串
function StringUtils.url_decode(s)
    if s == nil then return nil end
    return (s:gsub("+", " "):gsub("%%(%x%x)", function(hex)
        return string.char(tonumber(hex, 16))
    end))
end

--- HTML 实体编码
-- @param s 输入字符串
-- @return string 编码后的字符串
function StringUtils.html_encode(s)
    if s == nil then return nil end
    local replacements = {
        ["&"] = "&amp;",
        ["<"] = "&lt;",
        [">"] = "&gt;",
        ['"'] = "&quot;",
        ["'"] = "&#39;",
    }
    return (s:gsub("[&<>'\"]", function(c)
        return replacements[c]
    end))
end

--- HTML 实体解码
-- @param s 输入字符串
-- @return string 解码后的字符串
function StringUtils.html_decode(s)
    if s == nil then return nil end
    local replacements = {
        ["&amp;"] = "&",
        ["&lt;"] = "<",
        ["&gt;"] = ">",
        ["&quot;"] = '"',
        ["&#39;"] = "'",
    }
    local result = s
    for entity, char in pairs(replacements) do
        result = result:gsub(entity, char)
    end
    return result
end

--- Base64 编码
-- @param s 输入字符串
-- @return string Base64 编码的字符串
function StringUtils.base64_encode(s)
    if s == nil then return nil end
    
    local b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    local result = {}
    
    for i = 1, #s, 3 do
        local bytes = {
            s:byte(i),
            s:byte(i + 1) or 0,
            s:byte(i + 2) or 0,
        }
        
        local n = bytes[1] * 65536 + bytes[2] * 256 + bytes[3]
        
        table.insert(result, b64_chars:sub(math.floor(n / 262144) + 1, math.floor(n / 262144) + 1))
        table.insert(result, b64_chars:sub(math.floor(n / 4096) % 64 + 1, math.floor(n / 4096) % 64 + 1))
        
        if i + 1 <= #s then
            table.insert(result, b64_chars:sub(math.floor(n / 64) % 64 + 1, math.floor(n / 64) % 64 + 1))
        else
            table.insert(result, "=")
        end
        
        if i + 2 <= #s then
            table.insert(result, b64_chars:sub(n % 64 + 1, n % 64 + 1))
        else
            table.insert(result, "=")
        end
    end
    
    return table.concat(result)
end

--- Base64 解码
-- @param s Base64 编码的字符串
-- @return string 解码后的字符串
function StringUtils.base64_decode(s)
    if s == nil then return nil end
    
    local b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    local char_to_index = {}
    for i = 1, #b64_chars do
        char_to_index[b64_chars:sub(i, i)] = i - 1
    end
    
    -- 统计填充数量
    local padding = 0
    for i = #s, 1, -1 do
        if s:sub(i, i) == "=" then
            padding = padding + 1
        else
            break
        end
    end
    
    -- 移除填充
    s = s:gsub("=+$", "")
    
    local result = {}
    
    for i = 1, #s, 4 do
        local c1 = char_to_index[s:sub(i, i)] or 0
        local c2 = char_to_index[s:sub(i+1, i+1)] or 0
        local c3 = char_to_index[s:sub(i+2, i+2)] or 0
        local c4 = char_to_index[s:sub(i+3, i+3)] or 0
        
        local n = c1 * 262144 + c2 * 4096 + c3 * 64 + c4
        
        table.insert(result, string.char(math.floor(n / 65536) % 256))
        
        if i + 2 <= #s and s:sub(i+2, i+2) ~= "=" then
            table.insert(result, string.char(math.floor(n / 256) % 256))
        end
        
        if i + 3 <= #s and s:sub(i+3, i+3) ~= "=" then
            table.insert(result, string.char(n % 256))
        end
    end
    
    return table.concat(result)
end

-------------------------------------------------------------------------------
-- 相似度和比较
-------------------------------------------------------------------------------

--- 计算两个字符串的编辑距离（Levenshtein Distance）
-- @param s1 第一个字符串
-- @param s2 第二个字符串
-- @return number 编辑距离
function StringUtils.levenshtein(s1, s2)
    if s1 == nil or s2 == nil then return -1 end
    
    local len1, len2 = #s1, #s2
    
    -- 优化：如果一个为空，返回另一个的长度
    if len1 == 0 then return len2 end
    if len2 == 0 then return len1 end
    
    -- 创建矩阵
    local matrix = {}
    for i = 0, len1 do
        matrix[i] = {}
        matrix[i][0] = i
    end
    for j = 0, len2 do
        matrix[0][j] = j
    end
    
    -- 填充矩阵
    for i = 1, len1 do
        for j = 1, len2 do
            local cost = (s1:sub(i, i) == s2:sub(j, j)) and 0 or 1
            matrix[i][j] = math.min(
                matrix[i-1][j] + 1,      -- 删除
                matrix[i][j-1] + 1,      -- 插入
                matrix[i-1][j-1] + cost  -- 替换
            )
        end
    end
    
    return matrix[len1][len2]
end

--- 计算两个字符串的相似度（0-1 之间）
-- @param s1 第一个字符串
-- @param s2 第二个字符串
-- @return number 相似度
function StringUtils.similarity(s1, s2)
    if s1 == nil or s2 == nil then return 0 end
    if s1 == s2 then return 1 end
    
    local distance = StringUtils.levenshtein(s1, s2)
    local max_len = math.max(#s1, #s2)
    
    if max_len == 0 then return 1 end
    return 1 - (distance / max_len)
end

-------------------------------------------------------------------------------
-- 实用工具
-------------------------------------------------------------------------------

--- 生成随机字符串
-- @param length 长度
-- @param charset 字符集（可选）
-- @return string 随机字符串
function StringUtils.random(length, charset)
    if length == nil or length <= 0 then return "" end
    
    charset = charset or "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    local result = {}
    local charset_len = #charset
    
    math.randomseed(os.time())
    
    for i = 1, length do
        local index = math.random(charset_len)
        table.insert(result, charset:sub(index, index))
    end
    
    return table.concat(result)
end

--- 生成 UUID（版本 4）
-- @return string UUID 字符串
function StringUtils.uuid()
    local template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    return (template:gsub("[xy]", function(c)
        local v = (c == "x") and math.random(0, 15) or math.random(8, 11)
        return string.format("%x", v)
    end))
end

--- 创建字符串构建器
-- @return table 字符串构建器对象
function StringUtils.builder()
    local buffer = {}
    return {
        append = function(self, ...)
            for i = 1, select("#", ...) do
                local arg = select(i, ...)
                if arg ~= nil then
                    table.insert(buffer, tostring(arg))
                end
            end
            return self
        end,
        append_line = function(self, ...)
            for i = 1, select("#", ...) do
                local arg = select(i, ...)
                if arg ~= nil then
                    table.insert(buffer, tostring(arg))
                    table.insert(buffer, "\n")
                end
            end
            return self
        end,
        clear = function(self)
            buffer = {}
            return self
        end,
        length = function(self)
            return #table.concat(buffer)
        end,
        to_string = function(self)
            return table.concat(buffer)
        end,
    }
end

-------------------------------------------------------------------------------
-- 导出模块
-------------------------------------------------------------------------------

return StringUtils
