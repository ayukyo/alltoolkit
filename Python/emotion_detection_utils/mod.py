"""
情感检测工具模块 (Emotion Detection Utils)

功能：
- 基于情感词典的文本情感分析
- 支持中文和英文情感检测
- 提供多种情感维度分析（快乐、悲伤、愤怒、恐惧、惊讶、厌恶）
- 零外部依赖，使用内置词典

使用示例：
    from emotion_detection_utils import EmotionDetector
    
    detector = EmotionDetector()
    result = detector.detect("今天天气真好，心情特别愉快！")
    print(result)
    # {'dominant_emotion': 'joy', 'scores': {'joy': 0.8, 'sadness': 0.0, ...}, 'sentiment': 'positive'}
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re


class Emotion(Enum):
    """情感类型枚举"""
    JOY = "joy"           # 快乐
    SADNESS = "sadness"   # 悲伤
    ANGER = "anger"       # 愤怒
    FEAR = "fear"         # 恐惧
    SURPRISE = "surprise" # 惊讶
    DISGUST = "disgust"   # 厌恶
    NEUTRAL = "neutral"   # 中性


class Sentiment(Enum):
    """情感极性"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class EmotionResult:
    """情感检测结果"""
    dominant_emotion: Emotion
    emotion_scores: Dict[Emotion, float]
    sentiment: Sentiment
    confidence: float
    keywords_found: List[str]
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "dominant_emotion": self.dominant_emotion.value,
            "emotion_scores": {e.value: s for e, s in self.emotion_scores.items()},
            "sentiment": self.sentiment.value,
            "confidence": self.confidence,
            "keywords_found": self.keywords_found
        }


# 中文情感词典
CHINESE_EMOTION_WORDS = {
    Emotion.JOY: [
        "开心", "快乐", "高兴", "愉快", "幸福", "欢乐", "欣喜", "喜悦", "兴奋", "激动",
        "满意", "满足", "舒适", "惬意", "甜蜜", "美好", "灿烂", "阳光", "温暖", "轻松",
        "感激", "感动", "欣慰", "自豪", "骄傲", "自信", "期待", "希望", "向往", "憧憬",
        "哈哈", "呵呵", "嘻嘻", "😄", "😊", "😁", "😀", "🥰", "😍", "🤗",
        "棒", "赞", "好", "不错", "厉害", "优秀", "精彩", "完美", "赞", "牛逼",
        "太棒了", "太好了", "太赞了", "最好", "最棒", "太厉害了"
    ],
    Emotion.SADNESS: [
        "悲伤", "难过", "伤心", "痛苦", "忧郁", "沮丧", "失落", "绝望", "哀伤", "凄凉",
        "孤独", "寂寞", "凄惨", "悲惨", "心痛", "心疼", "难过", "眼泪", "哭泣", "流泪",
        "遗憾", "惋惜", "失望", "落寞", "惆怅", "忧伤", "愁苦", "愁闷", "郁闷", "消沉",
        "😔", "😢", "😭", "😞", "💔", "😢", "😥", "😟"
    ],
    Emotion.ANGER: [
        "愤怒", "生气", "恼火", "恼怒", "气愤", "愤慨", "暴怒", "震怒", "激愤", "恼恨",
        "讨厌", "厌恶", "憎恨", "怨恨", "敌意", "仇恨", "憎恶", "厌烦", "烦躁", "焦躁",
        "火大", "不爽", "气愤", "气死", "气炸", "憋气", "窝火", "发火", "发怒", "发狂",
        "😡", "😤", "😠", "💢", "🤬"
    ],
    Emotion.FEAR: [
        "害怕", "恐惧", "惊恐", "惊慌", "恐慌", "畏惧", "惧怕", "担心", "担忧", "忧虑",
        "焦虑", "紧张", "不安", "惶恐", "恐慌", "惊惧", "害怕", "悚然", "毛骨悚然", "不寒而栗",
        "提心吊胆", "惴惴不安", "心惊胆战", "战战兢兢", "如履薄冰", "如临深渊",
        "😨", "😰", "😱", "😳", "😰"
    ],
    Emotion.SURPRISE: [
        "惊讶", "惊奇", "吃惊", "惊喜", "意外", "意外", "突然", "震惊", "震撼", "惊奇",
        "不可思议", "难以置信", "出乎意料", "始料未及", "猝不及防", "没想到", "居然",
        "竟然", "居然", "天哪", "天啊", "哇", "哇塞", "厉害了", "神了",
        "😲", "😮", "😯", "🤯", "😱", "😳", "🫢"
    ],
    Emotion.DISGUST: [
        "恶心", "厌恶", "讨厌", "厌烦", "反感", "排斥", "憎恶", "厌弃", "嫌弃", "鄙夷",
        "恶心死了", "令人作呕", "令人反感", "让人恶心", "看不惯", "受不了", "忍无可忍",
        "俗气", "低俗", "庸俗", "粗俗", "猥琐", "猥亵", "肮脏", "污秽",
        "🤢", "🤮", "😒", "🙄", "🤦"
    ]
}

