"""
密码强度工具集 (Password Strength Utils)
提供密码强度分析、安全检测、破解时间估算、强密码生成等功能
零外部依赖，纯 Python 标准库实现

功能列表:
1. PasswordStrength - 密码强度分析器
2. PasswordCrackEstimator - 破解时间估算器
3. PasswordGenerator - 安全密码生成器
4. PasswordValidator - 密码验证器
5. PasswordEntropy - 密码熵计算器
6. CommonPasswordChecker - 常见密码检测
"""

import string
import math
import random
import hashlib
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum


class StrengthLevel(Enum):
    """密码强度级别"""
    VERY_WEAK = 1    # 非常弱
    WEAK = 2         # 弱
    MEDIUM = 3       # 中等
    STRONG = 4       # 强
    VERY_STRONG = 5  # 非常强


class PasswordIssue(Enum):
    """密码问题类型"""
    TOO_SHORT = "密码太短"
    TOO_LONG = "密码过长"
    NO_LOWERCASE = "缺少小写字母"
    NO_UPPERCASE = "缺少大写字母"
    NO_DIGITS = "缺少数字"
    NO_SPECIAL = "缺少特殊字符"
    COMMON_PASSWORD = "常见弱密码"
    SEQUENTIAL_CHARS = "包含连续字符"
    REPEATED_CHARS = "包含重复字符"
    KEYBOARD_PATTERN = "包含键盘模式"
    DATE_PATTERN = "包含日期模式"
    DICTIONARY_WORD = "包含字典单词"
    REVERSED_WORD = "包含反向单词"


@dataclass
class StrengthResult:
    """密码强度分析结果"""
    password: str
    score: int  # 0-100
    level: StrengthLevel
    entropy: float  # 信息熵（位）
    crack_time: str  # 预估破解时间
    issues: List[PasswordIssue] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    @property
    def is_strong(self) -> bool:
        """是否为强密码"""
        return self.level.value >= StrengthLevel.STRONG.value
    
    @property
    def is_acceptable(self) -> bool:
        """是否可接受"""
        return self.level.value >= StrengthLevel.MEDIUM.value
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "password": self.password,
            "score": self.score,
            "level": self.level.name,
            "entropy": round(self.entropy, 2),
            "crack_time": self.crack_time,
            "issues": [issue.value for issue in self.issues],
            "suggestions": self.suggestions,
            "is_strong": self.is_strong,
            "is_acceptable": self.is_acceptable
        }


class PasswordEntropy:
    """
    密码熵计算器
    计算密码的信息熵，衡量密码的随机性和不可预测性
    """
    
    # 字符集大小
    CHARSET_SIZES = {
        'lowercase': 26,
        'uppercase': 26,
        'digits': 10,
        'special': 32,  # 常见特殊字符
        'extended': 128,  # ASCII扩展字符
    }
    
    @classmethod
    def calculate(cls, password: str) -> float:
        """
        计算密码的信息熵（位）
        
        Args:
            password: 密码字符串
        
        Returns:
            信息熵（位）
        """
        if not password:
            return 0.0
        
        # 计算使用的字符集大小
        charset_size = cls._get_charset_size(password)
        
        # 熵 = 长度 * log2(字符集大小)
        entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
        
        return entropy
    
    @classmethod
    def _get_charset_size(cls, password: str) -> int:
        """获取密码使用的字符集大小"""
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        has_extended = any(ord(c) > 127 for c in password)
        
        charset_size = 0
        if has_lower:
            charset_size += cls.CHARSET_SIZES['lowercase']
        if has_upper:
            charset_size += cls.CHARSET_SIZES['uppercase']
        if has_digit:
            charset_size += cls.CHARSET_SIZES['digits']
        if has_special:
            charset_size += cls.CHARSET_SIZES['special']
        if has_extended:
            charset_size += cls.CHARSET_SIZES['extended']
        
        # 如果都没有，至少是基本字符
        return charset_size if charset_size > 0 else 26


