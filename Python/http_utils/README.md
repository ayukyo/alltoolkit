# HTTP Utils 🌐

**Python HTTP 工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`http_utils` 是一个全面的 Python HTTP 工具模块，提供 HTTP 客户端、简易服务器、URL 解析、头部处理、Cookie 管理等功能。所有实现均使用 Python 标准库（`urllib`、`http.server` 等），零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **HTTP 客户端** - 完整的请求/响应处理
- **HTTP 服务器** - 支持路由和中间件
- **URL 工具** - 解析、构建、编码、解码
- **头部处理** - 解析和格式化 HTTP 头部
- **Cookie 管理** - 解析、创建、格式化 Cookie
- **JSON 支持** - 自动序列化/反序列化
- **SSL/TLS** - 安全 HTTP 连接
- **文件下载** - 从 URL 下载文件
- **CORS 支持** - 跨域请求处理
- **线程服务器** - 并发处理多个请求
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/http_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

### HTTP 客户端

```python
from mod import HTTPClient, get, post

# 简单 GET 请求
response = get("https://api.example.com/users")
if response.ok:
    data = response.json()
    print(data)

# 使用客户端
client = HTTPClient(
    base_url="https://api.example.com",
    default_headers={"Authorization": "Bearer token123"}
)

# POST JSON 数据
response = client.post("/users", json_data={"name": "John", "age": 30})
print(response.json())

# 带查询参数的 GET
response = client.get("/search", params={"q": "python", "page": 1})
```

### HTTP 服务器

```python
from mod import HTTPServer, ServerConfig, RequestInfo

# 创建服务器
server = HTTPServer(ServerConfig(host="localhost", port=8080))

# 注册路由
@server.route("/")
def home(request: RequestInfo):
    return {"message": "Welcome!"}

@server.route("/hello")
def hello(request: RequestInfo):
    name = request.query.get("name", ["World"])[0]
    return {"message": f"Hello, {name}!"}

@server.route("/api/data", methods=["POST"])
def api_data(request: RequestInfo):
    import json
    data = json.loads(request.body.decode("utf-8"))
    return {"received": data, "status": "ok"}

# 启动服务器
server.start(blocking=True)
```

---

## 📚 API 参考

### HTTPClient 类

完整的 HTTP 客户端，支持所有 HTTP 方法和配置选项。

```python
client = HTTPClient(
    base_url="https://api.example.com",  # 基础 URL
    default_headers={"X-Custom": "value"},  # 默认头部
    timeout=30.0,  # 超时时间（秒）
    verify_ssl=True  # 验证 SSL 证书
)

# 请求方法
response = client.get("/path")
response = client.post("/path", json_data={"key": "value"})
response = client.put("/path", data={"field": "value"})
response = client.delete("/path")
response = client.patch("/path")
response = client.head("/path")
response = client.options("/path")

# 通用请求方法
response = client.request("GET", "/path", headers={}, params={})
```

### HTTPResponse 类

HTTP 响应对象，提供便捷的访问方法。

```python
response = get("https://api.example.com/data")

# 状态检查
print(response.ok)           # 是否成功 (2xx)
print(response.is_redirect)  # 是否重定向 (3xx)
print(response.is_error)     # 是否错误 (4xx/5xx)

# 获取内容
print(response.status_code)  # 状态码
print(response.text())       # 文本内容
print(response.json())       # JSON 解析
print(response.headers)      # 响应头部

# 元数据
print(response.url)          # 最终 URL
print(response.elapsed_time) # 请求耗时
```

### URL 工具函数

```python
from mod import (
    parse_url, build_url, url_encode, url_decode,
    is_valid_url, get_domain, normalize_url,
    encode_query_params, decode_query_params
)

# 解析 URL
parsed = parse_url("https://user:pass@example.com:8080/path?q=1#section")
# {'scheme': 'https', 'hostname': 'example.com', 'port': 8080, ...}

# 构建 URL
url = build_url("https", "api.example.com", "/v1/users", 
                port=443, params={"id": 123})
# https://api.example.com:443/v1/users?id=123

# URL 编码/解码
encoded = url_encode("Hello World! 你好")
# Hello%20World%21%20%E4%BD%A0%E5%A5%BD

decoded = url_decode(encoded)
# Hello World! 你好

# 验证 URL
is_valid_url("https://example.com")  # True
is_valid_url("not-a-url")            # False

# 获取域名
get_domain("https://www.example.com/path")  # www.example.com

# 标准化 URL
normalize_url("example.com")  # http://example.com
```

