# Rabin Karp Utils


Rabin-Karp 字符串匹配算法工具模块

Rabin-Karp 算法是一种基于哈希的字符串匹配算法，特别适合多模式匹配场景。
核心思想：使用滚动哈希快速计算子串哈希值，减少字符串比较次数。

时间复杂度:
- 单模式匹配: O(n + m) 平均，O(nm) 最坏
- 多模式匹配: O(n + km) 其中 k 为模式数量

空间复杂度: O(1) 单模式，O(k) 多模式

特点:
- 支持多模式同时匹配
- 支持扩展到二维模式匹配
- 适合检测抄袭、DNA序列分析等场景


## 功能

### 类

- **MatchResult**: 匹配结果
- **RollingHash**: 滚动哈希类

使用多项式滚动哈希实现高效的字符串哈希计算。
支持在 O(1) 时间内滑动窗口更新哈希值。
  方法: compute, slide, hash
- **RabinKarpMatcher**: Rabin-Karp 匹配器类

预编译模式，支持高效的多文本搜索。
适合需要多次搜索相同模式的场景。
  方法: search, search_iter, add_pattern, remove_pattern

### 函数

- **rabin_karp_search(text, pattern, base**, ...) - 单模式 Rabin-Karp 搜索
- **multi_pattern_search(text, patterns, base**, ...) - 多模式 Rabin-Karp 搜索
- **find_all_occurrences(text, pattern**) - 查找模式在文本中的所有出现位置（便捷方法）
- **contains_pattern(text, pattern**) - 检查文本是否包含模式
- **count_occurrences(text, pattern**) - 统计模式在文本中出现的次数
- **find_with_wildcards(text, pattern, wildcard**) - 支持通配符的 Rabin-Karp 搜索
- **find_longest_repeated_substring(text, min_length**) - 查找最长重复子串
- **find_common_substring(strings, min_length**) - 查找多个字符串的最长公共子串
- **compute_similarity(text1, text2, k**) - 基于公共子串的文本相似度计算
- **detect_plagiarism(documents, threshold, k**) - 检测文档之间的抄袭嫌疑

... 共 22 个函数

## 使用示例

```python
from mod import rabin_karp_search

# 使用 rabin_karp_search
result = rabin_karp_search()
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
