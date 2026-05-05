# Regex Builder Utilities 🔨

零依赖正则表达式构建器，通过流畅 API 构建复杂正则表达式，无需掌握正则语法。

## 功能特性

### 📝 字符匹配
- `literal(text)` - 匹配字面文本（自动转义特殊字符）
- `char(char)` - 匹配单个字符
- `char_class(*chars)` - 匹配字符类中的任意字符 `[abc]`
- `char_range(start, end)` - 匹配字符范围 `[a-z]`
- `char_ranges(*ranges)` - 匹配多个字符范围 `[a-zA-Z]`
- `negated_char_class(*chars)` - 匹配不在字符类中的字符 `[^abc]`
- `any_char()` - 匹配任意字符 `.`
- `digit()` / `non_digit()` - 数字 / 非数字 `\d` / `\D`
- `word_char()` / `non_word_char()` - 单词字符 / 非单词字符 `\w` / `\W`
- `whitespace()` / `non_whitespace()` - 空白 / 非空白 `\s` / `\S`

### 🔢 量词
- `optional(pattern)` - 零次或一次 `?`
- `zero_or_more(pattern)` - 零次或多次 `*`
- `one_or_more(pattern)` - 一次或多次 `+`
- `exactly(n, pattern)` - 恰好 n 次 `{n}`
- `min_times(n, pattern)` - 至少 n 次 `{n,}`
- `max_times(n, pattern)` - 最多 n 次 `{0,n}`
- `min_max(min, max, pattern)` - n 到 m 次 `{n,m}`
- `lazy()` - 懒惰量词 `?`
- `any_of(*patterns)` - 多选一 `(?:a|b|c)`

### 🎯 锚点
- `start()` - 字符串开头 `^`
- `end()` - 字符串结尾 `$`
- `word_boundary()` - 单词边界 `\b`
- `non_word_boundary()` - 非单词边界 `\B`
- `start_of_string()` - 字符串绝对开头 `\A`
- `end_of_string()` - 字符串绝对结尾 `\z`

### 📦 分组
- `group(pattern, name=None)` - 捕获组 `(pattern)` 或命名组 `(?P<name>pattern)`
- `non_capturing_group(pattern)` - 非捕获组 `(?:pattern)`
- `backreference(group)` - 反向引用 `\1` 或 `(?P=name)`

### 👀 断言
- `lookahead(pattern)` - 正向前瞻 `(?=pattern)`
- `negative_lookahead(pattern)` - 负向前瞻 `(?!pattern)`
- `lookbehind(pattern)` - 正向后顾 `(?<=pattern)`
- `negative_lookbehind(pattern)` - 负向后顾 `(?<!pattern)`

### 🚩 标志
- `ignore_case()` - 忽略大小写
- `multiline()` - 多行模式
- `dotall()` - 点号匹配换行
- `verbose()` - 详细模式
- `ascii_only()` - ASCII 模式

### ⚡ 快捷模式
- `email()` - 邮箱模式
- `url()` - URL 模式
- `phone_cn()` - 中国手机号
- `ipv4()` - IPv4 地址
- `date_iso()` - ISO 日期
- `time_24h()` - 24小时制时间
- `uuid()` - UUID
- `hex_color()` - 十六进制颜色
- `chinese()` - 中文字符

### 🔧 组合方法
- `then(pattern)` - 添加后续模式
- `maybe(pattern)` - 可选模式（语义化）
- `repeat(count, pattern)` - 重复指定次数
- `wrap(left, right, pattern)` - 包裹模式
- `quote(pattern)` - 引号包裹

### 🧪 测试方法
- `build()` - 构建正则字符串
- `compile()` - 编译为 Pattern 对象
- `test(text)` - 测试是否匹配
- `match(text)` - 匹配返回 Match 对象
- `find_all(text)` - 查找所有匹配
- `replace(text, replacement)` - 替换匹配
- `split(text)` - 分割文本

## 快捷函数

```python
from mod import (
    email_pattern,     # 邮箱正则
    phone_cn_pattern,  # 中国手机号
    url_pattern,       # URL
    ipv4_pattern,      # IPv4 地址
    date_pattern,      # 日期 (iso/cn)
    time_pattern,      # 时间 (24h/12h)
    uuid_pattern,      # UUID
    hex_color_pattern, # 十六进制颜色
    chinese_pattern,   # 中文字符
    username_pattern,  # 用户名
    password_pattern,  # 密码验证
    number_pattern,    # 数字
    between_delimiters, # 分隔符之间的内容
    quoted_string,     # 引号字符串
)
```

## 使用示例

### 基用法

```python
from mod import RegexBuilder

# 构建简单模式
builder = RegexBuilder()
pattern = builder.literal('hello').one_or_more().build()
# 结果: 'hello+'

# 测试匹配
builder = RegexBuilder().literal('hello').one_or_more()
print(builder.test('helloooo'))  # True
print(builder.find_all('hello hellooo hellooooo'))
# ['hello', 'hellooo', 'hellooooo']
```

### 构建邮箱正则

