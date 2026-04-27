# Suffix Tree Utils


Suffix Tree Utils - 后缀树工具库

后缀树（Suffix Tree）是一种紧凑的树形数据结构，用于存储字符串的所有后缀。
支持 O(m) 时间复杂度的模式匹配（m 为模式长度）。

核心功能：
- 后缀树构建（Ukkonen 算法，O(n) 时间复杂度）
- 模式匹配（子串查找）
- 最长重复子串查找
- 最长公共子串查找
- 所有重复子串枚举
- 子串计数

零外部依赖，纯 Python 实现。


## 功能

### 类

- **SuffixTreeNode**: 后缀树节点
  方法: edge_length, is_leaf
- **SuffixTree**: 后缀树实现（Ukkonen 算法）

时间复杂度: O(n) 构建
空间复杂度: O(n)
  方法: search, count_occurrences, contains, longest_repeated_substring, all_repeated_substrings ... (6 个方法)
- **GeneralizedSuffixTree**: 广义后缀树 - 支持多个字符串
  方法: longest_common_substring, all_common_substrings

### 函数

- **build_suffix_tree(text**) - 构建后缀树的便捷函数
- **find_all_occurrences(text, pattern**) - 在文本中查找模式的所有出现位置
- **longest_repeated_substring(text**) - 查找文本中的最长重复子串
- **longest_common_substring(text1, text2**) - 查找两个字符串的最长公共子串
- **count_occurrences(text, pattern**) - 计算模式在文本中的出现次数
- **build_suffix_array(text**) - 构建后缀数组
- **edge_length(self, leaf_end**) - 计算边的长度
- **is_leaf(self**) - 判断是否为叶节点
- **search(self, pattern**) - 查找模式串在文本中的所有出现位置
- **count_occurrences(self, pattern**) - 计算模式串在文本中的出现次数

... 共 16 个函数

## 使用示例

```python
from mod import build_suffix_tree

# 使用 build_suffix_tree
result = build_suffix_tree()
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
