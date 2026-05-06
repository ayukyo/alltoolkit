# URL Utilities - URL 处理工具库

Lua URL 处理工具函数库，提供完整的 URL 解析、构建、编码、解码功能。

## 特性

- ✅ **零依赖** - 仅使用 Lua 标准库
- ✅ **完整解析** - 支持 scheme、userinfo、host、port、path、query、fragment
- ✅ **IPv6 支持** - 正确处理 IPv6 地址
- ✅ **查询字符串** - 完整的查询参数解析与构建
- ✅ **URL 规范化** - 路径规范化、默认端口移除
- ✅ **URL 操作** - 路径拼接、相对 URL 解析
- ✅ **URL 验证** - 安全性检查、同源判断
- ✅ **URL Builder** - 流式 API 构建 URL

## 安装

将 `url_utils` 目录复制到项目中，使用 `require` 加载：

```lua
local UrlUtils = require("url_utils.mod")
```

## 快速开始

### URL 编码解码

```lua
local UrlUtils = require("url_utils.mod")

-- URL 编码
local encoded = UrlUtils.url_encode("hello world")
-- 输出: "hello%20world"

-- URL 解码
local decoded = UrlUtils.url_decode("hello%20world")
-- 输出: "hello world"

-- 查询字符串编码（空格变为 +）
local query_encoded = UrlUtils.encode_query("name=John Doe")
-- 输出: "name=John+Doe"
```

### 查询字符串处理

```lua
-- 解析查询字符串
local params = UrlUtils.parse_query("name=John&age=30&city=New+York")
print(params.name)  -- "John"
print(params.age)   -- "30"
print(params.city)  -- "New York"

-- 构建查询字符串
local query = UrlUtils.build_query({ name = "John", age = "30" })
-- 输出: "age=30&name=John"（自动排序）

-- 合并查询参数到 URL
local url = UrlUtils.merge_query("http://example.com?a=1", { b = "2", c = "3" })
-- 输出: "http://example.com?a=1&b=2&c=3"
```

### URL 解析

```lua
-- 解析完整 URL
local parsed = UrlUtils.parse("https://user:pass@example.com:8080/path?q=1#section")
print(parsed.scheme)    -- "https"
print(parsed.userinfo)  -- "user:pass"
print(parsed.host)      -- "example.com"
print(parsed.port)      -- 8080
print(parsed.path)      -- "/path"
print(parsed.query)     -- "q=1"
print(parsed.fragment)  -- "section"

-- 构建 URL
local url = UrlUtils.build({
    scheme = "https",
    host = "example.com",
    path = "/api/users",
    query = "page=1",
    fragment = "results"
})
-- 输出: "https://example.com/api/users?page=1#results"
```

### URL 验证

```lua
-- 检查是否有效 URL
print(UrlUtils.is_valid("http://example.com"))  -- true
print(UrlUtils.is_valid("not a url"))           -- false

-- 检查是否 HTTP URL
print(UrlUtils.is_http("https://example.com"))  -- true
print(UrlUtils.is_http("ftp://example.com"))    -- false

-- 检查是否安全 URL（无用户信息）
print(UrlUtils.is_safe("https://example.com"))              -- true
print(UrlUtils.is_safe("https://user:pass@example.com"))    -- false
```

### URL 规范化

```lua
-- 规范化 URL
local url = UrlUtils.normalize("HTTP://EXAMPLE.COM:80/PATH/../file")
-- 输出: "http://example.com/file"

-- 路径规范化
local path = UrlUtils.normalize_path("/a/./b/../c/")
-- 输出: "/a/c/"
```

### URL 组件提取

```lua
-- 获取域名
print(UrlUtils.get_domain("http://www.example.com/path"))
-- 输出: "www.example.com"

-- 获取顶级域名
print(UrlUtils.get_tld("http://sub.example.com"))
-- 输出: "example.com"

-- 获取子域名
print(UrlUtils.get_subdomain("http://www.example.com"))
-- 输出: "www"

-- 获取文件扩展名
print(UrlUtils.get_extension("http://example.com/file.txt"))
-- 输出: "txt"

-- 获取文件名
print(UrlUtils.get_filename("http://example.com/path/document.pdf"))
-- 输出: "document.pdf"
```