class PasswordCrackEstimator:
    """
    密码破解时间估算器
    基于不同攻击场景估算破解时间
    """
    
    # 不同攻击方式的尝试速度（次/秒）
    ONLINE_ATTACK = 1_000  # 在线攻击，较慢
    OFFLINE_FAST = 10_000_000  # 离线快速哈希
    OFFLINE_SLOW = 100_000  # 离线慢速哈希（bcrypt等）
    GPU_ATTACK = 100_000_000_000  # GPU 暴力破解
    
    @classmethod
    def estimate_time(cls, password: str, attempts_per_second: int = OFFLINE_FAST) -> str:
        """
        估算破解时间
        
        Args:
            password: 密码
            attempts_per_second: 每秒尝试次数
        
        Returns:
            人类可读的破解时间字符串
        """
        if not password:
            return "瞬间"
        
        entropy = PasswordEntropy.calculate(password)
        
        # 可能的组合数 = 2^熵
        combinations = 2 ** entropy
        
        # 平均需要尝试一半的组合
        average_attempts = combinations / 2
        
        # 估算秒数
        seconds = average_attempts / attempts_per_second
        
        return cls._format_time(seconds)
    
    @classmethod
    def estimate_all_scenarios(cls, password: str) -> Dict[str, str]:
        """
        估算所有攻击场景的破解时间
        
        Args:
            password: 密码
        
        Returns:
            场景 -> 时间的映射
        """
        return {
            "在线攻击": cls.estimate_time(password, cls.ONLINE_ATTACK),
            "离线快速哈希": cls.estimate_time(password, cls.OFFLINE_FAST),
            "离线慢速哈希": cls.estimate_time(password, cls.OFFLINE_SLOW),
            "GPU暴力破解": cls.estimate_time(password, cls.GPU_ATTACK)
        }
    
    @classmethod
    def _format_time(cls, seconds: float) -> str:
        """格式化时间"""
        if seconds < 0.001:
            return "瞬间"
        elif seconds < 1:
            return f"{seconds * 1000:.1f} 毫秒"
        elif seconds < 60:
            return f"{seconds:.1f} 秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} 分钟"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f} 小时"
        elif seconds < 2592000:  # 30天
            days = seconds / 86400
            return f"{days:.1f} 天"
        elif seconds < 31536000:  # 365天
            months = seconds / 2592000
            return f"{months:.1f} 个月"
        elif seconds < 31536000 * 1000:
            years = seconds / 31536000
            return f"{years:.1f} 年"
        elif seconds < 31536000 * 1000000:
            millennia = seconds / (31536000 * 1000)
            return f"{millennia:.1f} 千年"
        elif seconds < 31536000 * 1000000000:
            million_years = seconds / (31536000 * 1000000)
            return f"{million_years:.1f} 百万年"
        elif seconds < 31536000 * 1000000000000:
            billion_years = seconds / (31536000 * 1000000000)
            return f"{billion_years:.1f} 十亿年"
        else:
            return "宇宙年龄级别的无数倍"


class CommonPasswordChecker:
    """
    常见密码检测器
    检测密码是否在常见密码列表中
    """
    
    # 常见弱密码列表（前100个最常见的）
    COMMON_PASSWORDS = {
        # 数字组合
        "123456", "123456789", "12345678", "12345", "1234567", "1234567890",
        "123123", "1234", "12345678910", "123",
        # 键盘模式
        "qwerty", "qwerty123", "qazwsx", "qweasd", "asdfgh", "zxcvbn",
        "qwertyuiop", "asdfghjkl", "zxcvbnm",
        # 常见单词
        "password", "password1", "password123", "passwd", "pass",
        "admin", "admin123", "administrator", "root", "user",
        "login", "welcome", "hello", "sunshine", "princess",
        # 个人信息相关
        "iloveyou", "letmein", "master", "love", "baby",
        # 简单组合
        "abc123", "abc12345", "abcd1234", "a123456", "a1b2c3",
        # 日期相关
        "000000", "111111", "222222", "333333", "444444", "555555",
        "666666", "777777", "888888", "999999",
        # 名字
        "michael", "jennifer", "jordan", "harley", "robert",
        "daniel", "andrew", "joshua", "matthew", "jessica",
        # 运动队
        "baseball", "football", "soccer", "hockey", "basketball",
        # 其他
        "dragon", "monkey", "shadow", "superman", "batman",
        "trustno1", "starwars", "killer", "pepper", "charlie",
        "donald", "password!", "whatever", "freedom", "money",
        "buster", "ginger", "jordan23", "cowboys", "dallas"
    }
    
    @classmethod
    def is_common(cls, password: str) -> bool:
        """
        检查密码是否为常见密码
        
        Args:
            password: 密码
        
        Returns:
            是否为常见密码
        """
        return password.lower() in cls.COMMON_PASSWORDS
    
    @classmethod
    def check_variants(cls, password: str) -> List[str]:
        """
        检查密码的常见变体
        
        Args:
            password: 密码
        
        Returns:
            匹配的变体类型列表
        """
        variants = []
        lower = password.lower()
        
        # 数字后缀变体
        base = ''.join(c for c in lower if not c.isdigit())
        if base and base in cls.COMMON_PASSWORDS:
            variants.append("数字后缀变体")
        
        # 大小写变体
        if lower in cls.COMMON_PASSWORDS:
            variants.append("大小写变体")
        
        # 反转变体
        if password[::-1].lower() in cls.COMMON_PASSWORDS:
            variants.append("反转变体")
        
        return variants


