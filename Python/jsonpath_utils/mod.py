"""
AllToolkit - Python JSONPath Utilities

A zero-dependency JSONPath query utility module.
Supports JSONPath expressions for querying and extracting data from JSON structures.

Features:
- Full JSONPath syntax support
- Filter expressions with comparison operators
- Array slicing and indexing
- Recursive descent
- Wildcard support
- Safe navigation with error handling

Author: AllToolkit
License: MIT
"""

import re
from typing import Any, List, Dict, Optional, Union, Callable, Tuple
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# Exceptions
# =============================================================================

class JSONPathError(Exception):
    """Base exception for JSONPath errors."""
    pass


class JSONPathSyntaxError(JSONPathError):
    """Raised when JSONPath expression has invalid syntax."""
    pass


class JSONPathTypeError(JSONPathError):
    """Raised when type mismatch occurs during evaluation."""
    pass


# =============================================================================
# Token Types
# =============================================================================

class TokenType(Enum):
    """Token types for JSONPath lexer."""
    ROOT = '$'
    CURRENT = '@'
    DOT = '.'
    LBRACKET = '['
    RBRACKET = ']'
    LPAREN = '('
    RPAREN = ')'
    STAR = '*'
    COMMA = ','
    COLON = ':'
    QUESTION = '?'
    DOTDOT = '..'
    NAME = 'NAME'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    EQ = '=='
    NE = '!='
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    AND = '&&'
    OR = '||'
    NOT = '!'
    EOF = 'EOF'


@dataclass
class Token:
    """Token representation."""
    type: TokenType
    value: Any
    position: int = 0


# =============================================================================
# Lexer
# =============================================================================

