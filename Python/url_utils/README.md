# URL Utilities (URL 工具集)

全面的 URL 处理工具集，提供解析、构建、编码、验证、规范化等功能。零外部依赖（除 idna），纯 Python 实现。

## 功能特性

### 🔍 URL 解析 (URLParser)

- **parse_url()** - 解析 URL 为详细组件
- **is_valid_url()** - 验证 URL 格式有效性
- **is_valid_scheme()** - 验证 scheme 格式
- **get_default_port()** - 获取 scheme 默认端口
- **is_default_port()** - 检查是否为默认端口

### 🔧 URL 构建 (URLBuilder)

- **链式调用构建 URL** - 支持 scheme、host、port、path、query、fragment
- **批量设置查询参数** - query_params() 方法
- **认证信息支持** - user() 方法设置用户名密码
- **从基础 URL 构建** - 支持从现有 URL 开始扩展

### 📝 URL 编码 (URLEncoder)

- **encode_url()** - URL 编码
- **decode_url()** - URL 解码
- **encode_path()** - 路径编码（保留斜杠）
- **encode_query()** - 查询参数值编码
- **encode_component()** - URL 组件编码
- **decode_component()** - URL 组件解码

### 🔢 查询字符串 (QueryStringParser)

- **parse()** - 解析查询字符串为字典
- **parse_to_list()** - 解析为键值对列表（保持顺序）
- **build()** - 构建查询字符串
- **get_param()** - 获取单个参数值
- **get_params()** - 获取参数所有值
- **set_param()** - 设置参数
- **remove_param()** - 移除参数
- **has_param()** - 检查参数是否存在

### ⚖️ URL 规范化 (URLNormalizer)

- **normalize()** - 规范化 URL（scheme 小写、路径清理等）
- **canonical()** - 生成规范 URL（用于比较存储）
- **resolve()** - 解析相对 URL
- **remove_tracking_params()** - 移除追踪参数（utm_*, fbclid 等）

### ✅ URL 验证 (URLValidator)

- **validate()** - 全面验证 URL（返回错误列表）
- **is_safe_url()** - 安全 URL 检查（防 XSS、SSRF）
- **is_same_origin()** - 同源检查

### 🛠️ URL 工具 (URLUtils)

- **extract_domain()** - 提取域名
- **extract_root_domain()** - 提取根域名（二级域名）
- **extract_tld()** - 提取顶级域名
- **extract_path()** - 提取路径
- **extract_filename()** - 提取文件名
- **extract_extension()** - 提取文件扩展名
- **change_scheme()** - 更改 scheme
- **ensure_scheme()** - 确保 URL 有 scheme
- **is_absolute() / is_relative()** - 绝对/相对 URL 检查
- **join()** - 连接 URL
- **get_base_url()** - 获取基础 URL
- **split_url() / unsplit()** - URL 分割/重组
- **get_url_depth()** - 获取路径深度
- **is_subdomain()** - 子域名检查
- **batch_resolve()** - 批量解析相对 URL

## 安装

零外部依赖（仅 idna 用于国际化域名）：

```python
from url_utils.mod import *
```

需要安装 idna（国际化域名支持）：

```bash
pip install idna
```

或使用 Python 内置的 urllib.parse（无 idna 时国际化域名功能受限）。

## 快速开始

### URL 解析

```python
from url_utils.mod import parse_url, validate_url

# 解析 URL
url = "https://user:pass@example.com:8080/path?q=1#frag"
info = parse_url(url)

print(info.scheme)      # 'https'
print(info.hostname)    # 'example.com'
print(info.port)        # 8080
print(info.username)    # 'user'
print(info.password)    # 'pass'
print(info.path)        # '/path'
print(info.query)       # 'q=1'
print(info.fragment)    # 'frag'

# 验证 URL
valid, errors = validate_url(url)
print(valid)  # True
```

### URL 构建

```python
from url_utils.mod import URLBuilder

# 链式调用构建
url = (URLBuilder()
       .scheme("https")
       .host("api.example.com")
       .path("/v1/users")
       .query_param("page", "1")
       .query_param("limit", "10")
       .fragment("results")
       .build())

print(url)  # https://api.example.com/v1/users?page=1&limit=10#results

# 批量设置查询参数
url = (URLBuilder()
       .scheme("https")
       .host("search.example.com")
       .path("/search")
       .query_params({
           "q": "python",
           "page": "1",
           "tags": ["web", "api"]
       })
       .build())

print(url)  # https://search.example.com/search?q=python&page=1&tags=web&tags=api
```

### URL 编码

```python
from url_utils.mod import encode_url, decode_url

# 编码解码
encoded = encode_url("hello world!")
print(encoded)  # hello%20world%21

decoded = decode_url("hello%20world%21")
print(decoded)  # hello world!

# 路径编码（保留斜杠）
from url_utils.mod import URLEncoder
path = URLEncoder.encode_path("/path with spaces/file.txt")
print(path)  # /path%20with%20spaces/file.txt
```

### 查询字符串处理