class PatternDetector:
    """
    密码模式检测器
    检测密码中的常见模式
    """
    
    # 键盘行模式
    KEYBOARD_ROWS = [
        "qwertyuiop", "asdfghjkl", "zxcvbnm",
        "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM",
        "1234567890", "0987654321"
    ]
    
    # 键盘斜线模式
    KEYBOARD_DIAGONALS = [
        "1qaz", "2wsx", "3edc", "4rfv", "5tgb", "6yhn", "7ujm", "8ik,", "9ol.", "0p;/",
        "qweasd", "asdfzxcv", "zxcvqwer"
    ]
    
    # 常见字典单词（简化版）
    COMMON_WORDS = {
        "password", "admin", "login", "welcome", "hello", "master",
        "dragon", "monkey", "shadow", "sunshine", "princess",
        "football", "baseball", "soccer", "hockey", "basketball",
        "superman", "batman", "starwars", "trustno1", "iloveyou",
        "love", "baby", "angel", "flower", "heart", "sweet",
        "computer", "internet", "secret", "summer", "winter"
    }
    
    @classmethod
    def detect_sequential(cls, password: str, min_length: int = 3) -> List[str]:
        """
        检测连续字符模式
        
        Args:
            password: 密码
            min_length: 最小序列长度
        
        Returns:
            检测到的连续序列列表
        """
        sequences = []
        lower = password.lower()
        
        # 检测字母序列
        for i in range(len(lower) - min_length + 1):
            segment = lower[i:i + min_length]
            if cls._is_alphabetical(segment):
                # 扩展序列
                j = i + min_length
                while j < len(lower) and cls._is_alphabetical(lower[i:j + 1]):
                    j += 1
                sequences.append(lower[i:j])
        
        # 检测数字序列
        for i in range(len(password) - min_length + 1):
            segment = password[i:i + min_length]
            if segment.isdigit() and cls._is_numerical(segment):
                j = i + min_length
                while j < len(password) and password[i:j + 1].isdigit() and cls._is_numerical(password[i:j + 1]):
                    j += 1
                sequences.append(password[i:j])
        
        return sequences
    
    @classmethod
    def _is_alphabetical(cls, s: str) -> bool:
        """检查是否为字母顺序序列"""
        if len(s) < 2 or not s.isalpha():
            return False
        for i in range(len(s) - 1):
            if ord(s[i + 1].lower()) - ord(s[i].lower()) != 1:
                return False
        return True
    
    @classmethod
    def _is_numerical(cls, s: str) -> bool:
        """检查是否为数字顺序序列"""
        if len(s) < 2 or not s.isdigit():
            return False
        for i in range(len(s) - 1):
            if int(s[i + 1]) - int(s[i]) != 1:
                return False
        return True
    
    @classmethod
    def detect_repeated(cls, password: str, min_length: int = 2) -> List[str]:
        """
        检测重复字符模式
        
        Args:
            password: 密码
            min_length: 最小重复长度
        
        Returns:
            检测到的重复模式列表
        """
        repeated = []
        i = 0
        
        while i < len(password):
            char = password[i]
            count = 1
            while i + count < len(password) and password[i + count] == char:
                count += 1
            if count >= min_length:
                repeated.append(char * count)
            i += count
        
        return repeated
    
    @classmethod
    def detect_keyboard_pattern(cls, password: str) -> List[str]:
        """
        检测键盘模式
        
        Args:
            password: 密码
        
        Returns:
            检测到的键盘模式列表
        """
        patterns = []
        lower = password.lower()
        
        # 检查键盘行
        for row in cls.KEYBOARD_ROWS:
            for i in range(len(row) - 2):
                segment = row[i:i + 3].lower()
                if segment in lower:
                    # 扩展匹配
                    j = i + 3
                    while j <= len(row) and row[i:j].lower() in lower:
                        j += 1
                    matched = row[i:j - 1].lower()
                    if matched not in patterns:
                        patterns.append(matched)
        
        # 检查斜线模式
        for diagonal in cls.KEYBOARD_DIAGONALS:
            if diagonal.lower() in lower:
                patterns.append(diagonal.lower())
        
        return patterns
    
    @classmethod
    def detect_date_pattern(cls, password: str) -> List[str]:
        """
        检测日期模式
        
        Args:
            password: 密码
        
        Returns:
            检测到的日期模式列表
        """
        patterns = []
        
        # 检测 8位日期 (YYYYMMDD, DDMMYYYY, MMDDYYYY)
        if len(password) >= 8:
            for i in range(len(password) - 7):
                segment = password[i:i + 8]
                if segment.isdigit():
                    # YYYYMMDD
                    year = int(segment[0:4])
                    month = int(segment[4:6])
                    day = int(segment[6:8])
                    if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                        patterns.append(segment)
        
        # 检测 6位日期 (YYMMDD, DDMMYY, MMDDYY)
        if len(password) >= 6:
            for i in range(len(password) - 5):
                segment = password[i:i + 6]
                if segment.isdigit():
                    # YYMMDD
                    year = int(segment[0:2])
                    month = int(segment[2:4])
                    day = int(segment[4:6])
                    if 0 <= year <= 99 and 1 <= month <= 12 and 1 <= day <= 31:
                        patterns.append(segment)
        
        return patterns
    
    @classmethod
    def detect_dictionary_word(cls, password: str) -> List[str]:
        """
        检测字典单词
        
        Args:
            password: 密码
        
        Returns:
            检测到的字典单词列表
        """
        found = []
        lower = password.lower()
        
        for word in cls.COMMON_WORDS:
            if word in lower:
                found.append(word)
        
        # 检查反向单词
        for word in cls.COMMON_WORDS:
            reversed_word = word[::-1]
            if reversed_word in lower and reversed_word not in found:
                found.append(f"{reversed_word}(反转)")
        
        return found


