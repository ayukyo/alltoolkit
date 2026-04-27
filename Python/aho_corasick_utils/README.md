# Aho Corasick Utils


AllToolkit - Aho-Corasick Algorithm Utilities Module
====================================================
A comprehensive Aho-Corasick automaton implementation with zero external dependencies.

The Aho-Corasick algorithm is an efficient string matching algorithm that can
find all occurrences of multiple patterns in a text in O(n + m + z) time,
where n is text length, m is total pattern length, and z is number of matches.

Features:
    - Build automaton from pattern set
    - Single-pass text matching
    - Case-sensitive and case-insensitive matching
    - Match callback support
    - Streaming text processing
    - Pattern removal and dynamic updates
    - Match positions and pattern info
    - Wildcard pattern support (optional)
    - Custom match handlers
    - Serialization/deserialization support

Use Cases:
    - Keyword detection and extraction
    - Sensitive word filtering
    - Spam detection
    - Virus signature matching
    - DNA sequence analysis
    - Log file pattern matching
    - Real-time content moderation

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **Match**: Represents a match found in the text
  方法: length
- **AhoCorasickNode**: Represents a node in the Aho-Corasick automaton
- **AhoCorasick**: Aho-Corasick string matching automaton
  方法: add_pattern, add_patterns, remove_pattern, build, finditer ... (23 个方法)
- **SensitiveWordFilter**: A convenience wrapper for sensitive word filtering using Aho-Corasick
  方法: add_word, add_words, remove_word, check, find ... (8 个方法)
- **WildcardAhoCorasick**: Aho-Corasick with wildcard support
  方法: add_pattern, add_patterns, findall, finditer
- **MultiPatternReplacer**: Efficient multi-pattern string replacer using Aho-Corasick
  方法: add, add_many, replace

### 函数

- **build_automaton(patterns, case_sensitive**) - Build an Aho-Corasick automaton from patterns.
- **find_all(patterns, text, case_sensitive**) - Find all occurrences of patterns in text.
- **contains_any(patterns, text, case_sensitive**) - Check if text contains any of the patterns.
- **replace_patterns(patterns, text, replacement**, ...) - Replace all pattern matches in text.
- **highlight_patterns(patterns, text, prefix**, ...) - Highlight all pattern matches in text.
- **length(self**) - Return the length of the matched pattern.
- **add_pattern(self, pattern, value**) - Add a single pattern to the automaton.
- **add_patterns(self, patterns, values**) - Add multiple patterns to the automaton.
- **remove_pattern(self, pattern**) - Remove a pattern from the automaton.
- **build(self**) - Build the failure links for the automaton.

... 共 44 个函数

## 使用示例

```python
from mod import build_automaton

# 使用 build_automaton
result = build_automaton()
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
