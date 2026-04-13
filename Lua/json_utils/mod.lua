---
-- JSON Utilities Module
-- JSON 处理工具函数库
--
-- 提供完整的 JSON 编码、解码、验证、格式化等功能。
-- 仅使用 Lua 标准库，零依赖。
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local JsonUtils = {}
local JsonUtilsMT = { __index = JsonUtils }

-- Forward declarations for mutually recursive functions
local encodeValue
local encodeArray
local encodeObject

--- 版本号
JsonUtils.VERSION = "1.0.0"

--- 错误类型
JsonUtils.Error = {
    InvalidJSON = "Invalid JSON syntax",
    InvalidType = "Invalid type for JSON encoding",
    UnexpectedToken = "Unexpected token",
    UnterminatedString = "Unterminated string",
    InvalidEscape = "Invalid escape sequence",
    InvalidNumber = "Invalid number format",
    MaxDepthExceeded = "Maximum nesting depth exceeded",
    CircularReference = "Circular reference detected",
}

--- 默认配置
JsonUtils.Config = {
    max_depth = 100,           -- 最大嵌套深度
    indent = "  ",             -- 缩进字符
    sort_keys = false,         -- 是否排序键
    escape_forward_slash = false, -- 是否转义正斜杠
    encode_empty_table_as_array = true, -- 空表编码为数组（默认）
    pretty = false,            -- 默认是否美化输出
    strict_parsing = false,    -- 是否严格解析模式
}

-------------------------------------------------------------------------------
-- 内部工具函数
-------------------------------------------------------------------------------

-- 本地缓存常用函数
local type = type
local pairs = pairs
local ipairs = ipairs
local tonumber = tonumber
local tostring = tostring
local math_floor = math.floor
local math_abs = math.abs
local math_huge = math.huge
local next = next
local table_insert = table.insert
local table_concat = table.concat
local table_sort = table.sort
local string_find = string.find
local string_sub = string.sub
local string_format = string.format
local string_byte = string.byte
local string_char = string.char
local string_match = string.match
local string_gmatch = string.gmatch
local string_rep = string.rep
local string_gsub = string.gsub

--- 检查表是否为数组（连续整数键从1开始）
-- @param t 要检查的表
-- @return boolean 如果是数组返回 true
local function isArray(t)
    if type(t) ~= "table" then return false end
    local count = 0
    for _ in pairs(t) do
        count = count + 1
    end
    if count == 0 then return JsonUtils.Config.encode_empty_table_as_array end
    for i = 1, count do
        if t[i] == nil then return false end
    end
    -- 检查是否只有连续整数键
    for k in pairs(t) do
        if type(k) ~= "number" or k < 1 or k > count or math_floor(k) ~= k then
            return false
        end
    end
    return true
end

--- 检查表是否为空
-- @param t 要检查的表
-- @return boolean 如果为空返回 true
local function isEmptyTable(t)
    if type(t) ~= "table" then return true end
    return next(t) == nil
end

--- 深度复制表
-- @param orig 原始表
-- @param visited 已访问表（用于处理循环引用）
-- @return table 复制后的表
local function deepCopy(orig, visited)
    if type(orig) ~= "table" then return orig end
    visited = visited or {}
    
    if visited[orig] then
        return visited[orig]
    end
    
    local copy = {}
    visited[orig] = copy
    
    for k, v in pairs(orig) do
        copy[deepCopy(k, visited)] = deepCopy(v, visited)
    end
    
    return copy
end

-------------------------------------------------------------------------------
-- JSON 编码器
-------------------------------------------------------------------------------

local Encoder = {}

--- Unicode 码点转 UTF-8
-- @param code Unicode 码点
-- @return string UTF-8 字符串
local function unicodeToUtf8(code)
    if code < 0x80 then
        return string_char(code)
    elseif code < 0x800 then
        return string_char(
            0xC0 + math_floor(code / 0x40),
            0x80 + (code % 0x40)
        )
    elseif code < 0x10000 then
        return string_char(
            0xE0 + math_floor(code / 0x1000),
            0x80 + (math_floor(code / 0x40) % 0x40),
            0x80 + (code % 0x40)
        )
    else
        return string_char(
            0xF0 + math_floor(code / 0x40000),
            0x80 + (math_floor(code / 0x1000) % 0x40),
            0x80 + (math_floor(code / 0x40) % 0x40),
            0x80 + (code % 0x40)
        )
    end
