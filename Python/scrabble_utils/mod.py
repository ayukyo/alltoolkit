"""
Scrabble Word Score Utils - 英语单词 Scrabble 评分工具

提供 Scrabble 游戏的单词评分、验证和策略分析功能。
零外部依赖，纯 Python 实现。

功能：
- 单词分数计算（标准 Scrabble 规则）
- 字母分数映射
- 双倍/三倍字母/单词分数计算
- Bingo 奖励（使用全部 7 个字母）
- 最佳单词推荐
- 可能单词生成（给定字母）
- 字母分布统计
- 英文字母频率分析
"""

from typing import List, Dict, Tuple, Set, Optional, Generator
from collections import defaultdict
from itertools import permutations, combinations
import re


# 标准 Scrabble 字母分数（英文字母）
LETTER_VALUES = {
    'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1, 'L': 1, 'N': 1, 'S': 1, 'T': 1, 'R': 1,
    'D': 2, 'G': 2,
    'B': 3, 'C': 3, 'M': 3, 'P': 3,
    'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
    'K': 5,
    'J': 8, 'X': 8,
    'Q': 10, 'Z': 10,
}

# 标准 Scrabble 字母分布（总共 100 个字母）
LETTER_DISTRIBUTION = {
    'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2,
    'I': 9, 'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6, 'O': 8, 'P': 2,
    'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1,
    'Y': 2, 'Z': 1,
}

# 空白牌（Wild card）数量
BLANK_COUNT = 2

# 英语字母频率（用于词频分析）
ENGLISH_FREQUENCY = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07,
}


class ScrabbleTile:
    """Scrabble 字母牌"""
    
    def __init__(self, letter: str, is_blank: bool = False):
        """
        初始化字母牌
        
        Args:
            letter: 字母（A-Z 或空白牌代表的字母）
            is_blank: 是否为空白牌
        """
        self.letter = letter.upper() if letter else ''
        self.is_blank = is_blank
    
    def value(self) -> int:
        """获取字母牌的分数"""
        if self.is_blank:
            return 0
        return LETTER_VALUES.get(self.letter, 0)
    
    def __str__(self) -> str:
        if self.is_blank:
            return f"[{self.letter}]"  # 空白牌显示为 [字母]
        return self.letter
    
    def __repr__(self) -> str:
        return f"ScrabbleTile('{self.letter}', is_blank={self.is_blank})"


class BoardPosition:
    """棋盘位置"""
    
    def __init__(self, row: int, col: int, multiplier: str = 'normal'):
        """
        初始化棋盘位置
        
        Args:
            row: 行号（0-14）
            col: 列号（0-14）
            multiplier: 分数乘数类型
                - 'normal': 普通
                - 'dl': 双倍字母 (Double Letter)
                - 'tl': 三倍字母 (Triple Letter)
                - 'dw': 双倍单词 (Double Word)
                - 'tw': 三倍单词 (Triple Word)
        """
        self.row = row
        self.col = col
        self.multiplier = multiplier
    
    def letter_multiplier(self) -> int:
        """获取字母分数乘数"""
        if self.multiplier == 'dl':
            return 2
        elif self.multiplier == 'tl':
            return 3
        return 1
    
    def word_multiplier(self) -> int:
        """获取单词分数乘数"""
        if self.multiplier == 'dw':
            return 2
        elif self.multiplier == 'tw':
            return 3
        return 1
    
    def __str__(self) -> str:
        return f"({self.row}, {self.col}) [{self.multiplier}]"


