# Slug Utils 📝

**Python URL Slug 生成工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`slug_utils` 是一个全面的 Python URL slug 生成工具模块，提供文本转 URL 友好字符串、多语言支持、批量处理等功能。所有实现均使用 Python 标准库（`re`、`unicodedata` 等），零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **多语言支持** - 中文拼音、日文罗马字、韩文罗马化
- **灵活配置** - 自定义分隔符、长度限制、停用词等
- **重音处理** - 自动转换重音字符为 ASCII
- **批量处理** - 支持批量生成和去重
- **专业函数** - 标题、文件名、用户名、URL 专用 slug 生成
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/slug_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```python
from mod import slugify, slugify_title, slugify_filename

# 基本用法
slug = slugify("Hello World!")
print(slug)  # 输出：hello-world

# 标题 slug（SEO 优化）
title_slug = slugify_title("10 Best Practices for Python in 2024!")
print(title_slug)  # 输出：10-best-practices-for-python-in-2024

# 文件名 slug
file_slug = slugify_filename("My Document (Final Version).pdf")
print(file_slug)  # 输出：my-document-final-version.pdf

# 带重音的文本
french_slug = slugify("Café & Restaurant")
print(french_slug)  # 输出：cafe-and-restaurant
```

---

## 📚 API 参考

### 核心函数

#### `slugify(text, **options)`

将文本转换为 URL 友好的 slug。

```python
slugify("Hello World!")
# 'hello-world'

slugify("Café & Restaurant", separator='_')
# 'cafe_and_restaurant'

slugify("The Quick Brown Fox", remove_stop_words=True)
# 'quick-brown-fox'

slugify("Hello World", max_length=8, truncate_words=True)
# 'hello'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str/bytes | 必填 | 输入文本 |
| `separator` | str | `'-'` | 单词分隔符 |
| `lowercase` | bool | `True` | 转换为小写 |
| `max_length` | int/None | `None` | 最大长度 |
| `allow_unicode` | bool | `False` | 允许 unicode 字符 |
| `remove_stop_words` | bool | `False` | 移除停用词 |
| `stop_words` | set/None | `None` | 自定义停用词集合 |
| `word_replacements` | dict/None | `None` | 自定义单词替换 |
| `allow_dots` | bool | `False` | 允许点号 |
| `allow_underscores` | bool | `False` | 允许下划线 |
| `truncate_words` | bool | `False` | 在单词边界截断 |
| `ensure_ascii` | bool | `True` | 确保 ASCII 输出 |

---

#### `unicode_to_ascii(text)`

将 unicode 文本转换为 ASCII 等效字符。

```python
unicode_to_ascii("Café")
# 'Cafe'

unicode_to_ascii("Ñoño")
# 'Nono'

unicode_to_ascii("北京")
# 'Bei Jing'
```

---

### 多语言支持

#### `slugify_cn(text, **options)`

将中文文本转换为拼音 slug。

```python
slugify_cn("北京")
# 'bei-jing'

slugify_cn("中文测试", separator='_')
# 'zhong_wen_ce_shi'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | 必填 | 中文文本 |
| `separator` | str | `'-'` | 分隔符 |
| `lowercase` | bool | `True` | 转换为小写 |
| `max_length` | int/None | `None` | 最大长度 |
| `pinyin_style` | str | `'toneless'` | 拼音风格 |

---

#### `slugify_jp(text, **options)`

将日文文本转换为罗马字 slug。

```python
slugify_jp("あいう")
# 'a-i-u'

slugify_jp("こんにちは")
# 'ko-n-ni-chi-ha'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | 必填 | 日文文本 |
| `separator` | str | `'-'` | 分隔符 |
| `lowercase` | bool | `True` | 转换为小写 |
| `max_length` | int/None | `None` | 最大长度 |
| `romaji_style` | str | `'hepburn'` | 罗马字风格 |

---

#### `slugify_kr(text, **options)`

将韩文文本转换为罗马化 slug。

```python
slugify_kr("가나다")
# 'ga-na-da'

