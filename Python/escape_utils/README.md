# Escape Utils - 转义工具模块

全面的字符串转义和反转义工具集，支持多种格式，零外部依赖。

## 支持的格式

| 格式 | 转义 | 反转义 | 说明 |
|------|------|--------|------|
| HTML | ✅ | ✅ | 支持 5 种基本实体 + 扩展实体 + 数字实体 |
| XML | ✅ | ✅ | 支持属性值特殊处理 |
| URL | ✅ | ✅ | RFC 3986 标准，支持查询字符串 |
| JSON | ✅ | ✅ | JSON 字符串转义，支持 ensure_ascii |
| Shell | ✅ | ❌ | POSIX/Bash/Windows 风格 |
| Regex | ✅ | ❌ | 正则表达式元字符转义 |
| Glob | ✅ | ❌ | Glob 模式特殊字符转义 |
| C | ✅ | ✅ | C 语言字符串转义 |
| SQL | ✅ | ❌ | 标准/MySQL/PostgreSQL 风格 |

## 快速开始

```python
from escape_utils import mod as escape_utils

# HTML 转义
escaped = escape_utils.escape_html('<script>alert("XSS")</script>')
# '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;'

# URL 编码
encoded = escape_utils.escape_url('你好世界')
# '%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C'

# 查询字符串
params = {'name': '张三', 'age': '25'}
query = escape_utils.escape_url_query(params)
# 'name=%E5%BC%A0%E4%B8%89&age=25'

# JSON 转义
escaped = escape_utils.escape_json_string('Hello\nWorld')
# 'Hello\\nWorld'

# Shell 转义
safe = escape_utils.escape_shell('hello world $HOME')
# "'hello world $HOME'"

# 正则表达式转义
pattern = escape_utils.escape_regex('a.b*c')
# 'a\\.b\\*c'

# 综合转义
escaped = escape_utils.escape('<test>', 'html')
```

## API 文档

### HTML 转义

```python
# 转义
escape_html(text: str, extended: bool = False) -> str

# 反转义
unescape_html(text: str, extended: bool = True) -> str
```

- 支持基本实体: `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&apos;`
- 支持扩展实体: `&nbsp;`, `&copy;`, `&euro;` 等 80+ 种
- 支持数字实体: `&#65;` (十进制), `&#x41;` (十六进制)

### URL 编码

```python
# 编码
escape_url(text: str, encoding: str = 'utf-8', 
           safe: str = '', plus_space: bool = True) -> str

# 解码
unescape_url(text: str, encoding: str = 'utf-8', 
             plus_space: bool = True) -> str

# 查询字符串编码
escape_url_query(params: dict, encoding: str = 'utf-8') -> str

# 查询字符串解码
unescape_url_query(query: str, encoding: str = 'utf-8') -> dict
```

### JSON 转义

```python
# 转义
escape_json_string(text: str, ensure_ascii: bool = True) -> str

# 反转义
unescape_json_string(text: str) -> str
```

### Shell 转义

```python
# 单个字符串
escape_shell(text: str, style: str = 'posix') -> str

# 参数列表
escape_shell_args(args: list, style: str = 'posix') -> str
```

- `posix`: POSIX/Bash 风格
- `windows`: Windows CMD 风格

### 正则表达式转义

```python
escape_regex(text: str) -> str
```

### Glob 转义

```python
escape_glob(text: str) -> str
```

### C 语言转义

```python
escape_c_string(text: str) -> str
unescape_c_string(text: str) -> str
```

### SQL 转义

```python
escape_sql_string(text: str, style: str = 'standard') -> str
```

⚠️ **注意**: 生产环境应使用数据库驱动的参数化查询，此函数仅供简单场景。

### 综合函数

```python
# 综合转义
escape(text: str, format: str, **kwargs) -> str

# 综合反转义
unescape(text: str, format: str, **kwargs) -> str

# 批量转义
batch_escape(texts: list, format: str, **kwargs) -> list

# 批量反转义
batch_unescape(texts: list, format: str, **kwargs) -> list
```

### 检测函数

```python
# 检测是否需要转义
needs_escape(text: str, format: str) -> bool

# 检测字符串中的转义格式
detect_escapes(text: str) -> list[str]
```

### 辅助函数

```python
# HTML/XML 属性转义
escape_for_attribute(text: str, attr_type: str = 'html') -> str

# CSS 转义
escape_for_css(text: str) -> str

# JavaScript 转义
escape_for_javascript(text: str) -> str
```

## 使用场景

1. **Web 开发**: 安全处理用户输入，生成安全的 HTML/XML 内容
2. **URL 构建**: 编码查询参数，处理特殊字符
3. **命令行**: 创建安全的 shell 命令
4. **正则匹配**: 转义用户输入用于正则搜索
5. **文件匹配**: 转义文件名用于 glob 匹配
6. **数据传输**: JSON/C 字符串转义
7. **数据库**: SQL 字符串处理（简单场景）

## 安全考虑

- **HTML/XSS**: 使用 `escape_html()` 防止 XSS 攻击
- **SQL 注入**: 推荐使用参数化查询，此模块仅供简单场景
- **Shell 命令**: 使用 `escape_shell()` 防止命令注入

## 特点

- ✅ 零外部依赖
- ✅ 纯 Python 实现
- ✅ 支持多种格式
- ✅ 自动检测转义格式
- ✅ 批量处理支持
- ✅ Unicode 支持
- ✅ 完整测试覆盖

## 许可证

MIT License