class ScrabbleWord:
    """Scrabble 单词"""
    
    def __init__(self, tiles: List[ScrabbleTile], positions: List[BoardPosition]):
        """
        初始化单词
        
        Args:
            tiles: 字母牌列表
            positions: 对应的棋盘位置列表
        """
        self.tiles = tiles
        self.positions = positions
        self._word_str = ''.join(t.letter for t in tiles)
    
    def word_string(self) -> str:
        """获取单词字符串"""
        return self._word_str
    
    def base_score(self) -> int:
        """计算基础分数（不含位置乘数）"""
        return sum(tile.value() for tile in self.tiles)
    
    def calculate_score(self, include_bingo: bool = False) -> int:
        """
        计算完整分数
        
        Args:
            include_bingo: 是否包含 Bingo 奖励（使用全部 7 个字母）
        
        Returns:
            总分数
        """
        if len(self.tiles) != len(self.positions):
            raise ValueError("字母牌数量与位置数量不匹配")
        
        letter_score = 0
        word_multiplier = 1
        
        for tile, pos in zip(self.tiles, self.positions):
            # 字母分数 × 字母乘数
            letter_score += tile.value() * pos.letter_multiplier()
            # 收集单词乘数
            word_multiplier *= pos.word_multiplier()
        
        total = letter_score * word_multiplier
        
        # Bingo 奖励：使用全部 7 个字母牌加 50 分
        if include_bingo and len(self.tiles) == 7:
            total += 50
        
        return total
    
    def __str__(self) -> str:
        return f"{self._word_str} ({self.calculate_score()}分)"


def letter_score(letter: str) -> int:
    """
    获取单个字母的 Scrabble 分数
    
    Args:
        letter: 字母（A-Z）
    
    Returns:
        字母分数
    
    Examples:
        >>> letter_score('A')
        1
        >>> letter_score('Q')
        10
        >>> letter_score('Z')
        10
    """
    return LETTER_VALUES.get(letter.upper(), 0)


def word_score(word: str, use_blanks: List[int] = None) -> int:
    """
    计算单词的基础分数
    
    Args:
        word: 单词字符串
        use_blanks: 使用空白牌的字母位置列表（这些位置分数为 0）
    
    Returns:
        单词分数
    
    Examples:
        >>> word_score('QUIZ')
        22
        >>> word_score('CAT')
        5
        >>> word_score('QUICK', use_blanks=[1])  # 用空白牌代替 U
        20
    """
    total = 0
    for i, letter in enumerate(word.upper()):
        if use_blanks and i in use_blanks:
            continue  # 空白牌分数为 0
        total += LETTER_VALUES.get(letter, 0)
    return total


def calculate_word_with_multipliers(
    word: str,
    letter_multipliers: List[int] = None,
    word_multipliers: List[int] = None,
    use_blanks: List[int] = None,
    bingo: bool = False
) -> int:
    """
    计算带乘数的单词分数
    
    Args:
        word: 单词字符串
        letter_multipliers: 每个字母的乘数列表（默认全为 1）
        word_multipliers: 单词乘数列表（会相乘）
        use_blanks: 空白牌位置列表
        bingo: 是否添加 Bingo 奖励
    
    Returns:
        总分数
    
    Examples:
        >>> calculate_word_with_multipliers('CAT')
        5
        >>> calculate_word_with_multipliers('CAT', letter_multipliers=[2, 1, 1])
        6  # C 在双倍字母位置
        >>> calculate_word_with_multipliers('CAT', word_multipliers=[2])
        10  # 双倍单词
        >>> calculate_word_with_multipliers('CAT', letter_multipliers=[2, 1, 1], word_multipliers=[2])
        12
    """
    word = word.upper()
    n = len(word)
    
    if letter_multipliers is None:
        letter_multipliers = [1] * n
    if word_multipliers is None:
        word_multipliers = [1]
    
    # 计算字母分数（含字母乘数）
    letter_score = 0
    for i, letter in enumerate(word):
        if use_blanks and i in use_blanks:
            letter_value = 0
        else:
            letter_value = LETTER_VALUES.get(letter, 0)
        letter_score += letter_value * letter_multipliers[i]
    
    # 应用单词乘数
    word_multiplier = 1
    for m in word_multipliers:
        word_multiplier *= m
    
    total = letter_score * word_multiplier
    
    # Bingo 奖励
    if bingo and n == 7:
        total += 50
    
    return total