# 英文情感词典
ENGLISH_EMOTION_WORDS = {
    Emotion.JOY: [
        "happy", "joy", "joyful", "glad", "pleased", "delighted", "cheerful", "thrilled",
        "excited", "exciting", "wonderful", "amazing", "fantastic", "great", "excellent",
        "awesome", "brilliant", "superb", "perfect", "beautiful", "lovely", "nice",
        "love", "loving", "loved", "like", "enjoy", "enjoyed", "enjoying",
        "smile", "smiling", "laugh", "laughing", "haha", "hehe", "lol", "haha",
        "😄", "😊", "😁", "😀", "🥰", "😍", "🤗", "congratulations", "congrats",
        "thankful", "grateful", "blessed", "lucky", "fortunate", "proud", "confident"
    ],
    Emotion.SADNESS: [
        "sad", "sorrow", "sorrowful", "unhappy", "depressed", "depression", "gloomy",
        "miserable", "heartbroken", "heartbreak", "grief", "grieving", "cry", "crying",
        "tears", "tearful", "weep", "weeping", "lonely", "loneliness", "alone",
        "disappointed", "disappointing", "disappointment", "hopeless", "hopelessness",
        "despair", "desperate", "pain", "painful", "hurt", "hurtful",
        "😔", "😢", "😭", "😞", "💔", "😥", "😟", "miss", "missing", "regret"
    ],
    Emotion.ANGER: [
        "angry", "anger", "mad", "furious", "rage", "enraged", "outrage", "outraged",
        "annoyed", "annoying", "irritated", "irritating", "frustrated", "frustrating",
        "hate", "hated", "hatred", "hostile", "hostility", "aggressive", "aggression",
        "upset", "pissed", "offended", "offensive", "disgusted", "disgust",
        "😡", "😤", "😠", "💢", "🤬", "damn", "hell", "suck", "sucks"
    ],
    Emotion.FEAR: [
        "fear", "afraid", "scared", "scary", "frightened", "frightening", "terrified",
        "terrifying", "horror", "horrified", "horrifying", "panic", "panicked",
        "anxious", "anxiety", "worried", "worry", "worrying", "concerned", "concern",
        "nervous", "uneasy", "apprehensive", "dread", "dreadful", "alarming",
        "😨", "😰", "😱", "😳", "threat", "dangerous", "danger", "risk", "risky"
    ],
    Emotion.SURPRISE: [
        "surprise", "surprised", "surprising", "amazed", "amazing", "astonished",
        "astonishing", "shocked", "shocking", "stunned", "stunning", "unexpected",
        "sudden", "suddenly", "wow", "whoa", "omg", "oh my god", "unbelievable",
        "incredible", "remarkable", "extraordinary", "phenomenal", "mind-blowing",
        "😲", "😮", "😯", "🤯", "😱", "😳", "🫢", "actually", "really"
    ],
    Emotion.DISGUST: [
        "disgust", "disgusted", "disgusting", "gross", "yuck", "eww", "nasty",
        "revolting", "repulsive", "repugnant", "loath", "loathe", "detest", "detestable",
        "abhor", "abhorrent", "despise", "sickening", "sick", "vile", "repugnant",
        "🤢", "🤮", "😒", "🙄", "🤦", "ugly", "ugliness", "cringe", "cringey"
    ]
}

