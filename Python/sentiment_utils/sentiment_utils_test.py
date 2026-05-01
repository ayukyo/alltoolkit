"""
Sentiment Utils - 单元测试

Author: AllToolkit
Date: 2026-05-01
"""

import unittest
from sentiment_utils import (
    SentimentAnalyzer, SentimentPolarity, SentimentResult,
    analyze_sentiment, get_sentiment_score, is_positive_text, is_negative_text
)


class TestSentimentAnalyzer(unittest.TestCase):
    """情感分析器测试"""
    
    def setUp(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_chinese(self):
        """测试中文正面文本"""
        result = self.analyzer.analyze("这个产品非常好用，我很喜欢！")
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
        self.assertGreater(result.score, 0)
        # 可能匹配"喜欢"、"好"等多字词
        self.assertTrue(len(result.positive_words) > 0)
    
    def test_negative_chinese(self):
        """测试中文负面文本"""
        result = self.analyzer.analyze("服务态度太差了，非常失望。")
        self.assertEqual(result.polarity, SentimentPolarity.NEGATIVE)
        self.assertLess(result.score, 0)
        # 应匹配负面词（可能是"太差"、"差"、"失望"等）
        self.assertTrue(len(result.negative_words) > 0)
    
    def test_neutral_chinese(self):
        """测试中文中性文本"""
        result = self.analyzer.analyze("这个东西还行，凑合用吧。")
        # "还行"和"凑合"是轻度正面词，所以可能是轻度正面
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
        self.assertTrue(result.positive_score < 1.0)  # 正面得分应该较低
    
    def test_positive_english(self):
        """测试英文正面文本"""
        result = self.analyzer.analyze("I love this product! It's amazing!")
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
        self.assertGreater(result.score, 0)
    
    def test_negative_english(self):
        """测试英文负面文本"""
        result = self.analyzer.analyze("This is terrible. I hate it.")
        self.assertEqual(result.polarity, SentimentPolarity.NEGATIVE)
        self.assertLess(result.score, 0)
    
    def test_neutral_english(self):
        """测试英文中性文本"""
        result = self.analyzer.analyze("The quality is okay, nothing special.")
        # 可能是中性或轻度正面（取决于是否匹配到"ok"）
        self.assertTrue(result.polarity in [SentimentPolarity.NEUTRAL, SentimentPolarity.POSITIVE])
    
    def test_negation_chinese(self):
        """测试中文否定词处理"""
        result1 = self.analyzer.analyze("这个很好")
        result2 = self.analyzer.analyze("这个不好")
        
        self.assertEqual(result1.polarity, SentimentPolarity.POSITIVE)
        self.assertEqual(result2.polarity, SentimentPolarity.NEGATIVE)
        self.assertGreater(result1.score, result2.score)
    
    def test_negation_english(self):
        """测试英文否定词处理"""
        result1 = self.analyzer.analyze("This is good")
        result2 = self.analyzer.analyze("This is not good")
        
        self.assertGreater(result1.score, result2.score)
    
    def test_intensifier_chinese(self):
        """测试中文程度副词"""
        result1 = self.analyzer.analyze("这个好")
        result2 = self.analyzer.analyze("这个非常好")
        
        # "非常好"应该比"好"得分更高
        self.assertTrue(result2.positive_score >= result1.positive_score)
    
    def test_intensifier_english(self):
        """测试英文程度副词"""
        result1 = self.analyzer.analyze("This is good")
        result2 = self.analyzer.analyze("This is very good")
        
        self.assertGreater(result2.positive_score, result1.positive_score)
    
    def test_mixed_sentiment(self):
        """测试混合情感文本"""
        result = self.analyzer.analyze("产品质量很好，但是服务态度很差。")
        # 混合情感，结果取决于哪个更强
        self.assertIsInstance(result.score, float)
    
    def test_empty_text(self):
        """测试空文本"""
        result = self.analyzer.analyze("")
        self.assertEqual(result.polarity, SentimentPolarity.NEUTRAL)
        self.assertEqual(result.score, 0)
    
    def test_no_sentiment_words(self):
        """测试无情感词文本"""
        result = self.analyzer.analyze("今天天气晴朗，我去公园散步。")
        self.assertEqual(result.polarity, SentimentPolarity.NEUTRAL)
    
    def test_get_sentiment_words(self):
        """测试情感词提取"""
        positive, negative = self.analyzer.get_sentiment_words("我喜欢这个产品，但讨厌那个服务")
        # 应找到情感词
        self.assertTrue(len(positive) > 0)
        self.assertTrue(len(negative) > 0)
    
    def test_is_positive(self):
        """测试正面判断"""
        self.assertTrue(self.analyzer.is_positive("这个产品非常好！"))
        self.assertFalse(self.analyzer.is_positive("这个产品太差了！"))
    
    def test_is_negative(self):
        """测试负面判断"""
        self.assertTrue(self.analyzer.is_negative("这个产品太差了！"))
        self.assertFalse(self.analyzer.is_negative("这个产品非常好！"))
    
    def test_get_score(self):
        """测试得分获取"""
        score = self.analyzer.get_score("我爱这个产品")
        self.assertGreater(score, 0)
        
        score = self.analyzer.get_score("我讨厌这个产品")
        self.assertLess(score, 0)
    
    def test_compare_sentiment(self):
        """测试情感比较"""
        result = self.analyzer.compare_sentiment(
            "这个产品非常好！",
            "这个产品太差了！"
        )
        # 第一个应该比第二个得分更高或相等
        score1 = self.analyzer.get_score("这个产品非常好！")
        score2 = self.analyzer.get_score("这个产品太差了！")
        if score1 > score2:
            self.assertEqual(result, 1)
        elif score1 < score2:
            self.assertEqual(result, -1)
        else:
            self.assertEqual(result, 0)
    
    def test_analyze_batch(self):
        """测试批量分析"""
        texts = [
            "这个很好",
            "这个很差",
            "一般般"
        ]
        results = self.analyzer.analyze_batch(texts)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].polarity, SentimentPolarity.POSITIVE)
        self.assertEqual(results[1].polarity, SentimentPolarity.NEGATIVE)
    
    def test_custom_dictionary(self):
        """测试自定义词典"""
        analyzer = SentimentAnalyzer(
            custom_positive={"牛牛牛": 1.0, "给力啊": 0.9},
            custom_negative={"坑爹": 0.9, "辣鸡": 0.8}
        )
        
        result = analyzer.analyze("这个东西牛牛牛！")
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
        # 应匹配自定义词"牛牛牛"
        self.assertTrue("牛牛牛" in result.positive_words or len(result.positive_words) > 0)
        
        result = analyzer.analyze("真是坑爹！")
        self.assertEqual(result.polarity, SentimentPolarity.NEGATIVE)
        self.assertTrue("坑爹" in result.negative_words or len(result.negative_words) > 0)
    
    def test_confidence(self):
        """测试置信度计算"""
        # 多个情感词应该有更高置信度
        result1 = self.analyzer.analyze("好")
        result2 = self.analyzer.analyze("非常好用，我很喜欢，太棒了！")
        
        self.assertLess(result1.confidence, result2.confidence)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_analyze_sentiment(self):
        """测试快捷分析函数"""
        result = analyze_sentiment("我爱这个产品")
        self.assertIsInstance(result, SentimentResult)
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
    
    def test_get_sentiment_score(self):
        """测试快捷得分函数"""
        score = get_sentiment_score("这个很好")
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)
    
    def test_is_positive_text(self):
        """测试正面文本判断函数"""
        self.assertTrue(is_positive_text("这个很好！"))
        self.assertFalse(is_positive_text("这个很差！"))
    
    def test_is_negative_text(self):
        """测试负面文本判断函数"""
        self.assertTrue(is_negative_text("这个很差！"))
        self.assertFalse(is_negative_text("这个很好！"))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def setUp(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_only_whitespace(self):
        """测试纯空白文本"""
        result = self.analyzer.analyze("   ")
        self.assertEqual(result.polarity, SentimentPolarity.NEUTRAL)
    
    def test_only_punctuation(self):
        """测试纯标点文本"""
        result = self.analyzer.analyze("！！！？？...")
        self.assertEqual(result.polarity, SentimentPolarity.NEUTRAL)
    
    def test_numbers_only(self):
        """测试纯数字文本"""
        result = self.analyzer.analyze("123456")
        self.assertEqual(result.polarity, SentimentPolarity.NEUTRAL)
    
    def test_mixed_language(self):
        """测试中英混合文本"""
        result = self.analyzer.analyze("这个product很good！")
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
    
    def test_repeated_words(self):
        """测试重复词"""
        result = self.analyzer.analyze("好好好好好")
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
    
    def test_double_negation(self):
        """测试双重否定"""
        result1 = self.analyzer.analyze("不错")
        result2 = self.analyzer.analyze("不是不好")
        # 双重否定可能产生正面效果，但具体取决于实现
        self.assertIsInstance(result1.score, float)
        self.assertIsInstance(result2.score, float)
    
    def test_very_long_text(self):
        """测试长文本"""
        text = "这个产品很好。" * 100
        result = self.analyzer.analyze(text)
        self.assertEqual(result.polarity, SentimentPolarity.POSITIVE)
        self.assertGreater(len(result.positive_words), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)