"""
Sentiment Analysis Utils - 零依赖情感分析工具

支持中英文情感分析，基于词典的方法。
功能：
- 情感极性判断（正面/负面/中性）
- 情感得分计算
- 程度副词加权
- 否定词处理
- 情感词提取

Author: AllToolkit
Date: 2026-05-01
"""

import re
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


class SentimentPolarity(Enum):
    """情感极性枚举"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class SentimentResult:
    """情感分析结果"""
    polarity: SentimentPolarity
    score: float  # -1.0 到 1.0
    positive_score: float
    negative_score: float
    positive_words: List[str]
    negative_words: List[str]
    confidence: float  # 0.0 到 1.0


class SentimentAnalyzer:
    """
    情感分析器
    
    基于词典的情感分析，支持中英文。
    使用方法：
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze("这个产品非常好用，我很喜欢！")
        print(result.polarity)  # SentimentPolarity.POSITIVE
        print(result.score)     # 0.8
    """
    
    # 中文正面情感词（多字词优先）
    CHINESE_POSITIVE = {
        # 高度正面（多字词）
        "喜欢": 0.9, "开心": 0.9, "快乐": 0.9, "幸福": 0.9,
        "优秀": 0.9, "出色": 0.9, "精彩": 0.9, "完美": 1.0,
        "热爱": 0.9, "最爱": 1.0, "超赞": 0.9, "极好": 0.9,
        # 中度正面（多字词）
        "不错": 0.7, "满意": 0.7, "舒服": 0.7, "舒适": 0.7,
        "推荐": 0.6, "感谢": 0.7, "给力": 0.8, "很好": 0.8,
        "好用": 0.7, "方便": 0.6, "实用": 0.6, "靠谱": 0.7,
        "值得": 0.7, "放心": 0.6, "惊喜": 0.8, "感动": 0.8,
        "温馨": 0.7, "甜蜜": 0.8, "可爱": 0.7, "美丽": 0.7,
        "漂亮": 0.7, "帅气": 0.7, "聪明": 0.6, "善良": 0.7,
        "友好": 0.6, "热情": 0.6, "专业": 0.6, "高效": 0.7,
        "便捷": 0.6, "成功": 0.7, "胜利": 0.8, "进步": 0.6,
        "提升": 0.6, "改善": 0.5, "厉害": 0.8, "很好": 0.8,
        # 轻度正面
        "还行": 0.4, "可以": 0.4, "凑合": 0.2, "过得去": 0.3,
        # 单字正面词
        "爱": 1.0, "棒": 0.8, "好": 0.7, "赞": 0.8, "牛": 0.8, "强": 0.7,
    }
    
    # 中文负面情感词（多字词优先）
    CHINESE_NEGATIVE = {
        # 高度负面（多字词）
        "讨厌": 0.9, "愤怒": 0.9, "恶心": 0.9, "垃圾": 0.9,
        "糟糕": 0.8, "失望": 0.7, "绝望": 0.9, "痛恨": 0.9,
        "很差": 0.8, "太差": 0.9, "极差": 0.9, "差劲": 0.8,
        # 中度负面（多字词）
        "不好": 0.6, "不满": 0.6, "难受": 0.6, "痛苦": 0.8,
        "伤心": 0.7, "生气": 0.7, "烦躁": 0.6, "无聊": 0.5,
        "难用": 0.7, "坑人": 0.7, "欺骗": 0.8, "后悔": 0.7,
        "浪费": 0.6, "损失": 0.6, "伤害": 0.7, "可怕": 0.7,
        "恐怖": 0.8, "危险": 0.6, "担心": 0.5, "害怕": 0.6,
        # 轻度负面
        "一般": 0.3, "勉强": 0.4,
        # 单字负面词
        "恨": 1.0, "烂": 0.8, "差": 0.7, "烦": 0.6, "累": 0.5,
        "坑": 0.7, "假": 0.6, "慢": 0.5, "卡": 0.5,
    }
    
    # 程度副词（加强词）
    CHINESE_INTENSIFIERS = {
        "非常": 1.5, "特别": 1.5, "十分": 1.4, "极其": 1.8, "超级": 1.6,
        "很": 1.3, "太": 1.5, "真的": 1.2, "实在": 1.3, "相当": 1.3,
        "格外": 1.4, "尤其": 1.4, "异常": 1.5, "万分": 1.7, "无比": 1.8,
        "比较": 1.1, "稍微": 0.7, "略微": 0.6, "有点": 0.6, "一些": 0.8,
        "越": 1.2, "更": 1.2, "最": 1.8, "极为": 1.7, "甚为": 1.5,
    }
    
    # 否定词
    CHINESE_NEGATORS = {
        "不", "不是", "没有", "没", "无", "非", "未", "别", "莫", "勿",
        "并不", "并非", "不是", "不再", "不会", "不要", "不再",
    }
    
    # 英文正面情感词
    ENGLISH_POSITIVE = {
        # High positive
        "love": 1.0, "excellent": 0.9, "amazing": 0.9, "wonderful": 0.9,
        "fantastic": 0.9, "perfect": 1.0, "brilliant": 0.9, "awesome": 0.9,
        # Medium positive
        "good": 0.7, "great": 0.8, "nice": 0.6, "happy": 0.7, "glad": 0.6,
        "like": 0.6, "enjoy": 0.7, "pleased": 0.6, "satisfied": 0.7,
        # Mild positive
        "ok": 0.3, "okay": 0.3, "fine": 0.4, "decent": 0.4, "alright": 0.3,
        # Other positive
        "beautiful": 0.7, "helpful": 0.6, "useful": 0.6, "convenient": 0.6,
        "comfortable": 0.6, "friendly": 0.6, "professional": 0.6, "efficient": 0.7,
        "success": 0.7, "successful": 0.7, "win": 0.7, "improve": 0.6,
        "recommend": 0.7, "worth": 0.6, "reliable": 0.6, "trust": 0.6,
        "best": 0.8, "better": 0.7, "cool": 0.6, "fun": 0.6, "easy": 0.5,
    }
    
    # 英文负面情感词
    ENGLISH_NEGATIVE = {
        # High negative
        "hate": 1.0, "terrible": 0.9, "awful": 0.9, "horrible": 0.9,
        "disgusting": 0.9, "worst": 1.0, "crap": 0.8, "garbage": 0.8,
        # Medium negative
        "bad": 0.7, "poor": 0.6, "sad": 0.6, "angry": 0.7, "upset": 0.6,
        "disappointed": 0.7, "frustrated": 0.6, "annoyed": 0.5, "boring": 0.5,
        # Mild negative
        "meh": 0.4, "mediocre": 0.4, "average": 0.3, "acceptable": 0.2,
        # Other negative
        "problem": 0.5, "error": 0.5, "fail": 0.7, "failure": 0.7, "bug": 0.5,
        "difficult": 0.4, "hard": 0.3, "slow": 0.5, "broken": 0.7, "crash": 0.8,
        "waste": 0.6, "useless": 0.7, "fake": 0.6, "scam": 0.8, "dangerous": 0.7,
        "regret": 0.7, "sorry": 0.5, "worried": 0.5, "afraid": 0.6, "fear": 0.6,
    }
    
    # 英文程度副词
    ENGLISH_INTENSIFIERS = {
        "very": 1.3, "really": 1.3, "extremely": 1.6, "absolutely": 1.5,
        "incredibly": 1.5, "totally": 1.4, "completely": 1.4, "highly": 1.3,
        "so": 1.2, "too": 1.3, "quite": 1.2, "pretty": 1.1, "fairly": 1.1,
        "rather": 1.1, "super": 1.4, "ultra": 1.5, "most": 1.5, "amazingly": 1.5,
        "slightly": 0.6, "somewhat": 0.7, "a bit": 0.6, "a little": 0.6,
        "kind of": 0.7, "sort of": 0.7, "barely": 0.5, "hardly": 0.5,
    }
    
    # 英文否定词
    ENGLISH_NEGATORS = {
        "not", "no", "never", "neither", "nobody", "nothing", "nowhere",
        "none", "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't",
        "hadn't", "doesn't", "don't", "didn't", "won't", "wouldn't", "couldn't",
        "shouldn't", "can't", "cannot", "mustn't", "needn't", "without",
    }
    
    def __init__(self, custom_positive: Dict[str, float] = None,
                 custom_negative: Dict[str, float] = None,
                 custom_intensifiers: Dict[str, float] = None,
                 custom_negators: set = None):
        """
        初始化情感分析器
        
        Args:
            custom_positive: 自定义正面词词典
            custom_negative: 自定义负面词词典
            custom_intensifiers: 自定义程度副词词典
            custom_negators: 自定义否定词集合
        """
        # 合并默认词典和自定义词典
        self.positive_words = {**self.CHINESE_POSITIVE, **self.ENGLISH_POSITIVE}
        self.negative_words = {**self.CHINESE_NEGATIVE, **self.ENGLISH_NEGATIVE}
        self.intensifiers = {**self.CHINESE_INTENSIFIERS, **self.ENGLISH_INTENSIFIERS}
        self.negators = self.CHINESE_NEGATORS | self.ENGLISH_NEGATORS
        
        if custom_positive:
            self.positive_words.update(custom_positive)
        if custom_negative:
            self.negative_words.update(custom_negative)
        if custom_intensifiers:
            self.intensifiers.update(custom_intensifiers)
        if custom_negators:
            self.negators.update(custom_negators)
    
    def _tokenize(self, text: str) -> List[str]:
        """
        分词（简单实现，零依赖）
        
        优先匹配多字词，然后匹配单字。
        对于英文按空格分词
        """
        tokens = []
        text_lower = text.lower()
        
        # 先提取多字中文词（按词典优先）
        all_words = set(self.positive_words.keys()) | set(self.negative_words.keys()) | \
                    set(self.intensifiers.keys()) | self.negators
        
        # 按长度降序排序，优先匹配长词
        sorted_words = sorted([w for w in all_words if len(w) > 1 and '\u4e00' <= w[0] <= '\u9fff'],
                              key=len, reverse=True)
        
        # 标记已匹配的位置
        matched_positions = set()
        
        # 先匹配多字词
        for word in sorted_words:
            start = 0
            while True:
                pos = text.find(word, start)
                if pos == -1:
                    break
                # 检查是否与已匹配的位置重叠
                word_positions = set(range(pos, pos + len(word)))
                if not word_positions & matched_positions:
                    tokens.append(word.lower())
                    matched_positions.update(word_positions)
                start = pos + 1
        
        # 匹配英文单词
        pattern = r'[a-zA-Z]+'
        for match in re.finditer(pattern, text_lower):
            start = match.start()
            word_positions = set(range(start, match.end()))
            if not word_positions & matched_positions:
                tokens.append(match.group())
                matched_positions.update(word_positions)
        
        # 最后匹配单字中文词
        for i, char in enumerate(text):
            if i in matched_positions:
                continue
            if '\u4e00' <= char <= '\u9fff':
                # 只有当这个单字在词典中时才添加
                if char in self.positive_words or char in self.negative_words:
                    tokens.append(char)
                    matched_positions.add(i)
        
        return tokens
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言（简单实现）"""
        chinese_count = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_count = len(re.sub(r'\s', '', text))
        
        if total_count == 0:
            return 'unknown'
        
        chinese_ratio = chinese_count / total_count
        if chinese_ratio > 0.3:
            return 'chinese'
        return 'english'
    
    def analyze(self, text: str) -> SentimentResult:
        """
        分析文本情感
        
        Args:
            text: 要分析的文本
            
        Returns:
            SentimentResult: 分析结果
        """
        tokens = self._tokenize(text)
        
        positive_score = 0.0
        negative_score = 0.0
        positive_words_found = []
        negative_words_found = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # 检查是否是情感词
            is_positive = token in self.positive_words
            is_negative = token in self.negative_words
            
            if is_positive or is_negative:
                # 计算修饰因子
                modifier = 1.0
                is_negated = False
                
                # 检查前2个词是否有否定词或程度副词
                for j in range(max(0, i - 2), i):
                    prev_token = tokens[j]
                    if prev_token in self.negators:
                        is_negated = True
                    elif prev_token in self.intensifiers:
                        modifier *= self.intensifiers[prev_token]
                
                # 计算得分
                if is_positive:
                    score = self.positive_words[token] * modifier
                    if is_negated:
                        negative_score += score
                        negative_words_found.append(f"不{token}")
                    else:
                        positive_score += score
                        positive_words_found.append(token)
                else:  # is_negative
                    score = self.negative_words[token] * modifier
                    if is_negated:
                        positive_score += score * 0.5  # 否定负面词，正向效果较弱
                        positive_words_found.append(f"不{token}")
                    else:
                        negative_score += score
                        negative_words_found.append(token)
            
            i += 1
        
        # 计算最终得分
        total_score = positive_score + negative_score
        if total_score > 0:
            final_score = (positive_score - negative_score) / total_score
        else:
            final_score = 0.0
        
        # 确定极性
        if final_score > 0.1:
            polarity = SentimentPolarity.POSITIVE
        elif final_score < -0.1:
            polarity = SentimentPolarity.NEGATIVE
        else:
            polarity = SentimentPolarity.NEUTRAL
        
        # 计算置信度
        word_count = len(positive_words_found) + len(negative_words_found)
        confidence = min(1.0, word_count / 3)  # 至少3个情感词才达到高置信度
        
        return SentimentResult(
            polarity=polarity,
            score=round(final_score, 3),
            positive_score=round(positive_score, 3),
            negative_score=round(negative_score, 3),
            positive_words=positive_words_found,
            negative_words=negative_words_found,
            confidence=round(confidence, 3)
        )
    
    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """批量分析文本"""
        return [self.analyze(text) for text in texts]
    
    def get_sentiment_words(self, text: str) -> Tuple[List[str], List[str]]:
        """
        提取文本中的情感词
        
        Returns:
            (正面词列表, 负面词列表)
        """
        tokens = self._tokenize(text)
        positive = []
        negative = []
        
        for token in tokens:
            if token in self.positive_words:
                positive.append(token)
            elif token in self.negative_words:
                negative.append(token)
        
        return positive, negative
    
    def is_positive(self, text: str, threshold: float = 0.1) -> bool:
        """判断文本是否为正面"""
        result = self.analyze(text)
        return result.score > threshold
    
    def is_negative(self, text: str, threshold: float = -0.1) -> bool:
        """判断文本是否为负面"""
        result = self.analyze(text)
        return result.score < threshold
    
    def get_score(self, text: str) -> float:
        """获取情感得分（-1.0 到 1.0）"""
        return self.analyze(text).score
    
    def compare_sentiment(self, text1: str, text2: str) -> int:
        """
        比较两段文本的情感
        
        Returns:
            1: text1更正面
            -1: text2更正面
            0: 情感相同
        """
        score1 = self.get_score(text1)
        score2 = self.get_score(text2)
        
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        return 0


