# Boyer Moore Utils


boyer_moore_utils/mod.py - Boyer-Moore 字符串搜索算法工具集
零外部依赖，纯Python标准库实现

功能：
- Boyer-Moore 字符串搜索（坏字符规则 + 好后缀规则）
- 单次搜索、全部搜索、计数、替换
- 大小写敏感/不敏感搜索
- 支持搜索位置限制
- 搜索结果详情（位置、匹配文本、上下文）
- 批量模式搜索（多模式匹配）
- 性能统计和对比工具

算法特点：
- 平均时间复杂度 O(n/m)，最坏 O(n)
- 从右向左匹配，利用跳过规则大幅减少比较次数
- 适用于长模式文本搜索，效率极高


## 功能

### 类

- **SearchResult**: 搜索结果对象
  方法: start, end, to_dict
- **SearchStats**: 搜索统计信息
  方法: to_dict, efficiency

### 函数

- **boyer_moore_search(text, pattern, case_sensitive**, ...) - 使用 Boyer-Moore 算法搜索模式在文本中首次出现的位置
- **boyer_moore_find_all(text, pattern, case_sensitive**, ...) - 查找模式在文本中所有出现的位置
- **boyer_moore_count(text, pattern, case_sensitive**, ...) - 统计模式在文本中出现的次数
- **boyer_moore_replace(text, pattern, replacement**, ...) - 替换文本中所有匹配的模式
- **boyer_moore_find_with_context(text, pattern, context_len**, ...) - 查找所有匹配并返回包含上下文的详细信息
- **boyer_moore_multi_search(text, patterns, case_sensitive**) - 在文本中搜索多个模式
- **boyer_moore_multi_find_first(text, patterns, case_sensitive**) - 查找多个模式中最早出现的那个
- **boyer_moore_search_with_stats(text, pattern, case_sensitive**) - 搜索并返回详细统计信息
- **compare_with_naive(text, pattern**) - 比较 Boyer-Moore 与朴素搜索的性能
- **search(text, pattern, case_sensitive**) - boyer_moore_search 的简写形式

... 共 19 个函数

## 使用示例

```python
from mod import boyer_moore_search

# 使用 boyer_moore_search
result = boyer_moore_search()
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
