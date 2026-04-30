--[[
Base64 Utils - Base64 编码/解码工具库
零外部依赖，纯 Lua 实现

功能：
- 标准 Base64 编码/解码
- URL 安全 Base64 编码/解码
- Base64 数据验证
- 编码数据统计
]]

local base64_utils = {}

-- Base64 字符表
local STANDARD_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
local URLSAFE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
local STANDARD_PADDING = "="

-- 反向查找表
local function build_decode_table(chars)
    local t = {}
    for i = 1, 64 do
        t[string.sub(chars, i, i)] = i - 1
    end
    return t
end

local STANDARD_DECODE_TABLE = build_decode_table(STANDARD_CHARS)
local URLSAFE_DECODE_TABLE = build_decode_table(URLSAFE_CHARS)

--[[
编码为 Base64
@param data string - 要编码的数据
@param urlsafe boolean - 是否使用 URL 安全字符（可选，默认 false）
@return string - Base64 编码结果
]]
function base64_utils.encode(data, urlsafe)
    if type(data) ~= "string" then
        error("encode: 参数必须是字符串")
    end
    
    if #data == 0 then
        return ""
    end
    
    local chars = urlsafe and URLSAFE_CHARS or STANDARD_CHARS
    local padding = urlsafe and "" or STANDARD_PADDING
    
    local result = {}
    local i = 1
    local len = #data
    
    -- 处理每 3 个字节
    while i <= len - 2 do
        local b1 = string.byte(data, i)
        local b2 = string.byte(data, i + 1)
        local b3 = string.byte(data, i + 2)
        
        local n = b1 * 65536 + b2 * 256 + b3
        
        table.insert(result, string.sub(chars, math.floor(n / 262144) % 64 + 1, math.floor(n / 262144) % 64 + 1))
        table.insert(result, string.sub(chars, math.floor(n / 4096) % 64 + 1, math.floor(n / 4096) % 64 + 1))
        table.insert(result, string.sub(chars, math.floor(n / 64) % 64 + 1, math.floor(n / 64) % 64 + 1))
        table.insert(result, string.sub(chars, n % 64 + 1, n % 64 + 1))
        
        i = i + 3
    end
    
    -- 处理剩余字节
    local remaining = len - i + 1
    
    if remaining == 1 then
        local b1 = string.byte(data, i)
        local n = b1 * 16
        
        table.insert(result, string.sub(chars, math.floor(b1 / 4) + 1, math.floor(b1 / 4) + 1))
        table.insert(result, string.sub(chars, (b1 % 4) * 16 + 1, (b1 % 4) * 16 + 1))
        
        if not urlsafe then
            table.insert(result, padding)
            table.insert(result, padding)
        end
    elseif remaining == 2 then
        local b1 = string.byte(data, i)
        local b2 = string.byte(data, i + 1)
        local n = b1 * 1024 + b2 * 4
        
        table.insert(result, string.sub(chars, math.floor(n / 4096) % 64 + 1, math.floor(n / 4096) % 64 + 1))
        table.insert(result, string.sub(chars, math.floor(n / 64) % 64 + 1, math.floor(n / 64) % 64 + 1))
        table.insert(result, string.sub(chars, n % 64 + 1, n % 64 + 1))
        
        if not urlsafe then
            table.insert(result, padding)
        end
    end
    
    return table.concat(result)
end

