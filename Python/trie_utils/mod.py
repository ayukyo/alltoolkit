"""
Trie (前缀树) 工具模块

提供完整的 Trie 数据结构实现，支持：
- 单词插入、删除、查找
- 前缀搜索和自动补全
- 拼写检查和建议
- 词频统计
- 模式匹配

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, Optional, Dict, Set, Tuple, Callable, Iterator
from collections import defaultdict


class TrieNode:
    """Trie 节点类"""
    
    __slots__ = ['children', 'is_end', 'count', 'data']
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False
        self.count: int = 0  # 词频统计
        self.data: Optional[dict] = None  # 附加数据


class Trie:
    """
    Trie (前缀树) 实现
    
    用于高效的字符串存储、检索和前缀匹配。
    
    时间复杂度：
    - 插入：O(m)，m 为字符串长度
    - 查找：O(m)
    - 前缀搜索：O(m + k)，k 为匹配数量
    
    空间复杂度：O(n * m)，n 为字符串数量，m 为平均长度
    
    示例:
        >>> trie = Trie()
        >>> trie.insert("hello")
        >>> trie.insert("world")
        >>> trie.search("hello")
        True
        >>> trie.starts_with("hel")
        ['hello']
    """
    
    def __init__(self):
        self.root = TrieNode()
        self._size: int = 0
    
    def insert(self, word: str, data: Optional[dict] = None) -> None:
        """
        插入单词到 Trie
        
        Args:
            word: 要插入的单词
            data: 可选的附加数据
        """
        if not word:
            return
            
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end:
            self._size += 1
        node.is_end = True
        node.count += 1
        if data:
            node.data = data
    
    def search(self, word: str) -> bool:
        """
        查找单词是否存在于 Trie
        
        Args:
            word: 要查找的单词
            
        Returns:
            bool: 单词是否存在
        """
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        """
        查找所有以指定前缀开头的单词
        
        Args:
            prefix: 前缀字符串
            limit: 返回结果的最大数量
            
        Returns:
            List[str]: 匹配的单词列表
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        
        results = []
        self._collect_words(node, prefix, results, limit)
        return results
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """查找前缀对应的节点"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _collect_words(self, node: TrieNode, prefix: str, 
                       results: List[str], limit: Optional[int] = None) -> None:
        """收集所有从该节点开始的完整单词"""
        if limit is not None and len(results) >= limit:
            return
            
        if node.is_end:
            results.append(prefix)
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results, limit)
    
    def delete(self, word: str) -> bool:
        """
        从 Trie 中删除单词
        
        Args:
            word: 要删除的单词
            
        Returns:
            bool: 是否成功删除
        """
        if not word:
            return False
        
        # 使用栈记录路径
        path = []
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            path.append((char, node))
            node = node.children[char]
        
        if not node.is_end:
            return False
        
        node.is_end = False
        node.count = 0
        node.data = None
        self._size -= 1
        
        # 清理空节点
        for char, parent in reversed(path):
            child = parent.children[char]
            if not child.children and not child.is_end:
                del parent.children[char]
            else:
                break
        
        return True
    
    def get_data(self, word: str) -> Optional[dict]:
        """
        获取单词关联的数据
        
        Args:
            word: 单词
            
        Returns:
            Optional[dict]: 关联的数据，不存在则返回 None
        """
        node = self._find_node(word)
        if node and node.is_end:
            return node.data
        return None
    
    def get_count(self, word: str) -> int:
        """
        获取单词的词频
        
        Args:
            word: 单词
            
        Returns:
            int: 词频计数
        """
        node = self._find_node(word)
        if node and node.is_end:
            return node.count
        return 0
    
    def count_prefix(self, prefix: str) -> int:
        """
        统计以指定前缀开头的单词数量
        
        Args:
            prefix: 前缀
            
        Returns:
            int: 单词数量
        """
        node = self._find_node(prefix)
        if node is None:
            return 0
        return self._count_words(node)
    
    def _count_words(self, node: TrieNode) -> int:
        """统计从该节点开始的单词数量"""
        count = 1 if node.is_end else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count
    
    def longest_common_prefix(self) -> str:
        """
        查找 Trie 中所有单词的最长公共前缀
        
        Returns:
            str: 最长公共前缀
        """
        if self._size == 0:
            return ""
        
        prefix = []
        node = self.root
        
        while len(node.children) == 1 and not node.is_end:
            char = next(iter(node.children))
            prefix.append(char)
            node = node.children[char]
        
        return "".join(prefix)
    
    def contains_prefix(self, prefix: str) -> bool:
        """
        检查是否存在以指定前缀开头的单词
        
        Args:
            prefix: 前缀
            
        Returns:
            bool: 是否存在
        """
        return self._find_node(prefix) is not None
    
    def autocomplete(self, prefix: str, limit: int = 10, 
                     sort_by: str = 'alphabetical') -> List[str]:
        """
        自动补全功能
        
        Args:
            prefix: 输入前缀
            limit: 返回结果数量限制
            sort_by: 排序方式 ('alphabetical', 'frequency')
            
        Returns:
            List[str]: 补全建议列表
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        
        # 收集所有匹配单词及其频率
        words_with_count = []
        self._collect_words_with_count(node, prefix, words_with_count)
        
        # 排序
        if sort_by == 'frequency':
            words_with_count.sort(key=lambda x: (-x[1], x[0]))
        else:
            words_with_count.sort(key=lambda x: x[0])
        
        return [word for word, _ in words_with_count[:limit]]
    
    def _collect_words_with_count(self, node: TrieNode, prefix: str,
                                   results: List[Tuple[str, int]]) -> None:
        """收集单词及其词频"""
        if node.is_end:
            results.append((prefix, node.count))
        
        for char, child in node.children.items():
            self._collect_words_with_count(child, prefix + char, results)
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, word: str) -> bool:
        return self.search(word)
    
    def __iter__(self) -> Iterator[str]:
        """迭代所有单词"""
        results = []
        self._collect_words(self.root, "", results)
        return iter(results)


