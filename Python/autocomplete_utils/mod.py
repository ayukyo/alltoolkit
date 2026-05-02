"""
自动补全工具模块
Autocomplete Utilities

提供完整的自动补全实现，包括：
- 基于 Trie 的前缀匹配
- 模糊搜索（编辑距离）
- 权重排序（频率/热度）
- 多语言支持
- 持久化支持

零外部依赖，仅使用 Python 标准库
"""

from typing import List, Optional, Dict, Tuple, Set, Iterator, Any
from dataclasses import dataclass, field
from collections import deque
import json
import re


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class Suggestion:
    """补全建议"""
    text: str                    # 建议文本
    score: float = 1.0          # 相关性得分
    frequency: int = 0          # 使用频率
    metadata: Dict = field(default_factory=dict)  # 额外元数据
    
    def __repr__(self) -> str:
        return f"Suggestion(text='{self.text}', score={self.score:.2f}, freq={self.frequency})"


@dataclass
class TrieNode:
    """Trie 节点"""
    children: Dict[str, 'TrieNode'] = field(default_factory=dict)
    is_word: bool = False
    frequency: int = 0
    metadata: Dict = field(default_factory=dict)


# ============================================================================
# Trie 自动补全器
# ============================================================================

class TrieAutocomplete:
    """
    基于 Trie 的自动补全器
    
    支持：
    - 前缀匹配
    - 按频率/权重排序
    - 模糊搜索
    - 持久化
    
    Args:
        case_sensitive: 是否区分大小写（默认 False）
        max_suggestions: 最大建议数量（默认 10）
    """
    
    def __init__(self, case_sensitive: bool = False, max_suggestions: int = 10):
        self.case_sensitive = case_sensitive
        self.max_suggestions = max_suggestions
        self.root = TrieNode()
        self._word_count = 0
    
    def _normalize(self, word: str) -> str:
        """标准化单词"""
        return word if self.case_sensitive else word.lower()
    
    # ========================================================================
    # 基础操作
    # ========================================================================
    
    def insert(
        self, 
        word: str, 
        frequency: int = 1, 
        metadata: Optional[Dict] = None
    ) -> None:
        """
        插入单词
        
        Args:
            word: 要插入的单词
            frequency: 使用频率（默认 1）
            metadata: 额外元数据
        """
        if not word:
            return
        
        node = self.root
        normalized = self._normalize(word)
        
        for char in normalized:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_word:
            self._word_count += 1
        
        node.is_word = True
        node.frequency += frequency
        if metadata:
            node.metadata.update(metadata)
    
    def insert_batch(
        self, 
        words: List[str], 
        frequencies: Optional[List[int]] = None,
        metadata_list: Optional[List[Dict]] = None
    ) -> None:
        """批量插入单词"""
        for i, word in enumerate(words):
            freq = frequencies[i] if frequencies else 1
            meta = metadata_list[i] if metadata_list and i < len(metadata_list) else None
            self.insert(word, freq, meta)
    
    def contains(self, word: str) -> bool:
        """检查单词是否存在"""
        node = self._find_node(word)
        return node is not None and node.is_word
    
    def remove(self, word: str) -> bool:
        """删除单词（保留节点结构）"""
        node = self._find_node(word)
        if node is None or not node.is_word:
            return False
        
        node.is_word = False
        node.frequency = 0
        node.metadata = {}
        self._word_count -= 1
        return True
    
    def clear(self) -> None:
        """清空所有单词"""
        self.root = TrieNode()
        self._word_count = 0
    
    # ========================================================================
    # 查询操作
    # ========================================================================
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """找到前缀对应的节点"""
        node = self.root
        normalized = self._normalize(prefix)
        
        for char in normalized:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def search(self, prefix: str) -> List[Suggestion]:
        """
        前缀搜索
        
        Args:
            prefix: 搜索前缀
            
        Returns:
            匹配的补全建议列表
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        
        suggestions = []
        self._collect_suggestions(node, prefix, suggestions)
        
        # 按频率和得分排序
        suggestions.sort(key=lambda s: (-s.frequency, -s.score, s.text))
        return suggestions[:self.max_suggestions]
    
    def _collect_suggestions(
        self, 
        node: TrieNode, 
        prefix: str, 
        suggestions: List[Suggestion]
    ) -> None:
        """收集所有补全建议"""
        if node.is_word:
            suggestions.append(Suggestion(
                text=prefix,
                score=1.0,
                frequency=node.frequency,
                metadata=node.metadata.copy()
            ))
        
        for char, child in node.children.items():
            self._collect_suggestions(child, prefix + char, suggestions)
    
    def fuzzy_search(
        self, 
        query: str, 
        max_distance: int = 2
    ) -> List[Suggestion]:
        """
        模糊搜索（编辑距离）
        
        Args:
            query: 查询字符串
            max_distance: 最大编辑距离
            
        Returns:
            匹配的补全建议列表
        """
        suggestions = []
        query_normalized = self._normalize(query)
        
        if not query_normalized:
            return self.search("")
        
        # 初始行：编辑距离表的第一行（空前缀）
        initial_row = list(range(len(query_normalized) + 1))
        
        # 使用动态规划进行模糊匹配
        self._fuzzy_search_recursive(
            self.root, "", query_normalized, 
            initial_row,
            max_distance, suggestions
        )
        
        # 按编辑距离和频率排序
        suggestions.sort(key=lambda s: (-s.score, -s.frequency, s.text))
        return suggestions[:self.max_suggestions]
    
    def _fuzzy_search_recursive(
        self,
        node: TrieNode,
        prefix: str,
        query: str,
        prev_row: List[int],
        max_distance: int,
        suggestions: List[Suggestion]
    ) -> None:
        """递归模糊搜索"""
        # 构建当前行
        current_row = [prev_row[0] + 1]  # 第一个元素：上一行第一个 + 1
        
        for i in range(len(query)):
            # 计算三个可能的操作
            insert_cost = current_row[i] + 1
            delete_cost = prev_row[i + 1] + 1
            replace_cost = prev_row[i] + (0 if (prefix and prefix[-1] == query[i]) else 1)
            
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        
        # 检查当前节点是否是单词，且编辑距离在范围内
        if node.is_word and current_row[-1] <= max_distance:
            distance = current_row[-1]
            score = 1.0 - (distance / max(len(query), len(prefix)))
            suggestions.append(Suggestion(
                text=prefix,
                score=score,
                frequency=node.frequency,
                metadata=node.metadata.copy() if node.metadata else {}
            ))
        
        # 如果当前行的最小值 <= max_distance，继续搜索子节点
        if min(current_row) <= max_distance:
            for char, child in node.children.items():
                self._fuzzy_search_recursive(
                    child, prefix + char, query,
                    current_row, max_distance, suggestions
                )
    
    # ========================================================================
    # 高级功能
    # ========================================================================
    
    def get_all_words(self) -> List[str]:
        """获取所有单词"""
        words = []
        self._collect_words(self.root, "", words)
        return words
    
    def _collect_words(self, node: TrieNode, prefix: str, words: List[str]) -> None:
        """收集所有单词"""
        if node.is_word:
            words.append(prefix)
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, words)
    
    def get_word_info(self, word: str) -> Optional[Dict]:
        """获取单词信息"""
        node = self._find_node(word)
        if node is None or not node.is_word:
            return None
        
        return {
            'word': word,
            'frequency': node.frequency,
            'metadata': node.metadata.copy()
        }
    
    def increment_frequency(self, word: str, amount: int = 1) -> bool:
        """增加单词频率"""
        node = self._find_node(word)
        if node is None or not node.is_word:
            return False
        
        node.frequency += amount
        return True
    
    def starts_with(self, prefix: str) -> bool:
        """检查是否存在以 prefix 开头的单词"""
        return self._find_node(prefix) is not None
    
    def count_prefix(self, prefix: str) -> int:
        """统计以 prefix 开头的单词数量"""
        node = self._find_node(prefix)
        if node is None:
            return 0
        
        count = 0
        self._count_words(node, count)
        return count
    
    def _count_words(self, node: TrieNode, count: int) -> int:
        """统计节点下的单词数"""
        result = 1 if node.is_word else 0
        for child in node.children.values():
            result += self._count_words(child, count)
        return result
    
    def longest_common_prefix(self) -> str:
        """获取最长公共前缀"""
        if not self.root.children:
            return ""
        
        prefix = []
        node = self.root
        
        while len(node.children) == 1 and not node.is_word:
            char = next(iter(node.children))
            prefix.append(char)
            node = node.children[char]
        
        return "".join(prefix)
    
    # ========================================================================
    # 序列化/反序列化
    # ========================================================================
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'case_sensitive': self.case_sensitive,
            'max_suggestions': self.max_suggestions,
            'words': [
                {'text': word, **(self.get_word_info(word) or {})}
                for word in self.get_all_words()
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TrieAutocomplete':
        """从字典创建"""
        trie = cls(
            case_sensitive=data.get('case_sensitive', False),
            max_suggestions=data.get('max_suggestions', 10)
        )
        
        for word_data in data.get('words', []):
            if isinstance(word_data, dict):
                trie.insert(
                    word_data['text'],
                    frequency=word_data.get('frequency', 1),
                    metadata=word_data.get('metadata')
                )
            else:
                trie.insert(word_data)
        
        return trie
    
    def to_json(self) -> str:
        """序列化为 JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TrieAutocomplete':
        """从 JSON 反序列化"""
        return cls.from_dict(json.loads(json_str))
    
    # ========================================================================
    # 统计信息
    # ========================================================================
    
    @property
    def word_count(self) -> int:
        """单词总数"""
        return self._word_count
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        words = self.get_all_words()
        total_freq = sum(
            self._find_node(w).frequency 
            for w in words if self._find_node(w)
        )
        
        return {
            'word_count': self._word_count,
            'total_frequency': total_freq,
            'avg_frequency': total_freq / self._word_count if self._word_count else 0,
            'case_sensitive': self.case_sensitive,
            'longest_common_prefix': self.longest_common_prefix(),
            'node_count': self._count_nodes(self.root)
        }
    
    def _count_nodes(self, node: TrieNode) -> int:
        """统计节点数量"""
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count
    
    # ========================================================================
    # 魔术方法
    # ========================================================================
    
    def __len__(self) -> int:
        return self._word_count
    
    def __contains__(self, word: str) -> bool:
        return self.contains(word)
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.get_all_words())
    
    def __repr__(self) -> str:
        return f"TrieAutocomplete(words={self._word_count}, case_sensitive={self.case_sensitive})"