--[[
解码 Base64 字符串
@param encoded string - Base64 编码的字符串
@param urlsafe boolean - 是否使用 URL 安全字符（可选，自动检测）
@return string - 解码后的原始数据
@return nil|string - 错误信息（如果失败）
]]
function base64_utils.decode(encoded, urlsafe)
    if type(encoded) ~= "string" then
        return nil, "decode: 参数必须是字符串"
    end
    
    if #encoded == 0 then
        return "", nil
    end
    
    -- 移除空白字符
    encoded = string.gsub(encoded, "%s", "")
    
    -- 检测是否 URL 安全格式
    local is_urlsafe = urlsafe
    if is_urlsafe == nil then
        is_urlsafe = string.find(encoded, "-") ~= nil or string.find(encoded, "_") ~= nil
    end
    
    local decode_table = is_urlsafe and URLSAFE_DECODE_TABLE or STANDARD_DECODE_TABLE
    
    -- 移除 padding
    local padding_count = 0
    while string.sub(encoded, #encoded, #encoded) == STANDARD_PADDING do
        padding_count = padding_count + 1
        encoded = string.sub(encoded, 1, #encoded - 1)
    end
    
    -- URL安全格式允许任意长度（无padding）
    -- 标准格式要求长度是4的倍数（或有padding）
    if not is_urlsafe then
        if #encoded % 4 ~= 0 and padding_count == 0 then
            return nil, "decode: 无效的 Base64 长度"
        end
    end
    
    local result = {}
    local i = 1
    local len = #encoded
    
    -- 处理每 4 个字符
    while i <= len - 3 do
        local c1 = string.sub(encoded, i, i)
        local c2 = string.sub(encoded, i + 1, i + 1)
        local c3 = string.sub(encoded, i + 2, i + 2)
        local c4 = string.sub(encoded, i + 3, i + 3)
        
        local v1 = decode_table[c1]
        local v2 = decode_table[c2]
        local v3 = decode_table[c3]
        local v4 = decode_table[c4]
        
        if not (v1 and v2 and v3 and v4) then
            return nil, "decode: 包含无效的 Base64 字符"
        end
        
        local n = v1 * 262144 + v2 * 4096 + v3 * 64 + v4
        
        table.insert(result, string.char(math.floor(n / 65536) % 256))
        table.insert(result, string.char(math.floor(n / 256) % 256))
        table.insert(result, string.char(n % 256))
        
        i = i + 4
    end
    
    -- 处理剩余字符（处理 padding 情况）
    local remaining = len - i + 1
    
    if remaining >= 2 then
        local c1 = string.sub(encoded, i, i)
        local c2 = string.sub(encoded, i + 1, i + 1)
        
        local v1 = decode_table[c1]
        local v2 = decode_table[c2]
        
        if not (v1 and v2) then
            return nil, "decode: 包含无效的 Base64 字符"
        end
        
        if remaining == 2 or padding_count >= 2 then
            -- 只有第一个字节有效
            table.insert(result, string.char(v1 * 4 + math.floor(v2 / 16)))
        elseif remaining >= 3 then
            local c3 = string.sub(encoded, i + 2, i + 2)
            local v3 = decode_table[c3]
            
            if not v3 then
                return nil, "decode: 包含无效的 Base64 字符"
            end
            
            if remaining == 3 or padding_count >= 1 then
                -- 前两个字节有效
                table.insert(result, string.char(v1 * 4 + math.floor(v2 / 16)))
                table.insert(result, string.char((v2 % 16) * 16 + math.floor(v3 / 4)))
            end
        end
    end
    
    return table.concat(result), nil
end

--[[
验证是否为有效的 Base64 字符串
@param str string - 要验证的字符串
@param urlsafe boolean - 是否检查 URL 安全格式（可选，自动检测）
@return boolean - 是否有效
]]
function base64_utils.is_valid(str, urlsafe)
    if type(str) ~= "string" or #str == 0 then
        return false
    end
    
    -- 检查 padding 是否只在末尾（标准格式）
    -- 首先检测格式
    local is_urlsafe = urlsafe
    if is_urlsafe == nil then
        is_urlsafe = string.find(str, "-") ~= nil or string.find(str, "_") ~= nil
    end
    
    -- 标准格式检查：padding 只能在末尾
    if not is_urlsafe then
        -- 检查是否有 padding 在非末尾位置
        local first_padding = string.find(str, "=", 1, true)
        if first_padding then
            -- padding 之后不能有非 padding 字符
            local after_padding = string.sub(str, first_padding + 1)
            if string.find(after_padding, "[^=]", 1) then
                return false
            end
            -- 最多两个 padding
            local padding_count = #str - first_padding + 1
            if padding_count > 2 then
                return false
            end
        end
    end
    
    -- 移除空白和 padding 进行字符验证
    local cleaned = string.gsub(str, "%s", "")
    cleaned = string.gsub(cleaned, "=+$", "")
    
    if #cleaned == 0 then
        return false
    end
    
    -- 构建有效字符集
    local valid_chars
    if is_urlsafe then
        valid_chars = URLSAFE_CHARS
    else
        valid_chars = STANDARD_CHARS
    end
    
    -- 验证每个字符
    for i = 1, #cleaned do
        local c = string.sub(cleaned, i, i)
        if string.find(valid_chars, c, 1, true) == nil then
            return false
        end
    end
    
    return true
end

--[[
获取 Base64 编码统计信息
@param data string - 要编码的数据
@param urlsafe boolean - 是否使用 URL 安全格式（可选）
@return table - 统计信息表
]]
function base64_utils.get_encode_stats(data, urlsafe)
    if type(data) ~= "string" then
        return nil
    end
    
    local encoded = base64_utils.encode(data, urlsafe)
    local padding_len = urlsafe and 0 or ((3 - #data % 3) % 3)
    
    return {
        original_size = #data,
        encoded_size = #encoded,
        overhead_bytes = #encoded - #data,
        overhead_percent = math.floor((#encoded / #data - 1) * 100 + 0.5),
        padding_count = padding_len,
        is_urlsafe = urlsafe or false
    }
end

--[[
编码为 URL 安全的 Base64（无 padding）
@param data string - 要编码的数据
@return string - URL 安全的 Base64 编码结果
]]
function base64_utils.encode_urlsafe(data)
    return base64_utils.encode(data, true)
end

--[[
解码 URL 安全的 Base64
@param encoded string - URL 安全的 Base64 编码字符串
@return string - 解码后的原始数据
@return nil|string - 错误信息（如果失败）
]]
function base64_utils.decode_urlsafe(encoded)
    return base64_utils.decode(encoded, true)
end

--[[
编码表格为 Base64 JSON
@param tbl table - 要编码的表格
@return string - Base64 编码的 JSON 数据
@return nil|string - 错误信息（如果失败）
]]
function base64_utils.encode_table(tbl)
    if type(tbl) ~= "table" then
        return nil, "encode_table: 参数必须是表格"
    end
    
    -- 简单的 JSON 序列化（零依赖）
    local function serialize(val, visited)
        visited = visited or {}
        
        if type(val) == "nil" then
            return "null"
        elseif type(val) == "boolean" then
            return val and "true" or "false"
        elseif type(val) == "number" then
            if math.floor(val) == val then
                return tostring(val)
            else
                return string.format("%.15g", val)
            end
        elseif type(val) == "string" then
            -- 转义特殊字符
            local escaped = string.gsub(val, '[%z\1-\31\\"]', function(c)
                return string.format("\\u%04x", string.byte(c))
            end)
            escaped = string.gsub(escaped, "\\\\", "\\")
            escaped = string.gsub(escaped, '\\"', '"')
            return '"' .. escaped .. '"'
        elseif type(val) == "table" then
            if visited[val] then
                return '"[循环引用]"'
            end
            visited[val] = true
            
            -- 检查是否为数组
            local is_array = true
            local max_index = 0
            for k, _ in pairs(val) do
                if type(k) ~= "number" or k <= 0 or math.floor(k) ~= k then
                    is_array = false
                    break
                end
                if k > max_index then max_index = k end
            end
            
            if is_array and max_index > 0 then
                local parts = {}
                for i = 1, max_index do
                    table.insert(parts, serialize(val[i], visited))
                end
                return "[" .. table.concat(parts, ",") .. "]"
            else
                -- 对象
                local parts = {}
                for k, v in pairs(val) do
                    local key = type(k) == "string" and k or tostring(k)
                    table.insert(parts, '"' .. key .. '":' .. serialize(v, visited))
                end
                return "{" .. table.concat(parts, ",") .. "}"
            end
        else
            return '"' .. tostring(val) .. '"'
        end
    end
    
    local json = serialize(tbl)
    return base64_utils.encode(json), nil
end

--[[
解码 Base64 JSON 为表格
@param encoded string - Base64 编码的 JSON 数据
@return table|nil - 解码后的表格
@return nil|string - 错误信息（如果失败）
]]
function base64_utils.decode_table(encoded)
    local json, err = base64_utils.decode(encoded)
    if err then
        return nil, err
    end
    
    -- 简单的 JSON 解析（零依赖）
    local function parse_json(str, pos)
        pos = pos or 1
        
        -- 跳过空白
        local function skip_whitespace()
            while pos <= #str and string.find(string.sub(str, pos, pos), "%s") do
                pos = pos + 1
            end
        end
        
        skip_whitespace()
        
        if pos > #str then
            return nil, pos, "意外的结束"
        end
        
        local char = string.sub(str, pos, pos)
        
        -- null
        if string.sub(str, pos, pos + 3) == "null" then
            return nil, pos + 4
        end
        
        -- boolean
        if string.sub(str, pos, pos + 3) == "true" then
            return true, pos + 4
        end
        if string.sub(str, pos, pos + 4) == "false" then
            return false, pos + 5
        end
        
        -- number
        if string.find(char, "[%d%-]") then
            local num_end = pos
            while num_end <= #str and string.find(string.sub(str, num_end, num_end), "[%d%.eE%+%-]") do
                num_end = num_end + 1
            end
            local num_str = string.sub(str, pos, num_end - 1)
            return tonumber(num_str), num_end
        end
        
        -- string
        if char == '"' then
            pos = pos + 1
            local result = {}
            while pos <= #str do
                local c = string.sub(str, pos, pos)
                if c == '"' then
                    return table.concat(result), pos + 1
                elseif c == "\\" then
                    pos = pos + 1
                    local escaped = string.sub(str, pos, pos)
                    if escaped == "n" then
                        table.insert(result, "\n")
                    elseif escaped == "t" then
                        table.insert(result, "\t")
                    elseif escaped == "r" then
                        table.insert(result, "\r")
                    elseif escaped == '"' then
                        table.insert(result, '"')
                    elseif escaped == "\\" then
                        table.insert(result, "\\")
                    elseif escaped == "u" then
                        local hex = string.sub(str, pos + 1, pos + 4)
                        local code = tonumber(hex, 16)
                        if code then
                            table.insert(result, string.char(code))
                        end
                        pos = pos + 4
                    else
                        table.insert(result, escaped)
                    end
                else
                    table.insert(result, c)
                end
                pos = pos + 1
            end
            return table.concat(result), pos
        end
        
        -- array
        if char == "[" then
            pos = pos + 1
            local arr = {}
            skip_whitespace()
            if string.sub(str, pos, pos) == "]" then
                return arr, pos + 1
            end
            while true do
                local val
                val, pos = parse_json(str, pos)
                table.insert(arr, val)
                skip_whitespace()
                local next_char = string.sub(str, pos, pos)
                if next_char == "]" then
                    return arr, pos + 1
                elseif next_char == "," then
                    pos = pos + 1
                else
                    return nil, pos, "期望 ',' 或 ']'"
                end
            end
        end
        
        -- object
        if char == "{" then
            pos = pos + 1
            local obj = {}
            skip_whitespace()
            if string.sub(str, pos, pos) == "}" then
                return obj, pos + 1
            end
            while true do
                skip_whitespace()
                local key
                key, pos = parse_json(str, pos)
                skip_whitespace()
                if string.sub(str, pos, pos) ~= ":" then
                    return nil, pos, "期望 ':'"
                end
                pos = pos + 1
                local val
                val, pos = parse_json(str, pos)
                obj[key] = val
                skip_whitespace()
                local next_char = string.sub(str, pos, pos)
                if next_char == "}" then
                    return obj, pos + 1
                elseif next_char == "," then
                    pos = pos + 1
                else
                    return nil, pos, "期望 ',' 或 '}'"
                end
            end
        end
        
        return nil, pos, "未知的 JSON 值"
    end
    
    local result, _, parse_err = parse_json(json)
    if parse_err then
        return nil, "JSON 解析错误: " .. parse_err
    end
    
    return result, nil
end

return base64_utils