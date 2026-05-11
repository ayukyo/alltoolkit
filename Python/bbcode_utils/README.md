# BBCode Utils - BBCode 解析与转换工具

零依赖的 BBCode（Bulletin Board Code）解析器，支持将 BBCode 转换为 HTML 或纯文本。

## 功能特性

- ✅ 完整的 BBCode 解析器
- ✅ 转换为 HTML
- ✅ 转换为纯文本
- ✅ 生成结构化 AST（抽象语法树）
- ✅ BBCode 语法验证
- ✅ 支持嵌套标签
- ✅ 自定义标签处理器
- ✅ 标签白名单（安全模式）
- ✅ 零外部依赖

## 支持的标签

| 标签 | 说明 | 示例 |
|------|------|------|
| `[b]` | 粗体 | `[b]粗体文字[/b]` |
| `[i]` | 斜体 | `[i]斜体文字[/i]` |
| `[u]` | 下划线 | `[u]下划线文字[/u]` |
| `[s]` | 删除线 | `[s]删除线[/s]` |
| `[url]` | 超链接 | `[url=https://example.com]链接[/url]` |
| `[img]` | 图片 | `[img]https://example.com/img.png[/img]` |
| `[quote]` | 引用 | `[quote]引用内容[/quote]` |
| `[code]` | 代码块 | `[code]print('hello')[/code]` |
| `[size]` | 字体大小 | `[size=24]大字[/size]` |
| `[color]` | 文字颜色 | `[color=red]红色[/color]` |
| `[center]` | 居中 | `[center]居中文字[/center]` |
| `[left]` | 左对齐 | `[left]左对齐[/left]` |
| `[right]` | 右对齐 | `[right]右对齐[/right]` |
| `[list]` | 无序列表 | `[list][*]项目[/list]` |
| `[olist]` | 有序列表 | `[olist][*]项目[/olist]` |
| `[table]` | 表格 | `[table][tr][td]单元格[/td][/tr][/table]` |
| `[spoiler]` | 折叠内容 | `[spoiler]隐藏内容[/spoiler]` |
| `[email]` | 邮件链接 | `[email=a@b.com]发邮件[/email]` |
| `[sub]` | 下标 | `H[sub]2[/sub]O` |
| `[sup]` | 上标 | `E=mc[sup]2[/sup]` |
| `[br]` | 换行 | `行1[br]行2` |
| `[hr]` | 水平线 | `内容[hr]内容` |

## 快速开始

### 基本用法

```python
from bbcode_utils.bbcode_utils import to_html, to_text, parse, validate

# 转换为 HTML
html = to_html("[b]Hello [i]World[/i][/b]")
# 输出: <strong>Hello <em>World</em></strong>

# 转换为纯文本
text = to_text("[b]Bold[/b] and [i]italic[/i]")
# 输出: Bold and italic

# 解析为 AST
ast = parse("[url=https://example.com]Click[/url]")
# ast 是结构化的 BBCodeNode 对象

# 验证 BBCode 语法
valid, errors = validate("[b]Unclosed")
# valid = False, errors = ["Unclosed tag: [b]"]
```

### 使用 BBCodeParser 类

```python
from bbcode_utils.bbcode_utils import BBCodeParser

parser = BBCodeParser()

# 解析 BBCode
ast = parser.parse("[quote]Hello[/quote]")

# 转换为 HTML
html = parser.to_html(ast)

# 转换为纯文本
text = parser.to_text(ast)

# 转换为字典
d = parser.to_dict(ast)
```

### 自定义标签处理器

```python
from bbcode_utils.bbcode_utils import BBCodeParser

parser = BBCodeParser()

def my_spoiler_handler(content, attrs, children):
    return f'<div class="my-spoiler">{content}</div>'

parser.register_handler("spoiler", my_spoiler_handler)

ast = parser.parse("[spoiler]Secret[/spoiler]")
html = parser.to_html(ast)
```

### 安全模式（禁止 URL 和图片）

```python
from bbcode_utils.bbcode_utils import create_safe_parser

# 创建只允许基本格式标签的解析器
parser = create_safe_parser()

# 以下标签会被忽略
html = parser.to_html(parser.parse("[url=https://evil.com]Click[/url]"))
# 输出: Click（URL 标签被移除）
```

### 限制允许的标签

```python
from bbcode_utils.bbcode_utils import BBCodeParser, DEFAULT_TAGS

# 只允许粗体和斜体
allowed = {
    "b": DEFAULT_TAGS["b"],
    "i": DEFAULT_TAGS["i"],
}
parser = BBCodeParser(allowed_tags=allowed)

html = parser.to_html(parser.parse("[b]Bold[/b] [u]Underline[/u]"))
# 输出: <strong>Bold</strong> Underline（u 标签被移除）
```

### 便捷函数

```python
from bbcode_utils.bbcode_utils import bbcode

# 快速转换
html = bbcode("[b]test[/b]", "html")    # HTML 输出
text = bbcode("[b]test[/b]", "text")    # 纯文本
ast = bbcode("[b]test[/b]", "ast")      # JSON 格式的 AST
```

## API 参考

### 主要函数

| 函数 | 说明 |
|------|------|
| `parse(text)` | 解析 BBCode 返回 AST |
| `to_html(text)` | 转换为 HTML |
| `to_text(text)` | 转换为纯文本 |
| `validate(text)` | 验证 BBCode 语法 |
| `get_supported_tags()` | 获取支持的标签列表 |
| `create_safe_parser()` | 创建安全模式解析器 |
| `bbcode(text, format)` | 便捷转换函数 |

### BBCodeParser 类

| 方法 | 说明 |
|------|------|
| `parse(text)` | 解析 BBCode 文本为 AST |
| `to_html(node)` | 将 AST 转换为 HTML |
| `to_text(node)` | 将 AST 转换为纯文本 |
| `to_dict(node)` | 将 AST 转换为字典 |
| `validate(text)` | 验证 BBCode 语法 |
| `register_handler(tag, func)` | 注册自定义标签处理器 |

### BBCodeNode 类

| 属性 | 类型 | 说明 |
|------|------|------|
| `type` | BBCodeNodeType | TEXT 或 TAG |
| `content` | str | 文本节点的内容 |
| `tag_name` | str | 标签名称 |
| `attributes` | dict | 标签属性 |
| `children` | list | 子节点列表 |

## 示例

### 论坛帖子

```python
from bbcode_utils.bbcode_utils import to_html

post = """
[b]公告标题[/b]

[quote=管理员]
这是一个重要的公告内容。
[/quote]

[list]
[*]第一项
[*]第二项
[*]第三项
[/list]

详细信息请访问 [url=https://example.com]官方网站[/url]
"""

html = to_html(post)
print(html)
```

### 代码分享

```python
from bbcode_utils.bbcode_utils import to_html

code_post = """
[b]Python 示例代码[/b]

[code]
def hello(name):
    print(f"Hello, {name}!")

hello("World")
[/code]

运行结果：
[quote]
Hello, World!
[/quote]
"""

html = to_html(code_post)
```

### 表格数据

```python
from bbcode_utils.bbcode_utils import to_html

table = """
[table]
[tr][th]姓名[/th][th]年龄[/th][th]城市[/th][/tr]
[tr][td]张三[/td][td]25[/td][td]北京[/td][/tr]
[tr][td]李四[/td][td]30[/td][td]上海[/td][/tr]
[/table]
"""

html = to_html(table)
```

## 测试

```bash
python bbcode_utils_test.py
```

## 许可证

MIT License

## 作者

AllToolkit 自动化开发助手
日期：2026-05-11