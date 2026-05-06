---
-- URL Utilities Module
-- URL 处理工具函数库
--
-- 提供常用的 URL 处理功能，包括解析、构建、编码、解码等。
-- 仅使用 Lua 标准库，零依赖。
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local UrlUtils = {}
local UrlUtilsMT = { __index = UrlUtils }

--- 版本号
UrlUtils.VERSION = "1.0.0"

--- 错误类型
UrlUtils.Error = {
    InvalidUrl = "Invalid URL",
    InvalidComponent = "Invalid URL component",
    InvalidPort = "Invalid port number",
    InvalidQuery = "Invalid query string",
}

-------------------------------------------------------------------------------
-- URL 编码与解码
-------------------------------------------------------------------------------

--- URL 编码（百分号编码）
-- @param s 输入字符串
-- @return string 编码后的字符串
function UrlUtils.url_encode(s)
    if s == nil then return nil end
    return (s:gsub("([^%w%.%-_%~])", function(c)
        return string.format("%%%02X", string.byte(c))
    end))
end

--- URL 解码（百分号解码）
-- @param s 输入字符串
-- @return string 解码后的字符串
function UrlUtils.url_decode(s)
    if s == nil then return nil end
    return (s:gsub("%%(%x%x)", function(hex)
        return string.char(tonumber(hex, 16))
    end))
end

--- URL 编码（用于路径部分，保留 /）
-- @param s 输入字符串
-- @return string 编码后的字符串
function UrlUtils.encode_path(s)
    if s == nil then return nil end
    return (s:gsub("([^%w%.%-_%~/])", function(c)
        return string.format("%%%02X", string.byte(c))
    end))
end

--- URL 编码（用于查询字符串）
-- @param s 输入字符串
-- @return string 编码后的字符串（空格变为 +）
function UrlUtils.encode_query(s)
    if s == nil then return nil end
    return (s:gsub("([^%w%.%-_%~])", function(c)
        if c == " " then
            return "+"
        end
        return string.format("%%%02X", string.byte(c))
    end))
end

--- URL 解码（用于查询字符串）
-- @param s 输入字符串
-- @return string 解码后的字符串（+ 变为空格）
function UrlUtils.decode_query(s)
    if s == nil then return nil end
    s = s:gsub("+", " ")
    return UrlUtils.url_decode(s)
end

-------------------------------------------------------------------------------
-- 查询字符串处理
-------------------------------------------------------------------------------

--- 解析查询字符串为表
-- @param query 查询字符串（如 "name=John&age=30"）
-- @return table 键值对表
function UrlUtils.parse_query(query)
    if query == nil or query == "" then return {} end
    
    -- 移除开头的 ?
    query = query:gsub("^%?", "")
    
    local result = {}
    
    for pair in query:gmatch("[^&]+") do
        local eq_pos = pair:find("=")
        local key, value
        
        if eq_pos then
            key = pair:sub(1, eq_pos - 1)
            value = pair:sub(eq_pos + 1)
        else
            key = pair
            value = ""
        end
        
        if key and #key > 0 then
            key = UrlUtils.decode_query(key)
            if value and #value > 0 then
                value = UrlUtils.decode_query(value)
            else
                value = ""
            end
            
            -- 处理重复键，转换为数组
            if result[key] then
                if type(result[key]) == "table" then
                    table.insert(result[key], value)
                else
                    result[key] = { result[key], value }
                end
            else
                result[key] = value
            end
        end
    end
    
    return result
end

--- 将表构建为查询字符串
-- @param params 参数表
-- @param prefix 是否添加 ? 前缀（默认 false）
-- @return string 查询字符串
function UrlUtils.build_query(params, prefix)
    if params == nil or type(params) ~= "table" then return "" end
    
    local parts = {}
    
    for key, value in pairs(params) do
        local encoded_key = UrlUtils.encode_query(tostring(key))
        
        if type(value) == "table" then
            -- 数组值，生成多个相同键
            for _, v in ipairs(value) do
                table.insert(parts, encoded_key .. "=" .. UrlUtils.encode_query(tostring(v)))
            end
        else
            local encoded_value = UrlUtils.encode_query(tostring(value))
            table.insert(parts, encoded_key .. "=" .. encoded_value)
        end
    end
    
    table.sort(parts)  -- 按字母顺序排序，便于缓存
    
    local query = table.concat(parts, "&")
    
    if prefix and #query > 0 then
        return "?" .. query
    end
    
    return query
