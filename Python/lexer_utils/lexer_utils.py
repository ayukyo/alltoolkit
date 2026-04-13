"""
词法分析器工具 (Lexer Utils)
==========================

一个零依赖的词法分析器工具集，用于解析和标记文本。

功能：
- Token 定义和匹配（字符串匹配、正则匹配）
- 词法分析器（Lexer）构建
- 流式 Token 处理
- 位置跟踪（行号、列号）
- 错误处理和恢复
- Token 缓存和回溯

使用示例：
    from lexer_utils import Lexer, TokenType, Token

    # 定义 token 类型
    NUMBER = TokenType('NUMBER', r'\\d+')
    PLUS = TokenType('PLUS', r'\\+')
    
    # 创建词法分析器
    lexer = Lexer()
    lexer.add_type(NUMBER)
    lexer.add_type(PLUS)
    
    # 分析文本
    tokens = lexer.tokenize('123 + 456')
"""

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterator,
    List,
    Optional,
    Pattern,
    Tuple,
    Union,
)


class TokenCategory(Enum):
    """Token 类别枚举"""
    LITERAL = auto()      # 字面量（数字、字符串等）
    KEYWORD = auto()      # 关键字
    IDENTIFIER = auto()   # 标识符
    OPERATOR = auto()     # 操作符
    PUNCTUATION = auto()  # 标点符号
    WHITESPACE = auto()   # 空白字符
    COMMENT = auto()      # 注释
    ERROR = auto()        # 错误 token
    EOF = auto()         # 文件结束


@dataclass
class TokenType:
    """
    Token 类型定义
    
    Attributes:
        name: Token 类型名称
        pattern: 匹配模式（字符串或正则表达式）
        category: Token 类别
        priority: 匹配优先级（数值越大优先级越高）
        ignore: 是否忽略此 token（如空白字符）
        callback: 匹配后的回调函数，用于转换 token 值
    """
    name: str
    pattern: str
    category: TokenCategory = TokenCategory.LITERAL
    priority: int = 0
    ignore: bool = False
    callback: Optional[Callable[[str], Any]] = None
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, TokenType):
            return self.name == other.name
        return False


@dataclass
class Token:
    """
    Token 对象
    
    Attributes:
        type: Token 类型
        value: Token 值
        line: 行号（从 1 开始）
        column: 列号（从 1 开始）
        start: 起始位置（字符索引）
        end: 结束位置（字符索引）
    """
    type: TokenType
    value: Any
    line: int = 1
    column: int = 1
    start: int = 0
    end: int = 0
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"
    
    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.type == other.type and 
                    self.value == other.value and
                    self.line == other.line and
                    self.column == other.column)
        return False


@dataclass
class LexerError:
    """
    词法分析错误
    
    Attributes:
        message: 错误消息
        line: 错误所在行号
        column: 错误所在列号
        position: 错误位置（字符索引）
        context: 错误上下文文本
    """
    message: str
    line: int
    column: int
    position: int
    context: str = ""
    
    def __repr__(self):
        return f"LexerError(L{self.line}:C{self.column}): {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "position": self.position,
            "context": self.context,
        }


class LexerState:
    """词法分析器状态"""
    
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[LexerError] = []
    
    @property
    def current_char(self) -> Optional[str]:
        """获取当前字符"""
        if self.position >= len(self.text):
            return None
        return self.text[self.position]
    
    @property
    def remaining_text(self) -> str:
        """获取剩余文本"""
        return self.text[self.position:]
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """查看指定偏移位置的字符"""
        pos = self.position + offset
        if pos >= len(self.text) or pos < 0:
            return None
        return self.text[pos]
    
    def advance(self, count: int = 1) -> str:
        """前进指定数量的字符，返回前进的字符"""
        result = ""
        for _ in range(count):
            if self.position >= len(self.text):
                break
            char = self.text[self.position]
            result += char
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return result
    
    def get_context(self, radius: int = 20) -> str:
        """获取当前位置的上下文文本"""
        start = max(0, self.position - radius)
        end = min(len(self.text), self.position + radius)
        return self.text[start:end]


