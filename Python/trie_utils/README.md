# Trie Utils


Trie（前缀树）工具模块

提供高效的字符串前缀匹配、自动补全、词典查找等功能。
零外部依赖，纯Python实现。

核心功能：
- Trie 数据结构的完整实现
- 前缀搜索与自动补全
- 通配符模式匹配
- 最长前缀匹配
- 词频统计
- 序列化与反序列化


## 功能

### 类

- **TrieNode**: Trie 节点
- **Trie**: Trie（前缀树）数据结构

适用于：
- 自动补全
- 拼写检查
- IP路由
- 词典实现
- 词频统计

示例:
    >>> trie = Trie()
    >>> trie
  方法: insert, search, starts_with, delete, longest_prefix ... (22 个方法)
- **SuffixTrie**: 后缀树（简化实现）

用于子串匹配、最长重复子串等问题
  方法: build_from_string, contains_substring, find_all_occurrences
- **PrefixSet**: 前缀集合

高效的前缀匹配集合，适用于大量字符串的前缀检测
  方法: add, update, matches_any_prefix, get_matching_prefix

### 函数

- **build_trie(words**) - 从单词列表构建Trie
- **find_common_prefix(words**) - 查找单词列表的最长公共前缀
- **word_frequency_analysis(words**) - 分析单词频率并返回排序结果
- **insert(self, word, data**) - 插入一个单词到Trie中
- **search(self, word**) - 精确搜索一个单词是否存在
- **starts_with(self, prefix, limit**) - 查找所有以指定前缀开头的单词
- **delete(self, word**) - 删除一个单词
- **longest_prefix(self, text**) - 查找文本中最长匹配的前缀单词
- **contains_prefix(self, prefix**) - 检查是否存在以指定前缀开头的单词
- **pattern_match(self, pattern, wildcard**) - 模式匹配（支持通配符）

... 共 32 个函数

## 使用示例

```python
from mod import build_trie

# 使用 build_trie
result = build_trie()
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
