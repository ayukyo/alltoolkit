# Levenshtein Utils - 编辑距离工具模块

提供 Levenshtein 编辑距离及相关字符串相似度计算功能。零外部依赖，仅使用 Python 标准库。

## 功能概览

| 功能模块 | 描述 |
|---------|------|
| 基础距离 | 经典 Levenshtein 距离计算 |
| 优化算法 | 空间优化、阈值剪枝版距离计算 |
| 相似度 | 比率计算、Jaro、Jaro-Winkler |
| 编辑序列 | 编辑操作回溯、对齐显示 |
| Damerau | 含相邻交换的 Damerau-Levenshtein |
| LCS | 最长公共子序列计算 |
| 模糊匹配 | 相似字符串搜索、模糊查找 |
| 批量操作 | 批量距离、相似度矩阵 |

## 安装使用

```python
from levenshtein_utils.mod import (
    levenshtein_distance,
    similarity_ratio,
    find_similar,
    jaro_winkler_similarity,
    longest_common_subsequence
)

# 计算编辑距离
dist = levenshtein_distance("kitten", "sitting")  # 3

# 计算相似度
sim = similarity_ratio("hello", "hallo")  # 0.8

# 模糊搜索
matches = find_similar("hello", ["hallo", "help", "world"], threshold=0.5)
```

## 详细功能

### 基础 Levenshtein 距离

```python
# 经典算法
dist = levenshtein_distance("kitten", "sitting")  # 3

# 空间优化版（适合长字符串）
dist = levenshtein_distance_optimized("kitten", "sitting")  # 3

# 带阈值（超过阈值提前终止）
dist = levenshtein_distance_threshold("hello", "world", 2)  # 3 (threshold+1)
```

### 相似度计算

```python
# 基础相似度比率
sim = similarity_ratio("hello", "hallo")  # 0.8

# 完整结果对象
result = similarity_result("kitten", "sitting")
result.distance      # 3
result.similarity    # 0.571
result.is_similar(0.5)  # True

# Jaro 相似度（适合姓名匹配）
jaro = jaro_similarity("MARTHA", "MARHTA")  # 0.944

# Jaro-Winkler（公共前缀加权）
jw = jaro_winkler_similarity("MARTHA", "MARHTA")  # 0.961
```

### 编辑操作序列

```python
# 获取编辑步骤
ops = levenshtein_operations("kitten", "sitting")
for op in ops:
    print(op.describe())

# 应用操作
result = apply_operations("kitten", ops)  # "sitting"

# 字符串对齐
a1, a2 = align_strings("kitten", "sitting")
# ('kitten--', 'sitting')
```

### Damerau-Levenshtein

```python
# 含相邻交换操作
dl = damerau_levenshtein_distance("ab", "ba")  # 1
l = levenshtein_distance("ab", "ba")  # 2
```

### 最长公共子序列 (LCS)

```python
# 获取 LCS
lcs = longest_common_subsequence("ABCBDAB", "BDCABA")  # "BCBA"

# 仅获取长度
length = lcs_length("ABCBDAB", "BDCABA")  # 4
```

### 模糊搜索

```python
# 在候选中找相似字符串
matches = find_similar("hello", ["hallo", "helloo", "world"], threshold=0.6)
# [('helloo', 0.889), ('hallo', 0.8)]

# 找最近的字符串
nearest, dist = find_nearest("hello", ["hallo", "world", "help"])
# ('hallo', 1)

# 在文本中模糊搜索
results = fuzzy_search("hello", "hallo world helloo", max_distance=2)
# [(0, 1, 'hallo'), (12, 1, 'helloo')]
```

### 批量操作

```python
# 批量相似度
sims = batch_similarity([("hello", "hallo"), ("world", "word")])
# [0.8, 0.8]

# 批量距离
dists = batch_distance([("kitten", "sitting"), ("hello", "hello")])
# [3, 0]

# 相似度矩阵
matrix = similarity_matrix(["hello", "hallo", "world"])
# [[1.0, 0.8, 0.2], [0.8, 1.0, 0.2], [0.2, 0.2, 1.0]]
```

### 工具函数

```python
# 归一化距离
norm = normalized_levenshtein("hello", "hallo")  # 0.2

# 汉明距离（仅等长字符串）
hamming = hamming_distance("karolin", "kathrin")  # 3

# 一次编辑判断
is_one = is_one_edit_away("hello", "hallo")  # True

# 拼写建议
suggestions = spell_check_suggestions("helo", ["hello", "help", "held"], max_distance=1)
# [('hello', 1), ('help', 1), ('held', 1)]
```

## 测试

```bash
python levenshtein_utils_test.py
```

测试覆盖（50+ 测试用例）:
- 基础 Levenshtein 距离（相同、空、Unicode、长字符串）
- 空间优化版（一致性、对称性）
- 阈值优化（阈值内、超阈值、长度差异）
- 相似度计算（比率、Jaro、Jaro-Winkler）
- 编辑操作序列（回溯、应用、描述）
- Damerau-Levenshtein（交换优势）
- LCS（经典例子、长度、边界）
- 模糊搜索（相似查找、最近、文本搜索）
- 批量操作（批量相似度、距离、矩阵）
- 工具函数（归一化、汉明、一次编辑）
- 边界情况（单字符、长字符串、阈值效率）

## 应用场景

- 拼写检查与纠错
- 模糊搜索
- DNA 序列比对
- 姓名匹配
- 文档相似度比较
- 数据清洗（重复检测）
- 机器翻译评估
- OCR 结果校正

## 算法说明

### Levenshtein 距离

定义：将字符串 A 转换为 B 所需的最少单字符编辑操作数。

允许操作：
- 插入一个字符
- 删除一个字符
- 替换一个字符

时间复杂度：O(m×n)
空间复杂度：O(m×n) 或优化版 O(min(m,n))

### Damerau-Levenshtein

额外允许相邻字符交换操作。

例子：`ab` → `ba`
- Levenshtein: 2（两次替换）
- Damerau: 1（一次交换）

### Jaro-Winkler

特点：对公共前缀给予更高权重。

公式：
```
JW = Jaro + (prefix_len × scale × (1 - Jaro))
```

适合：姓名匹配、拼写变体检测。

## 性能建议

- 长字符串使用 `levenshtein_distance_optimized`
- 有阈值需求使用 `levenshtein_distance_threshold`
- 批量计算使用 `batch_*` 函数
- 姓名匹配优先用 Jaro-Winkler

## 许可证

MIT License - 详见项目 LICENSE 文件

---

**作者**: AllToolkit  
**日期**: 2026-05-20