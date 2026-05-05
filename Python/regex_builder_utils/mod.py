# -*- coding: utf-8 -*-
"""
AllToolkit - Regex Builder Utilities 🔨

零依赖正则表达式构建器，通过流畅 API 构建复杂正则表达式，无需掌握正则语法。

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import re
from typing import List, Optional, Union, Tuple, Pattern, Callable, Any, Match


def _is_regex_pattern(s: str) -> bool:
    """判断字符串是否是已形成的正则模式（如 \\w, \\d, [a-z] 等）"""
    # 以反斜杠开头的特殊字符类（如 \d, \w, \s, \D, \W, \S, \b, \B）
    if s.startswith('\\') and len(s) <= 4:
        return True
    # 字符类
    if s.startswith('[') and s.endswith(']'):
        return True
    # 已经是组
    if s.startswith('(') and s.endswith(')'):
        return True
    # 单个特殊字符
    if s in ('.', '^', '$'):
        return True
    # 已经包含转义字符的模式
    if '\\' in s:
        return True
    return False


def _wrap_pattern(pattern: str) -> str:
    """智能包装模式：如果是纯文本则转义，如果已是正则则直接使用"""
    if _is_regex_pattern(pattern):
        return pattern
    return re.escape(pattern)


class RegexBuilder:
    """
    正则表达式构建器 - 流畅 API 构建正则表达式
    
    示例:
        # 构建邮箱正则
        pattern = (RegexBuilder()
            .start()
            .one_or_more(RegexBuilder.CHAR_CLASS.word)
            .literal('@')
            .one_or_more(RegexBuilder.CHAR_CLASS.word)
            .literal('.')
            .min_max(2, 4, RegexBuilder.CHAR_CLASS.word)
            .end()
            .build())
    """
    
    # 字符类常量
    class CHAR_CLASS:
        """字符类快捷方式"""
        DIGIT = r'\d'
        NON_DIGIT = r'\D'
        WORD = r'\w'
        NON_WORD = r'\W'
        WHITESPACE = r'\s'
        NON_WHITESPACE = r'\S'
        ANY = '.'
        WORD_BOUNDARY = r'\b'
        NON_WORD_BOUNDARY = r'\B'
    
    # 锚点常量
    class ANCHOR:
        """锚点"""
        START = '^'
        END = '$'
        START_OF_STRING = r'\A'
        END_OF_STRING = r'\z'
        END_OF_STRING_BEFORE_NEWLINE = r'\Z'
    
    def __init__(self):
        """初始化构建器"""
        self._parts: List[str] = []
        self._flags: int = 0
        self._group_counter: int = 0
    
    # =========================================================================
    # 字符匹配
    # =========================================================================
    
    def literal(self, text: str) -> 'RegexBuilder':
        """
        匹配字面文本（自动转义特殊字符）
        
        Args:
            text: 要匹配的字面文本
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().literal('hello').build()  # 'hello'
            RegexBuilder().literal('1+1=2').build()  # '1\\+1=2'
        """
        self._parts.append(re.escape(text))
        return self
    
    def char(self, char: str) -> 'RegexBuilder':
        """
        匹配单个字符
        
        Args:
            char: 单个字符
            
        Returns:
            构建器实例
        """
        if len(char) != 1:
            raise ValueError("char() 只接受单个字符")
        self._parts.append(re.escape(char))
        return self
    
    def char_class(self, *chars: str) -> 'RegexBuilder':
        """
        匹配字符类中的任意一个字符
        
        Args:
            *chars: 字符类中的字符
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().char_class('a', 'b', 'c').build()  # '[abc]'
        """
        chars_str = ''.join(re.escape(c) if c not in '-]^\\' else '\\' + c for c in chars)
        self._parts.append(f'[{chars_str}]')
        return self
    
    def char_range(self, start: str, end: str) -> 'RegexBuilder':
        """
        匹配字符范围
        
        Args:
            start: 起始字符
            end: 结束字符
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().char_range('a', 'z').build()  # '[a-z]'
            RegexBuilder().char_range('0', '9').build()  # '[0-9]'
        """
        if len(start) != 1 or len(end) != 1:
            raise ValueError("char_range() 只接受单个字符")
        self._parts.append(f'[{start}-{end}]')
        return self
    
    def char_ranges(self, *ranges: Tuple[str, str]) -> 'RegexBuilder':
        """
        匹配多个字符范围
        
        Args:
            *ranges: 字符范围元组
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().char_ranges(('a', 'z'), ('A', 'Z')).build()  # '[a-zA-Z]'
        """
        ranges_str = ''.join(f'{r[0]}-{r[1]}' for r in ranges)
        self._parts.append(f'[{ranges_str}]')
        return self
    
    def negated_char_class(self, *chars: str) -> 'RegexBuilder':
        """
        匹配不在字符类中的任意字符
        
        Args:
            *chars: 排除的字符
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().negated_char_class('a', 'b', 'c').build()  # '[^abc]'
        """
        chars_str = ''.join(re.escape(c) if c not in '-]^\\' else '\\' + c for c in chars)
        self._parts.append(f'[^{chars_str}]')
        return self
    
    def any_char(self) -> 'RegexBuilder':
        """匹配任意字符（除换行符）"""
        self._parts.append('.')
        return self
    
    def digit(self) -> 'RegexBuilder':
        """匹配数字字符"""
        self._parts.append(r'\d')
        return self
    
    def non_digit(self) -> 'RegexBuilder':
        """匹配非数字字符"""
        self._parts.append(r'\D')
        return self
    
    def word_char(self) -> 'RegexBuilder':
        """匹配单词字符 [a-zA-Z0-9_]"""
        self._parts.append(r'\w')
        return self
    
    def non_word_char(self) -> 'RegexBuilder':
        """匹配非单词字符"""
        self._parts.append(r'\W')
        return self
    
    def whitespace(self) -> 'RegexBuilder':
        """匹配空白字符"""
        self._parts.append(r'\s')
        return self
    
    def non_whitespace(self) -> 'RegexBuilder':
        """匹配非空白字符"""
        self._parts.append(r'\S')
        return self
    
    def any_of(self, *patterns: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        匹配多个模式中的任意一个（或）
        
        Args:
            *patterns: 可选的模式
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().any_of('cat', 'dog', 'bird').build()  # '(?:cat|dog|bird)'
        """
        parts = []
        for p in patterns:
            if isinstance(p, RegexBuilder):
                parts.append(p.build())
            else:
                parts.append(p)
        self._parts.append(f'(?:{"|".join(parts)})')
        return self
    
    # =========================================================================
    # 量词
    # =========================================================================
    
    def optional(self, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配零次或一次
        
        Args:
            pattern: 可选的模式，如果为 None 则对前一个元素应用
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().literal('color').optional('u').build()  # 'color(?:u)?'
        """
        if pattern is None:
            self._parts.append('?')
        else:
            if isinstance(pattern, RegexBuilder):
                p = pattern.build()
            else:
                # 如果是单个字母/字符，不转义；如果是正则模式，保持原样
                p = pattern if len(pattern) == 1 and pattern.isalnum() else _wrap_pattern(pattern)
            self._parts.append(f'(?:{p})?')
        return self
    
    def zero_or_more(self, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配零次或多次
        
        Args:
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        if pattern is None:
            self._parts.append('*')
        else:
            if isinstance(pattern, RegexBuilder):
                p = pattern.build()
            else:
                p = re.escape(pattern)
            self._parts.append(f'(?:{p})*')
        return self
    
    def one_or_more(self, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配一次或多次
        
        Args:
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        if pattern is None:
            self._parts.append('+')
        else:
            if isinstance(pattern, RegexBuilder):
                p = pattern.build()
            else:
                p = re.escape(pattern)
            self._parts.append(f'(?:{p})+')
        return self
    
    def exactly(self, n: int, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配恰好 n 次
        
        Args:
            n: 重复次数
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        if pattern is None:
            self._parts.append(f'{{{n}}}')
        else:
            if isinstance(pattern, RegexBuilder):
                p = pattern.build()
            else:
                p = pattern  # 不再转义，直接使用
            self._parts.append(f'(?:{p}){{{n}}}')
        return self
    
    def min_times(self, min_count: int, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配至少 n 次
        
        Args:
            min_count: 最小重复次数
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        if pattern is None:
            self._parts.append(f'{{{min_count},}}')
        else:
            if isinstance(pattern, RegexBuilder):
                self._parts.append(f'(?:{pattern.build()}){{{min_count},}}')
            else:
                self._parts.append(f'(?:{re.escape(pattern)}){{{min_count},}}')
        return self
    
    def max_times(self, max_count: int, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配最多 n 次
        
        Args:
            max_count: 最大重复次数
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        if pattern is None:
            self._parts.append(f'{{0,{max_count}}}')
        else:
            if isinstance(pattern, RegexBuilder):
                self._parts.append(f'(?:{pattern.build()}){{0,{max_count}}}')
            else:
                self._parts.append(f'(?:{re.escape(pattern)}){{0,{max_count}}}')
        return self
    
    def min_max(self, min_count: int, max_count: int, pattern: Optional[Union[str, 'RegexBuilder']] = None) -> 'RegexBuilder':
        """
        匹配 n 到 m 次
        
        Args:
            min_count: 最小重复次数
            max_count: 最大重复次数
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        if pattern is None:
            self._parts.append(f'{{{min_count},{max_count}}}')
        else:
            if isinstance(pattern, RegexBuilder):
                self._parts.append(f'(?:{pattern.build()}){{{min_count},{max_count}}}')
            else:
                self._parts.append(f'(?:{re.escape(pattern)}){{{min_count},{max_count}}}')
        return self
    
    def lazy(self) -> 'RegexBuilder':
        """
        使量词变为懒惰模式（非贪婪）
        
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().zero_or_more().lazy()  # '*?'
        """
        self._parts.append('?')
        return self
    
    def possessive(self) -> 'RegexBuilder':
        """
        使量词变为占有模式
        
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().one_or_more().possessive()  # '+'
        """
        self._parts.append('+')
        return self
    
    # =========================================================================
    # 锚点
    # =========================================================================
    
    def start(self) -> 'RegexBuilder':
        """匹配字符串开头 ^"""
        self._parts.append('^')
        return self
    
    def end(self) -> 'RegexBuilder':
        """匹配字符串结尾 $"""
        self._parts.append('$')
        return self
    
    def word_boundary(self) -> 'RegexBuilder':
        """匹配单词边界"""
        self._parts.append(r'\b')
        return self
    
    def non_word_boundary(self) -> 'RegexBuilder':
        """匹配非单词边界"""
        self._parts.append(r'\B')
        return self
    
    def start_of_string(self) -> 'RegexBuilder':
        """匹配字符串绝对开头 \\A"""
        self._parts.append(r'\A')
        return self
    
    def end_of_string(self) -> 'RegexBuilder':
        """匹配字符串绝对结尾 \\Z"""
        self._parts.append(r'\Z')
        return self
    
    # =========================================================================
    # 分组
    # =========================================================================
    
    def group(self, pattern: Union[str, 'RegexBuilder'], name: Optional[str] = None) -> 'RegexBuilder':
        """
        创建捕获组
        
        Args:
            pattern: 组内的模式
            name: 可选的组名
            
        Returns:
            构建器实例
            
        示例:
            RegexBuilder().group(r'\d+', 'year').build()  # '(?P<year>\\d+)'
        """
        if isinstance(pattern, RegexBuilder):
            inner = pattern.build()
        else:
            inner = pattern
        
        if name:
            self._parts.append(f'(?P<{name}>{inner})')
            self._group_counter += 1
        else:
            self._parts.append(f'({inner})')
            self._group_counter += 1
        return self
    
    def non_capturing_group(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        创建非捕获组
        
        Args:
            pattern: 组内的模式
            
        Returns:
            构建器实例
        """
        if isinstance(pattern, RegexBuilder):
            inner = pattern.build()
        else:
            inner = pattern
        self._parts.append(f'(?:{inner})')
        return self
    
    def backreference(self, group: Union[int, str]) -> 'RegexBuilder':
        """
        引用之前的捕获组
        
        Args:
            group: 组号或组名
            
        Returns:
            构建器实例
        """
        if isinstance(group, int):
            self._parts.append(f'\\{group}')
        else:
            self._parts.append(f'(?P={group})')
        return self
    
    # =========================================================================
    # 前瞻和后顾断言
    # =========================================================================
    
    def lookahead(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        正向前瞻断言 - 匹配后面跟着 pattern 的位置
        
        Args:
            pattern: 断言模式
            
        Returns:
            构建器实例
            
        示例:
            # 匹配后面跟着数字的字母
            RegexBuilder().word_char().one_or_more().lookahead(r'\d').build()
        """
        if isinstance(pattern, RegexBuilder):
            inner = pattern.build()
        else:
            inner = pattern
        self._parts.append(f'(?={inner})')
        return self
    
    def negative_lookahead(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        负向前瞻断言 - 匹配后面不跟着 pattern 的位置
        
        Args:
            pattern: 断言模式
            
        Returns:
            构建器实例
        """
        if isinstance(pattern, RegexBuilder):
            inner = pattern.build()
        else:
            inner = pattern
        self._parts.append(f'(?!{inner})')
        return self
    
    def lookbehind(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        正向后顾断言 - 匹配前面是 pattern 的位置
        
        Args:
            pattern: 断言模式
            
        Returns:
            构建器实例
        """
        if isinstance(pattern, RegexBuilder):
            inner = pattern.build()
        else:
            inner = pattern
        self._parts.append(f'(?<={inner})')
        return self
    
    def negative_lookbehind(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        负向后顾断言 - 匹配前面不是 pattern 的位置
        
        Args:
            pattern: 断言模式
            
        Returns:
            构建器实例
        """
        if isinstance(pattern, RegexBuilder):
            inner = pattern.build()
        else:
            inner = pattern
        self._parts.append(f'(?<!{inner})')
        return self
    
    # =========================================================================
    # 条件分支
    # =========================================================================
    
    def either(self, *patterns: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        匹配多个模式中的任意一个（同 any_of）
        
        Args:
            *patterns: 可选的模式
            
        Returns:
            构建器实例
        """
        return self.any_of(*patterns)
    
    # =========================================================================
    # 标志/修饰符
    # =========================================================================
    
    def ignore_case(self) -> 'RegexBuilder':
        """设置忽略大小写标志 (re.IGNORECASE)"""
        self._flags |= re.IGNORECASE
        return self
    
    def multiline(self) -> 'RegexBuilder':
        """设置多行模式标志 (re.MULTILINE)"""
        self._flags |= re.MULTILINE
        return self
    
    def dotall(self) -> 'RegexBuilder':
        """设置 dotall 标志，使 . 匹配换行符 (re.DOTALL)"""
        self._flags |= re.DOTALL
        return self
    
    def verbose(self) -> 'RegexBuilder':
        """设置 verbose 标志，允许注释和空白 (re.VERBOSE)"""
        self._flags |= re.VERBOSE
        return self
    
    def ascii_only(self) -> 'RegexBuilder':
        """设置 ASCII 标志，使 \\w, \\b, \\d 等只匹配 ASCII"""
        self._flags |= re.ASCII
        return self
    
    # =========================================================================
    # 常用模式快捷方法
    # =========================================================================
    
    def email(self) -> 'RegexBuilder':
        """添加简单邮箱模式"""
        self._parts.append(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        return self
    
    def url(self) -> 'RegexBuilder':
        """添加 URL 模式"""
        self._parts.append(r'https?://[^\s]+')
        return self
    
    def phone_cn(self) -> 'RegexBuilder':
        """添加中国手机号模式"""
        self._parts.append(r'1[3-9]\d{9}')
        return self
    
    def ipv4(self) -> 'RegexBuilder':
        """添加 IPv4 地址模式"""
        self._parts.append(r'(?:\d{1,3}\.){3}\d{1,3}')
        return self
    
    def date_iso(self) -> 'RegexBuilder':
        """添加 ISO 日期模式 (YYYY-MM-DD)"""
        self._parts.append(r'\d{4}-\d{2}-\d{2}')
        return self
    
    def time_24h(self) -> 'RegexBuilder':
        """添加 24 小时制时间模式"""
        self._parts.append(r'[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?')
        return self
    
    def uuid(self) -> 'RegexBuilder':
        """添加 UUID 模式"""
        self._parts.append(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
        return self
    
    def hex_color(self) -> 'RegexBuilder':
        """添加十六进制颜色模式"""
        self._parts.append(r'#[0-9a-fA-F]{3,6}')
        return self
    
    def chinese(self) -> 'RegexBuilder':
        """添加中文字符模式"""
        self._parts.append(r'[\u4e00-\u9fa5]')
        return self
    
    # =========================================================================
    # 组合操作
    # =========================================================================
    
    def then(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        添加后续模式（语义化方法名）
        
        Args:
            pattern: 要添加的模式
            
        Returns:
            构建器实例
        """
        if isinstance(pattern, RegexBuilder):
            self._parts.append(pattern.build())
        else:
            self._parts.append(pattern)
        return self
    
    def maybe(self, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        可选模式（零次或一次）
        
        Args:
            pattern: 可选的模式
            
        Returns:
            构建器实例
        """
        return self.optional(pattern)
    
    def repeat(self, count: int, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        重复模式指定次数
        
        Args:
            count: 重复次数
            pattern: 要重复的模式
            
        Returns:
            构建器实例
        """
        return self.exactly(count, pattern)
    
    def wrap(self, left: str, right: str, pattern: Union[str, 'RegexBuilder']) -> 'RegexBuilder':
        """
        用左右分隔符包裹模式
        
        Args:
            left: 左分隔符
            right: 右分隔符
            pattern: 要包裹的模式
            
        Returns:
            构建器实例
        """
        self.literal(left)
        if isinstance(pattern, RegexBuilder):
            self._parts.append(pattern.build())
        else:
            self._parts.append(pattern)
        self.literal(right)
        return self
    
    def quote(self, pattern: Union[str, 'RegexBuilder'], quote_char: str = '"') -> 'RegexBuilder':
        """
        用引号包裹模式
        
        Args:
            pattern: 要包裹的模式
            quote_char: 引号字符，默认为双引号
            
        Returns:
            构建器实例
        """
        return self.wrap(quote_char, quote_char, pattern)
    
    # =========================================================================
    # 构建和测试
    # =========================================================================
    
    def build(self) -> str:
        """
        构建正则表达式字符串
        
        Returns:
            正则表达式字符串
        """
        return ''.join(self._parts)
    
    def compile(self) -> Pattern:
        """
        编译为正则表达式对象
        
        Returns:
            编译后的 re.Pattern 对象
        """
        return re.compile(self.build(), self._flags)
    
    def test(self, text: str) -> bool:
        """
        测试文本是否匹配
        
        Args:
            text: 要测试的文本
            
        Returns:
            是否匹配
        """
        return bool(self.compile().search(text))
    
    def match(self, text: str) -> Optional[Match]:
        """
        匹配文本
        
        Args:
            text: 要匹配的文本
            
        Returns:
            匹配对象或 None
        """
        return self.compile().search(text)
    
    def find_all(self, text: str) -> List[str]:
        """
        查找所有匹配
        
        Args:
            text: 要搜索的文本
            
        Returns:
            所有匹配的列表
        """
        return self.compile().findall(text)
    
    def replace(self, text: str, replacement: str) -> str:
        """
        替换所有匹配
        
        Args:
            text: 原文本
            replacement: 替换字符串
            
        Returns:
            替换后的文本
        """
        return self.compile().sub(replacement, text)
    
    def split(self, text: str) -> List[str]:
        """
        按匹配分割文本
        
        Args:
            text: 要分割的文本
            
        Returns:
            分割后的列表
        """
        return self.compile().split(text)
    
    def __str__(self) -> str:
        return self.build()
    
    def __repr__(self) -> str:
        return f"RegexBuilder('{self.build()}')"


# =============================================================================
# 快捷函数
# =============================================================================

def builder() -> RegexBuilder:
    """
    创建新的正则表达式构建器
    
    Returns:
        新的 RegexBuilder 实例
        
    示例:
        pattern = builder().literal('hello').one_or_more().build()
    """
    return RegexBuilder()


def email_pattern() -> str:
    """返回简单邮箱正则模式"""
    return (RegexBuilder()
        .word_char().one_or_more()
        .literal('@')
        .word_char().one_or_more()
        .literal('.')
        .word_char().min_max(2, 4)
        .build())


def phone_cn_pattern() -> str:
    """返回中国手机号正则模式"""
    return (RegexBuilder()
        .literal('1')
        .char_class(*'3456789')
        .digit().exactly(9)
        .build())


def url_pattern() -> str:
    """返回 URL 正则模式"""
    return (RegexBuilder()
        .literal('http')
        .optional('s')
        .literal('://')
        .non_whitespace().one_or_more()
        .build())


def ipv4_pattern() -> str:
    """返回 IPv4 地址正则模式"""
    octet = (RegexBuilder()
        .either(
            RegexBuilder().char_range('0', '9').build(),
            RegexBuilder().char_range('1', '9').char_range('0', '9').build(),
            RegexBuilder().literal('1').char_range('0', '9').exactly(2, RegexBuilder.CHAR_CLASS.DIGIT).build(),
            RegexBuilder().literal('2').either(
                RegexBuilder().char_range('0', '4').char_range('0', '9').build(),
                RegexBuilder().literal('5').char_range('0', '5').build()
            ).build()
        ).build())
    
    return (RegexBuilder()
        .non_capturing_group(octet)
        .literal('.')
        .non_capturing_group(octet)
        .literal('.')
        .non_capturing_group(octet)
        .literal('.')
        .non_capturing_group(octet)
        .build())


def date_pattern(fmt: str = 'iso') -> str:
    """
    返回日期正则模式
    
    Args:
        fmt: 日期格式，支持 'iso' (YYYY-MM-DD), 'cn' (YYYY年MM月DD日)
        
    Returns:
        日期正则模式
    """
    builder = RegexBuilder()
    
    if fmt == 'iso':
        return (builder
            .exactly(4, RegexBuilder.CHAR_CLASS.DIGIT)
            .literal('-')
            .min_max(1, 2, RegexBuilder.CHAR_CLASS.DIGIT)
            .literal('-')
            .min_max(1, 2, RegexBuilder.CHAR_CLASS.DIGIT)
            .build())
    elif fmt == 'cn':
        return (builder
            .exactly(4, RegexBuilder.CHAR_CLASS.DIGIT)
            .literal('年')
            .min_max(1, 2, RegexBuilder.CHAR_CLASS.DIGIT)
            .literal('月')
            .min_max(1, 2, RegexBuilder.CHAR_CLASS.DIGIT)
            .literal('日')
            .build())
    else:
        raise ValueError(f"不支持的日期格式: {fmt}")


def time_pattern(fmt: str = '24h') -> str:
    """
    返回时间正则模式
    
    Args:
        fmt: 时间格式，支持 '24h', '12h'
        
    Returns:
        时间正则模式
    """
    builder = RegexBuilder()
    
    if fmt == '24h':
        return (builder
            .non_capturing_group(
                RegexBuilder().either(
                    RegexBuilder().char_range('0', '1').char_range('0', '9').build(),
                    RegexBuilder().literal('2').char_range('0', '3').build()
                ).build()
            )
            .literal(':')
            .non_capturing_group(
                RegexBuilder().char_range('0', '5').char_range('0', '9').build()
            )
            .optional(
                RegexBuilder().literal(':').non_capturing_group(
                    RegexBuilder().char_range('0', '5').char_range('0', '9').build()
                ).build()
            )
            .build())
    elif fmt == '12h':
        return (builder
            .non_capturing_group(
                RegexBuilder().either(
                    RegexBuilder().literal('0').optional(
                        RegexBuilder().char_range('1', '9').build()
                    ).build(),
                    RegexBuilder().literal('1').char_range('0', '2').build()
                ).build()
            )
            .literal(':')
            .non_capturing_group(
                RegexBuilder().char_range('0', '5').char_range('0', '9').build()
            )
            .optional(
                RegexBuilder().literal(':').non_capturing_group(
                    RegexBuilder().char_range('0', '5').char_range('0', '9').build()
                ).build()
            )
            .whitespace().zero_or_more()
            .non_capturing_group(
                RegexBuilder().either('AM', 'PM', 'am', 'pm').build()
            )
            .build())
    else:
        raise ValueError(f"不支持的时间格式: {fmt}")


def uuid_pattern() -> str:
    """返回 UUID 正则模式"""
    return (RegexBuilder()
        .word_char().exactly(8)
        .literal('-')
        .word_char().exactly(4)
        .literal('-')
        .word_char().exactly(4)
        .literal('-')
        .word_char().exactly(4)
        .literal('-')
        .word_char().exactly(12)
        .build())


def hex_color_pattern(allow_shorthand: bool = True) -> str:
    """
    返回十六进制颜色正则模式
    
    Args:
        allow_shorthand: 是否允许简写形式 (#fff)
        
    Returns:
        十六进制颜色正则模式
    """
    builder = RegexBuilder().literal('#')
    
    if allow_shorthand:
        hex_6 = RegexBuilder().min_max(6, 6, RegexBuilder.CHAR_CLASS.WORD).build()
        hex_3 = RegexBuilder().min_max(3, 3, RegexBuilder.CHAR_CLASS.WORD).build()
        return builder.either(hex_6, hex_3).build()
    else:
        return builder.min_max(6, 6, RegexBuilder.CHAR_CLASS.WORD).build()


def chinese_pattern(min_len: int = 1, max_len: Optional[int] = None) -> str:
    """
    返回中文字符正则模式
    
    Args:
        min_len: 最小长度
        max_len: 最大长度（可选）
        
    Returns:
        中文字符正则模式
    """
    builder = RegexBuilder()
    
    if max_len is not None:
        builder.min_max(min_len, max_len, RegexBuilder().chinese().build())
    else:
        builder.min_times(min_len, RegexBuilder().chinese().build())
    
    return builder.build()


def username_pattern(min_len: int = 3, max_len: int = 20) -> str:
    """
    返回用户名正则模式
    
    Args:
        min_len: 最小长度
        max_len: 最大长度
        
    Returns:
        用户名正则模式
    """
    builder = RegexBuilder()
    
    return (builder
        .char_class(*'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        .min_max(min_len - 1, max_len - 1,
            RegexBuilder().char_ranges(('a', 'z'), ('A', 'Z'), ('0', '9')).literal('_').literal('-').build()
        )
        .build())


def password_pattern(
    min_len: int = 8,
    require_upper: bool = True,
    require_lower: bool = True,
    require_digit: bool = True,
    require_special: bool = False,
    special_chars: str = '@$!%*?&#'
) -> str:
    """
    返回密码正则模式
    
    Args:
        min_len: 最小长度
        require_upper: 是否需要大写字母
        require_lower: 是否需要小写字母
        require_digit: 是否需要数字
        require_special: 是否需要特殊字符
        special_chars: 特殊字符集合
        
    Returns:
        密码正则模式
    """
    builder = RegexBuilder()
    
    # 前瞻断言
    if require_upper:
        builder.lookahead(RegexBuilder().min_times(1, RegexBuilder().char_range('A', 'Z').build()).build())
    if require_lower:
        builder.lookahead(RegexBuilder().min_times(1, RegexBuilder().char_range('a', 'z').build()).build())
    if require_digit:
        builder.lookahead(RegexBuilder().min_times(1, RegexBuilder.CHAR_CLASS.DIGIT).build())
    if require_special:
        builder.lookahead(RegexBuilder().min_times(1, special_chars).build())
    
    # 主匹配
    char_class = RegexBuilder().char_ranges(('a', 'z'), ('A', 'Z'), ('0', '9')).build()
    if require_special:
        char_class = RegexBuilder().literal(char_class[1:-1]).literal(special_chars).build()
        char_class = f'[{char_class}]'
    
    builder.min_times(min_len, char_class)
    
    return builder.build()


def number_pattern(
    allow_negative: bool = True,
    allow_decimal: bool = True,
    decimal_places: Optional[int] = None,
    allow_thousands_sep: bool = False
) -> str:
    """
    返回数字正则模式
    
    Args:
        allow_negative: 是否允许负数
        allow_decimal: 是否允许小数
        decimal_places: 小数位数限制
        allow_thousands_sep: 是否允许千位分隔符
        
    Returns:
        数字正则模式
    """
    builder = RegexBuilder()
    
    # 负号
    if allow_negative:
        builder.optional('-')
    
    # 整数部分
    if allow_thousands_sep:
        builder.literal('1').literal(',').literal('0').literal('0').literal('0')
    else:
        builder.one_or_more(RegexBuilder.CHAR_CLASS.DIGIT)
    
    # 小数部分
    if allow_decimal:
        if decimal_places is not None:
            builder.optional(
                RegexBuilder()
                    .literal('.')
                    .exactly(decimal_places, RegexBuilder.CHAR_CLASS.DIGIT)
                    .build()
            )
        else:
            builder.optional(
                RegexBuilder()
                    .literal('.')
                    .one_or_more(RegexBuilder.CHAR_CLASS.DIGIT)
                    .build()
            )
    
    return builder.build()


def between_delimiters(
    left: str,
    right: str,
    content_pattern: Optional[str] = None,
    allow_nested: bool = False
) -> str:
    """
    返回匹配两个分隔符之间内容的正则模式
    
    Args:
        left: 左分隔符
        right: 右分隔符
        content_pattern: 内容模式（可选）
        allow_nested: 是否允许嵌套
        
    Returns:
        正则模式
    """
    builder = RegexBuilder()
    
    # 左分隔符
    builder.literal(left)
    
    # 内容
    if content_pattern:
        builder.group(content_pattern)
    elif allow_nested:
        # 嵌套匹配较为复杂，使用简单的方式
        builder.group(
            RegexBuilder()
                .zero_or_more(
                    RegexBuilder()
                        .either(
                            RegexBuilder().non_word_char().build(),
                            RegexBuilder().non_capturing_group(left).build(),
                            RegexBuilder().non_capturing_group(right).build()
                        )
                        .build()
                )
                .build()
        )
    else:
        # 非贪婪匹配任意内容
        builder.group(
            RegexBuilder().any_char().zero_or_more().lazy().build()
        )
    
    # 右分隔符
    builder.literal(right)
    
    return builder.build()


def quoted_string(quote_char: str = '"', allow_escape: bool = True) -> str:
    """
    返回引号字符串正则模式
    
    Args:
        quote_char: 引号字符
        allow_escape: 是否允许转义引号
        
    Returns:
        引号字符串正则模式
    """
    builder = RegexBuilder()
    
    builder.literal(quote_char)
    
    if allow_escape:
        # 匹配转义字符或非引号字符
        builder.group(
            RegexBuilder()
                .zero_or_more(
                    RegexBuilder()
                        .either(
                            RegexBuilder().literal('\\').any_char().build(),
                            RegexBuilder().negated_char_class(quote_char, '\\').build()
                        )
                        .build()
                )
                .build()
        )
    else:
        builder.group(
            RegexBuilder().zero_or_more(
                RegexBuilder().negated_char_class(quote_char).build()
            ).build()
        )
    
    builder.literal(quote_char)
    
    return builder.build()


# =============================================================================
# 预定义构建器
# =============================================================================

# 常用字符类快捷构建器
DIGIT = RegexBuilder().digit()
WORD_CHAR = RegexBuilder().word_char()
WHITESPACE = RegexBuilder().whitespace()
ANY_CHAR = RegexBuilder().any_char()


if __name__ == '__main__':
    # 简单测试
    print("=== Regex Builder Utils Demo ===")
    print()
    
    # 示例 1: 构建邮箱模式
    email = (RegexBuilder()
        .start()
        .one_or_more(RegexBuilder.CHAR_CLASS.WORD)
        .literal('@')
        .one_or_more(RegexBuilder.CHAR_CLASS.WORD)
        .literal('.')
        .min_max(2, 4, RegexBuilder.CHAR_CLASS.WORD)
        .end()
        .build())
    print(f"Email pattern: {email}")
    
    # 示例 2: 构建手机号模式
    phone = (RegexBuilder()
        .start()
        .literal('1')
        .char_class(*'3456789')
        .exactly(9, RegexBuilder.CHAR_CLASS.DIGIT)
        .end()
        .build())
    print(f"Phone CN pattern: {phone}")
    
    # 示例 3: 构建带命名的日期模式
    date = (RegexBuilder()
        .start()
        .group(r'\d{4}', 'year')
        .literal('-')
        .group(r'\d{2}', 'month')
        .literal('-')
        .group(r'\d{2}', 'day')
        .end()
        .build())
    print(f"Named date pattern: {date}")
    
    # 示例 4: 使用快捷函数
    print(f"\nQuick patterns:")
    print(f"  Email: {email_pattern()}")
    print(f"  Phone CN: {phone_cn_pattern()}")
    print(f"  URL: {url_pattern()}")
    print(f"  UUID: {uuid_pattern()}")
    print(f"  Hex color: {hex_color_pattern()}")
    print(f"  Date ISO: {date_pattern('iso')}")
    print(f"  Time 24h: {time_pattern('24h')}")