### 头部工具函数

```python
from mod import (
    parse_headers, format_headers, get_content_type,
    create_basic_auth_header, parse_auth_header
)

# 解析头部
headers = parse_headers("Content-Type: application/json\r\nAuthorization: Bearer token")
# {'Content-Type': 'application/json', 'Authorization': 'Bearer token'}

# 格式化头部
header_str = format_headers({"Content-Type": "application/json"})
# Content-Type: application/json

# 获取内容类型
get_content_type("file.json")  # application/json
get_content_type("file.html")  # text/html

# Basic Auth
auth = create_basic_auth_header("username", "password")
# Basic dXNlcm5hbWU6cGFzc3dvcmQ=

# 解析 Auth 头部
auth_type, credentials = parse_auth_header("Bearer token123")
```

### Cookie 工具函数

```python
from mod import parse_cookies, format_cookies, create_cookie

# 解析 Cookie
cookies = parse_cookies("session=abc123; user=john; theme=dark")
# {'session': 'abc123', 'user': 'john', 'theme': 'dark'}

# 格式化 Cookie
cookie_str = format_cookies({"session": "abc123", "user": "john"})
# session=abc123; user=john

# 创建 Cookie
cookie = create_cookie(
    name="session",
    value="xyz789",
    path="/",
    domain="example.com",
    secure=True,
    httponly=True
)
# session=xyz789; Path=/; Domain=example.com; Secure; HttpOnly
```

### 便捷函数

```python
from mod import get, post, put, delete, fetch_json, download_file, check_url_status

# 简单请求
response = get("https://api.example.com/users")
response = post("https://api.example.com/users", json_data={"name": "John"})

# 获取 JSON
data = fetch_json("https://api.example.com/data.json")

# 下载文件
download_file("https://example.com/file.zip", "/path/to/save.zip")

# 检查状态
status = check_url_status("https://example.com")  # 200
```

---

## 🔧 高级用法

### 自定义请求配置

```python
from mod import HTTPClient, HTTPRequest, Method

# 创建详细请求
request = HTTPRequest(
    method=Method.POST.value,
    url="https://api.example.com/upload",
    headers={
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer token"
    },
    body=b"binary data here",
    timeout=60.0,
    follow_redirects=True,
    max_redirects=5,
    verify_ssl=True
)

client = HTTPClient()
response = client.request(request.method, request.url, 
                         headers=request.headers, 
                         data=request.body,
                         timeout=request.timeout)
```

### 服务器中间件模式

```python
from mod import HTTPServer, RequestInfo

server = HTTPServer()

# 认证中间件
def require_auth(handler_func):
    def wrapper(request: RequestInfo):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return {"error": "Unauthorized"}, 401
        return handler_func(request)
    return wrapper

@server.route("/protected")
@require_auth
def protected_resource(request: RequestInfo):
    return {"data": "secret information"}
```

### 文件服务

```python
from mod import HTTPServer, RequestInfo
import os

server = HTTPServer()

@server.route("/static/<path>")
def serve_static(request: RequestInfo):
    # 简单示例，生产环境需要更多安全检查
    file_path = os.path.join("static", request.path.strip("/"))
    if os.path.exists(file_path):
        return server.send_file_response(file_path)
    return {"error": "Not Found"}, 404
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/http_utils
python http_utils_test.py
```

测试覆盖：
- URL 工具函数
- 头部工具函数
- Cookie 工具函数
- HTTP 客户端
- HTTP 服务器
- 集成测试
- 模块信息

---

## 📝 示例

查看 `examples/` 目录获取完整示例：

```bash
# 运行所有示例
python examples/basic_usage.py

# 运行 HTTP 服务器示例
python examples/basic_usage.py server
```

---

## ⚠️ 注意事项

1. **线程安全** - HTTPClient 不是线程安全的，多线程环境下请创建多个实例
2. **SSL 验证** - 生产环境请保持 `verify_ssl=True`
3. **超时设置** - 始终设置合理的超时时间避免阻塞
4. **错误处理** - 检查 `response.ok` 或使用 try/except 处理异常
5. **大文件下载** - 使用 `download_file` 函数而非直接加载到内存

---

## 📄 许可证

MIT License - 详见 AllToolkit 主仓库

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**AllToolkit** - 一套工具，无限可能 🔧
