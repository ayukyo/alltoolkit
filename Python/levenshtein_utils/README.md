# Levenshtein Distance Utils - 编辑距离工具

计算字符串相似度的实用工具集，零外部依赖。

## 功能特性

- ✅ **Levenshtein 编辑距离** - 计算将一个字符串转换为另一个所需的最少编辑操作次数
- ✅ **字符串相似度** - 计算 0-1 范围的相似度分数
- ✅ **模糊匹配** - 在候选列表中查找最相似的字符串
- ✅ **编辑操作序列** - 获取详细的编辑操作步骤
- ✅ **自定义成本** - 支持自定义插入/删除/替换操作成本
- ✅ **Damerau-Levenshtein** - 支持相邻字符交换的扩展距离
- ✅ **汉明距离** - 适用于等长字符串的距离计算

## 快速开始

### 基本编辑距离

```python
from mod import levenshtein_distance, similarity

# 计算编辑距离
dist = levenshtein_distance("kitten", "sitting")
print(dist)  # 输出: 3

# 计算相似度 (0-1)
sim = similarity("kitten", "sitting")
print(f"{sim:.2%}")  # 输出: 57.14%
```

### 模糊匹配

```python
from mod import find_closest, find_all_closest

candidates = ["apple", "banana", "orange", "application"]

# 查找最相似的字符串
closest = find_closest("banan", candidates)
print(closest)  # 输出: "banana"

# 查找前 N 个最相似的字符串
top_matches = find_all_closest("banan", candidates, top_n=3)
for word, sim in top_matches:
    print(f"{word}: {sim:.2%}")
# 输出:
# banana: 83.33%
# apple: 20.00%
# orange: 20.00%

# 使用阈值过滤
result = find_closest("xyz", candidates, threshold=0.5)
print(result)  # 输出: None (无满足阈值的匹配)
```

### 编辑操作序列

```python
from mod import edit_sequence, apply_edits

# 获取编辑距离和操作序列
dist, ops = edit_sequence("kitten", "sitting")
print(f"编辑距离: {dist}")
print("操作序列:")
for op, data in ops:
    print(f"  - {op}: {data}")

# 应用编辑操作
result = apply_edits("kitten", ops)
print(result)  # 输出: "sitting"
```

### 高级功能

```python
from mod import (
    damerau_levenshtein_distance,
    hamming_distance,
    ratio,
    normalized_distance
)

# Damerau-Levenshtein 距离 (支持相邻字符交换)
dl_dist = damerau_levenshtein_distance("abcd", "acbd")
print(dl_dist)  # 输出: 1 (只需一次相邻交换)

# 汉明距离 (仅限等长字符串)
h_dist = hamming_distance("karolin", "kathrin")
print(h_dist)  # 输出: 3

# 匹配比率 (与 fuzzywuzzy 兼容)
r = ratio("hello world", "hello")
print(f"{r:.2f}%")  # 输出: 62.50%

# 归一化距离
nd = normalized_distance("abc", "abd")
print(nd)  # 输出: 0.167
```

### 自定义操作成本

```python
from mod import levenshtein_distance

# 插入操作成本更高
dist = levenshtein_distance(
    "abc",
    "ab",
    insert_cost=2,    # 插入成本
    delete_cost=1,    # 删除成本
    replace_cost=1    # 替换成本
)
```

## API 参考

### `levenshtein_distance(s1, s2, *, insert_cost=1, delete_cost=1, replace_cost=1)`

计算两个字符串之间的 Levenshtein 编辑距离。

**参数:**
- `s1` (str): 源字符串
- `s2` (str): 目标字符串
- `insert_cost` (float): 插入操作成本，默认 1
- `delete_cost` (float): 删除操作成本，默认 1
- `replace_cost` (float): 替换操作成本，默认 1

**返回:** `int` - 编辑距离

### `similarity(s1, s2)`

计算两个字符串的相似度 (0-1)。

**返回:** `float` - 相似度，1 表示完全相同，0 表示完全不同

### `find_closest(target, candidates, *, threshold=0.0, return_distance=False)`

在候选列表中查找最相似的字符串。

**参数:**
- `target` (str): 目标字符串
- `candidates` (List[str]): 候选字符串列表
- `threshold` (float): 相似度阈值 (0-1)
- `return_distance` (bool): 是否返回距离

**返回:** `str` 或 `Tuple[str, int]` 或 `None`

### `find_all_closest(target, candidates, *, top_n=5, threshold=0.0)`

查找所有满足阈值的相似字符串，按相似度排序。

**返回:** `List[Tuple[str, float]]` - (字符串, 相似度) 列表

### `edit_sequence(s1, s2)`

计算编辑距离并返回编辑操作序列。

**返回:** `Tuple[int, List]` - (距离, 操作列表)

操作类型:
- `('equal', (i, j, length))`: 相同字符片段
- `('replace', (i, char))`: 在位置 i 替换字符
- `('insert', (i, char))`: 在位置 i 插入字符
- `('delete', (i, length))`: 从位置 i 删除字符

### `apply_edits(s, operations)`

将编辑操作序列应用到字符串。

### `damerau_levenshtein_distance(s1, s2)`

计算 Damerau-Levenshtein 距离（支持相邻字符交换）。

### `hamming_distance(s1, s2)`

计算汉明距离（仅限等长字符串）。

**异常:** `ValueError` - 当字符串长度不等时

### `ratio(s1, s2)`

计算匹配比率 (0-100)，与 fuzzywuzzy 库兼容。

### `normalized_distance(s1, s2)`

计算归一化编辑距离 (0-1)。

## 使用场景

1. **拼写检查和纠正**
   ```python
   dictionary = ["apple", "banana", "orange"]
   user_input = "appel"
   suggestion = find_closest(user_input, dictionary)
   ```

2. **模糊搜索**
   ```python
   def search_products(query, products):
       return find_all_closest(query, products, threshold=0.6)
   ```

3. **数据去重**
   ```python
   def find_duplicates(records):
       duplicates = []
       for i, r1 in enumerate(records):
           for r2 in records[i+1:]:
               if similarity(r1, r2) > 0.9:
                   duplicates.append((r1, r2))
       return duplicates
   ```

4. **DNA 序列比对**
   ```python
   seq1 = "AGCTAGCT"
   seq2 = "AGCTAGGT"
   distance = levenshtein_distance(seq1, seq2)
   ```

## 性能说明

- 时间复杂度: O(m × n)，其中 m 和 n 是两个字符串的长度
- 空间复杂度: O(min(m, n))，使用优化的动态规划算法
- 对于大字符串，考虑使用更高效的算法（如 BK-tree）

## 测试

运行测试：

```bash
python -m pytest test_mod.py -v
```

## 许可证

MIT License