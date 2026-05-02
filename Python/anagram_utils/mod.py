"""
Anagram Utils - 变位词工具模块

提供变位词检测、生成、求解等功能。
变位词(Anagram)是指通过重新排列字母顺序而形成的新词或短语。

功能:
- 检测两个字符串是否为变位词
- 生成单词的所有排列组合
- 查找变位词
- 从字母池生成可能的单词
- 变位词评分和分类

零外部依赖，仅使用 Python 标准库。
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import Counter, defaultdict
from itertools import permutations
import math


def normalize_text(text: str) -> str:
    """
    规范化文本：移除空格、标点，转换为小写
    
    Args:
        text: 输入文本
        
    Returns:
        规范化后的文本
        
    Examples:
        >>> normalize_text("Listen!")
        'listen'
        >>> normalize_text("A gentleman")
        'agentleman'
    """
    return ''.join(c.lower() for c in text if c.isalnum())


def get_char_count(text: str) -> Counter:
    """
    获取文本中每个字符的出现次数
    
    Args:
        text: 输入文本
        
    Returns:
        字符计数的 Counter 对象
        
    Examples:
        >>> get_char_count("hello")
        Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
    """
    return Counter(c.lower() for c in text if c.isalnum())


def is_anagram(text1: str, text2: str, *, strict: bool = False) -> bool:
    """
    检测两个字符串是否为变位词
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        strict: 严格模式 - 区分大小写，不移除空格和标点
        
    Returns:
        是否为变位词
        
    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("A gentleman", "Elegant man")
        True
        >>> is_anagram("hello", "world")
        False
        >>> is_anagram("Listen", "silent", strict=True)
        False
    """
    if strict:
        return Counter(text1) == Counter(text2)
    
    return get_char_count(text1) == get_char_count(text2)


def find_anagrams(word: str, word_list: List[str], *, strict: bool = False) -> List[str]:
    """
    在单词列表中查找给定单词的变位词
    
    Args:
        word: 目标单词
        word_list: 待搜索的单词列表
        strict: 严格模式
        
    Returns:
        找到的变位词列表
        
    Examples:
        >>> words = ["listen", "silent", "enlist", "hello", "tinsel"]
        >>> find_anagrams("listen", words)
        ['silent', 'enlist', 'tinsel']
    """
    target_count = get_char_count(word) if not strict else Counter(word)
    result = []
    
    for w in word_list:
        if strict:
            if Counter(w) == target_count and w != word:
                result.append(w)
        else:
            if get_char_count(w) == target_count and w.lower() != word.lower():
                result.append(w)
    
    return result


def group_anagrams(words: List[str]) -> List[List[str]]:
    """
    将单词列表按变位词分组
    
    Args:
        words: 单词列表
        
    Returns:
        分组后的变位词列表
        
    Examples:
        >>> group_anagrams(["listen", "silent", "hello", "world", "enlist"])
        [['listen', 'silent', 'enlist'], ['hello'], ['world']]
    """
    groups: Dict[str, List[str]] = defaultdict(list)
    
    for word in words:
        # 使用排序后的字符作为键
        key = ''.join(sorted(normalize_text(word)))
        groups[key].append(word)
    
    # 返回至少有一个单词的组
    return [group for group in groups.values() if group]


def generate_permutations(text: str, *, max_length: Optional[int] = None) -> List[str]:
    """
    生成文本的所有排列组合
    
    Args:
        text: 输入文本
        max_length: 最大排列长度（None 表示使用完整长度）
        
    Returns:
        所有排列的列表（去重）
        
    Examples:
        >>> sorted(generate_permutations("abc"))
        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
        >>> len(generate_permutations("aab"))  # 自动去重
        3
    """
    text = normalize_text(text)
    n = len(text)
    
    if max_length is None:
        max_length = n
    
    max_length = min(max_length, n)
    result: Set[str] = set()
    
    for length in range(1, max_length + 1):
        for perm in permutations(text, length):
            result.add(''.join(perm))
    
    return list(result)


def generate_anagrams(text: str, *, min_length: int = 2) -> List[str]:
    """
    生成文本的所有可能变位词（同一长度的排列）
    
    Args:
        text: 输入文本
        min_length: 最小单词长度
        
    Returns:
        变位词列表
        
    Examples:
        >>> sorted(generate_anagrams("abc"))
        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
        >>> len(generate_anagrams("listen"))  # 720 种排列
        720
    """
    text = normalize_text(text)
    
    if len(text) < min_length:
        return []
    
    result: Set[str] = set()
    
    for perm in permutations(text):
        word = ''.join(perm)
        if len(word) >= min_length:
            result.add(word)
    
    return list(result)


def can_form_word(letters: str, word: str) -> bool:
    """
    检查是否可以用给定的字母组成目标单词
    
    Args:
        letters: 可用字母池
        word: 目标单词
        
    Returns:
        是否可以组成
        
    Examples:
        >>> can_form_word("abcdef", "cab")
        True
        >>> can_form_word("abc", "abcd")
        False
    """
    letters_count = get_char_count(letters)
    word_count = get_char_count(word)
    
    for char, count in word_count.items():
        if letters_count.get(char, 0) < count:
            return False
    
    return True


def find_formable_words(letters: str, word_list: List[str], *, min_length: int = 1) -> List[str]:
    """
    从字母池中找出所有可以组成的单词
    
    Args:
        letters: 可用字母池
        word_list: 候选单词列表
        min_length: 最小单词长度
        
    Returns:
        可以组成的单词列表
        
    Examples:
        >>> words = ["cab", "bad", "ace", "deed", "bead"]
        >>> sorted(find_formable_words("abcde", words))
        ['ace', 'bad', 'cab']
    """
    result = []
    letters_count = get_char_count(letters)
    
    for word in word_list:
        if len(normalize_text(word)) < min_length:
            continue
        
        word_count = get_char_count(word)
        
        can_form = True
        for char, count in word_count.items():
            if letters_count.get(char, 0) < count:
                can_form = False
                break
        
        if can_form:
            result.append(word)
    
    return result


def anagram_distance(text1: str, text2: str) -> int:
    """
    计算两个字符串的"变位距离"
    即需要移除多少字符才能使它们成为变位词
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        变位距离（越小越相似）
        
    Examples:
        >>> anagram_distance("listen", "silent")
        0
        >>> anagram_distance("listen", "list")
        2
        >>> anagram_distance("abc", "def")
        6
    """
    count1 = get_char_count(text1)
    count2 = get_char_count(text2)
    
    # 计算差异
    all_chars = set(count1.keys()) | set(count2.keys())
    distance = 0
    
    for char in all_chars:
        distance += abs(count1.get(char, 0) - count2.get(char, 0))
    
    return distance


def anagram_similarity(text1: str, text2: str) -> float:
    """
    计算两个字符串的变位相似度（0-1）
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        相似度分数（1 表示完全相同的变位词）
        
    Examples:
        >>> anagram_similarity("listen", "silent")
        1.0
        >>> anagram_similarity("listen", "list")
        0.6666666666666666
        >>> anagram_similarity("abc", "def")
        0.0
    """
    count1 = get_char_count(text1)
    count2 = get_char_count(text2)
    
    total_chars = sum(count1.values()) + sum(count2.values())
    
    if total_chars == 0:
        return 1.0
    
    distance = anagram_distance(text1, text2)
    return 1.0 - (distance / total_chars)


def get_unique_chars(text: str) -> Set[str]:
    """
    获取文本中的唯一字符集
    
    Args:
        text: 输入文本
        
    Returns:
        唯一字符集合
        
    Examples:
        >>> get_unique_chars("hello")
        {'h', 'e', 'l', 'o'}
    """
    return set(normalize_text(text))


def get_missing_chars(source: str, target: str) -> Counter:
    """
    获取从源字符串组成目标字符串所需的额外字符
    
    Args:
        source: 源字符串（字母池）
        target: 目标字符串
        
    Returns:
        缺少的字符及其数量
        
    Examples:
        >>> get_missing_chars("abc", "abcd")
        Counter({'d': 1})
        >>> get_missing_chars("aabbc", "aabbcc")
        Counter({'c': 1})
    """
    source_count = get_char_count(source)
    target_count = get_char_count(target)
    missing = Counter()
    
    for char, count in target_count.items():
        diff = count - source_count.get(char, 0)
        if diff > 0:
            missing[char] = diff
    
    return missing


def get_extra_chars(source: str, target: str) -> Counter:
    """
    获取源字符串中组成目标字符串后剩余的字符
    
    Args:
        source: 源字符串（字母池）
        target: 目标字符串
        
    Returns:
        剩余的字符及其数量
        
    Examples:
        >>> get_extra_chars("abcde", "abc")
        Counter({'d': 1, 'e': 1})
    """
    source_count = get_char_count(source)
    target_count = get_char_count(target)
    extra = Counter()
    
    for char, count in source_count.items():
        diff = count - target_count.get(char, 0)
        if diff > 0:
            extra[char] = diff
    
    return extra


def subtract_chars(text: str, to_remove: str) -> str:
    """
    从文本中移除指定字符（变位词减法）
    
    Args:
        text: 源文本
        to_remove: 要移除的字符
        
    Returns:
        移除后的文本
        
    Examples:
        >>> subtract_chars("listen", "sil")
        'ten'
        >>> subtract_chars("aabbbcc", "ab")
        'abbc'
    """
    text_count = get_char_count(text)
    remove_count = get_char_count(to_remove)
    
    result = []
    for char, count in text_count.items():
        remaining = count - remove_count.get(char, 0)
        result.extend([char] * remaining)
    
    return ''.join(result)


def add_chars(text: str, to_add: str) -> str:
    """
    向文本添加字符（变位词加法）
    
    Args:
        text: 源文本
        to_add: 要添加的字符
        
    Returns:
        添加后的文本
        
    Examples:
        >>> add_chars("abc", "de")
        'abcde'
    """
    return normalize_text(text) + normalize_text(to_add)


def sort_chars(text: str) -> str:
    """
    将文本字符排序（用于变位词规范化）
    
    Args:
        text: 输入文本
        
    Returns:
        排序后的文本
        
    Examples:
        >>> sort_chars("listen")
        'eilnst'
    """
    return ''.join(sorted(normalize_text(text)))


def anagram_signature(text: str) -> str:
    """
    获取文本的变位词签名（排序后的字符）
    用于快速识别变位词
    
    Args:
        text: 输入文本
        
    Returns:
        变位词签名
        
    Examples:
        >>> anagram_signature("silent")
        'eilnst'
        >>> anagram_signature("listen")
        'eilnst'
    """
    return sort_chars(text)


def count_anagram_pairs(words: List[str]) -> int:
    """
    计算单词列表中变位词对的数量
    
    Args:
        words: 单词列表
        
    Returns:
        变位词对的数量
        
    Examples:
        >>> count_anagram_pairs(["listen", "silent", "hello", "world", "enlist"])
        3
    """
    groups = group_anagrams(words)
    total = 0
    
    for group in groups:
        n = len(group)
        if n > 1:
            # C(n, 2) = n * (n-1) / 2
            total += n * (n - 1) // 2
    
    return total


def longest_anagram_group(words: List[str]) -> List[str]:
    """
    找出最长的变位词组
    
    Args:
        words: 单词列表
        
    Returns:
        最长的变位词组
        
    Examples:
        >>> longest_anagram_group(["listen", "silent", "hello", "enlist", "tinsel"])
        ['listen', 'silent', 'enlist', 'tinsel']
    """
    groups = group_anagrams(words)
    
    if not groups:
        return []
    
    return max(groups, key=len)


def has_anagram_in_list(word: str, word_list: List[str]) -> bool:
    """
    检查单词列表中是否存在给定单词的变位词
    
    Args:
        word: 目标单词
        word_list: 单词列表
        
    Returns:
        是否存在变位词
        
    Examples:
        >>> has_anagram_in_list("listen", ["hello", "silent", "world"])
        True
        >>> has_anagram_in_list("hello", ["world", "test"])
        False
    """
    return len(find_anagrams(word, word_list)) > 0


def get_anagram_info(text: str) -> Dict:
    """
    获取文本的变位词信息
    
    Args:
        text: 输入文本
        
    Returns:
        包含各种信息的字典
        
    Examples:
        >>> info = get_anagram_info("listen")
        >>> info['length']
        6
        >>> info['unique_chars']
        5
    """
    normalized = normalize_text(text)
    char_count = get_char_count(text)
    
    # 计算排列数（考虑重复字符）
    # n! / (n1! * n2! * ...) 其中 n1, n2 是各字符重复次数
    permutation_count = math.factorial(len(normalized))
    for c in char_count.values():
        permutation_count //= math.factorial(c)
    
    return {
        'original': text,
        'normalized': normalized,
        'length': len(normalized),
        'unique_chars': len(char_count),
        'char_frequency': dict(char_count),
        'signature': anagram_signature(text),
        'is_palindrome': normalized == normalized[::-1],
        'permutation_count': permutation_count
    }


def is_partial_anagram(source: str, target: str) -> bool:
    """
    检查是否是部分变位词（source 包含 target 的所有字符）
    
    Args:
        source: 源字符串（字母池）
        target: 目标字符串
        
    Returns:
        是否是部分变位词
        
    Examples:
        >>> is_partial_anagram("listen", "silent")
        True
        >>> is_partial_anagram("listening", "silent")
        True
        >>> is_partial_anagram("list", "silent")
        False
    """
    source_count = get_char_count(source)
    target_count = get_char_count(target)
    
    for char, count in target_count.items():
        if source_count.get(char, 0) < count:
            return False
    
    return True


def find_all_formable_words(letters: str, word_list: List[str], 
                            *, min_length: int = 2, max_length: Optional[int] = None) -> Dict[int, List[str]]:
    """
    从字母池中找出所有可以组成的单词，按长度分组
    
    Args:
        letters: 可用字母池
        word_list: 候选单词列表
        min_length: 最小单词长度
        max_length: 最大单词长度（None 表示不限制）
        
    Returns:
        按长度分组的单词字典
        
    Examples:
        >>> words = ["cab", "bad", "ace", "deed", "bead", "ab", "abcde"]
        >>> result = find_all_formable_words("abcde", words)
        >>> 2 in result  # "ab"
        True
        >>> 3 in result  # "cab", "bad", "ace"
        True
    """
    result: Dict[int, List[str]] = defaultdict(list)
    letters_count = get_char_count(letters)
    letters_len = len(normalize_text(letters))
    
    if max_length is None:
        max_length = letters_len
    
    for word in word_list:
        word_normalized = normalize_text(word)
        word_len = len(word_normalized)
        
        if word_len < min_length or word_len > max_length:
            continue
        
        word_count = get_char_count(word)
        
        can_form = True
        for char, count in word_count.items():
            if letters_count.get(char, 0) < count:
                can_form = False
                break
        
        if can_form:
            result[word_len].append(word)
    
    return dict(result)


def multiset_anagram_check(texts: List[str]) -> bool:
    """
    检查多个字符串是否互为变位词
    
    Args:
        texts: 字符串列表
        
    Returns:
        是否全部互为变位词
        
    Examples:
        >>> multiset_anagram_check(["listen", "silent", "enlist"])
        True
        >>> multiset_anagram_check(["listen", "silent", "hello"])
        False
    """
    if len(texts) < 2:
        return True
    
    first_count = get_char_count(texts[0])
    
    for text in texts[1:]:
        if get_char_count(text) != first_count:
            return False
    
    return True


def find_anagram_subset(letters: str, target_length: int) -> int:
    """
    计算从给定字母中能组成特定长度变位词的数量
    
    Args:
        letters: 可用字母池
        target_length: 目标长度
        
    Returns:
        可能的排列数量
        
    Examples:
        >>> find_anagram_subset("abc", 2)  # P(3,2) = 6
        6
        >>> find_anagram_subset("aab", 2)  # aa, ab, ba = 3 unique
        3
    """
    letters = normalize_text(letters)
    char_count = get_char_count(letters)
    n = len(letters)
    
    if target_length > n:
        return 0
    
    # 对于有重复字符的情况，精确计算比较复杂
    # 这里使用生成排列并去重的方式
    perms = set()
    for perm in permutations(letters, target_length):
        perms.add(''.join(perm))
    
    return len(perms)


def suggest_anagram_words(letters: str, word_list: List[str], 
                          top_n: int = 10) -> List[Tuple[str, int]]:
    """
    从字母池中建议可能的单词，按使用字母数排序
    
    Args:
        letters: 可用字母池
        word_list: 候选单词列表
        top_n: 返回前 N 个建议
        
    Returns:
        (单词, 使用字母数) 的列表，按使用字母数降序排列
        
    Examples:
        >>> words = ["cab", "bad", "ace", "deed", "bead"]
        >>> suggest_anagram_words("abcde", words, 3)
        [('bead', 4), ('cab', 3), ('bad', 3)]
    """
    formable = find_formable_words(letters, word_list)
    
    # 按使用的字母数量排序
    scored = [(word, len(normalize_text(word))) for word in formable]
    scored.sort(key=lambda x: (-x[1], x[0]))
    
    return scored[:top_n]


class AnagramSolver:
    """
    变位词求解器类
    
    提供更高级的变位词求解功能，包括缓存和批量处理。
    
    Examples:
        >>> solver = AnagramSolver(["listen", "silent", "hello", "world"])
        >>> solver.find_anagrams("listen")
        ['silent']
        >>> solver.get_all_anagrams_of_length(6)
        [['listen', 'silent']]
    """
    
    def __init__(self, word_list: List[str]):
        """
        初始化求解器
        
        Args:
            word_list: 单词列表
        """
        self.word_list = [normalize_text(w) for w in word_list]
        self._build_index()
    
    def _build_index(self):
        """构建变位词索引"""
        self._signature_index: Dict[str, List[str]] = defaultdict(list)
        
        for word in self.word_list:
            signature = anagram_signature(word)
            self._signature_index[signature].append(word)
    
    def find_anagrams(self, word: str) -> List[str]:
        """
        查找给定单词的变位词
        
        Args:
            word: 目标单词
            
        Returns:
            变位词列表
        """
        signature = anagram_signature(word)
        word_normalized = normalize_text(word)
        
        return [w for w in self._signature_index.get(signature, [])
                if w != word_normalized]
    
    def get_all_anagram_groups(self) -> List[List[str]]:
        """
        获取所有变位词组
        
        Returns:
            变位词组列表
        """
        return [group for group in self._signature_index.values() if len(group) > 1]
    
    def get_all_anagrams_of_length(self, length: int) -> List[List[str]]:
        """
        获取指定长度的所有变位词组
        
        Args:
            length: 目标长度
            
        Returns:
            指定长度的变位词组列表
        """
        result = []
        
        for signature, group in self._signature_index.items():
            if len(signature) == length and len(group) > 1:
                result.append(group)
        
        return result
    
    def find_formable_words(self, letters: str, min_length: int = 2) -> List[str]:
        """
        从字母池中找出所有可以组成的单词
        
        Args:
            letters: 可用字母池
            min_length: 最小单词长度
            
        Returns:
            可以组成的单词列表
        """
        return find_formable_words(letters, self.word_list, min_length=min_length)
    
    def get_words_with_signature(self, signature: str) -> List[str]:
        """
        获取具有指定签名的所有单词
        
        Args:
            signature: 变位词签名
            
        Returns:
            单词列表
        """
        return self._signature_index.get(signature, []).copy()
    
    def add_word(self, word: str):
        """
        添加单词到求解器
        
        Args:
            word: 要添加的单词
        """
        word_normalized = normalize_text(word)
        if word_normalized not in self.word_list:
            self.word_list.append(word_normalized)
            signature = anagram_signature(word_normalized)
            self._signature_index[signature].append(word_normalized)
    
    def remove_word(self, word: str) -> bool:
        """
        从求解器中移除单词
        
        Args:
            word: 要移除的单词
            
        Returns:
            是否成功移除
        """
        word_normalized = normalize_text(word)
        
        if word_normalized in self.word_list:
            self.word_list.remove(word_normalized)
            signature = anagram_signature(word_normalized)
            
            if word_normalized in self._signature_index[signature]:
                self._signature_index[signature].remove(word_normalized)
            
            return True
        
        return False
    
    def get_stats(self) -> Dict:
        """
        获取求解器统计信息
        
        Returns:
            统计信息字典
        """
        anagram_groups = self.get_all_anagram_groups()
        
        return {
            'total_words': len(self.word_list),
            'unique_signatures': len(self._signature_index),
            'anagram_groups_count': len(anagram_groups),
            'total_anagram_words': sum(len(g) for g in anagram_groups),
            'largest_group_size': max((len(g) for g in anagram_groups), default=0),
            'groups_by_length': {
                length: len([g for g in anagram_groups if len(g[0]) == length])
                for length in sorted(set(len(g[0]) for g in anagram_groups))
            } if anagram_groups else {}
        }


if __name__ == "__main__":
    # 简单演示
    print("Anagram Utils 演示")
    print("=" * 50)
    
    # 基本检测
    print(f"'listen' 和 'silent' 是变位词: {is_anagram('listen', 'silent')}")
    print(f"'A gentleman' 和 'Elegant man' 是变位词: {is_anagram('A gentleman', 'Elegant man')}")
    
    # 查找变位词
    words = ["listen", "silent", "enlist", "tinsel", "hello", "world"]
    print(f"\n'listen' 的变位词: {find_anagrams('listen', words)}")
    
    # 分组
    print(f"\n分组结果: {group_anagrams(words)}")
    
    # 变位距离
    print(f"\n'listen' 和 'silent' 的变位距离: {anagram_distance('listen', 'silent')}")
    print(f"'listen' 和 'list' 的变位距离: {anagram_distance('listen', 'list')}")
    
    # 使用 AnagramSolver
    solver = AnagramSolver(words)
    print(f"\n求解器统计: {solver.get_stats()}")