class PasswordStrength:
    """
    密码强度分析器
    主类，综合分析密码强度
    """
    
    # 默认配置
    DEFAULT_MIN_LENGTH = 8
    DEFAULT_MAX_LENGTH = 128
    DEFAULT_MIN_SCORE = 60
    
    def __init__(self, 
                 min_length: int = DEFAULT_MIN_LENGTH,
                 max_length: int = DEFAULT_MAX_LENGTH,
                 require_uppercase: bool = True,
                 require_lowercase: bool = True,
                 require_digit: bool = True,
                 require_special: bool = True,
                 min_score: int = DEFAULT_MIN_SCORE):
        """
        初始化密码强度分析器
        
        Args:
            min_length: 最小长度
            max_length: 最大长度
            require_uppercase: 是否要求大写字母
            require_lowercase: 是否要求小写字母
            require_digit: 是否要求数字
            require_special: 是否要求特殊字符
            min_score: 最低分数
        """
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
        self.min_score = min_score
    
    def analyze(self, password: str) -> StrengthResult:
        """
        分析密码强度
        
        Args:
            password: 密码
        
        Returns:
            强度分析结果
        """
        issues = []
        suggestions = []
        score = 0
        
        # 基础分数：长度
        length = len(password)
        if length < self.min_length:
            issues.append(PasswordIssue.TOO_SHORT)
            suggestions.append(f"密码长度至少需要 {self.min_length} 个字符")
        elif length > self.max_length:
            issues.append(PasswordIssue.TOO_LONG)
            suggestions.append(f"密码长度不能超过 {self.max_length} 个字符")
        else:
            # 长度加分
            score += min(length * 4, 40)
        
        # 字符类型检查
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if self.require_lowercase and not has_lower:
            issues.append(PasswordIssue.NO_LOWERCASE)
            suggestions.append("添加小写字母可以增强密码强度")
        else:
            score += 10
        
        if self.require_uppercase and not has_upper:
            issues.append(PasswordIssue.NO_UPPERCASE)
            suggestions.append("添加大写字母可以增强密码强度")
        else:
            score += 10
        
        if self.require_digit and not has_digit:
            issues.append(PasswordIssue.NO_DIGITS)
            suggestions.append("添加数字可以增强密码强度")
        else:
            score += 10
        
        if self.require_special and not has_special:
            issues.append(PasswordIssue.NO_SPECIAL)
            suggestions.append("添加特殊字符可以增强密码强度")
        else:
            score += 15
        
        # 检测模式问题
        # 连续字符
        sequential = PatternDetector.detect_sequential(password)
        if sequential:
            issues.append(PasswordIssue.SEQUENTIAL_CHARS)
            suggestions.append("避免使用连续字符序列")
            score -= len(sequential) * 5
        
        # 重复字符
        repeated = PatternDetector.detect_repeated(password)
        if any(len(r) >= 3 for r in repeated):
            issues.append(PasswordIssue.REPEATED_CHARS)
            suggestions.append("避免重复使用相同字符")
            score -= 10
        
        # 键盘模式
        keyboard_patterns = PatternDetector.detect_keyboard_pattern(password)
        if keyboard_patterns:
            issues.append(PasswordIssue.KEYBOARD_PATTERN)
            suggestions.append("避免使用键盘上的连续按键")
            score -= len(keyboard_patterns) * 10
        
        # 日期模式
        date_patterns = PatternDetector.detect_date_pattern(password)
        if date_patterns:
            issues.append(PasswordIssue.DATE_PATTERN)
            suggestions.append("避免使用日期作为密码")
            score -= 15
        
        # 字典单词
        dict_words = PatternDetector.detect_dictionary_word(password)
        if dict_words:
            issues.append(PasswordIssue.DICTIONARY_WORD)
            suggestions.append("避免使用常见单词")
            score -= len(dict_words) * 10
        
        # 常见密码检查
        if CommonPasswordChecker.is_common(password):
            issues.append(PasswordIssue.COMMON_PASSWORD)
            suggestions.append("这是一个常见密码，极易被破解")
            score -= 30
        
        # 检查变体
        variants = CommonPasswordChecker.check_variants(password)
        if variants and PasswordIssue.COMMON_PASSWORD not in issues:
            score -= 15
            suggestions.append("密码与常见密码相似")
        
        # 计算熵
        entropy = PasswordEntropy.calculate(password)
        
        # 熵加分
        score += min(entropy / 2, 30)
        
        # 确保分数在0-100范围内
        score = max(0, min(100, score))
        
        # 确定强度级别
        if score < 20:
            level = StrengthLevel.VERY_WEAK
        elif score < 40:
            level = StrengthLevel.WEAK
        elif score < 60:
            level = StrengthLevel.MEDIUM
        elif score < 80:
            level = StrengthLevel.STRONG
        else:
            level = StrengthLevel.VERY_STRONG
        
        # 估算破解时间
        crack_time = PasswordCrackEstimator.estimate_time(password)
        
        # 如果没有建议，添加正面反馈
        if not suggestions:
            suggestions.append("这是一个强密码！继续保持")
        
        return StrengthResult(
            password="*" * len(password),  # 隐藏实际密码
            score=score,
            level=level,
            entropy=entropy,
            crack_time=crack_time,
            issues=issues,
            suggestions=suggestions
        )
    
    def validate(self, password: str) -> Tuple[bool, List[str]]:
        """
        验证密码是否符合要求
        
        Args:
            password: 密码
        
        Returns:
            (是否有效, 错误消息列表)
        """
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"密码长度至少需要 {self.min_length} 个字符")
        
        if len(password) > self.max_length:
            errors.append(f"密码长度不能超过 {self.max_length} 个字符")
        
        if self.require_lowercase and not any(c.islower() for c in password):
            errors.append("密码必须包含小写字母")
        
        if self.require_uppercase and not any(c.isupper() for c in password):
            errors.append("密码必须包含大写字母")
        
        if self.require_digit and not any(c.isdigit() for c in password):
            errors.append("密码必须包含数字")
        
        if self.require_special and not any(c in string.punctuation for c in password):
            errors.append("密码必须包含特殊字符")
        
        result = self.analyze(password)
        if result.score < self.min_score:
            errors.append(f"密码强度不足，得分 {result.score}/100，最低要求 {self.min_score}/100")
        
        return len(errors) == 0, errors


