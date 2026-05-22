"""
scrabble_utils 测试文件

测试所有 Scrabble 单词评分功能
"""

import unittest
from mod import (
    letter_score, word_score, calculate_word_with_multipliers,
    get_standard_board, remaining_tiles, can_form_word,
    letter_frequency_analysis, word_difficulty_score,
    tile_distribution_summary, high_value_letters, rare_letters,
    score_distribution, validate_scrabble_word, best_placement_score,
    word_rank_by_score, letter_rack_analysis, score, high_score_words,
    ScrabbleTile, BoardPosition, ScrabbleWord,
    LETTER_VALUES, LETTER_DISTRIBUTION, ENGLISH_FREQUENCY
)


class TestLetterScore(unittest.TestCase):
    """测试字母分数"""
    
    def test_basic_letters(self):
        """测试基础字母分数"""
        self.assertEqual(letter_score('A'), 1)
        self.assertEqual(letter_score('E'), 1)
        self.assertEqual(letter_score('I'), 1)
        self.assertEqual(letter_score('O'), 1)
        self.assertEqual(letter_score('U'), 1)
    
    def test_two_point_letters(self):
        """测试 2 分字母"""
        self.assertEqual(letter_score('D'), 2)
        self.assertEqual(letter_score('G'), 2)
    
    def test_three_point_letters(self):
        """测试 3 分字母"""
        self.assertEqual(letter_score('B'), 3)
        self.assertEqual(letter_score('C'), 3)
        self.assertEqual(letter_score('M'), 3)
        self.assertEqual(letter_score('P'), 3)
    
    def test_four_point_letters(self):
        """测试 4 分字母"""
        self.assertEqual(letter_score('F'), 4)
        self.assertEqual(letter_score('H'), 4)
        self.assertEqual(letter_score('V'), 4)
        self.assertEqual(letter_score('W'), 4)
        self.assertEqual(letter_score('Y'), 4)
    
    def test_five_point_letters(self):
        """测试 5 分字母"""
        self.assertEqual(letter_score('K'), 5)
    
    def test_eight_point_letters(self):
        """测试 8 分字母"""
        self.assertEqual(letter_score('J'), 8)
        self.assertEqual(letter_score('X'), 8)
    
    def test_ten_point_letters(self):
        """测试 10 分字母"""
        self.assertEqual(letter_score('Q'), 10)
        self.assertEqual(letter_score('Z'), 10)
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(letter_score('a'), 1)
        self.assertEqual(letter_score('Q'), 10)
        self.assertEqual(letter_score('q'), 10)
    
    def test_invalid_letter(self):
        """测试无效字母"""
        self.assertEqual(letter_score('?'), 0)
        self.assertEqual(letter_score('1'), 0)


class TestWordScore(unittest.TestCase):
    """测试单词分数"""
    
    def test_simple_words(self):
        """测试简单单词"""
        self.assertEqual(word_score('CAT'), 5)  # C(3) + A(1) + T(1) = 5
        self.assertEqual(word_score('DOG'), 5)  # D(2) + O(1) + G(2) = 5
        self.assertEqual(word_score('THE'), 6)  # T(1) + H(4) + E(1) = 6
    
    def test_high_value_words(self):
        """测试高价值单词"""
        self.assertEqual(word_score('QUIZ'), 22)  # Q(10) + U(1) + I(1) + Z(10) = 22
        self.assertEqual(word_score('JAZZY'), 33)  # J(8) + A(1) + Z(10) + Z(10) + Y(4) = 33
    
    def test_long_words(self):
        """测试长单词"""
        self.assertEqual(word_score('QUICKLY'), 25)  # Q(10) + U(1) + I(1) + C(3) + K(5) + L(1) + Y(4) = 25
    
    def test_with_blanks(self):
        """测试使用空白牌"""
        # QUIZ: Q(10) + U(1) + I(1) + Z(10) = 22
        # 用空白牌代替 Q: U(1) + I(1) + Z(10) = 12
        self.assertEqual(word_score('QUIZ', use_blanks=[0]), 12)
        # 用空白牌代替 U: Q(10) + I(1) + Z(10) = 21
        self.assertEqual(word_score('QUIZ', use_blanks=[1]), 21)


