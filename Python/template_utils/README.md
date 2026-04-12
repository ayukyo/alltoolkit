# AllToolkit - Python Template Utils 🎯

**零依赖模板引擎 - 功能完整的生产就绪工具**

---

## 📖 概述

`template_utils` 提供功能强大的字符串模板引擎，支持变量替换、条件判断、循环、模板继承和包含。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **变量替换** - 支持 `{{ variable }}` 语法
- **过滤器** - 内置 20+ 过滤器，支持自定义
- **条件块** - if/elif/else/endif
- **循环块** - for/endfor，支持解包和字典遍历
- **模板继承** - extends/block/endblock
- **模板包含** - include 标签
- **自动转义** - 可选的 HTML 自动转义
- **点号访问** - 支持 `{{ user.name }}` 嵌套访问
- **循环变量** - loop.index, loop.first, loop.last 等
- **全局变量** - 设置所有模板可用的全局上下文

---

## 🚀 快速开始

### 基础使用

```python
from mod import render

# 简单变量替换
template = "Hello, {{ name }}!"
result = render(template, {"name": "World"})
print(result)  # Hello, World!

# 多个变量
template = "{{ greeting }}, {{ name }}! You are {{ age }} years old."
result = render(template, {
    "greeting": "Hello",
    "name": "Alice",
    "age": 30
})
```

### 使用过滤器

```python
from mod import render

# 内置过滤器
template = """
{{ name | upper }}
{{ name | lower }}
{{ name | capitalize }}
{{ name | title }}
{{ text | strip }}
{{ items | length }}
{{ items | first }}
{{ items | last }}
{{ text | escape }}
{{ text | truncate }}
""".strip()

# 链式过滤器
template = "{{ name | lower | capitalize }}"
result = render(template, {"name": "HELLO"})  # Hello

# 带参数的过滤器
template = "{{ name | default:'Unknown' }}"
result = render(template, {})  # Unknown
```

---

## 📚 API 参考

### TemplateEngine 类

| 方法 | 描述 | 返回 |
|------|------|------|
| `render(template, context)` | 渲染模板字符串 | `str` |
| `render_file(name, context)` | 加载并渲染模板文件 | `str` |
| `register_filter(name, func)` | 注册自定义过滤器 | `None` |
| `set_globals(**kwargs)` | 设置全局变量 | `None` |
| `set_loader(func)` | 设置模板加载器 | `None` |

### TemplateConfig 类

| 属性 | 描述 | 默认值 |
|------|------|--------|
| `var_start` | 变量开始标记 | `{{` |
| `var_end` | 变量结束标记 | `}}` |
| `block_start` | 块开始标记 | `{%` |
| `block_end` | 块结束标记 | `%}` |
| `max_render_depth` | 最大渲染深度 | `50` |
| `max_loop_iterations` | 最大循环次数 | `1000` |

### 模块级函数

| 函数 | 描述 |
|------|------|
| `render(template, context)` | 使用默认引擎渲染 |
| `render_file(name, context)` | 渲染模板文件 |
| `register_filter(name, func)` | 注册过滤器 |
| `set_globals(**kwargs)` | 设置全局变量 |
| `set_loader(func)` | 设置加载器 |
| `set_autoescape(enabled)` | 启用/禁用自动转义 |

---

## 🎯 使用场景

### 1. 电子邮件模板

```python
from mod import render

email_template = """
Subject: Welcome {{ user.name | upper }}!

Dear {{ user.name }},

{% if user.premium %}
感谢您成为 Premium 会员！
{% else %}
感谢您的注册！
{% endif %}

账户详情：
{% for field, value in user.fields %}
- {{ field | capitalize }}: {{ value }}
{% endfor %}

此致，
{{ company }} 团队
""".strip()

context = {
    "user": {
        "name": "alice",
        "premium": True,
        "fields": [("email", "alice@example.com"), ("joined", "2024-01-01")]
    },
    "company": "Acme"
}

result = render(email_template, context)
```

### 2. HTML 页面生成

```python
from mod import render

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default{% endblock %}</title>
</head>
<body>
    <nav>
        {% for item in nav_items %}
        <a href="{{ item.url }}">{{ item.name }}</a>
        {% endfor %}
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
""".strip()

context = {
    "nav_items": [
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "/about"},
        {"name": "Contact", "url": "/contact"}
    ]
}
```

### 3. 配置文件生成

```python
from mod import render

config_template = """
# 自动生成的配置
app_name = {{ app_name }}
version = {{ version }}

{% if debug %}
debug_mode = true
log_level = DEBUG
{% else %}
debug_mode = false
log_level = INFO
{% endif %}

{% for port in ports %}
listen_{{ loop.index }} = {{ port }}
{% endfor %}
""".strip()

context = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "debug": False,
    "ports": [8080, 8443]
}
```

### 4. 代码生成

