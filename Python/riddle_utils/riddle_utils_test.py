"""
Riddle Utilities 测试文件

测试谜语工具库的核心功能
"""

import unittest
import sys
import os
from datetime import date

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riddle_utils import (
    RiddleManager,
    Riddle,
    Hint,
    RiddleCategory,
    RiddleDifficulty,
    RiddleLanguage,
    RiddleSession,
    RiddleGenerator,
    RiddleQuiz,
    get_random_riddle,
    get_daily_riddle,
    check_riddle_answer,
)


class TestRiddle(unittest.TestCase):
    """测试 Riddle 数据类"""
    
    def test_riddle_creation(self):
        """测试谜语创建"""
        riddle = Riddle(
            id="test_001",
            question="测试谜题",
            answer="测试答案",
            category=RiddleCategory.OBJECT,
            difficulty=RiddleDifficulty.EASY,
            language=RiddleLanguage.CHINESE,
        )
        
        self.assertEqual(riddle.id, "test_001")
        self.assertEqual(riddle.question, "测试谜题")
        self.assertEqual(riddle.answer, "测试答案")
        self.assertEqual(riddle.category, RiddleCategory.OBJECT)
        self.assertEqual(riddle.difficulty, RiddleDifficulty.EASY)
    
    def test_riddle_with_hints(self):
        """测试带提示的谜语"""
        hints = [
            Hint(1, "这是提示1", "category"),
            Hint(2, "这是提示2", "description"),
        ]
        
        riddle = Riddle(
            id="test_002",
            question="有提示的谜题",
            answer="答案",
            category=RiddleCategory.ANIMAL,
            difficulty=RiddleDifficulty.MEDIUM,
            language=RiddleLanguage.CHINESE,
            hints=hints,
        )
        
        self.assertEqual(len(riddle.hints), 2)
        self.assertEqual(riddle.hints[0].level, 1)
        self.assertEqual(riddle.hints[1].content, "这是提示2")
    
    def test_riddle_alternative_answers(self):
        """测试别名答案"""
        riddle = Riddle(
            id="test_003",
            question="谜题",
            answer="主答案",
            category=RiddleCategory.OBJECT,
            difficulty=RiddleDifficulty.EASY,
            language=RiddleLanguage.ENGLISH,
            alternative_answers=["别名1", "别名2"],
        )
        
        self.assertEqual(len(riddle.alternative_answers), 2)


