# diff_utils - 文本差异比较工具模块

一个功能完整的文本差异比较工具库，零外部依赖，全部使用 Python 标准库实现。

## 功能特性

### 🔍 差异比较
- **行级差异** - 按行比较文本差异
- **字符级差异** - 精确到字符的差异比较
- **词级差异** - 按词语单位比较差异

### 📊 相似度计算
- **Levenshtein 距离/相似度** - 经典编辑距离算法
- **Jaccard 相似度** - 基于 n-gram 的集合相似度
- **余弦相似度** - 基于字符频率的向量相似度
- **Damerau-Levenshtein** - 支持相邻字符交换的编辑距离

### 🎨 格式化输出
- **Unified Diff** - 标准 Git 风格的 diff 格式
- **Context Diff** - 传统上下文 diff 格式
- **彩色终端输出** - ANSI 颜色高亮显示
- **HTML 输出** - 带样式的 HTML 差异展示

### 🔀 合并冲突
- **冲突检测** - 三方合并冲突检测
- **冲突标记** - 生成标准冲突标记格式

### 🩹 补丁操作
- **补丁生成** - 生成可应用的补丁文件
- **补丁应用** - 将补丁应用到原始文本

### 📈 统计分析
- **详细统计** - 行数变化、相似度、变更位置
- **变更摘要** - 人类可读的变更摘要
- **相似字符串查找** - 在候选列表中查找相似字符串

## 快速开始

### 基本使用

```python
from diff_utils.mod import (
    diff_lines, diff_chars, compute_diff_result,
    similarity_score, format_diff_unified, format_diff_colored,
    diff_statistics, get_change_summary
)

# 行级差异比较
old_text = "Hello\nWorld\nPython"
new_text = "Hello\nEveryone\nPython"

diff = diff_lines(old_text, new_text)
for op_type, lines in diff:
    print(f"{op_type.value}: {lines}")

# 获取完整差异结果
result = compute_diff_result(old_text, new_text)
print(f"相似度: {result.similarity:.2%}")
print(f"添加: {result.additions}, 删除: {result.deletions}")

# 计算相似度
sim = similarity_score("hello", "hallo", method="levenshtein")
print(f"相似度: {sim:.2%}")

# 生成 unified diff
unified = format_diff_unified(old_text, new_text, from_file="old.txt", to_file="new.txt")
print(unified)

# 获取变更统计
stats = diff_statistics(old_text, new_text)
print(f"统计: {stats}")

# 获取变更摘要
summary = get_change_summary(old_text, new_text)
print(summary)
```

### 相似度计算

```python
from diff_utils.mod import (
    levenshtein_distance, levenshtein_similarity,
    jaccard_similarity, cosine_similarity,
    damerau_levenshtein_distance, similarity_score
)

text1 = "kitten"
text2 = "sitting"

# Levenshtein 距离
dist = levenshtein_distance(text1, text2)
print(f"距离: {dist}")  # 输出: 3

# Levenshtein 相似度
sim = levenshtein_similarity(text1, text2)
print(f"相似度: {sim:.2%}")  # 输出: 57.14%

# Jaccard 相似度 (bigram)
sim = jaccard_similarity(text1, text2)
print(f"Jaccard 相似度: {sim:.2%}")

# 余弦相似度
sim = cosine_similarity(text1, text2)
print(f"余弦相似度: {sim:.2%}")

# Damerau-Levenshtein (支持字符交换)
dist = damerau_levenshtein_distance("ab", "ba")
print(f"D-L 距离: {dist}")  # 输出: 1 (一次交换)

# 通用相似度计算接口
for method in ["levenshtein", "jaccard", "cosine", "damerau"]:
    sim = similarity_score(text1, text2, method=method)
    print(f"{method}: {sim:.2%}")
```

### 格式化输出

