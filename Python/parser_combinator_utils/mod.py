"""
Parser Combinator Utils - 解析器组合子工具库

一个零外部依赖的解析器组合子库，用于构建各种解析器。
支持字符解析、字符串解析、数字解析、组合子操作等。

功能特点:
- 基础解析器: char, string, digit, letter, whitespace 等
- 组合子: sequence, choice, many, many1, optional, sep_by 等
- 映射和绑定: map, bind, then, skip
- 解析结果: Success, Failure 类型
- 支持回溯和错误信息

使用示例:
    from parser_combinator_utils import Parser, char, string, many, digit
    
    # 解析一个数字
    number = many1(digit()).map(lambda cs: int(''.join(cs)))
    result = number.parse("123")  # Success(123)
"""

from dataclasses import dataclass
from typing import (
    Any, Callable, Generic, List, Optional, Tuple, TypeVar, Union
)
from functools import wraps
import re

# 类型变量
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


@dataclass
class ParseResult(Generic[T]):
    """解析结果基类"""
    pass


@dataclass
class Success(ParseResult[T]):
    """解析成功"""
    value: T
    remaining: str
    position: int = 0
    
    def is_success(self) -> bool:
        return True
    
    def is_failure(self) -> bool:
        return False
    
    def get_value(self) -> T:
        return self.value
    
    def get_error(self) -> str:
        raise ValueError("Success has no error")
    
    def map(self, f: Callable[[T], U]) -> 'Success[U]':
        return Success(f(self.value), self.remaining, self.position)
    
    def __repr__(self) -> str:
        return f"Success({self.value!r}, remaining={self.remaining!r})"


@dataclass
class Failure(ParseResult[T]):
    """解析失败"""
    error: str
    position: int = 0
    expected: Optional[str] = None
    
    def is_success(self) -> bool:
        return False
    
    def is_failure(self) -> bool:
        return True
    
    def get_value(self) -> T:
        raise ValueError(f"Parse failed: {self.error}")
    
    def get_error(self) -> str:
        return self.error
    
    def map(self, f: Callable[[T], U]) -> 'Failure[U]':
        return Failure(self.error, self.position, self.expected)
    
    def __repr__(self) -> str:
        return f"Failure({self.error!r}, position={self.position})"