### URL 操作

```lua
-- 路径拼接
local url = UrlUtils.join("http://example.com/api", "users/1")
-- 输出: "http://example.com/api/users/1"

-- 相对 URL 解析
local url = UrlUtils.resolve("/path", "http://example.com/base")
-- 输出: "http://example.com/path"

-- 同源判断
print(UrlUtils.is_same_origin("http://example.com/a", "http://example.com/b"))
-- 输出: true
```

### URL 参数操作

```lua
-- 获取参数
local value = UrlUtils.get_param("http://example.com?name=John", "name")
-- 输出: "John"

-- 设置参数
local url = UrlUtils.set_param("http://example.com?a=1", "b", "2")
-- 输出: "http://example.com?a=1&b=2"

-- 删除参数
local url = UrlUtils.remove_param("http://example.com?a=1&b=2", "a")
-- 输出: "http://example.com?b=2"
```

### URL Builder（流式 API）

```lua
local url = UrlUtils.builder("https", "api.example.com")
    :set_port(443)
    :set_path("/v1")
    :add_path("/users")
    :add_param("page", "1")
    :add_param("limit", "10")
    :add_params({ sort = "name", order = "desc" })
    :set_fragment("results")
    :build()
-- 输出: "https://api.example.com/v1/users?limit=10&order=desc&page=1&sort=name#results"
```

## API 参考

### 编码解码

| 函数 | 描述 |
|------|------|
| `url_encode(s)` | URL 百分号编码 |
| `url_decode(s)` | URL 百分号解码 |
| `encode_path(s)` | 路径编码（保留 `/`） |
| `encode_query(s)` | 查询编码（空格变为 `+`） |
| `decode_query(s)` | 查询解码（`+` 变为空格） |

### 查询字符串

| 函数 | 描述 |
|------|------|
| `parse_query(query)` | 解析查询字符串为表 |
| `build_query(params, prefix)` | 将表构建为查询字符串 |
| `merge_query(url, params)` | 合并查询参数到 URL |

### URL 解析

| 函数 | 描述 |
|------|------|
| `parse(url)` | 解析 URL，返回组件表 |
| `build(components)` | 从组件表构建 URL |

### URL 验证

| 函数 | 描述 |
|------|------|
| `is_valid(url)` | 检查是否有效 URL |
| `is_http(url)` | 检查是否 HTTP/HTTPS URL |
| `is_safe(url)` | 检查是否安全 URL |
| `default_port(scheme)` | 获取协议默认端口 |

### URL 规范化

| 函数 | 描述 |
|------|------|
| `normalize(url)` | 规范化 URL |
| `normalize_path(path)` | 规范化路径（处理 `.` 和 `..`） |

### URL 操作

| 函数 | 描述 |
|------|------|
| `get_extension(url)` | 获取文件扩展名 |
| `get_filename(url)` | 获取文件名 |
| `get_domain(url)` | 获取域名 |
| `get_tld(url)` | 获取顶级域名 |
| `get_subdomain(url)` | 获取子域名 |
| `join(base, path)` | 拼接 URL 路径 |
| `resolve(url, base)` | 解析相对 URL |
| `is_same_origin(url1, url2)` | 判断是否同源 |

### URL 参数操作

| 函数 | 描述 |
|------|------|
| `get_param(url, key)` | 获取指定参数 |
| `set_param(url, key, value)` | 设置参数 |
| `remove_param(url, key)` | 删除参数 |

### 实用工具

| 函数 | 描述 |
|------|------|
| `hash(url)` | 计算 URL 哈希值 |
| `builder(scheme, host)` | 创建 URL Builder |

## 运行测试

```bash
lua url_utils_test.lua
```

## 版本历史

### v1.0.0 (2026-05-06)
- 初始版本
- 完整的 URL 解析与构建功能
- 查询字符串处理
- URL 编码解码
- URL 规范化
- URL Builder 流式 API

## 许可证

MIT License

## 作者

AllToolkit