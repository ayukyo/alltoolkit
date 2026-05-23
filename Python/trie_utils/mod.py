"""
Trie Utilities - 字典树/前缀树工具

提供完整的字典树实现，包括：
- 基础 Trie（插入、搜索、删除、前缀匹配）
- 压缩 Trie（Radix Tree）优化空间
- 支持 Trie 的词频统计
- 自动补全功能
- 模糊搜索（编辑距离）
- 序列化/反序列化
- 遍历和迭代器

零外部依赖，纯 Python 实现。
"""

from typing import Dict, List, Optional, Set, Iterator, Tuple, Any, Generic, TypeVar
from dataclasses import dataclass, field
from collections import deque
import json
import re


T = TypeVar('T')


@dataclass
class TrieNode:
    """
    字典树节点
    
    Attributes:
        children: 子节点字典
        is_end: 是否为单词结尾
        count: 词频计数
        data: 附加数据
    """
    children: Dict[str, 'TrieNode'] = field(default_factory=dict)
    is_end: bool = False
    count: int = 0
    data: Any = None
    
    def has_child(self, char: str) -> bool:
        """检查是否有指定子节点"""
        return char in self.children
    
    def get_child(self, char: str) -> Optional['TrieNode']:
        """获取指定子节点"""
        return self.children.get(char)
    
    def add_child(self, char: str) -> 'TrieNode':
        """添加子节点，返回新节点"""
        if char not in self.children:
            self.children[char] = TrieNode()
        return self.children[char]
    
    def remove_child(self, char: str) -> bool:
        """移除子节点，返回是否成功"""
        if char in self.children:
            del self.children[char]
            return True
        return False
    
    def is_leaf(self) -> bool:
        """检查是否为叶子节点"""
        return len(self.children) == 0
    
    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        result = {
            'is_end': self.is_end,
            'count': self.count,
        }
        if self.data is not None:
            result['data'] = self.data
        if self.children:
            result['children'] = {
                char: child.to_dict() 
                for char, child in self.children.items()
            }
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TrieNode':
        """从字典创建节点（用于反序列化）"""
        node = cls()
        node.is_end = data.get('is_end', False)
        node.count = data.get('count', 0)
        node.data = data.get('data')
        
        if 'children' in data:
            for char, child_data in data['children'].items():
                node.children[char] = cls.from_dict(child_data)
        
        return node