class Parser(Generic[T]):
    """
    解析器类 - 核心解析器类型
    
    所有解析器都是 Parser 的实例，可以组合使用。
    """
    
    def __init__(self, parse_func: Callable[[str, int], ParseResult[T]]):
        """
        初始化解析器
        
        Args:
            parse_func: 解析函数，接受输入字符串和位置，返回解析结果
        """
        self._parse = parse_func
    
    def parse(self, input_str: str, position: int = 0) -> ParseResult[T]:
        """
        解析输入字符串
        
        Args:
            input_str: 输入字符串
            position: 起始位置
            
        Returns:
            解析结果
        """
        return self._parse(input_str, position)
    
    def parse_all(self, input_str: str) -> ParseResult[T]:
        """
        解析整个输入字符串，要求完全消费
        
        Args:
            input_str: 输入字符串
            
        Returns:
            解析结果，如果输入未完全消费则返回失败
        """
        result = self._parse(input_str, 0)
        if result.is_success():
            if result.remaining:
                return Failure(
                    f"Expected end of input but got {result.remaining!r}",
                    position=len(input_str) - len(result.remaining)
                )
        return result
    
    def map(self, f: Callable[[T], U]) -> 'Parser[U]':
        """
        映射解析结果
        
        Args:
            f: 映射函数
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[U]:
            result = self._parse(input_str, pos)
            if result.is_success():
                try:
                    return Success(f(result.value), result.remaining, result.position)
                except Exception as e:
                    return Failure(str(e), pos)
            return result.map(f)
        return Parser(parse_func)
    
    def bind(self, f: Callable[[T], 'Parser[U]']) -> 'Parser[U]':
        """
        绑定解析器（flatMap）
        
        Args:
            f: 绑定函数
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[U]:
            result = self._parse(input_str, pos)
            if result.is_success():
                next_parser = f(result.value)
                return next_parser._parse(input_str, result.position)
            return Failure(result.error, result.position, result.expected)
        return Parser(parse_func)
    
    def then(self, other: 'Parser[U]') -> 'Parser[U]':
        """
        顺序解析，丢弃第一个结果，保留第二个
        
        Args:
            other: 第二个解析器
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[U]:
            result = self._parse(input_str, pos)
            if result.is_success():
                return other._parse(input_str, result.position)
            return Failure(result.error, result.position, result.expected)
        return Parser(parse_func)
    
    def skip(self, other: 'Parser[U]') -> 'Parser[T]':
        """
        顺序解析，保留第一个结果，丢弃第二个
        
        Args:
            other: 第二个解析器
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[T]:
            result1 = self._parse(input_str, pos)
            if result1.is_success():
                result2 = other._parse(input_str, result1.position)
                if result2.is_success():
                    return Success(result1.value, result2.remaining, result2.position)
                return Failure(result2.error, result2.position, result2.expected)
            return Failure(result1.error, result1.position, result1.expected)
        return Parser(parse_func)
    
    def or_else(self, other: 'Parser[T]') -> 'Parser[T]':
        """
        选择解析，如果第一个失败则尝试第二个
        
        Args:
            other: 备选解析器
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[T]:
            result = self._parse(input_str, pos)
            if result.is_success():
                return result
            return other._parse(input_str, pos)
        return Parser(parse_func)
    
    def many(self) -> 'Parser[List[T]]':
        """
        重复解析零次或多次
        
        Returns:
            新的解析器，返回结果列表
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[List[T]]:
            values = []
            current_pos = pos
            while True:
                result = self._parse(input_str, current_pos)
                if result.is_success():
                    values.append(result.value)
                    current_pos = result.position
                else:
                    break
            return Success(values, input_str[current_pos:], current_pos)
        return Parser(parse_func)
    
    def many1(self) -> 'Parser[List[T]]':
        """
        重复解析一次或多次
        
        Returns:
            新的解析器，返回结果列表
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[List[T]]:
            first = self._parse(input_str, pos)
            if first.is_failure():
                return Failure(first.error, first.position, first.expected)
            
            values = [first.value]
            current_pos = first.position
            
            while True:
                result = self._parse(input_str, current_pos)
                if result.is_success():
                    values.append(result.value)
                    current_pos = result.position
                else:
                    break
            
            return Success(values, input_str[current_pos:], current_pos)
        return Parser(parse_func)
    
    def optional(self) -> 'Parser[Optional[T]]':
        """
        可选解析，失败时返回 None
        
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[Optional[T]]:
            result = self._parse(input_str, pos)
            if result.is_success():
                return Success(result.value, result.remaining, result.position)
            return Success(None, input_str[pos:], pos)
        return Parser(parse_func)
    
    def sep_by(self, sep: 'Parser[Any]') -> 'Parser[List[T]]':
        """
        用分隔符分隔的重复解析
        
        Args:
            sep: 分隔符解析器
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[List[T]]:
            first = self._parse(input_str, pos)
            if first.is_failure():
                return Success([], input_str[pos:], pos)
            
            values = [first.value]
            current_pos = first.position
            
            while True:
                sep_result = sep._parse(input_str, current_pos)
                if sep_result.is_failure():
                    break
                
                item_result = self._parse(input_str, sep_result.position)
                if item_result.is_failure():
                    break
                
                values.append(item_result.value)
                current_pos = item_result.position
            
            return Success(values, input_str[current_pos:], current_pos)
        return Parser(parse_func)
    
    def sep_by1(self, sep: 'Parser[Any]') -> 'Parser[List[T]]':
        """
        用分隔符分隔的重复解析（至少一个）
        
        Args:
            sep: 分隔符解析器
            
        Returns:
            新的解析器
        """
        def parse_func(input_str: str, pos: int) -> ParseResult[List[T]]:
            first = self._parse(input_str, pos)
            if first.is_failure():
                return Failure(first.error, first.position, first.expected)
            
            values = [first.value]
            current_pos = first.position
            
            while True:
                sep_result = sep._parse(input_str, current_pos)
                if sep_result.is_failure():
                    break
                
                item_result = self._parse(input_str, sep_result.position)
                if item_result.is_failure():
                    break
                
                values.append(item_result.value)
                current_pos = item_result.position
            
            return Success(values, input_str[current_pos:], current_pos)
        return Parser(parse_func)
    
    def between(self, left: 'Parser[Any]', right: 'Parser[Any]') -> 'Parser[T]':
        """
        在两个解析器之间解析
        
        Args:
            left: 左侧解析器
            right: 右侧解析器
            
        Returns:
            新的解析器
        """
        return left.then(self).skip(right)
    
    def __or__(self, other: 'Parser[T]') -> 'Parser[T]':
        """支持 | 运算符"""
        return self.or_else(other)
    
    def __rshift__(self, other: 'Parser[U]') -> 'Parser[U]':
        """支持 >> 运算符 (then)"""
        return self.then(other)
    
    def __lshift__(self, other: 'Parser[U]') -> 'Parser[T]':
        """支持 << 运算符 (skip)"""
        return self.skip(other)


# ==================== 基础解析器 ====================

def char(c: str) -> Parser[str]:
    """
    解析单个字符
    
    Args:
        c: 要匹配的字符
        
    Returns:
        解析器
    """
    if len(c) != 1:
        raise ValueError("char() expects a single character")
    
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if pos < len(input_str):
            if input_str[pos] == c:
                return Success(c, input_str[pos+1:], pos + 1)
        return Failure(f"Expected {c!r}", pos, c)
    return Parser(parse_func)


def string(s: str) -> Parser[str]:
    """
    解析字符串
    
    Args:
        s: 要匹配的字符串
        
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if input_str[pos:pos+len(s)] == s:
            return Success(s, input_str[pos+len(s):], pos + len(s))
        return Failure(f"Expected {s!r}", pos, s)
    return Parser(parse_func)


