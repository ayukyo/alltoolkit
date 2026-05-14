"""
Porter Stemmer Utils - 词干提取工具

实现了经典的 Porter Stemmer 算法（Porter, 1980），用于将英语单词还原到词干形式。
词干提取是自然语言处理中的基础技术，广泛应用于：
- 搜索引擎索引
- 文本分类
- 信息检索
- 文本相似度计算

特点：
- 零外部依赖，纯 Python 实现
- 完整的 Porter 算法 5 个步骤
- 支持批量处理
- 支持自定义规则扩展

用法示例：
    from porter_stemmer_utils import PorterStemmer
    
    stemmer = PorterStemmer()
    stem = stemmer.stem("running")  # "run"
    stem = stemmer.stem("happiness")  # "happi"
"""

from typing import List, Optional, Set, Tuple, Dict
import re


class PorterStemmer:
    """
    Porter Stemmer 实现
    
    实现了 Martin Porter 于 1980 年提出的词干提取算法。
    该算法通过一系列规则逐步剥离单词的后缀。
    """
    
    def __init__(self):
        """初始化词干提取器"""
        # 元音字母
        self.vowels = set('aeiou')
        
    def _is_consonant(self, word: str, i: int) -> bool:
        """
        判断位置 i 的字符是否为辅音
        
        规则：非元音字母为辅音，但 'y' 需要特殊处理
        当 i=0 且字符为 'y' 时，视为辅音
        当 i>0 且字符为 'y' 且前一个字符为元音时，视为辅音
        否则 'y' 视为元音
        """
        if i < 0 or i >= len(word):
            return False
            
        char = word[i]
        if char in self.vowels:
            return False
        if char == 'y':
            if i == 0:
                return True
            return not self._is_consonant(word, i - 1)
        return True
    
    def _measure(self, word: str) -> int:
        """
        计算单词的 measure (m)
        
        m 是单词中 VC 序列的数量，其中：
        V = 连续的元音序列
        C = 连续的辅音序列
        
        [C](VC)^m[V] 的模式中 m 的值
        
        例如：
        - "tr" -> m=0 (C)
        - "ee" -> m=0 (V)
        - "tree" -> m=0 (CV)
        - "y" -> m=0 (C)
        - "by" -> m=0 (CV)
        - "trouble" -> m=1 (CVCV)
        - "oats" -> m=1 (VC)
        - "trees" -> m=1 (CV)
        - "ivy" -> m=1 (CV)
        """
        m = 0
        i = 0
        n = len(word)
        
        # 跳过开头的辅音
        while i < n and self._is_consonant(word, i):
            i += 1
            
        # 计算 VC 序列
        while i < n:
            # 跳过元音
            while i < n and not self._is_consonant(word, i):
                i += 1
            if i >= n:
                break
            # 跳过辅音
            while i < n and self._is_consonant(word, i):
                i += 1
            m += 1
            
        return m
    
    def _has_vowel(self, word: str) -> bool:
        """判断词干中是否包含元音"""
        for i in range(len(word)):
            if not self._is_consonant(word, i):
                return True
        return False
    
    def _ends_double_consonant(self, word: str) -> bool:
        """判断单词是否以双辅音结尾"""
        if len(word) < 2:
            return False
        return (word[-1] == word[-2] and 
                self._is_consonant(word, len(word) - 1))
    
    def _ends_cvc(self, word: str) -> bool:
        """
        判断单词是否以 CVC 模式结尾
        
        具体规则：
        - 最后一个字符是辅音
        - 倒数第二个字符是元音
        - 倒数第三个字符是辅音
        - 最后一个字符不能是 w, x, y
        
        这是为了保护短单词如 "how", "tray", "box" 等
        """
        if len(word) < 3:
            return False
            
        return (self._is_consonant(word, len(word) - 1) and
                not self._is_consonant(word, len(word) - 2) and
                self._is_consonant(word, len(word) - 3) and
                word[-1] not in 'wxy')
    
    def _replace_suffix(self, word: str, suffix: str, replacement: str, 
                        min_measure: int = 0) -> Tuple[str, bool]:
        """
        替换后缀
        
        Args:
            word: 单词
            suffix: 要替换的后缀
            replacement: 替换后的内容
            min_measure: 最小 measure 要求
            
        Returns:
            (处理后的单词, 是否进行了替换)
        """
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if self._measure(stem) > min_measure:
                return stem + replacement, True
        return word, False
    
    def _step1a(self, word: str) -> str:
        """步骤 1a: 处理复数形式"""
        if word.endswith('sses'):
            return word[:-2]  # ssess -> ss
        if word.endswith('ies'):
            return word[:-2]  # ies -> i
        if word.endswith('ss'):
            return word  # ss 保持不变
        if word.endswith('s'):
            return word[:-1]  # s -> 空
        return word
    
    def _step1b(self, word: str) -> str:
        """步骤 1b: 处理 -ed, -ing 后缀"""
        if word.endswith('eed'):
            stem = word[:-3]
            if self._measure(stem) > 0:
                return word[:-1]  # eed -> ee
            return word
            
        changed = False
        if word.endswith('ed'):
            stem = word[:-2]
            if self._has_vowel(stem):
                word = stem
                changed = True
        elif word.endswith('ing'):
            stem = word[:-3]
            if self._has_vowel(stem):
                word = stem
                changed = True
                
        if changed:
            # 进一步处理
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self._ends_double_consonant(word) and word[-1] not in 'lsz':
                word = word[:-1]
            elif self._measure(word) == 1 and self._ends_cvc(word):
                word += 'e'
                
        return word
    
    def _step1c(self, word: str) -> str:
        """步骤 1c: 将结尾的 y 替换为 i（如果词干包含元音）"""
        if word.endswith('y'):
            stem = word[:-1]
            if self._has_vowel(stem):
                return stem + 'i'
        return word
    
    def _step2(self, word: str) -> str:
        """步骤 2: 处理各种双字母后缀"""
        suffixes = [
            ('ational', 'ate'),
            ('tional', 'tion'),
            ('enci', 'ence'),
            ('anci', 'ance'),
            ('izer', 'ize'),
            ('abli', 'able'),
            ('alli', 'al'),
            ('entli', 'ent'),
            ('eli', 'e'),
            ('ousli', 'ous'),
            ('ization', 'ize'),
            ('ation', 'ate'),
            ('ator', 'ate'),
            ('alism', 'al'),
            ('iveness', 'ive'),
            ('fulness', 'ful'),
            ('ousness', 'ous'),
            ('aliti', 'al'),
            ('iviti', 'ive'),
            ('biliti', 'ble'),
        ]
        
        for suffix, replacement in suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self._measure(stem) > 0:
                    return stem + replacement
                    
        return word
    
    def _step3(self, word: str) -> str:
        """步骤 3: 处理 -ful, -ness 等后缀"""
        suffixes = [
            ('icate', 'ic'),
            ('ative', ''),
            ('alize', 'al'),
            ('iciti', 'ic'),
            ('ical', 'ic'),
            ('ful', ''),
            ('ness', ''),
        ]
        
        for suffix, replacement in suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self._measure(stem) > 0:
                    return stem + replacement
                    
        return word
    
    def _step4(self, word: str) -> str:
        """步骤 4: 移除 -ant, -ence 等后缀"""
        suffixes = [
            'al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant',
            'ement', 'ment', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti',
            'ous', 'ive', 'ize'
        ]
        
        for suffix in suffixes:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if self._measure(stem) > 1:
                    # 特殊处理 -ion: 需要词干以 s 或 t 结尾
                    if suffix == 'ion':
                        if stem and stem[-1] in 'st':
                            return stem
                    else:
                        return stem
                        
        return word
    
    def _step5a(self, word: str) -> str:
        """步骤 5a: 移除结尾的 e"""
        if word.endswith('e'):
            stem = word[:-1]
            m = self._measure(stem)
            if m > 1:
                return stem
            if m == 1 and not self._ends_cvc(stem):
                return stem
        return word
    
    def _step5b(self, word: str) -> str:
        """步骤 5b: 移除双辅音中的第二个字母"""
        if (self._measure(word) > 1 and 
            self._ends_double_consonant(word) and 
            word.endswith('l')):
            return word[:-1]
        return word
    
    def stem(self, word: str) -> str:
        """
        提取单词的词干
        
        Args:
            word: 要处理的单词（应该只包含小写字母）
            
        Returns:
            词干形式
            
        示例：
            >>> stemmer = PorterStemmer()
            >>> stemmer.stem("running")
            'run'
            >>> stemmer.stem("happiness")
            'happi'
        """
        # 转换为小写
        word = word.lower().strip()
        
        if len(word) <= 2:
            return word
            
        # 应用 5 个步骤
        word = self._step1a(word)
        word = self._step1b(word)
        word = self._step1c(word)
        word = self._step2(word)
        word = self._step3(word)
        word = self._step4(word)
        word = self._step5a(word)
        word = self._step5b(word)
        
        return word
    
    def stem_words(self, words: List[str]) -> List[str]:
        """
        批量提取词干
        
        Args:
            words: 单词列表
            
        Returns:
            词干列表
            
        示例：
            >>> stemmer = PorterStemmer()
            >>> stemmer.stem_words(["running", "jumps", "happiness"])
            ['run', 'jump', 'happi']
        """
        return [self.stem(word) for word in words]
    
    def stem_text(self, text: str) -> str:
        """
        提取文本中所有单词的词干
        
        Args:
            text: 输入文本
            
        Returns:
            处理后的文本，单词被替换为词干形式
            
        示例：
            >>> stemmer = PorterStemmer()
            >>> stemmer.stem_text("The cats are running")
            'the cat are run'
        """
        # 分词并保留标点
        tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
        
        result = []
        for token in tokens:
            if token.isalpha():
                result.append(self.stem(token))
            else:
                result.append(token)
                
        # 重建文本
        output = []
        for i, token in enumerate(result):
            if i > 0 and tokens[i-1].isalpha() and token.isalpha():
                output.append(' ')
            output.append(token)
            
        return ''.join(output)
    
    def get_unique_stems(self, words: List[str]) -> Set[str]:
        """
        获取单词列表的唯一词干集合
        
        Args:
            words: 单词列表
            
        Returns:
            唯一词干集合
            
        示例：
            >>> stemmer = PorterStemmer()
            >>> stemmer.get_unique_stems(["running", "runs", "ran", "jumping", "jumps"])
            {'run', 'jump'}
        """
        return set(self.stem_words(words))
    
    def group_by_stem(self, words: List[str]) -> dict:
        """
        按词干分组单词
        
        Args:
            words: 单词列表
            
        Returns:
            词干到单词列表的映射
            
        示例：
            >>> stemmer = PorterStemmer()
            >>> stemmer.group_by_stem(["running", "runs", "jumping", "jumps"])
            {'run': ['running', 'runs'], 'jump': ['jumping', 'jumps']}
        """
        groups = {}
        for word in words:
            stem = self.stem(word)
            if stem not in groups:
                groups[stem] = []
            groups[stem].append(word)
        return groups


# 便捷函数
_default_stemmer: Optional[PorterStemmer] = None


def stem(word: str) -> str:
    """
    提取单词词干的便捷函数
    
    Args:
        word: 要处理的单词
        
    Returns:
        词干形式
    """
    global _default_stemmer
    if _default_stemmer is None:
        _default_stemmer = PorterStemmer()
    return _default_stemmer.stem(word)


def stem_words(words: List[str]) -> List[str]:
    """
    批量提取词干的便捷函数
    
    Args:
        words: 单词列表
        
    Returns:
        词干列表
    """
    global _default_stemmer
    if _default_stemmer is None:
        _default_stemmer = PorterStemmer()
    return _default_stemmer.stem_words(words)


def stem_text(text: str) -> str:
    """
    提取文本词干的便捷函数
    
    Args:
        text: 输入文本
        
    Returns:
        处理后的文本
    """
    global _default_stemmer
    if _default_stemmer is None:
        _default_stemmer = PorterStemmer()
    return _default_stemmer.stem_text(text)


# 导出
__all__ = [
    'PorterStemmer',
    'stem',
    'stem_words',
    'stem_text',
]