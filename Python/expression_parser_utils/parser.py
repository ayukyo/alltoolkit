"""
Expression Parser - 核心解析器模块

实现一个安全的递归下降解析器，支持：
- 四则运算和幂运算
- 括号
- 变量
- 函数调用
- 比较和逻辑运算
"""

import re
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum, auto


class TokenType(Enum):
    """词法分析器 Token 类型"""
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    MOD = auto()
    FLOOR_DIV = auto()
    EOF = auto()


class Token:
    """词法分析器 Token"""
    def __init__(self, type_: TokenType, value: Any, position: int = 0):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


class ExpressionError(Exception):
    """表达式错误"""
    def __init__(self, message: str, position: int = 0):
        self.message = message
        self.position = position
        super().__init__(f"Position {position}: {message}")


class Lexer:
    """词法分析器"""

    KEYWORDS = {
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'true': TokenType.NUMBER,
        'false': TokenType.NUMBER,
        'True': TokenType.NUMBER,
        'False': TokenType.NUMBER,
    }

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None

    def error(self, message: str):
        raise ExpressionError(message, self.pos)

    def advance(self):
        """前进一个字符"""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self, offset: int = 1) -> Optional[str]:
        """预览字符"""
        peek_pos = self.pos + offset
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self) -> Token:
        """解析数字（整数或浮点数）"""
        start_pos = self.pos
        result = ''

        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        # 处理科学计数法
        if self.current_char and self.current_char.lower() == 'e':
            result += self.current_char
            self.advance()
            if self.current_char and self.current_char in '+-':
                result += self.current_char
                self.advance()
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        try:
            if '.' in result or 'e' in result.lower():
                return Token(TokenType.NUMBER, float(result), start_pos)
            else:
                return Token(TokenType.NUMBER, int(result), start_pos)
        except ValueError:
            self.error(f"Invalid number: {result}")

    def string(self, quote_char: str) -> Token:
        """解析字符串"""
        start_pos = self.pos
        result = ''
        self.advance()  # 跳过起始引号

        while self.current_char and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == quote_char:
                    result += quote_char
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()

        if not self.current_char:
            self.error("Unterminated string")

        self.advance()  # 跳过结束引号
        return Token(TokenType.STRING, result, start_pos)

    def identifier(self) -> Token:
        """解析标识符或关键字"""
        start_pos = self.pos
        result = ''

        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # 检查是否是布尔常量
        if result.lower() in ('true', 'false'):
            return Token(TokenType.NUMBER, result.lower() == 'true', start_pos)

        # 检查关键字
        if result in self.KEYWORDS:
            return Token(self.KEYWORDS[result], result, start_pos)

        return Token(TokenType.IDENTIFIER, result, start_pos)

    def get_next_token(self) -> Token:
        """获取下一个 Token"""
        while self.current_char:
            # 跳过空白
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # 数字
            if self.current_char.isdigit():
                return self.number()

            # 字符串
            if self.current_char in '"\'':
                return self.string(self.current_char)

            # 标识符或关键字
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            # 运算符
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.pos - 1)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.pos - 1)

            if self.current_char == '*':
                self.advance()
                if self.current_char == '*':
                    self.advance()
                    return Token(TokenType.POWER, '**', self.pos - 2)
                return Token(TokenType.MULTIPLY, '*', self.pos - 1)

            if self.current_char == '/':
                self.advance()
                if self.current_char == '/':
                    self.advance()
                    return Token(TokenType.FLOOR_DIV, '//', self.pos - 2)
                return Token(TokenType.DIVIDE, '/', self.pos - 1)

            if self.current_char == '%':
                self.advance()
                return Token(TokenType.MOD, '%', self.pos - 1)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.pos - 1)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.pos - 1)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.pos - 1)

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.pos - 2)
                self.error("Single '=' is not supported, use '==' for comparison")

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NE, '!=', self.pos - 2)
                # NOT 运算符
                return Token(TokenType.NOT, '!', self.pos - 1)

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LE, '<=', self.pos - 2)
                return Token(TokenType.LT, '<', self.pos - 1)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GE, '>=', self.pos - 2)
                return Token(TokenType.GT, '>', self.pos - 1)

            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token(TokenType.AND, '&&', self.pos - 2)
                self.error("Single '&' is not supported, use '&&' for logical AND")

            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token(TokenType.OR, '||', self.pos - 2)
                self.error("Single '|' is not supported, use '||' for logical OR")

            self.error(f"Unexpected character: {self.current_char}")

        return Token(TokenType.EOF, None, self.pos)


