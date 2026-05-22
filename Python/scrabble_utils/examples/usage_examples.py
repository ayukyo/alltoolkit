"""
scrabble_utils 使用示例

演示 Scrabble 单词评分工具库的各种功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    letter_score, word_score, calculate_word_with_multipliers,
    get_standard_board, remaining_tiles, can_form_word,
    letter_frequency_analysis, word_difficulty_score,
    tile_distribution_summary, high_value_letters, rare_letters,
    score_distribution, validate_scrabble_word, best_placement_score,
    word_rank_by_score, letter_rack_analysis, score, high_score_words,
    ScrabbleTile, BoardPosition, ScrabbleWord,
    LETTER_VALUES, LETTER_DISTRIBUTION
)


def print_separator(title: str):
    """打印分隔符"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def example_basic_scoring():
    """基础评分示例"""
    print_separator("基础单词评分")
    
    # 单字母分数
    print("字母分数:")
    for letter in ['A', 'B', 'C', 'D', 'E', 'K', 'Q', 'X', 'Z']:
        print(f"  {letter}: {letter_score(letter)} 分")
    
    # 单词分数
    print("\n单词分数:")
    words = ['CAT', 'DOG', 'THE', 'QUICK', 'JAZZY', 'QUIZ', 'ZOO']
    for word in words:
        print(f"  {word}: {word_score(word)} 分")
    
    # 高分单词
    print("\n高分单词示例:")
    for word in high_score_words(30):
        print(f"  {word}: {word_score(word)} 分")


def example_letter_distribution():
    """字母分布示例"""
    print_separator("字母分布分析")
    
    # 分数分布
    print("按分数分组的字母:")
    for value, letters in score_distribution().items():
        print(f"  {value} 分: {', '.join(letters)}")
    
    # 高价值字母
    print("\n高价值字母:")
    print(f"  分数 >= 5: {', '.join(high_value_letters(5))}")
    print(f"  分数 >= 8: {', '.join(high_value_letters(8))}")
    
    # 稀有字母
    print("\n稀有字母:")
    print(f"  牌数 <= 2: {', '.join(rare_letters(2))}")
    print(f"  牌数 <= 1: {', '.join(rare_letters(1))}")
    
    # 字母牌分布摘要
    print("\n字母牌分布摘要:")
    summary = tile_distribution_summary()
    for letter in ['Q', 'Z', 'J', 'X', 'K']:
        info = summary[letter]
        print(f"  {letter}: {info['count']} 张, {info['value']} 分/张, 频率 {info['frequency']}%")


def example_multipliers():
    """乘数评分示例"""
    print_separator("带乘数的分数计算")
    
    # 双倍字母
    print("双倍字母位置 (DL):")
    word = 'CAT'
    base = word_score(word)
    doubled = calculate_word_with_multipliers(word, letter_multipliers=[2, 1, 1])
    print(f"  {word} 基分数: {base}")
    print(f"  {word} (C 在 DL): {doubled}")
    
    # 三倍字母
    print("\n三倍字母位置 (TL):")
    tripled = calculate_word_with_multipliers(word, letter_multipliers=[3, 1, 1])
    print(f"  {word} (C 在 TL): {tripled}")
    
    # 双倍单词
    print("\n双倍单词位置 (DW):")
    dw_score = calculate_word_with_multipliers(word, word_multipliers=[2])
    print(f"  {word} (在 DW): {dw_score}")
    
    # 三倍单词
    print("\n三倍单词位置 (TW):")
    tw_score = calculate_word_with_multipliers(word, word_multipliers=[3])
    print(f"  {word} (在 TW): {tw_score}")
    
    # 组合乘数
    print("\n组合乘数:")
    word = 'QUIZ'
    # Q(10)*3 + U(1) + I(1) + Z(10) = 42, then *2 = 84
    combined = calculate_word_with_multipliers(
        word,
        letter_multipliers=[3, 1, 1, 1],
        word_multipliers=[2]
    )
    print(f"  {word} (Q 在 TL + 整词在 DW): {combined}")
    
    # Bingo 奖励
    print("\nBingo 奖励 (使用 7 个字母):")
    word = 'QUICKLY'
    no_bingo = calculate_word_with_multipliers(word, bingo=False)
    with_bingo = calculate_word_with_multipliers(word, bingo=True)
    print(f"  {word} 无 Bingo: {no_bingo}")
    print(f"  {word} 有 Bingo: {with_bingo} (+50)")