```python
from mod import render

class_template = """
class {{ class_name }}:
    \"\"\"{{ docstring }}\"\"\"
    
    def __init__(self{% for param in params %}, {{ param.name }}{% endfor %}):
{% for param in params %}
        self.{{ param.name }} = {{ param.name }}
{% endfor %}
    
{% for method in methods %}
    def {{ method.name }}(self{% for p in method.params %}, {{ p }}{% endfor %}):
        \"\"\"{{ method.doc }}\"\"\"
        pass

{% endfor %}
""".strip()

context = {
    "class_name": "UserService",
    "docstring": "用户服务类",
    "params": [{"name": "db"}, {"name": "cache"}],
    "methods": [
        {"name": "get_user", "params": ["user_id"], "doc": "获取用户"},
        {"name": "create_user", "params": ["data"], "doc": "创建用户"}
    ]
}
```

### 5. 报告生成

```python
from mod import render

report_template = """
# {{ report.title }}

生成时间：{{ report.date }}

## 摘要

{% if report.summary %}
{{ report.summary }}
{% else %}
暂无摘要
{% endif %}

## 数据

| {% for header in report.headers %}{{ header }} |{% endfor %}
{% for row in report.rows %}
| {% for cell in row %}{{ cell }} |{% endfor %}
{% endfor %}

## 详情

{% for item in report.items %}
### {{ item.title }}
{{ item.description }}

{% endfor %}
""".strip()
```

### 6. 自定义过滤器

```python
from mod import TemplateEngine, register_filter

# 注册自定义过滤器
def currency(value):
    """格式化货币"""
    return f"¥{float(value):,.2f}"

def date_format(value, fmt="%Y-%m-%d"):
    """格式化日期"""
    from datetime import datetime
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime(fmt)

register_filter("currency", currency)
register_filter("date", date_format)

template = "价格：{{ price | currency }}, 日期：{{ date | date:'%Y年%m月%d日' }}"
result = render(template, {"price": 1234.5, "date": "2024-01-15"})
# 价格：¥1,234.50, 日期：2024 年 01 月 15 日
```

### 7. 模板继承

```python
from mod import TemplateEngine

engine = TemplateEngine()

# 设置模板加载器
templates = {
    "base.html": """
<html>
<head>{% block title %}默认标题{% endblock %}</head>
<body>
    <header>{% block header %}默认头部{% endblock %}</header>
    <main>{% block content %}默认内容{% endblock %}</main>
    <footer>{% block footer %}默认底部{% endblock %}</footer>
</body>
</html>
""",
    "home.html": """
{% extends "base.html" %}
{% block title %}首页{% endblock %}
{% block header %}
    <nav>首页导航</nav>
{% endblock %}
{% block content %}
    <h1>欢迎来到首页</h1>
{% endblock %}
"""
}

engine.set_loader(lambda name: templates.get(name, ""))
result = engine.render_file("home.html", {})
```

### 8. 模板包含

```python
from mod import TemplateEngine

engine = TemplateEngine()

templates = {
    "item.html": "<li>{{ item }}</li>",
    "list.html": """
<ul>
{% for item in items %}
{% include 'item.html' %}
{% endfor %}
</ul>
"""
}

engine.set_loader(lambda name: templates.get(name, ""))
result = engine.render_file("list.html", {"items": ["A", "B", "C"]})
# <ul><li>A</li><li>B</li><li>C</li></ul>
```

---

## 🔧 内置过滤器

### 字符串处理

| 过滤器 | 描述 | 示例 |
|--------|------|------|
| `upper` | 转大写 | `{{ "hello" \| upper }}` → `HELLO` |
| `lower` | 转小写 | `{{ "HELLO" \| lower }}` → `hello` |
| `capitalize` | 首字母大写 | `{{ "hello" \| capitalize }}` → `Hello` |
| `title` | 标题格式 | `{{ "hello world" \| title }}` → `Hello World` |
| `strip` | 去除空白 | `{{ "  hi  " \| strip }}` → `hi` |
| `escape` | HTML 转义 | `{{ "<br>" \| escape }}` → `&lt;br&gt;` |
| `escapejs` | JS 转义 | 转义 JavaScript 特殊字符 |

### 数据类型转换

| 过滤器 | 描述 | 示例 |
|--------|------|------|
| `int` | 转整数 | `{{ "42" \| int }}` → `42` |
| `float` | 转浮点 | `{{ "3.14" \| float }}` → `3.14` |
| `str` | 转字符串 | `{{ 42 \| str }}` → `"42"` |
| `bool` | 转布尔 | `{{ "true" \| bool }}` → `True` |
| `list` | 转列表 | `{{ "abc" \| list }}` → `['a','b','c']` |

### 集合操作