def get_standard_board() -> List[List[BoardPosition]]:
    """
    获取标准 Scrabble 棋盘布局
    
    Returns:
        15x15 棋盘位置矩阵
    
    Board layout:
        - TW (Triple Word): (0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)
        - DW (Double Word): (1,1), (1,13), (2,2), (2,12), (3,3), (3,11), (4,4), (4,10),
                           (7,7), (10,4), (10,10), (11,3), (11,11), (12,2), (12,12), (13,1), (13,13)
        - TL (Triple Letter): (1,5), (1,9), (3,7), (5,1), (5,5), (5,9), (5,13), (7,3), (7,11),
                              (9,1), (9,5), (9,9), (9,13), (11,7), (13,5), (13,9)
        - DL (Double Letter): (0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6),
                              (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0),
                              (11,7), (11,14), (12,6), (12,8), (14,3), (14,11)
    """
    board = [[BoardPosition(r, c, 'normal') for c in range(15)] for r in range(15)]
    
    # Triple Word positions
    tw_positions = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
    for r, c in tw_positions:
        board[r][c].multiplier = 'tw'
    
    # Double Word positions
    dw_positions = [
        (1, 1), (1, 13), (2, 2), (2, 12), (3, 3), (3, 11), (4, 4), (4, 10),
        (7, 7),
        (10, 4), (10, 10), (11, 3), (11, 11), (12, 2), (12, 12), (13, 1), (13, 13)
    ]
    for r, c in dw_positions:
        board[r][c].multiplier = 'dw'
    
    # Triple Letter positions
    tl_positions = [
        (1, 5), (1, 9), (3, 7), (5, 1), (5, 5), (5, 9), (5, 13), (7, 3), (7, 11),
        (9, 1), (9, 5), (9, 9), (9, 13), (11, 7), (13, 5), (13, 9)
    ]
    for r, c in tl_positions:
        board[r][c].multiplier = 'tl'
    
    # Double Letter positions
    dl_positions = [
        (0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6),
        (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0),
        (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)
    ]
    for r, c in dl_positions:
        board[r][c].multiplier = 'dl'
    
    return board


def remaining_tiles(used_letters: Dict[str, int]) -> Dict[str, int]:
    """
    计算剩余字母牌数量
    
    Args:
        used_letters: 已使用的字母数量字典
    
    Returns:
        剩余字母数量字典
    
    Examples:
        >>> remaining_tiles({'A': 3, 'E': 5})
        {'A': 6, 'E': 7, ...}
    """
    remaining = {}
    for letter, total in LETTER_DISTRIBUTION.items():
        used = used_letters.get(letter, 0)
        remaining[letter] = total - used
    return remaining


def draw_random_tiles(count: int, available: Dict[str, int] = None) -> List[str]:
    """
    随机抽取字母牌
    
    Args:
        count: 抽取数量
        available: 可用字母池（默认使用完整分布）
    
    Returns:
        抽取的字母列表
    
    注意：此函数使用标准 random 模块，如需确定性结果请设置随机种子
    """
    import random
    
    if available is None:
        available = LETTER_DISTRIBUTION.copy()
    
    # 构建字母池
    pool = []
    for letter, count in available.items():
        pool.extend([letter] * count)
    
    if count > len(pool):
        raise ValueError(f"字母池不足：需要 {count}，仅有 {len(pool)}")
    
    # 随机抽取
    return random.sample(pool, count)


def can_form_word(word: str, available_letters: List[str], has_blank: bool = False) -> Tuple[bool, List[int]]:
    """
    检查是否可以用给定字母组成单词
    
    Args:
        word: 目标单词
        available_letters: 可用字母列表
        has_blank: 是否有空白牌
    
    Returns:
        (是否可以组成, 需要使用空白牌的位置列表)
    
    Examples:
        >>> can_form_word('CAT', ['C', 'A', 'T'])
        (True, [])
        >>> can_form_word('QUICK', ['Q', 'I', 'C', 'K'], has_blank=True)
        (True, [1])  # 需要用空白牌代替 U
    """
    word = word.upper()
    available = [l.upper() for l in available_letters]
    
    letter_counts = defaultdict(int)
    for letter in available:
        letter_counts[letter] += 1
    
    blank_positions = []
    
    for i, letter in enumerate(word):
        if letter_counts[letter] > 0:
            letter_counts[letter] -= 1
        elif has_blank:
            blank_positions.append(i)
            has_blank = False  # 只有一张空白牌
        else:
            return (False, [])
    
    return (True, blank_positions)


