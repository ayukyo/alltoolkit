"""
情感检测工具模块测试
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from emotion_detection_utils.mod import (
    EmotionDetector,
    Emotion,
    Sentiment,
    EmotionResult,
    detect_emotion,
    get_sentiment,
    is_positive,
    is_negative
)


class TestEmotionDetector(unittest.TestCase):
    """情感检测器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.detector = EmotionDetector()
    
    def test_detect_chinese_joy(self):
        """测试中文快乐情感检测"""
        result = self.detector.detect("今天天气真好，心情特别愉快！")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
        self.assertEqual(result.sentiment, Sentiment.POSITIVE)
        self.assertGreater(result.confidence, 0)
        self.assertIn("愉快", result.keywords_found)
    
    def test_detect_chinese_sadness(self):
        """测试中文悲伤情感检测"""
        result = self.detector.detect("我很难过，失去了一位好朋友。")
        self.assertEqual(result.dominant_emotion, Emotion.SADNESS)
        self.assertEqual(result.sentiment, Sentiment.NEGATIVE)
        self.assertIn("难过", result.keywords_found)
    
    def test_detect_chinese_anger(self):
        """测试中文愤怒情感检测"""
        result = self.detector.detect("这太让人气愤了，我真的非常生气！")
        self.assertEqual(result.dominant_emotion, Emotion.ANGER)
        self.assertEqual(result.sentiment, Sentiment.NEGATIVE)
    
    def test_detect_chinese_fear(self):
        """测试中文恐惧情感检测"""
        result = self.detector.detect("我很害怕，不敢一个人走夜路。")
        self.assertEqual(result.dominant_emotion, Emotion.FEAR)
        self.assertEqual(result.sentiment, Sentiment.NEGATIVE)
    
    def test_detect_chinese_surprise(self):
        """测试中文惊讶情感检测"""
        result = self.detector.detect("哇，真是太不可思议了！")
        self.assertEqual(result.dominant_emotion, Emotion.SURPRISE)
        self.assertEqual(result.sentiment, Sentiment.NEUTRAL)
    
    def test_detect_chinese_disgust(self):
        """测试中文厌恶情感检测"""
        result = self.detector.detect("这东西太恶心了，让人作呕。")
        self.assertEqual(result.dominant_emotion, Emotion.DISGUST)
        self.assertEqual(result.sentiment, Sentiment.NEGATIVE)
    
    def test_detect_english_joy(self):
        """测试英文快乐情感检测"""
        result = self.detector.detect("I am so happy today! It's wonderful!")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
        self.assertEqual(result.sentiment, Sentiment.POSITIVE)
        self.assertIn("happy", result.keywords_found)
    
    def test_detect_english_sadness(self):
        """测试英文悲伤情感检测"""
        result = self.detector.detect("I feel so sad and lonely right now.")
        self.assertEqual(result.dominant_emotion, Emotion.SADNESS)
        self.assertEqual(result.sentiment, Sentiment.NEGATIVE)
    
    def test_detect_english_anger(self):
        """测试英文愤怒情感检测"""
        result = self.detector.detect("I am extremely angry about this situation!")
        self.assertEqual(result.dominant_emotion, Emotion.ANGER)
        self.assertEqual(result.sentiment, Sentiment.NEGATIVE)
    
    def test_detect_neutral(self):
        """测试中性文本检测"""
        result = self.detector.detect("今天下午三点开会。")
        self.assertEqual(result.dominant_emotion, Emotion.NEUTRAL)
        self.assertEqual(result.sentiment, Sentiment.NEUTRAL)
    
    def test_detect_empty_text(self):
        """测试空文本"""
        result = self.detector.detect("")
        self.assertEqual(result.dominant_emotion, Emotion.NEUTRAL)
        self.assertEqual(result.sentiment, Sentiment.NEUTRAL)
        self.assertEqual(result.confidence, 0.0)
    
    def test_detect_whitespace_only(self):
        """测试仅含空白的文本"""
        result = self.detector.detect("   \n\t  ")
        self.assertEqual(result.dominant_emotion, Emotion.NEUTRAL)
    
    def test_negation_handling(self):
        """测试否定词处理"""
        # "不高兴" 应该被反转
        result = self.detector.detect("我今天不高兴。")
        # 否定后快乐可能变成其他情感
        self.assertNotEqual(result.dominant_emotion, Emotion.JOY)
    
    def test_intensifier_handling(self):
        """测试增强词处理"""
        result1 = self.detector.detect("高兴")
        result2 = self.detector.detect("非常高兴")
        # 增强后的情感分数应该更高
        self.assertGreaterEqual(
            result2.emotion_scores[Emotion.JOY],
            result1.emotion_scores[Emotion.JOY]
        )
    
    def test_batch_detect(self):
        """测试批量检测"""
        texts = [
            "我很开心",
            "I am very sad",
            "这太让人愤怒了",
            "中性文本"
        ]
        results = self.detector.batch_detect(texts)
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0].dominant_emotion, Emotion.JOY)
        self.assertEqual(results[1].dominant_emotion, Emotion.SADNESS)
        self.assertEqual(results[2].dominant_emotion, Emotion.ANGER)
        self.assertEqual(results[3].dominant_emotion, Emotion.NEUTRAL)
    
    def test_get_emotion_distribution(self):
        """测试情感分布获取"""
        distribution = self.detector.get_emotion_distribution("我很开心也很兴奋")
        self.assertIsInstance(distribution, dict)
        self.assertIn("joy", distribution)
        self.assertGreaterEqual(distribution["joy"], 0)
        self.assertLessEqual(distribution["joy"], 1)
    
    def test_is_positive(self):
        """测试正面情感判断"""
        self.assertTrue(self.detector.is_positive("今天真是太棒了！"))
        self.assertFalse(self.detector.is_positive("我很伤心"))
    
    def test_is_negative(self):
        """测试负面情感判断"""
        self.assertTrue(self.detector.is_negative("我很愤怒"))
        self.assertFalse(self.detector.is_negative("今天天气真好"))
    
    def test_get_sentiment_score(self):
        """测试情感分数"""
        score_positive = self.detector.get_sentiment_score("我很开心快乐")
        score_negative = self.detector.get_sentiment_score("我非常伤心难过")
        score_neutral = self.detector.get_sentiment_score("今天天气一般")
        
        self.assertGreater(score_positive, 0)
        self.assertLess(score_negative, 0)
        self.assertAlmostEqual(score_neutral, 0, places=1)
    
    def test_mixed_emotions(self):
        """测试混合情感"""
        result = self.detector.detect("虽然取得了成功，但我还是很担心未来")
        # 应该检测到多种情感
        non_zero_emotions = sum(1 for score in result.emotion_scores.values() if score > 0)
        self.assertGreaterEqual(non_zero_emotions, 1)
    
    def test_emoji_detection(self):
        """测试表情符号检测"""
        result = self.detector.detect("😄 今天心情真好 😊")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
        self.assertEqual(result.sentiment, Sentiment.POSITIVE)
    
    def test_to_dict(self):
        """测试结果转换为字典"""
        result = self.detector.detect("我很开心")
        result_dict = result.to_dict()
        
        self.assertIn("dominant_emotion", result_dict)
        self.assertIn("emotion_scores", result_dict)
        self.assertIn("sentiment", result_dict)
        self.assertIn("confidence", result_dict)
        self.assertIn("keywords_found", result_dict)
        
        self.assertIsInstance(result_dict["emotion_scores"], dict)
        self.assertIn("joy", result_dict["emotion_scores"])
    
    def test_language_detection(self):
        """测试语言自动检测"""
        detector_auto = EmotionDetector(language="auto")
        
        result_zh = detector_auto.detect("我很开心")
        result_en = detector_auto.detect("I am very happy")
        
        self.assertEqual(result_zh.dominant_emotion, Emotion.JOY)
        self.assertEqual(result_en.dominant_emotion, Emotion.JOY)
    
    def test_chinese_language_setting(self):
        """测试中文语言设置"""
        detector_zh = EmotionDetector(language="zh")
        result = detector_zh.detect("我很开心")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
    
    def test_english_language_setting(self):
        """测试英文语言设置"""
        detector_en = EmotionDetector(language="en")
        result = detector_en.detect("I am very happy")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        # detect_emotion
        result = detect_emotion("我很开心")
        self.assertIsInstance(result, EmotionResult)
        
        # get_sentiment
        sentiment = get_sentiment("我很开心")
        self.assertEqual(sentiment, "positive")
        
        # is_positive
        self.assertTrue(is_positive("我很开心"))
        
        # is_negative
        self.assertTrue(is_negative("我很伤心"))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def setUp(self):
        self.detector = EmotionDetector()
    
    def test_long_text(self):
        """测试长文本"""
        long_text = "开心 " * 1000
        result = self.detector.detect(long_text)
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
    
    def test_special_characters(self):
        """测试特殊字符"""
        result = self.detector.detect("!!!???@@@###")
        self.assertEqual(result.dominant_emotion, Emotion.NEUTRAL)
    
    def test_numbers_only(self):
        """测试仅数字"""
        result = self.detector.detect("123 456 789")
        self.assertEqual(result.dominant_emotion, Emotion.NEUTRAL)
    
    def test_mixed_language(self):
        """测试混合语言"""
        result = self.detector.detect("I am 很 happy 开心")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
    
    def test_repeated_emotional_words(self):
        """测试重复情感词"""
        result = self.detector.detect("开心开心开心开心开心")
        self.assertEqual(result.dominant_emotion, Emotion.JOY)
    
    def test_conflicting_emotions(self):
        """测试冲突情感"""
        result = self.detector.detect("我既开心又伤心")
        # 应该有多个非零情感分数
        self.assertIn(result.dominant_emotion, [Emotion.JOY, Emotion.SADNESS])


if __name__ == "__main__":
    unittest.main()