def example_board():
    """棋盘示例"""
    print_separator("标准 Scrabble 棋盘")
    
    board = get_standard_board()
    
    print("棋盘大小: 15 x 15")
    
    # 特殊位置
    print("\n三倍单词位置 (TW):")
    tw_positions = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
    for r, c in tw_positions:
        print(f"  ({r}, {c})")
    
    print("\n双倍单词位置 (DW):")
    dw_positions = [(1, 1), (2, 2), (3, 3), (4, 4), (7, 7)]
    for r, c in dw_positions:
        print(f"  ({r}, {c})")
    
    print("\n中心位置 (Star):")
    center = board[7][7]
    print(f"  (7, 7) - {center.multiplier} (双倍单词)")
    
    # 使用 BoardPosition 和 ScrabbleWord
    print("\n构建 ScrabbleWord:")
    tiles = [
        ScrabbleTile('C'),
        ScrabbleTile('A'),
        ScrabbleTile('T')
    ]
    positions = [
        board[1][1],  # DW
        board[1][2],  # Normal
        board[1][3],  # DL
    ]
    word = ScrabbleWord(tiles, positions)
    print(f"  单词: {word.word_string()}")
    print(f"  基础分数: {word.base_score()}")
    print(f"  实际分数: {word.calculate_score()}")


def example_word_forming():
    """单词组成检查示例"""
    print_separator("单词组成检查")
    
    # 精确匹配
    result, blanks = can_form_word('CAT', ['C', 'A', 'T'])
    print(f"'CAT' 用 ['C', 'A', 'T']: {result}, 空白牌位置: {blanks}")
    
    # 额外字母
    result, blanks = can_form_word('CAT', ['C', 'A', 'T', 'S', 'D', 'O', 'G'])
    print(f"'CAT' 用 ['C', 'A', 'T', 'S', 'D', 'O', 'G']: {result}, 空白牌位置: {blanks}")
    
    # 缺少字母
    result, blanks = can_form_word('CAT', ['C', 'T'])
    print(f"'CAT' 用 ['C', 'T']: {result}, 空白牌位置: {blanks}")
    
    # 使用空白牌
    result, blanks = can_form_word('CAT', ['C', 'T'], has_blank=True)
    print(f"'CAT' 用 ['C', 'T'] + 空白牌: {result}, 空白牌位置: {blanks}")
    
    # 高价值单词
    result, blanks = can_form_word('QUIZ', ['Q', 'I', 'Z'], has_blank=True)
    print(f"'QUIZ' 用 ['Q', 'I', 'Z'] + 空白牌: {result}, 空白牌位置: {blanks}")


def example_word_analysis():
    """单词分析示例"""
    print_separator("单词难度分析")
    
    words = ['CAT', 'DOG', 'THE', 'QUICK', 'JAZZY', 'QUIZZIFY']
    
    print("单词难度分数:")
    for word in words:
        difficulty = word_difficulty_score(word)
        analysis = letter_frequency_analysis(word)
        high_value = [l for l, (c, r) in analysis.items() if LETTER_VALUES.get(l, 0) >= 5]
        print(f"  {word}: 难度 {difficulty:.1f}, 高价值字母: {high_value}")
    
    print("\n字母频率分析 (JAZZY):")
    analysis = letter_frequency_analysis('JAZZY')
    for letter, (count, rarity) in analysis.items():
        print(f"  {letter}: 出现 {count} 次, 稀有度 {rarity:.1f}")


def example_rack_analysis():
    """字母 Rack 分析示例"""
    print_separator("字母 Rack 分析")
    
    # 基础 Rack
    rack1 = ['C', 'A', 'T', 'S', 'D', 'O', 'G']
    analysis1 = letter_rack_analysis(rack1)
    print(f"Rack 1: {', '.join(rack1)}")
    print(f"  总价值: {analysis1['total_value']}")
    print(f"  平均价值: {analysis1['avg_value']:.1f}")
    print(f"  Bingo 潜力: {analysis1['bingo_potential']}")
    print(f"  高价值字母: {', '.join(analysis1['high_value_letters']) or '无'}")
    
    # 高价值 Rack
    rack2 = ['Q', 'Z', 'J', 'X', 'K', 'A', 'E']
    analysis2 = letter_rack_analysis(rack2)
    print(f"\nRack 2: {', '.join(rack2)}")
    print(f"  总价值: {analysis2['total_value']}")
    print(f"  平均价值: {analysis2['avg_value']:.1f}")
    print(f"  Bingo 潜力: {analysis2['bingo_potential']}")
    print(f"  高价值字母: {', '.join(analysis2['high_value_letters'])}")
    print(f"  平衡度分数: {analysis2['balance_score']:.1f}")
    
    # 平衡 Rack
    rack3 = ['A', 'E', 'I', 'O', 'R', 'S', 'T']
    analysis3 = letter_rack_analysis(rack3)
    print(f"\nRack 3: {', '.join(rack3)}")
    print(f"  总价值: {analysis3['total_value']}")
    print(f"  平均价值: {analysis3['avg_value']:.1f}")
    print(f"  高价值字母: {', '.join(analysis3['high_value_letters']) or '无'}")
    print(f"  常见字母: {', '.join(analysis3['common_letters'])}")
    print(f"  平衡度分数: {analysis3['balance_score']:.1f}")