class TestCalculateWithMultipliers(unittest.TestCase):
    """测试带乘数的分数计算"""
    
    def test_no_multipliers(self):
        """测试无乘数"""
        self.assertEqual(calculate_word_with_multipliers('CAT'), 5)
    
    def test_double_letter(self):
        """测试双倍字母"""
        # C(3)*2 + A(1) + T(1) = 8
        self.assertEqual(calculate_word_with_multipliers('CAT', letter_multipliers=[2, 1, 1]), 8)
    
    def test_triple_letter(self):
        """测试三倍字母"""
        # C(3)*3 + A(1) + T(1) = 11
        self.assertEqual(calculate_word_with_multipliers('CAT', letter_multipliers=[3, 1, 1]), 11)
    
    def test_double_word(self):
        """测试双倍单词"""
        # (C(3) + A(1) + T(1)) * 2 = 10
        self.assertEqual(calculate_word_with_multipliers('CAT', word_multipliers=[2]), 10)
    
    def test_triple_word(self):
        """测试三倍单词"""
        # (C(3) + A(1) + T(1)) * 3 = 15
        self.assertEqual(calculate_word_with_multipliers('CAT', word_multipliers=[3]), 15)
    
    def test_combined_multipliers(self):
        """测试组合乘数"""
        # C(3)*2 + A(1) + T(1) = 8, then *2 = 16
        self.assertEqual(
            calculate_word_with_multipliers('CAT', letter_multipliers=[2, 1, 1], word_multipliers=[2]),
            16
        )
    
    def test_bingo_bonus(self):
        """测试 Bingo 奖励"""
        # QUICKLY: 25 + 50 = 75
        score_no_bingo = calculate_word_with_multipliers('QUICKLY', bingo=False)
        score_with_bingo = calculate_word_with_multipliers('QUICKLY', bingo=True)
        self.assertEqual(score_with_bingo - score_no_bingo, 50)


class TestScrabbleTile(unittest.TestCase):
    """测试字母牌"""
    
    def test_normal_tile(self):
        """测试普通字母牌"""
        tile = ScrabbleTile('Q')
        self.assertEqual(tile.letter, 'Q')
        self.assertFalse(tile.is_blank)
        self.assertEqual(tile.value(), 10)
    
    def test_blank_tile(self):
        """测试空白牌"""
        tile = ScrabbleTile('Q', is_blank=True)
        self.assertEqual(tile.letter, 'Q')
        self.assertTrue(tile.is_blank)
        self.assertEqual(tile.value(), 0)
    
    def test_tile_string(self):
        """测试字母牌字符串表示"""
        normal = ScrabbleTile('A')
        self.assertEqual(str(normal), 'A')
        
        blank = ScrabbleTile('Q', is_blank=True)
        self.assertEqual(str(blank), '[Q]')


class TestBoardPosition(unittest.TestCase):
    """测试棋盘位置"""
    
    def test_normal_position(self):
        """测试普通位置"""
        pos = BoardPosition(7, 7, 'normal')
        self.assertEqual(pos.letter_multiplier(), 1)
        self.assertEqual(pos.word_multiplier(), 1)
    
    def test_double_letter_position(self):
        """测试双倍字母位置"""
        pos = BoardPosition(0, 3, 'dl')
        self.assertEqual(pos.letter_multiplier(), 2)
        self.assertEqual(pos.word_multiplier(), 1)
    
    def test_triple_letter_position(self):
        """测试三倍字母位置"""
        pos = BoardPosition(1, 5, 'tl')
        self.assertEqual(pos.letter_multiplier(), 3)
        self.assertEqual(pos.word_multiplier(), 1)
    
    def test_double_word_position(self):
        """测试双倍单词位置"""
        pos = BoardPosition(1, 1, 'dw')
        self.assertEqual(pos.letter_multiplier(), 1)
        self.assertEqual(pos.word_multiplier(), 2)
    
    def test_triple_word_position(self):
        """测试三倍单词位置"""
        pos = BoardPosition(0, 0, 'tw')
        self.assertEqual(pos.letter_multiplier(), 1)
        self.assertEqual(pos.word_multiplier(), 3)


class TestStandardBoard(unittest.TestCase):
    """测试标准棋盘"""
    
    def test_board_size(self):
        """测试棋盘大小"""
        board = get_standard_board()
        self.assertEqual(len(board), 15)
        self.assertEqual(len(board[0]), 15)
    
    def test_center_position(self):
        """测试中心位置"""
        board = get_standard_board()
        center = board[7][7]
        self.assertEqual(center.multiplier, 'dw')
    
    def test_corner_positions(self):
        """测试角落位置"""
        board = get_standard_board()
        corners = [(0, 0), (0, 14), (14, 0), (14, 14)]
        for r, c in corners:
            self.assertEqual(board[r][c].multiplier, 'tw')
    
    def test_triple_letter_positions(self):
        """测试三倍字母位置"""
        board = get_standard_board()
        tl_positions = [(1, 5), (1, 9), (5, 1), (5, 5)]
        for r, c in tl_positions:
            self.assertEqual(board[r][c].multiplier, 'tl')