class SpellChecker:
    """
    基于 Trie 的拼写检查器
    
    支持编辑距离计算和拼写建议
    
    示例:
        >>> checker = SpellChecker()
        >>> checker.load_words(["hello", "world", "help"])
        >>> checker.suggest("helo")
        ['hello', 'help']
    """
    
    def __init__(self, max_edit_distance: int = 2):
        """
        初始化拼写检查器
        
        Args:
            max_edit_distance: 最大编辑距离
        """
        self.trie = Trie()
        self.max_edit_distance = max_edit_distance
        self._word_set: Set[str] = set()
    
    def load_words(self, words: List[str]) -> None:
        """
        加载单词列表
        
        Args:
            words: 单词列表
        """
        for word in words:
            word = word.lower().strip()
            if word:
                self.trie.insert(word)
                self._word_set.add(word)
    
    def is_correct(self, word: str) -> bool:
        """
        检查单词拼写是否正确
        
        Args:
            word: 要检查的单词
            
        Returns:
            bool: 拼写是否正确
        """
        return word.lower() in self._word_set
    
    def suggest(self, word: str, limit: int = 5) -> List[str]:
        """
        提供拼写建议
        
        Args:
            word: 可能拼写错误的单词
            limit: 返回建议数量
            
        Returns:
            List[str]: 拼写建议列表
        """
        word = word.lower()
        
        if word in self._word_set:
            return [word]
        
        suggestions = set()
        
        # 编辑距离为 1 的变体
        edits1 = self._edits1(word)
        for edit in edits1:
            if edit in self._word_set:
                suggestions.add(edit)
        
        if len(suggestions) >= limit:
            return sorted(suggestions)[:limit]
        
        # 编辑距离为 2 的变体
        edits2 = set()
        for e1 in edits1:
            edits2.update(self._edits1(e1))
        
        for edit in edits2:
            if edit in self._word_set:
                suggestions.add(edit)
            if len(suggestions) >= limit * 2:
                break
        
        return sorted(suggestions)[:limit]
    
    def _edits1(self, word: str) -> Set[str]:
        """生成编辑距离为 1 的所有变体"""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        
        return set(deletes + transposes + replaces + inserts)
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """
        自动补全
        
        Args:
            prefix: 前缀
            limit: 返回数量
            
        Returns:
            List[str]: 补全建议
        """
        return self.trie.autocomplete(prefix.lower(), limit)