class PasswordGenerator:
    """
    安全密码生成器
    生成符合安全要求的随机密码
    """
    
    # 字符集
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    AMBIGUOUS = "il1Lo0O"  # 容易混淆的字符
    
    def __init__(self,
                 length: int = 16,
                 use_lowercase: bool = True,
                 use_uppercase: bool = True,
                 use_digits: bool = True,
                 use_special: bool = True,
                 exclude_ambiguous: bool = True):
        """
        初始化密码生成器
        
        Args:
            length: 密码长度
            use_lowercase: 是否使用小写字母
            use_uppercase: 是否使用大写字母
            use_digits: 是否使用数字
            use_special: 是否使用特殊字符
            exclude_ambiguous: 是否排除容易混淆的字符
        """
        self.length = length
        self.use_lowercase = use_lowercase
        self.use_uppercase = use_uppercase
        self.use_digits = use_digits
        self.use_special = use_special
        self.exclude_ambiguous = exclude_ambiguous
    
    def generate(self) -> str:
        """
        生成随机密码
        
        Returns:
            生成的密码
        """
        # 构建字符集
        charset = ""
        required_chars = []
        
        if self.use_lowercase:
            chars = self.LOWERCASE
            if self.exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            if chars:
                required_chars.append(random.choice(chars))
        
        if self.use_uppercase:
            chars = self.UPPERCASE
            if self.exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            if chars:
                required_chars.append(random.choice(chars))
        
        if self.use_digits:
            chars = self.DIGITS
            if self.exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            if chars:
                required_chars.append(random.choice(chars))
        
        if self.use_special:
            charset += self.SPECIAL
            required_chars.append(random.choice(self.SPECIAL))
        
        if not charset:
            charset = self.LOWERCASE
        
        # 生成密码
        password = list(required_chars)
        
        # 填充剩余长度
        remaining = self.length - len(password)
        password.extend(random.choice(charset) for _ in range(remaining))
        
        # 打乱顺序
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_multiple(self, count: int) -> List[str]:
        """
        生成多个密码
        
        Args:
            count: 数量
        
        Returns:
            密码列表
        """
        return [self.generate() for _ in range(count)]
    
    def generate_passphrase(self, word_count: int = 4, 
                          separator: str = "-",
                          capitalize: bool = False,
                          add_number: bool = False) -> str:
        """
        生成密码短语（更容易记忆）
        
        Args:
            word_count: 单词数量
            separator: 分隔符
            capitalize: 是否首字母大写
            add_number: 是否添加数字
        
        Returns:
            生成的密码短语
        """
        # 简化的单词列表
        words = [
            "correct", "horse", "battery", "staple", "apple", "banana",
            "orange", "purple", "green", "blue", "red", "yellow",
            "happy", "sunny", "cloud", "storm", "river", "mountain",
            "forest", "ocean", "desert", "island", "valley", "bridge",
            "castle", "tower", "garden", "meadow", "stream", "shadow",
            "light", "dark", "bright", "strong", "swift", "gentle",
            "quiet", "loud", "soft", "hard", "warm", "cool", "fresh",
            "clear", "clean", "pure", "wild", "free", "brave", "smart"
        ]
        
        selected = random.sample(words, word_count)
        
        if capitalize:
            selected = [w.capitalize() for w in selected]
        
        passphrase = separator.join(selected)
        
        if add_number:
            passphrase += str(random.randint(0, 99))
        
        return passphrase


