# width_utils - 字符串显示宽度计算工具

用于计算字符串在终端/等宽字体环境中的显示宽度，零外部依赖。

## 功能特性

- **显示宽度计算** - 考虑 CJK 宽字符、Emoji 等
- **字符宽度检测** - 判断字符是宽字符还是窄字符
- **字符串截断** - 按显示宽度截断，支持省略号
- **字符串填充** - 左填充、右填充、居中对齐
- **多列对齐** - 按显示宽度对齐多列文本
- **ANSI 码处理** - 计算宽度时忽略 ANSI 控制码
- **文本换行** - 按显示宽度换行

## 主要函数

### char_width(char, ambiguous_as_wide, emoji_as_wide)
计算单个字符的显示宽度。

```python
char_width('A')      # 1 (ASCII)
char_width('中')     # 2 (CJK)
char_width('😀')     # 2 (Emoji)
```

### width(text, ambiguous_as_wide, emoji_as_wide)
计算字符串的显示宽度。

```python
width("Hello")       # 5
width("你好")        # 4 (每个汉字宽度为2)
width("Hello世界")   # 9 (5 + 4)
```

### is_wide(char)
判断字符是否为宽字符。

### is_combining(char)
判断字符是否为组合字符。

### is_zero_width(char)
判断字符是否为零宽度字符。

### truncate(text, max_width, ellipsis)
按显示宽度截断字符串。

```python
truncate("Hello World", 10)          # "Hello Worl"
truncate("你好世界再见", 8, '...')   # "你好世..."
```

### pad_left(text, target_width, fill_char)
左填充字符串到指定宽度。

```python
pad_left("测试", 8)      # "    测试"
```

### pad_right(text, target_width, fill_char)
右填充字符串到指定宽度。

### center(text, target_width, fill_char)
居中对齐字符串。

### align_columns(rows, separator)
对齐多列文本。

```python
align_columns([
    ["姓名", "年龄"],
    ["张三", "25"],
    ["李四", "30"],
])
# 输出:
# 姓名  | 年龄
# 张三  | 25
# 李四  | 30
```

### strip_ansi(text)
移除 ANSI 控制码。

### width_with_ansi(text)
计算包含 ANSI 码的文本的显示宽度（忽略 ANSI 码）。

### split_by_width(text, max_width)
按显示宽度分割字符串。

### wrap_text(text, width_limit)
按显示宽度换行文本。

## 使用示例

```python
from width_utils import width, truncate, align_columns

# 计算宽度
print(width("Hello世界"))  # 9

# 截断
print(truncate("这是一段很长的中文文本", 10, '...'))  # "这是一段..."

# 多列对齐
rows = [
    ["项目", "状态", "进度"],
    ["开发", "进行中", "60%"],
    ["测试", "已完成", "100%"],
]
print(align_columns(rows))
# 项目    状态    进度
# 开发    进行中  60%
# 测试    已完成  100%
```

## 测试

运行测试：
```bash
python width_utils/width_utils_test.py
```

测试覆盖率：76 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*