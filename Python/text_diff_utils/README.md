# Text Diff Utilities (文本差异比较工具集)

全面的文本差异比较工具集，提供多种差异算法、格式化输出和补丁功能。零外部依赖，纯 Python 实现。

## 功能特性

### 🔍 差异比较

- **diff_lines()** - 按行比较文本
- **diff_words()** - 按单词比较文本
- **diff_chars()** - 按字符比较文本

### 📝 格式化输出

- **unified_diff()** - 统一差异格式（git 风格）
- **context_diff()** - 上下文差异格式
- **html_diff()** - HTML 并排差异显示
- **inline_diff()** - 内联差异格式

### 🧮 相似度计算

- **similarity_ratio()** - 计算文本相似度（0-1）
- **levenshtein_distance()** - Levenshtein 编辑距离
- **normalized_levenshtein()** - 归一化编辑距离
- **lcs()** - 最长公共子序列
- **lcs_length()** - LCS 长度

### 🛠️ 补丁功能

- **create_patch()** - 创建补丁文件
- **apply_patch()** - 应用补丁

### 📊 工具函数

- **find_matching_blocks()** - 查找匹配块
- **get_diff_summary()** - 获取差异摘要统计
- **text_diff_summary()** - 人类可读的差异摘要
- **batch_diff()** - 批量比较文本对
- **find_duplicate_blocks()** - 查找重复块

### 🎯 TextDiffer 类

面向对象的差异比较器，支持配置选项。

## 安装

零外部依赖，纯 Python 实现：

```python
from text_diff_utils.mod import *
```

## 快速开始

### 基础差异比较

```python
from text_diff_utils.mod import diff_lines, get_diff_summary

old_text = """第一行
第二行
第三行"""

new_text = """第一行
修改的第二行
第三行
新增的第四行"""

# 按行比较
result = diff_lines(old_text, new_text)

# 查看统计信息
print(result.stats)
# {'added': 1, 'deleted': 0, 'replaced': 1, 'unchanged': 2, 'total_changes': 2}

# 检查是否有变化
print(result.has_changes())  # True

# 获取所有变更
for op in result.get_changes():
    print(f"{op.type.value}: {op.old_content} -> {op.new_content}")
```

### 生成统一差异格式

```python
from text_diff_utils.mod import unified_diff

old = "line1\nline2\nline3"
new = "line1\nmodified\nline3"

diff = unified_diff(old, new, "old.txt", "new.txt")
print(diff)
```

输出：
```
--- old.txt
+++ new.txt
@@ -1,3 +1,3 @@
 line1
-line2
+modified
 line3
```

### 生成 HTML 差异

```python
from text_diff_utils.mod import html_diff

old = "原始内容\n第二行"
new = "修改内容\n第二行"

html = html_diff(old, new, "原文件", "新文件")

# 保存为 HTML 文件
with open("diff.html", "w") as f:
    f.write(html)
```

### 计算相似度

```python
from text_diff_utils.mod import similarity_ratio, levenshtein_distance, lcs

text1 = "hello world"
text2 = "hello there"

# 相似度（0-1）
print(f"相似度: {similarity_ratio(text1, text2):.2%}")

# 编辑距离
print(f"编辑距离: {levenshtein_distance(text1, text2)}")

# 最长公共子序列
print(f"LCS: '{lcs(text1, text2)}'")
```

### 使用 TextDiffer 类

```python
from text_diff_utils.mod import TextDiffer

# 创建比较器（忽略空白差异）
differ = TextDiffer(ignore_whitespace=True, ignore_case=False)

# 比较文本
result = differ.diff("hello\n  world", "hello\nworld")
print(result.has_changes())  # False（因为忽略了空白）

# 生成统一差异
diff = differ.unified_diff(old_text, new_text)

# 计算相似度
similarity = differ.similarity(old_text, new_text)
```

### 差异摘要

```python
from text_diff_utils.mod import text_diff_summary, get_diff_summary

old = "line1\nline2\nline3"
new = "line1\nmodified\nline3\nline4"

# 人类可读的摘要
print(text_diff_summary(old, new))
# Output: "~1 lines, +1 lines (similarity: 66.7%)

# 详细统计
stats = get_diff_summary(old, new)
print(stats)
# {'old_lines': 3, 'new_lines': 4, 'added_lines': 1, ...}
```

### 单词级差异

```python
from text_diff_utils.mod import diff_words, DiffType

old = "The quick brown fox"
new = "The slow brown dog"

result = diff_words(old, new)

for word, diff_type in result:
    if diff_type == DiffType.INSERT:
        print(f"+{word}")
    elif diff_type == DiffType.DELETE:
        print(f"-{word}")
    else:
        print(f" {word}")
```

### 字符级差异

```python
from text_diff_utils.mod import diff_chars

old = "kitten"
new = "sitting"

result = diff_chars(old, new)

for char, diff_type in result:
    print(f"{diff_type.value}: {char}")
```

## 运行测试

```bash
cd Python/text_diff_utils
python text_diff_utils_test.py
```

## 运行示例

```bash
cd Python/text_diff_utils/examples
python usage_examples.py
```

## 应用场景

1. **版本控制系统** - 比较、合并代码变更
2. **文档对比** - 比较文档版本差异
3. **代码审查工具** - 高亮显示代码变更
4. **文本编辑器** - 实现撤销/重做差异
5. **数据同步** - 检测数据变更
6. **抄袭检测** - 计算文本相似度
7. **翻译工具** - 比较原文和译文

## 特点

- ✅ 零外部依赖
- ✅ 纯 Python 实现
- ✅ 多种差异算法（行、单词、字符）
- ✅ 多种输出格式（统一、上下文、HTML、内联）
- ✅ 相似度计算和编辑距离
- ✅ 补丁生成和应用
- ✅ 完整的测试覆盖
- ✅ 支持大文本和 Unicode

## API 参考

### 差异比较函数

```python
diff_lines(old_text, new_text, ignore_whitespace=False, ignore_case=False) -> DiffResult
diff_words(old_text, new_text, ignore_case=False) -> List[Tuple[str, DiffType]]
diff_chars(old_text, new_text, ignore_whitespace=False, ignore_case=False) -> List[Tuple[str, DiffType]]
```

### 格式化函数

```python
unified_diff(old_text, new_text, fromfile="old", tofile="new", n=3) -> str
context_diff(old_text, new_text, fromfile="old", tofile="new", n=3) -> str
html_diff(old_text, new_text, old_title="Original", new_title="Modified") -> str
inline_diff(old_text, new_text, prefix_add="+ ", prefix_del="- ", prefix_eq="  ") -> str
```

### 相似度函数

```python
similarity_ratio(old_text, new_text) -> float  # 0.0 - 1.0
levenshtein_distance(s1, s2) -> int
normalized_levenshtein(s1, s2) -> float  # 0.0 - 1.0
lcs(s1, s2) -> str
lcs_length(s1, s2) -> int
```

### 补丁函数

```python
create_patch(old_text, new_text, fromfile="old", tofile="new") -> str
apply_patch(original_text, patch_text) -> str
```

## 作者

AllToolkit 自动化开发

## 版本

1.0.0 (2026-04-16)