def satisfy(predicate: Callable[[str], bool], description: str = "character") -> Parser[str]:
    """
    解析满足条件的字符
    
    Args:
        predicate: 条件函数
        description: 描述信息
        
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if pos < len(input_str):
            c = input_str[pos]
            if predicate(c):
                return Success(c, input_str[pos+1:], pos + 1)
        return Failure(f"Expected {description}", pos, description)
    return Parser(parse_func)


def digit() -> Parser[str]:
    """解析数字字符 (0-9)"""
    return satisfy(lambda c: c.isdigit(), "digit")


def letter() -> Parser[str]:
    """解析字母字符 (a-z, A-Z)"""
    return satisfy(lambda c: c.isalpha(), "letter")


def alphanumeric() -> Parser[str]:
    """解析字母数字字符"""
    return satisfy(lambda c: c.isalnum(), "alphanumeric")


def whitespace() -> Parser[str]:
    """解析空白字符"""
    return satisfy(lambda c: c.isspace(), "whitespace")


def spaces() -> Parser[str]:
    """解析零个或多个空白字符，返回合并的字符串"""
    return whitespace().many().map(lambda cs: ''.join(cs))


def spaces1() -> Parser[str]:
    """解析一个或多个空白字符，返回合并的字符串"""
    return whitespace().many1().map(lambda cs: ''.join(cs))


def newline() -> Parser[str]:
    """解析换行符"""
    return satisfy(lambda c: c == '\n' or c == '\r', "newline")


def tab() -> Parser[str]:
    """解析制表符"""
    return satisfy(lambda c: c == '\t', "tab")


def any_char() -> Parser[str]:
    """解析任意字符"""
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if pos < len(input_str):
            return Success(input_str[pos], input_str[pos+1:], pos + 1)
        return Failure("Expected any character", pos, "any char")
    return Parser(parse_func)


def none_of(chars: str) -> Parser[str]:
    """
    解析不在给定集合中的字符
    
    Args:
        chars: 禁止字符集合
        
    Returns:
        解析器
    """
    return satisfy(lambda c: c not in chars, f"character not in {chars!r}")


def one_of(chars: str) -> Parser[str]:
    """
    解析给定集合中的字符
    
    Args:
        chars: 允许字符集合
        
    Returns:
        解析器
    """
    return satisfy(lambda c: c in chars, f"character in {chars!r}")


# ==================== 组合子 ====================

def sequence(*parsers: Parser[Any]) -> Parser[List[Any]]:
    """
    顺序解析多个解析器
    
    Args:
        *parsers: 解析器序列
        
    Returns:
        解析器，返回结果列表
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[List[Any]]:
        values = []
        current_pos = pos
        for parser in parsers:
            result = parser._parse(input_str, current_pos)
            if result.is_failure():
                return Failure(result.error, result.position, result.expected)
            values.append(result.value)
            current_pos = result.position
        return Success(values, input_str[current_pos:], current_pos)
    return Parser(parse_func)