end

--- 合并查询参数到 URL
-- @param url 原始 URL
-- @param params 额外的参数表
-- @return string 合并后的 URL
function UrlUtils.merge_query(url, params)
    if url == nil then return nil end
    if params == nil or type(params) ~= "table" or next(params) == nil then
        return url
    end
    
    -- 分离 URL 和现有查询
    local base_url, existing_query = url:match("^([^?]*)(%??.*)$")
    if existing_query and existing_query:sub(1, 1) == "?" then
        existing_query = existing_query:sub(2)
    else
        existing_query = ""
    end
    
    -- 合并查询参数
    local merged = UrlUtils.parse_query(existing_query)
    for key, value in pairs(params) do
        merged[key] = value
    end
    
    -- 构建新 URL
    local new_query = UrlUtils.build_query(merged)
    if #new_query > 0 then
        return base_url .. "?" .. new_query
    end
    return base_url
end

-------------------------------------------------------------------------------
-- URL 解析
-------------------------------------------------------------------------------

--- URL 组件
-- @class URL
-- @field scheme 协议（如 http, https）
-- @field userinfo 用户信息（如 user:password）
-- @field host 主机名
-- @field port 端口号
-- @field path 路径
-- @field query 查询字符串（不含 ?）
-- @field fragment 片段标识符（不含 #）

