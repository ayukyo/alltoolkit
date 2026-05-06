---
-- URL Builder 示例
-- 展示流式 API 构建 URL
--
-- @author AllToolkit
-- @version 1.0.0

-- 加载模块
package.path = package.path .. ";../?.lua;../?/mod.lua"
local UrlUtils = require("url_utils.mod")

print("\n========================================")
print("URL Builder 流式 API 示例")
print("========================================\n")

-- =====================
-- 1. 基础构建
-- =====================
print("1. 基础构建")
print("-------------------")

local url = UrlUtils.builder("https", "api.example.com")
    :set_path("/v1")
    :add_param("format", "json")
    :build()

print("构建结果: " .. url)

print()

-- =====================
-- 2. 添加路径段
-- =====================
print("2. 添加路径段")
print("-------------------")

local url = UrlUtils.builder("https", "example.com")
    :set_path("/api")
    :add_path("/users")
    :add_path("/123")
    :add_path("profile")
    :build()

print("路径拼接: " .. url)

print()

-- =====================
-- 3. 添加多个参数
-- =====================
print("3. 添加多个参数")
print("-------------------")

local url = UrlUtils.builder("https", "search.example.com")
    :set_path("/search")
    :add_param("q", "lua url parser")
    :add_param("page", "1")
    :add_param("limit", "20")
    :add_param("sort", "relevance")
    :set_fragment("results")
    :build()

print("多参数 URL: " .. url)

print()

-- =====================
-- 4. 批量添加参数
-- =====================
print("4. 批量添加参数")
print("-------------------")

local url = UrlUtils.builder("https", "api.example.com")
    :set_path("/products")
    :add_params({
        category = "electronics",
        brand = "sony",
        min_price = "100",
        max_price = "1000",
    })
    :build()

print("批量参数: " .. url)

print()

-- =====================
-- 5. 完整示例
-- =====================
print("5. 完整示例")
print("-------------------")

local url = UrlUtils.builder("https", "api.github.com")
    :set_port(443)  -- 通常可以省略，因为是默认端口
    :set_path("/repos")
    :add_path("/owner")
    :add_path("/repo")
    :add_path("/issues")
    :add_params({
        state = "open",
        sort = "created",
        direction = "desc",
    })
    :set_fragment("issue-1")
    :build()

print("GitHub API URL: " .. url)

print()

-- =====================
-- 6. 链式操作灵活性
-- =====================
print("6. 链式操作灵活性")
print("-------------------")

-- 可以随时调整任何部分
local builder = UrlUtils.builder("http", "localhost")
    :set_port(3000)

-- 添加基础路径
builder:set_path("/api")

-- 可以分步添加参数
builder:add_param("version", "v1")
builder:add_param("debug", "true")

-- 可以修改已设置的值
builder:set_port(8080)

-- 最终构建
local url = builder:build()
print("灵活构建: " .. url)

-- =====================
-- 7. 删除参数
-- =====================
print("\n7. 删除参数")
print("-------------------")

local url = UrlUtils.builder("https", "example.com")
    :set_path("/api")
    :add_param("a", "1")
    :add_param("b", "2")
    :add_param("c", "3")
    :build()

print("完整参数: " .. url)

-- 从已有 URL 继续构建... 
-- 注意：builder 不支持从 URL 解析，需要手动处理
local url2 = UrlUtils.remove_param(url, "b")
print("删除 b: " .. url2)

print("\n========================================")
print("示例完成")
print("========================================\n")