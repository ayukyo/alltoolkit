# Glob Pattern Utils 🌐

Glob 模式匹配工具，支持复杂通配符模式匹配。

## 特性

- ✅ **标准 Glob** - `*` `?` `[abc]`
- ✅ **Brace 扩展** - `{a,b,c}`
- ✅ **字符类** - `[a-z]` `[^abc]`
- ✅ **转义字符** - `\\`
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from glob_pattern_utils import match, glob

# 匹配
pattern = "*.py"
print(match("test.py", pattern))  # True
print(match("test.txt", pattern))  # False

# Brace 扩展
pattern = "file.{py,txt,md}"
print(match("file.py", pattern))  # True
print(match("file.txt", pattern))  # True

# 复杂模式
pattern = "test[0-9]*.{py,js}"
print(match("test1_hello.py", pattern))  # True
```

## API 参考

| 函数 | 说明 |
|------|------|
| `match(text, pattern)` | 匹配单个字符串 |
| `glob(directory, pattern)` | 目录 glob |
| `translate(pattern)` | 模式转正则 |