def generate_possible_words(letters: List[str], max_length: int = None, has_blank: bool = False) -> Generator[str, None, None]:
    """
    从给定字母生成所有可能的单词排列
    
    Args:
        letters: 可用字母列表
        max_length: 最大单词长度（默认为字母数量）
        has_blank: 是否有空白牌
    
    Returns:
        所有可能的单词排列生成器
    
    注意：此函数仅生成排列，不验证是否为有效英语单词
    """
    if max_length is None:
        max_length = len(letters)
    
    letters = [l.upper() for l in letters]
    
    # 不含空白牌：直接生成排列
    if not has_blank:
        for length in range(2, min(max_length + 1, len(letters) + 1)):
            for perm in permutations(letters, length):
                yield ''.join(perm)
    else:
        # 含空白牌：为每个位置尝试所有字母
        for length in range(2, min(max_length + 1, len(letters) + 1)):
            for perm in permutations(letters, length):
                base_word = ''.join(perm)
                # 尝试将空白牌位置替换为任意字母
                for i in range(length):
                    for replacement in LETTER_VALUES.keys():
                        word = base_word[:i] + replacement + base_word[i+1:]
                        yield word


def letter_frequency_analysis(word: str) -> Dict[str, Tuple[int, float]]:
    """
    分析单词中字母的频率和稀有度
    
    Args:
        word: 单词
    
    Returns:
        字母到 (出现次数, 稀有度分数) 的映射
    
    稀有度分数越高表示字母越稀有
    """
    word = word.upper()
    
    result = {}
    letter_counts = defaultdict(int)
    for letter in word:
        letter_counts[letter] += 1
    
    for letter, count in letter_counts.items():
        # 稀有度 = 100 - 英文频率百分比
        frequency = ENGLISH_FREQUENCY.get(letter, 0)
        rarity = 100 - frequency
        result[letter] = (count, rarity)
    
    return result


def word_difficulty_score(word: str) -> float:
    """
    计算单词的难度分数
    
    Args:
        word: 单词
    
    Returns:
        难度分数（0-100），越高越难
    
    基于字母稀有度、分数分布和长度计算
    """
    word = word.upper()
    if not word:
        return 0
    
    # 字母分数总和
    total_value = sum(LETTER_VALUES.get(l, 0) for l in word)
    
    # 平均字母分数
    avg_value = total_value / len(word)
    
    # 稀有字母比例（分数 >= 4 的字母）
    rare_letters = sum(1 for l in word if LETTER_VALUES.get(l, 0) >= 4)
    rare_ratio = rare_letters / len(word)
    
    # 长度惩罚（长单词更难）
    length_factor = min(len(word) / 7, 1.0)
    
    # 综合难度分数
    difficulty = (avg_value * 10) + (rare_ratio * 50) + (length_factor * 20)
    
    return min(difficulty, 100)


def tile_distribution_summary() -> Dict[str, Dict]:
    """
    获取字母牌分布摘要
    
    Returns:
        字母分布信息字典
    """
    summary = {}
    for letter, count in LETTER_DISTRIBUTION.items():
        value = LETTER_VALUES.get(letter, 0)
        frequency = ENGLISH_FREQUENCY.get(letter, 0)
        summary[letter] = {
            'count': count,
            'value': value,
            'frequency': frequency,
            'total_value': value * count,
        }
    
    return summary


