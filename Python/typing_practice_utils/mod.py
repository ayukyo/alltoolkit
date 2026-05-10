"""
Typing Practice Utils - 打字练习工具
提供打字练习文本生成、速度计算、准确率分析等功能
零外部依赖，纯 Python 标准库实现
"""

import random
import time
import string
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    """难度等级"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class TextType(Enum):
    """文本类型"""
    WORDS = "words"           # 单词
    SENTENCES = "sentences"   # 句子
    PARAGRAPHS = "paragraphs" # 段落
    CODE = "code"             # 代码
    NUMBERS = "numbers"       # 数字
    MIXED = "mixed"           # 混合


@dataclass
class TypingResult:
    """打字结果"""
    original_text: str
    typed_text: str
    time_seconds: float
    correct_chars: int
    total_chars: int
    errors: List[Tuple[int, str, str]]  # (position, expected, actual)
    wpm: float  # 每分钟单词数
    cpm: float  # 每分钟字符数
    accuracy: float  # 准确率百分比
    
    def __str__(self) -> str:
        return (
            f"TypingResult(\n"
            f"  时间: {self.time_seconds:.1f}秒\n"
            f"  WPM: {self.wpm:.1f}\n"
            f"  CPM: {self.cpm:.1f}\n"
            f"  准确率: {self.accuracy:.1f}%\n"
            f"  正确字符: {self.correct_chars}/{self.total_chars}\n"
            f"  错误数: {len(self.errors)}\n"
            f")"
        )


class TextGenerator:
    """文本生成器"""
    
    # 常用英文单词库
    EASY_WORDS = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me"
    ]
    
    MEDIUM_WORDS = [
        "computer", "keyboard", "monitor", "software", "hardware", "program",
        "developer", "algorithm", "database", "network", "security", "server",
        "client", "protocol", "interface", "variable", "function", "method",
        "object", "instance", "module", "package", "library", "framework",
        "debugging", "testing", "deployment", "production", "development", "version"
    ]
    
    HARD_WORDS = [
        "synchronization", "asynchronous", "polymorphism", "encapsulation",
        "inheritance", "abstraction", "implementation", "instantiation",
        "serialization", "deserialization", "multithreading", "concurrency",
        "parallelism", "optimization", "refactoring", "architectural",
        "microservices", "containerization", "orchestration", "kubernetes"
    ]
    
    # 常用句子
    SENTENCES = [
        "The quick brown fox jumps over the lazy dog.",
        "A journey of a thousand miles begins with a single step.",
        "To be or not to be, that is the question.",
        "All that glitters is not gold.",
        "Actions speak louder than words.",
        "Practice makes perfect.",
        "Time flies when you're having fun.",
        "Knowledge is power.",
        "The early bird catches the worm.",
        "Where there's a will, there's a way.",
        "Success is not final, failure is not fatal.",
        "Life is what happens when you're busy making other plans.",
        "The only thing we have to fear is fear itself.",
        "In the middle of difficulty lies opportunity.",
        "Be the change you wish to see in the world."
    ]
    
    # 代码片段
    CODE_SNIPPETS = [
        "def hello_world():",
        "    print('Hello, World!')",
        "for i in range(10):",
        "    print(i)",
        "if __name__ == '__main__':",
        "    main()",
        "class Solution:",
        "    def solve(self, n):",
        "        return n * 2",
        "import os",
        "from typing import List",
        "async def fetch_data():",
        "    await session.get(url)",
        "with open('file.txt', 'r') as f:",
        "    data = f.read()",
        "result = [x * 2 for x in range(10)]",
        "lambda x: x ** 2",
        "try:\n    do_something()\nexcept Exception as e:\n    pass"
    ]
    
    @classmethod
    def generate_words(cls, count: int = 20, difficulty: Difficulty = Difficulty.EASY) -> str:
        """生成单词练习文本"""
        if difficulty == Difficulty.EASY:
            words = cls.EASY_WORDS
        elif difficulty == Difficulty.MEDIUM:
            words = cls.MEDIUM_WORDS
        elif difficulty == Difficulty.HARD:
            words = cls.HARD_WORDS
        else:  # EXPERT
            words = cls.EASY_WORDS + cls.MEDIUM_WORDS + cls.HARD_WORDS
        
        selected = random.choices(words, k=count)
        return " ".join(selected)
    
    @classmethod
    def generate_sentence(cls, difficulty: Difficulty = Difficulty.EASY) -> str:
        """生成句子练习文本"""
        sentence = random.choice(cls.SENTENCES)
        if difficulty == Difficulty.EASY:
            # 简单难度只保留前半句
            if len(sentence) > 30:
                parts = sentence.split(", ")
                if len(parts) > 1:
                    return parts[0] + "."
        return sentence
    
    @classmethod
    def generate_paragraph(cls, sentences: int = 3) -> str:
        """生成段落练习文本"""
        selected = random.sample(cls.SENTENCES, min(sentences, len(cls.SENTENCES)))
        return " ".join(selected)
    
    @classmethod
    def generate_code(cls, lines: int = 5) -> str:
        """生成代码练习文本"""
        selected = random.sample(cls.CODE_SNIPPETS, min(lines, len(cls.CODE_SNIPPETS)))
        return "\n".join(selected)
    
    @classmethod
    def generate_numbers(cls, count: int = 10) -> str:
        """生成数字练习文本"""
        numbers = []
        for _ in range(count):
            # 随机生成不同类型的数字
            choice = random.randint(1, 4)
            if choice == 1:
                numbers.append(str(random.randint(0, 9)) * random.randint(3, 6))
            elif choice == 2:
                numbers.append(str(random.randint(100, 9999)))
            elif choice == 3:
                numbers.append(f"{random.uniform(0, 100):.2f}")
            else:
                numbers.append(f"{random.randint(100000, 999999):,}")
        return " ".join(numbers)
    
    @classmethod
    def generate_mixed(cls, length: int = 50) -> str:
        """生成混合练习文本"""
        parts = []
        current_length = 0
        
        while current_length < length:
            choice = random.randint(1, 4)
            if choice == 1:
                part = random.choice(cls.EASY_WORDS)
            elif choice == 2:
                part = str(random.randint(10, 99))
            elif choice == 3:
                part = random.choice(string.punctuation)
            else:
                part = random.choice(cls.MEDIUM_WORDS)
            
            parts.append(part)
            current_length += len(part) + 1
        
        return " ".join(parts)[:length]
    
    @classmethod
    def generate(cls, text_type: TextType = TextType.WORDS, 
                 difficulty: Difficulty = Difficulty.EASY,
                 **kwargs) -> str:
        """
        生成练习文本
        
        Args:
            text_type: 文本类型
            difficulty: 难度等级
            **kwargs: 额外参数
                - count: 单词数量 (默认 20)
                - sentences: 句子数量 (默认 3)
                - lines: 代码行数 (默认 5)
        
        Returns:
            生成的文本
        """
        if text_type == TextType.WORDS:
            return cls.generate_words(kwargs.get('count', 20), difficulty)
        elif text_type == TextType.SENTENCES:
            return cls.generate_sentence(difficulty)
        elif text_type == TextType.PARAGRAPHS:
            return cls.generate_paragraph(kwargs.get('sentences', 3))
        elif text_type == TextType.CODE:
            return cls.generate_code(kwargs.get('lines', 5))
        elif text_type == TextType.NUMBERS:
            return cls.generate_numbers(kwargs.get('count', 10))
        elif text_type == TextType.MIXED:
            return cls.generate_mixed(kwargs.get('length', 50))
        else:
            return cls.generate_words()


class TypingAnalyzer:
    """打字分析器"""
    
    @staticmethod
    def calculate_wpm(text: str, time_seconds: float) -> float:
        """
        计算每分钟单词数 (WPM)
        标准定义: 5个字符 = 1个单词
        
        Args:
            text: 输入的文本
            time_seconds: 用时（秒）
        
        Returns:
            WPM 值
        """
        if time_seconds <= 0:
            return 0.0
        
        # 标准化：5个字符 = 1个单词
        words = len(text) / 5
        minutes = time_seconds / 60
        
        return round(words / minutes, 2)
    
    @staticmethod
    def calculate_cpm(text: str, time_seconds: float) -> float:
        """
        计算每分钟字符数 (CPM)
        
        Args:
            text: 输入的文本
            time_seconds: 用时（秒）
        
        Returns:
            CPM 值
        """
        if time_seconds <= 0:
            return 0.0
        
        chars = len(text)
        minutes = time_seconds / 60
        
        return round(chars / minutes, 2)
    
    @staticmethod
    def calculate_accuracy(original: str, typed: str) -> Tuple[float, int, int, List[Tuple[int, str, str]]]:
        """
        计算准确率
        
        Args:
            original: 原始文本
            typed: 输入的文本
        
        Returns:
            (准确率百分比, 正确字符数, 总字符数, 错误列表)
        """
        max_len = max(len(original), len(typed))
        min_len = min(len(original), len(typed))
        
        errors = []
        correct = 0
        
        # 比较每个字符
        for i in range(max_len):
            if i >= len(original):
                # 多输入的字符
                errors.append((i, "", typed[i]))
            elif i >= len(typed):
                # 漏输的字符
                errors.append((i, original[i], ""))
            elif original[i] == typed[i]:
                correct += 1
            else:
                errors.append((i, original[i], typed[i]))
        
        total = max(len(original), len(typed))
        accuracy = (correct / total * 100) if total > 0 else 100.0
        
        return round(accuracy, 2), correct, total, errors
    
    @staticmethod
    def analyze(original: str, typed: str, time_seconds: float) -> TypingResult:
        """
        完整分析打字结果
        
        Args:
            original: 原始文本
            typed: 输入的文本
            time_seconds: 用时（秒）
        
        Returns:
            TypingResult 对象
        """
        accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
        
        return TypingResult(
            original_text=original,
            typed_text=typed,
            time_seconds=time_seconds,
            correct_chars=correct,
            total_chars=total,
            errors=errors,
            wpm=TypingAnalyzer.calculate_wpm(typed, time_seconds),
            cpm=TypingAnalyzer.calculate_cpm(typed, time_seconds),
            accuracy=accuracy
        )


class TypingPractice:
    """打字练习主类"""
    
    def __init__(self):
        self.generator = TextGenerator()
        self.analyzer = TypingAnalyzer()
        self.history: List[TypingResult] = []
        self._start_time: Optional[float] = None
        self._current_text: Optional[str] = None
    
    def start_session(self, text_type: TextType = TextType.WORDS,
                      difficulty: Difficulty = Difficulty.EASY,
                      **kwargs) -> str:
        """
        开始新的练习会话
        
        Args:
            text_type: 文本类型
            difficulty: 难度等级
            **kwargs: 传递给生成器的额外参数
        
        Returns:
            要练习的文本
        """
        self._current_text = self.generator.generate(text_type, difficulty, **kwargs)
        self._start_time = None
        return self._current_text
    
    def begin_typing(self) -> None:
        """开始计时（用户开始输入时调用）"""
        self._start_time = time.time()
    
    def finish_typing(self, typed_text: str) -> TypingResult:
        """
        结束输入并分析结果
        
        Args:
            typed_text: 用户输入的文本
        
        Returns:
            TypingResult 分析结果
        """
        if self._start_time is None:
            raise ValueError("尚未开始计时，请先调用 begin_typing()")
        
        end_time = time.time()
        elapsed = end_time - self._start_time
        
        result = self.analyzer.analyze(self._current_text, typed_text, elapsed)
        self.history.append(result)
        
        # 重置状态
        self._start_time = None
        self._current_text = None
        
        return result
    
    def get_statistics(self) -> Dict:
        """
        获取历史统计数据
        
        Returns:
            统计数据字典
        """
        if not self.history:
            return {
                "total_sessions": 0,
                "average_wpm": 0,
                "average_accuracy": 0,
                "best_wpm": 0,
                "best_accuracy": 0
            }
        
        wpms = [r.wpm for r in self.history]
        accuracies = [r.accuracy for r in self.history]
        
        return {
            "total_sessions": len(self.history),
            "average_wpm": round(sum(wpms) / len(wpms), 2),
            "average_accuracy": round(sum(accuracies) / len(accuracies), 2),
            "best_wpm": max(wpms),
            "best_accuracy": max(accuracies),
            "total_time_seconds": sum(r.time_seconds for r in self.history)
        }
    
    def clear_history(self) -> None:
        """清除历史记录"""
        self.history.clear()
    
    @staticmethod
    def get_performance_level(wpm: float) -> str:
        """
        根据 WPM 获取性能等级
        
        Args:
            wpm: 每分钟单词数
        
        Returns:
            等级描述
        """
        if wpm < 20:
            return "初级 (Beginner)"
        elif wpm < 30:
            return "入门 (Elementary)"
        elif wpm < 40:
            return "中级 (Intermediate)"
        elif wpm < 50:
            return "熟练 (Proficient)"
        elif wpm < 60:
            return "精通 (Advanced)"
        elif wpm < 80:
            return "专家 (Expert)"
        else:
            return "大师 (Master)"


# 便捷函数
def generate_practice_text(text_type: TextType = TextType.WORDS,
                          difficulty: Difficulty = Difficulty.EASY,
                          **kwargs) -> str:
    """生成练习文本的便捷函数"""
    return TextGenerator.generate(text_type, difficulty, **kwargs)


def analyze_typing(original: str, typed: str, time_seconds: float) -> TypingResult:
    """分析打字结果的便捷函数"""
    return TypingAnalyzer.analyze(original, typed, time_seconds)


def quick_practice(difficulty: Difficulty = Difficulty.EASY,
                   word_count: int = 20) -> Tuple[str, Callable[[str], TypingResult]]:
    """
    快速练习的便捷函数
    
    Args:
        difficulty: 难度等级
        word_count: 单词数量
    
    Returns:
        (练习文本, 完成函数)
        完成函数接受用户输入的文本，返回 TypingResult
    """
    practice = TypingPractice()
    text = practice.start_session(TextType.WORDS, difficulty, count=word_count)
    
    def finish(typed_text: str) -> TypingResult:
        practice.begin_typing()
        # 模拟即时开始（实际使用中用户会花时间输入）
        # 这里我们返回一个等待输入的闭包
        start = time.time()
        result = practice.finish_typing(typed_text)
        return result
    
    return text, finish


if __name__ == "__main__":
    # 简单演示
    print("=" * 50)
    print("打字练习工具演示")
    print("=" * 50)
    
    # 生成不同类型的练习文本
    print("\n【单词练习 - 简单】")
    print(TextGenerator.generate_words(10, Difficulty.EASY))
    
    print("\n【单词练习 - 困难】")
    print(TextGenerator.generate_words(10, Difficulty.HARD))
    
    print("\n【句子练习】")
    print(TextGenerator.generate_sentence())
    
    print("\n【段落练习】")
    print(TextGenerator.generate_paragraph(2))
    
    print("\n【代码练习】")
    print(TextGenerator.generate_code(3))
    
    print("\n【数字练习】")
    print(TextGenerator.generate_numbers(5))
    
    print("\n【混合练习】")
    print(TextGenerator.generate_mixed(40))
    
    # 分析演示
    print("\n" + "=" * 50)
    print("分析演示")
    print("=" * 50)
    
    original = "The quick brown fox"
    typed = "The quikc brown fox"
    time_sec = 5.0
    
    result = TypingAnalyzer.analyze(original, typed, time_sec)
    print(f"\n原文: {original}")
    print(f"输入: {typed}")
    print(f"\n{result}")
    print(f"\n性能等级: {TypingPractice.get_performance_level(result.wpm)}")