```python
from diff_utils.mod import (
    format_diff_unified, format_diff_context,
    format_diff_colored, format_diff_html, Colors
)

old_text = "line1\nold content\nline3"
new_text = "line1\nnew content\nline3"

# Unified Diff (Git 风格)
unified = format_diff_unified(old_text, new_text, from_file="original.txt", to_file="modified.txt")
print(unified)
# --- original.txt
# +++ modified.txt
# @@ -1,3 +1,3 @@
#  line1
# -old content
# +new content
#  line3

# Context Diff
context = format_diff_context(old_text, new_text)
print(context)

# 彩色终端输出 (行级)
colored = format_diff_colored(old_text, new_text, level="line")
print(colored)

# 彩色终端输出 (字符级)
colored = format_diff_colored("hello world", "hallo world", level="char")
print(colored)

# HTML 输出
html = format_diff_html(old_text, new_text)
with open("diff.html", "w") as f:
    f.write(html)
```

### 合并冲突检测

```python
from diff_utils.mod import detect_merge_conflicts, format_conflict_markers

base = "line1\noriginal\nline3"
ours = "line1\nour change\nline3"
theirs = "line1\ntheir change\nline3"

# 检测冲突
conflicts = detect_merge_conflicts(base, ours, theirs)

for conflict in conflicts:
    print(f"冲突位置: 行 {conflict.start_line} - {conflict.end_line}")
    print(f"我们的内容: {conflict.our_content}")
    print(f"他们的内容: {conflict.their_content}")
    
    # 生成冲突标记
    markers = format_conflict_markers(conflict)
    print(markers)
    # <<<<<<< OURS
    # our change
    # =======
    # their change
    # >>>>>>> THEIRS
```

### 补丁生成与应用

```python
from diff_utils.mod import generate_patch, apply_patch

original = "line1\noriginal content\nline3"
modified = "line1\nmodified content\nline3"

# 生成补丁
patch = generate_patch(original, modified, from_file="file.txt", to_file="file.txt")
print(patch)

# 应用补丁
restored = apply_patch(original, patch)
print(restored)
# line1
# modified content
# line3
```

### 查找相似字符串

```python
from diff_utils.mod import find_similar_strings

target = "hello"
candidates = ["hello", "hallo", "helloo", "world", "help", "helicopter"]

# 查找相似字符串（阈值 0.5）
similar = find_similar_strings(target, candidates, threshold=0.5)
for string, score in similar:
    print(f"{string}: {score:.2%}")

# 输出:
# hello: 100.00%
# hallo: 80.00%
# helloo: 83.33%
# help: 60.00%

# 使用不同的相似度算法
similar_jaccard = find_similar_strings(target, candidates, threshold=0.3, method="jaccard")
similar_cosine = find_similar_strings(target, candidates, threshold=0.3, method="cosine")
```

### 差异高亮

```python
from diff_utils.mod import highlight_differences

text1 = "Hello, World!"
text2 = "Hello, Python!"

# 高亮差异
highlighted1, highlighted2 = highlight_differences(text1, text2)
print(f"原文: {highlighted1}")   # Hello, [[World]]!
print(f"新文: {highlighted2}")   # Hello, [[Python]]!

# 自定义标记
h1, h2 = highlight_differences(text1, text2, marker_start="**", marker_end="**")
print(f"原文: {h1}")   # Hello, **World**!
print(f"新文: {h2}")   # Hello, **Python**!
```

### 最长公共子序列

```python
from diff_utils.mod import find_longest_common_subsequence

s1 = "ABCDEF"
s2 = "XYZABC"

lcs = find_longest_common_subsequence(s1, s2)
print(f"最长公共子序列: {lcs}")  # 输出: ABC
```

## API 参考

### 差异比较函数

| 函数 | 描述 |
|------|------|
| `diff_lines(old, new)` | 行级差异比较 |
| `diff_chars(old, new)` | 字符级差异比较 |
| `diff_words(old, new)` | 词级差异比较 |
| `compute_diff_result(old, new, level)` | 获取完整差异结果 |

### 相似度函数