| 过滤器 | 描述 | 示例 |
|--------|------|------|
| `length` | 长度 | `{{ [1,2,3] \| length }}` → `3` |
| `first` | 第一个 | `{{ [1,2,3] \| first }}` → `1` |
| `last` | 最后一个 | `{{ [1,2,3] \| last }}` → `3` |
| `reverse` | 反转 | `{{ [1,2,3] \| reverse }}` → `[3,2,1]` |
| `sort` | 排序 | `{{ [3,1,2] \| sort }}` → `[1,2,3]` |
| `join` | 连接 | `{{ ['a','b'] \| join }}` → `ab` |

### 其他

| 过滤器 | 描述 | 示例 |
|--------|------|------|
| `default` | 默认值 | `{{ name \| default:'Unknown' }}` |
| `truncate` | 截断 (50 字符) | `{{ long_text \| truncate }}` |
| `truncatechars` | 截断 (指定字符) | `{{ text \| truncatechars:100 }}` |

---

## 🎮 循环变量

在 for 循环中可以使用 `loop` 对象：

| 属性 | 描述 |
|------|------|
| `loop.index` | 当前迭代次数 (从 1 开始) |
| `loop.index0` | 当前迭代次数 (从 0 开始) |
| `loop.first` | 是否是第一次迭代 |
| `loop.last` | 是否是最后一次迭代 |
| `loop.length` | 总迭代次数 |

```python
template = """
{% for item in items %}
{{ loop.index }}. {{ item }}{% if loop.first %} (第一个){% endif %}{% if loop.last %} (最后一个){% endif %}
{% endfor %}
""".strip()
```

---

## 🔐 条件表达式

### 比较运算符

```python
{% if count > 10 %}很多{% endif %}
{% if count >= 10 %}至少 10 个{% endif %}
{% if count < 10 %}很少{% endif %}
{% if count <= 10 %}最多 10 个{% endif %}
{% if count == 10 %}正好 10 个{% endif %}
{% if count != 10 %}不是 10 个{% endif %}
```

### 逻辑运算符

```python
{% if a and b %}两者都为真{% endif %}
{% if a or b %}至少一个为真{% endif %}
{% if not a %}a 为假{% endif %}
```

### 成员运算符

```python
{% if item in items %}找到了{% endif %}
{% if key not in data %}不存在{% endif %}
```

---

## 🧪 运行测试

```bash
cd template_utils
python template_utils_test.py -v
```

### 测试覆盖

- ✅ 变量替换
- ✅ 过滤器 (所有内置 + 自定义)
- ✅ 条件块 (if/elif/else)
- ✅ 循环块 (for/endfor)
- ✅ 循环变量 (loop.*)
- ✅ 模板继承 (extends/block)
- ✅ 模板包含 (include)
- ✅ 自动转义
- ✅ 嵌套访问 (点号语法)
- ✅ 元组解包
- ✅ 字典遍历
- ✅ 全局变量
- ✅ 边界情况处理
- ✅ 错误处理

---

## ⚠️ 注意事项

1. **性能**: 复杂模板建议缓存渲染结果
2. **安全**: 启用 `autoescape` 防止 XSS 攻击
3. **循环限制**: 默认最大 1000 次迭代，防止无限循环
4. **渲染深度**: 默认最大 50 层嵌套，防止递归过深
5. **None 值**: 渲染为空白字符串，不是 "None"
6. **文件加载**: 需要设置 `loader` 才能使用 `render_file` 和 `include`

---

## 🔧 配置选项

```python
from mod import TemplateEngine, TemplateConfig

config = TemplateConfig(
    var_start="{{",          # 变量开始标记
    var_end="}}",            # 变量结束标记
    block_start="{%",        # 块开始标记
    block_end="%}",          # 块结束标记
    max_render_depth=50,     # 最大渲染深度
    max_loop_iterations=1000, # 最大循环次数
)

engine = TemplateEngine(
    config=config,
    autoescape=True,  # 启用自动转义
)
```

---

## 📁 文件结构

```
template_utils/
├── mod.py                      # 主要实现
├── template_utils_test.py      # 测试套件 (80+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 💡 最佳实践

### 1. 启用自动转义

```python
# 对于 HTML 模板，始终启用自动转义
engine = TemplateEngine(autoescape=True)
```

### 2. 使用模板继承

```python
# base.html - 基础模板
<html>
<head>{% block head %}{% endblock %}</head>
<body>{% block body %}{% endblock %}</body>
</html>

# page.html - 页面模板
{% extends "base.html" %}
{% block head %}<title>My Page</title>{% endblock %}
{% block body %}<h1>Content</h1>{% endblock %}
```

### 3. 提取常用部分

```python
# 将重复内容提取为 include
{% include 'header.html' %}
{% include 'footer.html' %}
```

### 4. 使用过滤器链

```python
# 链式处理
{{ user.name | lower | capitalize | truncate }}
```

### 5. 设置全局变量

```python
# 对于所有模板都需要的变量
set_globals(
    site_name="MySite",
    site_url="https://example.com",
    version="1.0.0"
)
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