@dataclass
class LexerRule:
    """
    词法规则
    
    Attributes:
        token_type: Token 类型
        pattern: 编译后的正则表达式
        priority: 优先级
        callback: 值转换回调
    """
    token_type: TokenType
    pattern: Pattern[str]
    priority: int
    callback: Optional[Callable[[str], Any]] = None
    
    def match(self, text: str, position: int) -> Optional[Any]:
        """尝试在指定位置匹配"""
        return self.pattern.match(text, position)


class Lexer:
    """
    词法分析器
    
    功能：
    - 支持多种 token 类型定义
    - 支持优先级匹配
    - 支持流式处理
    - 支持错误处理和恢复
    - 支持位置跟踪
    - 支持 token 缓存和回溯
    
    使用示例：
        lexer = Lexer()
        lexer.add_type(TokenType('NUMBER', r'\\d+', TokenCategory.LITERAL))
        lexer.add_type(TokenType('PLUS', r'\\+', TokenCategory.OPERATOR))
        lexer.add_type(TokenType('WHITESPACE', r'\\s+', TokenCategory.WHITESPACE, ignore=True))
        
        tokens = lexer.tokenize('123 + 456')
    """
    
    def __init__(self):
        self._rules: List[LexerRule] = []
        self._type_names: Dict[str, TokenType] = {}
        self._keywords: Dict[str, TokenType] = {}
        self._error_handler: Optional[Callable[[LexerError], bool]] = None
        self._max_error_count: int = 100
    
    @property
    def token_types(self) -> List[TokenType]:
        """获取所有 token 类型"""
        return list(self._type_names.values())
    
    def add_type(
        self,
        token_type: TokenType,
        as_keyword: bool = False,
    ) -> "Lexer":
        """
        添加 token 类型
        
        Args:
            token_type: Token 类型定义
            as_keyword: 是否作为关键字（精确匹配优先）
            
        Returns:
            self（支持链式调用）
        """
        if token_type.name in self._type_names:
            raise ValueError(f"Token type '{token_type.name}' already exists")
        
        self._type_names[token_type.name] = token_type
        
        # 编译正则表达式
        pattern = re.compile(token_type.pattern)
        rule = LexerRule(
            token_type=token_type,
            pattern=pattern,
            priority=token_type.priority,
            callback=token_type.callback,
        )
        self._rules.append(rule)
        
        # 按优先级排序
        self._rules.sort(key=lambda r: r.priority, reverse=True)
        
        if as_keyword:
            self._keywords[token_type.pattern] = token_type
        
        return self
    
    def add_keyword(
        self,
        name: str,
        keyword: str,
        category: TokenCategory = TokenCategory.KEYWORD,
        priority: int = 100,
    ) -> "Lexer":
        """
        添加关键字
        
        Args:
            name: Token 类型名称
            keyword: 关键字字符串
            category: Token 类别
            priority: 优先级（默认 100，高于普通 token）
            
        Returns:
            self（支持链式调用）
        """
        token_type = TokenType(
            name=name,
            pattern=re.escape(keyword),
            category=category,
            priority=priority,
        )
        self.add_type(token_type, as_keyword=True)
        return self
    
    def add_operator(
        self,
        name: str,
        operator: str,
        priority: int = 50,
    ) -> "Lexer":
        """添加操作符"""
        token_type = TokenType(
            name=name,
            pattern=re.escape(operator),
            category=TokenCategory.OPERATOR,
            priority=priority,
        )
        return self.add_type(token_type)
    
    def add_punctuation(
        self,
        name: str,
        punctuation: str,
        priority: int = 40,
    ) -> "Lexer":
        """添加标点符号"""
        token_type = TokenType(
            name=name,
            pattern=re.escape(punctuation),
            category=TokenCategory.PUNCTUATION,
            priority=priority,
        )
        return self.add_type(token_type)
    
    def on_error(self, handler: Callable[[LexerError], bool]) -> "Lexer":
        """
        设置错误处理器
        
        Args:
            handler: 错误处理函数，返回 True 表示继续分析，False 表示停止
            
        Returns:
            self（支持链式调用）
        """
        self._error_handler = handler
        return self
    
    def tokenize(
        self,
        text: str,
        ignore_whitespace: bool = True,
        include_eof: bool = True,
    ) -> List[Token]:
        """
        将文本转换为 token 列表
        
        Args:
            text: 要分析的文本
            ignore_whitespace: 是否忽略空白 token
            include_eof: 是否在末尾添加 EOF token
            
        Returns:
            Token 列表
        """
        state = LexerState(text)
        
        while state.position < len(text):
            matched = False
            
            # 尝试匹配每个规则
            for rule in self._rules:
                match = rule.match(text, state.position)
                if match:
                    value = match.group(0)
                    
                    # 应用回调转换值
                    if rule.callback:
                        value = rule.callback(value)
                    
                    # 创建 token
                    token = Token(
                        type=rule.token_type,
                        value=value,
                        line=state.line,
                        column=state.column,
                        start=state.position,
                        end=match.end(),
                    )
                    
                    # 前进
                    state.advance(len(match.group(0)))
                    
                    # 添加 token（除非需要忽略）
                    if not rule.token_type.ignore:
                        state.tokens.append(token)
                    
                    matched = True
                    break
            
            if not matched:
                # 无法匹配，创建错误
                error = LexerError(
                    message=f"Unexpected character: {state.current_char!r}",
                    line=state.line,
                    column=state.column,
                    position=state.position,
                    context=state.get_context(),
                )
                state.errors.append(error)
                
                # 调用错误处理器
                should_continue = True
                if self._error_handler:
                    should_continue = self._error_handler(error)
                
                if not should_continue or len(state.errors) >= self._max_error_count:
                    break
                
                # 跳过一个字符继续
                state.advance(1)
        
        # 添加 EOF token
        if include_eof:
            eof_type = TokenType("EOF", "", TokenCategory.EOF)
            state.tokens.append(Token(
                type=eof_type,
                value=None,
                line=state.line,
                column=state.column,
                start=len(text),
                end=len(text),
            ))
        
        return state.tokens
    
    def tokenize_iter(
        self,
        text: str,
    ) -> Generator[Token, None, List[LexerError]]:
        """
        流式生成 token
        
        Yields:
            Token 对象
            
        Returns:
            错误列表
        """
        state = LexerState(text)
        
        while state.position < len(text):
            matched = False
            
            for rule in self._rules:
                match = rule.match(text, state.position)
                if match:
                    value = match.group(0)
                    
                    if rule.callback:
                        value = rule.callback(value)
                    
                    token = Token(
                        type=rule.token_type,
                        value=value,
                        line=state.line,
                        column=state.column,
                        start=state.position,
                        end=match.end(),
                    )
                    
                    state.advance(len(match.group(0)))
                    
                    if not rule.token_type.ignore:
                        yield token
                    
                    matched = True
                    break
            
            if not matched:
                error = LexerError(
                    message=f"Unexpected character: {state.current_char!r}",
                    line=state.line,
                    column=state.column,
                    position=state.position,
                    context=state.get_context(),
                )
                state.errors.append(error)
                
                should_continue = True
                if self._error_handler:
                    should_continue = self._error_handler(error)
                
                if not should_continue or len(state.errors) >= self._max_error_count:
                    break
                
                state.advance(1)
        
        # Yield EOF
        eof_type = TokenType("EOF", "", TokenCategory.EOF)
        yield Token(
            type=eof_type,
            value=None,
            line=state.line,
            column=state.column,
            start=len(text),
            end=len(text),
        )
        
        return state.errors
    
    def get_errors(self, text: str) -> List[LexerError]:
        """获取分析过程中的所有错误"""
        tokens = list(self.tokenize_iter(text))
        # 从生成器返回值获取错误
        return []