class TestCanFormWord(unittest.TestCase):
    """测试单词组成"""
    
    def test_exact_match(self):
        """测试精确匹配"""
        result, blanks = can_form_word('CAT', ['C', 'A', 'T'])
        self.assertTrue(result)
        self.assertEqual(blanks, [])
    
    def test_extra_letters(self):
        """测试额外字母"""
        result, blanks = can_form_word('CAT', ['C', 'A', 'T', 'S', 'D'])
        self.assertTrue(result)
        self.assertEqual(blanks, [])
    
    def test_missing_letter(self):
        """测试缺少字母"""
        result, blanks = can_form_word('CAT', ['C', 'A'])
        self.assertFalse(result)
    
    def test_with_blank(self):
        """测试使用空白牌"""
        result, blanks = can_form_word('CAT', ['C', 'A'], has_blank=True)
        self.assertTrue(result)
        self.assertEqual(blanks, [2])  # T 位置使用空白牌
    
    def test_missing_without_blank(self):
        """测试缺少字母且无空白牌"""
        result, blanks = can_form_word('CAT', ['C', 'A'], has_blank=False)
        self.assertFalse(result)


class TestLetterFrequencyAnalysis(unittest.TestCase):
    """测试字母频率分析"""
    
    def test_simple_word(self):
        """测试简单单词"""
        analysis = letter_frequency_analysis('CAT')
        self.assertIn('C', analysis)
        self.assertIn('A', analysis)
        self.assertIn('T', analysis)
        self.assertEqual(analysis['C'][0], 1)
    
    def test_repeated_letters(self):
        """测试重复字母"""
        analysis = letter_frequency_analysis('BANANA')
        self.assertEqual(analysis['A'][0], 3)  # A 出现 3 次
        self.assertEqual(analysis['N'][0], 2)  # N 出现 2 次
    
    def test_rarity_values(self):
        """测试稀有度值"""
        analysis = letter_frequency_analysis('CAT')
        # A 是常见字母，稀有度应该较低
        self.assertLess(analysis['A'][1], analysis['C'][1])


class TestWordDifficulty(unittest.TestCase):
    """测试单词难度"""
    
    def test_easy_word(self):
        """测试简单单词"""
        difficulty = word_difficulty_score('CAT')
        self.assertGreater(difficulty, 0)
        self.assertLess(difficulty, 50)
    
    def test_hard_word(self):
        """测试难单词"""
        easy = word_difficulty_score('CAT')
        hard = word_difficulty_score('QUIZZIFY')
        self.assertGreater(hard, easy)
    
    def test_empty_word(self):
        """测试空单词"""
        self.assertEqual(word_difficulty_score(''), 0)


class TestHighValueLetters(unittest.TestCase):
    """测试高价值字母"""
    
    def test_default_threshold(self):
        """测试默认阈值"""
        letters = high_value_letters()
        self.assertIn('Q', letters)
        self.assertIn('Z', letters)
        self.assertIn('J', letters)
        self.assertIn('X', letters)
        self.assertIn('K', letters)
    
    def test_high_threshold(self):
        """测试高阈值"""
        letters = high_value_letters(8)
        self.assertIn('Q', letters)
        self.assertIn('Z', letters)
        self.assertIn('J', letters)
        self.assertIn('X', letters)
        self.assertNotIn('K', letters)


class TestRareLetters(unittest.TestCase):
    """测试稀有字母"""
    
    def test_default_threshold(self):
        """测试默认阈值"""
        letters = rare_letters()
        self.assertIn('Q', letters)  # 1 个
        self.assertIn('Z', letters)  # 1 个
        self.assertIn('J', letters)  # 1 个
        self.assertIn('X', letters)  # 1 个
        self.assertIn('K', letters)  # 1 个


class TestScoreDistribution(unittest.TestCase):
    """测试分数分布"""
    
    def test_distribution(self):
        """测试分布"""
        dist = score_distribution()
        self.assertIn(1, dist)
        self.assertIn(10, dist)
        self.assertEqual(set(dist[10]), {'Q', 'Z'})
    
    def test_all_values_present(self):
        """测试所有分数值存在"""
        dist = score_distribution()
        expected_values = {1, 2, 3, 4, 5, 8, 10}
        self.assertEqual(set(dist.keys()), expected_values)


