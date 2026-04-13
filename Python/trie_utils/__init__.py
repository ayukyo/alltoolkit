"""Trie (前缀树) 工具模块"""

from .mod import (
    Trie,
    TrieNode,
    SpellChecker,
    WordDictionary,
    SuffixTrie,
    TrieSet,
    build_trie_from_words,
    find_common_prefix,
    group_by_prefix,
    autocomplete_suggestions,
)

__all__ = [
    'Trie',
    'TrieNode',
    'SpellChecker',
    'WordDictionary',
    'SuffixTrie',
    'TrieSet',
    'build_trie_from_words',
    'find_common_prefix',
    'group_by_prefix',
    'autocomplete_suggestions',
]