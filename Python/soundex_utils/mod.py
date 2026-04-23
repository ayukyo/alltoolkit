"""
SOUNDEX 语音编码工具模块

SOUNDEX 是一种语音算法，用于按发音索引姓名。由 Robert C. Russell 于1918年发明，
广泛用于家谱研究、姓名匹配和模糊字符串匹配。

功能特点:
- 标准 SOUNDEX 编码（美国人口普查局版本）
- 增强 SOUNEX 变体（处理前缀和特殊字符）
- 姓名相似度比较
- 批量编码和匹配
- 支持多语言字符转写

零外部依赖，纯 Python 实现。
"""

from typing import Optional, List, Tuple, Dict, Set
import re
import unicodedata


class SoundexEncoder:
    """
    SOUNDEX 编码器类
    
    提供完整的 SOUNDEX 编码功能，支持自定义规则和变体。
    
    示例:
        >>> encoder = SoundexEncoder()
        >>> encoder.encode("Smith")
        'S530'
        >>> encoder.encode("Smythe")
        'S530'
    """
    
    # 标准 SOUNDEX 编码映射表
    # 1: B, F, P, V
    # 2: C, G, J, K, Q, S, X, Z
    # 3: D, T
    # 4: L
    # 5: M, N
    # 6: R
    # 注意: A, E, I, O, U, H, W, Y 不编码（作为分隔符）
    
    STANDARD_MAPPING = {
        'b': '1', 'f': '1', 'p': '1', 'v': '1',
        'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
        'd': '3', 't': '3',
        'l': '4',
        'm': '5', 'n': '5',
        'r': '6',
    }
    
    # 特殊字符转写映射（处理多语言字符）
    TRANSLITERATION = {
        'ä': 'a', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'å': 'a',
        'ë': 'e', 'è': 'e', 'é': 'e', 'ê': 'e',
        'ï': 'i', 'ì': 'i', 'í': 'i', 'î': 'i',
        'ö': 'o', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ø': 'o',
        'ü': 'u', 'ù': 'u', 'ú': 'u', 'û': 'u',
        'ç': 's', 'č': 'c', 'ć': 'c',
        'ñ': 'n', 'ń': 'n',
        'ß': 'ss',
        'ž': 'z', 'ź': 'z', 'ż': 'z',
        'š': 's', 'ś': 's',
        'đ': 'd',
        'ł': 'l',
        'ř': 'r',
    }
    
    def __init__(self, length: int = 4, enhanced: bool = False):
        """
        初始化 SOUNDEX 编码器
        
        Args:
            length: 输出编码长度，默认为 4
            enhanced: 是否使用增强模式（处理前缀如 'Mc', 'Mac'）
        """
        self.length = length
        self.enhanced = enhanced
        self._mapping = self.STANDARD_MAPPING.copy()
        self._transliteration = self.TRANSLITERATION.copy()
    
    def _transliterate(self, text: str) -> str:
        """将非 ASCII 字符转写为 ASCII 字符"""
        result = []
        for char in text.lower():
            if char in self._transliteration:
                result.append(self._transliteration[char])
            elif ord(char) < 128:
                result.append(char)
            else:
                # 使用 Unicode 标准化
                normalized = unicodedata.normalize('NFKD', char)
                ascii_char = ''.join(c for c in normalized if ord(c) < 128)
                result.append(ascii_char if ascii_char else '?')
        return ''.join(result)
    
    def _preprocess(self, name: str) -> str:
        """预处理姓名字符串"""
        # 转写非 ASCII 字符
        name = self._transliterate(name)
        # 移除非字母字符
        name = re.sub(r'[^a-zA-Z]', '', name)
        return name
    
    def _handle_enhanced_prefix(self, name: str) -> str:
        """处理增强模式下的特殊前缀"""
        if not self.enhanced:
            return name
        
        # 处理 Mc 和 Mac 前缀
        lower_name = name.lower()
        if lower_name.startswith('mc') and len(name) > 2:
            # Mc 后面的字母大写，如 McDonald
            return 'Mac' + name[2:]
        elif lower_name.startswith('mac') and len(name) > 3:
            # 保持 Mac 前缀一致
            return 'Mac' + name[3:]
        
        return name
    
    def encode(self, name: str) -> str:
        """
        将姓名编码为 SOUNDEX 代码
        
        Args:
            name: 要编码的姓名
            
        Returns:
            SOUNDEX 编码字符串
            
        示例:
            >>> encoder = SoundexEncoder()
            >>> encoder.encode("Robert")
            'R163'
            >>> encoder.encode("Rupert")
            'R163'
        """
        if not name:
            return ''
        
        # 预处理
        name = self._preprocess(name)
        if not name:
            return ''
        
        # 增强前缀处理
        name = self._handle_enhanced_prefix(name)
        
        # 保留首字母
        first_letter = name[0].upper()
        
        # 编码剩余字母
        coded = []
        prev_code = self._mapping.get(name[0].lower(), '')
        
        for char in name[1:]:
            code = self._mapping.get(char.lower(), '')
            
            # 跳过元音和 H, W（它们作为分隔符）
            if char.lower() in 'aeiouhw':
                prev_code = ''  # 重置前一个编码
                continue
            
            # 如果当前编码不同于前一个编码（排除相邻重复）
            if code and code != prev_code:
                coded.append(code)
            elif char.lower() in 'aeiouy':
                prev_code = ''
            
            prev_code = code
        
        # 组合结果
        result = first_letter + ''.join(coded)
        
        # 填充或截断到指定长度
        result = result[:self.length]
        result = result.ljust(self.length, '0')
        
        return result
    
    def encode_batch(self, names: List[str]) -> Dict[str, str]:
        """
        批量编码姓名
        
        Args:
            names: 姓名列表
            
        Returns:
            姓名到编码的映射字典
        """
        return {name: self.encode(name) for name in names}
    
    def similarity(self, name1: str, name2: str) -> float:
        """
        计算两个姓名的 SOUNDEX 相似度
        
        Args:
            name1: 第一个姓名
            name2: 第二个姓名
            
        Returns:
            相似度分数（0.0 到 1.0）
        """
        code1 = self.encode(name1)
        code2 = self.encode(name2)
        
        if not code1 or not code2:
            return 0.0
        
        if code1 == code2:
            return 1.0
        
        # 计算编码差异
        matches = sum(1 for c1, c2 in zip(code1, code2) if c1 == c2)
        return matches / self.length
    
    def matches(self, name1: str, name2: str, threshold: float = 1.0) -> bool:
        """
        判断两个姓名是否匹配
        
        Args:
            name1: 第一个姓名
            name2: 第二一个姓名
            threshold: 匹配阈值（默认 1.0 表示完全相同编码）
            
        Returns:
            是否匹配
        """
        return self.similarity(name1, name2) >= threshold
    
    def find_similar(self, target: str, candidates: List[str], 
                     threshold: float = 0.75) -> List[Tuple[str, float]]:
        """
        在候选列表中查找与目标相似的姓名
        
        Args:
            target: 目标姓名
            candidates: 候选姓名列表
            threshold: 相似度阈值
            
        Returns:
            匹配的姓名和相似度列表，按相似度降序排列
        """
        results = []
        target_code = self.encode(target)
        
        for candidate in candidates:
            score = self.similarity(target, candidate)
            if score >= threshold:
                results.append((candidate, score))
        
        # 按相似度降序排序
        results.sort(key=lambda x: (-x[1], x[0]))
        return results
    
    def group_by_code(self, names: List[str]) -> Dict[str, List[str]]:
        """
        按编码将姓名分组
        
        Args:
            names: 姓名列表
            
        Returns:
            编码到姓名列表的映射
        """
        groups: Dict[str, List[str]] = {}
        for name in names:
            code = self.encode(name)
            if code not in groups:
                groups[code] = []
            groups[code].append(name)
        return groups
    
    def get_phonetic_variants(self, code: str) -> List[str]:
        """
        获取给定编码可能的语音变体字母组合
        
        Args:
            code: SOUNDEX 编码
            
        Returns:
            可能的字母组合列表
        """
        reverse_mapping = {
            '1': ['B', 'F', 'P', 'V'],
            '2': ['C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z'],
            '3': ['D', 'T'],
            '4': ['L'],
            '5': ['M', 'N'],
            '6': ['R'],
            '0': [''],
        }
        
        if not code or len(code) < 1:
            return []
        
        variants = [[code[0]]]  # 首字母保持不变
        
        for digit in code[1:]:
            if digit in reverse_mapping:
                variants.append(reverse_mapping[digit])
            else:
                variants.append([''])
        
        # 生成所有组合（限制数量以避免爆炸）
        result = ['']
        for letters in variants:
            new_result = []
            for prefix in result:
                for letter in letters:
                    new_result.append(prefix + letter)
                    if len(new_result) > 1000:  # 限制数量
                        break
                if len(new_result) > 1000:
                    break
            result = new_result
        
        return result[:100]


