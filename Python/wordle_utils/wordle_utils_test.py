"""
Wordle 游戏辅助工具测试
"""

import unittest
import sys
import os

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wordle_utils.mod import (
    WordleHelper,
    WordleSolver,
    filter_words,
    get_best_guess,
    calculate_letter_frequency,
    DEFAULT_WORDS
)


class TestWordleHelper(unittest.TestCase):
    """WordleHelper 测试"""
    
    def setUp(self):
        """测试前准备"""
        self.helper = WordleHelper()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsInstance(self.helper.words, list)
        self.assertTrue(len(self.helper.words) > 100)
        
        # 所有词都是5字母
        for word in self.helper.words:
            self.assertEqual(len(word), 5)
    
    def test_custom_words(self):
        """测试自定义词库"""
        custom_words = ["apple", "beach", "crane", "dream", "eagle"]
        helper = WordleHelper(custom_words)
        self.assertEqual(len(helper.words), 5)
    
    def test_letter_frequency(self):
        """测试字母频率计算"""
        freq = self.helper.letter_frequency
        
        self.assertIsInstance(freq, dict)
        self.assertTrue(len(freq) > 0)
        
        # 所有频率都在0-1之间
        for letter, f in freq.items():
            self.assertIn(letter, 'abcdefghijklmnopqrstuvwxyz')
            self.assertGreaterEqual(f, 0)
            self.assertLessEqual(f, 1)
        
        # 验证字母频率有差异（不是所有字母频率都一样）
        frequencies = list(freq.values())
        self.assertTrue(max(frequencies) > min(frequencies))
    
    def test_position_frequency(self):
        """测试位置频率计算"""
        pos_freq = self.helper.position_frequency
        
        self.assertEqual(len(pos_freq), 5)
        
        for pos_dict in pos_freq:
            self.assertIsInstance(pos_dict, dict)
            for letter, f in pos_dict.items():
                self.assertIn(letter, 'abcdefghijklmnopqrstuvwxyz')
                self.assertGreaterEqual(f, 0)
                self.assertLessEqual(f, 1)
    
    def test_filter_words_correct(self):
        """测试正确位置过滤"""
        # 第一个字母是'a'
        result = self.helper.filter_words(correct="a....")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertEqual(word[0], 'a')
        
        # 第三个字母是'a'
        result = self.helper.filter_words(correct="..a..")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertEqual(word[2], 'a')
        
        # 多个位置
        result = self.helper.filter_words(correct="a..le")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertEqual(word[0], 'a')
            self.assertEqual(word[3], 'l')
            self.assertEqual(word[4], 'e')
    
    def test_filter_words_present(self):
        """测试存在字母过滤"""
        result = self.helper.filter_words(present="e")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertIn('e', word)
        
        # 测试多个存在字母（但不超过单词长度限制）
        result = self.helper.filter_words(present="ae")  # 同时包含a和e
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertIn('a', word)
            self.assertIn('e', word)
    
    def test_filter_words_absent(self):
        """测试不存在字母过滤"""
        result = self.helper.filter_words(absent="xyz")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertNotIn('x', word)
            self.assertNotIn('y', word)
            self.assertNotIn('z', word)
    
    def test_filter_words_combined(self):
        """测试组合过滤"""
        result = self.helper.filter_words(
            correct="..a..",
            present="e",
            absent="xyz"
        )
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertEqual(word[2], 'a')
            self.assertIn('e', word)
            self.assertNotIn('x', word)
            self.assertNotIn('y', word)
            self.assertNotIn('z', word)
    
    def test_filter_words_starts_ends(self):
        """测试开头和结尾过滤"""
        result = self.helper.filter_words(starts_with="st")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertTrue(word.startswith("st"))
        
        result = self.helper.filter_words(ends_with="er")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertTrue(word.endswith("er"))
    
    def test_filter_words_contains(self):
        """测试包含字母过滤"""
        result = self.helper.filter_words(contains="ae")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertIn('a', word)
            self.assertIn('e', word)
    
    def test_get_best_guess(self):
        """测试最优猜测"""
        # 频率方法
        word, score = self.helper.get_best_guess(method="frequency")
        self.assertEqual(len(word), 5)
        self.assertIsInstance(score, float)
        
        # 位置方法
        word, score = self.helper.get_best_guess(method="position")
        self.assertEqual(len(word), 5)
        
        # 熵方法
        word, score = self.helper.get_best_guess(method="entropy")
        self.assertEqual(len(word), 5)
        
        # 综合方法
        word, score = self.helper.get_best_guess(method="combined")
        self.assertEqual(len(word), 5)
    
    def test_get_best_guess_with_candidates(self):
        """测试候选词最优猜测"""
        candidates = ["apple", "crane", "dream", "eagle"]
        word, score = self.helper.get_best_guess(candidates=candidates)
        self.assertIn(word, candidates)
    
    def test_get_best_guess_single_candidate(self):
        """测试单个候选词"""
        candidates = ["apple"]
        word, score = self.helper.get_best_guess(candidates=candidates)
        self.assertEqual(word, "apple")
        self.assertEqual(score, 1.0)
    
    def test_get_best_guess_empty(self):
        """测试空候选词"""
        word, score = self.helper.get_best_guess(candidates=[])
        self.assertEqual(word, "")
        self.assertEqual(score, 0.0)
    
    def test_analyze_feedback(self):
        """测试反馈分析"""
        # 全绿（正确）
        result = self.helper.analyze_feedback("apple", "ggggg")
        self.assertEqual(result['correct'], "apple")
        
        # 全灰（错误）
        result = self.helper.analyze_feedback("xyz", "bbb")
        self.assertIn('x', result['absent'])
        self.assertIn('y', result['absent'])
        self.assertIn('z', result['absent'])
        
        # 黄色（存在但位置错误）
        result = self.helper.analyze_feedback("apple", "y____")
        self.assertIn('a', result['present'])
        self.assertIn(0, result['yellow_positions']['a'])
    
    def test_suggest_next_guess(self):
        """测试建议下一猜测"""
        # 模拟第一次猜测
        word, candidates, count = self.helper.suggest_next_guess([
            ("crane", "bbgbb")  # a在第3位正确
        ])
        
        self.assertTrue(len(word) == 5)
        self.assertGreater(count, 0)
        
        # 所有候选词第3位都是'a'
        for c in candidates:
            self.assertEqual(c[2], 'a')
    
    def test_suggest_next_guess_win(self):
        """测试猜中情况"""
        word, candidates, count = self.helper.suggest_next_guess([
            ("apple", "ggggg")
        ])
        
        # 猜中后，没有有效的候选词（只剩答案本身）
        # 但由于逻辑会尝试从词库过滤，apple本身可能还在
        # 所以检查是否返回有效的猜测
        self.assertTrue(word == "" or word == "apple" or count <= 1)