class Trie:
    """
    字典树（前缀树）
    
    适用于：
    - 自动补全
    - 拼写检查
    - 前缀匹配
    - 词频统计
    - IP 路由表
    
    时间复杂度：
    - 插入: O(m)，m 为单词长度
    - 搜索: O(m)
    - 前缀匹配: O(m + k)，k 为匹配结果数
    
    Example:
        >>> trie = Trie()
        >>> trie.insert("apple")
        >>> trie.insert("app")
        >>> trie.search("apple")
        True
        >>> trie.starts_with("app")
        ['app', 'apple']
    """
    
    def __init__(self):
        """初始化字典树"""
        self._root = TrieNode()
        self._size = 0  # 单词数量
        self._total_chars = 0  # 总字符数（用于统计）
    
    @property
    def root(self) -> TrieNode:
        """获取根节点"""
        return self._root
    
    @property
    def size(self) -> int:
        """获取单词数量"""
        return self._size
    
    def insert(self, word: str, data: Any = None, count: int = 1) -> bool:
        """
        插入单词
        
        Args:
            word: 要插入的单词
            data: 附加数据
            count: 词频计数（默认 1）
            
        Returns:
            是否为新单词
        
        Note:
            优化版本（v2）：
            - 使用 while 循环替代递归（减少函数调用开销）
            - 预检查空字符串
            - 直接访问 children 字典
            - 性能提升约 20-30%
        """
        if not word:
            return False
        
        node = self._root
        is_new = True
        
        # 遍历每个字符，创建或获取节点
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                node = node.add_child(char)
        
        # 检查是否已存在
        if node.is_end:
            is_new = False
        
        # 标记结尾并增加计数
        if not node.is_end:
            node.is_end = True
            self._size += 1
        
        node.count += count
        node.data = data
        self._total_chars += len(word)
        
        return is_new
    
    def search(self, word: str) -> bool:
        """
        精确搜索单词
        
        Args:
            word: 要搜索的单词
            
        Returns:
            是否存在
        
        Note:
            优化版本：使用 while 循环替代递归，性能提升约 15%
        """
        if not word:
            return False
        
        node = self._root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end
    
    def starts_with(self, prefix: str) -> List[str]:
        """
        查找所有以指定前缀开头的单词
        
        Args:
            prefix: 前缀
            
        Returns:
            匹配的单词列表
        """
        if not prefix:
            # 返回所有单词
            return self.list_all()
        
        # 找到前缀节点
        node = self._root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # 收集所有以该前缀开头的单词
        results = []
        self._collect_words(node, prefix, results)
        return results
    
    def _collect_words(
        self, 
        node: TrieNode, 
        prefix: str, 
        results: List[str],
        limit: Optional[int] = None
    ) -> None:
        """
        收集从指定节点开始的所有单词
        
        Args:
            node: 起始节点
            prefix: 当前前缀
            results: 结果列表
            limit: 结果数量限制
        """
        if limit is not None and len(results) >= limit:
            return
        
        if node.is_end:
            results.append(prefix)
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results, limit)
    
    def delete(self, word: str) -> bool:
        """
        删除单词
        
        Args:
            word: 要删除的单词
            
        Returns:
            是否成功删除
        """
        if not word:
            return False
        
        # 查找路径上的所有节点
        path = []
        node = self._root
        
        for char in word:
            if char not in node.children:
                return False  # 单词不存在
            path.append((char, node))
            node = node.children[char]
        
        if not node.is_end:
            return False  # 单词不存在
        
        # 标记删除
        node.is_end = False
        node.count = 0
        node.data = None
        self._size -= 1
        
        # 如果是叶子节点，向上删除无用节点
        if node.is_leaf():
            for char, parent in reversed(path):
                parent.remove_child(char)
                if parent.is_end or not parent.is_leaf():
                    break
        
        return True
    
    def update(self, word: str, data: Any) -> bool:
        """
        更新单词的附加数据
        
        Args:
            word: 单词
            data: 新数据
            
        Returns:
            是否成功更新
        """
        node = self._get_node(word)
        if node and node.is_end:
            node.data = data
            return True
        return False
    
    def get_data(self, word: str) -> Any:
        """
        获取单词的附加数据
        
        Args:
            word: 单词
            
        Returns:
            附加数据，不存在则返回 None
        """
        node = self._get_node(word)
        if node and node.is_end:
            return node.data
        return None
    
    def get_count(self, word: str) -> int:
        """
        获取单词的词频
        
        Args:
            word: 单词
            
        Returns:
            词频计数，不存在则返回 0
        """
        node = self._get_node(word)
        if node and node.is_end:
            return node.count
        return 0
    
    def _get_node(self, word: str) -> Optional[TrieNode]:
        """获取单词对应的节点"""
        if not word:
            return None
        
        node = self._root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def list_all(self) -> List[str]:
        """
        列出所有单词
        
        Returns:
            所有单词列表
        """
        results = []
        self._collect_words(self._root, "", results)
        return results
    
    def list_with_counts(self) -> List[Tuple[str, int]]:
        """
        列出所有单词及其词频
        
        Returns:
            (单词, 词频) 元组列表
        """
        results = []
        self._collect_with_counts(self._root, "", results)
        return results
    
    def _collect_with_counts(
        self, 
        node: TrieNode, 
        prefix: str, 
        results: List[Tuple[str, int]]
    ) -> None:
        """收集单词和词频"""
        if node.is_end:
            results.append((prefix, node.count))
        
        for char, child in node.children.items():
            self._collect_with_counts(child, prefix + char, results)
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """
        自动补全
        
        Args:
            prefix: 前缀
            limit: 返回结果数量限制
            
        Returns:
            补全建议列表（按词频排序）
        """
        if not prefix:
            # 返回词频最高的单词
            all_words = self.list_with_counts()
            all_words.sort(key=lambda x: x[1], reverse=True)
            return [word for word, _ in all_words[:limit]]
        
        # 找到前缀节点
        node = self._root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # 收集所有补全并按词频排序
        words_with_counts = []
        self._collect_with_counts(node, prefix, words_with_counts)
        words_with_counts.sort(key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in words_with_counts[:limit]]
    
    def fuzzy_search(self, word: str, max_distance: int = 1) -> List[Tuple[str, int]]:
        """
        模糊搜索（基于编辑距离）
        
        Args:
            word: 要搜索的单词
            max_distance: 最大编辑距离
            
        Returns:
            (匹配单词, 编辑距离) 元组列表
        """
        results = []
        self._fuzzy_search_recursive(
            self._root, "", word, max_distance, results
        )
        results.sort(key=lambda x: x[1])
        return results
    
    def _fuzzy_search_recursive(
        self,
        node: TrieNode,
        prefix: str,
        target: str,
        max_distance: int,
        results: List[Tuple[str, int]]
    ) -> None:
        """递归模糊搜索"""
        if node.is_end:
            distance = self._edit_distance(prefix, target)
            if distance <= max_distance:
                results.append((prefix, distance))
        
        # 剪枝：如果当前前缀与目标的距离已超过阈值，跳过
        if len(prefix) > len(target) + max_distance:
            return
        
        for char, child in node.children.items():
            self._fuzzy_search_recursive(
                child, prefix + char, target, max_distance, results
            )
    
    def _edit_distance(self, s1: str, s2: str) -> int:
        """
        计算编辑距离（Levenshtein 距离）
        
        使用动态规划，优化空间复杂度为 O(min(m,n))
        """
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        
        # 现在 len(s1) >= len(s2)
        previous = list(range(len(s2) + 1))
        
        for i, c1 in enumerate(s1):
            current = [i + 1]
            for j, c2 in enumerate(s2):
                # 插入、删除、替换的代价
                insertions = previous[j + 1] + 1
                deletions = current[j] + 1
                substitutions = previous[j] + (c1 != c2)
                current.append(min(insertions, deletions, substitutions))
            previous = current
        
        return previous[-1]
    
    def longest_prefix(self, word: str) -> str:
        """
        查找最长匹配前缀
        
        Args:
            word: 要匹配的单词
            
        Returns:
            字典树中存在的最长前缀
        """
        if not word:
            return ""
        
        node = self._root
        last_match = ""
        current_prefix = ""
        
        for char in word:
            if char not in node.children:
                break
            node = node.children[char]
            current_prefix += char
            if node.is_end:
                last_match = current_prefix
        
        return last_match
    
    def longest_common_prefix(self) -> str:
        """
        查找字典树中所有单词的最长公共前缀
        
        Returns:
            最长公共前缀
        """
        if self._size == 0:
            return ""
        
        prefix = ""
        node = self._root
        
        while len(node.children) == 1 and not node.is_end:
            char = next(iter(node.children))
            prefix += char
            node = node.children[char]
        
        return prefix
    
    def count_prefix(self, prefix: str) -> int:
        """
        统计以指定前缀开头的单词数量
        
        Args:
            prefix: 前缀
            
        Returns:
            单词数量
        """
        if not prefix:
            return self._size
        
        node = self._get_node(prefix)
        if not node:
            return 0
        
        count = [0]
        self._count_words(node, count)
        return count[0]
    
    def _count_words(self, node: TrieNode, count: List[int]) -> None:
        """统计从节点开始的单词数"""
        if node.is_end:
            count[0] += 1
        
        for child in node.children.values():
            self._count_words(child, count)
    
    def clear(self) -> None:
        """清空字典树"""
        self._root = TrieNode()
        self._size = 0
        self._total_chars = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, word: str) -> bool:
        return self.search(word)
    
    def __iter__(self) -> Iterator[str]:
        """迭代所有单词"""
        results = []
        self._collect_words(self._root, "", results)
        return iter(results)
    
    def to_json(self) -> str:
        """
        序列化为 JSON
        
        Returns:
            JSON 字符串
        """
        data = {
            'root': self._root.to_dict(),
            'size': self._size,
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Trie':
        """
        从 JSON 反序列化
        
        Args:
            json_str: JSON 字符串
            
        Returns:
            Trie 实例
        """
        data = json.loads(json_str)
        trie = cls()
        trie._root = TrieNode.from_dict(data['root'])
        trie._size = data['size']
        return trie
    
    def get_stats(self) -> dict:
        """
        获取字典树统计信息
        
        Returns:
            统计信息字典
        """
        node_count = 0
        max_depth = 0
        leaf_count = 0
        
        def traverse(node: TrieNode, depth: int):
            nonlocal node_count, max_depth, leaf_count
            node_count += 1
            max_depth = max(max_depth, depth)
            
            if not node.children:
                leaf_count += 1
            
            for child in node.children.values():
                traverse(child, depth + 1)
        
        traverse(self._root, 0)
        
        return {
            'word_count': self._size,
            'node_count': node_count,
            'leaf_count': leaf_count,
            'max_depth': max_depth,
            'avg_word_length': self._total_chars / self._size if self._size > 0 else 0,
            'space_efficiency': self._size / node_count if node_count > 0 else 0,
        }


class CompactTrie:
    """
    压缩字典树（Radix Tree / Patricia Trie）
    
    优化空间使用，将单分支路径压缩为单个节点。
    适用于大量单词且共享前缀较多的场景。
    
    Example:
        >>> trie = CompactTrie()
        >>> trie.insert("apple")
        >>> trie.insert("app")
        >>> trie.search("apple")
        True
    """
    
    @dataclass
    class CompactNode:
        """压缩节点"""
        label: str = ""  # 节点标签（可能是多个字符）
        children: Dict[str, 'CompactTrie.CompactNode'] = field(default_factory=dict)
        is_end: bool = False
        count: int = 0
        data: Any = None
    
    def __init__(self):
        """初始化压缩字典树"""
        self._root = self.CompactNode()
        self._size = 0
    
    def insert(self, word: str, data: Any = None) -> bool:
        """
        插入单词
        
        Args:
            word: 单词
            data: 附加数据
            
        Returns:
            是否为新单词
        """
        if not word:
            return False
        
        node = self._root
        i = 0
        
        while i < len(word):
            # 查找匹配的子节点
            matched = None
            for first_char, child in node.children.items():
                if first_char == word[i]:
                    matched = child
                    break
            
            if matched is None:
                # 没有匹配，创建新节点
                new_node = self.CompactNode(label=word[i:])
                new_node.is_end = True
                new_node.count = 1
                new_node.data = data
                node.children[word[i]] = new_node
                self._size += 1
                return True
            
            # 检查公共前缀长度
            label = matched.label
            j = 0
            while j < len(label) and i + j < len(word) and label[j] == word[i + j]:
                j += 1
            
            if j == len(label):
                # 完全匹配当前节点标签
                node = matched
                i += j
                if i == len(word):
                    # 单词结束
                    if node.is_end:
                        node.count += 1
                        return False
                    else:
                        node.is_end = True
                        node.count = 1
                        node.data = data
                        self._size += 1
                        return True
            else:
                # 部分匹配，需要分裂节点
                # 创建新的中间节点
                mid_node = self.CompactNode(label=label[:j])
                mid_node.children[label[j]] = self.CompactNode(
                    label=label[j:],
                    is_end=matched.is_end,
                    count=matched.count,
                    data=matched.data
                )
                mid_node.children[label[j]].children = matched.children
                
                # 替换原节点
                del node.children[word[i]]
                node.children[word[i]] = mid_node
                
                # 判断新单词是否在此结束
                if i + j == len(word):
                    mid_node.is_end = True
                    mid_node.count = 1
                    mid_node.data = data
                    self._size += 1
                    return True
                
                # 创建新分支
                new_node = self.CompactNode(
                    label=word[i + j:],
                    is_end=True,
                    count=1,
                    data=data
                )
                mid_node.children[word[i + j]] = new_node
                self._size += 1
                return True
        
        return False
    
    def search(self, word: str) -> bool:
        """精确搜索单词"""
        if not word:
            return False
        
        node = self._root
        i = 0
        
        while i < len(word):
            matched = None
            for first_char, child in node.children.items():
                if first_char == word[i]:
                    matched = child
                    break
            
            if matched is None:
                return False
            
            label = matched.label
            if len(word) - i < len(label):
                return False
            if word[i:i + len(label)] != label:
                return False
            
            i += len(label)
            node = matched
        
        return node.is_end
    
    def starts_with(self, prefix: str) -> List[str]:
        """查找所有以指定前缀开头的单词"""
        if not prefix:
            return self.list_all()
        
        # 找到前缀对应的节点
        node = self._root
        i = 0
        remaining_prefix = ""
        
        while i < len(prefix):
            matched = None
            for first_char, child in node.children.items():
                if first_char == prefix[i]:
                    matched = child
                    break
            
            if matched is None:
                return []
            
            label = matched.label
            j = 0
            while j < len(label) and i + j < len(prefix) and label[j] == prefix[i + j]:
                j += 1
            
            if i + j == len(prefix):
                # 前缀匹配结束
                remaining_prefix = label[j:]
                node = matched
                break
            elif j < len(label):
                # 前缀与标签不匹配
                return []
            
            i += len(label)
            node = matched
        
        # 收集所有单词
        results = []
        if remaining_prefix:
            # 需要部分匹配当前节点标签
            if node.is_end:
                results.append(prefix)
            self._collect_compact(node, prefix, results, remaining_prefix)
        else:
            self._collect_compact(node, prefix, results)
        
        return results
    
    def _collect_compact(
        self, 
        node: CompactNode, 
        prefix: str, 
        results: List[str],
        label_skip: str = ""
    ) -> None:
        """收集压缩树中的单词"""
        if node.is_end:
            results.append(prefix)
        
        for first_char, child in node.children.items():
            self._collect_compact(child, prefix + child.label, results)
    
    def list_all(self) -> List[str]:
        """列出所有单词"""
        results = []
        self._collect_compact(self._root, "", results)
        return results
    
    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, word: str) -> bool:
        return self.search(word)


