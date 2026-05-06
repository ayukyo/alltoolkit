---
-- URL Utilities Test Suite
-- URL 工具函数测试套件
--
-- @author AllToolkit
-- @version 1.0.0

-- 加载模块
package.path = package.path .. ";./?.lua;./?/init.lua;./mod.lua"
local UrlUtils = dofile("mod.lua")

-- 测试工具函数
local function assertEquals(actual, expected, message)
    if actual ~= expected then
        print("[FAIL] " .. (message or "Assertion failed"))
        print("  Expected: " .. tostring(expected))
        print("  Actual: " .. tostring(actual))
        return false
    end
    return true
end

local function assertTrue(value, message)
    if not value then
        print("[FAIL] " .. (message or "Expected true"))
        return false
    end
    return true
end

local function assertFalse(value, message)
    if value then
        print("[FAIL] " .. (message or "Expected false"))
        return false
    end
    return true
end

local function assertNotNil(value, message)
    if value == nil then
        print("[FAIL] " .. (message or "Expected non-nil value"))
        return false
    end
    return true
end

local function assertNil(value, message)
    if value ~= nil then
        print("[FAIL] " .. (message or "Expected nil"))
        print("  Actual: " .. tostring(value))
        return false
    end
    return true
end

-- 测试计数器
local total_tests = 0
local passed_tests = 0

local function runTest(name, func)
    total_tests = total_tests + 1
    local success, err = pcall(func)
    if success then
        passed_tests = passed_tests + 1
        print("[PASS] " .. name)
    else
        print("[FAIL] " .. name .. ": " .. tostring(err))
    end
end

-- =====================
-- 测试开始
-- =====================

print("\n========================================")
print("URL Utilities Test Suite")
print("========================================\n")

-- =====================
-- URL 编码解码测试
-- =====================

print("--- URL 编码解码测试 ---\n")

runTest("url_encode: 基本编码", function()
    assertEquals(UrlUtils.url_encode("hello world"), "hello%20world")
    assertEquals(UrlUtils.url_encode("a+b=c"), "a%2Bb%3Dc")
    assertEquals(UrlUtils.url_encode("测试"), "%E6%B5%8B%E8%AF%95")
end)

runTest("url_encode: 空值处理", function()
    assertNil(UrlUtils.url_encode(nil))
    assertEquals(UrlUtils.url_encode(""), "")
end)

runTest("url_decode: 基本解码", function()
    assertEquals(UrlUtils.url_decode("hello%20world"), "hello world")
    assertEquals(UrlUtils.url_decode("a%2Bb%3Dc"), "a+b=c")
    assertEquals(UrlUtils.url_decode("%E6%B5%8B%E8%AF%95"), "测试")
end)

runTest("url_decode: 空值处理", function()
    assertNil(UrlUtils.url_decode(nil))
    assertEquals(UrlUtils.url_decode(""), "")
end)

runTest("encode_query: 查询编码", function()
    assertEquals(UrlUtils.encode_query("hello world"), "hello+world")
    assertEquals(UrlUtils.encode_query("a&b=c"), "a%26b%3Dc")
end)

runTest("decode_query: 查询解码", function()
    assertEquals(UrlUtils.decode_query("hello+world"), "hello world")
    assertEquals(UrlUtils.decode_query("a%26b%3Dc"), "a&b=c")
end)

runTest("encode_path: 路径编码", function()
    assertEquals(UrlUtils.encode_path("/path/to/file"), "/path/to/file")
    assertEquals(UrlUtils.encode_path("/path with space"), "/path%20with%20space")
end)

-- =====================
-- 查询字符串测试
-- =====================

print("\n--- 查询字符串测试 ---\n")

runTest("parse_query: 基本解析", function()
    local params = UrlUtils.parse_query("name=John&age=30")
    assertEquals(params.name, "John")
    assertEquals(params.age, "30")
end)

runTest("parse_query: URL 编码", function()
    local params = UrlUtils.parse_query("name=John%20Doe&city=New%20York")
    assertEquals(params.name, "John Doe")
    assertEquals(params.city, "New York")
end)

runTest("parse_query: 空值", function()
    local params = UrlUtils.parse_query("name=&age=30")
    assertEquals(params.name, "")
    assertEquals(params.age, "30")
end)

runTest("parse_query: 带 ? 前缀", function()
    local params = UrlUtils.parse_query("?name=John")
    assertEquals(params.name, "John")
end)

runTest("parse_query: 空字符串", function()
    local params = UrlUtils.parse_query("")
    assertEquals(next(params), nil)
end)

runTest("parse_query: nil 处理", function()
    local params = UrlUtils.parse_query(nil)
    assertEquals(next(params), nil)
end)

runTest("build_query: 基本构建", function()
    local query = UrlUtils.build_query({ name = "John", age = "30" })
    assertTrue(query:find("name=John") ~= nil)
    assertTrue(query:find("age=30") ~= nil)
end)