# ============================================================================
# N-gram 自动补全器
# ============================================================================

class NGramAutocomplete:
    """
    基于 N-gram 的自动补全器
    
    适用于：
    - 单词补全
    - 句子补全
    - 模糊匹配
    
    Args:
        n: N-gram 大小（默认 2）
        case_sensitive: 是否区分大小写
        max_suggestions: 最大建议数量
    """
    
    def __init__(
        self, 
        n: int = 2, 
        case_sensitive: bool = False, 
        max_suggestions: int = 10
    ):
        self.n = n
        self.case_sensitive = case_sensitive
        self.max_suggestions = max_suggestions
        self.ngram_index: Dict[str, Dict[str, int]] = {}  # ngram -> {word: freq}
        self.word_freq: Dict[str, int] = {}
        self._word_count = 0
    
    def _normalize(self, text: str) -> str:
        """标准化文本"""
        return text if self.case_sensitive else text.lower()
    
    def _get_ngrams(self, word: str) -> List[str]:
        """获取单词的 N-gram"""
        padded = "^" + word + "$"
        return [padded[i:i+self.n] for i in range(len(padded) - self.n + 1)]
    
    def insert(self, word: str, frequency: int = 1) -> None:
        """插入单词"""
        if not word:
            return
        
        normalized = self._normalize(word)
        
        # 更新词频
        if word not in self.word_freq:
            self._word_count += 1
        
        self.word_freq[word] = self.word_freq.get(word, 0) + frequency
        
        # 更新 N-gram 索引
        for ngram in self._get_ngrams(normalized):
            if ngram not in self.ngram_index:
                self.ngram_index[ngram] = {}
            self.ngram_index[ngram][word] = self.ngram_index[ngram].get(word, 0) + 1
    
    def insert_batch(self, words: List[str], frequencies: Optional[List[int]] = None) -> None:
        """批量插入单词"""
        for i, word in enumerate(words):
            freq = frequencies[i] if frequencies else 1
            self.insert(word, freq)
    
    def search(self, query: str, min_score: float = 0.1) -> List[Suggestion]:
        """
        搜索匹配的单词
        
        Args:
            query: 查询字符串
            min_score: 最小得分阈值
            
        Returns:
            匹配的补全建议列表
        """
        if not query:
            # 返回最高频的单词
            sorted_words = sorted(
                self.word_freq.items(),
                key=lambda x: -x[1]
            )
            return [
                Suggestion(text=w, score=1.0, frequency=f)
                for w, f in sorted_words[:self.max_suggestions]
            ]
        
        normalized = self._normalize(query)
        query_ngrams = set(self._get_ngrams(normalized))
        
        # 计算每个候选词的得分
        scores: Dict[str, float] = {}
        for ngram in query_ngrams:
            if ngram in self.ngram_index:
                for word in self.ngram_index[ngram]:
                    if word not in scores:
                        scores[word] = 0
                    scores[word] += 1
        
        # 归一化得分
        suggestions = []
        for word, overlap in scores.items():
            word_ngrams = set(self._get_ngrams(self._normalize(word)))
            jaccard = overlap / (len(query_ngrams) + len(word_ngrams) - overlap)
            
            if jaccard >= min_score:
                suggestions.append(Suggestion(
                    text=word,
                    score=jaccard,
                    frequency=self.word_freq.get(word, 0)
                ))
        
        # 排序并返回
        suggestions.sort(key=lambda s: (-s.score, -s.frequency, s.text))
        return suggestions[:self.max_suggestions]
    
    def prefix_search(self, prefix: str) -> List[Suggestion]:
        """前缀搜索"""
        if not prefix:
            return self.search("")
        
        normalized = self._normalize(prefix)
        suggestions = []
        
        for word, freq in self.word_freq.items():
            if self._normalize(word).startswith(normalized):
                score = 1.0
                suggestions.append(Suggestion(text=word, score=score, frequency=freq))
        
        suggestions.sort(key=lambda s: (-s.frequency, -s.score, s.text))
        return suggestions[:self.max_suggestions]
    
    def contains(self, word: str) -> bool:
        """检查单词是否存在"""
        return word in self.word_freq
    
    def remove(self, word: str) -> bool:
        """删除单词"""
        if word not in self.word_freq:
            return False
        
        normalized = self._normalize(word)
        
        # 从 N-gram 索引中移除
        for ngram in self._get_ngrams(normalized):
            if ngram in self.ngram_index:
                self.ngram_index[ngram].pop(word, None)
                if not self.ngram_index[ngram]:
                    del self.ngram_index[ngram]
        
        del self.word_freq[word]
        self._word_count -= 1
        return True
    
    def clear(self) -> None:
        """清空所有数据"""
        self.ngram_index = {}
        self.word_freq = {}
        self._word_count = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'word_count': self._word_count,
            'ngram_count': len(self.ngram_index),
            'n': self.n,
            'case_sensitive': self.case_sensitive,
            'avg_word_freq': sum(self.word_freq.values()) / self._word_count if self._word_count else 0
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'n': self.n,
            'case_sensitive': self.case_sensitive,
            'max_suggestions': self.max_suggestions,
            'word_freq': self.word_freq.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'NGramAutocomplete':
        """从字典创建"""
        ngram = cls(
            n=data.get('n', 2),
            case_sensitive=data.get('case_sensitive', False),
            max_suggestions=data.get('max_suggestions', 10)
        )
        
        for word, freq in data.get('word_freq', {}).items():
            ngram.word_freq[word] = freq
            ngram._word_count += 1
            
            normalized = ngram._normalize(word)
            for ng in ngram._get_ngrams(normalized):
                if ng not in ngram.ngram_index:
                    ngram.ngram_index[ng] = {}
                ngram.ngram_index[ng][word] = freq
        
        return ngram
    
    def __len__(self) -> int:
        return self._word_count
    
    def __contains__(self, word: str) -> bool:
        return word in self.word_freq
    
    def __repr__(self) -> str:
        return f"NGramAutocomplete(words={self._word_count}, n={self.n})"