class TestRiddleManager(unittest.TestCase):
    """测试 RiddleManager"""
    
    def setUp(self):
        """设置测试环境"""
        self.manager = RiddleManager(seed=42)
    
    def test_builtin_riddles_loaded(self):
        """测试内置谜语加载"""
        self.assertGreater(self.manager.count(), 0)
    
    def test_get_riddle(self):
        """测试获取谜语"""
        riddle = self.manager.get_riddle("zh_obj_001")
        
        self.assertIsNotNone(riddle)
        self.assertEqual(riddle.answer, "西瓜")
    
    def test_get_random(self):
        """测试获取随机谜语"""
        riddle = self.manager.get_random()
        
        self.assertIsNotNone(riddle)
        self.assertIsInstance(riddle, Riddle)
    
    def test_get_random_by_category(self):
        """测试按类别获取随机谜语"""
        riddle = self.manager.get_random(category=RiddleCategory.ANIMAL)
        
        self.assertEqual(riddle.category, RiddleCategory.ANIMAL)
    
    def test_get_random_by_difficulty(self):
        """测试按难度获取随机谜语"""
        riddle = self.manager.get_random(difficulty=RiddleDifficulty.EASY)
        
        self.assertEqual(riddle.difficulty, RiddleDifficulty.EASY)
    
    def test_get_random_by_language(self):
        """测试按语言获取随机谜语"""
        riddle = self.manager.get_random(language=RiddleLanguage.ENGLISH)
        
        self.assertEqual(riddle.language, RiddleLanguage.ENGLISH)
    
    def test_get_hint(self):
        """测试获取提示"""
        hint = self.manager.get_hint("zh_obj_001", level=1)
        
        self.assertIsNotNone(hint)
        self.assertEqual(hint.level, 1)
        self.assertIn("水果", hint.content)
    
    def test_get_hint_levels(self):
        """测试不同级别的提示"""
        hint1 = self.manager.get_hint("zh_obj_001", level=1)
        hint5 = self.manager.get_hint("zh_obj_001", level=5)
        
        self.assertEqual(hint1.level, 1)
        self.assertEqual(hint5.level, 5)
    
    def test_check_answer_correct(self):
        """测试正确答案"""
        is_correct, feedback = self.manager.check_answer("zh_obj_001", "西瓜")
        
        self.assertTrue(is_correct)
        self.assertIn("正确", feedback)
    
    def test_check_answer_wrong(self):
        """测试错误答案"""
        is_correct, feedback = self.manager.check_answer("zh_obj_001", "苹果")
        
        self.assertFalse(is_correct)
        self.assertIn("不对", feedback)
    
    def test_check_answer_alternative(self):
        """测试别名答案"""
        is_correct, feedback = self.manager.check_answer("en_obj_002", "footprints")
        
        self.assertTrue(is_correct)
    
    def test_check_answer_fuzzy(self):
        """测试模糊匹配"""
        # 测试带空格的答案
        is_correct, feedback = self.manager.check_answer("zh_obj_001", "西 瓜")
        
        self.assertTrue(is_correct)
    
    def test_check_answer_case_insensitive(self):
        """测试不区分大小写"""
        is_correct, feedback = self.manager.check_answer("en_obj_001", "KEYBOARD")
        
        self.assertTrue(is_correct)
    
    def test_get_daily_riddle(self):
        """测试每日谜语"""
        riddle1 = self.manager.get_daily_riddle(date(2024, 1, 1))
        riddle2 = self.manager.get_daily_riddle(date(2024, 1, 1))
        riddle3 = self.manager.get_daily_riddle(date(2024, 1, 2))
        
        # 同一天应该返回相同的谜语
        self.assertEqual(riddle1.id, riddle2.id)
        # 不同天可能返回不同的谜语
        # (注意：这个测试可能偶然失败，因为可能恰好在两天选择了同一个谜语)
    
    def test_get_by_category(self):
        """测试按类别获取所有谜语"""
        animals = self.manager.get_by_category(RiddleCategory.ANIMAL)
        
        for r in animals:
            self.assertEqual(r.category, RiddleCategory.ANIMAL)
    
    def test_get_by_difficulty(self):
        """测试按难度获取所有谜语"""
        easy_riddles = self.manager.get_by_difficulty(RiddleDifficulty.EASY)
        
        for r in easy_riddles:
            self.assertEqual(r.difficulty, RiddleDifficulty.EASY)
    
    def test_search(self):
        """测试搜索谜语"""
        results = self.manager.search("西瓜")
        
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertIn("西瓜", r.question.lower() + r.answer.lower())
    
    def test_add_riddle(self):
        """测试添加谜语"""
        new_riddle = Riddle(
            id="new_001",
            question="新谜题",
            answer="新答案",
            category=RiddleCategory.OBJECT,
            difficulty=RiddleDifficulty.EASY,
            language=RiddleLanguage.CHINESE,
        )
        
        self.manager.add_riddle(new_riddle)
        self.assertIsNotNone(self.manager.get_riddle("new_001"))
    
    def test_remove_riddle(self):
        """测试移除谜语"""
        # 先添加一个谜语
        new_riddle = Riddle(
            id="remove_001",
            question="要删除的谜题",
            answer="答案",
            category=RiddleCategory.OBJECT,
            difficulty=RiddleDifficulty.EASY,
            language=RiddleLanguage.CHINESE,
        )
        
        self.manager.add_riddle(new_riddle)
        self.assertTrue(self.manager.remove_riddle("remove_001"))
        self.assertIsNone(self.manager.get_riddle("remove_001"))
    
    def test_count_by_category(self):
        """测试按类别统计"""
        counts = self.manager.count_by_category()
        
        self.assertGreater(len(counts), 0)
        self.assertIn(RiddleCategory.OBJECT, counts)
    
    def test_get_categories(self):
        """测试获取所有类别"""
        categories = self.manager.get_categories()
        
        self.assertGreater(len(categories), 0)
    
    def test_export_import(self):
        """测试导出导入"""
        data = self.manager.export_to_dict()
        
        self.assertIn("riddles", data)
        self.assertGreater(len(data["riddles"]), 0)
        
        # 创建新管理器并导入
        new_manager = RiddleManager()
        new_manager.import_from_dict(data)
        
        self.assertGreater(new_manager.count(), 0)


