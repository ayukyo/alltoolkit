# URL Utilities - AllToolkit Python 🌐

**零依赖的 URL 解析、验证和操作工具模块**

---

## 📖 概述

`url_utils` 提供全面的 URL 处理功能，包括：

- ✅ URL 解析和验证
- ✅ URL 规范化
- ✅ 查询参数操作
- ✅ 路径操作
- ✅ URL 比较
- ✅ URL 构建和连接
- ✅ URL 清理和安全检查
- ✅ 简单的 URL 短链模拟

**零依赖** - 仅使用 Python 标准库

---

## 🚀 快速开始

### 安装

```bash
# 复制模块到你的项目
cp -r AllToolkit/Python/url_utils your_project/
```

### 基本使用

```python
from mod import URL, parse_url, validate_url, normalize_url

# 解析 URL
url = parse_url("https://example.com:8080/path?q=test#section")
print(url.scheme)    # "https"
print(url.host)      # "example.com"
print(url.port)      # 8080
print(url.path)      # "/path"
print(url.query)     # {"q": "test"}
print(url.fragment)  # "section"

# 验证 URL
valid, error = validate_url("https://example.com")
print(valid)  # True

# 规范化 URL
normalized = normalize_url("HTTPS://EXAMPLE.COM:443/Path/")
print(normalized)  # "https://example.com/Path"
```

---

## 📚 API 文档

### URL 类

#### 构造函数

```python
url = URL(
    url="",           # 完整 URL 字符串（如果提供，其他参数被忽略）
    scheme="https",   # URL 方案
    host="",          # 主机名或 IP
    port=None,        # 端口号
    path="/",         # 路径
    query=None,       # 查询参数字典
    fragment="",      # 片段
    username="",      # 用户名（认证）
    password=""       # 密码（认证）
)
```

#### 属性

