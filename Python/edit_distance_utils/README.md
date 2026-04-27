# Edit Distance Utils


edit_distance_utils - 编辑距离与字符串相似度工具集

提供多种编辑距离算法和字符串相似度计算方法，适用于：
- 拼写检查与自动纠正
- 模糊搜索与匹配
- DNA序列比对
- 抄袭检测
- 自动补全建议

零外部依赖，纯Python实现。


## 功能

### 类

- **EditDistanceCalculator**: 编辑距离计算器类

提供缓存和批量计算功能，适用于需要多次计算相似度的场景

Example:
    >>> calc = EditDistanceCalculator(method='jaro_winkler')
    >>> calc
  方法: similarity, batch_similarity, clear_cache

### 函数

- **levenshtein_distance(s1, s2**) - 计算两个字符串之间的 Levenshtein 编辑距离
- **damerau_levenshtein_distance(s1, s2**) - 计算两个字符串之间的 Damerau-Levenshtein 编辑距离
- **hamming_distance(s1, s2**) - 计算两个等长字符串之间的 Hamming 距离
- **jaro_similarity(s1, s2**) - 计算两个字符串之间的 Jaro 相似度
- **jaro_winkler_similarity(s1, s2, scaling_factor**) - 计算两个字符串之间的 Jaro-Winkler 相似度
- **lcs_length(s1, s2**) - 计算两个字符串的最长公共子序列长度
- **lcs_string(s1, s2**) - 获取两个字符串的最长公共子序列
- **normalized_levenshtein(s1, s2**) - 计算归一化的 Levenshtein 相似度
- **similarity_ratio(s1, s2, method**) - 计算两个字符串的相似比率
- **fuzzy_match(query, candidates, threshold**, ...) - 模糊匹配：从候选列表中找出与查询字符串相似的项

... 共 20 个函数

## 使用示例

```python
from mod import levenshtein_distance

# 使用 levenshtein_distance
result = levenshtein_distance()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