| 函数 | 描述 |
|------|------|
| `levenshtein_distance(s1, s2)` | Levenshtein 编辑距离 |
| `levenshtein_similarity(s1, s2)` | Levenshtein 相似度 (0-1) |
| `jaccard_similarity(s1, s2, ngram)` | Jaccard 相似度 |
| `cosine_similarity(s1, s2)` | 余弦相似度 |
| `damerau_levenshtein_distance(s1, s2)` | D-L 编辑距离 |
| `similarity_score(s1, s2, method)` | 通用相似度接口 |

### 格式化函数

| 函数 | 描述 |
|------|------|
| `format_diff_unified(old, new, ...)` | Unified diff 格式 |
| `format_diff_context(old, new, ...)` | Context diff 格式 |
| `format_diff_colored(old, new, level)` | 彩色终端输出 |
| `format_diff_html(old, new, level)` | HTML 格式输出 |

### 合并冲突函数

| 函数 | 描述 |
|------|------|
| `detect_merge_conflicts(base, ours, theirs)` | 检测三方合并冲突 |
| `format_conflict_markers(conflict)` | 生成冲突标记文本 |

### 补丁函数

| 函数 | 描述 |
|------|------|
| `generate_patch(old, new, ...)` | 生成补丁文本 |
| `apply_patch(original, patch)` | 应用补丁 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `diff_statistics(old, new)` | 详细差异统计 |
| `get_change_summary(old, new)` | 人类可读的变更摘要 |
| `find_longest_common_subsequence(s1, s2)` | 最长公共子序列 |
| `find_similar_strings(target, candidates, ...)` | 查找相似字符串 |
| `highlight_differences(text1, text2, ...)` | 高亮差异 |

## 数据类型

### DiffType (枚举)

```python
class DiffType(Enum):
    EQUAL = "equal"      # 相同
    INSERT = "insert"    # 插入
    DELETE = "delete"    # 删除
    REPLACE = "replace"  # 替换
```

### DiffOp (数据类)

```python
@dataclass
class DiffOp:
    type: DiffType           # 操作类型
    old_start: int           # 原文起始位置
    old_end: int             # 原文结束位置
    new_start: int           # 新文起始位置
    new_end: int             # 新文结束位置
    old_content: List[str]   # 原文内容
    new_content: List[str]   # 新文内容
```

### DiffResult (数据类)

```python
@dataclass
class DiffResult:
    ops: List[DiffOp]     # 差异操作列表
    similarity: float     # 相似度 (0-1)
    additions: int        # 添加数量
    deletions: int         # 删除数量
    changes: int           # 总变更数
    unchanged: int         # 未变更数量
```

### ConflictRegion (数据类)

```python
@dataclass
class ConflictRegion:
    start_line: int              # 冲突起始行
    end_line: int                # 冲突结束行
    our_content: List[str]       # 我们的内容
    their_content: List[str]      # 他们的内容
    base_content: Optional[List[str]]  # 基础内容
```

## 测试

运行测试：

```bash
# 使用 pytest
python -m pytest diff_utils_test.py -v

# 或直接运行
python diff_utils_test.py
```

## 应用场景

- **版本控制系统** - 比较、合并文件版本
- **代码审查工具** - 展示代码变更
- **文本编辑器** - 实现差异高亮功能
- **文档协作** - 追踪文档修改历史
- **数据同步** - 检测数据变更
- **拼写检查** - 找出相似单词
- **模糊搜索** - 容错搜索功能
- **抄袭检测** - 文本相似度分析

## 特点

- ✅ **零外部依赖** - 仅使用 Python 标准库
- ✅ **完整测试覆盖** - 包含全面的单元测试
- ✅ **多种算法支持** - Levenshtein、Jaccard、Cosine 等
- ✅ **多种输出格式** - Unified、Context、彩色终端、HTML
- ✅ **Unicode 支持** - 完整支持中文等 Unicode 字符
- ✅ **类型提示** - 完整的类型注解

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-04-13)
- 初始版本发布
- 支持行级、字符级、词级差异比较
- 支持多种相似度算法
- 支持 Unified/Context/彩色/HTML 输出格式
- 支持合并冲突检测
- 支持补丁生成与应用
- 支持差异统计和摘要