class WordDictionary:
    """
    支持通配符匹配的单词字典
    
    支持通配符：
    - '.' 匹配任意单个字符
    - '*' 匹配任意多个字符（包括零个）
    
    示例:
        >>> wd = WordDictionary()
        >>> wd.add_word("hello")
        >>> wd.add_word("help")
        >>> wd.search("h.llo")
        True
        >>> wd.search("he*")
        True
    """
    
    def __init__(self):
        self.trie = Trie()
        self._words: Set[str] = set()
    
    def add_word(self, word: str) -> None:
        """添加单词"""
        self.trie.insert(word)
        self._words.add(word)
    
    def search(self, pattern: str) -> bool:
        """
        搜索匹配模式
        
        Args:
            pattern: 含通配符的模式
            
        Returns:
            bool: 是否存在匹配
        """
        return self._search_pattern(self.trie.root, pattern, 0)
    
    def _search_pattern(self, node: TrieNode, pattern: str, index: int) -> bool:
        """递归搜索模式"""
        if index == len(pattern):
            return node.is_end
        
        char = pattern[index]
        
        if char == '.':
            # 匹配任意单个字符
            for child in node.children.values():
                if self._search_pattern(child, pattern, index + 1):
                    return True
            return False
        
        elif char == '*':
            # 匹配任意多个字符
            # 情况1：* 匹配零个字符
            if self._search_pattern(node, pattern, index + 1):
                return True
            # 情况2：* 匹配一个或多个字符
            for child in node.children.values():
                if self._search_pattern(child, pattern, index):
                    return True
            return False
        
        else:
            # 精确匹配
            if char in node.children:
                return self._search_pattern(node.children[char], pattern, index + 1)
            return False
    
    def find_all_matches(self, pattern: str) -> List[str]:
        """
        查找所有匹配模式的单词
        
        Args:
            pattern: 含通配符的模式
            
        Returns:
            List[str]: 所有匹配的单词
        """
        results = []
        self._find_matches(self.trie.root, pattern, 0, "", results)
        return results
    
    def _find_matches(self, node: TrieNode, pattern: str, index: int,
                      current: str, results: List[str]) -> None:
        """递归查找所有匹配"""
        if index == len(pattern):
            if node.is_end:
                results.append(current)
            return
        
        char = pattern[index]
        
        if char == '.':
            for c, child in node.children.items():
                self._find_matches(child, pattern, index + 1, current + c, results)
        
        elif char == '*':
            # 匹配零个
            self._find_matches(node, pattern, index + 1, current, results)
            # 匹配一个或多个
            for c, child in node.children.items():
                self._find_matches(child, pattern, index, current + c, results)
        
        else:
            if char in node.children:
                self._find_matches(node.children[char], pattern, index + 1,
                                 current + char, results)