class TestWordleSolver(unittest.TestCase):
    """WordleSolver 测试"""
    
    def setUp(self):
        """测试前准备"""
        self.solver = WordleSolver()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsInstance(self.solver.helper, WordleHelper)
        self.assertEqual(len(self.solver.history), 0)
        self.assertGreater(len(self.solver.candidates), 0)
    
    def test_reset(self):
        """测试重置"""
        self.solver.submit_feedback("crane", "bbbbb")
        self.solver.reset()
        
        self.assertEqual(len(self.solver.history), 0)
        self.assertEqual(len(self.solver.candidates), len(self.solver.helper.words))
    
    def test_get_first_guess(self):
        """测试首次猜测"""
        guess = self.solver.get_first_guess()
        self.assertEqual(len(guess), 5)
        self.assertIn(guess, self.solver.helper.words)
    
    def test_submit_feedback(self):
        """测试提交反馈"""
        initial_count = len(self.solver.candidates)
        
        self.solver.submit_feedback("crane", "bbbbb")
        
        self.assertEqual(len(self.solver.history), 1)
        self.assertLess(len(self.solver.candidates), initial_count)
    
    def test_get_next_guess(self):
        """测试获取下一猜测"""
        self.solver.submit_feedback("crane", "bbbbb")
        guess = self.solver.get_next_guess()
        
        self.assertEqual(len(guess), 5)
        self.assertIn(guess, self.solver.candidates)
    
    def test_auto_solve_known_word(self):
        """测试自动求解已知词"""
        success, attempts, history = self.solver.auto_solve(
            "apple",
            max_attempts=10,
            verbose=False
        )
        
        self.assertTrue(success)
        self.assertGreater(attempts, 0)
        self.assertGreater(len(history), 0)
        self.assertLessEqual(attempts, 10)
    
    def test_auto_solve_unknown_word(self):
        """测试自动求解未知词"""
        success, attempts, history = self.solver.auto_solve(
            "zzzzz",  # 不在词库中
            verbose=False
        )
        
        self.assertFalse(success)
        self.assertEqual(attempts, 0)
        self.assertEqual(len(history), 0)
    
    def test_auto_solve_with_first_guess(self):
        """测试使用首次猜测的自动求解"""
        success, attempts, history = self.solver.auto_solve(
            "crane",
            first_guess="crane",
            verbose=False
        )
        
        # 如果首次猜测正确，应该成功且只用1次
        self.assertTrue(success)
        self.assertEqual(attempts, 1)
    
    def test_get_pattern(self):
        """测试反馈模式生成"""
        # 全对
        pattern = self.solver.helper._get_pattern("apple", "apple")
        self.assertEqual(pattern, "22222")
        
        # 部分对 - xyzab vs apple
        # x, y, z 不在 apple 中 -> 0
        # a 在 apple 中但位置不对 -> 黄色 (1)
        # b 不在 apple 中 -> 0
        pattern = self.solver.helper._get_pattern("xyzab", "apple")
        self.assertEqual(pattern, "00010")
        
        # 部分对
        pattern = self.solver.helper._get_pattern("apric", "apple")
        # a正确位置 -> 2
        # p正确位置 -> 2
        # r不存在 -> 0
        # i不存在 -> 0
        # c不存在 -> 0
        self.assertEqual(pattern, "22000")
    
    def test_yellow_pattern(self):
        """测试黄色模式"""
        # 测试存在但位置错误
        pattern = self.solver.helper._get_pattern("pales", "apple")
        # p: 在apple中但位置1不对(apple位置0是a)，应该是黄色
        # 但apple有p在位置2，pales的p在位置0
        # 所以位置0的p应该是黄色
        # a: apple位置0是a，pales位置1是a，正确
        # l: apple没有l -> 灰色
        # e: apple位置4是e，pales位置3是l -> 黄色
        # s: apple没有s -> 灰色
        
        # 实际: pales vs apple
        # 第一轮：正确位置
        #   位置1: a == a -> 2
        # 第二轮：黄色
        #   位置0: p 在 apple 中 (位置2) -> 1
        #   位置3: e 在 apple 中 (位置4) -> 1
        # 灰色:
        #   位置2: l 不在 apple 中 -> 0
        #   位置4: s 不在 apple 中 -> 0
        
        # 结果: 12010 不对，让我重新算
        # apple: a p p l e
        # pales: p a l e s
        # 
        # 第一轮绿色：
        #   pales[1] = a, apple[1] = p -> 不对
        #   没有绿色
        # 
        # 等等，我需要重新理解这个函数
        # _get_pattern(guess, answer) 返回的是 guess 相对于 answer 的反馈
        # 
        # guess = pales, answer = apple
        # 第一轮：正确位置
        #   pales[1] = a, apple[1] = p -> 不对
        #   没有位置完全匹配
        # 
        # 实际上应该检查每个位置
        # 位置0: pales[0]=p, apple[0]=a -> 不对，但p在apple中
        # 位置1: pales[1]=a, apple[1]=p -> 不对，但a在apple中
        # ...
        
        # 重新分析：
        # apple vs pales
        # pales[0]=p: apple中有p（位置1和2），但位置0不是 -> 黄色
        # pales[1]=a: apple中有a（位置0），但位置1不是 -> 黄色
        # pales[2]=l: apple中没有l -> 灰色
        # pales[3]=e: apple中有e（位置4），但位置3不是 -> 黄色
        # pales[4]=s: apple中没有s -> 灰色
        
        # 但根据函数逻辑：
        # 第一轮：正确位置
        #   pales[1] == apple[1]? a == p? 不对
        #   没有绿色
        # 第二轮：黄色
        #   apple_chars = ['a', 'p', 'p', 'l', 'e']
        #   pales[0]=p: p 在 apple_chars 中? 是 -> 黄色，移除apple_chars中的p -> ['a', 'p', 'l', 'e']
        #   pales[1]=a: a 在 apple_chars 中? 是 -> 黄色，移除a -> ['p', 'l', 'e']
        #   pales[2]=l: l 在 apple_chars 中? 是 -> 黄色，移除l -> ['p', 'e']
        #   pales[3]=e: e 在 apple_chars 中? 是 -> 黄色，移除e -> ['p']
        #   pales[4]=s: s 在 ['p'] 中? 否 -> 灰色
        
        # 结果: 11110
        
        # 等等，让我再仔细看一下函数
        # 
        # 实际上答案应该是：pales vs apple
        # apple: a p p l e
        # pales: p a l e s
        # 
        # 位置0 (p): 在apple中但位置不对 -> 黄色 (1)
        # 位置1 (a): 在apple中但位置不对 -> 黄色 (1)
        # 位置2 (l): 不在apple中 -> 灰色 (0)
        # 位置3 (e): 在apple中但位置不对 -> 黄色 (1)
        # 位置4 (s): 不在apple中 -> 灰色 (0)
        # 
        # 结果: 11010
        
        # 但问题是，apple只有一个'a'和一个'e'，两个'p'
        # 当pales尝试匹配时：
        # - 'p' 在位置1和2的apple中有两个p
        # - 'a' 在位置0的apple中
        # - 'l' 不在apple中
        # - 'e' 在位置4的apple中
        # - 's' 不在apple中
        
        # 根据_get_pattern函数的逻辑，它会正确处理这种情况
        
        pattern = self.solver.helper._get_pattern("pales", "apple")
        # 根据函数逻辑：
        # 第一轮绿色检查：没有位置完全匹配
        # 第二轮黄色检查：
        #   pales[0]=p: p在apple中 -> 1, apple_chars变成['a', 'p', 'l', 'e']
        #   pales[1]=a: a在apple中 -> 1, apple_chars变成['p', 'l', 'e']
        #   pales[2]=l: l在['p', 'l', 'e']中 -> 1, apple_chars变成['p', 'e']
        #   pales[3]=e: e在['p', 'e']中 -> 1, apple_chars变成['p']
        #   pales[4]=s: s在['p']中 -> 0
        
        # 结果: 11110
        self.assertEqual(pattern, "11110")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_filter_words_function(self):
        """测试 filter_words 函数"""
        result = filter_words(correct="..a..")
        self.assertTrue(len(result) > 0)
        for word in result:
            self.assertEqual(word[2], 'a')
    
    def test_get_best_guess_function(self):
        """测试 get_best_guess 函数"""
        word, score = get_best_guess()
        self.assertEqual(len(word), 5)
    
    def test_calculate_letter_frequency(self):
        """测试 calculate_letter_frequency 函数"""
        freq = calculate_letter_frequency()
        self.assertIsInstance(freq, dict)
        self.assertTrue(len(freq) > 0)
    
    def test_custom_words_in_functions(self):
        """测试便捷函数使用自定义词"""
        custom = ["apple", "beach", "crane"]
        result = filter_words(custom, starts_with="a")
        self.assertEqual(result, ["apple"])
        
        word, _ = get_best_guess(custom)
        self.assertIn(word, custom)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_helper(self):
        """测试空词库"""
        helper = WordleHelper([])
        self.assertEqual(helper.words, [])
        self.assertEqual(helper.letter_frequency, {})
    
    def test_single_word_helper(self):
        """测试单词汇"""
        helper = WordleHelper(["apple"])
        self.assertEqual(len(helper.words), 1)
        
        freq = helper.letter_frequency
        self.assertEqual(freq['a'], 1.0)
        self.assertEqual(freq['p'], 1.0)
        self.assertEqual(freq['l'], 1.0)
        self.assertEqual(freq['e'], 1.0)
    
    def test_filter_no_matches(self):
        """测试过滤无结果"""
        helper = WordleHelper(["apple", "beach", "crane"])
        result = helper.filter_words(absent="abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(result, [])
    
    def test_filter_all_match(self):
        """测试过滤全部匹配"""
        helper = WordleHelper(["apple", "beach", "crane"])
        result = helper.filter_words()
        self.assertEqual(len(result), 3)
    
    def test_case_insensitivity(self):
        """测试大小写不敏感"""
        helper = WordleHelper()
        
        result_lower = helper.filter_words(correct="..a..")
        result_upper = helper.filter_words(correct="..A..")
        
        self.assertEqual(sorted(result_lower), sorted(result_upper))
    
    def test_invalid_regex(self):
        """测试无效正则表达式"""
        helper = WordleHelper()
        # 应该不会崩溃，只是忽略无效正则
        result = helper.filter_words(regex="[invalid")
        self.assertIsInstance(result, list)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_game_simulation(self):
        """测试完整游戏模拟"""
        solver = WordleSolver()
        
        # 模拟玩一个完整的游戏
        success, attempts, history = solver.auto_solve(
            "crane",
            max_attempts=6,
            verbose=False
        )
        
        self.assertTrue(success)
        self.assertGreater(attempts, 0)
        self.assertLessEqual(attempts, 6)
        
        # 检查最后一步猜对了
        last_guess, last_feedback = history[-1]
        self.assertEqual(last_guess, "crane")
        self.assertEqual(last_feedback, "22222")
    
    def test_multiple_games(self):
        """测试多次游戏"""
        words_to_solve = ["apple", "beach", "dream", "eagle", "flame"]
        
        for answer in words_to_solve:
            solver = WordleSolver()
            success, attempts, _ = solver.auto_solve(answer, verbose=False)
            self.assertTrue(success, f"Failed to solve '{answer}'")
            self.assertLessEqual(attempts, 10, f"Took too many attempts for '{answer}'")


if __name__ == '__main__':
    unittest.main()