```python
from url_utils.mod import QueryStringParser, get_query_params

# 解析查询字符串
params = QueryStringParser.parse("q=python&tags=web&tags=api")
print(params)  # {'q': ['python'], 'tags': ['web', 'api']}

# 获取单个参数
q = QueryStringParser.get_param("q=python&page=1", "q")
print(q)  # 'python'

# 修改参数
modified = QueryStringParser.set_param("q=python", "page", "2")
print(modified)  # 'q=python&page=2'

removed = QueryStringParser.remove_param("q=python&page=1", "page")
print(removed)  # 'q=python'

# 从 URL 获取查询参数
params = get_query_params("https://example.com?a=1&b=2")
print(params)  # {'a': ['1'], 'b': ['2']}
```

### URL 规范化

```python
from url_utils.mod import normalize_url, clean_url

# 规范化 URL
url = "HTTPS://EXAMPLE.COM:443/path//to/page?b=2&a=1&utm_source=google"
normalized = normalize_url(url)
print(normalized)  # https://example.com/path/to/page?a=1&b=2

# 移除追踪参数
url = "https://example.com/page?utm_source=google&ref=twitter&id=123"
clean = clean_url(url)
print(clean)  # https://example.com/page?id=123

# 解析相对 URL
from url_utils.mod import URLNormalizer
base = "https://example.com/docs/"
resolved = URLNormalizer.resolve(base, "page.html")
print(resolved)  # https://example.com/docs/page.html
```

### URL 验证

```python
from url_utils.mod import validate_url, is_safe_url

# 验证 URL
valid, errors = validate_url("https://example.com")
print(valid)  # True

valid, errors = validate_url("javascript:alert(1)")
print(valid)  # False
print(errors)  # ['危险的 scheme: javascript']

# 安全 URL 检查（防 XSS、SSRF）
safe = is_safe_url("https://example.com")
print(safe)  # True

safe = is_safe_url("javascript:alert(1)")
print(safe)  # False

safe = is_safe_url("http://192.168.1.1")  # 私有 IP
print(safe)  # False

safe = is_safe_url("http://192.168.1.1", allow_private_ip=True)
print(safe)  # True
```

### URL 工具函数

```python
from url_utils.mod import URLUtils, get_domain, set_query_param, remove_query_param

url = "https://blog.example.com/articles/python.html?ref=home&page=1"

# 提取信息
print(get_domain(url))                    # 'blog.example.com'
print(URLUtils.extract_root_domain(url))  # 'example.com'
print(URLUtils.extract_tld(url))          # 'html' (实际是文件名后缀，域名是 .com)
print(URLUtils.extract_filename(url))     # 'python.html'
print(URLUtils.extract_extension(url))    # 'html'
print(URLUtils.get_url_depth(url))        # 2

# 修改 URL
print(set_query_param(url, "new", "value"))     # 添加参数
print(remove_query_param(url, "ref"))           # 移除参数

# URL 分割重组
parts = URLUtils.split_url(url)
print(parts)  # ('https', 'blog.example.com', '/articles/python.html', 'ref=home&page=1', '')

reconstructed = URLUtils.unsplit(parts)
print(reconstructed == url)  # True
```

## 运行测试

```bash
cd Python/url_utils
python url_utils_test.py
```

## 运行示例

```bash
cd Python/url_utils/examples
python usage_examples.py
```

## 应用场景

1. **Web 应用开发** - URL 解析、构建、验证
2. **API 开发** - 构建 API 请求 URL、解析响应链接
3. **爬虫/抓取** - URL 规范化、相对 URL 解析
4. **安全审计** - URL 安全检查、防 XSS/SSRF
5. **数据分析** - 提取 URL 组件、域名分析
6. **链接管理** - URL 清理、追踪参数移除
7. **SEO 工具** - URL 规范化、同源检查
8. **用户输入处理** - URL 验证、清理、规范化

## 特点

- ✅ 零外部依赖（仅可选的 idna）
- ✅ 纯 Python 实现
- ✅ 完整的解析/构建/编码/验证功能
- ✅ 查询字符串全面支持
- ✅ URL 规范化和清理
- ✅ 安全检查（XSS、SSRF）
- ✅ 完整的测试覆盖
- ✅ 丰富的使用示例
- ✅ 支持国际化域名 (IDN)
- ✅ IPv4/IPv6 支持

## API 参考

### 便捷函数

```python
parse_url(url) -> URLInfo
build_url(base_url="") -> URLBuilder
encode_url(url, safe="") -> str
decode_url(url) -> str
normalize_url(url) -> str
validate_url(url) -> Tuple[bool, List[str]]
is_safe_url(url, allow_private_ip=False) -> bool
clean_url(url) -> str
get_domain(url) -> Optional[str]
get_query_params(url) -> Dict[str, List[str]]
set_query_param(url, key, value) -> str
remove_query_param(url, key) -> str
```

### URLParser 类方法

```python
URLParser.parse(url) -> URLInfo
URLParser.is_valid_url(url) -> bool
URLParser.is_valid_scheme(scheme) -> bool
URLParser.get_default_port(scheme) -> Optional[int]
URLParser.is_default_port(scheme, port) -> bool
```

### URLBuilder 类方法

```python
builder = URLBuilder(base_url="")
builder.scheme(s) -> builder
builder.host(h) -> builder
builder.port(p) -> builder
builder.path(p) -> builder
builder.query_param(k, v) -> builder
builder.query_params(dict) -> builder
builder.fragment(f) -> builder
builder.user(username, password="") -> builder
builder.build() -> str
```

## 作者

AllToolkit 自动化开发

## 版本

1.0.0 (2026-04-20)