# ============================================================================
# 组合自动补全器
# ============================================================================

class HybridAutocomplete:
    """
    混合自动补全器
    
    结合 Trie 和 N-gram 的优点：
    - Trie 用于精确前缀匹配
    - N-gram 用于模糊匹配
    
    Args:
        case_sensitive: 是否区分大小写
        max_suggestions: 最大建议数量
        fuzzy_weight: 模糊匹配权重（0-1）
    """
    
    def __init__(
        self, 
        case_sensitive: bool = False, 
        max_suggestions: int = 10,
        fuzzy_weight: float = 0.5
    ):
        self.case_sensitive = case_sensitive
        self.max_suggestions = max_suggestions
        self.fuzzy_weight = fuzzy_weight
        
        self.trie = TrieAutocomplete(case_sensitive, max_suggestions * 2)
        self.ngram = NGramAutocomplete(2, case_sensitive, max_suggestions * 2)
        self._word_count = 0
    
    def insert(
        self, 
        word: str, 
        frequency: int = 1, 
        metadata: Optional[Dict] = None
    ) -> None:
        """插入单词"""
        self.trie.insert(word, frequency, metadata)
        self.ngram.insert(word, frequency)
        self._word_count = self.trie.word_count
    
    def insert_batch(self, words: List[str], frequencies: Optional[List[int]] = None) -> None:
        """批量插入单词"""
        for i, word in enumerate(words):
            freq = frequencies[i] if frequencies else 1
            self.insert(word, freq)
    
    def search(self, query: str, fuzzy: bool = True) -> List[Suggestion]:
        """
        搜索匹配的单词
        
        Args:
            query: 查询字符串
            fuzzy: 是否启用模糊匹配
            
        Returns:
            匹配的补全建议列表
        """
        # Trie 精确前缀匹配
        trie_results = self.trie.search(query)
        
        if not fuzzy:
            return trie_results[:self.max_suggestions]
        
        # N-gram 模糊匹配
        ngram_results = self.ngram.search(query)
        
        # 合并结果
        merged: Dict[str, Suggestion] = {}
        
        for s in trie_results:
            merged[s.text] = Suggestion(
                text=s.text,
                score=s.score,
                frequency=s.frequency,
                metadata=s.metadata
            )
        
        for s in ngram_results:
            if s.text in merged:
                # 结合两个得分
                merged[s.text].score = (
                    merged[s.text].score * (1 - self.fuzzy_weight) + 
                    s.score * self.fuzzy_weight
                )
            else:
                merged[s.text] = Suggestion(
                    text=s.text,
                    score=s.score * self.fuzzy_weight,
                    frequency=s.frequency,
                    metadata=s.metadata
                )
        
        # 排序
        results = list(merged.values())
        results.sort(key=lambda s: (-s.score, -s.frequency, s.text))
        return results[:self.max_suggestions]
    
    def contains(self, word: str) -> bool:
        """检查单词是否存在"""
        return word in self.trie
    
    def remove(self, word: str) -> bool:
        """删除单词"""
        trie_removed = self.trie.remove(word)
        ngram_removed = self.ngram.remove(word)
        self._word_count = self.trie.word_count
        return trie_removed or ngram_removed
    
    def clear(self) -> None:
        """清空所有数据"""
        self.trie.clear()
        self.ngram.clear()
        self._word_count = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'word_count': self._word_count,
            'case_sensitive': self.case_sensitive,
            'fuzzy_weight': self.fuzzy_weight,
            'trie_stats': self.trie.get_stats(),
            'ngram_stats': self.ngram.get_stats()
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'case_sensitive': self.case_sensitive,
            'max_suggestions': self.max_suggestions,
            'fuzzy_weight': self.fuzzy_weight,
            'trie': self.trie.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HybridAutocomplete':
        """从字典创建"""
        hybrid = cls(
            case_sensitive=data.get('case_sensitive', False),
            max_suggestions=data.get('max_suggestions', 10),
            fuzzy_weight=data.get('fuzzy_weight', 0.5)
        )
        
        trie_data = data.get('trie', {})
        for word_data in trie_data.get('words', []):
            if isinstance(word_data, dict):
                hybrid.insert(
                    word_data['text'],
                    frequency=word_data.get('frequency', 1),
                    metadata=word_data.get('metadata')
                )
            else:
                hybrid.insert(word_data)
        
        return hybrid
    
    def __len__(self) -> int:
        return self._word_count
    
    def __contains__(self, word: str) -> bool:
        return word in self.trie
    
    def __repr__(self) -> str:
        return f"HybridAutocomplete(words={self._word_count})"


