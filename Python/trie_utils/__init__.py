"""Trie (前缀树/字典树) 工具模块

提供完整的字典树实现，包括：
- 基础 Trie（插入、搜索、删除、前缀匹配）
- 压缩 Trie（Radix Tree）优化空间
- 后缀 Trie（子串匹配、重复模式检测）
- 自动补全功能
- 模糊搜索（编辑距离）
- 词频统计
"""

from .mod import (
    Trie,
    TrieNode,
    CompactTrie,
    SuffixTrie,
    build_trie,
    build_word_trie,
    autocomplete_from_list,
)

__all__ = [
    'Trie',
    'TrieNode',
    'CompactTrie',
    'SuffixTrie',
    'build_trie',
    'build_word_trie',
    'autocomplete_from_list',
]