runTest("build_query: URL 编码", function()
    local query = UrlUtils.build_query({ name = "John Doe" })
    assertEquals(query, "name=John+Doe")
end)

runTest("build_query: 带 ? 前缀", function()
    local query = UrlUtils.build_query({ name = "John" }, true)
    assertEquals(query, "?name=John")
end)

runTest("merge_query: 合并参数", function()
    local url = UrlUtils.merge_query("http://example.com/path?a=1", { b = "2", c = "3" })
    assertTrue(url:find("a=1") ~= nil)
    assertTrue(url:find("b=2") ~= nil)
    assertTrue(url:find("c=3") ~= nil)
end)

-- =====================
-- URL 解析测试
-- =====================

print("\n--- URL 解析测试 ---\n")

runTest("parse: 完整 URL", function()
    local parsed = UrlUtils.parse("https://user:pass@example.com:8080/path?query=value#fragment")
    assertEquals(parsed.scheme, "https")
    assertEquals(parsed.userinfo, "user:pass")
    assertEquals(parsed.host, "example.com")
    assertEquals(parsed.port, 8080)
    assertEquals(parsed.path, "/path")
    assertEquals(parsed.query, "query=value")
    assertEquals(parsed.fragment, "fragment")
end)

runTest("parse: 简单 URL", function()
    local parsed = UrlUtils.parse("http://example.com")
    assertEquals(parsed.scheme, "http")
    assertEquals(parsed.host, "example.com")
    assertEquals(parsed.path, "/")
    assertNil(parsed.port)
    assertNil(parsed.query)
    assertNil(parsed.fragment)
end)

runTest("parse: 带路径", function()
    local parsed = UrlUtils.parse("http://example.com/path/to/resource")
    assertEquals(parsed.host, "example.com")
    assertEquals(parsed.path, "/path/to/resource")
end)

runTest("parse: 带端口", function()
    local parsed = UrlUtils.parse("http://example.com:8080")
    assertEquals(parsed.host, "example.com")
    assertEquals(parsed.port, 8080)
end)

runTest("parse: 带 IPv6 地址", function()
    local parsed = UrlUtils.parse("http://[::1]:8080/path")
    assertEquals(parsed.host, "[::1]")
    assertEquals(parsed.port, 8080)
end)

runTest("parse: nil 处理", function()
    assertNil(UrlUtils.parse(nil))
    assertNil(UrlUtils.parse(""))
end)

runTest("build: 完整 URL", function()
    local url = UrlUtils.build({
        scheme = "https",
        host = "example.com",
        port = 443,
        path = "/path",
        query = "a=1",
        fragment = "section",
    })
    assertTrue(url:find("^https://example.com") ~= nil)
    assertTrue(url:find("/path") ~= nil)
    assertTrue(url:find("%?a=1") ~= nil)
    assertTrue(url:find("#section") ~= nil)
end)

runTest("build: 最小 URL", function()
    local url = UrlUtils.build({ host = "example.com" })
    assertTrue(url:find("example.com") ~= nil)
end)

-- =====================
-- URL 验证测试
-- =====================

print("\n--- URL 验证测试 ---\n")

runTest("is_valid: 有效 URL", function()
    assertTrue(UrlUtils.is_valid("http://example.com"))
    assertTrue(UrlUtils.is_valid("https://example.com/path"))
    assertTrue(UrlUtils.is_valid("ftp://ftp.example.com"))
end)

runTest("is_valid: 无效 URL", function()
    assertFalse(UrlUtils.is_valid(nil))
    assertFalse(UrlUtils.is_valid(""))
    assertFalse(UrlUtils.is_valid("not a url"))
end)

runTest("is_http: HTTP URL", function()
    assertTrue(UrlUtils.is_http("http://example.com"))
    assertTrue(UrlUtils.is_http("https://example.com"))
    assertFalse(UrlUtils.is_http("ftp://example.com"))
end)

runTest("is_safe: 安全 URL", function()
    assertTrue(UrlUtils.is_safe("https://example.com"))
    assertFalse(UrlUtils.is_safe("https://user:pass@example.com"))
    assertFalse(UrlUtils.is_safe("ftp://example.com"))
end)

runTest("default_port: 默认端口", function()
    assertEquals(UrlUtils.default_port("http"), 80)
    assertEquals(UrlUtils.default_port("https"), 443)
    assertEquals(UrlUtils.default_port("ftp"), 21)
    assertNil(UrlUtils.default_port("unknown"))
end)

-- =====================
-- URL 规范化测试
-- =====================

print("\n--- URL 规范化测试 ---\n")

runTest("normalize: 大小写规范化", function()
    local url = UrlUtils.normalize("HTTP://EXAMPLE.COM/Path")
    assertTrue(url ~= nil and url:lower():find("http://example.com") ~= nil)
end)

runTest("normalize: 移除默认端口", function()
    local url = UrlUtils.normalize("http://example.com:80/path")
    assertTrue(url ~= nil and url:find(":80") == nil)
end)