class TestValidateScrabbleWord(unittest.TestCase):
    """测试单词验证"""
    
    def test_valid_word(self):
        """测试有效单词"""
        valid, msg = validate_scrabble_word('CAT')
        self.assertTrue(valid)
    
    def test_empty_word(self):
        """测试空单词"""
        valid, msg = validate_scrabble_word('')
        self.assertFalse(valid)
        self.assertIn("空", msg)
    
    def test_single_letter(self):
        """测试单字母"""
        valid, msg = validate_scrabble_word('A')
        self.assertFalse(valid)
        self.assertIn("2", msg)
    
    def test_too_long(self):
        """测试过长单词"""
        valid, msg = validate_scrabble_word('ABCDEFGHIJKLMNOP')
        self.assertFalse(valid)
        self.assertIn("15", msg)
    
    def test_non_alpha(self):
        """测试非字母字符"""
        valid, msg = validate_scrabble_word('CAT123')
        self.assertFalse(valid)
        self.assertIn("字母", msg)


class TestWordRankByScore(unittest.TestCase):
    """测试单词排序"""
    
    def test_ranking(self):
        """测试排序"""
        words = ['CAT', 'DOG', 'QUIZ', 'JAZZY']
        ranked = word_rank_by_score(words)
        # QUIZ (22) 和 JAZZY (24) 应该排在前面
        self.assertEqual(ranked[0][0], 'JAZZY')
        self.assertEqual(ranked[1][0], 'QUIZ')
    
    def test_empty_list(self):
        """测试空列表"""
        ranked = word_rank_by_score([])
        self.assertEqual(ranked, [])


class TestLetterRackAnalysis(unittest.TestCase):
    """测试字母 Rack 分析"""
    
    def test_basic_analysis(self):
        """测试基础分析"""
        rack = ['C', 'A', 'T', 'S']
        analysis = letter_rack_analysis(rack)
        self.assertEqual(analysis['total_value'], 6)  # C(3) + A(1) + T(1) + S(1)
        self.assertEqual(analysis['avg_value'], 1.5)
    
    def test_high_value_rack(self):
        """测试高价值 Rack"""
        rack = ['Q', 'Z', 'J', 'X', 'K']
        analysis = letter_rack_analysis(rack)
        self.assertEqual(len(analysis['high_value_letters']), 5)
    
    def test_bingo_rack(self):
        """测试 Bingo Rack"""
        rack = ['C', 'A', 'T', 'S', 'D', 'O', 'G']
        analysis = letter_rack_analysis(rack)
        self.assertTrue(analysis['bingo_potential'])
    
    def test_non_bingo_rack(self):
        """测试非 Bingo Rack"""
        rack = ['C', 'A', 'T']
        analysis = letter_rack_analysis(rack)
        self.assertFalse(analysis['bingo_potential'])


class TestBestPlacementScore(unittest.TestCase):
    """测试最佳放置分数"""
    
    def test_short_word(self):
        """测试短单词"""
        score, positions = best_placement_score('CAT')
        self.assertGreater(score, 5)  # 应该能利用一些乘数
    
    def test_word_length(self):
        """测试单词长度"""
        score, positions = best_placement_score('QUIZ')
        self.assertEqual(len(positions), 4)


class TestRemainingTiles(unittest.TestCase):
    """测试剩余字母"""
    
    def test_no_used(self):
        """测试无使用字母"""
        remaining = remaining_tiles({})
        self.assertEqual(remaining['A'], 9)
        self.assertEqual(remaining['E'], 12)
    
    def test_some_used(self):
        """测试部分使用"""
        remaining = remaining_tiles({'A': 3, 'E': 5})
        self.assertEqual(remaining['A'], 6)
        self.assertEqual(remaining['E'], 7)


class TestQuickScore(unittest.TestCase):
    """测试快速分数函数"""
    
    def test_score_function(self):
        """测试 score 函数"""
        self.assertEqual(score('CAT'), 5)
        self.assertEqual(score('QUIZ'), 22)


class TestHighScoreWords(unittest.TestCase):
    """测试高分单词列表"""
    
    def test_default_min(self):
        """测试默认最低分数"""
        words = high_score_words()
        for word in words:
            self.assertGreaterEqual(word_score(word), 20)
    
    def test_high_min(self):
        """测试高最低分数"""
        words = high_score_words(30)
        for word in words:
            self.assertGreaterEqual(word_score(word), 30)


if __name__ == "__main__":
    unittest.main(verbosity=2)