class SoundexRefinedEncoder(SoundexEncoder):
    """
    改进的 SOUNDEX 编码器（Refined Soundex）
    
    使用更精细的编码映射，减少误匹配。
    
    示例:
        >>> encoder = SoundexRefinedEncoder()
        >>> encoder.encode("Smith")
        'S5300'
    """
    
    # 改进的编码映射（更精细）
    REFINED_MAPPING = {
        'b': '1', 'p': '1',
        'f': '2', 'v': '2',
        'c': '3', 's': '3', 'k': '3', 'g': '3', 'j': '3', 'q': '3', 'x': '3', 'z': '3',
        'd': '4', 't': '4',
        'l': '5',
        'm': '6', 'n': '6',
        'r': '7',
    }
    
    def __init__(self, length: int = 5, enhanced: bool = False):
        super().__init__(length=length, enhanced=enhanced)
        self._mapping = self.REFINED_MAPPING.copy()


class SoundexSQL:
    """
    SOUNDEX SQL 辅助工具类
    
    提供 SQL 数据库相关的 SOUNDEX 功能。
    """
    
    @staticmethod
    def where_clause(column: str, value: str) -> str:
        """
        生成 SOUNDEX 匹配的 WHERE 子句
        
        Args:
            column: 数据库列名
            value: 要匹配的值
            
        Returns:
            SQL WHERE 子句片段
        """
        # 使用标准 SQL SOUNDEX 函数
        return f"SOUNDEX({column}) = SOUNDEX('{value}')"
    
    @staticmethod
    def create_index_sql(table: str, column: str) -> str:
        """
        生成创建 SOUNDEX 索引的 SQL 语句
        
        Args:
            table: 表名
            column: 列名
            
        Returns:
            CREATE INDEX SQL 语句
        """
        index_name = f"idx_soundex_{table}_{column}"
        return f"CREATE INDEX {index_name} ON {table} (SOUNDEX({column}))"