def choice(*parsers: Parser[T]) -> Parser[T]:
    """
    选择解析，尝试多个解析器直到成功
    
    Args:
        *parsers: 解析器序列
        
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[T]:
        errors = []
        for parser in parsers:
            result = parser._parse(input_str, pos)
            if result.is_success():
                return result
            errors.append(result.error)
        return Failure(f"All choices failed: {'; '.join(errors)}", pos)
    return Parser(parse_func)


def optional(parser: Parser[T]) -> Parser[Optional[T]]:
    """
    可选解析
    
    Args:
        parser: 解析器
        
    Returns:
        解析器，失败时返回 None
    """
    return parser.optional()


def many(parser: Parser[T]) -> Parser[List[T]]:
    """
    重复解析零次或多次
    
    Args:
        parser: 解析器
        
    Returns:
        解析器
    """
    return parser.many()


def many1(parser: Parser[T]) -> Parser[List[T]]:
    """
    重复解析一次或多次
    
    Args:
        parser: 解析器
        
    Returns:
        解析器
    """
    return parser.many1()


def sep_by(parser: Parser[T], sep: Parser[Any]) -> Parser[List[T]]:
    """
    用分隔符分隔的重复解析
    
    Args:
        parser: 元素解析器
        sep: 分隔符解析器
        
    Returns:
        解析器
    """
    return parser.sep_by(sep)


def sep_by1(parser: Parser[T], sep: Parser[Any]) -> Parser[List[T]]:
    """
    用分隔符分隔的重复解析（至少一个）
    
    Args:
        parser: 元素解析器
        sep: 分隔符解析器
        
    Returns:
        解析器
    """
    return parser.sep_by1(sep)


def between(left: Parser[Any], parser: Parser[T], right: Parser[Any]) -> Parser[T]:
    """
    在两个解析器之间解析
    
    Args:
        left: 左侧解析器
        parser: 主解析器
        right: 右侧解析器
        
    Returns:
        解析器
    """
    return parser.between(left, right)


def lazy(parser_factory: Callable[[], Parser[T]]) -> Parser[T]:
    """
    延迟解析器，用于递归定义
    
    Args:
        parser_factory: 返回解析器的函数
        
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[T]:
        return parser_factory()._parse(input_str, pos)
    return Parser(parse_func)


def eof() -> Parser[None]:
    """
    解析结束标记
    
    Returns:
        解析器，成功时返回 None
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[None]:
        if pos >= len(input_str):
            return Success(None, "", pos)
        return Failure("Expected end of input", pos, "EOF")
    return Parser(parse_func)


# ==================== 高级解析器 ====================

def regex(pattern: str) -> Parser[str]:
    """
    使用正则表达式解析
    
    Args:
        pattern: 正则表达式模式
        
    Returns:
        解析器
    """
    compiled = re.compile(pattern)
    
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        match = compiled.match(input_str, pos)
        if match:
            return Success(match.group(), input_str[match.end():], match.end())
        return Failure(f"Expected pattern /{pattern}/", pos, pattern)
    return Parser(parse_func)


def integer() -> Parser[int]:
    """
    解析整数
    
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[int]:
        if pos >= len(input_str):
            return Failure("Expected integer", pos, "integer")
        
        # 检查负号
        negative = False
        if input_str[pos] == '-':
            negative = True
            pos += 1
        elif input_str[pos] == '+':
            pos += 1
        
        if pos >= len(input_str) or not input_str[pos].isdigit():
            return Failure("Expected integer", pos, "integer")
        
        start = pos
        while pos < len(input_str) and input_str[pos].isdigit():
            pos += 1
        
        num_str = input_str[start:pos]
        value = int(num_str) if not negative else -int(num_str)
        return Success(value, input_str[pos:], pos)
    
    return Parser(parse_func)