class JSONPathLexer:
    """Tokenizer for JSONPath expressions."""
    
    def __init__(self, expression: str):
        self.expression = expression
        self.pos = 0
        self.length = len(expression)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the JSONPath expression."""
        tokens = []
        
        while self.pos < self.length:
            char = self.expression[self.pos]
            
            # Skip whitespace
            if char.isspace():
                self.pos += 1
                continue
            
            # Root
            if char == '$':
                tokens.append(Token(TokenType.ROOT, '$', self.pos))
                self.pos += 1
                continue
            
            # Current node
            if char == '@':
                tokens.append(Token(TokenType.CURRENT, '@', self.pos))
                self.pos += 1
                continue
            
            # Dot
            if char == '.':
                if self.pos + 1 < self.length and self.expression[self.pos + 1] == '.':
                    tokens.append(Token(TokenType.DOTDOT, '..', self.pos))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.DOT, '.', self.pos))
                    self.pos += 1
                continue
            
            # Brackets
            if char == '[':
                tokens.append(Token(TokenType.LBRACKET, '[', self.pos))
                self.pos += 1
                continue
            
            if char == ']':
                tokens.append(Token(TokenType.RBRACKET, ']', self.pos))
                self.pos += 1
                continue
            
            # Parentheses
            if char == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.pos))
                self.pos += 1
                continue
            
            if char == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.pos))
                self.pos += 1
                continue
            
            # Star (wildcard)
            if char == '*':
                tokens.append(Token(TokenType.STAR, '*', self.pos))
                self.pos += 1
                continue
            
            # Comma
            if char == ',':
                tokens.append(Token(TokenType.COMMA, ',', self.pos))
                self.pos += 1
                continue
            
            # Colon (for slices)
            if char == ':':
                tokens.append(Token(TokenType.COLON, ':', self.pos))
                self.pos += 1
                continue
            
            # Question mark (for filters)
            if char == '?':
                tokens.append(Token(TokenType.QUESTION, '?', self.pos))
                self.pos += 1
                continue
            
            # Comparison operators
            if char == '=' and self.pos + 1 < self.length and self.expression[self.pos + 1] == '=':
                tokens.append(Token(TokenType.EQ, '==', self.pos))
                self.pos += 2
                continue
            
            if char == '!' and self.pos + 1 < self.length and self.expression[self.pos + 1] == '=':
                tokens.append(Token(TokenType.NE, '!=', self.pos))
                self.pos += 2
                continue
            
            if char == '!':
                tokens.append(Token(TokenType.NOT, '!', self.pos))
                self.pos += 1
                continue
            
            if char == '<':
                if self.pos + 1 < self.length and self.expression[self.pos + 1] == '=':
                    tokens.append(Token(TokenType.LE, '<=', self.pos))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.LT, '<', self.pos))
                    self.pos += 1
                continue
            
            if char == '>':
                if self.pos + 1 < self.length and self.expression[self.pos + 1] == '=':
                    tokens.append(Token(TokenType.GE, '>=', self.pos))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.GT, '>', self.pos))
                    self.pos += 1
                continue
            
            if char == '&' and self.pos + 1 < self.length and self.expression[self.pos + 1] == '&':
                tokens.append(Token(TokenType.AND, '&&', self.pos))
                self.pos += 2
                continue
            
            if char == '|' and self.pos + 1 < self.length and self.expression[self.pos + 1] == '|':
                tokens.append(Token(TokenType.OR, '||', self.pos))
                self.pos += 2
                continue
            
            # String literal
            if char in ('"', "'"):
                tokens.append(self._read_string(char))
                continue
            
            # Number
            if char.isdigit() or (char == '-' and self.pos + 1 < self.length and 
                                   self.expression[self.pos + 1].isdigit()):
                tokens.append(self._read_number())
                continue
            
            # Name/identifier
            if char.isalpha() or char == '_':
                tokens.append(self._read_name())
                continue
            
            # Unknown character
            raise JSONPathSyntaxError(f"Unexpected character '{char}' at position {self.pos}")
        
        tokens.append(Token(TokenType.EOF, None, self.pos))
        return tokens
    
    def _read_string(self, quote: str) -> Token:
        """Read a string literal."""
        start = self.pos
        self.pos += 1  # Skip opening quote
        result = []
        
        while self.pos < self.length:
            char = self.expression[self.pos]
            
            if char == quote:
                self.pos += 1  # Skip closing quote
                return Token(TokenType.STRING, ''.join(result), start)
            
            if char == '\\' and self.pos + 1 < self.length:
                self.pos += 1
                escaped = self.expression[self.pos]
                if escaped == 'n':
                    result.append('\n')
                elif escaped == 't':
                    result.append('\t')
                elif escaped == 'r':
                    result.append('\r')
                elif escaped == '\\':
                    result.append('\\')
                elif escaped == quote:
                    result.append(quote)
                else:
                    result.append(escaped)
                self.pos += 1
                continue
            
            result.append(char)
            self.pos += 1
        
        raise JSONPathSyntaxError(f"Unterminated string starting at position {start}")
    
    def _read_number(self) -> Token:
        """Read a number literal."""
        start = self.pos
        result = []
        
        # Handle negative sign
        if self.expression[self.pos] == '-':
            result.append('-')
            self.pos += 1
        
        # Read integer part
        while self.pos < self.length and self.expression[self.pos].isdigit():
            result.append(self.expression[self.pos])
            self.pos += 1
        
        # Read decimal part
        if self.pos < self.length and self.expression[self.pos] == '.':
            result.append('.')
            self.pos += 1
            while self.pos < self.length and self.expression[self.pos].isdigit():
                result.append(self.expression[self.pos])
                self.pos += 1
        
        value_str = ''.join(result)
        if '.' in value_str:
            return Token(TokenType.NUMBER, float(value_str), start)
        else:
            return Token(TokenType.NUMBER, int(value_str), start)
    
    def _read_name(self) -> Token:
        """Read an identifier/name."""
        start = self.pos
        result = []
        
        while self.pos < self.length:
            char = self.expression[self.pos]
            if char.isalnum() or char == '_':
                result.append(char)
                self.pos += 1
            else:
                break
        
        return Token(TokenType.NAME, ''.join(result), start)


# =============================================================================
# AST Nodes
# =============================================================================

class ASTNode:
    """Base class for AST nodes."""
    pass


@dataclass
class RootNode(ASTNode):
    """Root node ($)"""
    pass


@dataclass
class CurrentNode(ASTNode):
    """Current node (@)"""
    pass


@dataclass
class ChildNode(ASTNode):
    """Child accessor (.name or [name])"""
    name: str


@dataclass
class IndexNode(ASTNode):
    """Array index accessor [n]"""
    index: int


@dataclass
class SliceNode(ASTNode):
    """Array slice [start:end:step]"""
    start: Optional[int]
    end: Optional[int]
    step: Optional[int]


@dataclass
class WildcardNode(ASTNode):
    """Wildcard (*)"""
    pass


@dataclass
class RecursiveNode(ASTNode):
    """Recursive descent (..)"""
    pass


@dataclass
class FilterNode(ASTNode):
    """Filter expression [?(expression)]"""
    expression: 'FilterExpression'


@dataclass
class UnionNode(ASTNode):
    """Union [a,b,c]"""
    indices: List[Union[int, str]]


@dataclass
class FilterExpression:
    """Filter expression in brackets."""
    pass


@dataclass
class ComparisonExpr(FilterExpression):
    """Comparison expression."""
    left: Any
    operator: str
    right: Any


@dataclass
class LogicalExpr(FilterExpression):
    """Logical expression (and/or)."""
    left: FilterExpression
    operator: str
    right: FilterExpression


@dataclass
class NotExpr(FilterExpression):
    """Not expression."""
    expression: FilterExpression


@dataclass
class PathExpr(FilterExpression):
    """Path expression in filter."""
    path: List[ASTNode]


@dataclass
class LiteralExpr(FilterExpression):
    """Literal value in filter."""
    value: Any


# =============================================================================
# Parser
# =============================================================================

class JSONPathParser:
    """Parser for JSONPath expressions."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> List[ASTNode]:
        """Parse the token stream into an AST."""
        nodes = []
        
        # Must start with root
        if self.current().type != TokenType.ROOT:
            raise JSONPathSyntaxError("JSONPath expression must start with '$'")
        
        nodes.append(RootNode())
        self.advance()
        
        while self.current().type != TokenType.EOF:
            nodes.append(self._parse_path_element())
        
        return nodes
    
    def current(self) -> Token:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, None, -1)
    
    def advance(self) -> Token:
        """Advance to next token and return current."""
        token = self.current()
        self.pos += 1
        return token
    
    def _parse_path_element(self) -> ASTNode:
        """Parse a single path element."""
        token = self.current()
        
        if token.type == TokenType.DOT:
            self.advance()
            next_token = self.current()
            
            if next_token.type == TokenType.NAME:
                self.advance()
                return ChildNode(next_token.value)
            elif next_token.type == TokenType.STAR:
                self.advance()
                return WildcardNode()
            else:
                raise JSONPathSyntaxError(f"Expected name or '*' after '.', got {next_token.type}")
        
        elif token.type == TokenType.DOTDOT:
            self.advance()
            return RecursiveNode()
        
        elif token.type == TokenType.LBRACKET:
            return self._parse_bracket()
        
        elif token.type == TokenType.STAR:
            # Handle wildcard as standalone (after recursive descent like $..*)
            self.advance()
            return WildcardNode()
        
        elif token.type == TokenType.NAME:
            # Handle name as standalone (after recursive descent like $..name)
            name = token.value
            self.advance()
            return ChildNode(name)
        
        else:
            raise JSONPathSyntaxError(f"Unexpected token {token.type} at position {token.position}")
    
    def _parse_bracket(self) -> ASTNode:
        """Parse bracket expression."""
        self.advance()  # Skip [
        
        token = self.current()
        
        # Wildcard
        if token.type == TokenType.STAR:
            self.advance()
            self._expect(TokenType.RBRACKET)
            return WildcardNode()
        
        # Filter expression
        if token.type == TokenType.QUESTION:
            self.advance()
            self._expect(TokenType.LPAREN)
            expr = self._parse_filter_expression()
            self._expect(TokenType.RPAREN)
            self._expect(TokenType.RBRACKET)
            return FilterNode(expr)
        
        # Slice starting with colon (like [:3] or [:])
        if token.type == TokenType.COLON:
            return self._parse_slice(None)
        
        # String - could be single property or union of strings
        if token.type == TokenType.STRING:
            name = token.value
            self.advance()
            next_token = self.current()
            # Check for union of strings
            if next_token.type == TokenType.COMMA:
                return self._parse_string_union(name)
            self._expect(TokenType.RBRACKET)
            return ChildNode(name)
        
        # Number or slice or union
        if token.type == TokenType.NUMBER:
            return self._parse_index_or_slice_or_union()
        
        # Negative number
        if token.type == TokenType.NAME and token.value == '-':
            return self._parse_index_or_slice_or_union()
        
        raise JSONPathSyntaxError(f"Unexpected token {token.type} in bracket expression")
    
    def _parse_string_union(self, first: str) -> UnionNode:
        """Parse union of string indices like ["a","b","c"]."""
        indices = [first]
        
        while self.current().type == TokenType.COMMA:
            self.advance()
            token = self.current()
            if token.type == TokenType.STRING:
                indices.append(token.value)
                self.advance()
            else:
                raise JSONPathSyntaxError(f"Expected string in union, got {token.type}")
        
        self._expect(TokenType.RBRACKET)
        return UnionNode(indices)
    
    def _parse_index_or_slice_or_union(self) -> ASTNode:
        """Parse index, slice, or union expression."""
        first = self._parse_number_or_name()
        
        token = self.current()
        
        # Slice
        if token.type == TokenType.COLON:
            return self._parse_slice(first if isinstance(first, int) else None)
        
        # Union
        if token.type == TokenType.COMMA:
            return self._parse_union(first)
        
        # Single index
        self._expect(TokenType.RBRACKET)
        
        if isinstance(first, int):
            return IndexNode(first)
        else:
            return ChildNode(first)
    
    def _parse_number_or_name(self) -> Union[int, str]:
        """Parse a number or name."""
        token = self.current()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return int(token.value) if isinstance(token.value, int) else int(token.value)
        
        if token.type == TokenType.NAME:
            self.advance()
            return token.value
        
        if token.type == TokenType.STRING:
            self.advance()
            return token.value
        
        raise JSONPathSyntaxError(f"Expected number or name, got {token.type}")
    
    def _parse_slice(self, start: Optional[int]) -> SliceNode:
        """Parse a slice expression [start:end:step]."""
        self.advance()  # Skip first :
        
        end = None
        step = None
        
        # Check for end
        if self.current().type == TokenType.NUMBER:
            end = int(self.advance().value)
        
        # Check for step
        if self.current().type == TokenType.COLON:
            self.advance()
            if self.current().type == TokenType.NUMBER:
                step = int(self.advance().value)
        
        self._expect(TokenType.RBRACKET)
        return SliceNode(start, end, step)
    
    def _parse_union(self, first: Union[int, str]) -> UnionNode:
        """Parse a union expression [a,b,c]."""
        indices = [first]
        
        while self.current().type == TokenType.COMMA:
            self.advance()
            indices.append(self._parse_number_or_name())
        
        self._expect(TokenType.RBRACKET)
        return UnionNode(indices)
    
    def _parse_filter_expression(self) -> FilterExpression:
        """Parse a filter expression."""
        return self._parse_or_expression()
    
    def _parse_or_expression(self) -> FilterExpression:
        """Parse OR expression."""
        left = self._parse_and_expression()
        
        while self.current().type == TokenType.OR:
            self.advance()
            right = self._parse_and_expression()
            left = LogicalExpr(left, '||', right)
        
        return left
    
    def _parse_and_expression(self) -> FilterExpression:
        """Parse AND expression."""
        left = self._parse_not_expression()
        
        while self.current().type == TokenType.AND:
            self.advance()
            right = self._parse_not_expression()
            left = LogicalExpr(left, '&&', right)
        
        return left
    
    def _parse_not_expression(self) -> FilterExpression:
        """Parse NOT expression."""
        if self.current().type == TokenType.NOT:
            self.advance()
            return NotExpr(self._parse_not_expression())
        return self._parse_comparison()
    
    def _parse_comparison(self) -> FilterExpression:
        """Parse comparison expression."""
        left = self._parse_value()
        
        token = self.current()
        if token.type in (TokenType.EQ, TokenType.NE, TokenType.LT, 
                          TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.advance().value
            right = self._parse_value()
            return ComparisonExpr(left, op, right)
        
        return left
    
    def _parse_value(self) -> FilterExpression:
        """Parse a value in filter expression."""
        token = self.current()
        
        # Current node reference
        if token.type == TokenType.CURRENT:
            self.advance()
            path = [CurrentNode()]
            while self.current().type in (TokenType.DOT, TokenType.LBRACKET):
                path.append(self._parse_path_element())
            return PathExpr(path)
        
        # Root reference
        if token.type == TokenType.ROOT:
            self.advance()
            path = [RootNode()]
            while self.current().type in (TokenType.DOT, TokenType.LBRACKET):
                path.append(self._parse_path_element())
            return PathExpr(path)
        
        # Number
        if token.type == TokenType.NUMBER:
            self.advance()
            return LiteralExpr(token.value)
        
        # String
        if token.type == TokenType.STRING:
            self.advance()
            return LiteralExpr(token.value)
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self._parse_filter_expression()
            self._expect(TokenType.RPAREN)
            return expr
        
        raise JSONPathSyntaxError(f"Unexpected token {token.type} in filter expression")
    
    def _expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type."""
        token = self.current()
        if token.type != token_type:
            raise JSONPathSyntaxError(
                f"Expected {token_type}, got {token.type} at position {token.position}"
            )
        return self.advance()


# =============================================================================
# Evaluator
# =============================================================================

class JSONPathEvaluator:
    """Evaluator for JSONPath expressions."""
    
    def __init__(self, ast: List[ASTNode]):
        self.ast = ast
        self.root_data = None
    
    def evaluate(self, data: Any) -> List[Any]:
        """Evaluate the JSONPath against data."""
        self.root_data = data  # Store root for filter expressions
        results = [data]
        
        for node in self.ast:
            new_results = []
            for current in results:
                new_results.extend(self._evaluate_node(node, current))
            results = new_results
        
        return results
    
    def _evaluate_node(self, node: ASTNode, current: Any) -> List[Any]:
        """Evaluate a single AST node against current data."""
        if isinstance(node, RootNode):
            return [current]
        
        if isinstance(node, CurrentNode):
            return [current]
        
        if isinstance(node, ChildNode):
            return self._evaluate_child(node, current)
        
        if isinstance(node, IndexNode):
            return self._evaluate_index(node, current)
        
        if isinstance(node, SliceNode):
            return self._evaluate_slice(node, current)
        
        if isinstance(node, WildcardNode):
            return self._evaluate_wildcard(current)
        
        if isinstance(node, RecursiveNode):
            return self._evaluate_recursive(current)
        
        if isinstance(node, FilterNode):
            return self._evaluate_filter(node, current)
        
        if isinstance(node, UnionNode):
            return self._evaluate_union(node, current)
        
        return []
    
    def _evaluate_child(self, node: ChildNode, current: Any) -> List[Any]:
        """Evaluate child accessor."""
        if isinstance(current, dict):
            if node.name in current:
                return [current[node.name]]
        return []
    
    def _evaluate_index(self, node: IndexNode, current: Any) -> List[Any]:
        """Evaluate array index."""
        if isinstance(current, list):
            index = node.index
            if index < 0:
                index = len(current) + index
            if 0 <= index < len(current):
                return [current[index]]
        return []
    
    def _evaluate_slice(self, node: SliceNode, current: Any) -> List[Any]:
        """Evaluate array slice."""
        if not isinstance(current, list):
            return []
        
        length = len(current)
        start = node.start if node.start is not None else 0
        end = node.end if node.end is not None else length
        step = node.step if node.step is not None else 1
        
        # Handle negative indices
        if start < 0:
            start = max(0, length + start)
        if end < 0:
            end = max(0, length + end)
        
        return [current[i] for i in range(start, end, step) if i < length]
    
    def _evaluate_wildcard(self, current: Any) -> List[Any]:
        """Evaluate wildcard."""
        if isinstance(current, dict):
            return list(current.values())
        elif isinstance(current, list):
            return current[:]
        return []
    
    def _evaluate_recursive(self, current: Any) -> List[Any]:
        """Evaluate recursive descent."""
        results = []
        self._collect_recursive(current, results)
        return results
    
    def _collect_recursive(self, data: Any, results: List[Any]):
        """Recursively collect all values."""
        results.append(data)
        
        if isinstance(data, dict):
            for value in data.values():
                self._collect_recursive(value, results)
        elif isinstance(data, list):
            for item in data:
                self._collect_recursive(item, results)
    
    def _evaluate_filter(self, node: FilterNode, current: Any) -> List[Any]:
        """Evaluate filter expression."""
        if not isinstance(current, list):
            return []
        
        results = []
        for item in current:
            if self._evaluate_filter_expression(node.expression, item):
                results.append(item)
        return results
    
    def _evaluate_filter_expression(self, expr: FilterExpression, current: Any) -> bool:
        """Evaluate a filter expression."""
        if isinstance(expr, ComparisonExpr):
            left = self._get_filter_value(expr.left, current)
            right = self._get_filter_value(expr.right, current)
            return self._compare(left, expr.operator, right)
        
        if isinstance(expr, LogicalExpr):
            left = self._evaluate_filter_expression(expr.left, current)
            right = self._evaluate_filter_expression(expr.right, current)
            if expr.operator == '&&':
                return left and right
            else:
                return left or right
        
        if isinstance(expr, NotExpr):
            return not self._evaluate_filter_expression(expr.expression, current)
        
        if isinstance(expr, LiteralExpr):
            return bool(expr.value)
        
        if isinstance(expr, PathExpr):
            values = self._evaluate_path_in_filter(expr.path, current)
            return bool(values)
        
        return False
    
    def _get_filter_value(self, expr: FilterExpression, current: Any) -> Any:
        """Get the value from a filter expression."""
        if isinstance(expr, LiteralExpr):
            return expr.value
        
        if isinstance(expr, PathExpr):
            values = self._evaluate_path_in_filter(expr.path, current)
            return values[0] if values else None
        
        return None
    
    def _evaluate_path_in_filter(self, path: List[ASTNode], current: Any) -> List[Any]:
        """Evaluate a path expression within a filter."""
        # Start with current or root depending on first node
        if path and isinstance(path[0], RootNode):
            results = [self.root_data]
            path = path[1:]  # Skip the root node since we already used it
        elif path and isinstance(path[0], CurrentNode):
            results = [current]
            path = path[1:]  # Skip the current node
        else:
            results = [current]
        
        for node in path:
            new_results = []
            for curr in results:
                new_results.extend(self._evaluate_node(node, curr))
            results = new_results
        
        return results
    
    def _compare(self, left: Any, operator: str, right: Any) -> bool:
        """Compare two values with an operator."""
        try:
            if operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '<':
                return left < right
            elif operator == '<=':
                return left <= right
            elif operator == '>':
                return left > right
            elif operator == '>=':
                return left >= right
        except TypeError:
            return False
        return False
    
    def _evaluate_union(self, node: UnionNode, current: Any) -> List[Any]:
        """Evaluate union expression."""
        results = []
        
        for index in node.indices:
            if isinstance(index, int):
                if isinstance(current, list):
                    idx = index if index >= 0 else len(current) + index
                    if 0 <= idx < len(current):
                        results.append(current[idx])
            else:
                if isinstance(current, dict) and index in current:
                    results.append(current[index])
        
        return results


# =============================================================================
# Main JSONPath Class
# =============================================================================

class JSONPath:
    """
    JSONPath query class.
    
    Usage:
        path = JSONPath('$.store.book[*].author')
        results = path.query(data)
    """
    
    def __init__(self, expression: str):
        """
        Initialize JSONPath with expression.
        
        Args:
            expression: JSONPath expression string
        """
        self.expression = expression
        self._ast = None
        self._compiled = False
    
    def compile(self) -> None:
        """Compile the expression."""
        if self._compiled:
            return
        
        lexer = JSONPathLexer(self.expression)
        tokens = lexer.tokenize()
        parser = JSONPathParser(tokens)
        self._ast = parser.parse()
        self._compiled = True
    
    def query(self, data: Any) -> List[Any]:
        """
        Query data with JSONPath expression.
        
        Args:
            data: JSON data (dict, list, or primitive)
        
        Returns:
            List of matching values
        """
        self.compile()
        evaluator = JSONPathEvaluator(self._ast)
        return evaluator.evaluate(data)
    
    def query_one(self, data: Any) -> Optional[Any]:
        """
        Query and return first match.
        
        Args:
            data: JSON data
        
        Returns:
            First matching value or None
        """
        results = self.query(data)
        return results[0] if results else None
    
    def match(self, data: Any) -> List[Dict[str, Any]]:
        """
        Query and return matches with paths.
        
        Args:
            data: JSON data
        
        Returns:
            List of dicts with 'path' and 'value' keys
        """
        self.compile()
        return self._match_recursive(data, self._ast[1:] if self._ast else [], ['$'])
    
    def _match_recursive(self, data: Any, remaining_ast: List[ASTNode], 
                         current_path: List[str]) -> List[Dict[str, Any]]:
        """Recursively match and build paths."""
        if not remaining_ast:
            return [{'path': ''.join(current_path), 'value': data}]
        
        node = remaining_ast[0]
        rest = remaining_ast[1:]
        results = []
        
        if isinstance(node, ChildNode):
            if isinstance(data, dict) and node.name in data:
                new_path = current_path + [f'.{node.name}']
                results.extend(self._match_recursive(data[node.name], rest, new_path))
        
        elif isinstance(node, IndexNode):
            if isinstance(data, list):
                index = node.index
                if index < 0:
                    index = len(data) + index
                if 0 <= index < len(data):
                    new_path = current_path + [f'[{index}]']
                    results.extend(self._match_recursive(data[index], rest, new_path))
        
        elif isinstance(node, WildcardNode):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = current_path + [f'.{key}']
                    results.extend(self._match_recursive(value, rest, new_path))
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    new_path = current_path + [f'[{i}]']
                    results.extend(self._match_recursive(item, rest, new_path))
        
        return results
    
    @staticmethod
    def find(expression: str, data: Any) -> List[Any]:
        """
        Static method to query data.
        
        Args:
            expression: JSONPath expression
            data: JSON data
        
        Returns:
            List of matching values
        """
        return JSONPath(expression).query(data)


# =============================================================================
# Convenience Functions
# =============================================================================

def find(expression: str, data: Any) -> List[Any]:
    """
    Query JSON data with JSONPath expression.
    
    Args:
        expression: JSONPath expression
        data: JSON data
    
    Returns:
        List of matching values
    
    Examples:
        >>> data = {'store': {'book': [{'title': 'Book 1'}, {'title': 'Book 2'}]}}
        >>> find('$.store.book[*].title', data)
        ['Book 1', 'Book 2']
    """
    return JSONPath(expression).query(data)


def find_one(expression: str, data: Any) -> Optional[Any]:
    """
    Query JSON data and return first match.
    
    Args:
        expression: JSONPath expression
        data: JSON data
    
    Returns:
        First matching value or None
    """
    return JSONPath(expression).query_one(data)


def compile(expression: str) -> JSONPath:
    """
    Compile a JSONPath expression for reuse.
    
    Args:
        expression: JSONPath expression
    
    Returns:
        Compiled JSONPath object
    """
    path = JSONPath(expression)
    path.compile()
    return path


def validate(expression: str) -> bool:
    """
    Validate a JSONPath expression.
    
    Args:
        expression: JSONPath expression
    
    Returns:
        True if valid, False otherwise
    """
    try:
        JSONPath(expression).compile()
        return True
    except JSONPathError:
        return False


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 3:
        print("JSONPath Utils - Command Line Interface")
        print("Usage: python mod.py <expression> <json_file>")
        print("\nExamples:")
        print("  python mod.py '$.store.book[*].author' data.json")
        print("  python mod.py '$..price' data.json")
        print("  python mod.py '$.store.book[?(@.price < 10)]' data.json")
        sys.exit(0)
    
    expression = sys.argv[1]
    json_file = sys.argv[2]
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        path = JSONPath(expression)
        results = path.query(data)
        
        print(f"Found {len(results)} result(s):")
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)
    except JSONPathError as e:
        print(f"Error: Invalid JSONPath: {e}")
        sys.exit(1)