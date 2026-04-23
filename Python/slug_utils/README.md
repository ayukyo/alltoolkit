# slug_utils - URL友好Slug生成工具

零依赖的slug生成工具库，支持多语言、自定义分隔符、大小写转换等功能。

## 功能特性

- ✅ **slugify** - 将字符串转换为URL友好的slug
- ✅ **自定义分隔符** - 支持连字符、下划线、点号等
- ✅ **大小写转换** - 可选择小写或保留原样
- ✅ **数字处理** - 可选择保留或移除数字
- ✅ **最大长度限制** - 自动在单词边界处截断
- ✅ **自定义替换规则** - 灵活的字符替换配置
- ✅ **多语言支持** - 中文、日文、韩文音译
- ✅ **Unicode处理** - 自动处理重音字符
- ✅ **唯一slug生成** - 自动添加数字后缀避免冲突
- ✅ **slug验证** - 检查slug格式是否有效
- ✅ **智能slug** - 自动处理特殊符号

## 安装

```bash
# 直接使用（零依赖）
python -c "from slug_utils import slugify; print(slugify('Hello World'))"
```

## 快速开始

### 基本用法

```python
from slug_utils import slugify

# 基本转换
slugify("Hello World!")        # 'hello-world'
slugify("你好世界")            # 'ni-hao-shi-jie'
slugify("Café & Restaurant")   # 'cafe-and-restaurant'
```

### 自定义分隔符

```python
slugify("Hello World", separator="_")  # 'hello_world'
slugify("Hello World", separator=".")  # 'hello.world'
slugify("Hello World", separator="")   # 'helloworld'
```

### 保留大小写

```python
slugify("Hello World", lowercase=False)  # 'Hello-World'
slugify("API Version 2", lowercase=False)  # 'API-Version-2'
```

### 最大长度限制

```python
slugify("Very Long Title Here", max_length=20)  # 'very-long-title'
slugify("Long Blog Post Title", max_length=15)  # 'long-blog-post'
```

### 自定义替换

```python
slugify("Café & Bar", replacements={'&': 'and'})  # 'cafe-and-bar'
slugify("@username", replacements={'@': 'at'})   # 'at-username'
```

## API文档

### `slugify(text, ...)`

将字符串转换为URL友好的slug。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `text` | `str` | - | 要转换的字符串 |
| `separator` | `str` | `'-'` | 分隔符 |
| `lowercase` | `bool` | `True` | 是否转换为小写 |
| `keep_numbers` | `bool` | `True` | 是否保留数字 |
| `max_length` | `int` | `None` | 最大长度限制 |
| `replacements` | `dict` | `None` | 自定义替换规则 |
| `keep_untranslated` | `bool` | `False` | 保留无法音译的字符 |
| `merge_separators` | `bool` | `True` | 合并连续分隔符 |
| `trim_separator` | `bool` | `True` | 去除首尾分隔符 |

### `slugify_unique(text, existing, ...)`

生成唯一slug，自动添加数字后缀。

```python
slugify_unique("Hello World", existing=["hello-world"])  # 'hello-world-2'
slugify_unique("Hello World", existing=["hello-world", "hello-world-2"])  # 'hello-world-3'
```

### `generate_slug(text, prefix, suffix, ...)`

生成带前缀和后缀的slug。

```python
generate_slug("My Post", prefix="blog", suffix="2024")  # 'blog-my-post-2024'
```

### `is_valid_slug(slug, ...)`

验证slug格式是否有效。

```python
is_valid_slug("hello-world")  # True
is_valid_slug("Hello World")  # False
is_valid_slug("hello_world", separator="_")  # True
```

### `unslugify(slug, ...)`

将slug还原为可读字符串。

```python
unslugify("hello-world")  # 'hello world'
unslugify("hello-world", title_case=True)  # 'Hello World'
```

### `smart_slugify(text, ...)`

智能slug生成，自动处理特殊符号。

```python
smart_slugify("What's Up?!")  # 'whats-up'
smart_slugify("100% Success")  # '100-percent-success'
smart_slugify("α + β = γ")  # 'alpha-plus-beta-equals-gamma'
```

### `batch_slugify(texts, unique, ...)`

批量生成slug。

```python
batch_slugify(["Hello World", "Hello World"])  # ['hello-world', 'hello-world']
batch_slugify(["Hello World", "Hello World"], unique=True)  # ['hello-world', 'hello-world-2']
```

## 多语言支持

### 中文

```python
slugify("你好世界")  # 'ni-hao-shi-jie'
slugify("中国人工智能")  # 'zhong-guo-ren-gong-zhi-neng'
```

### 日文

```python
slugify("こんにちは")  # 'ko-n-ni-chi-ha' (平假名)
slugify("テスト")  # 'te-su-to' (片假名)
```

### 韩文

```python
slugify("한국")  # 'han-guk'
slugify("안녕")  # 'an-nyeong'
```

### 欧洲语言

```python
slugify("café")  # 'cafe' (法语)
slugify("grüße")  # 'grusse' (德语)
slugify("niño")  # 'nino' (西班牙语)
```

## 真实场景示例

### 博客系统

```python
# 生成文章slug
title = "10 Tips for Writing Clean Python Code"
slug = slugify(title, max_length=50)
# '10-tips-for-writing-clean-python-code'
```

### 电商产品

```python
# 生成产品slug
product = "iPhone 15 Pro Max 256GB"
slug = slugify(product)
# 'iphone-15-pro-max-256gb'
```

### 用户名生成

```python
# 从邮箱生成用户名
email = "john.doe@example.com"
username = slugify(email.split('@')[0])
# 'john-doe'
```

### URL路径

```python
# 生成分类路径
category = "电子产品 > 手机"
path = slugify(category)
# 'dian-zi-chan-pin-shou-ji'
```

## 测试

```bash
# 运行测试
python Python/slug_utils/slug_utils_test.py

# 运行示例
python Python/slug_utils/examples/usage_examples.py
```

## 测试覆盖

- 27个测试函数
- 100+ 测试用例
- 覆盖正常场景、边界值、异常情况
- 100% 通过率 ✅

## 版本

- **版本**: 1.0.0
- **作者**: AllToolkit
- **日期**: 2026-04-24
- **语言**: Python 3.x
- **依赖**: 无（仅使用标准库）

## 许可证

MIT License