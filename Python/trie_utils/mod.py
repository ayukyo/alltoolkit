"""
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
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Iterator
from collections import defaultdict
import json


class TrieNode:
    """Trie 节点"""
    
    __slots__ = ['children', 'is_end', 'count', 'data']
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False
        self.count: int = 0  # 以该节点结尾的单词出现次数
        self.data: Any = None  # 可存储额外数据
    
    def __repr__(self) -> str:
        return f"TrieNode(end={self.is_end}, count={self.count}, children={len(self.children)})"


class Trie:
    """
    Trie（前缀树）数据结构
    
    适用于：
    - 自动补全
    - 拼写检查
    - IP路由
    - 词典实现
    - 词频统计
    
    示例:
        >>> trie = Trie()
        >>> trie.insert("hello")
        >>> trie.insert("help")
        >>> trie.search("hello")
        True
        >>> trie.starts_with("hel")
        ['hello', 'help']
    """
    
    def __init__(self):
        self.root = TrieNode()
        self._size = 0
        self._total_chars = 0  # 所有插入字符串的总字符数
    
    def insert(self, word: str, data: Any = None) -> None:
        """
        插入一个单词到Trie中
        
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
            self._total_chars += len(word)
        
        node.is_end = True
        node.count += 1
        if data is not None:
            node.data = data
    
    def search(self, word: str) -> bool:
        """
        精确搜索一个单词是否存在
        
        Args:
            word: 要搜索的单词
            
        Returns:
            是否存在
        """
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix: str, limit: int = 10) -> List[str]:
        """
        查找所有以指定前缀开头的单词
        
        Args:
            prefix: 前缀
            limit: 返回结果的最大数量
            
        Returns:
            匹配的单词列表
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
    
    def _collect_words(self, node: TrieNode, prefix: str, results: List[str], 
                       limit: int, min_count: int = 0) -> None:
        """收集以prefix开头的所有单词"""
        if len(results) >= limit:
            return
        
        if node.is_end and node.count >= min_count:
            results.append(prefix)
        
        # 按词频排序，优先返回高频词
        sorted_children = sorted(node.children.items(), 
                                key=lambda x: x[1].count, reverse=True)
        
        for char, child in sorted_children:
            if len(results) >= limit:
                break
            self._collect_words(child, prefix + char, results, limit, min_count)
    
    def delete(self, word: str) -> bool:
        """
        删除一个单词
        
        Args:
            word: 要删除的单词
            
        Returns:
            是否成功删除
        """
        if not word:
            return False
        
        # 使用栈记录路径：(节点, 字符)
        path = []
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            path.append((node, char))
            node = node.children[char]
        
        if not node.is_end:
            return False
        
        self._size -= 1
        node.is_end = False
        node.count = 0
        node.data = None
        
        # 清理无用节点（从叶子向根）
        for parent, char in reversed(path):
            child = parent.children[char]
            if not child.is_end and not child.children:
                del parent.children[char]
            else:
                break
        
        return True
    
    def longest_prefix(self, text: str) -> str:
        """
        查找文本中最长匹配的前缀单词
        
        Args:
            text: 输入文本
            
        Returns:
            最长匹配的单词，无匹配返回空字符串
        """
        node = self.root
        longest = ""
        current = ""
        
        for char in text:
            if char not in node.children:
                break
            node = node.children[char]
            current += char
            if node.is_end:
                longest = current
        
        return longest
    
    def contains_prefix(self, prefix: str) -> bool:
        """
        检查是否存在以指定前缀开头的单词
        
        Args:
            prefix: 前缀
            
        Returns:
            是否存在
        """
        return self._find_node(prefix) is not None
    
    def pattern_match(self, pattern: str, wildcard: str = '?') -> List[str]:
        """
        模式匹配（支持通配符）
        
        Args:
            pattern: 模式字符串
            wildcard: 通配符字符，默认'?'
            
        Returns:
            匹配的单词列表
        """
        results = []
        self._pattern_match_recursive(self.root, "", pattern, wildcard, results)
        return results
    
    def _pattern_match_recursive(self, node: TrieNode, current: str, 
                                  pattern: str, wildcard: str, 
                                  results: List[str]) -> None:
        """递归实现模式匹配"""
        if not pattern:
            if node.is_end:
                results.append(current)
            return
        
        char = pattern[0]
        remaining = pattern[1:]
        
        if char == wildcard:
            # 通配符匹配任意字符
            for child_char, child_node in node.children.items():
                self._pattern_match_recursive(child_node, current + child_char, 
                                              remaining, wildcard, results)
        else:
            if char in node.children:
                self._pattern_match_recursive(node.children[char], 
                                             current + char, remaining, 
                                             wildcard, results)
    
    def get_data(self, word: str) -> Optional[Any]:
        """
        获取单词关联的数据
        
        Args:
            word: 单词
            
        Returns:
            关联的数据，不存在返回None
        """
        node = self._find_node(word)
        if node and node.is_end:
            return node.data
        return None
    
    def set_data(self, word: str, data: Any) -> bool:
        """
        设置单词关联的数据
        
        Args:
            word: 单词
            data: 要设置的数据
            
        Returns:
            是否成功
        """
        node = self._find_node(word)
        if node and node.is_end:
            node.data = data
            return True
        return False
    
    def get_count(self, word: str) -> int:
        """
        获取单词的出现次数
        
        Args:
            word: 单词
            
        Returns:
            出现次数，不存在返回0
        """
        node = self._find_node(word)
        if node and node.is_end:
            return node.count
        return 0
    
    def autocomplete(self, prefix: str, max_suggestions: int = 5) -> List[Tuple[str, int]]:
        """
        自动补全，返回建议及其频率
        
        Args:
            prefix: 输入前缀
            max_suggestions: 最大建议数量
            
        Returns:
            (单词, 频率) 元组列表，按频率排序
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        
        results = []
        self._collect_with_count(node, prefix, results)
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_suggestions]
    
    def _collect_with_count(self, node: TrieNode, prefix: str, 
                            results: List[Tuple[str, int]]) -> None:
        """收集单词及其频率"""
        if node.is_end:
            results.append((prefix, node.count))
        
        for char, child in node.children.items():
            self._collect_with_count(child, prefix + char, results)
    
    def all_words(self) -> Iterator[str]:
        """
        迭代所有单词
        
        Yields:
            所有插入的单词
        """
        yield from self._iterate_words(self.root, "")
    
    def _iterate_words(self, node: TrieNode, prefix: str) -> Iterator[str]:
        """递归迭代单词"""
        if node.is_end:
            yield prefix
        
        for char, child in node.children.items():
            yield from self._iterate_words(child, prefix + char)
    
    def suggest_corrections(self, word: str, max_distance: int = 2) -> List[Tuple[str, int]]:
        """
        建议拼写纠正（基于编辑距离）
        
        Args:
            word: 输入单词
            max_distance: 最大编辑距离
            
        Returns:
            (建议词, 编辑距离) 列表
        """
        # 生成所有可能的编辑
        candidates = set()
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        # 原词
        candidates.add(word)
        
        # 删除一个字符
        for i in range(len(word)):
            candidates.add(word[:i] + word[i+1:])
        
        # 替换一个字符
        for i in range(len(word)):
            for c in alphabet:
                candidates.add(word[:i] + c + word[i+1:])
        
        # 插入一个字符
        for i in range(len(word) + 1):
            for c in alphabet:
                candidates.add(word[:i] + c + word[i:])
        
        # 交换相邻字符
        for i in range(len(word) - 1):
            candidates.add(word[:i] + word[i+1] + word[i] + word[i+2:])
        
        # 在Trie中查找并计算编辑距离
        results = []
        for candidate in candidates:
            if self.search(candidate):
                dist = self._edit_distance(word, candidate)
                if dist <= max_distance:
                    results.append((candidate, dist))
        
        results.sort(key=lambda x: x[1])
        return results
    
    def _edit_distance(self, s1: str, s2: str) -> int:
        """计算编辑距离（Levenshtein距离）"""
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        
        if len(s2) == 0:
            return len(s1)
        
        prev_row = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        
        return prev_row[-1]
    
    def word_exists_with_path(self, word: str) -> Tuple[bool, List[str]]:
        """
        检查单词是否存在，并返回路径
        
        Args:
            word: 要检查的单词
            
        Returns:
            (是否存在, 路径节点列表)
        """
        path = []
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False, path
            node = node.children[char]
            path.append(char)
        
        return node.is_end, path
    
    def count_words_with_prefix(self, prefix: str) -> int:
        """
        统计以指定前缀开头的单词数量
        
        Args:
            prefix: 前缀
            
        Returns:
            单词数量
        """
        node = self._find_node(prefix)
        if node is None:
            return 0
        
        return self._count_words(node)
    
    def _count_words(self, node: TrieNode) -> int:
        """递归统计节点下的单词数"""
        count = 1 if node.is_end else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count
    
    def to_dict(self) -> Dict:
        """
        将Trie序列化为字典
        
        Returns:
            序列化后的字典
        """
        return {
            'root': self._node_to_dict(self.root),
            'size': self._size,
            'total_chars': self._total_chars
        }
    
    def _node_to_dict(self, node: TrieNode) -> Dict:
        """将节点转换为字典"""
        result = {
            'is_end': node.is_end,
            'count': node.count,
        }
        if node.data is not None:
            result['data'] = node.data
        if node.children:
            result['children'] = {
                char: self._node_to_dict(child) 
                for char, child in node.children.items()
            }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Trie':
        """
        从字典反序列化Trie
        
        Args:
            data: 序列化的字典
            
        Returns:
            Trie实例
        """
        trie = cls()
        if 'root' in data:
            trie.root = trie._dict_to_node(data['root'])
        if 'size' in data:
            trie._size = data['size']
        if 'total_chars' in data:
            trie._total_chars = data['total_chars']
        return trie
    
    def _dict_to_node(self, data: Dict) -> TrieNode:
        """从字典创建节点"""
        node = TrieNode()
        node.is_end = data.get('is_end', False)
        node.count = data.get('count', 0)
        node.data = data.get('data')
        
        if 'children' in data:
            for char, child_data in data['children'].items():
                node.children[char] = self._dict_to_node(child_data)
        
        return node
    
    def to_json(self, indent: int = 2) -> str:
        """
        导出为JSON字符串
        
        Args:
            indent: 缩进空格数
            
        Returns:
            JSON字符串
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Trie':
        """
        从JSON字符串加载
        
        Args:
            json_str: JSON字符串
            
        Returns:
            Trie实例
        """
        return cls.from_dict(json.loads(json_str))
    
    def size(self) -> int:
        """返回Trie中的单词数量"""
        return self._size
    
    def is_empty(self) -> bool:
        """检查Trie是否为空"""
        return self._size == 0
    
    def clear(self) -> None:
        """清空Trie"""
        self.root = TrieNode()
        self._size = 0
        self._total_chars = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, word: str) -> bool:
        return self.search(word)
    
    def __iter__(self) -> Iterator[str]:
        return self.all_words()
    
    def __repr__(self) -> str:
        return f"Trie(size={self._size}, nodes≈{self._total_chars})"


class SuffixTrie:
    """
    后缀树（简化实现）
    
    用于子串匹配、最长重复子串等问题
    """
    
    def __init__(self):
        self.trie = Trie()
    
    def build_from_string(self, text: str) -> None:
        """
        从字符串构建后缀树
        
        Args:
            text: 输入字符串
        """
        self.trie.clear()
        for i in range(len(text)):
            self.trie.insert(text[i:])
    
    def contains_substring(self, pattern: str) -> bool:
        """
        检查是否包含子串
        
        Args:
            pattern: 要查找的子串
            
        Returns:
            是否包含
        """
        return self.trie.contains_prefix(pattern)
    
    def find_all_occurrences(self, pattern: str) -> List[int]:
        """
        查找所有出现位置
        
        Args:
            pattern: 要查找的子串
            
        Returns:
            起始位置列表
        """
        if not self.trie.contains_prefix(pattern):
            return []
        
        # 获取所有以pattern开头的后缀
        suffixes = self.trie.starts_with(pattern, limit=10000)
        
        # 从原始后缀长度反推位置
        positions = []
        original_length = max(len(s) for s in suffixes) if suffixes else 0
        
        for suffix in suffixes:
            pos = original_length - len(suffix)
            positions.append(pos)
        
        return sorted(positions)


class PrefixSet:
    """
    前缀集合
    
    高效的前缀匹配集合，适用于大量字符串的前缀检测
    """
    
    def __init__(self):
        self.trie = Trie()
    
    def add(self, prefix: str) -> None:
        """添加前缀"""
        self.trie.insert(prefix)
    
    def update(self, prefixes: List[str]) -> None:
        """批量添加前缀"""
        for prefix in prefixes:
            self.trie.insert(prefix)
    
    def matches_any_prefix(self, text: str) -> bool:
        """
        检查文本是否以集合中任一前缀开头
        
        Args:
            text: 输入文本
            
        Returns:
            是否匹配
        """
        return bool(self.trie.longest_prefix(text))
    
    def get_matching_prefix(self, text: str) -> Optional[str]:
        """
        获取匹配的最长前缀
        
        Args:
            text: 输入文本
            
        Returns:
            匹配的前缀，无匹配返回None
        """
        result = self.trie.longest_prefix(text)
        return result if result else None
    
    def __contains__(self, prefix: str) -> bool:
        return prefix in self.trie
    
    def __len__(self) -> int:
        return len(self.trie)


# 便捷函数
def build_trie(words: List[str]) -> Trie:
    """
    从单词列表构建Trie
    
    Args:
        words: 单词列表
        
    Returns:
        构建好的Trie
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
        最长公共前缀
    """
    if not words:
        return ""
    
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix


def word_frequency_analysis(words: List[str]) -> Dict[str, int]:
    """
    分析单词频率并返回排序结果
    
    Args:
        words: 单词列表
        
    Returns:
        {单词: 频率} 字典
    """
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    result = {}
    for word in trie:
        result[word] = trie.get_count(word)
    
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


if __name__ == "__main__":
    # 简单演示
    print("=== Trie 工具模块演示 ===\n")
    
    # 创建Trie并插入单词
    trie = Trie()
    words = ["hello", "help", "helper", "helicopter", "helium", 
             "world", "word", "work", "worker"]
    
    for word in words:
        trie.insert(word)
    
    print(f"Trie大小: {trie.size()} 个单词")
    
    # 搜索演示
    print(f"\n搜索 'hello': {trie.search('hello')}")
    print(f"搜索 'hel': {trie.search('hel')}")
    
    # 前缀搜索
    print(f"\n以 'hel' 开头的单词: {trie.starts_with('hel')}")
    print(f"以 'wor' 开头的单词: {trie.starts_with('wor')}")
    
    # 自动补全
    trie.insert("hello", data={"meaning": "打招呼"})
    print(f"\n自动补全 'hel': {trie.autocomplete('hel')}")
    
    # 模式匹配
    print(f"\n模式匹配 'h?lp': {trie.pattern_match('h?lp')}")
    
    # 最长前缀
    print(f"\n'helperworld' 的最长前缀: {trie.longest_prefix('helperworld')}")
    
    # 拼写建议
    print(f"\n'helo' 的纠正建议: {trie.suggest_corrections('helo')}")
    
    print("\n=== 演示完成 ===")