end

--- 转义字符串
-- @param s 要转义的字符串
-- @param config 配置选项
-- @return string 转义后的字符串
local function escapeString(s, config)
    local result = {}
    
    for i = 1, #s do
        local c = string_sub(s, i, i)
        local b = string_byte(c)
        
        if c == '"' then
            result[#result + 1] = '\\"'
        elseif c == '\\' then
            result[#result + 1] = '\\\\'
        elseif config and config.escape_forward_slash and c == '/' then
            result[#result + 1] = '\\/'
        elseif b == 8 then
            result[#result + 1] = '\\b'
        elseif b == 9 then
            result[#result + 1] = '\\t'
        elseif b == 10 then
            result[#result + 1] = '\\n'
        elseif b == 12 then
            result[#result + 1] = '\\f'
        elseif b == 13 then
            result[#result + 1] = '\\r'
        elseif b < 32 then
            result[#result + 1] = string_format('\\u%04x', b)
        else
            result[#result + 1] = c
        end
    end
    
    return table_concat(result)
end

--- 编码值
-- @param value 要编码的值
-- @param visited 已访问表（循环引用检测）
-- @param depth 当前深度
-- @param config 配置选项
-- @return string JSON 字符串
encodeValue = function(value, visited, depth, config)
    config = config or JsonUtils.Config
    visited = visited or {}
    depth = depth or 0
    
    -- 深度检查
    if depth > config.max_depth then
        error(JsonUtils.Error.MaxDepthExceeded)
    end
    
    local valueType = type(value)
    
    if value == nil then
        return "null"
    elseif valueType == "boolean" then
        return value and "true" or "false"
    elseif valueType == "number" then
        if value ~= value then -- NaN
            return "null"
        elseif value == math_huge or value == -math_huge then
            return "null"
        else
            -- 处理整数和小数
            if value == math_floor(value) and math_abs(value) < 2^53 then
                return tostring(value)
            else
                return string_format("%.17g", value)
            end
        end
    elseif valueType == "string" then
        return '"' .. escapeString(value, config) .. '"'
    elseif valueType == "table" then
        -- 循环引用检测
        if visited[value] then
            error(JsonUtils.Error.CircularReference)
        end
        visited[value] = true
        
        local result
        
        if isArray(value) then
            result = encodeArray(value, visited, depth, config)
        else
            result = encodeObject(value, visited, depth, config)
        end
        
        visited[value] = nil
        return result
    else
        error(JsonUtils.Error.InvalidType .. ": " .. valueType)
    end
end

--- 编码数组
-- @param arr 数组
-- @param visited 已访问表
-- @param depth 当前深度
-- @param config 配置选项
-- @return string JSON 数组字符串
encodeArray = function(arr, visited, depth, config)
    local parts = {}
    local count = 0
    
    -- 计算数组长度
    for _ in pairs(arr) do count = count + 1 end
    
    for i = 1, count do
        parts[i] = encodeValue(arr[i], visited, depth + 1, config)
    end
    
    if config.pretty then
        local indent = string_rep(config.indent, depth)
        local childIndent = string_rep(config.indent, depth + 1)
        if #parts == 0 then
            return "[]"
        else
            return "[\n" .. childIndent .. table_concat(parts, ",\n" .. childIndent) .. "\n" .. indent .. "]"
        end
    else
        return "[" .. table_concat(parts, ",") .. "]"
    end
end

--- 编码对象
-- @param obj 对象
-- @param visited 已访问表
-- @param depth 当前深度
-- @param config 配置选项
-- @return string JSON 对象字符串
encodeObject = function(obj, visited, depth, config)
    local parts = {}
    local keys = {}
    
    -- 收集键
    for k in pairs(obj) do
        keys[#keys + 1] = k
    end
    
    -- 排序键（如果配置要求）
    if config.sort_keys then
        table_sort(keys, function(a, b)
            return tostring(a) < tostring(b)
        end)
    end
    
    -- 编码键值对
    for _, k in ipairs(keys) do
        local v = obj[k]
        local keyStr
        if type(k) == "string" then
            keyStr = '"' .. escapeString(k, config) .. '"'
        elseif type(k) == "number" then
            keyStr = '"' .. tostring(k) .. '"'
        else
            -- 跳过非字符串/数字键
        end
        
        if keyStr then
            local valueStr = encodeValue(v, visited, depth + 1, config)
            parts[#parts + 1] = keyStr .. ":" .. (config.pretty and " " or "") .. valueStr
        end
    end
    
    if config.pretty then
        local indent = string_rep(config.indent, depth)
        local childIndent = string_rep(config.indent, depth + 1)
        if #parts == 0 then
            return "{}"
        else
            return "{\n" .. childIndent .. table_concat(parts, ",\n" .. childIndent) .. "\n" .. indent .. "}"
        end
    else
        return "{" .. table_concat(parts, ",") .. "}"
    end
end

-------------------------------------------------------------------------------
-- JSON 解码器
-------------------------------------------------------------------------------

local Decoder = {}
Decoder.__index = Decoder

--- 创建解码器
-- @param str JSON 字符串
-- @param config 配置选项
-- @return table 解码器对象
function Decoder.new(str, config)
    local self = {
        str = str,
        pos = 1,
        len = #str,
        config = config or JsonUtils.Config,
    }
    return setmetatable(self, Decoder)
end

--- 跳过空白字符
function Decoder:skipWhitespace()
    while self.pos <= self.len do
        local c = string_sub(self.str, self.pos, self.pos)
        if c == " " or c == "\t" or c == "\n" or c == "\r" then
            self.pos = self.pos + 1
        else
            break
        end
    end
end

--- 查看当前字符
-- @return string 当前字符
function Decoder:peek()
    if self.pos > self.len then
        return nil
    end
    return string_sub(self.str, self.pos, self.pos)
end

--- 消费当前字符
-- @return string 当前字符
function Decoder:consume()
    local c = self:peek()
    self.pos = self.pos + 1
    return c
end

--- 期望特定字符
-- @param expected 期望的字符
function Decoder:expect(expected)
    local c = self:consume()
    if c ~= expected then
        error(JsonUtils.Error.UnexpectedToken .. ": expected '" .. expected .. "', got '" .. (c or "EOF") .. "' at position " .. self.pos)
    end
end

--- 解析值
-- @param depth 当前深度
-- @return any 解析后的值
function Decoder:parseValue(depth)
    depth = depth or 0
    
    if depth > self.config.max_depth then
        error(JsonUtils.Error.MaxDepthExceeded)
    end
    
    self:skipWhitespace()
    
    local c = self:peek()
    
    if c == nil then
        error(JsonUtils.Error.UnexpectedToken .. ": unexpected end of input")
    elseif c == 'n' then
        return self:parseNull()
    elseif c == 't' then
        return self:parseTrue()
    elseif c == 'f' then
        return self:parseFalse()
    elseif c == '"' then
        return self:parseString()
    elseif c == '[' then
        return self:parseArray(depth)
    elseif c == '{' then
        return self:parseObject(depth)
    elseif c == '-' or (c >= '0' and c <= '9') then
        return self:parseNumber()
    else
        error(JsonUtils.Error.UnexpectedToken .. ": '" .. c .. "' at position " .. self.pos)
    end
end

--- 解析 null
-- @return nil
function Decoder:parseNull()
    if string_sub(self.str, self.pos, self.pos + 3) == "null" then
        self.pos = self.pos + 4
        return nil
    end
    error(JsonUtils.Error.InvalidJSON .. ": expected 'null' at position " .. self.pos)
end

--- 解析 true
-- @return boolean true
function Decoder:parseTrue()
    if string_sub(self.str, self.pos, self.pos + 3) == "true" then
        self.pos = self.pos + 4
        return true
    end
    error(JsonUtils.Error.InvalidJSON .. ": expected 'true' at position " .. self.pos)
end

--- 解析 false
-- @return boolean false
function Decoder:parseFalse()
    if string_sub(self.str, self.pos, self.pos + 4) == "false" then
        self.pos = self.pos + 5
        return false
    end
    error(JsonUtils.Error.InvalidJSON .. ": expected 'false' at position " .. self.pos)
end

--- 解析字符串
-- @return string 解析后的字符串
function Decoder:parseString()
    self:expect('"')
    
    local result = {}
    local start = self.pos
    
    while self.pos <= self.len do
        local c = string_sub(self.str, self.pos, self.pos)
        
        if c == '"' then
            result[#result + 1] = string_sub(self.str, start, self.pos - 1)
            self.pos = self.pos + 1
            return table_concat(result)
        elseif c == '\\' then
            result[#result + 1] = string_sub(self.str, start, self.pos - 1)
            self.pos = self.pos + 1
            
            if self.pos > self.len then
                error(JsonUtils.Error.UnterminatedString)
            end
            
            local escape = string_sub(self.str, self.pos, self.pos)
            self.pos = self.pos + 1
            
            if escape == '"' then
                result[#result + 1] = '"'
            elseif escape == '\\' then
                result[#result + 1] = '\\'
            elseif escape == '/' then
                result[#result + 1] = '/'
            elseif escape == 'b' then
                result[#result + 1] = '\b'
            elseif escape == 't' then
                result[#result + 1] = '\t'
            elseif escape == 'n' then
                result[#result + 1] = '\n'
            elseif escape == 'f' then
                result[#result + 1] = '\f'
            elseif escape == 'r' then
                result[#result + 1] = '\r'
            elseif escape == 'u' then
                -- Unicode 转义
                if self.pos + 3 > self.len then
                    error(JsonUtils.Error.InvalidEscape)
                end
                local hex = string_sub(self.str, self.pos, self.pos + 3)
                self.pos = self.pos + 4
                local code = tonumber(hex, 16)
                if not code then
                    error(JsonUtils.Error.InvalidEscape .. ": invalid unicode escape")
                end
                
                -- 处理 UTF-16 代理对
                if code >= 0xD800 and code <= 0xDBFF then
                    -- 高代理
                    if string_sub(self.str, self.pos, self.pos + 1) == '\\u' then
                        self.pos = self.pos + 2
                        local lowHex = string_sub(self.str, self.pos, self.pos + 3)
                        self.pos = self.pos + 4
                        local lowCode = tonumber(lowHex, 16)
                        if lowCode and lowCode >= 0xDC00 and lowCode <= 0xDFFF then
                            code = 0x10000 + (code - 0xD800) * 0x400 + (lowCode - 0xDC00)
                        end
                    end
                end
                
                -- 转换为 UTF-8
                result[#result + 1] = unicodeToUtf8(code)
            else
                error(JsonUtils.Error.InvalidEscape .. ": \\" .. escape)
            end
            
            start = self.pos
        else
            self.pos = self.pos + 1
        end
    end
    
    error(JsonUtils.Error.UnterminatedString)
end

--- 解析数字
-- @return number 解析后的数字
function Decoder:parseNumber()
    local start = self.pos
    
    -- 负号
    if self:peek() == '-' then
        self.pos = self.pos + 1
    end
    
    -- 整数部分
    local c = self:peek()
    if c == '0' then
        self.pos = self.pos + 1
    elseif c and c >= '1' and c <= '9' then
        self.pos = self.pos + 1
        while self:peek() and self:peek() >= '0' and self:peek() <= '9' do
            self.pos = self.pos + 1
        end
    else
        error(JsonUtils.Error.InvalidNumber .. " at position " .. self.pos)
    end
    
    -- 小数部分
    if self:peek() == '.' then
        self.pos = self.pos + 1
        local hasDigit = false
        while self:peek() and self:peek() >= '0' and self:peek() <= '9' do
            self.pos = self.pos + 1
            hasDigit = true
        end
        if not hasDigit then
            error(JsonUtils.Error.InvalidNumber .. ": expected digit after decimal point")
        end
    end
    
    -- 指数部分
    if self:peek() == 'e' or self:peek() == 'E' then
        self.pos = self.pos + 1
        if self:peek() == '+' or self:peek() == '-' then
            self.pos = self.pos + 1
        end
        local hasDigit = false
        while self:peek() and self:peek() >= '0' and self:peek() <= '9' do
            self.pos = self.pos + 1
            hasDigit = true
        end
        if not hasDigit then
            error(JsonUtils.Error.InvalidNumber .. ": expected digit in exponent")
        end
    end
    
    local numStr = string_sub(self.str, start, self.pos - 1)
    local num = tonumber(numStr)
    
    if not num then
        error(JsonUtils.Error.InvalidNumber .. ": " .. numStr)
    end
    
    return num
end

--- 解析数组
-- @param depth 当前深度
-- @return table 解析后的数组
function Decoder:parseArray(depth)
    self:expect('[')
    local result = {}
    
    self:skipWhitespace()
    
    if self:peek() == ']' then
        self:consume()
        return result
    end
    
    while true do
        local value = self:parseValue(depth + 1)
        result[#result + 1] = value
        
        self:skipWhitespace()
        local c = self:peek()
        
        if c == ']' then
            self:consume()
            return result
        elseif c == ',' then
            self:consume()
            self:skipWhitespace()
        else
            error(JsonUtils.Error.UnexpectedToken .. ": expected ',' or ']' at position " .. self.pos)
        end
    end
end

--- 解析对象
-- @param depth 当前深度
-- @return table 解析后的对象
function Decoder:parseObject(depth)
    self:expect('{')
    local result = {}
    
    self:skipWhitespace()
    
    if self:peek() == '}' then
        self:consume()
        return result
    end
    
    while true do
        self:skipWhitespace()
        
        -- 解析键
        if self:peek() ~= '"' then
            error(JsonUtils.Error.UnexpectedToken .. ": expected string key at position " .. self.pos)
        end
        
        local key = self:parseString()
        
        self:skipWhitespace()
        
        -- 期望冒号
        self:expect(':')
        
        -- 解析值
        local value = self:parseValue(depth + 1)
        result[key] = value
        
        self:skipWhitespace()
        local c = self:peek()
        
        if c == '}' then
            self:consume()
            return result
        elseif c == ',' then
            self:consume()
        else
            error(JsonUtils.Error.UnexpectedToken .. ": expected ',' or '}' at position " .. self.pos)
        end
    end
end

-------------------------------------------------------------------------------
-- 公共 API
-------------------------------------------------------------------------------

--- 将 Lua 值编码为 JSON 字符串
-- @param value 要编码的 Lua 值
-- @param config 配置选项（可选）
-- @return string JSON 字符串
-- @raise 编码失败时抛出错误
function JsonUtils.encode(value, config)
    config = config or {}
    for k, v in pairs(JsonUtils.Config) do
        if config[k] == nil then
            config[k] = v
        end
    end
    
    local ok, result = pcall(encodeValue, value, {}, 0, config)
    if ok then
        return result
    else
        error("JSON encode error: " .. result)
    end
end

--- 将 Lua 值编码为格式化的 JSON 字符串（美化输出）
-- @param value 要编码的 Lua 值
-- @param indent 缩进字符（可选，默认为两个空格）
-- @return string 格式化的 JSON 字符串
function JsonUtils.encode_pretty(value, indent)
    local config = {
        pretty = true,
        indent = indent or "  ",
        max_depth = JsonUtils.Config.max_depth,
        sort_keys = JsonUtils.Config.sort_keys,
    }
    return JsonUtils.encode(value, config)
end

--- 将 JSON 字符串解码为 Lua 值
-- @param str JSON 字符串
-- @param config 配置选项（可选）
-- @return any 解码后的 Lua 值
-- @raise 解码失败时抛出错误
function JsonUtils.decode(str, config)
    if type(str) ~= "string" then
        error("JSON decode error: input must be a string")
    end
    
    config = config or {}
    for k, v in pairs(JsonUtils.Config) do
        if config[k] == nil then
            config[k] = v
        end
    end
    
    local decoder = Decoder.new(str, config)
    local result = decoder:parseValue(0)
    
    decoder:skipWhitespace()
    if decoder.pos <= decoder.len then
        error(JsonUtils.Error.InvalidJSON .. ": unexpected content after JSON at position " .. decoder.pos)
    end
    
    return result
end

--- 安全解码（不抛出错误）
-- @param str JSON 字符串
-- @param config 配置选项（可选）
-- @return any|nil 解码后的值或 nil
-- @return string|nil 错误信息（解码成功时为 nil）
function JsonUtils.decode_safe(str, config)
    local ok, result = pcall(JsonUtils.decode, str, config)
    if ok then
        return result, nil
    else
        return nil, result
    end
end

--- 验证 JSON 字符串是否有效
-- @param str JSON 字符串
-- @return boolean 是否有效
-- @return string|nil 错误信息（有效时为 nil）
function JsonUtils.validate(str)
    local ok, err = pcall(JsonUtils.decode, str)
    if ok then
        return true, nil
    else
        return false, err
    end
end

--- 判断值是否可以序列化为 JSON
-- @param value 要检查的值
-- @return boolean 是否可以序列化
function JsonUtils.is_json_serializable(value)
    local visited = {}
    
    local function check(v, depth)
        if depth > JsonUtils.Config.max_depth then
            return false
        end
        
        local t = type(v)
        
        if v == nil or t == "boolean" or t == "number" or t == "string" then
            return true
        end
        
        if t == "table" then
            if visited[v] then
                return false -- 循环引用
            end
            visited[v] = true
            
            for k, val in pairs(v) do
                if type(k) ~= "string" and type(k) ~= "number" then
                    return false
                end
                if not check(k, depth + 1) or not check(val, depth + 1) then
                    return false
                end
            end
            
            visited[v] = nil
            return true
        end
        
        return false
    end
    
    return check(value, 0)
end

--- 安全编码（不抛出错误）
-- @param value 要编码的值
-- @param config 配置选项（可选）
-- @return string|nil JSON 字符串或 nil
-- @return string|nil 错误信息（编码成功时为 nil）
function JsonUtils.encode_safe(value, config)
    local ok, result = pcall(JsonUtils.encode, value, config)
    if ok then
        return result, nil
    else
        return nil, result
    end
end

--- 从文件读取 JSON
-- @param filename 文件路径
-- @param config 配置选项（可选）
-- @return any 解码后的 Lua 值
-- @raise 读取或解码失败时抛出错误
function JsonUtils.read_file(filename, config)
    local file, err = io.open(filename, "r")
    if not file then
        error("Cannot open file: " .. filename .. " - " .. (err or "unknown error"))
    end
    
    local content = file:read("*a")
    file:close()
    
    return JsonUtils.decode(content, config)
end

--- 将 JSON 写入文件
-- @param filename 文件路径
-- @param value 要编码的值
-- @param config 配置选项（可选）
-- @raise 写入或编码失败时抛出错误
function JsonUtils.write_file(filename, value, config)
    local file, err = io.open(filename, "w")
    if not file then
        error("Cannot open file for writing: " .. filename .. " - " .. (err or "unknown error"))
    end
    
    local jsonStr = JsonUtils.encode(value, config)
    file:write(jsonStr)
    file:close()
end

--- 将 JSON 写入文件（美化格式）
-- @param filename 文件路径
-- @param value 要编码的值
-- @param indent 缩进字符（可选）
function JsonUtils.write_file_pretty(filename, value, indent)
    local config = {
        pretty = true,
        indent = indent or "  ",
        max_depth = JsonUtils.Config.max_depth,
        sort_keys = JsonUtils.Config.sort_keys,
    }
    JsonUtils.write_file(filename, value, config)
end

--- 深度克隆 Lua 表
-- @param t 要克隆的表
-- @return table 克隆后的表
function JsonUtils.deep_clone(t)
    if type(t) ~= "table" then return t end
    return deepCopy(t)
end

--- 合并两个表
-- @param target 目标表
-- @param source 源表
-- @param deep 是否深度合并（可选，默认为 false）
-- @return table 合并后的表
function JsonUtils.merge(target, source, deep)
    if type(target) ~= "table" then target = {} end
    if type(source) ~= "table" then return target end
    
    for k, v in pairs(source) do
        if deep and type(v) == "table" and type(target[k]) == "table" then
            target[k] = JsonUtils.merge(target[k], v, deep)
        else
            target[k] = v
        end
    end
    
    return target
end

--- 获取 JSON 值的类型
-- @param value Lua 值
-- @return string JSON 类型名："null", "boolean", "number", "string", "array", "object"
function JsonUtils.typeof(value)
    if value == nil then
        return "null"
    elseif type(value) == "boolean" then
        return "boolean"
    elseif type(value) == "number" then
        return "number"
    elseif type(value) == "string" then
        return "string"
    elseif type(value) == "table" then
        if isArray(value) then
            return "array"
        else
            return "object"
        end
    else
        return "unknown"
    end
end

--- 安全获取嵌套值
-- @param t 表
-- @param path 路径（字符串或数组）
-- @param default 默认值（可选）
-- @return any 找到的值或默认值
function JsonUtils.get(t, path, default)
    if type(t) ~= "table" then return default end
    
    local keys
    if type(path) == "string" then
        keys = {}
        for key in string_gmatch(path, "[^%.]+") do
            keys[#keys + 1] = key
        end
    else
        keys = path
    end
    
    local current = t
    for _, key in ipairs(keys) do
        if type(current) ~= "table" then
            return default
        end
        current = current[key]
        if current == nil then
            return default
        end
    end
    
    return current
end

--- 设置嵌套值
-- @param t 表
-- @param path 路径（字符串或数组）
-- @param value 要设置的值
-- @return table 修改后的表
function JsonUtils.set(t, path, value)
    if type(t) ~= "table" then t = {} end
    
    local keys
    if type(path) == "string" then
        keys = {}
        for key in string_gmatch(path, "[^%.]+") do
            keys[#keys + 1] = key
        end
    else
        keys = path
    end
    
    local current = t
    for i = 1, #keys - 1 do
        local key = keys[i]
        if type(current[key]) ~= "table" then
            current[key] = {}
        end
        current = current[key]
    end
    
    current[keys[#keys]] = value
    return t
end

--- 深度比较两个值
-- @param a 第一个值
-- @param b 第二个值
-- @return boolean 是否相等
function JsonUtils.equals(a, b)
    if type(a) ~= type(b) then
        return false
    end
    
    if type(a) ~= "table" then
        return a == b
    end
    
    -- 检查所有键
    local keys = {}
    for k in pairs(a) do keys[k] = true end
    for k in pairs(b) do keys[k] = true end
    
    for k in pairs(keys) do
        if not JsonUtils.equals(a[k], b[k]) then
            return false
        end
    end
    
    return true
end

--- 字符串化（用于调试）
-- @param value 要字符串化的值
-- @param max_depth 最大深度（可选，默认 10）
-- @return string 字符串表示
function JsonUtils.stringify(value, max_depth)
    max_depth = max_depth or 10
    
    local function stringify_inner(v, depth, visited)
        if depth > max_depth then
            return "..."
        end
        
        if v == nil then
            return "nil"
        elseif type(v) == "boolean" then
            return v and "true" or "false"
        elseif type(v) == "number" then
            return tostring(v)
        elseif type(v) == "string" then
            return '"' .. v .. '"'
        elseif type(v) == "table" then
            if visited[v] then
                return "<circular>"
            end
            visited[v] = true
            
            local parts = {}
            if isArray(v) then
                for i, item in ipairs(v) do
                    parts[i] = stringify_inner(item, depth + 1, visited)
                end
                return "[" .. table_concat(parts, ", ") .. "]"
            else
                for k, val in pairs(v) do
                    parts[#parts + 1] = tostring(k) .. ": " .. stringify_inner(val, depth + 1, visited)
                end
                return "{" .. table_concat(parts, ", ") .. "}"
            end
        else
            return "<" .. type(v) .. ">"
        end
    end
    
    return stringify_inner(value, 0, {})
end

-------------------------------------------------------------------------------
-- 模块导出
-------------------------------------------------------------------------------

return JsonUtils