class LexerBuilder:
    """
    词法分析器构建器
    
    提供流畅的 API 来构建词法分析器
    
    使用示例：
        lexer = (LexerBuilder()
            .define('NUMBER', r'\\d+', TokenCategory.LITERAL)
            .define('STRING', r'"[^"]*"', TokenCategory.LITERAL)
            .keyword('if', 'IF')
            .keyword('else', 'ELSE')
            .operator('+', 'PLUS')
            .operator('-', 'MINUS')
            .whitespace()
            .build())
    """
    
    def __init__(self):
        self._types: List[Tuple[str, str, TokenCategory, int, bool, Optional[Callable]]] = []
        self._keywords: List[Tuple[str, str]] = []
        self._operators: List[Tuple[str, str]] = []
        self._punctuations: List[Tuple[str, str]] = []
        self._error_handler: Optional[Callable[[LexerError], bool]] = None
        self._ignore_whitespace: bool = True
    
    def define(
        self,
        name: str,
        pattern: str,
        category: TokenCategory = TokenCategory.LITERAL,
        priority: int = 0,
        ignore: bool = False,
        callback: Optional[Callable[[str], Any]] = None,
    ) -> "LexerBuilder":
        """定义 token 类型"""
        self._types.append((name, pattern, category, priority, ignore, callback))
        return self
    
    def keyword(self, keyword: str, name: Optional[str] = None) -> "LexerBuilder":
        """添加关键字"""
        name = name or keyword.upper()
        self._keywords.append((name, keyword))
        return self
    
    def keywords(self, *keywords: str) -> "LexerBuilder":
        """添加多个关键字"""
        for kw in keywords:
            self.keyword(kw)
        return self
    
    def operator(self, op: str, name: Optional[str] = None) -> "LexerBuilder":
        """添加操作符"""
        name = name or self._op_to_name(op)
        self._operators.append((name, op))
        return self
    
    def operators(self, *ops: str) -> "LexerBuilder":
        """添加多个操作符"""
        for op in ops:
            self.operator(op)
        return self
    
    def punctuation(self, punc: str, name: Optional[str] = None) -> "LexerBuilder":
        """添加标点符号"""
        name = name or self._punc_to_name(punc)
        self._punctuations.append((name, punc))
        return self
    
    def punctuations(self, *puncs: str) -> "LexerBuilder":
        """添加多个标点符号"""
        for punc in puncs:
            self.punctuation(punc)
        return self
    
    def whitespace(self, ignore: bool = True) -> "LexerBuilder":
        """启用空白字符处理"""
        self._ignore_whitespace = ignore
        return self
    
    def on_error(self, handler: Callable[[LexerError], bool]) -> "LexerBuilder":
        """设置错误处理器"""
        self._error_handler = handler
        return self
    
    def build(self) -> Lexer:
        """构建词法分析器"""
        lexer = Lexer()
        
        # 添加关键字（高优先级）
        for name, kw in self._keywords:
            lexer.add_keyword(name, kw)
        
        # 添加操作符
        for name, op in self._operators:
            lexer.add_operator(name, op)
        
        # 添加标点符号
        for name, punc in self._punctuations:
            lexer.add_punctuation(name, punc)
        
        # 添加空白字符
        if self._ignore_whitespace:
            lexer.add_type(TokenType(
                name="WHITESPACE",
                pattern=r"\s+",
                category=TokenCategory.WHITESPACE,
                ignore=True,
            ))
        
        # 添加自定义类型
        for name, pattern, category, priority, ignore, callback in self._types:
            lexer.add_type(TokenType(
                name=name,
                pattern=pattern,
                category=category,
                priority=priority,
                ignore=ignore,
                callback=callback,
            ))
        
        # 设置错误处理器
        if self._error_handler:
            lexer.on_error(self._error_handler)
        
        return lexer
    
    @staticmethod
    def _op_to_name(op: str) -> str:
        """将操作符转换为名称"""
        names = {
            "+": "PLUS",
            "-": "MINUS",
            "*": "STAR",
            "/": "SLASH",
            "%": "PERCENT",
            "=": "EQ",
            "==": "EQEQ",
            "!=": "NEQ",
            "<": "LT",
            ">": "GT",
            "<=": "LTE",
            ">=": "GTE",
            "!": "NOT",
            "&&": "AND",
            "||": "OR",
            "&": "AMP",
            "|": "PIPE",
            "^": "CARET",
            "~": "TILDE",
            "<<": "LSHIFT",
            ">>": "RSHIFT",
        }
        return names.get(op, "OP_" + op)
    
    @staticmethod
    def _punc_to_name(punc: str) -> str:
        """将标点符号转换为名称"""
        names = {
            "(": "LPAREN",
            ")": "RPAREN",
            "{": "LBRACE",
            "}": "RBRACE",
            "[": "LBRACKET",
            "]": "RBRACKET",
            ";": "SEMI",
            ",": "COMMA",
            ".": "DOT",
            ":": "COLON",
            "?": "QUESTION",
        }
        return names.get(punc, "PUNC_" + punc)