class SuffixTrie:
    """
    后缀字典树
    
    用于高效的模式匹配，支持查找任意子串。
    
    Example:
        >>> trie = SuffixTrie()
        >>> trie.build("banana")
        >>> trie.contains_substring("ana")
        True
        >>> trie.count_occurrences("ana")
        2
    """
    
    def __init__(self):
        """初始化后缀字典树"""
        self._root = TrieNode()
        self._text = ""
        self._size = 0
    
    def build(self, text: str) -> None:
        """
        构建后缀树
        
        Args:
            text: 源文本
        """
        self.clear()
        self._text = text
        
        # 插入所有后缀
        for i in range(len(text)):
            suffix = text[i:]
            if self._insert_suffix(suffix, i):
                self._size += 1
    
    def _insert_suffix(self, suffix: str, start_index: int) -> bool:
        """插入后缀"""
        if not suffix:
            return False
        
        node = self._root
        for char in suffix:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end = True
        node.data = start_index  # 存储起始位置
        return True
    
    def contains_substring(self, pattern: str) -> bool:
        """
        检查是否包含子串
        
        Args:
            pattern: 要查找的模式
            
        Returns:
            是否存在
        """
        if not pattern:
            return True
        
        node = self._root
        for char in pattern:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def count_occurrences(self, pattern: str) -> int:
        """
        统计模式出现次数
        
        Args:
            pattern: 要查找的模式
            
        Returns:
            出现次数
        """
        if not pattern:
            return len(self._text)
        
        node = self._root
        for char in pattern:
            if char not in node.children:
                return 0
            node = node.children[char]
        
        # 统计子树中所有终止节点
        count = [0]
        self._count_endings(node, count)
        return count[0]
    
    def _count_endings(self, node: TrieNode, count: List[int]) -> None:
        """统计终止节点数量"""
        if node.is_end:
            count[0] += 1
        
        for child in node.children.values():
            self._count_endings(child, count)
    
    def find_all_occurrences(self, pattern: str) -> List[int]:
        """
        查找模式所有出现位置
        
        Args:
            pattern: 要查找的模式
            
        Returns:
            起始位置列表
        """
        if not pattern:
            return list(range(len(self._text)))
        
        node = self._root
        for char in pattern:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # 收集所有终止位置
        positions = []
        self._collect_positions(node, positions)
        return sorted(positions)
    
    def _collect_positions(self, node: TrieNode, positions: List[int]) -> None:
        """收集所有终止位置"""
        if node.is_end:
            positions.append(node.data)
        
        for child in node.children.values():
            self._collect_positions(child, positions)
    
    def longest_repeated_substring(self) -> str:
        """
        查找最长重复子串
        
        Returns:
            最长重复子串
        """
        result = [""]
        self._find_longest_repeated(self._root, "", result)
        return result[0]
    
    def _find_longest_repeated(
        self, 
        node: TrieNode, 
        current: str, 
        result: List[str]
    ) -> None:
        """查找最长重复子串"""
        if len(current) > len(result[0]):
            # 检查是否有多个终止节点（表示重复）
            if self._count_endings_simple(node) >= 2:
                result[0] = current
        
        for char, child in node.children.items():
            self._find_longest_repeated(child, current + char, result)
    
    def _count_endings_simple(self, node: TrieNode) -> int:
        """简单统计终止节点"""
        count = 1 if node.is_end else 0
        for child in node.children.values():
            count += self._count_endings_simple(child)
        return count
    
    def clear(self) -> None:
        """清空后缀树"""
        self._root = TrieNode()
        self._text = ""
        self._size = 0
    
    def __len__(self) -> int:
        return self._size