class TestRiddleSession(unittest.TestCase):
    """测试 RiddleSession"""
    
    def test_session_creation(self):
        """测试会话创建"""
        session = RiddleSession(riddle_id="test_001")
        
        self.assertEqual(session.riddle_id, "test_001")
        self.assertEqual(session.hints_used, 0)
        self.assertEqual(session.attempts, 0)
        self.assertFalse(session.solved)
    
    def test_session_calculate_score(self):
        """测试得分计算"""
        session = RiddleSession(riddle_id="test_001")
        
        # 没有提示和错误尝试
        score = session.calculate_score()
        self.assertEqual(score, 100)
        
        # 使用了提示
        session.hints_used = 2
        score = session.calculate_score()
        self.assertEqual(score, 70)  # 100 - 2*15
        
        # 有错误尝试
        session.attempts = 3
        score = session.calculate_score()
        self.assertEqual(score, 60)  # 100 - 2*15 - 2*5
    
    def test_session_minimum_score(self):
        """测试最低分数"""
        session = RiddleSession(riddle_id="test_001")
        session.hints_used = 10
        session.attempts = 20
        
        score = session.calculate_score()
        self.assertEqual(score, 0)  # 不应该为负数


class TestRiddleGenerator(unittest.TestCase):
    """测试 RiddleGenerator"""
    
    def setUp(self):
        self.generator = RiddleGenerator(seed=42)
    
    def test_generate_object_riddle(self):
        """测试生成物品谜语"""
        features = {
            "missing": "脚",
            "ability": "报时",
            "cannot": "走",
            "category_hint": "这是日常用品",
            "first_letter": "钟",
            "explanation": "钟表能显示时间但不能走路。",
        }
        
        riddle = self.generator.generate_object_riddle("钟表", features)
        
        self.assertEqual(riddle.answer, "钟表")
        self.assertEqual(riddle.category, RiddleCategory.OBJECT)
        self.assertGreater(len(riddle.hints), 0)
    
    def test_generate_character_riddle(self):
        """测试生成字谜"""
        riddle = self.generator.generate_character_riddle(
            character="日",
            composition="太阳从地上升起",
            meaning="太阳",
        )
        
        self.assertEqual(riddle.answer, "日")
        self.assertEqual(riddle.category, RiddleCategory.CHARACTER)
        self.assertIn("日", riddle.explanation)