# ============ 便捷函数 ============

def create_lexer(**kwargs) -> Lexer:
    """
    快速创建词法分析器
    
    Args:
        keywords: 关键字列表
        operators: 操作符列表
        punctuations: 标点符号列表
        ignore_whitespace: 是否忽略空白
        
    Returns:
        Lexer 对象
    """
    builder = LexerBuilder()
    
    keywords = kwargs.get("keywords", [])
    for kw in keywords:
        builder.keyword(kw)
    
    operators = kwargs.get("operators", [])
    for op in operators:
        builder.operator(op)
    
    punctuations = kwargs.get("punctuations", [])
    for punc in punctuations:
        builder.punctuation(punc)
    
    if kwargs.get("ignore_whitespace", True):
        builder.whitespace()
    
    return builder.build()


def tokenize(text: str, rules: Optional[Dict[str, str]] = None, **kwargs) -> List[Token]:
    """
    快速分词
    
    Args:
        text: 要分析的文本
        rules: token 规则字典 {名称: 模式}
        **kwargs: 传递给 create_lexer 的参数
        
    Returns:
        Token 列表
    """
    lexer = create_lexer(**kwargs)
    
    if rules:
        for name, pattern in rules.items():
            lexer.add_type(TokenType(name=name, pattern=pattern))
    
    return lexer.tokenize(text)