class PasswordValidator:
    """
    密码验证器
    提供多种验证规则
    """
    
    def __init__(self, analyzer: Optional[PasswordStrength] = None):
        """
        初始化验证器
        
        Args:
            analyzer: 密码强度分析器实例
        """
        self.analyzer = analyzer or PasswordStrength()
    
    def validate(self, password: str, 
                min_length: Optional[int] = None,
                max_length: Optional[int] = None,
                require_upper: Optional[bool] = None,
                require_lower: Optional[bool] = None,
                require_digit: Optional[bool] = None,
                require_special: Optional[bool] = None,
                min_entropy: Optional[float] = None,
                min_score: Optional[int] = None,
                exclude_common: bool = True) -> Tuple[bool, List[str]]:
        """
        验证密码
        
        Args:
            password: 密码
            min_length: 最小长度（覆盖分析器设置）
            max_length: 最大长度（覆盖分析器设置）
            require_upper: 是否要求大写字母
            require_lower: 是否要求小写字母
            require_digit: 是否要求数字
            require_special: 是否要求特殊字符
            min_entropy: 最小熵值
            min_score: 最小分数
            exclude_common: 是否排除常见密码
        
        Returns:
            (是否有效, 错误消息列表)
        """
        errors = []
        
        # 长度检查
        min_len = min_length if min_length is not None else self.analyzer.min_length
        max_len = max_length if max_length is not None else self.analyzer.max_length
        
        if len(password) < min_len:
            errors.append(f"密码长度不足，至少需要 {min_len} 个字符")
        
        if len(password) > max_len:
            errors.append(f"密码长度超限，最多 {max_len} 个字符")
        
        # 字符类型检查
        if require_upper is None:
            require_upper = self.analyzer.require_uppercase
        if require_lower is None:
            require_lower = self.analyzer.require_lowercase
        if require_digit is None:
            require_digit = self.analyzer.require_digit
        if require_special is None:
            require_special = self.analyzer.require_special
        
        if require_upper and not any(c.isupper() for c in password):
            errors.append("密码必须包含大写字母")
        
        if require_lower and not any(c.islower() for c in password):
            errors.append("密码必须包含小写字母")
        
        if require_digit and not any(c.isdigit() for c in password):
            errors.append("密码必须包含数字")
        
        if require_special and not any(c in string.punctuation for c in password):
            errors.append("密码必须包含特殊字符")
        
        # 熵检查
        if min_entropy is not None:
            entropy = PasswordEntropy.calculate(password)
            if entropy < min_entropy:
                errors.append(f"密码熵值不足，至少需要 {min_entropy:.1f} 位，当前 {entropy:.1f} 位")
        
        # 强度分数检查
        if min_score is not None:
            result = self.analyzer.analyze(password)
            if result.score < min_score:
                errors.append(f"密码强度不足，至少需要 {min_score} 分，当前 {result.score} 分")
        
        # 常见密码检查
        if exclude_common and CommonPasswordChecker.is_common(password):
            errors.append("这是一个常见密码，请使用更独特的密码")
        
        return len(errors) == 0, errors
    
    def get_strength_summary(self, password: str) -> str:
        """
        获取密码强度摘要
        
        Args:
            password: 密码
        
        Returns:
            强度摘要字符串
        """
        result = self.analyzer.analyze(password)
        
        summary = [
            f"密码强度: {result.level.name}",
            f"得分: {result.score}/100",
            f"熵值: {result.entropy:.1f} 位",
            f"预估破解时间: {result.crack_time}"
        ]
        
        if result.issues:
            summary.append(f"问题: {', '.join(i.value for i in result.issues)}")
        
        return "\n".join(summary)