runTest("normalize_path: 路径规范化", function()
    assertEquals(UrlUtils.normalize_path("/a/./b/../c/"), "/a/c/")
    assertEquals(UrlUtils.normalize_path("/a/b/../../c"), "/c")
end)

-- =====================
-- URL 操作测试
-- =====================

print("\n--- URL 操作测试 ---\n")

runTest("get_extension: 获取扩展名", function()
    assertEquals(UrlUtils.get_extension("http://example.com/file.txt"), "txt")
    assertEquals(UrlUtils.get_extension("http://example.com/path/image.png"), "png")
    assertNil(UrlUtils.get_extension("http://example.com/path/"))
end)

runTest("get_filename: 获取文件名", function()
    assertEquals(UrlUtils.get_filename("http://example.com/path/file.txt"), "file.txt")
    assertEquals(UrlUtils.get_filename("http://example.com/document.pdf"), "document.pdf")
end)

runTest("get_domain: 获取域名", function()
    assertEquals(UrlUtils.get_domain("http://www.example.com/path"), "www.example.com")
    assertEquals(UrlUtils.get_domain("https://sub.domain.example.com:8080"), "sub.domain.example.com")
end)

runTest("get_tld: 获取顶级域名", function()
    assertEquals(UrlUtils.get_tld("http://www.example.com"), "example.com")
    assertEquals(UrlUtils.get_tld("http://test.co.uk"), "co.uk")
end)

runTest("get_subdomain: 获取子域名", function()
    assertEquals(UrlUtils.get_subdomain("http://www.example.com"), "www")
    assertEquals(UrlUtils.get_subdomain("http://a.b.c.example.com"), "a.b.c")
    assertNil(UrlUtils.get_subdomain("http://example.com"))
end)

runTest("join: 路径拼接", function()
    local url = UrlUtils.join("http://example.com/path", "subdir")
    assertTrue(url ~= nil and url:find("/path/subdir") ~= nil)
end)

runTest("join: 绝对路径", function()
    local url = UrlUtils.join("http://example.com/path", "/newpath")
    assertTrue(url ~= nil and url:find("/newpath") ~= nil)
end)

runTest("resolve: 相对 URL 解析", function()
    local url = UrlUtils.resolve("/path", "http://example.com/base")
    assertEquals(url, "http://example.com/path")
end)

runTest("is_same_origin: 同源判断", function()
    assertTrue(UrlUtils.is_same_origin(
        "http://example.com/a",
        "http://example.com/b"
    ))
    assertFalse(UrlUtils.is_same_origin(
        "http://example.com/a",
        "http://other.com/b"
    ))
end)

-- =====================
-- URL 参数提取测试
-- =====================

print("\n--- URL 参数提取测试 ---\n")

runTest("get_param: 获取参数", function()
    assertEquals(UrlUtils.get_param("http://example.com?name=John&age=30", "name"), "John")
    assertEquals(UrlUtils.get_param("http://example.com?name=John&age=30", "age"), "30")
    assertNil(UrlUtils.get_param("http://example.com?name=John", "missing"))
end)

runTest("set_param: 设置参数", function()
    local url = UrlUtils.set_param("http://example.com?a=1", "b", "2")
    assertTrue(url ~= nil and url:find("b=2") ~= nil)
end)

runTest("remove_param: 删除参数", function()
    local url = UrlUtils.remove_param("http://example.com?a=1&b=2", "a")
    assertTrue(url ~= nil and url:find("a=") == nil)
    assertTrue(url ~= nil and url:find("b=2") ~= nil)
end)

-- =====================
-- 实用工具测试
-- =====================

print("\n--- 实用工具测试 ---\n")

runTest("hash: URL 哈希", function()
    local hash1 = UrlUtils.hash("http://example.com/path")
    local hash2 = UrlUtils.hash("http://example.com/path")
    local hash3 = UrlUtils.hash("http://example.com/other")
    
    assertEquals(hash1, hash2)
    assertTrue(hash1 ~= hash3)
    assertEquals(#hash1, 8)
end)

runTest("builder: URL 构建器", function()
    local url = UrlUtils.builder("https", "example.com")
        :set_port(8080)
        :set_path("/api/users")
        :add_param("page", "1")
        :add_param("limit", "10")
        :set_fragment("results")
        :build()
    
    assertTrue(url ~= nil and url:find("https://example.com:8080") ~= nil)
    assertTrue(url ~= nil and url:find("/api/users") ~= nil)
    assertTrue(url ~= nil and url:find("page=1") ~= nil)
    assertTrue(url ~= nil and url:find("#results") ~= nil)
end)

-- =====================
-- 测试结果统计
-- =====================

print("\n========================================")
print(string.format("测试结果: %d/%d 通过", passed_tests, total_tests))
print("========================================\n")

if passed_tests == total_tests then
    print("✓ 所有测试通过！")
    os.exit(0)
else
    print("✗ 存在失败的测试")
    os.exit(1)
end