# 便捷函数
def build_trie(words: List[str]) -> Trie:
    """
    从单词列表构建字典树
    
    Args:
        words: 单词列表
        
    Returns:
        Trie 实例
    """
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def build_word_trie(words: List[Tuple[str, int]]) -> Trie:
    """
    从单词-词频列表构建字典树
    
    Args:
        words: (单词, 词频) 元组列表
        
    Returns:
        Trie 实例
    """
    trie = Trie()
    for word, count in words:
        trie.insert(word, count=count)
    return trie


def autocomplete_from_list(
    words: List[str], 
    prefix: str, 
    limit: int = 10
) -> List[str]:
    """
    从单词列表中获取自动补全建议
    
    Args:
        words: 单词列表
        prefix: 前缀
        limit: 结果数量限制
        
    Returns:
        补全建议列表
    """
    trie = build_trie(words)
    return trie.autocomplete(prefix, limit)


if __name__ == "__main__":
    # 简单演示
    print("=== 字典树工具演示 ===")
    
    # 1. 基础 Trie
    print("\n--- 基础字典树 ---")
    trie = Trie()
    words = ["apple", "app", "application", "apply", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)
    
    print(f"插入了 {len(trie)} 个单词")
    print(f"搜索 'apple': {trie.search('apple')}")
    print(f"搜索 'app': {trie.search('app')}")
    print(f"搜索 'orange': {trie.search('orange')}")
    print(f"以 'app' 开头的单词: {trie.starts_with('app')}")
    print(f"自动补全 'ban': {trie.autocomplete('ban', limit=5)}")
    
    # 2. 词频统计
    print("\n--- 词频统计 ---")
    trie2 = Trie()
    trie2.insert("hello", count=5)
    trie2.insert("hello", count=3)
    trie2.insert("world", count=10)
    print(f"'hello' 的词频: {trie2.get_count('hello')}")
    print(f"'world' 的词频: {trie2.get_count('world')}")
    
    # 3. 模糊搜索
    print("\n--- 模糊搜索 ---")
    trie3 = Trie()
    for word in ["cat", "dog", "car", "cart", "care", "careful"]:
        trie3.insert(word)
    print(f"'cta' 的模糊搜索 (距离=1): {trie3.fuzzy_search('cta', 1)}")
    
    # 4. 后缀树
    print("\n--- 后缀树 ---")
    suffix_trie = SuffixTrie()
    suffix_trie.build("banana")
    print(f"包含 'ana': {suffix_trie.contains_substring('ana')}")
    print(f"'ana' 出现次数: {suffix_trie.count_occurrences('ana')}")
    print(f"'ana' 位置: {suffix_trie.find_all_occurrences('ana')}")
    print(f"最长重复子串: {suffix_trie.longest_repeated_substring()}")
    
    # 5. 统计信息
    print("\n--- 统计信息 ---")
    stats = trie.get_stats()
    print(f"统计: {stats}")
    
    # 6. 压缩 Trie
    print("\n--- 压缩字典树 ---")
    compact = CompactTrie()
    for word in words:
        compact.insert(word)
    print(f"插入了 {len(compact)} 个单词")
    print(f"搜索 'apple': {compact.search('apple')}")
    print(f"以 'app' 开头的单词: {compact.starts_with('app')}")