--- 解析 URL
-- @param url URL 字符串
-- @return table|nil URL 组件表，解析失败返回 nil
function UrlUtils.parse(url)
    if url == nil or type(url) ~= "string" or #url == 0 then
        return nil
    end
    
    local result = {
        scheme = nil,
        userinfo = nil,
        host = nil,
        port = nil,
        path = nil,
        query = nil,
        fragment = nil,
    }
    
    -- 解析 fragment
    local fragment_start = url:find("#")
    if fragment_start then
        result.fragment = url:sub(fragment_start + 1)
        url = url:sub(1, fragment_start - 1)
    end
    
    -- 解析 query
    local query_start = url:find("?")
    if query_start then
        result.query = url:sub(query_start + 1)
        url = url:sub(1, query_start - 1)
    end
    
    -- 解析 scheme
    local scheme_end = url:find("://")
    if scheme_end then
        result.scheme = url:sub(1, scheme_end - 1):lower()
        url = url:sub(scheme_end + 3)
    end
    
    -- 解析路径部分
    local path_start = url:find("/")
    if path_start then
        result.path = url:sub(path_start)
        url = url:sub(1, path_start - 1)
    else
        result.path = "/"
    end
    
    -- 解析 userinfo 和 host:port
    local at_pos = url:find("@")
    if at_pos then
        result.userinfo = url:sub(1, at_pos - 1)
        url = url:sub(at_pos + 1)
    end
    
    -- 解析 port（IPv6 地址处理）
    local host = url
    
    -- 检查是否是 IPv6 地址（包含方括号）
    if host:sub(1, 1) == "[" then
        local bracket_end = host:find("]")
        if bracket_end then
            result.host = host:sub(1, bracket_end)
            local port_part = host:sub(bracket_end + 1)
            if port_part:sub(1, 1) == ":" then
                result.port = port_part:sub(2)
            end
        end
    else
        -- 普通 host:port
        local colon_pos = host:reverse():find(":")
        if colon_pos then
            -- 检查是否有多个冒号（可能是 IPv6 地址）
            local colon_count = 0
            for _ in host:gmatch(":") do
                colon_count = colon_count + 1
            end
            
            if colon_count == 1 then
                -- 只有一个冒号，是 host:port
                result.host = host:sub(1, #host - colon_pos)
                result.port = host:sub(#host - colon_pos + 2)
            else
                -- 多个冒号，可能是 IPv6
                result.host = host
            end
        else
            result.host = host
        end
    end
    
    -- 验证 port
    if result.port then
        result.port = tonumber(result.port)
        if result.port == nil or result.port < 1 or result.port > 65535 then
            return nil  -- 无效端口
        end
    end
    
    return result
end

--- 构建 URL
-- @param components URL 组件表
-- @return string URL 字符串
function UrlUtils.build(components)
    if components == nil or type(components) ~= "table" then
        return nil
    end
    
    local result = {}
    
    -- 添加 scheme
    if components.scheme then
        table.insert(result, components.scheme:lower())
        table.insert(result, "://")
    end
    
    -- 添加 userinfo
    if components.userinfo then
        table.insert(result, components.userinfo)
        table.insert(result, "@")
    end
    
    -- 添加 host
    if components.host then
        table.insert(result, components.host)
    end
    
    -- 添加 port
    if components.port then
        table.insert(result, ":")
        table.insert(result, tostring(components.port))
    end
    
    -- 添加 path
    if components.path then
        if components.path:sub(1, 1) ~= "/" then
            table.insert(result, "/")
        end
        table.insert(result, components.path)
    else
        table.insert(result, "/")
    end
    
    -- 添加 query
    if components.query then
        table.insert(result, "?")
        table.insert(result, components.query)
    end
    
    -- 添加 fragment
    if components.fragment then
        table.insert(result, "#")
        table.insert(result, components.fragment)
    end
    
    return table.concat(result)
end

-------------------------------------------------------------------------------
-- URL 验证
-------------------------------------------------------------------------------

--- 检查是否是有效的 URL
-- @param url URL 字符串
-- @return boolean 是否有效
function UrlUtils.is_valid(url)
    if url == nil or type(url) ~= "string" or #url == 0 then
        return false
    end
    
    local parsed = UrlUtils.parse(url)
    return parsed ~= nil and parsed.host ~= nil and #parsed.host > 0
end

--- 检查是否是 HTTP/HTTPS URL
-- @param url URL 字符串
-- @return boolean 是否是 HTTP URL
function UrlUtils.is_http(url)
    if not UrlUtils.is_valid(url) then return false end
    local parsed = UrlUtils.parse(url)
    return parsed.scheme == "http" or parsed.scheme == "https"
end

--- 检查是否是安全的 URL（仅 HTTP/HTTPS，无用户信息）
-- @param url URL 字符串
-- @return boolean 是否安全
function UrlUtils.is_safe(url)
    if not UrlUtils.is_valid(url) then return false end
    local parsed = UrlUtils.parse(url)
    if parsed.scheme ~= "http" and parsed.scheme ~= "https" then
        return false
    end
    if parsed.userinfo then
        return false
    end
    return true
end

--- 获取默认端口
-- @param scheme 协议名
-- @return number|nil 默认端口号
function UrlUtils.default_port(scheme)
    if scheme == nil then return nil end
    
    local ports = {
        http = 80,
        https = 443,
        ftp = 21,
        ssh = 22,
        telnet = 23,
        smtp = 25,
        dns = 53,
        pop3 = 110,
        imap = 143,
        ldap = 389,
        mysql = 3306,
        postgresql = 5432,
        redis = 6379,
        mongodb = 27017,
    }
    
    return ports[scheme:lower()]
end

--- 规范化 URL
-- @param url URL 字符串
-- @return string|nil 规范化后的 URL
function UrlUtils.normalize(url)
    if not UrlUtils.is_valid(url) then return nil end
    
    local parsed = UrlUtils.parse(url)
    
    -- 小写 scheme 和 host
    if parsed.scheme then
        parsed.scheme = parsed.scheme:lower()
    end
    if parsed.host then
        parsed.host = parsed.host:lower()
    end
    
    -- 移除默认端口
    if parsed.port then
        local default = UrlUtils.default_port(parsed.scheme)
        if default and parsed.port == default then
            parsed.port = nil
        end
    end
    
    -- 规范化路径
    if parsed.path then
        parsed.path = UrlUtils.normalize_path(parsed.path)
    end
    
    -- 解码并重新编码查询参数
    if parsed.query and #parsed.query > 0 then
        local params = UrlUtils.parse_query(parsed.query)
        parsed.query = UrlUtils.build_query(params)
    end
    
    return UrlUtils.build(parsed)
end

--- 规范化路径（处理 . 和 ..）
-- @param path 路径字符串
-- @return string 规范化后的路径
function UrlUtils.normalize_path(path)
    if path == nil or #path == 0 then return "/" end
    
    -- 分割路径
    local parts = {}
    for part in path:gmatch("[^/]+") do
        if part == ".." then
            if #parts > 0 then
                table.remove(parts)
            end
        elseif part ~= "." then
            table.insert(parts, part)
        end
    end
    
    -- 重新构建路径
    local result = "/" .. table.concat(parts, "/")
    
    -- 保留尾部斜杠
    if path:sub(-1) == "/" and result:sub(-1) ~= "/" then
        result = result .. "/"
    end
    
    return result
end

-------------------------------------------------------------------------------
-- URL 操作
-------------------------------------------------------------------------------

--- 获取 URL 的文件扩展名
-- @param url URL 字符串
-- @return string|nil 扩展名（不含点），无扩展名返回 nil
function UrlUtils.get_extension(url)
    if url == nil then return nil end
    
    local parsed = UrlUtils.parse(url)
    if parsed == nil or parsed.path == nil then return nil end
    
    -- 移除查询和片段
    local path = parsed.path
    
    -- 获取最后一个路径段
    local filename = path:match("([^/]+)$")
    if filename == nil then return nil end
    
    -- 获取扩展名
    local ext = filename:match("%.([^%.]+)$")
    return ext
end

--- 获取 URL 的文件名
-- @param url URL 字符串
-- @return string|nil 文件名
function UrlUtils.get_filename(url)
    if url == nil then return nil end
    
    local parsed = UrlUtils.parse(url)
    if parsed == nil or parsed.path == nil then return nil end
    
    return parsed.path:match("([^/]+)$")
end

--- 获取 URL 的域名
-- @param url URL 字符串
-- @return string|nil 域名
function UrlUtils.get_domain(url)
    if url == nil then return nil end
    
    local parsed = UrlUtils.parse(url)
    if parsed == nil or parsed.host == nil then return nil end
    
    -- 移除 IPv6 方括号
    local host = parsed.host
    if host:sub(1, 1) == "[" and host:sub(-1) == "]" then
        return host:sub(2, -2)
    end
    
    return host
end

--- 获取 URL 的顶级域名
-- @param url URL 字符串
-- @return string|nil 顶级域名
function UrlUtils.get_tld(url)
    local domain = UrlUtils.get_domain(url)
    if domain == nil then return nil end
    
    -- IPv6 地址返回 nil
    if domain:match("^%x%x*:%x%x*:") then
        return nil
    end
    
    -- IPv4 地址返回 nil
    if domain:match("^%d+%.%d+%.%d+%.%d+$") then
        return nil
    end
    
    -- 获取最后两部分
    local parts = {}
    for part in domain:gmatch("[^%.]+") do
        table.insert(parts, part)
    end
    
    if #parts >= 2 then
        return parts[#parts - 1] .. "." .. parts[#parts]
    elseif #parts == 1 then
        return parts[1]
    end
    
    return nil
end

--- 获取 URL 的子域名
-- @param url URL 字符串
-- @return string|nil 子域名（不含主域名）
function UrlUtils.get_subdomain(url)
    local domain = UrlUtils.get_domain(url)
    if domain == nil then return nil end
    
    local parts = {}
    for part in domain:gmatch("[^%.]+") do
        table.insert(parts, part)
    end
    
    if #parts > 2 then
        local subdomain_parts = {}
        for i = 1, #parts - 2 do
            table.insert(subdomain_parts, parts[i])
        end
        return table.concat(subdomain_parts, ".")
    end
    
    return nil
end

--- 拼接 URL 路径
-- @param base 基础 URL
-- @param path 相对路径
-- @return string 拼接后的 URL
function UrlUtils.join(base, path)
    if base == nil then return path end
    if path == nil then return base end
    
    -- 如果 path 是绝对 URL，直接返回
    if path:match("^[a-zA-Z][a-zA-Z0-9+%.%-]*://") then
        return path
    end
    
    -- 如果 path 是绝对路径
    if path:sub(1, 1) == "/" then
        local parsed = UrlUtils.parse(base)
        if parsed then
            parsed.path = path
            parsed.query = nil
            parsed.fragment = nil
            return UrlUtils.build(parsed)
        end
        return nil
    end
    
    -- 相对路径拼接
    local parsed = UrlUtils.parse(base)
    if parsed == nil then return nil end
    
    -- 移除查询和片段
    parsed.query = nil
    parsed.fragment = nil
    
    -- 拼接路径
    if parsed.path then
        -- 获取目录部分
        local dir = parsed.path:match("^(.*)/[^/]*$") or "/"
        parsed.path = UrlUtils.normalize_path(dir .. "/" .. path)
    else
        parsed.path = UrlUtils.normalize_path("/" .. path)
    end
    
    return UrlUtils.build(parsed)
end

--- 解析相对 URL
-- @param url 相对或绝对 URL
-- @param base 基础 URL
-- @return string|nil 绝对 URL
function UrlUtils.resolve(url, base)
    if url == nil then return nil end
    
    -- 如果已经是绝对 URL
    if url:match("^[a-zA-Z][a-zA-Z0-9+%.%-]*://") then
        return UrlUtils.normalize(url)
    end
    
    if base == nil then return nil end
    
    local base_parsed = UrlUtils.parse(base)
    if base_parsed == nil then return nil end
    
    -- 协议相对 URL (//example.com/path)
    if url:sub(1, 2) == "//" then
        base_parsed.host = url:sub(3)
        -- 解析 host 和可能的 port/path
        local host_part = url:sub(3)
        local path_start = host_part:find("/")
        if path_start then
            base_parsed.host = host_part:sub(1, path_start - 1)
            base_parsed.path = host_part:sub(path_start)
        else
            base_parsed.host = host_part
            base_parsed.path = "/"
        end
        base_parsed.query = nil
        base_parsed.fragment = nil
        return UrlUtils.build(base_parsed)
    end
    
    -- 绝对路径
    if url:sub(1, 1) == "/" then
        base_parsed.path = url
        -- 移除查询和片段，稍后从 url 解析
        local query_start = url:find("?")
        local fragment_start = url:find("#")
        
        if fragment_start then
            base_parsed.fragment = url:sub(fragment_start + 1)
            url = url:sub(1, fragment_start - 1)
        end
        if query_start then
            base_parsed.query = url:sub(query_start + 1)
            base_parsed.path = url:sub(1, query_start - 1)
        end
        
        return UrlUtils.build(base_parsed)
    end
    
    -- 相对路径
    return UrlUtils.join(base, url)
end

--- 判断两个 URL 是否同源
-- @param url1 第一个 URL
-- @param url2 第二个 URL
-- @return boolean 是否同源
function UrlUtils.is_same_origin(url1, url2)
    local p1 = UrlUtils.parse(url1)
    local p2 = UrlUtils.parse(url2)
    
    if p1 == nil or p2 == nil then return false end
    
    return p1.scheme == p2.scheme and p1.host == p2.host and p1.port == p2.port
end

-------------------------------------------------------------------------------
-- URL 参数提取
-------------------------------------------------------------------------------

--- 从 URL 获取指定查询参数
-- @param url URL 字符串
-- @param key 参数名
-- @return string|nil 参数值
function UrlUtils.get_param(url, key)
    if url == nil or key == nil then return nil end
    
    local parsed = UrlUtils.parse(url)
    if parsed == nil or parsed.query == nil then return nil end
    
    local params = UrlUtils.parse_query(parsed.query)
    return params[key]
end

--- 设置 URL 查询参数
-- @param url URL 字符串
-- @param key 参数名
-- @param value 参数值
-- @return string 新的 URL
function UrlUtils.set_param(url, key, value)
    if url == nil then return nil end
    
    local parsed = UrlUtils.parse(url)
    if parsed == nil then return nil end
    
    local params = UrlUtils.parse_query(parsed.query)
    params[key] = value
    parsed.query = UrlUtils.build_query(params)
    
    return UrlUtils.build(parsed)
end

--- 删除 URL 查询参数
-- @param url URL 字符串
-- @param key 参数名
-- @return string 新的 URL
function UrlUtils.remove_param(url, key)
    if url == nil then return nil end
    
    local parsed = UrlUtils.parse(url)
    if parsed == nil then return nil end
    
    local params = UrlUtils.parse_query(parsed.query)
    params[key] = nil
    parsed.query = UrlUtils.build_query(params)
    
    if parsed.query == "" then
        parsed.query = nil
    end
    
    return UrlUtils.build(parsed)
end

-------------------------------------------------------------------------------
-- 实用工具
-------------------------------------------------------------------------------

--- 获取 URL 的哈希值（用于缓存键）
-- @param url URL 字符串
-- @return string|nil MD5 风格的哈希值（使用简单哈希算法）
function UrlUtils.hash(url)
    if url == nil then return nil end
    
    -- 使用 DJB2 哈希算法
    local hash_value = 5381
    
    for i = 1, #url do
        local c = string.byte(url, i)
        hash_value = ((hash_value * 33) + c) % (2 ^ 32)
    end
    
    -- 转换为十六进制
    return string.format("%08x", hash_value)
end

--- 创建 URL 构建器
-- @param scheme 协议（可选）
-- @param host 主机名（可选）
-- @return table URL 构建器对象
function UrlUtils.builder(scheme, host)
    local obj = {
        scheme = scheme,
        userinfo = nil,
        host = host,
        port = nil,
        path = nil,
        query_params = {},
        fragment = nil,
    }
    
    local function build_query_string(self)
        return UrlUtils.build_query(self.query_params)
    end
    
    return {
        set_scheme = function(self, s)
            obj.scheme = s
            return self
        end,
        set_userinfo = function(self, ui)
            obj.userinfo = ui
            return self
        end,
        set_host = function(self, h)
            obj.host = h
            return self
        end,
        set_port = function(self, p)
            obj.port = tonumber(p)
            return self
        end,
        set_path = function(self, p)
            obj.path = p
            return self
        end,
        add_path = function(self, p)
            if obj.path == nil then
                obj.path = p
            else
                if obj.path:sub(-1) == "/" and p:sub(1, 1) == "/" then
                    obj.path = obj.path .. p:sub(2)
                elseif obj.path:sub(-1) ~= "/" and p:sub(1, 1) ~= "/" then
                    obj.path = obj.path .. "/" .. p
                else
                    obj.path = obj.path .. p
                end
            end
            return self
        end,
        add_param = function(self, key, value)
            obj.query_params[key] = value
            return self
        end,
        add_params = function(self, params)
            for k, v in pairs(params) do
                obj.query_params[k] = v
            end
            return self
        end,
        remove_param = function(self, key)
            obj.query_params[key] = nil
            return self
        end,
        set_fragment = function(self, f)
            obj.fragment = f
            return self
        end,
        build = function(self)
            local query = build_query_string(obj)
            return UrlUtils.build({
                scheme = obj.scheme,
                userinfo = obj.userinfo,
                host = obj.host,
                port = obj.port,
                path = obj.path,
                query = #query > 0 and query or nil,
                fragment = obj.fragment,
            })
        end,
    }
end

-------------------------------------------------------------------------------
-- 导出模块
-------------------------------------------------------------------------------

return UrlUtils