slugify_kr("안녕하세요")
# 'an-nyeong-ha-se-yo'
```

---

### 专用 Slug 函数

#### `slugify_title(title, **options)`

为博客文章、页面标题生成 SEO 友好的 slug。

```python
slugify_title("10 Best Practices for Python Development in 2024!")
# '10-best-practices-for-python-development-in-2024'

slugify_title("My Title", max_length=60, preserve_case=True)
# 'My-Title'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | str | 必填 | 标题文本 |
| `separator` | str | `'-'` | 分隔符 |
| `max_length` | int | `60` | 最大长度（SEO 推荐） |
| `preserve_case` | bool | `False` | 保留大小写 |

---

#### `slugify_filename(filename, **options)`

生成安全的文件名 slug。

```python
slugify_filename("My Document (Final Version).pdf")
# 'my-document-final-version.pdf'

slugify_filename("archive.tar.gz", preserve_extension=False)
# 'archive-tar-gz'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `filename` | str | 必填 | 原始文件名 |
| `preserve_extension` | bool | `True` | 保留文件扩展名 |
| `separator` | str | `'-'` | 分隔符 |

---

#### `slugify_username(username, **options)`

生成安全的用户名 slug。

```python
slugify_username("John.Doe@2024!")
# 'john_doe_2024'

slugify_username("ab", min_length=3)
# 'ab_'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `username` | str | 必填 | 期望的用户名 |
| `separator` | str | `'_'` | 分隔符（用户名常用下划线） |
| `min_length` | int | `3` | 最小长度 |

---

#### `slugify_url(url, **options)`

从 URL 路径生成 slug。

```python
slugify_url("https://example.com/blog/my-post-title")
# 'my-post-title'

slugify_url("https://example.com/page?id=123#section")
# 'page'

slugify_url("https://example.com/blog/post", keep_domain=True)
# 'example-com-blog-post'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | str | 必填 | 完整 URL 或路径 |
| `keep_domain` | bool | `False` | 包含域名 |
| `separator` | str | `'-'` | 分隔符 |

---

### 批量处理

#### `slugify_batch(texts, **options)`

为多个文本生成 slugs。

```python
slugify_batch(["Hello World", "Hello World", "Foo Bar"])
# ['hello-world', 'hello-world-1', 'foo-bar']

slugify_batch(["A", "B", "C"], ensure_unique=False)
# ['a', 'b', 'c']
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `texts` | list | 必填 | 文本列表 |
| `separator` | str | `'-'` | 分隔符 |
| `lowercase` | bool | `True` | 转换为小写 |
| `ensure_unique` | bool | `True` | 确保唯一性 |

---

#### `slugify_dict(data, **options)`

为字典值生成 slugs。

```python
slugify_dict({"title": "My Post", "content": "Some Content"}, keys=["title"])
# {'title': 'my-post', 'content': 'Some Content'}

slugify_dict({"a": "Hello", "b": "World"})
# {'a': 'hello', 'b': 'world'}
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data` | dict | 必填 | 包含文本值的字典 |
| `keys` | list/None | `None` | 要处理的键列表 |
| `separator` | str | `'-'` | 分隔符 |

---

### 验证和工具函数

#### `is_valid_slug(slug, **options)`

验证字符串是否为有效的 slug。

```python
is_valid_slug("hello-world")
# True

is_valid_slug("Hello_World")
# False

is_valid_slug("hello_world", allow_underscores=True)
# True

is_valid_slug("-invalid-")
# False
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `slug` | str | 必填 | 要验证的字符串 |
| `allow_unicode` | bool | `False` | 允许 unicode |
| `allow_dots` | bool | `False` | 允许点号 |
| `allow_underscores` | bool | `False` | 允许下划线 |
| `min_length` | int | `1` | 最小长度 |
| `max_length` | int/None | `None` | 最大长度 |

---

#### `suggest_slug(text, existing_slugs, **options)`

建议一个不与现有 slugs 冲突的唯一 slug。

```python
suggest_slug("My Post", ["my-post", "my-post-1"])
# 'my-post-2'