```python
from mod import RegexBuilder

email_pattern = (RegexBuilder()
    .start()
    .one_or_more(RegexBuilder.CHAR_CLASS.WORD)
    .literal('@')
    .one_or_more(RegexBuilder.CHAR_CLASS.WORD)
    .literal('.')
    .min_max(2, 4, RegexBuilder.CHAR_CLASS.WORD)
    .end()
    .build())

print(email_pattern)
# ^\w+@\w+\.{2,4}\w$

print(RegexBuilder().compile(email_pattern).match('test@example.com'))
# 匹配成功
```

### 构建中国手机号正则

```python
from mod import RegexBuilder

phone_pattern = (RegexBuilder()
    .start()
    .literal('1')
    .char_class(*'3456789')
    .exactly(9, RegexBuilder.CHAR_CLASS.DIGIT)
    .end()
    .build())

print(phone_pattern)
# ^1[3456789]\d{9}$
```

### 带命名组的日期匹配

```python
from mod import RegexBuilder

date_pattern = (RegexBuilder()
    .start()
    .group(r'\d{4}', 'year')
    .literal('-')
    .group(r'\d{2}', 'month')
    .literal('-')
    .group(r'\d{2}', 'day')
    .end()
    .build())

match = RegexBuilder().compile(date_pattern).match('2024-05-10')
print(match.group('year'))   # '2024'
print(match.group('month'))  # '05'
print(match.group('day'))    # '10'
```

### 密码验证（大小写+数字+长度）

```python
from mod import RegexBuilder

password_pattern = (RegexBuilder()
    .start()
    .lookahead(RegexBuilder().min_times(1, RegexBuilder().char_range('a', 'z').build()).build())
    .lookahead(RegexBuilder().min_times(1, RegexBuilder().char_range('A', 'Z').build()).build())
    .lookahead(RegexBuilder().min_times(1, RegexBuilder.CHAR_CLASS.DIGIT).build())
    .min_times(8, RegexBuilder.CHAR_CLASS.WORD)
    .end()
    .build())

# 验证密码
pattern = RegexBuilder().compile(password_pattern)
print(bool(pattern.match('Password1')))  # True
print(bool(pattern.match('password')))   # False (缺少大写)
```

### 使用快捷函数

```python
from mod import email_pattern, phone_cn_pattern, date_pattern

# 快速获取常用正则
print(email_pattern())      # \w+@\w+\.{2,4}\w
print(phone_cn_pattern())   # 1[3456789]\d{9}
print(date_pattern('iso'))  # \d{4}-\d{1,2}-\d{1,2}
print(date_pattern('cn'))   # \d{4}年\d{1,2}月\d{1,2}日
```

### 提取分隔符之间的内容

```python
from mod import between_delimiters

# 提取方括号内容
pattern = between_delimiters('[', ']')
match = re.search(pattern, 'text [content] more')
print(match.group(1))  # 'content'

# 提取引号字符串
from mod import quoted_string
pattern = quoted_string()
match = re.search(pattern, 'say "hello world"')
print(match.group(1))  # 'hello world'
```

## 测试

运行测试：

```bash
python regex_builder_utils_test.py
```

或使用 pytest：

```bash
pytest regex_builder_utils_test.py -v
```

## 零依赖

纯 Python 标准库实现，无需安装任何第三方依赖。

## API 参考

### RegexBuilder 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `literal(text)` | text: str | Builder | 匹配字面文本（自动转义） |
| `char(char)` | char: str | Builder | 匹配单字符 |
| `char_class(*chars)` | chars: str | Builder | 字符类 `[abc]` |
| `char_range(start, end)` | start, end: str | Builder | 字符范围 `[a-z]` |
| `any_char()` | - | Builder | 任意字符 `.` |
| `digit()` | - | Builder | 数字 `\d` |
| `word_char()` | - | Builder | 单词字符 `\w` |
| `whitespace()` | - | Builder | 空白 `\s` |
| `optional(pattern)` | pattern: str/Builder | Builder | 零次或一次 `?` |
| `zero_or_more(pattern)` | pattern: str/Builder | Builder | 零次或多次 `*` |
| `one_or_more(pattern)` | pattern: str/Builder | Builder | 一次或多次 `+` |
| `exactly(n, pattern)` | n: int, pattern | Builder | 恰好 n 次 `{n}` |
| `min_max(min, max, pattern)` | min, max: int, pattern | Builder | n 到 m 次 `{n,m}` |
| `start()` | - | Builder | 开头锚点 `^` |
| `end()` | - | Builder | 结尾锚点 `$` |
| `group(pattern, name)` | pattern, name: str | Builder | 捕获组 |
| `lookahead(pattern)` | pattern: str/Builder | Builder | 正向前瞻 |
| `ignore_case()` | - | Builder | 忽略大小写标志 |
| `build()` | - | str | 构建正则字符串 |
| `compile()` | - | Pattern | 编译为 Pattern |
| `test(text)` | text: str | bool | 测试是否匹配 |

## License

MIT License