def example_best_placement():
    """最佳放置示例"""
    print_separator("最佳放置分析")
    
    words = ['CAT', 'QUIZ', 'QUICK', 'JAZZY']
    
    print("单词最佳放置分数:")
    for word in words:
        best_score, best_positions = best_placement_score(word)
        base_score = word_score(word)
        print(f"  {word}:")
        print(f"    基础分数: {base_score}")
        print(f"    最佳分数: {best_score}")
        print(f"    分数提升: {best_score - base_score}")


def example_word_ranking():
    """单词排序示例"""
    print_separator("单词分数排序")
    
    words = ['CAT', 'DOG', 'QUICK', 'JAZZY', 'QUIZ', 'ZOO', 'THE', 'AND']
    ranked = word_rank_by_score(words)
    
    print("按分数排序的单词:")
    for word, score in ranked:
        print(f"  {word}: {score} 分")


def example_remaining_tiles():
    """剩余字母示例"""
    print_separator("剩余字母计算")
    
    # 游戏开始
    print("游戏开始时的字母数量:")
    remaining = remaining_tiles({})
    for letter in ['A', 'E', 'I', 'O', 'U']:
        print(f"  {letter}: {remaining[letter]} 张")
    
    # 游戏中期
    print("\n使用一些字母后:")
    used = {'A': 5, 'E': 8, 'I': 4, 'O': 6, 'U': 3}
    remaining = remaining_tiles(used)
    for letter in ['A', 'E', 'I', 'O', 'U']:
        print(f"  {letter}: {remaining[letter]} 张 (用了 {used.get(letter, 0)})")


def example_validation():
    """单词验证示例"""
    print_separator("单词验证")
    
    test_words = ['A', 'CAT', 'QUIZZIFY', 'ABCDEFGHIJKLMNOP', 'CAT123', '']
    
    print("验证结果:")
    for word in test_words:
        valid, msg = validate_scrabble_word(word)
        status = "✓ 有效" if valid else f"✗ 无效: {msg}"
        print(f"  '{word}': {status}")


def example_blank_tiles():
    """空白牌使用示例"""
    print_separator("空白牌使用")
    
    word = 'QUIZ'
    
    # 无空白牌
    print(f"{word} 无空白牌: {word_score(word)} 分")
    
    # 用空白牌代替 Q
    print(f"{word} 用空白牌代替 Q: {word_score(word, use_blanks=[0])} 分")
    
    # 用空白牌代替 U
    print(f"{word} 用空白牌代替 U: {word_score(word, use_blanks=[1])} 分")
    
    # 用空白牌代替 Z
    print(f"{word} 用空白牌代替 Z: {word_score(word, use_blanks=[3])} 分")
    
    # 空白牌 ScrabbleTile
    print("\n空白牌 ScrabbleTile:")
    blank_tile = ScrabbleTile('Q', is_blank=True)
    print(f"  字母: {blank_tile.letter}")
    print(f"  空白牌: {blank_tile.is_blank}")
    print(f"  分数: {blank_tile.value()}")
    print(f"  显示: {str(blank_tile)}")


if __name__ == "__main__":
    example_basic_scoring()
    example_letter_distribution()
    example_multipliers()
    example_board()
    example_word_forming()
    example_word_analysis()
    example_rack_analysis()
    example_best_placement()
    example_word_ranking()
    example_remaining_tiles()
    example_validation()
    example_blank_tiles()
    
    print("\n" + "="*50)
    print("  所有示例完成!")
    print("="*50)