def high_value_letters(min_value: int = 5) -> List[str]:
    """
    获取高价值字母列表
    
    Args:
        min_value: 最低分数阈值
    
    Returns:
        高价值字母列表
    """
    return [letter for letter, value in LETTER_VALUES.items() if value >= min_value]


def rare_letters(min_count: int = 2) -> List[str]:
    """
    获取稀有字母列表（牌数少）
    
    Args:
        min_count: 最大牌数阈值
    
    Returns:
        稀有字母列表
    """
    return [letter for letter, count in LETTER_DISTRIBUTION.items() if count <= min_count]


def score_distribution() -> Dict[int, List[str]]:
    """
    按分数分组字母
    
    Returns:
        分数到字母列表的映射
    """
    distribution = defaultdict(list)
    for letter, value in LETTER_VALUES.items():
        distribution[value].append(letter)
    
    return dict(sorted(distribution.items()))


def validate_scrabble_word(word: str) -> Tuple[bool, str]:
    """
    验证单词是否符合 Scrabble 规则
    
    Args:
        word: 单词
    
    Returns:
        (是否有效, 错误信息)
    """
    word = word.upper()
    
    # 检查是否为空
    if not word:
        return (False, "单词不能为空")
    
    # 检查长度（Scrabble 最短单词为 2 字母）
    if len(word) < 2:
        return (False, "单词长度至少为 2")
    
    # 检查长度（Scrabble 最长单词为 15 字母，棋盘宽度）
    if len(word) > 15:
        return (False, "单词长度不能超过 15")
    
    # 检查是否只包含字母
    if not word.isalpha():
        return (False, "单词只能包含字母 A-Z")
    
    return (True, "")


def best_placement_score(word: str, board: List[List[BoardPosition]] = None) -> Tuple[int, List[Tuple[int, int]]]:
    """
    计算单词在棋盘上的最佳放置分数
    
    Args:
        word: 单词
        board: 棋盘（默认使用标准棋盘）
    
    Returns:
        (最高分数, 最佳放置位置列表)
    """
    if board is None:
        board = get_standard_board()
    
    word = word.upper()
    n = len(word)
    
    best_score = 0
    best_positions = []
    
    # 尝试水平放置
    for row in range(15):
        for col in range(15 - n + 1):
            positions = [board[row][col + i] for i in range(n)]
            score = calculate_word_with_multipliers(
                word,
                letter_multipliers=[p.letter_multiplier() for p in positions],
                word_multipliers=[p.word_multiplier() for p in positions if p.word_multiplier() > 1],
                bingo=(n == 7)
            )
            if score > best_score:
                best_score = score
                best_positions = [(row, col + i) for i in range(n)]
    
    # 尝试垂直放置
    for col in range(15):
        for row in range(15 - n + 1):
            positions = [board[row + i][col] for i in range(n)]
            score = calculate_word_with_multipliers(
                word,
                letter_multipliers=[p.letter_multiplier() for p in positions],
                word_multipliers=[p.word_multiplier() for p in positions if p.word_multiplier() > 1],
                bingo=(n == 7)
            )
            if score > best_score:
                best_score = score
                best_positions = [(row + i, col) for i in range(n)]
    
    return (best_score, best_positions)


def word_rank_by_score(words: List[str]) -> List[Tuple[str, int]]:
    """
    按分数排序单词
    
    Args:
        words: 单词列表
    
    Returns:
        (单词, 分数) 列表，按分数降序
    """
    scored = [(word, word_score(word)) for word in words]
    return sorted(scored, key=lambda x: -x[1])