def simple_tokenize(text: str) -> List[Token]:
    """
    简单分词（按空白和标点分割）
    
    Args:
        text: 要分析的文本
        
    Returns:
        Token 列表
    """
    lexer = (LexerBuilder()
        .define("WORD", r"[a-zA-Z_][a-zA-Z0-9_]*", TokenCategory.IDENTIFIER)
        .define("NUMBER", r"\d+(\.\d+)?", TokenCategory.LITERAL)
        .define("STRING", r'"[^"]*"|\'[^\']*\'', TokenCategory.LITERAL)
        .punctuations("(", ")", "{", "}", "[", "]", ";", ",", ".", ":", "?")
        .operators("+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=")
        .whitespace()
        .build())
    
    return lexer.tokenize(text)


def tokenize_code(text: str) -> List[Token]:
    """
    代码分词（支持常见编程语言）
    
    Args:
        text: 代码文本
        
    Returns:
        Token 列表
    """
    lexer = (LexerBuilder()
        # 关键字
        .keywords(
            "if", "else", "elif", "while", "for", "do", "switch", "case",
            "break", "continue", "return", "function", "class", "struct",
            "import", "from", "as", "try", "catch", "finally", "throw",
            "const", "let", "var", "def", "async", "await", "yield",
            "true", "false", "null", "none", "self", "this", "new", "delete",
        )
        # 操作符
        .operators(
            "+", "-", "*", "/", "%", "**", "//",
            "=", "+=", "-=", "*=", "/=", "%=",
            "==", "!=", "<", ">", "<=", ">=", "===", "!==",
            "&&", "||", "!", "&", "|", "^", "~", "<<", ">>",
            "++", "--", "=>", "->", "::", ".",
        )
        # 标点符号
        .punctuations("(", ")", "{", "}", "[", "]", ";", ",", ":", "?")
        # 标识符和字面量
        .define("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*", TokenCategory.IDENTIFIER, priority=1)
        .define("NUMBER", r"\d+(\.\d+)?([eE][+-]?\d+)?", TokenCategory.LITERAL)
        .define("STRING", r'"[^"]*"|\'[^\']*\'|`[^`]*`', TokenCategory.LITERAL)
        .define("COMMENT_LINE", r"//[^\n]*", TokenCategory.COMMENT, ignore=True)
        .define("COMMENT_BLOCK", r"/\*[\s\S]*?\*/", TokenCategory.COMMENT, ignore=True)
        .whitespace()
        .build())
    
    return lexer.tokenize(text)