# 情感增强词
INTENSIFIERS = {
    "非常": 1.5, "很": 1.3, "特别": 1.5, "超级": 1.8, "极其": 1.8,
    "相当": 1.4, "十分": 1.4, "格外": 1.5, "格外": 1.5, "分外": 1.5,
    "格外": 1.5, "实在": 1.3, "真": 1.2, "真的": 1.3,
    "so": 1.3, "very": 1.5, "really": 1.4, "extremely": 1.8,
    "absolutely": 1.8, "incredibly": 1.7, "totally": 1.5, "completely": 1.6,
    "quite": 1.3, "pretty": 1.2, "super": 1.7, "amazingly": 1.6
}

# 否定词
NEGATORS = {
    "不", "没", "无", "非", "别", "莫", "未", "勿",
    "not", "no", "never", "neither", "nobody", "nothing", "nowhere",
    "don't", "doesn't", "didn't", "won't", "wouldn't", "couldn't",
    "shouldn't", "can't", "cannot", "isn't", "aren't", "wasn't", "weren't"
}

# 否定词组（直接映射为负面情感）
NEGATED_PHRASES = {
    # 快乐的否定 → 悲伤/负面
    "不高兴": Emotion.SADNESS,
    "不开心": Emotion.SADNESS,
    "不快乐": Emotion.SADNESS,
    "不幸福": Emotion.SADNESS,
    "不愉快": Emotion.SADNESS,
    "不满意": Emotion.SADNESS,
    "不满足": Emotion.SADNESS,
    "没意思": Emotion.SADNESS,
    "没劲": Emotion.SADNESS,
    "不好": Emotion.SADNESS,
    "not happy": Emotion.SADNESS,
    "not good": Emotion.SADNESS,
    "not happy": Emotion.SADNESS,
    "not great": Emotion.SADNESS,
    
    # 愤怒的否定 → 中性/平静
    "不生气": Emotion.NEUTRAL,
    "不愤怒": Emotion.NEUTRAL,
    "不恼火": Emotion.NEUTRAL,
    "not angry": Emotion.NEUTRAL,
    
    # 悲伤的否定 → 平静/中性
    "不难过": Emotion.NEUTRAL,
    "不伤心": Emotion.NEUTRAL,
    "不悲伤": Emotion.NEUTRAL,
    "not sad": Emotion.NEUTRAL,
}