def letter_rack_analysis(rack: List[str]) -> Dict:
    """
    分析字母 Rack 的潜力
    
    Args:
        rack: 字母列表（玩家手中的字母）
    
    Returns:
        分析结果字典
    """
    rack = [l.upper() for l in rack]
    
    # 基础统计
    total_value = sum(LETTER_VALUES.get(l, 0) for l in rack)
    
    # 高价值字母
    high_value = [l for l in rack if LETTER_VALUES.get(l, 0) >= 5]
    
    # 稀有字母
    rare = [l for l in rack if LETTER_DISTRIBUTION.get(l, 0) <= 2]
    
    # 常见字母（便于组合）
    common = [l for l in rack if ENGLISH_FREQUENCY.get(l, 0) >= 6]
    
    # 字母分布
    distribution = defaultdict(int)
    for l in rack:
        distribution[l] += 1
    
    # Bingo 潜力（7 字母）
    bingo_potential = len(rack) == 7
    
    # 平衡度分数（高分字母和常见字母的平衡）
    balance_score = (len(common) / len(rack) * 50) + (len(high_value) / len(rack) * 50)
    
    return {
        'total_value': total_value,
        'high_value_letters': high_value,
        'rare_letters': rare,
        'common_letters': common,
        'distribution': dict(distribution),
        'bingo_potential': bingo_potential,
        'balance_score': balance_score,
        'avg_value': total_value / len(rack) if rack else 0,
    }


# 便捷函数
def score(word: str) -> int:
    """快速计算单词分数"""
    return word_score(word)


def high_score_words(min_score: int = 20) -> List[str]:
    """
    获取高分数单词示例（常用高价值单词）
    
    Args:
        min_score: 最低分数
    
    Returns:
        高分数单词列表
    """
    # 一些高分单词示例
    examples = [
        'QUICKLY', 'JAZZY', 'QUIZ', 'ZAX', 'JINX', 'JOKE',
        'ZOMBIE', 'QUARTZ', 'SQUEEZED', 'JACUZZI',
        'QUIZZIFY', 'MAXIMIZE', 'EXERCIZE',
    ]
    
    return [w for w in examples if word_score(w) >= min_score]


if __name__ == "__main__":
    print("=== Scrabble 单词分数计算 ===")
    
    # 基础分数
    words = ['CAT', 'DOG', 'QUICK', 'JAZZY', 'QUIZ', 'ZOO']
    for word in words:
        print(f"{word}: {word_score(word)} 分")
    
    print("\n=== 字母分数分布 ===")
    for value, letters in score_distribution().items():
        print(f"{value} 分: {', '.join(letters)}")
    
    print("\n=== 高价值字母 ===")
    print(f"分数 >= 5: {', '.join(high_value_letters(5))}")
    print(f"分数 >= 8: {', '.join(high_value_letters(8))}")
    
    print("\n=== 稀有字母 ===")
    print(f"牌数 <= 2: {', '.join(rare_letters(2))}")
    
    print("\n=== 带乘数的分数计算 ===")
    # CAT 在双倍字母位置
    print(f"CAT (C 在 DL): {calculate_word_with_multipliers('CAT', letter_multipliers=[2, 1, 1])} 分")
    # CAT 在双倍单词位置
    print(f"CAT (在 DW): {calculate_word_with_multipliers('CAT', word_multipliers=[2])} 分")
    # CAT 在三倍单词位置
    print(f"CAT (在 TW): {calculate_word_with_multipliers('CAT', word_multipliers=[3])} 分")
    
    print("\n=== 单词难度分析 ===")
    test_words = ['CAT', 'QUICK', 'JAZZY', 'QUIZZIFY']
    for word in test_words:
        difficulty = word_difficulty_score(word)
        print(f"{word}: 难度 {difficulty:.1f}")
    
    print("\n=== 字母 Rack 分析 ===")
    rack = ['Q', 'U', 'I', 'C', 'K', 'Z', 'A']
    analysis = letter_rack_analysis(rack)
    print(f"Rack: {', '.join(rack)}")
    print(f"总价值: {analysis['total_value']} 分")
    print(f"高价值字母: {', '.join(analysis['high_value_letters'])}")
    print(f"Bingo 潜力: {analysis['bingo_potential']}")
    
    print("\n=== 最佳放置分析 ===")
    word = 'QUICK'
    best_score, best_pos = best_placement_score(word)
    print(f"{word} 最佳分数: {best_score} 分")
    print(f"最佳位置: {best_pos[:3]}...")