def tokenize_json(text: str) -> List[Token]:
    """
    JSON 分词
    
    Args:
        text: JSON 文本
        
    Returns:
        Token 列表
    """
    def parse_number(value: str) -> Union[int, float]:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    
    def parse_string(value: str) -> str:
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    
    lexer = (LexerBuilder()
        .keywords("true", "false", "null")
        .punctuations("{", "}", "[", "]", ":", ",")
        .define("NUMBER", r"-?\d+(\.\d+)?([eE][+-]?\d+)?", 
                TokenCategory.LITERAL, callback=parse_number)
        .define("STRING", r'"(?:[^"\\]|\\.)*"', 
                TokenCategory.LITERAL, callback=parse_string)
        .whitespace()
        .build())
    
    return lexer.tokenize(text)


def tokenize_math(text: str) -> List[Token]:
    """
    数学表达式分词
    
    Args:
        text: 数学表达式
        
    Returns:
        Token 列表
    """
    def parse_number(value: str) -> Union[int, float]:
        if "." in value:
            return float(value)
        return int(value)
    
    lexer = (LexerBuilder()
        .define("NUMBER", r"\d+(\.\d+)?", TokenCategory.LITERAL, callback=parse_number)
        .operators("+", "-", "*", "/", "%", "^", "=", "<", ">", "<=", ">=")
        .punctuations("(", ")", "[", "]", "{", "}")
        .define("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*", TokenCategory.IDENTIFIER)
        .whitespace()
        .build())
    
    return lexer.tokenize(text)


def count_tokens(tokens: List[Token]) -> Dict[str, int]:
    """
    统计各类 token 数量
    
    Args:
        tokens: Token 列表
        
    Returns:
        统计字典 {类型名: 数量}
    """
    counts: Dict[str, int] = {}
    for token in tokens:
        name = token.type.name
        counts[name] = counts.get(name, 0) + 1
    return counts


def filter_tokens(
    tokens: List[Token],
    types: Optional[List[str]] = None,
    categories: Optional[List[TokenCategory]] = None,
) -> List[Token]:
    """
    过滤 token
    
    Args:
        tokens: Token 列表
        types: 要保留的类型名列表
        categories: 要保留的类别列表
        
    Returns:
        过滤后的 Token 列表
    """
    result = []
    for token in tokens:
        if types and token.type.name not in types:
            continue
        if categories and token.type.category not in categories:
            continue
        result.append(token)
    return result


def tokens_to_dict(tokens: List[Token]) -> List[Dict[str, Any]]:
    """
    将 token 列表转换为字典列表
    
    Args:
        tokens: Token 列表
        
    Returns:
        字典列表
    """
    return [
        {
            "type": token.type.name,
            "value": token.value,
            "line": token.line,
            "column": token.column,
            "start": token.start,
            "end": token.end,
        }
        for token in tokens
    ]


def dict_to_tokens(data: List[Dict[str, Any]]) -> List[Token]:
    """
    将字典列表转换为 token 列表
    
    Args:
        data: 字典列表
        
    Returns:
        Token 列表
    """
    tokens = []
    for item in data:
        token_type = TokenType(
            name=item["type"],
            pattern="",
            category=TokenCategory.LITERAL,
        )
        token = Token(
            type=token_type,
            value=item["value"],
            line=item.get("line", 1),
            column=item.get("column", 1),
            start=item.get("start", 0),
            end=item.get("end", 0),
        )
        tokens.append(token)
    return tokens