| 属性 | 描述 |
|------|------|
| `scheme` | URL 方案 (http, https, etc.) |
| `host` | 主机名或 IP 地址 |
| `port` | 端口号 |
| `path` | URL 路径 |
| `query` | 查询参数字典 |
| `fragment` | URL 片段 (#...) |
| `username` | 认证用户名 |
| `password` | 认证密码 |

#### 方法

**字符串转换**

```python
url = URL("https://example.com/path")

# 转换为字符串
url.to_string()  # "https://example.com/path"
url.to_string(include_auth=True)  # 包含认证信息

str(url)  # __str__ 支持
repr(url)  # __repr__ 支持
```

**规范化**

```python
url = URL("HTTPS://EXAMPLE.COM:443/a/b/../c/")
normalized = url.normalize()
print(normalized.to_string())  # "https://example.com/a/c"
```

**查询参数操作**

```python
url = URL("https://example.com/search?q=test")

# 获取参数
url.get_param("q")              # "test"
url.get_param("missing", "N/A") # "N/A" (默认值)

# 设置参数（链式调用）
url.set_param("page", "1")
    .set_param("sort", "asc")

# 移除参数
url.remove_param("q")

# 检查参数
url.has_param("q")  # True/False

# 获取所有参数
url.get_params()  # {"q": "test", "page": "1"}
```

**路径操作**

```python
url = URL("https://example.com/a/b/c")

# 获取路径段
url.get_path_segments()  # ["a", "b", "c"]

# 设置路径
url.set_path("/new/path")

# 追加路径段（链式调用）
url.append_path("d").append_path("e")

# 获取父路径
url.get_parent_path()  # "/a/b"

# 获取来源（scheme + host + port）
url.get_origin()  # "https://example.com"

# 获取基础 URL（来源 + 路径）
url.get_base_url()  # "https://example.com/a/b/c"
```

**检查方法**

```python
url = URL("https://example.com/path?q=1#frag")

url.is_secure()     # True (HTTPS)
url.is_absolute()   # True (有 scheme 和 host)
url.has_query()     # True
url.has_fragment()  # True
url.has_auth()      # True/False
```

**比较**

```python
url1 = URL("https://example.com/path1")
url2 = URL("https://example.com/path2")
url3 = URL("http://example.com/path1")

# 检查同源
url1.same_origin(url2)  # True
url1.same_origin(url3)  # False (不同 scheme)

# 检查相等
url1.equals(url2)  # False (不同路径)
url1.equals(url2, ignore_query=True)  # 忽略查询参数比较

# 复制
url_copy = url1.copy()
```

---

### 便捷函数

```python
from mod import (
    parse_url, validate_url, is_valid_url, normalize_url,
    extract_domain, extract_path, extract_query_params,
    build_url, join_url, sanitize_url, get_url_info
)

# 解析 URL
url = parse_url("https://example.com/path")

# 验证 URL
valid, error = validate_url("https://example.com")
is_valid = is_valid_url("https://example.com")  # True

# 规范化 URL
normalized = normalize_url("HTTPS://EXAMPLE.COM:443/")

# 提取组件
domain = extract_domain("https://sub.example.com/path")  # "sub.example.com"
path = extract_path("https://example.com/a/b/c")         # "/a/b/c"
params = extract_query_params("https://example.com?a=1&b=2")  # {"a": "1", "b": "2"}

# 构建 URL
url = build_url(
    scheme="https",
    host="example.com",
    port=8080,
    path="/api/v1",
    query={"key": "value"},
    fragment="section"
)

# 连接 URL
join_url("https://example.com/a/b", "c")      # "https://example.com/a/b/c"
join_url("https://example.com/a/b", "/c")     # "https://example.com/c"

# 清理 URL（安全检查）
safe_url = sanitize_url("https://example.com/path")
# 会拒绝 javascript:, data: 等危险 scheme

# 获取完整 URL 信息
info = get_url_info("https://example.com:8080/path?q=1")
# 返回包含 scheme, host, port, path, query, fragment, origin, is_secure 等的字典
```

---

### URLShortener 类

简单的内存 URL 短链器（演示用途）：

```python
from mod import URLShortener

shortener = URLShortener()

# 缩短 URL
original = "https://example.com/very/long/path"
short = shortener.shorten(original)
print(short)  # "https://short.url/1"

# 展开短 URL
expanded = shortener.expand(short)
print(expanded)  # "https://example.com/very/long/path"

# 同一 URL 返回相同短链
short2 = shortener.shorten(original)
print(short == short2)  # True
```

---

## 📝 使用示例

### 示例 1: URL 验证和清理

```python
from mod import validate_url, sanitize_url, URLValidationError

def process_user_url(user_input: str) -> str:
    """验证并清理用户提供的 URL"""
    # 验证
    valid, error = validate_url(user_input)
    if not valid:
        raise ValueError(f"Invalid URL: {error}")
    
    # 清理（只允许 http/https）
    try:
        return sanitize_url(user_input)
    except URLValidationError as e:
        raise ValueError(f"Unsafe URL: {e}")

# 使用
url = process_user_url("https://example.com/page")
print(url)
```

### 示例 2: 构建 API 请求 URL

```python
from mod import URL

def build_api_url(base: str, endpoint: str, params: dict) -> str:
    """构建 API 请求 URL"""
    url = URL(base)
    url.append_path(endpoint)
    
    for key, value in params.items():
        url.set_param(key, value)
    
    return url.to_string()

# 使用
api_url = build_api_url(
    "https://api.example.com",
    "v1/users",
    {"page": "1", "limit": "20", "sort": "created_at"}
)
print(api_url)
# https://api.example.com/v1/users?page=1&limit=20&sort=created_at
```

### 示例 3: URL 规范化用于比较

```python
from mod import URL

def are_urls_equivalent(url1_str: str, url2_str: str) -> bool:
    """检查两个 URL 是否指向同一资源"""
    url1 = URL(url1_str).normalize()
    url2 = URL(url2_str).normalize()
    
    # 比较时忽略片段
    return url1.equals(url2, ignore_fragment=True)

# 使用
print(are_urls_equivalent(
    "https://Example.COM/Page?b=2&a=1#top",
    "https://example.com/page?a=1&b=2#bottom"
))  # True
```

### 示例 4: 提取和分析 URL

```python
from mod import get_url_info

def analyze_url(url_str: str):
    """分析 URL 并返回报告"""
    info = get_url_info(url_str)
    
    print(f"URL: {info['url']}")
    print(f"Scheme: {info['scheme']}")
    print(f"Domain: {info['host']}")
    print(f"Port: {info['port'] or 'default'}")
    print(f"Path: {info['path']}")
    print(f"Secure: {'✓' if info['is_secure'] else '✗'}")
    print(f"Has Auth: {'✓' if info['has_auth'] else '✗'}")
    print(f"Path Segments: {info['path_segments']}")
    
    return info

# 使用
analyze_url("https://user:pass@api.example.com:8080/v1/data?key=value")
```

---

## 🧪 运行测试

```bash
cd url_utils
python url_utils_test.py
```

### 测试覆盖

- ✅ URL 解析（各种格式）
- ✅ URL 验证（域名、IPv4、IPv6、端口）
- ✅ URL 规范化（大小写、端口、路径、查询参数）
- ✅ 字符串转换
- ✅ 查询参数操作
- ✅ 路径操作
- ✅ URL 比较
- ✅ 属性检查
- ✅ 便捷函数
- ✅ URL 短链器
- ✅ 边界情况和边缘案例
- ✅ 方法链式调用

---

## 🔒 安全注意事项

1. **XSS 防护**: 使用 `sanitize_url()` 过滤危险 scheme（如 `javascript:`）
2. **认证信息**: 默认情况下 `to_string()` 不包含用户名/密码
3. **URL 长度限制**: 默认最大 2048 字符，防止 DoS
4. **重定向验证**: 始终验证重定向 URL 的 scheme 和域名

```python
# 安全实践示例
from mod import sanitize_url, URLValidationError

def safe_redirect(user_url: str, allowed_domains: list) -> str:
    """安全重定向"""
    try:
        # 清理和验证
        url = sanitize_url(user_url, allowed_schemes=['http', 'https'])
        parsed = URL(url)
        
        # 检查域名白名单
        if parsed.host not in allowed_domains:
            raise ValueError("Domain not allowed")
        
        return url
        
    except (URLValidationError, ValueError) as e:
        # 回退到安全默认值
        return "https://example.com/"
```

---

## 🎯 适用场景

- Web 爬虫 URL 处理
- API 客户端 URL 构建
- 重定向验证
- 链接清理和规范化
- URL 去重
- 网站地图生成
- SEO URL 分析
- 网络安全检查

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