# 便捷函数
_default_encoder = SoundexEncoder()


def encode(name: str) -> str:
    """
    使用默认编码器编码姓名
    
    Args:
        name: 要编码的姓名
        
    Returns:
        SOUNDEX 编码
    """
    return _default_encoder.encode(name)


def similarity(name1: str, name2: str) -> float:
    """
    计算两个姓名的相似度
    
    Args:
        name1: 第一个姓名
        name2: 第二一个姓名
        
    Returns:
        相似度分数（0.0 到 1.0）
    """
    return _default_encoder.similarity(name1, name2)


def matches(name1: str, name2: str, threshold: float = 1.0) -> bool:
    """
    判断两个姓名是否匹配
    
    Args:
        name1: 第一个姓名
        name2: 第二一个姓名
        threshold: 匹配阈值
        
    Returns:
        是否匹配
    """
    return _default_encoder.matches(name1, name2, threshold)


def find_similar(target: str, candidates: List[str], 
                 threshold: float = 0.75) -> List[Tuple[str, float]]:
    """
    在候选列表中查找与目标相似的姓名
    
    Args:
        target: 目标姓名
        candidates: 候选姓名列表
        threshold: 相似度阈值
        
    Returns:
        匹配结果列表
    """
    return _default_encoder.find_similar(target, candidates, threshold)


def group_by_sound(names: List[str]) -> Dict[str, List[str]]:
    """
    按发音将姓名分组
    
    Args:
        names: 姓名列表
        
    Returns:
        发音分组
    """
    return _default_encoder.group_by_code(names)


# 常见姓名的 SOUNDEX 编码示例
COMMON_NAMES = {
    'Smith': 'S530',
    'Smythe': 'S530',
    'Schmidt': 'S530',
    'Johnson': 'J525',
    'Johnston': 'J525',
    'Williams': 'W452',
    'Wilson': 'W425',
    'Brown': 'B650',
    'Browne': 'B650',
    'Davis': 'D120',
    'Davies': 'D120',
    'Miller': 'M460',
    'Mueller': 'M460',
    'Muller': 'M460',
    'Taylor': 'T460',
    'Anderson': 'A536',
    'Thomas': 'T520',
    'Thompson': 'T512',
    'Garcia': 'G620',
    'Martinez': 'M635',
    'Robinson': 'R152',
    'Clark': 'C462',
    'Clarke': 'C462',
    'Rodriguez': 'R362',
    'Lewis': 'L200',
    'Lee': 'L000',
    'Walker': 'W426',
    'Hall': 'H400',
    'Allen': 'A450',
    'Young': 'Y520',
    'King': 'K520',
}


def get_common_code(name: str) -> Optional[str]:
    """
    获取常见姓名的 SOUNDEX 编码
    
    Args:
        name: 姓名
        
    Returns:
        编码（如果姓名在常见列表中）或 None
    """
    return COMMON_NAMES.get(name)


if __name__ == '__main__':
    # 简单演示
    encoder = SoundexEncoder()
    
    print("SOUNDEX 编码示例:")
    test_names = ['Smith', 'Smythe', 'Schmidt', 'Johnson', 'Williams', 'Brown']
    for name in test_names:
        print(f"  {name} -> {encoder.encode(name)}")
    
    print("\n姓名相似度:")
    pairs = [('Smith', 'Smythe'), ('Smith', 'Schmidt'), ('Johnson', 'Johnston')]
    for n1, n2 in pairs:
        sim = encoder.similarity(n1, n2)
        match = encoder.matches(n1, n2)
        print(f"  {n1} vs {n2}: 相似度={sim:.2f}, 匹配={match}")
    
    print("\n姓名分组:")
    names = ['Smith', 'Smythe', 'Johnson', 'Johnston', 'Brown', 'Browne']
    groups = encoder.group_by_code(names)
    for code, group in groups.items():
        print(f"  {code}: {group}")