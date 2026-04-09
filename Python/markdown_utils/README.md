# AllToolkit - Markdown Utilities 📝

**零依赖 Python Markdown 处理工具库**

---

## 📖 概述

`markdown_utils` 是一个功能全面的 Markdown 处理工具模块，提供 Markdown 与 HTML 互转、内容提取、文档生成、验证和转换等功能。完全使用 Python 标准库实现，无需任何外部依赖。

### 核心功能

- 🔄 **格式转换**: Markdown ↔ HTML 双向转换
- 📤 **内容提取**: 提取标题、链接、代码块、表格
- 📝 **文档生成**: 创建表格、链接、代码块、列表等
- ✅ **验证检查**: 检测 Markdown 语法问题
- 🔄 **内容转换**: 标题级别调整、格式移除、词数统计
- 🛠️ **实用工具**: 文档合并、分割、注释清理

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/markdown_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# Markdown 转 HTML
md = "# Hello\n**Bold** and *italic*"
html = markdown_to_html(md)
print(html)
# 输出：<h1>Hello</h1><p><strong>Bold</strong> and <em>italic</em></p>

# HTML 转 Markdown
html = "<h1>Title</h1><p>Text</p>"
md = html_to_markdown(html)
print(md)
# 输出：# Title\n\nText

# 提取标题
headings = extract_headings("# Title\n## Subtitle")
for h in headings:
    print(f"{h.level}: {h.text}")

# 创建表格
table = create_table(
    ["Name", "Age"],
    [["Alice", "25"], ["Bob", "30"]]
)
print(table)
```

---

## 📚 API 参考

### 格式转换

| 函数 | 描述 | 示例 |
|------|------|------|
| `markdown_to_html(md, extensions)` | Markdown 转 HTML | `markdown_to_html("# Hello")` |
| `html_to_markdown(html)` | HTML 转 Markdown | `html_to_markdown("<h1>Hi</h1>")` |
| `escape_html(text)` | 转义 HTML 实体 | `escape_html("<script>")` |
| `unescape_html(text)` | 还原 HTML 实体 | `unescape_html("&lt;div&gt;")` |

### 内容提取

| 函数 | 描述 | 返回 |
|------|------|------|
| `extract_headings(md)` | 提取所有标题 | `List[HeadingInfo]` |
| `extract_links(md, include_images)` | 提取所有链接 | `List[LinkInfo]` |
| `extract_code_blocks(md)` | 提取所有代码块 | `List[CodeBlockInfo]` |
| `extract_tables(md)` | 提取所有表格 | `List[TableInfo]` |

### 文档生成

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_table(headers, rows, alignments)` | 创建表格 | 见下方示例 |
| `create_link(text, url, title)` | 创建链接 | `create_link("Google", "https://google.com")` |
| `create_image(alt, url, title)` | 创建图片 | `create_image("Logo", "logo.png")` |
| `create_code_block(code, language)` | 创建代码块 | `create_code_block("print(1)", "python")` |
| `create_inline_code(code)` | 创建行内代码 | `create_inline_code("code")` |
| `create_list(items, ordered, start)` | 创建列表 | `create_list(["A", "B"], ordered=True)` |
| `create_blockquote(text)` | 创建引用 | `create_blockquote("Quote")` |
| `create_heading(text, level)` | 创建标题 | `create_heading("Title", 1)` |
| `create_horizontal_rule(style)` | 创建分隔线 | `create_horizontal_rule()` |

### 验证和转换

| 函数 | 描述 | 示例 |
|------|------|------|
| `validate_markdown(md)` | 验证 Markdown | `validate_markdown(md)` |
| `transform_headings(md, offset)` | 调整标题级别 | `transform_headings(md, 1)` |
| `remove_formatting(md, keep)` | 移除格式 | `remove_formatting(md)` |
| `word_count(md)` | 统计词数 | `word_count(md)` |

### 实用工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `join_markdown(*docs, separator)` | 合并文档 | `join_markdown(doc1, doc2)` |
| `split_by_heading(md, max_level)` | 按标题分割 | `split_by_heading(md)` |
| `strip_comments(md)` | 移除注释 | `strip_comments(md)` |

---

## 💡 使用示例

### 示例 1: 生成 API 文档

```python
from mod import *

doc = []

# 标题
doc.append(create_heading("API 参考", 1))
doc.append("")

# 表格
doc.append(create_table(
    ["方法", "端点", "描述"],
    [
        ["GET", "/users", "获取用户列表"],
        ["POST", "/users", "创建用户"],
        ["DELETE", "/users/:id", "删除用户"],
    ]
))
doc.append("")

# 代码示例
doc.append(create_heading("使用示例", 2))
code = """import requests

response = requests.get("https://api.example.com/users")
users = response.json()"""
doc.append(create_code_block(code, "python"))

# 输出完整文档
print("\n".join(doc))
```

### 示例 2: 分析 Markdown 文档

```python
from mod import *

md = """
# 项目文档

## 简介
这是一个示例项目。[了解更多](https://example.com)

## 安装
```bash
pip install myproject
```

| 步骤 | 描述 |
|:---|:---|
| 1 | 克隆仓库 |
| 2 | 安装依赖 |
"""

# 提取所有标题
print("文档结构:")
for h in extract_headings(md):
    print(f"  {'#' * h.level} {h.text}")

# 提取链接
print("\n链接:")
for link in extract_links(md):
    if not link.is_image:
        print(f"  {link.text}: {link.url}")

# 提取代码块
print("\n代码块:")
for block in extract_code_blocks(md):
    if not block.is_inline:
        print(f"  语言：{block.language}")

# 验证文档
is_valid, issues = validate_markdown(md)
print(f"\n验证：{'✓ 有效' if is_valid else '✗ 无效'}")
for issue in issues:
    print(f"  - {issue}")
```