# 便捷函数
def check_password(password: str) -> StrengthResult:
    """
    快速检查密码强度
    
    Args:
        password: 密码
    
    Returns:
        强度分析结果
    """
    analyzer = PasswordStrength()
    return analyzer.analyze(password)


def generate_password(length: int = 16, 
                      use_special: bool = True,
                      exclude_ambiguous: bool = True) -> str:
    """
    快速生成密码
    
    Args:
        length: 密码长度
        use_special: 是否使用特殊字符
        exclude_ambiguous: 是否排除混淆字符
    
    Returns:
        生成的密码
    """
    generator = PasswordGenerator(
        length=length,
        use_special=use_special,
        exclude_ambiguous=exclude_ambiguous
    )
    return generator.generate()


def generate_passphrase(word_count: int = 4) -> str:
    """
    快速生成密码短语
    
    Args:
        word_count: 单词数量
    
    Returns:
        生成的密码短语
    """
    generator = PasswordGenerator()
    return generator.generate_passphrase(word_count=word_count)


def is_strong_password(password: str, min_score: int = 60) -> bool:
    """
    检查密码是否足够强
    
    Args:
        password: 密码
        min_score: 最低分数
    
    Returns:
        是否为强密码
    """
    result = check_password(password)
    return result.score >= min_score