suggest_slug("Test", [])
# 'test'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | 必填 | 要 slugify 的文本 |
| `existing_slugs` | list | 必填 | 现有 slugs 列表 |
| `separator` | str | `'-'` | 分隔符 |
| `max_attempts` | int | `10` | 最大尝试次数 |

---

#### `count_words_in_slug(slug, separator='-')`

统计 slug 中的单词数。

```python
count_words_in_slug("hello-world-foo-bar")
# 4

count_words_in_slug("hello_world_foo", separator='_')
# 3
```

---

#### `truncate_slug(slug, max_length, **options)`

截断 slug 到最大长度。

```python
truncate_slug("hello-world-foo-bar", 12)
# 'hello-world'

truncate_slug("hello-world", 7, preserve_words=False)
# 'hello-w'
```

**参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `slug` | str | 必填 | 要截断的 slug |
| `max_length` | int | 必填 | 最大长度 |
| `separator` | str | `'-'` | 分隔符 |
| `preserve_words` | bool | `True` | 在单词边界截断 |

---

## 📝 使用场景

### 博客/文章系统

```python
# 生成文章 URL
def create_post_url(title):
    slug = slugify_title(title, max_length=60)
    return f"/blog/{slug}"

create_post_url("How to Build a REST API with Python")
# '/blog/how-to-build-a-rest-api-with-python'
```

### 文件上传

```python
# 安全文件名
def safe_filename(original_name):
    return slugify_filename(original_name)

safe_filename("My Resume (2024 Final).pdf")
# 'my-resume-2024-final.pdf'
```

### 用户注册

```python
# 用户名规范化
def normalize_username(desired_name, existing_users):
    return suggest_slug(desired_name, existing_users)

normalize_username("John.Doe", ["john_doe", "john_doe-1"])
# 'john_doe-2'
```

### 多语言内容

```python
# 中文内容
slugify_cn("人工智能技术详解")
# 'ren-gong-zhi-neng-ji-shu-xiang-jie'

# 日文内容
slugify_jp("機械学習入門")
# 'ji-xie-xue-xi-ru-men'
```

---

## 🧪 测试

运行测试套件：

```bash
cd AllToolkit/Python/slug_utils
python slug_utils_test.py
```

### 测试覆盖

- ✅ 基本 slug 生成
- ✅ Unicode 和重音处理
- ✅ 最大长度和截断
- ✅ 停用词移除
- ✅ 单词替换
- ✅ 专用函数（标题、文件名、用户名、URL）
- ✅ 多语言支持（中文、日文、韩文）
- ✅ 批量处理
- ✅ 验证函数
- ✅ 边界情况和异常处理

---

## 🔧 自定义

### 自定义停用词

```python
custom_stops = {"custom", "words", "to", "remove"}
slugify("Custom Words To Remove", remove_stop_words=True, stop_words=custom_stops)
# ''
```

### 自定义单词替换

```python
custom_replacements = {"python": "py", "javascript": "js"}
slugify("Python and JavaScript", word_replacements=custom_replacements)
# 'py-and-js'
```

### 自定义分隔符

```python
slugify("Hello World", separator='_')
# 'hello_world'

slugify("Hello World", separator='.')
# 'hello.world'
```

---

## 📊 性能

- 零外部依赖，启动快速
- 使用标准库 `re` 和 `unicodedata`，性能优化
- 批量处理支持，适合大量数据

---

## 🤝 贡献

欢迎贡献代码、测试、文档！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **AllToolkit 主仓库**: https://github.com/ayukyo/alltoolkit
- **Python 模块列表**: https://github.com/ayukyo/alltoolkit/Python
- **问题反馈**: https://github.com/ayukyo/alltoolkit/issues

---

**最后更新**: 2026-04-12