### 示例 3: 文档转换和清理

```python
from mod import *

# 从 HTML 转换
html = """
<h1>标题</h1>
<p>这是<strong>加粗</strong>文本</p>
<ul><li>项目 1</li><li>项目 2</li></ul>
"""

md = html_to_markdown(html)
print("转换后的 Markdown:")
print(md)

# 移除所有格式获取纯文本
plain = remove_formatting(md)
print(f"\n纯文本：{plain}")

# 统计信息
stats = word_count(md)
print(f"\n统计：{stats['word_count']} 词，{stats['line_count']} 行")
```

### 示例 4: 生成 README

```python
from mod import *

readme = []

# 项目标题
readme.append(create_heading("MyProject", 1))
readme.append(create_image("Build", "https://img.shields.io/badge/build-passing-brightgreen"))
readme.append("")

# 简介
readme.append(create_heading("简介", 2))
readme.append("这是一个很酷的项目！")
readme.append("")

# 安装
readme.append(create_heading("安装", 2))
readme.append(create_list([
    "克隆：`git clone https://github.com/user/project.git`",
    "安装：`pip install -r requirements.txt`",
    "运行：`python main.py`",
]))
readme.append("")

# 功能表格
readme.append(create_heading("功能", 2))
readme.append(create_table(
    ["功能", "状态"],
    [["用户认证", "✅ 完成"], ["数据同步", "🚧 进行中"], ["AI 分析", "📋 计划"]]
))
readme.append("")

# 保存
with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(readme))
```

### 示例 5: 变更日志生成

```python
from mod import *

changelog = []

changelog.append(create_heading("变更日志", 1))
changelog.append("")

# 新版本
changelog.append(create_heading("[2.0.0] - 2026-04-09", 2))
changelog.append("")
changelog.append(create_heading("新增", 3))
changelog.append(create_list([
    "添加用户管理模块",
    "支持 OAuth 2.0",
    "新增数据导出",
]))
changelog.append("")
changelog.append(create_heading("修复", 3))
changelog.append(create_list([
    "修复登录问题",
    "修复数据同步 bug",
]))
changelog.append("")
changelog.append(create_horizontal_rule())

print("\n".join(changelog))
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/markdown_utils
python markdown_utils_test.py
```

### 测试覆盖

- ✅ HTML 实体转义和还原
- ✅ Markdown ↔ HTML 双向转换
- ✅ 标题、链接、代码块、表格提取
- ✅ 表格、链接、代码、列表生成
- ✅ Markdown 语法验证
- ✅ 标题级别转换
- ✅ 格式移除和词数统计
- ✅ 文档合并和分割
- ✅ 边界情况和 Unicode 支持

---

## 📊 数据类说明

### HeadingInfo

```python
@dataclass
class HeadingInfo:
    level: int          # 标题级别 1-6
    text: str           # 标题文本
    line_number: int    # 行号
    anchor: str         # URL 锚点
    
    def to_markdown(self) -> str:  # 转回 Markdown
```

### LinkInfo

```python
@dataclass
class LinkInfo:
    text: str           # 链接文本
    url: str            # 链接地址
    title: str          # 标题（可选）
    line_number: int    # 行号
    is_image: bool      # 是否为图片
    
    def to_markdown(self) -> str:
```

### CodeBlockInfo

```python
@dataclass
class CodeBlockInfo:
    language: str       # 编程语言
    code: str           # 代码内容
    line_number: int    # 行号
    is_inline: bool     # 是否为行内代码
    
    def to_markdown(self) -> str:
```

### TableInfo

```python
@dataclass
class TableInfo:
    headers: List[str]      # 表头
    rows: List[List[str]]   # 数据行
    alignments: List[str]   # 对齐方式
    line_number: int        # 行号
    
    def to_markdown(self) -> str:
```

---

## 🔧 扩展建议

### 添加自定义扩展

```python
from mod import markdown_to_html

# 当前支持的扩展
md = "# Title\n\n| A | B |\n|---|---|"
html = markdown_to_html(md, extensions=['tables', 'fenced_code'])
```

### 自定义验证规则

```python
from mod import validate_markdown, extract_headings

def custom_validate(md):
    issues = []
    
    # 检查标题层级
    headings = extract_headings(md)
    if len(headings) > 10:
        issues.append("文档标题过多")
    
    # 检查代码块语言
    blocks = extract_code_blocks(md)
    for block in blocks:
        if not block.language:
            issues.append(f"未指定语言：行 {block.line_number}")
    
    return len(issues) == 0, issues
```

---

## 📝 注意事项

### Markdown 语法支持

**完全支持:**
- 标题 (1-6 级)
- 粗体、斜体、删除线
- 链接和图片
- 代码块（行内和围栏）
- 无序和有序列表
- 引用块
- 表格
- 分隔线

**部分支持:**
- 参考式链接
- 脚注
- 定义列表
- 任务列表

### 性能考虑

- 对于大型文档 (>100KB)，建议分块处理
- 多次操作时，缓存解析结果
- 避免在循环中重复调用 `validate_markdown`

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

---

## 📝 更新日志

### v1.0.0 (2026-04-09)
- ✨ 初始版本
- 🔄 Markdown ↔ HTML 完整转换
- 📤 标题、链接、代码、表格提取
- 📝 完整的文档生成功能
- ✅ Markdown 语法验证
- 🔄 内容转换和清理
- 🛠️ 实用工具函数
- 🧪 完整的测试套件