class ASTNode:
    """抽象语法树节点基类"""
    pass


class NumberNode(ASTNode):
    """数字节点"""
    def __init__(self, value: Union[int, float]):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class StringNode(ASTNode):
    """字符串节点"""
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"String({self.value!r})"


class BooleanNode(ASTNode):
    """布尔节点"""
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"


class VariableNode(ASTNode):
    """变量节点"""
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"


class BinaryOpNode(ASTNode):
    """二元运算节点"""
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op!r}, {self.right})"


class UnaryOpNode(ASTNode):
    """一元运算节点"""
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op!r}, {self.operand})"


class FunctionCallNode(ASTNode):
    """函数调用节点"""
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"


class ExpressionParser:
    """
    表达式解析器
    
    支持的运算符（优先级从低到高）：
    - or, ||          逻辑或
    - and, &&         逻辑与
    - not, !          逻辑非
    - ==, !=, <, <=, >, >=   比较
    - +, -            加减
    - *, /, //, %     乘除模
    - **              幂运算
    - 一元 -, +       正负号
    
    使用示例:
    >>> parser = ExpressionParser()
    >>> ast = parser.parse("2 + 3 * 4")
    >>> result = parser.evaluate(ast)
    >>> print(result)  # 14
    """

    def __init__(self, variables: Optional[Dict[str, Any]] = None,
                 functions: Optional[Dict[str, Callable]] = None):
        self.variables = variables or {}
        self.functions = functions or {}
        self._lexer: Optional[Lexer] = None
        self._current_token: Optional[Token] = None

    def parse(self, text: str) -> ASTNode:
        """解析表达式文本，返回 AST"""
        self._lexer = Lexer(text)
        self._current_token = self._lexer.get_next_token()
        ast = self._expression()
        
        if self._current_token.type != TokenType.EOF:
            raise ExpressionError(
                f"Unexpected token: {self._current_token.value}",
                self._current_token.position
            )
        
        return ast

    def _eat(self, token_type: TokenType) -> Token:
        """消费一个 Token"""
        if self._current_token.type == token_type:
            token = self._current_token
            self._current_token = self._lexer.get_next_token()
            return token
        raise ExpressionError(
            f"Expected {token_type}, got {self._current_token.type}",
            self._current_token.position
        )

    def _expression(self) -> ASTNode:
        """表达式入口（处理 or）"""
        return self._or_expression()

    def _or_expression(self) -> ASTNode:
        """or 表达式"""
        node = self._and_expression()

        while self._current_token.type in (TokenType.OR,):
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            node = BinaryOpNode(node, op, self._and_expression())

        return node

    def _and_expression(self) -> ASTNode:
        """and 表达式"""
        node = self._not_expression()

        while self._current_token.type in (TokenType.AND,):
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            node = BinaryOpNode(node, op, self._not_expression())

        return node

    def _not_expression(self) -> ASTNode:
        """not 表达式"""
        if self._current_token.type == TokenType.NOT:
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            return UnaryOpNode(op, self._not_expression())
        return self._comparison()

    def _comparison(self) -> ASTNode:
        """比较表达式"""
        node = self._additive()

        while self._current_token.type in (
            TokenType.EQ, TokenType.NE,
            TokenType.LT, TokenType.LE,
            TokenType.GT, TokenType.GE
        ):
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            node = BinaryOpNode(node, op, self._additive())

        return node

    def _additive(self) -> ASTNode:
        """加减表达式"""
        node = self._multiplicative()

        while self._current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            node = BinaryOpNode(node, op, self._multiplicative())

        return node

    def _multiplicative(self) -> ASTNode:
        """乘除模表达式"""
        node = self._power()

        while self._current_token.type in (
            TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.MOD, TokenType.FLOOR_DIV
        ):
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            node = BinaryOpNode(node, op, self._power())

        return node

    def _power(self) -> ASTNode:
        """幂表达式（右结合）"""
        node = self._unary()

        if self._current_token.type == TokenType.POWER:
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            node = BinaryOpNode(node, op, self._power())  # 右结合

        return node

    def _unary(self) -> ASTNode:
        """一元运算"""
        if self._current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self._current_token.value
            self._current_token = self._lexer.get_next_token()
            return UnaryOpNode(op, self._unary())
        return self._primary()

    def _primary(self) -> ASTNode:
        """基本表达式"""
        token = self._current_token

        if token.type == TokenType.NUMBER:
            self._current_token = self._lexer.get_next_token()
            return NumberNode(token.value)

        if token.type == TokenType.STRING:
            self._current_token = self._lexer.get_next_token()
            return StringNode(token.value)

        if token.type == TokenType.IDENTIFIER:
            name = token.value
            self._current_token = self._lexer.get_next_token()

            # 函数调用
            if self._current_token.type == TokenType.LPAREN:
                self._current_token = self._lexer.get_next_token()
                args = []

                if self._current_token.type != TokenType.RPAREN:
                    args.append(self._expression())
                    while self._current_token.type == TokenType.COMMA:
                        self._current_token = self._lexer.get_next_token()
                        args.append(self._expression())

                self._eat(TokenType.RPAREN)
                return FunctionCallNode(name, args)

            return VariableNode(name)

        if token.type == TokenType.LPAREN:
            self._current_token = self._lexer.get_next_token()
            node = self._expression()
            self._eat(TokenType.RPAREN)
            return node

        raise ExpressionError(
            f"Unexpected token: {token.type}",
            token.position
        )

    def evaluate(self, node: ASTNode, variables: Optional[Dict[str, Any]] = None,
                 functions: Optional[Dict[str, Callable]] = None) -> Any:
        """
        计算表达式的值
        
        Args:
            node: AST 节点
            variables: 变量字典（可选，覆盖初始化时的变量）
            functions: 函数字典（可选，覆盖初始化时的函数）
        
        Returns:
            计算结果
        """
        vars_dict = {**self.variables, **(variables or {})}
        funcs_dict = {**self.functions, **(functions or {})}

        return self._eval_node(node, vars_dict, funcs_dict)

    def _eval_node(self, node: ASTNode, variables: Dict[str, Any],
                   functions: Dict[str, Callable]) -> Any:
        """递归计算节点值"""

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, BooleanNode):
            return node.value

        if isinstance(node, VariableNode):
            if node.name not in variables:
                raise ExpressionError(f"Undefined variable: {node.name}")
            return variables[node.name]

        if isinstance(node, UnaryOpNode):
            operand = self._eval_node(node.operand, variables, functions)
            if node.op == '-':
                return -operand
            if node.op == '+':
                return +operand
            if node.op in ('not', '!'):
                return not operand
            raise ExpressionError(f"Unknown unary operator: {node.op}")

        if isinstance(node, BinaryOpNode):
            # 短路求值
            if node.op in ('and', '&&'):
                left = self._eval_node(node.left, variables, functions)
                if not left:
                    return False
                return bool(self._eval_node(node.right, variables, functions))

            if node.op in ('or', '||'):
                left = self._eval_node(node.left, variables, functions)
                if left:
                    return True
                return bool(self._eval_node(node.right, variables, functions))

            left = self._eval_node(node.left, variables, functions)
            right = self._eval_node(node.right, variables, functions)

            # 算术运算
            if node.op == '+':
                # 支持字符串拼接
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            if node.op == '-':
                return left - right
            if node.op == '*':
                return left * right
            if node.op == '/':
                if right == 0:
                    raise ExpressionError("Division by zero")
                return left / right
            if node.op == '//':
                if right == 0:
                    raise ExpressionError("Division by zero")
                return left // right
            if node.op == '%':
                if right == 0:
                    raise ExpressionError("Modulo by zero")
                return left % right
            if node.op == '**':
                return left ** right

            # 比较运算
            if node.op == '==':
                return left == right
            if node.op == '!=':
                return left != right
            if node.op == '<':
                return left < right
            if node.op == '<=':
                return left <= right
            if node.op == '>':
                return left > right
            if node.op == '>=':
                return left >= right

            raise ExpressionError(f"Unknown operator: {node.op}")

        if isinstance(node, FunctionCallNode):
            if node.name not in functions:
                raise ExpressionError(f"Undefined function: {node.name}")

            args = [self._eval_node(arg, variables, functions) for arg in node.args]
            return functions[node.name](*args)

        raise ExpressionError(f"Unknown node type: {type(node)}")