# Kmp Utils


kmp_utils/mod.py - Knuth-Morris-Pratt (KMP) 字符串搜索算法工具集
零外部依赖，纯Python标准库实现

功能：
- KMP 字符串搜索（利用失败函数避免重复比较）
- 单次搜索、全部搜索、计数、替换
- 大小写敏感/不敏感搜索
- 支持搜索位置限制
- 搜索结果详情（位置、匹配文本、上下文）
- 批量模式搜索（多模式匹配）
- Aho-Corasick 简化版多模式匹配
- 边界检测（前缀/后缀/子串）
- 周期性字符串分析

算法特点：
- 时间复杂度 O(n + m)，n 为文本长度，m 为模式长度
- 预处理模式构建失败函数，匹配时无需回溯
- 适用于需要多次匹配同一模式或批量模式匹配的场景


## 功能

### 类

- **MatchResult**: 匹配结果对象
  方法: matched, context
- **AhoCorasickNode**: Aho-Corasick 自动机节点
- **AhoCorasick**: Aho-Corasick 多模式匹配自动机

基于 KMP 的失败函数思想构建 Trie 树自动机，
实现一次扫描匹配多个模式的高效搜索。

时间复杂度: O(n + m + k)，其中 n 是文本长度，m 是模式总长度，k 是匹配数

示例:
    >>> ac = AhoCorasick(["he", "she", "his", "hers"])
    >>> ac
  方法: search, search_with_positions

### 函数

- **build_failure_function(pattern**) - 构建 KMP 失败函数（部分匹配表 / Next 数组）
- **build_next_array(pattern**) - 构建 KMP 的 next 数组（另一种表示形式）
- **search(text, pattern, start**) - KMP 单次搜索 - 查找模式在文本中首次出现的位置
- **search_all(text, pattern, overlapping**) - KMP 全部搜索 - 查找模式在文本中所有出现的位置
- **count(text, pattern, overlapping**) - 计算模式在文本中出现的次数
- **replace(text, pattern, replacement**, ...) - 替换文本中的模式
- **search_ignore_case(text, pattern, start**) - 大小写不敏感的单次搜索
- **search_all_ignore_case(text, pattern, overlapping**) - 大小写不敏感的全部搜索
- **search_detailed(text, pattern, start**) - 详细搜索 - 返回匹配结果对象
- **search_all_detailed(text, pattern, overlapping**) - 详细全部搜索 - 返回所有匹配结果对象

... 共 34 个函数

## 使用示例

```python
from mod import build_failure_function

# 使用 build_failure_function
result = build_failure_function()
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