class TestRiddleQuiz(unittest.TestCase):
    """测试 RiddleQuiz"""
    
    def setUp(self):
        self.quiz = RiddleQuiz()
    
    def test_start_round(self):
        """测试开始新一轮"""
        riddle = self.quiz.start_round()
        
        self.assertIsNotNone(riddle)
        self.assertIsNotNone(self.quiz._current_riddle)
    
    def test_current_question(self):
        """测试获取当前问题"""
        self.quiz.start_round()
        question = self.quiz.current_question()
        
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 0)
    
    def test_get_hint(self):
        """测试获取提示"""
        self.quiz.start_round()
        hint = self.quiz.get_hint()
        
        self.assertIn("提示", hint)
    
    def test_answer_correct(self):
        """测试正确回答"""
        self.quiz.start_round()
        result = self.quiz.answer(self.quiz._current_riddle.answer)
        
        self.assertTrue(result["correct"])
        self.assertGreater(result["score"], 0)
    
    def test_answer_wrong(self):
        """测试错误回答"""
        self.quiz.start_round()
        result = self.quiz.answer("错误答案")
        
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)
    
    def test_answer_with_hints(self):
        """测试使用提示后回答"""
        self.quiz.start_round()
        self.quiz.get_hint()
        self.quiz.get_hint()
        
        result = self.quiz.answer(self.quiz._current_riddle.answer)
        
        self.assertTrue(result["correct"])
        # 使用提示后分数应该降低
        self.assertEqual(result["hints_used"], 2)
    
    def test_give_up(self):
        """测试放弃"""
        self.quiz.start_round()
        result = self.quiz.give_up()
        
        self.assertFalse(result["correct"])
        self.assertIsNotNone(result["answer"])
    
    def test_get_stats(self):
        """测试获取统计"""
        self.quiz.start_round()
        self.quiz.answer(self.quiz._current_riddle.answer)
        
        stats = self.quiz.get_stats()
        
        self.assertEqual(stats["rounds_played"], 1)
        self.assertEqual(stats["correct_answers"], 1)
        self.assertGreater(stats["total_score"], 0)
    
    def test_reset(self):
        """测试重置"""
        self.quiz.start_round()
        self.quiz.answer(self.quiz._current_riddle.answer)
        
        self.quiz.reset()
        
        stats = self.quiz.get_stats()
        self.assertEqual(stats["rounds_played"], 0)
        self.assertEqual(stats["total_score"], 0)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_random_riddle(self):
        """测试获取随机谜语函数"""
        riddle = get_random_riddle()
        
        self.assertIsNotNone(riddle)
        self.assertIsInstance(riddle, Riddle)
    
    def test_get_random_riddle_with_params(self):
        """测试带参数的获取随机谜语"""
        riddle = get_random_riddle(language="en")
        
        self.assertEqual(riddle.language, RiddleLanguage.ENGLISH)
    
    def test_get_daily_riddle(self):
        """测试获取每日谜语"""
        riddle = get_daily_riddle()
        
        self.assertIsNotNone(riddle)
    
    def test_check_riddle_answer(self):
        """测试检查答案函数"""
        manager = RiddleManager()
        riddle = manager.get_random()
        
        is_correct, feedback = check_riddle_answer(riddle.id, riddle.answer)
        
        self.assertTrue(is_correct)


class TestStringSimilarity(unittest.TestCase):
    """测试字符串相似度"""
    
    def setUp(self):
        self.manager = RiddleManager()
    
    def test_similarity_identical(self):
        """测试相同字符串"""
        similarity = self.manager._calculate_similarity("abc", "abc")
        
        self.assertEqual(similarity, 1.0)
    
    def test_similarity_different(self):
        """测试不同字符串"""
        similarity = self.manager._calculate_similarity("abc", "xyz")
        
        self.assertLess(similarity, 0.5)
    
    def test_similarity_similar(self):
        """测试相似字符串"""
        similarity = self.manager._calculate_similarity("abc", "abd")
        
        self.assertGreater(similarity, 0.5)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_game_flow(self):
        """测试完整游戏流程"""
        quiz = RiddleQuiz()
        
        # 开始三轮游戏
        for _ in range(3):
            quiz.start_round()
            
            # 使用一个提示
            quiz.get_hint()
            
            # 回答
            quiz.answer(quiz._current_riddle.answer)
        
        stats = quiz.get_stats()
        
        self.assertEqual(stats["rounds_played"], 3)
        self.assertEqual(stats["correct_answers"], 3)
        self.assertGreater(stats["total_score"], 0)
    
    def test_riddle_categories_coverage(self):
        """测试类别覆盖"""
        manager = RiddleManager()
        
        categories_found = set()
        for _ in range(50):
            try:
                riddle = manager.get_random()
                categories_found.add(riddle.category)
            except ValueError:
                break
        
        # 应该有多个类别
        self.assertGreater(len(categories_found), 3)
    
    def test_riddle_difficulties_coverage(self):
        """测试难度覆盖"""
        manager = RiddleManager()
        
        difficulties_found = set()
        for _ in range(50):
            try:
                riddle = manager.get_random()
                difficulties_found.add(riddle.difficulty)
            except ValueError:
                break
        
        # 应该有多个难度级别
        self.assertGreater(len(difficulties_found), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)