def float_num() -> Parser[float]:
    """
    解析浮点数
    
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[float]:
        if pos >= len(input_str):
            return Failure("Expected float", pos, "float")
        
        start = pos
        
        # 检查正负号
        if input_str[pos] in '+-':
            pos += 1
        
        # 整数部分
        while pos < len(input_str) and input_str[pos].isdigit():
            pos += 1
        
        # 小数部分
        if pos < len(input_str) and input_str[pos] == '.':
            pos += 1
            while pos < len(input_str) and input_str[pos].isdigit():
                pos += 1
        
        # 科学计数法
        if pos < len(input_str) and input_str[pos].lower() == 'e':
            pos += 1
            if pos < len(input_str) and input_str[pos] in '+-':
                pos += 1
            while pos < len(input_str) and input_str[pos].isdigit():
                pos += 1
        
        if pos == start:
            return Failure("Expected float", start, "float")
        
        try:
            value = float(input_str[start:pos])
            return Success(value, input_str[pos:], pos)
        except ValueError:
            return Failure("Invalid float", start, "float")
    
    return Parser(parse_func)


def quoted_string(quote_char: str = '"', escape_char: str = '\\') -> Parser[str]:
    """
    解析带引号的字符串
    
    Args:
        quote_char: 引号字符
        escape_char: 转义字符
        
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if pos >= len(input_str) or input_str[pos] != quote_char:
            return Failure(f"Expected {quote_char!r}", pos, quote_char)
        
        pos += 1
        chars = []
        
        while pos < len(input_str):
            c = input_str[pos]
            
            if c == escape_char and pos + 1 < len(input_str):
                # 转义字符
                pos += 1
                next_c = input_str[pos]
                if next_c == 'n':
                    chars.append('\n')
                elif next_c == 't':
                    chars.append('\t')
                elif next_c == 'r':
                    chars.append('\r')
                elif next_c == '\\':
                    chars.append('\\')
                elif next_c == quote_char:
                    chars.append(quote_char)
                else:
                    chars.append(next_c)
                pos += 1
            
            elif c == quote_char:
                return Success(''.join(chars), input_str[pos+1:], pos + 1)
            
            else:
                chars.append(c)
                pos += 1
        
        return Failure("Unterminated string", pos, "end of string")
    
    return Parser(parse_func)


