#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Captcha Utils - CAPTCHA 生成与验证工具模块
============================================
提供文本验证码生成、ASCII 艺术 CAPTCHA、图像 CAPTCHA（可选）功能。
零外部依赖核心实现，可选 Pillow 支持增强图像生成。

主要功能:
- 文本验证码生成（数字、字母、混合）
- ASCII 艺术 CAPTCHA（无外部依赖）
- 图像 CAPTCHA（Pillow 可选）
- 噪声与扭曲处理
- 数学验证码（算术运算）
- 验证码存储与验证
- 批量验证码生成
- 验证码难度控制

作者: AllToolkit
日期: 2026-05-15
"""

import random
import string
import hashlib
import time
import math
from typing import Optional, Dict, List, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import io
import base64


# =============================================================================
# Pillow 可选导入
# =============================================================================

_PILLOW_AVAILABLE = False
Image = None
ImageDraw = None
ImageFont = None
ImageFilter = None

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    _PILLOW_AVAILABLE = True
except ImportError:
    pass


# =============================================================================
# 常量与配置
# =============================================================================

# ASCII 艺术字符映射
ASCII_ART_CHARS = {
    '0': [
        " ██████ ",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██████ "
    ],
    '1': [
        "  ██    ",
        " ████   ",
        "  ██    ",
        "  ██    ",
        "██████  "
    ],
    '2': [
        " ██████ ",
        "     ██ ",
        " █████  ",
        "██      ",
        "███████ "
    ],
    '3': [
        " ██████ ",
        "     ██ ",
        " ██████ ",
        "     ██ ",
        " ██████ "
    ],
    '4': [
        "██    ██",
        "██    ██",
        "████████",
        "      ██",
        "      ██"
    ],
    '5': [
        "███████ ",
        "██      ",
        "██████  ",
        "     ██ ",
        "██████  "
    ],
    '6': [
        " ██████ ",
        "██      ",
        "██████  ",
        "██    ██",
        " ██████ "
    ],
    '7': [
        "███████ ",
        "     ██ ",
        "    ██  ",
        "   ██   ",
        "  ██    "
    ],
    '8': [
        " ██████ ",
        "██    ██",
        " ██████ ",
        "██    ██",
        " ██████ "
    ],
    '9': [
        " ██████ ",
        "██    ██",
        " ███████",
        "     ██ ",
        " ██████ "
    ],
    'A': [
        "   ██   ",
        "  ████  ",
        " ██  ██ ",
        "████████",
        "██    ██"
    ],
    'B': [
        "██████  ",
        "██    ██",
        "██████  ",
        "██    ██",
        "██████  "
    ],
    'C': [
        " ██████ ",
        "██      ",
        "██      ",
        "██      ",
        " ██████ "
    ],
    'D': [
        "██████  ",
        "██    ██",
        "██    ██",
        "██    ██",
        "██████  "
    ],
    'E': [
        "███████ ",
        "██      ",
        "██████  ",
        "██      ",
        "███████ "
    ],
    'F': [
        "███████ ",
        "██      ",
        "██████  ",
        "██      ",
        "██      "
    ],
    'G': [
        " ██████ ",
        "██      ",
        "██  ████",
        "██    ██",
        " ██████ "
    ],
    'H': [
        "██    ██",
        "██    ██",
        "████████",
        "██    ██",
        "██    ██"
    ],
    'I': [
        "██████  ",
        "  ██    ",
        "  ██    ",
        "  ██    ",
        "██████  "
    ],
    'J': [
        "███████ ",
        "    ██  ",
        "    ██  ",
        "██  ██  ",
        " ████   "
    ],
    'K': [
        "██    ██",
        "██  ██  ",
        "████    ",
        "██  ██  ",
        "██    ██"
    ],
    'L': [
        "██      ",
        "██      ",
        "██      ",
        "██      ",
        "███████ "
    ],
    'M': [
        "██    ██",
        "███  ███",
        "██ ██ ██",
        "██    ██",
        "██    ██"
    ],
    'N': [
        "██    ██",
        "███   ██",
        "██ ██ ██",
        "██   ███",
        "██    ██"
    ],
    'O': [
        " ██████ ",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██████ "
    ],
    'P': [
        "██████  ",
        "██    ██",
        "██████  ",
        "██      ",
        "██      "
    ],
    'Q': [
        " ██████ ",
        "██    ██",
        "██    ██",
        "██  ███ ",
        " ███████"
    ],
    'R': [
        "██████  ",
        "██    ██",
        "██████  ",
        "██  ██  ",
        "██    ██"
    ],
    'S': [
        " ██████ ",
        "██      ",
        " █████  ",
        "     ██ ",
        "██████  "
    ],
    'T': [
        "███████ ",
        "  ██    ",
        "  ██    ",
        "  ██    ",
        "  ██    "
    ],
    'U': [
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        " ██████ "
    ],
    'V': [
        "██    ██",
        "██    ██",
        "██    ██",
        " ██  ██ ",
        "  ████  "
    ],
    'W': [
        "██    ██",
        "██    ██",
        "██ ██ ██",
        "███  ███",
        "██    ██"
    ],
    'X': [
        "██    ██",
        " ██  ██ ",
        "  ████  ",
        " ██  ██ ",
        "██    ██"
    ],
    'Y': [
        "██    ██",
        " ██  ██ ",
        "  ████  ",
        "  ██    ",
        "  ██    "
    ],
    'Z': [
        "███████ ",
        "    ██  ",
        "  ██    ",
        "██      ",
        "███████ "
    ],
}

# 简化版 ASCII 艺术（用于窄显示）
SIMPLE_ASCII_CHARS = {
    '0': ['╭───╮', '│   │', '│   │', '│   │', '╰───╯'],
    '1': ['  ┌─', '  │ ', '  │ ', '  │ ', '──┘ '],
    '2': ['╭──╮ ', '   ─┤', '╭─┘ ', '│   ', '╰───╯'],
    '3': ['╭──╮ ', '   ─┤', '   ─┤', '   ─┤', '╰──╯ '],
    '4': ['│  ┌─', '│  │ ', '╰──┤ ', '   │ ', '   ╰ '],
    '5': ['╭─── ', '│──╮ ', '   ─┤', '   ─┤', '╰──╯ '],
    '6': ['╭──╮ ', '│   ', '│──╮ ', '│  │ ', '╰──╯ '],
    '7': ['╭───', '  ─┤', '   │', '   │', '   ╰'],
    '8': ['╭──╮ ', '│  │ ', '╰──╯ ', '│  │ ', '╰──╯ '],
    '9': ['╭──╮ ', '│  │ ', '╰──┤ ', '   │ ', '╰──╯ '],
    'A': [' ╭─╮ ', '│ │ │', '╰─┬─╯', '  │  ', '  ╰  '],
    'B': ['╭──╮ ', '│  │ ', '╰──┤ ', '│  │ ', '╰──╯ '],
    'C': ['╭───╮', '│    ', '│    ', '│    ', '╰───╯'],
    'D': ['╭──╮ ', '│  │ ', '│  │ ', '│  │ ', '╰──╯ '],
    'E': ['╭─── ', '│──  ', '│─   ', '│──  ', '╰─── '],
    'F': ['╭─── ', '│──  ', '│─   ', '│    ', '╰    '],
    'G': ['╭───╮', '│    ', '│ ──╮', '│   │', '╰───╯'],
    'H': ['│   │', '│   │', '╰─┬─╯', '│   │', '╰   ╯'],
    'I': ['╭───', '  │ ', '  │ ', '  │ ', '╰───'],
    'J': ['╭───', '  │ ', '  │ ', '┌│  ', '╰───'],
    'K': ['│  ┌─', '│ ┌─ ', '╰─┤  ', '│ └─ ', '│  └─'],
    'L': ['│    ', '│    ', '│    ', '│    ', '╰─── '],
    'M': ['╭─╮─╭', '│ │ │', '│ │ │', '╰ ╰ ╰', '     '],
    'N': ['╭─┌─╮', '│ │ │', '│ │ │', '╰ ╰ ╰', '     '],
    'O': ['╭───╮', '│   │', '│   │', '│   │', '╰───╯'],
    'P': ['╭──╮ ', '│  │ ', '╰──┤ ', '│   ', '╰   '],
    'Q': ['╭───╮', '│   │', '│ ─ │', '│   ╰', '╰───┘'],
    'R': ['╭──╮ ', '│  │ ', '╰──┤ ', '│ │  ', '╰ ╰  '],
    'S': ['╭─── ', '│    ', '╰─── ', '   │ ', '───╯ '],
    'T': ['╭───', '  │ ', '  │ ', '  │ ', '  ╰ '],
    'U': ['│   │', '│   │', '│   │', '│   │', '╰───╯'],
    'V': ['│   │', '│   │', ' │ │ ', ' │ │ ', '  ╰  '],
    'W': ['│ │ │', '│ │ │', '│ │ │', '╰ ╰ ╰', '     '],
    'X': ['╲ ╱ ', ' ╲╱ ', ' ╱╲ ', '╱ ╲ ', '     '],
    'Y': ['╲ ╱ ', ' ╲╱ ', '  │ ', '  │ ', '  ╰ '],
    'Z': ['╭───', '  ╱ ', ' ╱  ', '╱   ', '╰───'],
}


class CaptchaType(Enum):
    """验证码类型"""
    TEXT = "text"              # 纯文本验证码
    ASCII_ART = "ascii"        # ASCII 艺术验证码
    IMAGE = "image"            # 图像验证码（需要 Pillow）
    MATH = "math"              # 数学验证码
    REVERSE = "reverse"        # 反序验证码
    MIXED = "mixed"            # 混合验证码


class CaptchaDifficulty(Enum):
    """验证码难度"""
    EASY = "easy"              # 简单（4字符，无干扰）
    MEDIUM = "medium"          # 中等（6字符，轻微干扰）
    HARD = "hard"              # 困难（8字符，较强干扰）
    EXTREME = "extreme"        # 极难（8字符，重干扰+扭曲）


class CaptchaCharset(Enum):
    """验证码字符集"""
    DIGITS = "digits"          # 纯数字
    LOWERCASE = "lower"        # 小写字母
    UPPERCASE = "upper"        # 大写字母
    ALPHANUMERIC = "alnum"     # 数字+字母
    MIXED = "mixed"            # 数字+大小写字母


@dataclass
class CaptchaResult:
    """验证码结果"""
    text: str                  # 验证码文本
    captcha: str               # 验证码内容（ASCII艺术或Base64图像）
    captcha_type: CaptchaType  # 验证码类型
    difficulty: CaptchaDifficulty  # 难度
    timestamp: float           # 生成时间戳
    expires_in: float          # 过期时间（秒）
    hash: str                  # 验证哈希（用于验证）
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() > self.timestamp + self.expires_in
    
    def verify(self, user_input: str, case_sensitive: bool = False) -> bool:
        """
        验证用户输入
        
        Args:
            user_input: 用户输入
            case_sensitive: 是否区分大小写
        
        Returns:
            是否正确
        """
        if self.is_expired():
            return False
        
        if not case_sensitive:
            return user_input.lower() == self.text.lower()
        return user_input == self.text
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'text': self.text,
            'captcha': self.captcha,
            'captcha_type': self.captcha_type.value,
            'difficulty': self.difficulty.value,
            'timestamp': self.timestamp,
            'expires_in': self.expires_in,
            'hash': self.hash,
            'expired': self.is_expired()
        }


@dataclass
class MathCaptchaResult:
    """数学验证码结果"""
    question: str              # 问题文本
    answer: int                # 答案
    captcha: str               # ASCII艺术问题
    captcha_type: CaptchaType  # 类型（MATH）
    difficulty: CaptchaDifficulty
    timestamp: float
    expires_in: float
    hash: str
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() > self.timestamp + self.expires_in
    
    def verify(self, user_input: Union[int, str]) -> bool:
        """
        验证用户答案
        
        Args:
            user_input: 用户答案（数字或字符串）
        
        Returns:
            是否正确
        """
        if self.is_expired():
            return False
        
        try:
            if isinstance(user_input, str):
                user_answer = int(user_input.strip())
            else:
                user_answer = user_input
            return user_answer == self.answer
        except (ValueError, TypeError):
            return False


# =============================================================================
# 验证码生成器
# =============================================================================

class CaptchaGenerator:
    """验证码生成器"""
    
    def __init__(self, secret: str = "default_secret"):
        """
        初始化验证码生成器
        
        Args:
            secret: 密钥（用于哈希生成）
        """
        self._secret = secret
        self._storage: Dict[str, CaptchaResult] = {}
    
    def _generate_hash(self, text: str, timestamp: float) -> str:
        """生成验证哈希"""
        data = f"{self._secret}:{text}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _get_charset(self, charset: CaptchaCharset) -> str:
        """获取字符集"""
        charset_map = {
            CaptchaCharset.DIGITS: string.digits,
            CaptchaCharset.LOWERCASE: string.ascii_lowercase,
            CaptchaCharset.UPPERCASE: string.ascii_uppercase,
            CaptchaCharset.ALPHANUMERIC: string.digits + string.ascii_uppercase,
            CaptchaCharset.MIXED: string.digits + string.ascii_letters,
        }
        return charset_map[charset]
    
    def _get_length_by_difficulty(self, difficulty: CaptchaDifficulty) -> int:
        """根据难度获取长度"""
        length_map = {
            CaptchaDifficulty.EASY: 4,
            CaptchaDifficulty.MEDIUM: 6,
            CaptchaDifficulty.HARD: 8,
            CaptchaDifficulty.EXTREME: 8,
        }
        return length_map[difficulty]
    
    def _generate_text(self, length: int, charset: str, 
                       exclude_similar: bool = True) -> str:
        """
        生成随机文本
        
        Args:
            length: 长度
            charset: 字符集
            exclude_similar: 是否排除相似字符（如 0/O, 1/I/l）
        
        Returns:
            随机文本
        """
        if exclude_similar:
            # 排除容易混淆的字符
            similar_chars = {'0', 'O', '1', 'I', 'l', '2', 'Z', '5', 'S', '8', 'B'}
            charset = ''.join(c for c in charset if c not in similar_chars)
        
        return ''.join(random.choice(charset) for _ in range(length))
    
    def generate_text_captcha(
        self,
        length: Optional[int] = None,
        charset: CaptchaCharset = CaptchaCharset.DIGITS,
        difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
        expires_in: float = 300.0,
        exclude_similar: bool = True
    ) -> CaptchaResult:
        """
        生成纯文本验证码
        
        Args:
            length: 验证码长度（可选，默认根据难度）
            charset: 字符集类型
            difficulty: 验证码难度
            expires_in: 过期时间（秒）
            exclude_similar: 是否排除相似字符
        
        Returns:
            CaptchaResult 对象
        
        Examples:
            >>> gen = CaptchaGenerator()
            >>> captcha = gen.generate_text_captcha(length=6)
            >>> captcha.text  # 随机6位数字
            '342891'
        """
        if length is None:
            length = self._get_length_by_difficulty(difficulty)
        
        charset_str = self._get_charset(charset)
        text = self._generate_text(length, charset_str, exclude_similar)
        
        timestamp = time.time()
        hash_val = self._generate_hash(text, timestamp)
        
        result = CaptchaResult(
            text=text,
            captcha=text,
            captcha_type=CaptchaType.TEXT,
            difficulty=difficulty,
            timestamp=timestamp,
            expires_in=expires_in,
            hash=hash_val
        )
        
        return result
    
    def generate_ascii_captcha(
        self,
        length: Optional[int] = None,
        charset: CaptchaCharset = CaptchaCharset.ALPHANUMERIC,
        difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
        expires_in: float = 300.0,
        simple_style: bool = False,
        add_noise: bool = True,
        exclude_similar: bool = True
    ) -> CaptchaResult:
        """
        生成 ASCII 艺术验证码
        
        Args:
            length: 验证码长度
            charset: 字符集类型
            difficulty: 验证码难度
            expires_in: 过期时间（秒）
            simple_style: 是否使用简化风格
            add_noise: 是否添加噪声
            exclude_similar: 是否排除相似字符
        
        Returns:
            CaptchaResult 对象
        
        Examples:
            >>> gen = CaptchaGenerator()
            >>> captcha = gen.generate_ascii_captcha(length=4)
            >>> print(captcha.captcha)
            ████
            ██    ██
            ...
        """
        if length is None:
            length = self._get_length_by_difficulty(difficulty)
        
        # 使用大写字母和数字（ASCII艺术只支持大写）
        charset_str = self._get_charset(CaptchaCharset.ALPHANUMERIC)
        text = self._generate_text(length, charset_str, exclude_similar)
        
        # 选择字符映射
        char_map = SIMPLE_ASCII_CHARS if simple_style else ASCII_ART_CHARS
        
        # 生成 ASCII 艺术
        ascii_lines = self._render_ascii_text(text, char_map, add_noise, difficulty)
        ascii_captcha = '\n'.join(ascii_lines)
        
        timestamp = time.time()
        hash_val = self._generate_hash(text, timestamp)
        
        result = CaptchaResult(
            text=text,
            captcha=ascii_captcha,
            captcha_type=CaptchaType.ASCII_ART,
            difficulty=difficulty,
            timestamp=timestamp,
            expires_in=expires_in,
            hash=hash_val
        )
        
        return result
    
    def _render_ascii_text(
        self,
        text: str,
        char_map: Dict,
        add_noise: bool,
        difficulty: CaptchaDifficulty
    ) -> List[str]:
        """
        渲染 ASCII 文本
        
        Args:
            text: 要渲染的文本
            char_map: 字符映射
            add_noise: 是否添加噪声
            difficulty: 验证码难度
        
        Returns:
            ASCII 艺术行列表
        """
        # 获取每个字符的艺术表示
        chars_art = []
        for c in text:
            if c in char_map:
                chars_art.append(char_map[c])
            else:
                # 未知字符用空白块替代
                chars_art.append(['    '] * 5)
        
        # 合并字符
        num_lines = 5
        result_lines = []
        
        for i in range(num_lines):
            line_parts = []
            for art in chars_art:
                line_parts.append(art[i])
            result_lines.append(' '.join(line_parts))
        
        # 添加噪声
        if add_noise:
            noise_level = {
                CaptchaDifficulty.EASY: 0.05,
                CaptchaDifficulty.MEDIUM: 0.15,
                CaptchaDifficulty.HARD: 0.25,
                CaptchaDifficulty.EXTREME: 0.35,
            }
            result_lines = self._add_noise_to_lines(
                result_lines, noise_level[difficulty]
            )
        
        # 添加干扰线
        if difficulty in (CaptchaDifficulty.HARD, CaptchaDifficulty.EXTREME):
            result_lines = self._add_interference_lines(result_lines)
        
        return result_lines
    
    def _add_noise_to_lines(self, lines: List[str], noise_level: float) -> List[str]:
        """添加噪声到 ASCII 行"""
        noise_chars = ['░', '▒', '▓', '·', '∙', '•', '○', '●', '█', '▄', '▀']
        result = []
        
        for line in lines:
            new_line = []
            for c in line:
                if c == ' ' and random.random() < noise_level:
                    new_line.append(random.choice(noise_chars))
                else:
                    new_line.append(c)
            result.append(''.join(new_line))
        
        return result
    
    def _add_interference_lines(self, lines: List[str]) -> List[str]:
        """添加干扰线"""
        if len(lines) < 3:
            return lines
        
        result = lines.copy()
        line_len = max(len(l) for l in lines)
        
        # 在中间插入干扰线
        interference_line = ''.join(
            random.choice(['─', '━', '┄', '┅', '╌', '╍']) 
            for _ in range(line_len)
        )
        
        # 随机插入位置
        insert_pos = random.randint(1, len(result) - 1)
        result.insert(insert_pos, interference_line)
        
        return result
    
    def generate_math_captcha(
        self,
        difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
        expires_in: float = 300.0,
        max_answer: int = 100
    ) -> MathCaptchaResult:
        """
        生成数学验证码
        
        Args:
            difficulty: 验证码难度
            expires_in: 过期时间（秒）
            max_answer: 最大答案值
        
        Returns:
            MathCaptchaResult 对象
        
        Examples:
            >>> gen = CaptchaGenerator()
            >>> captcha = gen.generate_math_captcha()
            >>> captcha.question  # 如 '3 + 7 = ?'
            '3 + 7 = ?'
            >>> captcha.answer
            10
        """
        # 根据难度调整范围
        ranges = {
            CaptchaDifficulty.EASY: (1, 10),
            CaptchaDifficulty.MEDIUM: (1, 50),
            CaptchaDifficulty.HARD: (1, max_answer),
            CaptchaDifficulty.EXTREME: (10, max_answer),
        }
        min_val, max_val = ranges[difficulty]
        
        # 根据难度选择运算类型
        if difficulty in (CaptchaDifficulty.EASY, CaptchaDifficulty.MEDIUM):
            operations = ['+', '-']
        else:
            operations = ['+', '-', '×', '÷']
        
        op = random.choice(operations)
        
        # 生成数字和答案
        if op == '+':
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            answer = a + b
            question = f"{a} + {b} = ?"
        elif op == '-':
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, min(a, max_val))  # 确保结果非负
            answer = a - b
            question = f"{a} - {b} = ?"
        elif op == '×':
            a = random.randint(min_val, max_val // 5)
            b = random.randint(min_val, 10)
            answer = a * b
            question = f"{a} × {b} = ?"
        else:  # ÷
            b = random.randint(1, 10)
            answer = random.randint(min_val, max_val // 10)
            a = answer * b  # 确保能整除
            question = f"{a} ÷ {b} = ?"
        
        # 生成 ASCII 艺术（可选）
        ascii_question = self._render_math_question(question, difficulty)
        
        timestamp = time.time()
        hash_val = self._generate_hash(str(answer), timestamp)
        
        return MathCaptchaResult(
            question=question,
            answer=answer,
            captcha=ascii_question,
            captcha_type=CaptchaType.MATH,
            difficulty=difficulty,
            timestamp=timestamp,
            expires_in=expires_in,
            hash=hash_val
        )
    
    def _render_math_question(self, question: str, 
                               difficulty: CaptchaDifficulty) -> str:
        """渲染数学问题为 ASCII 艺术"""
        # 简单的格式化
        lines = []
        lines.append("╭" + "─" * (len(question) + 4) + "╮")
        lines.append("│" + " " * 2 + question + " " * 2 + "│")
        lines.append("╰" + "─" * (len(question) + 4) + "╯")
        
        if difficulty in (CaptchaDifficulty.HARD, CaptchaDifficulty.EXTREME):
            # 添加干扰
            lines.append("  " + random.choice(['∙∙∙∙∙', '·····', '≈≈≈≈≈']))
        
        return '\n'.join(lines)
    
    def generate_reverse_captcha(
        self,
        length: Optional[int] = None,
        charset: CaptchaCharset = CaptchaCharset.DIGITS,
        difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
        expires_in: float = 300.0
    ) -> CaptchaResult:
        """
        生成反序验证码（用户需要输入反转后的文本）
        
        Args:
            length: 验证码长度
            charset: 字符集类型
            difficulty: 验证码难度
            expires_in: 过期时间（秒）
        
        Returns:
            CaptchaResult 对象
        
        Examples:
            >>> gen = CaptchaGenerator()
            >>> captcha = gen.generate_reverse_captcha()
            >>> captcha.text  # 显示 '1234'
            '1234'
            >>> # 用户需要输入 '4321'
        """
        if length is None:
            length = self._get_length_by_difficulty(difficulty)
        
        charset_str = self._get_charset(charset)
        original_text = self._generate_text(length, charset_str)
        
        # 显示原文本，但答案是反转后的
        reversed_text = original_text[::-1]
        
        timestamp = time.time()
        # 哈希使用反转后的文本
        hash_val = self._generate_hash(reversed_text, timestamp)
        
        # 显示提示
        hint = "请输入反转后的文本: "
        display = hint + original_text
        
        result = CaptchaResult(
            text=reversed_text,  # 答案是反转后的
            captcha=display,
            captcha_type=CaptchaType.REVERSE,
            difficulty=difficulty,
            timestamp=timestamp,
            expires_in=expires_in,
            hash=hash_val
        )
        
        return result
    
    def generate_image_captcha(
        self,
        length: Optional[int] = None,
        charset: CaptchaCharset = CaptchaCharset.ALPHANUMERIC,
        difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
        expires_in: float = 300.0,
        width: int = 200,
        height: int = 80,
        font_size: int = 40,
        output_format: str = "base64"
    ) -> CaptchaResult:
        """
        生成图像验证码（需要 Pillow）
        
        Args:
            length: 验证码长度
            charset: 字符集类型
            difficulty: 验证码难度
            expires_in: 过期时间（秒）
            width: 图像宽度
            height: 图像高度
            font_size: 字体大小
            output_format: 输出格式（base64 或 path）
        
        Returns:
            CaptchaResult 对象
        
        Raises:
            ImportError: 如果 Pillow 不可用
        
        Examples:
            >>> gen = CaptchaGenerator()
            >>> captcha = gen.generate_image_captcha()
            >>> # captcha.captcha 是 Base64 编码的 PNG
        """
        if not _PILLOW_AVAILABLE:
            raise ImportError("Pillow 库未安装，无法生成图像验证码")
        
        if length is None:
            length = self._get_length_by_difficulty(difficulty)
        
        charset_str = self._get_charset(CaptchaCharset.ALPHANUMERIC)
        text = self._generate_text(length, charset_str, exclude_similar=True)
        
        # 创建图像
        img = Image.new('RGB', (width, height), color=self._get_random_bg_color())
        draw = ImageDraw.Draw(img)
        
        # 尝试使用字体
        try:
            # 使用默认字体或尝试加载系统字体
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # 绘制文本（带扭曲）
        text_width = len(text) * font_size * 0.6
        start_x = (width - text_width) // 2
        
        for i, char in enumerate(text):
            x = start_x + i * font_size * 0.6
            y = (height - font_size) // 2
            
            # 添加随机偏移和旋转
            y_offset = random.randint(-10, 10) if difficulty in (CaptchaDifficulty.HARD, CaptchaDifficulty.EXTREME) else 0
            
            char_img = Image.new('RGBA', (font_size, font_size + 20), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((0, y_offset), char, font=font, fill=self._get_random_text_color())
            
            # 随机旋转
            if difficulty == CaptchaDifficulty.EXTREME:
                rotation = random.randint(-30, 30)
                char_img = char_img.rotate(rotation, expand=True)
            
            # 粘贴到主图
            img.paste(char_img, (int(x), int(y)), char_img)
        
        # 添加噪声
        if difficulty in (CaptchaDifficulty.MEDIUM, CaptchaDifficulty.HARD, CaptchaDifficulty.EXTREME):
            self._add_image_noise(img, draw, difficulty)
        
        # 添加干扰线
        if difficulty in (CaptchaDifficulty.HARD, CaptchaDifficulty.EXTREME):
            self._add_interference_to_image(draw, width, height)
        
        # 输出
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        
        if output_format == 'base64':
            captcha_data = base64.b64encode(buffer.getvalue()).decode('ascii')
        else:
            captcha_data = buffer.getvalue()
        
        timestamp = time.time()
        hash_val = self._generate_hash(text, timestamp)
        
        return CaptchaResult(
            text=text,
            captcha=captcha_data,
            captcha_type=CaptchaType.IMAGE,
            difficulty=difficulty,
            timestamp=timestamp,
            expires_in=expires_in,
            hash=hash_val
        )
    
    def _get_random_bg_color(self) -> Tuple[int, int, int]:
        """获取随机背景色"""
        # 使用浅色背景
        return (
            random.randint(220, 255),
            random.randint(220, 255),
            random.randint(220, 255)
        )
    
    def _get_random_text_color(self) -> Tuple[int, int, int]:
        """获取随机文本颜色"""
        # 使用深色文本
        return (
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)
        )
    
    def _add_image_noise(self, img, draw, difficulty: CaptchaDifficulty) -> None:
        """添加图像噪声"""
        noise_count = {
            CaptchaDifficulty.MEDIUM: 100,
            CaptchaDifficulty.HARD: 200,
            CaptchaDifficulty.EXTREME: 400,
        }
        
        width, height = img.size
        
        for _ in range(noise_count.get(difficulty, 0)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            draw.point((x, y), fill=color)
    
    def _add_interference_to_image(self, draw, width: int, height: int) -> None:
        """添加干扰线"""
        for _ in range(3):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    
    def generate_mixed_captcha(
        self,
        difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
        expires_in: float = 300.0
    ) -> Union[CaptchaResult, MathCaptchaResult]:
        """
        随机生成混合类型验证码
        
        Args:
            difficulty: 验证码难度
            expires_in: 过期时间（秒）
        
        Returns:
            验证码结果
        
        Examples:
            >>> gen = CaptchaGenerator()
            >>> captcha = gen.generate_mixed_captcha()
            >>> captcha.captcha_type  # 随机类型
        """
        types = [CaptchaType.TEXT, CaptchaType.ASCII_ART, CaptchaType.MATH, CaptchaType.REVERSE]
        chosen_type = random.choice(types)
        
        if chosen_type == CaptchaType.TEXT:
            return self.generate_text_captcha(difficulty=difficulty, expires_in=expires_in)
        elif chosen_type == CaptchaType.ASCII_ART:
            return self.generate_ascii_captcha(difficulty=difficulty, expires_in=expires_in)
        elif chosen_type == CaptchaType.MATH:
            return self.generate_math_captcha(difficulty=difficulty, expires_in=expires_in)
        else:
            return self.generate_reverse_captcha(difficulty=difficulty, expires_in=expires_in)


# =============================================================================
# 验证码存储与验证
# =============================================================================

class CaptchaStore:
    """验证码存储器"""
    
    def __init__(self, max_size: int = 1000, cleanup_interval: float = 60.0):
        """
        初始化存储器
        
        Args:
            max_size: 最大存储数量
            cleanup_interval: 清理间隔（秒）
        """
        self._store: Dict[str, Union[CaptchaResult, MathCaptchaResult]] = {}
        self._max_size = max_size
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()
    
    def store(self, captcha_id: str, captcha: Union[CaptchaResult, MathCaptchaResult]) -> None:
        """
        存储验证码
        
        Args:
            captcha_id: 验证码ID
            captcha: 验证码结果
        """
        # 清理过期验证码
        if time.time() - self._last_cleanup > self._cleanup_interval:
            self._cleanup_expired()
        
        # 如果超过最大数量，移除最早的
        if len(self._store) >= self._max_size:
            self._remove_oldest()
        
        self._store[captcha_id] = captcha
    
    def get(self, captcha_id: str) -> Optional[Union[CaptchaResult, MathCaptchaResult]]:
        """获取验证码"""
        return self._store.get(captcha_id)
    
    def verify(self, captcha_id: str, user_input: str,
               case_sensitive: bool = False, remove_on_success: bool = True) -> bool:
        """
        验证用户输入
        
        Args:
            captcha_id: 验证码ID
            user_input: 用户输入
            case_sensitive: 是否区分大小写
            remove_on_success: 成功后是否删除
        
        Returns:
            是否正确
        """
        captcha = self._store.get(captcha_id)
        if captcha is None:
            return False
        
        result = captcha.verify(user_input, case_sensitive)
        
        if result and remove_on_success:
            del self._store[captcha_id]
        
        return result
    
    def remove(self, captcha_id: str) -> bool:
        """删除验证码"""
        if captcha_id in self._store:
            del self._store[captcha_id]
            return True
        return False
    
    def _cleanup_expired(self) -> int:
        """清理过期验证码"""
        expired_ids = [
            id for id, captcha in self._store.items()
            if captcha.is_expired()
        ]
        
        for id in expired_ids:
            del self._store[id]
        
        self._last_cleanup = time.time()
        return len(expired_ids)
    
    def _remove_oldest(self) -> None:
        """移除最早的验证码"""
        if not self._store:
            return
        
        oldest_id = min(
            self._store.keys(),
            key=lambda x: self._store[x].timestamp
        )
        del self._store[oldest_id]
    
    def clear(self) -> None:
        """清空存储"""
        self._store.clear()
    
    def size(self) -> int:
        """获取存储数量"""
        return len(self._store)


# =============================================================================
# 快捷函数
# =============================================================================

_default_generator = CaptchaGenerator()
_default_store = CaptchaStore()


def generate_captcha(
    captcha_type: CaptchaType = CaptchaType.ASCII_ART,
    length: Optional[int] = None,
    charset: CaptchaCharset = CaptchaCharset.ALPHANUMERIC,
    difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM,
    expires_in: float = 300.0
) -> Union[CaptchaResult, MathCaptchaResult]:
    """
    快捷生成验证码
    
    Args:
        captcha_type: 验证码类型
        length: 验证码长度
        charset: 字符集类型
        difficulty: 验证码难度
        expires_in: 过期时间（秒）
    
    Returns:
        验证码结果
    
    Examples:
        >>> captcha = generate_captcha()
        >>> print(captcha.captcha)
    """
    if captcha_type == CaptchaType.TEXT:
        return _default_generator.generate_text_captcha(
            length=length, charset=charset, difficulty=difficulty, expires_in=expires_in
        )
    elif captcha_type == CaptchaType.ASCII_ART:
        return _default_generator.generate_ascii_captcha(
            length=length, charset=charset, difficulty=difficulty, expires_in=expires_in
        )
    elif captcha_type == CaptchaType.MATH:
        return _default_generator.generate_math_captcha(
            difficulty=difficulty, expires_in=expires_in
        )
    elif captcha_type == CaptchaType.REVERSE:
        return _default_generator.generate_reverse_captcha(
            length=length, charset=charset, difficulty=difficulty, expires_in=expires_in
        )
    elif captcha_type == CaptchaType.IMAGE:
        return _default_generator.generate_image_captcha(
            length=length, charset=charset, difficulty=difficulty, expires_in=expires_in
        )
    else:
        return _default_generator.generate_mixed_captcha(
            difficulty=difficulty, expires_in=expires_in
        )


def create_and_store_captcha(
    captcha_id: str,
    captcha_type: CaptchaType = CaptchaType.ASCII_ART,
    difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM
) -> Union[CaptchaResult, MathCaptchaResult]:
    """
    生成并存储验证码
    
    Args:
        captcha_id: 验证码ID
        captcha_type: 验证码类型
        difficulty: 验证码难度
    
    Returns:
        验证码结果
    """
    captcha = generate_captcha(captcha_type=captcha_type, difficulty=difficulty)
    _default_store.store(captcha_id, captcha)
    return captcha


def verify_captcha(
    captcha_id: str,
    user_input: str,
    case_sensitive: bool = False
) -> bool:
    """
    快捷验证验证码
    
    Args:
        captcha_id: 验证码ID
        user_input: 用户输入
        case_sensitive: 是否区分大小写
    
    Returns:
        是否正确
    """
    return _default_store.verify(captcha_id, user_input, case_sensitive)


def generate_batch_captchas(
    count: int,
    captcha_type: CaptchaType = CaptchaType.ASCII_ART,
    difficulty: CaptchaDifficulty = CaptchaDifficulty.MEDIUM
) -> List[Union[CaptchaResult, MathCaptchaResult]]:
    """
    批量生成验证码
    
    Args:
        count: 生成数量
        captcha_type: 验证码类型
        difficulty: 验证码难度
    
    Returns:
        验证码结果列表
    """
    return [
        generate_captcha(captcha_type=captcha_type, difficulty=difficulty)
        for _ in range(count)
    ]


# =============================================================================
# 演示
# =============================================================================

if __name__ == "__main__":
    print("Captcha Utils 演示")
    print("=" * 60)
    
    gen = CaptchaGenerator()
    
    # 1. 文本验证码
    print("\n1. 文本验证码:")
    text_captcha = gen.generate_text_captcha(length=6)
    print(f"   验证码: {text_captcha.text}")
    print(f"   类型: {text_captcha.captcha_type.value}")
    print(f"   过期时间: {text_captcha.expires_in}秒")
    
    # 2. ASCII 艺术验证码
    print("\n2. ASCII 艺术验证码:")
    ascii_captcha = gen.generate_ascii_captcha(length=4, difficulty=CaptchaDifficulty.MEDIUM)
    print(f"   答案: {ascii_captcha.text}")
    print("   显示:")
    for line in ascii_captcha.captcha.split('\n'):
        print(f"   {line}")
    
    # 3. 简化版 ASCII 验证码
    print("\n3. 简化版 ASCII 验证码:")
    simple_captcha = gen.generate_ascii_captcha(length=4, simple_style=True, add_noise=False)
    print(f"   答案: {simple_captcha.text}")
    print("   显示:")
    for line in simple_captcha.captcha.split('\n'):
        print(f"   {line}")
    
    # 4. 数学验证码
    print("\n4. 数学验证码:")
    math_captcha = gen.generate_math_captcha()
    print(f"   问题: {math_captcha.question}")
    print(f"   答案: {math_captcha.answer}")
    print("   显示:")
    print(math_captcha.captcha)
    
    # 5. 反序验证码
    print("\n5. 反序验证码:")
    reverse_captcha = gen.generate_reverse_captcha()
    print(f"   显示: {reverse_captcha.captcha}")
    print(f"   正确答案: {reverse_captcha.text}")
    
    # 6. 验证演示
    print("\n6. 验证演示:")
    test_captcha = gen.generate_text_captcha(length=4)
    print(f"   验证码: {test_captcha.text}")
    
    # 正确输入
    correct = test_captcha.verify(test_captcha.text)
    print(f"   输入 '{test_captcha.text}': {correct}")
    
    # 错误输入
    wrong = test_captcha.verify("0000")
    print(f"   输入 '0000': {wrong}")
    
    # 7. 不同难度
    print("\n7. 不同难度验证码:")
    for diff in CaptchaDifficulty:
        captcha = gen.generate_ascii_captcha(difficulty=diff, length=4)
        print(f"\n   难度: {diff.value}")
        print(f"   答案: {captcha.text}")
        print("   显示:")
        for line in captcha.captcha.split('\n')[:5]:
            print(f"   {line}")
    
    print("\n" + "=" * 60)
    print("演示完成")