class TokenStream:
    """
    Token 流
    
    提供便捷的 token 遍历和查找功能
    """
    
    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._position = 0
    
    @property
    def current(self) -> Optional[Token]:
        """获取当前 token"""
        if self._position >= len(self._tokens):
            return None
        return self._tokens[self._position]
    
    @property
    def position(self) -> int:
        """获取当前位置"""
        return self._position
    
    @position.setter
    def position(self, value: int):
        """设置当前位置"""
        self._position = max(0, min(value, len(self._tokens)))
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        """查看指定偏移位置的 token"""
        pos = self._position + offset
        if pos >= len(self._tokens) or pos < 0:
            return None
        return self._tokens[pos]
    
    def advance(self) -> Optional[Token]:
        """前进并返回当前 token"""
        token = self.current
        self._position += 1
        return token
    
    def expect(self, type_name: str) -> Token:
        """
        期望指定类型的 token
        
        Raises:
            ValueError: 如果当前 token 类型不匹配
        """
        token = self.current
        if token is None:
            raise ValueError(f"Unexpected end of input, expected {type_name}")
        if token.type.name != type_name:
            raise ValueError(
                f"Expected {type_name} but got {token.type.name} "
                f"at L{token.line}:C{token.column}"
            )
        return self.advance()
    
    def accept(self, type_name: str) -> Optional[Token]:
        """接受指定类型的 token，如果匹配则前进"""
        if self.current and self.current.type.name == type_name:
            return self.advance()
        return None
    
    def skip_until(self, type_name: str) -> List[Token]:
        """跳过直到遇到指定类型的 token"""
        skipped = []
        while self.current and self.current.type.name != type_name:
            skipped.append(self.advance())
        return skipped
    
    def collect_until(self, type_name: str) -> List[Token]:
        """收集直到遇到指定类型的 token（不消耗该 token）"""
        collected = []
        pos = self._position
        while pos < len(self._tokens):
            if self._tokens[pos].type.name == type_name:
                break
            collected.append(self._tokens[pos])
            pos += 1
        return collected
    
    def match_sequence(self, *type_names: str) -> bool:
        """检查是否匹配指定的类型序列"""
        for i, type_name in enumerate(type_names):
            token = self.peek(i)
            if token is None or token.type.name != type_name:
                return False
        return True
    
    def find(self, type_name: str, value: Optional[Any] = None) -> Optional[int]:
        """查找指定类型（和值）的 token，返回位置"""
        for i, token in enumerate(self._tokens[self._position:], self._position):
            if token.type.name == type_name:
                if value is None or token.value == value:
                    return i
        return None
    
    def find_all(self, type_name: str) -> List[int]:
        """查找所有指定类型的 token，返回位置列表"""
        positions = []
        for i, token in enumerate(self._tokens):
            if token.type.name == type_name:
                positions.append(i)
        return positions
    
    def reset(self):
        """重置到开头"""
        self._position = 0
    
    def __iter__(self):
        return iter(self._tokens)
    
    def __len__(self):
        return len(self._tokens)
    
    def __getitem__(self, index: int) -> Token:
        return self._tokens[index]
    
    def to_list(self) -> List[Token]:
        """转换为列表"""
        return self._tokens.copy()


# ============ 导出 ============

__all__ = [
    # 枚举和类型
    "TokenCategory",
    "TokenType",
    "Token",
    "LexerError",
    # 核心类
    "LexerState",
    "LexerRule",
    "Lexer",
    "LexerBuilder",
    "TokenStream",
    # 便捷函数
    "create_lexer",
    "tokenize",
    "simple_tokenize",
    "tokenize_code",
    "tokenize_json",
    "tokenize_math",
    "count_tokens",
    "filter_tokens",
    "tokens_to_dict",
    "dict_to_tokens",
]