def identifier() -> Parser[str]:
    """
    解析标识符 (字母或下划线开头，后跟字母数字或下划线)
    
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if pos >= len(input_str):
            return Failure("Expected identifier", pos, "identifier")
        
        c = input_str[pos]
        if not (c.isalpha() or c == '_'):
            return Failure("Expected identifier", pos, "identifier")
        
        start = pos
        pos += 1
        
        while pos < len(input_str):
            c = input_str[pos]
            if not (c.isalnum() or c == '_'):
                break
            pos += 1
        
        return Success(input_str[start:pos], input_str[pos:], pos)
    
    return Parser(parse_func)


def keyword(kw: str) -> Parser[str]:
    """
    解析关键字（确保后面不是标识符字符）
    
    Args:
        kw: 关键字
        
    Returns:
        解析器
    """
    def parse_func(input_str: str, pos: int) -> ParseResult[str]:
        if input_str[pos:pos+len(kw)] == kw:
            # 检查后面是否有标识符字符
            next_pos = pos + len(kw)
            if next_pos >= len(input_str) or not (input_str[next_pos].isalnum() or input_str[next_pos] == '_'):
                return Success(kw, input_str[next_pos:], next_pos)
        return Failure(f"Expected keyword {kw!r}", pos, kw)
    
    return Parser(parse_func)


# ==================== 工具函数 ====================

def run_parser(parser: Parser[T], input_str: str) -> ParseResult[T]:
    """
    运行解析器
    
    Args:
        parser: 解析器
        input_str: 输入字符串
        
    Returns:
        解析结果
    """
    return parser.parse_all(input_str)


def parse_or_error(parser: Parser[T], input_str: str) -> T:
    """
    解析输入，失败时抛出异常
    
    Args:
        parser: 解析器
        input_str: 输入字符串
        
    Returns:
        解析结果值
        
    Raises:
        ValueError: 解析失败时
    """
    result = parser.parse_all(input_str)
    if result.is_success():
        return result.value
    raise ValueError(f"Parse error: {result.error}")


# ==================== 预定义解析器 ====================

# 常用解析器
digit_parser = digit()
letter_parser = letter()
alphanumeric_parser = alphanumeric()
whitespace_parser = whitespace()
spaces_parser = spaces()
spaces1_parser = spaces1()
integer_parser = integer()
float_parser = float_num()
identifier_parser = identifier()

# 数字解析器
digits = many1(digit()).map(lambda cs: ''.join(cs))
letters = many1(letter()).map(lambda cs: ''.join(cs))
alphanumerics = many1(alphanumeric()).map(lambda cs: ''.join(cs))


# ==================== JSON 解析器示例 ====================

def json_parser() -> Parser[Any]:
    """
    创建 JSON 解析器
    
    Returns:
        JSON 解析器
    """
    # 延迟定义以支持递归
    def json_value() -> Parser[Any]:
        return choice(
            json_null(),
            json_bool(),
            json_number(),
            json_string(),
            json_array(),
            json_object()
        )
    
    def json_null() -> Parser[None]:
        return keyword("null").map(lambda _: None)
    
    def json_bool() -> Parser[bool]:
        return choice(
            keyword("true").map(lambda _: True),
            keyword("false").map(lambda _: False)
        )
    
    def json_number() -> Parser[Union[int, float]]:
        return choice(float_num(), integer())
    
    def json_string() -> Parser[str]:
        return quoted_string('"')
    
    def json_array() -> Parser[List[Any]]:
        def parse_func(input_str: str, pos: int) -> ParseResult[List[Any]]:
            # 跳过空白和 [
            ws = spaces_parser._parse(input_str, pos)
            if ws.is_failure():
                return ws
            
            pos = ws.position
            if pos >= len(input_str) or input_str[pos] != '[':
                return Failure("Expected '['", pos, "[")
            pos += 1
            
            # 跳过空白
            ws = spaces_parser._parse(input_str, pos)
            pos = ws.position
            
            # 空数组
            if input_str[pos:pos+1] == ']':
                return Success([], input_str[pos+1:], pos + 1)
            
            # 解析元素
            values = []
            while True:
                # 解析值
                result = json_value()._parse(input_str, pos)
                if result.is_failure():
                    return result
                values.append(result.value)
                pos = result.position
                
                # 跳过空白
                ws = spaces_parser._parse(input_str, pos)
                pos = ws.position
                
                # 检查逗号或结束
                if pos >= len(input_str):
                    return Failure("Expected ',' or ']'", pos)
                if input_str[pos] == ']':
                    return Success(values, input_str[pos+1:], pos + 1)
                if input_str[pos] != ',':
                    return Failure("Expected ',' or ']'", pos)
                pos += 1
                
                # 跳过空白
                ws = spaces_parser._parse(input_str, pos)
                pos = ws.position
        
        return Parser(parse_func)
    
    def json_object() -> Parser[dict]:
        def parse_func(input_str: str, pos: int) -> ParseResult[dict]:
            # 跳过空白和 {
            ws = spaces_parser._parse(input_str, pos)
            if ws.is_failure():
                return ws
            
            pos = ws.position
            if pos >= len(input_str) or input_str[pos] != '{':
                return Failure("Expected '{'", pos, "{")
            pos += 1
            
            # 跳过空白
            ws = spaces_parser._parse(input_str, pos)
            pos = ws.position
            
            # 空对象
            if input_str[pos:pos+1] == '}':
                return Success({}, input_str[pos+1:], pos + 1)
            
            # 解析键值对
            obj = {}
            while True:
                # 解析键
                key_result = json_string()._parse(input_str, pos)
                if key_result.is_failure():
                    return key_result
                key = key_result.value
                pos = key_result.position
                
                # 跳过空白
                ws = spaces_parser._parse(input_str, pos)
                pos = ws.position
                
                # 解析冒号
                if pos >= len(input_str) or input_str[pos] != ':':
                    return Failure("Expected ':'", pos)
                pos += 1
                
                # 跳过空白
                ws = spaces_parser._parse(input_str, pos)
                pos = ws.position
                
                # 解析值
                value_result = json_value()._parse(input_str, pos)
                if value_result.is_failure():
                    return value_result
                obj[key] = value_result.value
                pos = value_result.position
                
                # 跳过空白
                ws = spaces_parser._parse(input_str, pos)
                pos = ws.position
                
                # 检查逗号或结束
                if pos >= len(input_str):
                    return Failure("Expected ',' or '}'", pos)
                if input_str[pos] == '}':
                    return Success(obj, input_str[pos+1:], pos + 1)
                if input_str[pos] != ',':
                    return Failure("Expected ',' or '}'", pos)
                pos += 1
                
                # 跳过空白
                ws = spaces_parser._parse(input_str, pos)
                pos = ws.position
        
        return Parser(parse_func)
    
    return json_value()


# 预编译的 JSON 解析器
_json_parser_instance = None

def parse_json(input_str: str) -> ParseResult[Any]:
    """
    解析 JSON 字符串
    
    Args:
        input_str: JSON 字符串
        
    Returns:
        解析结果
    """
    global _json_parser_instance
    if _json_parser_instance is None:
        _json_parser_instance = json_parser()
    return _json_parser_instance.parse_all(input_str)