def analyze_sentiment(text: str) -> SentimentResult:
    """
    快捷函数：分析文本情感
    
    Args:
        text: 要分析的文本
        
    Returns:
        SentimentResult: 分析结果
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)


def get_sentiment_score(text: str) -> float:
    """快捷函数：获取情感得分"""
    return analyze_sentiment(text).score


def is_positive_text(text: str) -> bool:
    """快捷函数：判断是否为正面文本"""
    return analyze_sentiment(text).polarity == SentimentPolarity.POSITIVE


def is_negative_text(text: str) -> bool:
    """快捷函数：判断是否为负面文本"""
    return analyze_sentiment(text).polarity == SentimentPolarity.NEGATIVE


if __name__ == "__main__":
    # 简单测试
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "这个产品非常好用，我很喜欢！",
        "服务态度太差了，非常失望。",
        "这个东西还行，凑合用吧。",
        "I love this product! It's amazing!",
        "This is terrible. I hate it.",
        "The quality is okay, nothing special.",
    ]
    
    print("=" * 60)
    print("Sentiment Analysis Demo")
    print("=" * 60)
    
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\n文本: {text}")
        print(f"极性: {result.polarity.value}")
        print(f"得分: {result.score}")
        print(f"正面词: {result.positive_words}")
        print(f"负面词: {result.negative_words}")
        print(f"置信度: {result.confidence}")