# ============================================================================
# 工具函数
# ============================================================================

def create_autocomplete(
    words: List[str],
    case_sensitive: bool = False,
    max_suggestions: int = 10,
    use_ngram: bool = False
) -> TrieAutocomplete:
    """
    创建自动补全器的便捷函数
    
    Args:
        words: 单词列表
        case_sensitive: 是否区分大小写
        max_suggestions: 最大建议数量
        use_ngram: 是否使用 N-gram
        
    Returns:
        配置好的自动补全器
    """
    if use_ngram:
        ac = NGramAutocomplete(case_sensitive=case_sensitive, max_suggestions=max_suggestions)
    else:
        ac = TrieAutocomplete(case_sensitive=case_sensitive, max_suggestions=max_suggestions)
    
    ac.insert_batch(words)
    return ac


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串的编辑距离
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        编辑距离
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        
        previous_row = current_row
    
    return previous_row[-1]


def jaccard_similarity(s1: str, s2: str, n: int = 2) -> float:
    """
    计算两个字符串的 Jaccard 相似度（基于 N-gram）
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        n: N-gram 大小
        
    Returns:
        相似度（0-1）
    """
    def get_ngrams(s: str) -> Set[str]:
        padded = "^" + s + "$"
        return set(padded[i:i+n] for i in range(len(padded) - n + 1))
    
    ngrams1 = get_ngrams(s1.lower())
    ngrams2 = get_ngrams(s2.lower())
    
    if not ngrams1 and not ngrams2:
        return 1.0
    
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    
    return len(intersection) / len(union) if union else 0.0