class EmotionDetector:
    """
    情感检测器
    
    基于情感词典的文本情感分析工具，支持中英文。
    """
    
    def __init__(self, language: str = "auto"):
        """
        初始化情感检测器
        
        Args:
            language: 语言设置，可选 "zh"（中文）、"en"（英文）或 "auto"（自动检测）
        """
        self.language = language
        self._build_emotion_dict()
    
    def _build_emotion_dict(self):
        """构建情感词典映射"""
        self.emotion_words = {}
        
        # 合并中英文词典
        for emotion, words in CHINESE_EMOTION_WORDS.items():
            for word in words:
                self.emotion_words[word] = emotion
        
        for emotion, words in ENGLISH_EMOTION_WORDS.items():
            for word in words:
                self.emotion_words[word.lower()] = emotion
    
    def _detect_language(self, text: str) -> str:
        """
        检测文本语言
        
        Args:
            text: 待检测文本
            
        Returns:
            语言代码 "zh" 或 "en"
        """
        # 统计中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(re.sub(r'\s', '', text))
        
        if total_chars == 0:
            return "en"
        
        chinese_ratio = chinese_chars / total_chars
        return "zh" if chinese_ratio > 0.3 else "en"
    
    def _tokenize(self, text: str, language: str) -> List[str]:
        """
        分词
        
        Args:
            text: 待分词文本
            language: 语言代码
            
        Returns:
            词列表
        """
        # 简单分词：按空格和标点分割
        tokens = re.findall(r'[\w]+|[\u4e00-\u9fff]|[^\w\s]', text.lower())
        
        # 对于中文，还需要考虑词组
        if language == "zh":
            # 提取所有可能的中文词组（2-4字）
            chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)
            for phrase in chinese_text:
                for length in range(2, min(5, len(phrase) + 1)):
                    for i in range(len(phrase) - length + 1):
                        tokens.append(phrase[i:i + length])
        
        return tokens
    
    def detect(self, text: str) -> EmotionResult:
        """
        检测文本情感
        
        Args:
            text: 待检测文本
            
        Returns:
            EmotionResult 对象
        """
        if not text or not text.strip():
            return EmotionResult(
                dominant_emotion=Emotion.NEUTRAL,
                emotion_scores={e: 0.0 for e in Emotion},
                sentiment=Sentiment.NEUTRAL,
                confidence=0.0,
                keywords_found=[]
            )
        
        # 检测语言
        language = self.language
        if language == "auto":
            language = self._detect_language(text)
        
        # 首先检查否定词组
        text_lower = text.lower()
        for phrase, emotion in NEGATED_PHRASES.items():
            if phrase in text_lower or phrase in text:
                # 找到否定词组，直接返回对应情感
                emotion_scores: Dict[Emotion, float] = {e: 0.0 for e in Emotion}
                emotion_scores[emotion] = 1.0
                
                # 确定情感极性
                if emotion == Emotion.JOY:
                    sentiment = Sentiment.POSITIVE
                elif emotion in [Emotion.SADNESS, Emotion.ANGER, Emotion.FEAR, Emotion.DISGUST]:
                    sentiment = Sentiment.NEGATIVE
                else:
                    sentiment = Sentiment.NEUTRAL
                
                return EmotionResult(
                    dominant_emotion=emotion,
                    emotion_scores=emotion_scores,
                    sentiment=sentiment,
                    confidence=0.8,
                    keywords_found=[phrase]
                )
        
        # 分词
        tokens = self._tokenize(text, language)
        
        # 计算情感分数
        emotion_scores = {e: 0.0 for e in Emotion}
        keywords_found: List[str] = []
        intensifier = 1.0
        negated = False
        
        for i, token in enumerate(tokens):
            # 检查否定词
            if token in NEGATORS:
                negated = True
                continue
            
            # 检查增强词
            if token in INTENSIFIERS:
                intensifier = INTENSIFIERS[token]
                continue
            
            # 检查情感词
            if token in self.emotion_words:
                emotion = self.emotion_words[token]
                score = 1.0 * intensifier
                
                if negated:
                    # 否定词反转情感
                    if emotion in [Emotion.JOY, Emotion.SURPRISE]:
                        emotion = Emotion.SADNESS
                    elif emotion in [Emotion.SADNESS, Emotion.ANGER, Emotion.FEAR, Emotion.DISGUST]:
                        emotion = Emotion.NEUTRAL
                    score *= 0.5  # 降低置信度
                
                emotion_scores[emotion] += score
                keywords_found.append(token)
                
                # 重置状态
                intensifier = 1.0
                negated = False
        
        # 添加中性分数（如果没有检测到任何情感）
        total_score = sum(emotion_scores.values())
        if total_score == 0:
            emotion_scores[Emotion.NEUTRAL] = 1.0
        
        # 归一化分数
        if total_score > 0:
            for emotion in emotion_scores:
                if emotion != Emotion.NEUTRAL:
                    emotion_scores[emotion] = emotion_scores[emotion] / total_score
        
        # 找出主导情感
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        # 计算置信度
        if dominant_emotion == Emotion.NEUTRAL:
            confidence = 0.5
        else:
            sorted_scores = sorted(emotion_scores.values(), reverse=True)
            confidence = sorted_scores[0] if len(sorted_scores) > 0 else 0.5
            if len(sorted_scores) > 1 and sorted_scores[0] > 0:
                confidence = sorted_scores[0] / (sorted_scores[0] + sorted_scores[1])
        
        # 确定情感极性
        if dominant_emotion == Emotion.JOY:
            sentiment = Sentiment.POSITIVE
        elif dominant_emotion in [Emotion.SADNESS, Emotion.ANGER, Emotion.FEAR, Emotion.DISGUST]:
            sentiment = Sentiment.NEGATIVE
        elif dominant_emotion == Emotion.SURPRISE:
            # 惊讶的情感极性取决于上下文，这里简化为中性
            sentiment = Sentiment.NEUTRAL
        else:
            sentiment = Sentiment.NEUTRAL
        
        return EmotionResult(
            dominant_emotion=dominant_emotion,
            emotion_scores=emotion_scores,
            sentiment=sentiment,
            confidence=round(confidence, 3),
            keywords_found=list(set(keywords_found))
        )
    
    def batch_detect(self, texts: List[str]) -> List[EmotionResult]:
        """
        批量检测文本情感
        
        Args:
            texts: 文本列表
            
        Returns:
            EmotionResult 列表
        """
        return [self.detect(text) for text in texts]
    
    def get_emotion_distribution(self, text: str) -> Dict[str, float]:
        """
        获取情感分布
        
        Args:
            text: 待检测文本
            
        Returns:
            情感分数字典
        """
        result = self.detect(text)
        return result.to_dict()["emotion_scores"]
    
    def is_positive(self, text: str, threshold: float = 0.5) -> bool:
        """
        判断文本是否为正面情感
        
        Args:
            text: 待检测文本
            threshold: 判断阈值
            
        Returns:
            是否为正面情感
        """
        result = self.detect(text)
        return result.sentiment == Sentiment.POSITIVE and result.confidence >= threshold
    
    def is_negative(self, text: str, threshold: float = 0.5) -> bool:
        """
        判断文本是否为负面情感
        
        Args:
            text: 待检测文本
            threshold: 判断阈值
            
        Returns:
            是否为负面情感
        """
        result = self.detect(text)
        return result.sentiment == Sentiment.NEGATIVE and result.confidence >= threshold
    
    def get_sentiment_score(self, text: str) -> float:
        """
        获取情感分数（-1 到 1）
        
        Args:
            text: 待检测文本
            
        Returns:
            情感分数，正值表示正面情感，负值表示负面情感
        """
        result = self.detect(text)
        positive_score = result.emotion_scores.get(Emotion.JOY, 0.0)
        negative_score = sum([
            result.emotion_scores.get(Emotion.SADNESS, 0.0),
            result.emotion_scores.get(Emotion.ANGER, 0.0),
            result.emotion_scores.get(Emotion.FEAR, 0.0),
            result.emotion_scores.get(Emotion.DISGUST, 0.0)
        ])
        
        score = positive_score - negative_score
        return round(score, 3)


# 便捷函数
def detect_emotion(text: str, language: str = "auto") -> EmotionResult:
    """
    检测文本情感的便捷函数
    
    Args:
        text: 待检测文本
        language: 语言设置
        
    Returns:
        EmotionResult 对象
    """
    detector = EmotionDetector(language)
    return detector.detect(text)


def get_sentiment(text: str) -> str:
    """
    获取情感极性的便捷函数
    
    Args:
        text: 待检测文本
        
    Returns:
        情感极性字符串
    """
    result = detect_emotion(text)
    return result.sentiment.value


def is_positive(text: str) -> bool:
    """判断文本是否为正面情感"""
    detector = EmotionDetector()
    return detector.is_positive(text)


def is_negative(text: str) -> bool:
    """判断文本是否为负面情感"""
    detector = EmotionDetector()
    return detector.is_negative(text)


# 导出
__all__ = [
    'Emotion',
    'Sentiment', 
    'EmotionResult',
    'EmotionDetector',
    'detect_emotion',
    'get_sentiment',
    'is_positive',
    'is_negative'
]