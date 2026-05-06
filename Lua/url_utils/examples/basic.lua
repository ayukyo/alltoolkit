---
-- URL Utilities 基础示例
-- 展示基本的 URL 处理功能
--
-- @author AllToolkit
-- @version 1.0.0

-- 加载模块
package.path = package.path .. ";../?.lua;../?/mod.lua"
local UrlUtils = require("url_utils.mod")

print("\n========================================")
print("URL Utilities 基础示例")
print("========================================\n")

-- =====================
-- 1. URL 编码解码
-- =====================
print("1. URL 编码解码")
print("-------------------")

local text = "Hello, 世界!"
print("原文: " .. text)

local encoded = UrlUtils.url_encode(text)
print("编码: " .. encoded)

local decoded = UrlUtils.url_decode(encoded)
print("解码: " .. decoded)

print()

-- =====================
-- 2. 查询字符串处理
-- =====================
print("2. 查询字符串处理")
print("-------------------")

local query_string = "name=张三&age=25&city=北京"
print("查询字符串: " .. query_string)

local params = UrlUtils.parse_query(query_string)
print("解析结果:")
for key, value in pairs(params) do
    print("  " .. key .. " = " .. value)
end

local built_query = UrlUtils.build_query(params, true)
print("重新构建: " .. built_query)

print()

-- =====================
-- 3. URL 解析
-- =====================
print("3. URL 解析")
print("-------------------")

local url = "https://admin:password@api.example.com:8080/v1/users?page=1&limit=10#section"
print("URL: " .. url)

local parsed = UrlUtils.parse(url)
print("解析结果:")
print("  scheme: " .. tostring(parsed.scheme))
print("  userinfo: " .. tostring(parsed.userinfo))
print("  host: " .. tostring(parsed.host))
print("  port: " .. tostring(parsed.port))
print("  path: " .. tostring(parsed.path))
print("  query: " .. tostring(parsed.query))
print("  fragment: " .. tostring(parsed.fragment))

print()

-- =====================
-- 4. URL 构建
-- =====================
print("4. URL 构建")
print("-------------------")

local new_url = UrlUtils.build({
    scheme = "https",
    host = "example.com",
    port = 443,
    path = "/api/v2/products",
    query = "category=electronics&sort=price",
    fragment = "top-deals"
})
print("构建的 URL: " .. new_url)

print()

-- =====================
-- 5. URL 验证
-- =====================
print("5. URL 验证")
print("-------------------")

local urls = {
    "https://example.com",
    "http://localhost:3000",
    "ftp://files.example.com",
    "not a url",
    "https://user:pass@example.com",
}

for _, test_url in ipairs(urls) do
    local valid = UrlUtils.is_valid(test_url)
    local http = UrlUtils.is_http(test_url)
    local safe = UrlUtils.is_safe(test_url)
    print("URL: " .. test_url)
    print("  有效: " .. tostring(valid) .. " | HTTP: " .. tostring(http) .. " | 安全: " .. tostring(safe))
end

print()

-- =====================
-- 6. URL 规范化
-- =====================
print("6. URL 规范化")
print("-------------------")

local unnormalized = "HTTP://EXAMPLE.COM:80/./path/../to/file/./"
print("原始 URL: " .. unnormalized)

local normalized = UrlUtils.normalize(unnormalized)
print("规范化: " .. tostring(normalized))

print()

-- =====================
-- 7. URL 组件提取
-- =====================
print("7. URL 组件提取")
print("-------------------")

local test_url = "https://www.sub.example.co.uk:443/images/photo.jpg?q=high#main"
print("URL: " .. test_url)

print("  域名: " .. tostring(UrlUtils.get_domain(test_url)))
print("  顶级域名: " .. tostring(UrlUtils.get_tld(test_url)))
print("  子域名: " .. tostring(UrlUtils.get_subdomain(test_url)))
print("  文件名: " .. tostring(UrlUtils.get_filename(test_url)))
print("  扩展名: " .. tostring(UrlUtils.get_extension(test_url)))

print()

-- =====================
-- 8. URL 参数操作
-- =====================
print("8. URL 参数操作")
print("-------------------")

local base_url = "https://example.com/api"
print("基础 URL: " .. base_url)

local with_param = UrlUtils.set_param(base_url, "version", "v2")
print("添加参数: " .. with_param)

local more_params = UrlUtils.set_param(with_param, "format", "json")
print("更多参数: " .. more_params)

local get_version = UrlUtils.get_param(more_params, "version")
print("获取 version: " .. tostring(get_version))

local removed = UrlUtils.remove_param(more_params, "format")
print("删除 format: " .. removed)

print("\n========================================")
print("示例完成")
print("========================================\n")