class SuffixTrie:
    """
    后缀 Trie 实现
    
    用于高效的子字符串匹配和模式搜索
    
    示例:
        >>> st = SuffixTrie("banana")
        >>> st.contains("ana")
        True
        >>> st.find_all("an")
        [1, 3]
    """
    
    def __init__(self, text: str = ""):
        """
        初始化后缀 Trie
        
        Args:
            text: 要构建后缀 Trie 的文本
        """
        self.trie = Trie()
        self._text = ""
        if text:
            self.build(text)
    
    def build(self, text: str) -> None:
        """
        构建后缀 Trie
        
        Args:
            text: 输入文本
        """
        self._text = text
        for i in range(len(text)):
            self.trie.insert(text[i:])
    
    def contains(self, pattern: str) -> bool:
        """
        检查是否包含指定模式
        
        Args:
            pattern: 要查找的模式
            
        Returns:
            bool: 是否包含
        """
        return self.trie.contains_prefix(pattern)
    
    def find_all(self, pattern: str) -> List[int]:
        """
        查找所有模式出现的位置
        
        Args:
            pattern: 要查找的模式
            
        Returns:
            List[int]: 所有起始位置的列表
        """
        positions = []
        pattern_len = len(pattern)
        
        for i in range(len(self._text) - pattern_len + 1):
            if self._text[i:i + pattern_len] == pattern:
                positions.append(i)
        
        return positions
    
    def count_occurrences(self, pattern: str) -> int:
        """
        统计模式出现次数
        
        Args:
            pattern: 要统计的模式
            
        Returns:
            int: 出现次数
        """
        return len(self.find_all(pattern))
    
    def longest_repeated_substring(self) -> str:
        """
        查找最长重复子串
        
        Returns:
            str: 最长重复子串
        """
        if not self._text:
            return ""
        
        result = ""
        n = len(self._text)
        
        # 检查所有可能的子串长度
        for length in range(1, n // 2 + 1):
            seen = set()
            for i in range(n - length + 1):
                substr = self._text[i:i + length]
                if substr in seen and len(substr) > len(result):
                    result = substr
                seen.add(substr)
        
        return result


class TrieSet:
    """
    基于 Trie 的字符串集合
    
    提供高效的集合操作
    
    示例:
        >>> ts = TrieSet()
        >>> ts.add("hello")
        >>> ts.add("world")
        >>> "hello" in ts
        True
    """
    
    def __init__(self, words: Optional[List[str]] = None):
        """
        初始化 TrieSet
        
        Args:
            words: 初始单词列表
        """
        self.trie = Trie()
        if words:
            for word in words:
                self.add(word)
    
    def add(self, word: str) -> None:
        """添加单词"""
        self.trie.insert(word)
    
    def remove(self, word: str) -> bool:
        """移除单词"""
        return self.trie.delete(word)
    
    def __contains__(self, word: str) -> bool:
        return self.trie.search(word)
    
    def __len__(self) -> int:
        return len(self.trie)
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.trie)
    
    def starts_with(self, prefix: str) -> List[str]:
        """查找前缀匹配的所有单词"""
        return self.trie.starts_with(prefix)
    
    def union(self, other: 'TrieSet') -> 'TrieSet':
        """并集"""
        result = TrieSet()
        for word in self:
            result.add(word)
        for word in other:
            result.add(word)
        return result
    
    def intersection(self, other: 'TrieSet') -> 'TrieSet':
        """交集"""
        result = TrieSet()
        for word in self:
            if word in other:
                result.add(word)
        return result
    
    def difference(self, other: 'TrieSet') -> 'TrieSet':
        """差集"""
        result = TrieSet()
        for word in self:
            if word not in other:
                result.add(word)
        return result
    
    def isdisjoint(self, other: 'TrieSet') -> bool:
        """是否没有交集"""
        for word in self:
            if word in other:
                return False
        return True
    
    def issubset(self, other: 'TrieSet') -> bool:
        """是否是子集"""
        for word in self:
            if word not in other:
                return False
        return True
    
    def issuperset(self, other: 'TrieSet') -> bool:
        """是否是超集"""
        return other.issubset(self)


def build_trie_from_words(words: List[str]) -> Trie:
    """
    从单词列表构建 Trie
    
    Args:
        words: 单词列表
        
    Returns:
        Trie: 构建好的 Trie
    """
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def find_common_prefix(words: List[str]) -> str:
    """
    查找单词列表的最长公共前缀
    
    Args:
        words: 单词列表
        
    Returns:
        str: 最长公共前缀
    """
    if not words:
        return ""
    
    trie = build_trie_from_words(words)
    return trie.longest_common_prefix()


def group_by_prefix(words: List[str], prefix_len: int = 2) -> Dict[str, List[str]]:
    """
    按前缀分组单词
    
    Args:
        words: 单词列表
        prefix_len: 前缀长度
        
    Returns:
        Dict[str, List[str]]: 分组结果
    """
    groups: Dict[str, List[str]] = defaultdict(list)
    
    for word in words:
        if len(word) >= prefix_len:
            prefix = word[:prefix_len]
            groups[prefix].append(word)
    
    return dict(groups)


def autocomplete_suggestions(trie: Trie, prefix: str, 
                            limit: int = 10,
                            sort_by_frequency: bool = False) -> List[str]:
    """
    获取自动补全建议
    
    Args:
        trie: Trie 对象
        prefix: 输入前缀
        limit: 返回数量限制
        sort_by_frequency: 是否按词频排序
        
    Returns:
        List[str]: 补全建议列表
    """
    sort_by = 'frequency' if sort_by_frequency else 'alphabetical'
    return trie.autocomplete(prefix, limit, sort_by)


# 导出公共接口
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