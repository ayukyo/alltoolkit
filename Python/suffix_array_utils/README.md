# Suffix Array Utils


Suffix Array Utils - 后缀数组工具模块

后缀数组是一种高效的字符串处理数据结构，用于解决多种字符串问题：
- 模式匹配（查找子串出现位置）
- 最长重复子串
- 最长公共子串
- 字符串排序和排名
- 统计不同子串数量

特点：
- 构建时间 O(n log n) 或 O(n log² n)
- 查询时间 O(m log n)，m为模式串长度
- 空间复杂度 O(n)

零外部依赖，纯Python实现。


## 功能

### 类

- **SuffixArray**: 后缀数组实现

后缀数组是字符串所有后缀按字典序排序后的数组，
每个元素表示对应后缀在原字符串中的起始位置。
  方法: search, contains, count_occurrences, longest_repeated_substring, all_repeated_substrings ... (11 个方法)
- **SuffixArrayAdvanced**: 后缀数组高级功能扩展
  方法: lcp_between_suffixes, count_substring_occurrences, find_maximal_palindromes

### 函数

- **build_suffix_array(text**) - 快速构建后缀数组
- **build_lcp_array(text**) - 快速构建LCP数组
- **find_all_occurrences(text, pattern**) - 在文本中查找模式串的所有出现位置
- **longest_repeated_substring(text**) - 找出文本中最长的重复子串
- **longest_common_substring(text1, text2**) - 找出两个字符串的最长公共子串
- **count_distinct_substrings(text**) - 计算字符串中不同子串的数量
- **pattern_exists(text, pattern**) - 检查模式串是否存在于文本中
- **search(self, pattern**) - 在文本中查找模式串的所有出现位置
- **contains(self, pattern**) - 检查模式串是否存在于文本中
- **count_occurrences(self, pattern**) - 统计模式串在文本中出现的次数

... 共 23 个函数

## 使用示例

```python
from mod import build_suffix_array

# 使用 build_suffix_array
result = build_suffix_array()
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
