# -*- coding: utf-8 -*-
"""
AllToolkit - Either Monad Utilities 🎯

零依赖的 Either 单子工具库，提供函数式风格的显式错误处理。
完全使用 Python 标准库实现，无需任何外部依赖。

Either 类型用于表示可能成功或失败的计算结果：
- Right: 表示成功（包含正确值）
- Left: 表示失败（包含错误值）

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

from typing import (
    Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar, 
    Union, Iterable, Iterator, overload
)
from functools import wraps
from dataclasses import dataclass


# =============================================================================
# 类型变量
# =============================================================================

L = TypeVar('L')  # Left 类型（错误类型）
R = TypeVar('R')  # Right 类型（成功类型）
L2 = TypeVar('L2')
R2 = TypeVar('R2')
T = TypeVar('T')
U = TypeVar('U')


# =============================================================================
# Either 基类
# =============================================================================

class Either(Generic[L, R]):
    """
    Either 单子基类
    
    表示一个值可能是 Left（错误）或 Right（成功）。
    这是一个不可变的、函数式的数据结构。
    
    Example:
        >>> result = Right(42)
        >>> result.is_right()
        True
        >>> result.get_or_else(0)
        42
        
        >>> error = Left("Something went wrong")
        >>> error.is_left()
        True
        >>> error.get_or_else(0)
        0
    """
    
    __slots__ = ()
    
    def is_left(self) -> bool:
        """检查是否为 Left"""
        raise NotImplementedError
    
    def is_right(self) -> bool:
        """检查是否为 Right"""
        raise NotImplementedError
    
    def left(self) -> Optional['Left[L, R]']:
        """获取 Left 值（如果是 Right 则返回 None）"""
        return None
    
    def right(self) -> Optional['Right[L, R]']:
        """获取 Right 值（如果是 Left 则返回 None）"""
        return None
    
    def map(self, func: Callable[[R], R2]) -> 'Either[L, R2]':
        """
        映射 Right 值
        
        Args:
            func: 映射函数
        
        Returns:
            新的 Either，Left 值保持不变
        
        Example:
            >>> Right(5).map(lambda x: x * 2)
            Right(10)
            >>> Left("error").map(lambda x: x * 2)
            Left('error')
        """
        raise NotImplementedError
    
    def map_left(self, func: Callable[[L], L2]) -> 'Either[L2, R]':
        """
        映射 Left 值
        
        Args:
            func: 映射函数
        
        Returns:
            新的 Either，Right 值保持不变
        
        Example:
            >>> Left(5).map_left(lambda x: x * 2)
            Left(10)
            >>> Right("success").map_left(lambda x: x * 2)
            Right('success')
        """
        raise NotImplementedError
    
    def flat_map(self, func: Callable[[R], 'Either[L, R2]']) -> 'Either[L, R2]':
        """
        扁平映射（绑定操作）
        
        Args:
            func: 返回 Either 的函数
        
        Returns:
            函数返回的 Either
        
        Example:
            >>> def safe_divide(n):
            ...     return Right(10 / n) if n != 0 else Left("Division by zero")
            >>> Right(2).flat_map(safe_divide)
            Right(5.0)
            >>> Right(0).flat_map(safe_divide)
            Left('Division by zero')
        """
        raise NotImplementedError
    
    def flatten(self: 'Either[L, Either[L, R]]') -> 'Either[L, R]':
        """
        展平嵌套的 Either
        
        Example:
            >>> Right(Right(5)).flatten()
            Right(5)
            >>> Right(Left("error")).flatten()
            Left('error')
        """
        raise NotImplementedError
    
    def get_or_else(self, default: Union[R, Callable[[], R]]) -> R:
        """
        获取值或返回默认值
        
        Args:
            default: 默认值或返回默认值的函数
        
        Returns:
            Right 值或默认值
        
        Example:
            >>> Right(5).get_or_else(0)
            5
            >>> Left("error").get_or_else(0)
            0
            >>> Left("error").get_or_else(lambda: len("error"))
            5
        """
        raise NotImplementedError
    
    def get_or_raise(self) -> R:
        """
        获取值或抛出异常
        
        Returns:
            Right 值
        
        Raises:
            ValueError: 如果是 Left
        
        Example:
            >>> Right(5).get_or_raise()
            5
            >>> Left("error").get_or_raise()
            Traceback (most recent call last):
                ...
            ValueError: error
        """
        raise NotImplementedError
    
    def or_else(self, other: 'Either[L, R]') -> 'Either[L, R]':
        """
        如果是 Left 则返回 other
        
        Args:
            other: 备选 Either
        
        Returns:
            当前 Right 或 other
        
        Example:
            >>> Right(5).or_else(Right(10))
            Right(5)
            >>> Left("error").or_else(Right(10))
            Right(10)
        """
        raise NotImplementedError
    
    def swap(self) -> 'Either[R, L]':
        """
        交换 Left 和 Right
        
        Returns:
            交换后的 Either
        
        Example:
            >>> Right(5).swap()
            Left(5)
            >>> Left("error").swap()
            Right('error')
        """
        raise NotImplementedError
    
    def fold(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T:
        """
        折叠操作，处理两种情况
        
        Args:
            on_left: 处理 Left 的函数
            on_right: 处理 Right 的函数
        
        Returns:
            处理结果
        
        Example:
            >>> Right(5).fold(lambda e: f"Error: {e}", lambda v: f"Value: {v}")
            'Value: 5'
            >>> Left("oops").fold(lambda e: f"Error: {e}", lambda v: f"Value: {v}")
            'Error: oops'
        """
        raise NotImplementedError
    
    def filter(self, predicate: Callable[[R], bool], 
               on_false: Union[L, Callable[[R], L]]) -> 'Either[L, R]':
        """
        过滤 Right 值
        
        Args:
            predicate: 条件函数
            on_false: 条件不满足时返回的 Left 值或函数
        
        Returns:
            满足条件返回 Right，否则返回 Left
        
        Example:
            >>> Right(5).filter(lambda x: x > 3, "Too small")
            Right(5)
            >>> Right(2).filter(lambda x: x > 3, "Too small")
            Left('Too small')
        """
        raise NotImplementedError
    
    def exists(self, predicate: Callable[[R], bool]) -> bool:
        """
        检查 Right 值是否满足条件
        
        Args:
            predicate: 条件函数
        
        Returns:
            Right 值满足条件返回 True，Left 返回 False
        
        Example:
            >>> Right(5).exists(lambda x: x > 3)
            True
            >>> Left("error").exists(lambda x: x > 3)
            False
        """
        raise NotImplementedError
    
    def for_all(self, predicate: Callable[[R], bool]) -> bool:
        """
        检查 Right 值是否满足条件（Left 返回 True）
        
        Args:
            predicate: 条件函数
        
        Returns:
            Right 值满足条件返回 True，Left 也返回 True
        
        Example:
            >>> Right(5).for_all(lambda x: x > 3)
            True
            >>> Left("error").for_all(lambda x: x > 3)
            True
        """
        raise NotImplementedError
    
    def to_optional(self) -> Optional[R]:
        """
        转换为 Optional
        
        Returns:
            Right 值或 None
        
        Example:
            >>> Right(5).to_optional()
            5
            >>> Left("error").to_optional()
            None
        """
        raise NotImplementedError
    
    def to_list(self) -> List[R]:
        """
        转换为列表
        
        Returns:
            Right 值的列表或空列表
        
        Example:
            >>> Right(5).to_list()
            [5]
            >>> Left("error").to_list()
            []
        """
        raise NotImplementedError
    
    def __bool__(self) -> bool:
        """转换为布尔值（Right 为 True，Left 为 False）"""
        return self.is_right()
    
    def __iter__(self) -> Iterator[R]:
        """迭代器（Right 迭代一次，Left 返回空迭代器）"""
        return iter([])
    
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError
    
    def __hash__(self) -> int:
        raise NotImplementedError
    
    def __repr__(self) -> str:
        raise NotImplementedError


# =============================================================================
# Left 类
# =============================================================================

@dataclass(frozen=True)
class Left(Either[L, R]):
    """
    Left 类型，表示失败/错误
    
    Example:
        >>> result: Either[str, int] = Left("Something went wrong")
        >>> result.is_left()
        True
        >>> result.get_or_else(0)
        0
    """
    _value: L
    
    def is_left(self) -> bool:
        return True
    
    def is_right(self) -> bool:
        return False
    
    def left(self) -> 'Left[L, R]':
        return self
    
    def map(self, func: Callable[[R], R2]) -> 'Either[L, R2]':
        return Left(self._value)  # type: ignore
    
    def map_left(self, func: Callable[[L], L2]) -> 'Either[L2, R]':
        return Left(func(self._value))  # type: ignore
    
    def flat_map(self, func: Callable[[R], 'Either[L, R2]']) -> 'Either[L, R2]':
        return Left(self._value)  # type: ignore
    
    def flatten(self: 'Either[L, Either[L, R]]') -> 'Either[L, R]':
        return Left(self._value)  # type: ignore
    
    def get_or_else(self, default: Union[R, Callable[[], R]]) -> R:
        if callable(default):
            return default()
        return default
    
    def get_or_raise(self) -> R:
        if isinstance(self._value, Exception):
            raise self._value
        raise ValueError(str(self._value))
    
    def or_else(self, other: 'Either[L, R]') -> 'Either[L, R]':
        return other
    
    def swap(self) -> 'Either[R, L]':
        return Right(self._value)  # type: ignore
    
    def fold(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T:
        return on_left(self._value)
    
    def filter(self, predicate: Callable[[R], bool], 
               on_false: Union[L, Callable[[R], L]]) -> 'Either[L, R]':
        return self
    
    def exists(self, predicate: Callable[[R], bool]) -> bool:
        return False
    
    def for_all(self, predicate: Callable[[R], bool]) -> bool:
        return True
    
    def to_optional(self) -> Optional[R]:
        return None
    
    def to_list(self) -> List[R]:
        return []
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Left):
            return self._value == other._value
        return False
    
    def __hash__(self) -> int:
        return hash(('Left', self._value))
    
    def __repr__(self) -> str:
        return f"Left({self._value!r})"
    
    def __iter__(self) -> Iterator[R]:
        return iter([])


# =============================================================================
# Right 类
# =============================================================================

@dataclass(frozen=True)
class Right(Either[L, R]):
    """
    Right 类型，表示成功
    
    Example:
        >>> result: Either[str, int] = Right(42)
        >>> result.is_right()
        True
        >>> result.get_or_else(0)
        42
    """
    _value: R
    
    def is_left(self) -> bool:
        return False
    
    def is_right(self) -> bool:
        return True
    
    def right(self) -> 'Right[L, R]':
        return self
    
    def map(self, func: Callable[[R], R2]) -> 'Either[L, R2]':
        return Right(func(self._value))  # type: ignore
    
    def map_left(self, func: Callable[[L], L2]) -> 'Either[L2, R]':
        return Right(self._value)  # type: ignore
    
    def flat_map(self, func: Callable[[R], 'Either[L, R2]']) -> 'Either[L, R2]':
        return func(self._value)
    
    def flatten(self: 'Either[L, Either[L, R]]') -> 'Either[L, R]':
        inner = self._value
        if isinstance(inner, Either):
            return inner  # type: ignore
        return self  # type: ignore
    
    def get_or_else(self, default: Union[R, Callable[[], R]]) -> R:
        return self._value
    
    def get_or_raise(self) -> R:
        return self._value
    
    def or_else(self, other: 'Either[L, R]') -> 'Either[L, R]':
        return self
    
    def swap(self) -> 'Either[R, L]':
        return Left(self._value)  # type: ignore
    
    def fold(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T:
        return on_right(self._value)
    
    def filter(self, predicate: Callable[[R], bool], 
               on_false: Union[L, Callable[[R], L]]) -> 'Either[L, R]':
        if predicate(self._value):
            return self
        if callable(on_false):
            return Left(on_false(self._value))  # type: ignore
        return Left(on_false)  # type: ignore
    
    def exists(self, predicate: Callable[[R], bool]) -> bool:
        return predicate(self._value)
    
    def for_all(self, predicate: Callable[[R], bool]) -> bool:
        return predicate(self._value)
    
    def to_optional(self) -> Optional[R]:
        return self._value
    
    def to_list(self) -> List[R]:
        return [self._value]
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Right):
            return self._value == other._value
        return False
    
    def __hash__(self) -> int:
        return hash(('Right', self._value))
    
    def __repr__(self) -> str:
        return f"Right({self._value!r})"
    
    def __iter__(self) -> Iterator[R]:
        return iter([self._value])


# =============================================================================
# 辅助函数
# =============================================================================

def left(value: L) -> Either[L, Any]:
    """
    创建 Left 值
    
    Args:
        value: 错误值
    
    Returns:
        Left 实例
    
    Example:
        >>> result = left("Error message")
        >>> result.is_left()
        True
    """
    return Left(value)


def right(value: R) -> Either[Any, R]:
    """
    创建 Right 值
    
    Args:
        value: 成功值
    
    Returns:
        Right 实例
    
    Example:
        >>> result = right(42)
        >>> result.is_right()
        True
    """
    return Right(value)


def from_optional(value: Optional[R], error: L) -> Either[L, R]:
    """
    从 Optional 创建 Either
    
    Args:
        value: 可选值
        error: None 时的错误值
    
    Returns:
        Right(value) 或 Left(error)
    
    Example:
        >>> from_optional(5, "Not found")
        Right(5)
        >>> from_optional(None, "Not found")
        Left('Not found')
    """
    if value is None:
        return Left(error)
    return Right(value)


def from_exception(func: Callable[[], R], 
                   error_mapper: Optional[Callable[[Exception], L]] = None) -> Either[L, R]:
    """
    从可能抛出异常的函数创建 Either
    
    Args:
        func: 可能抛出异常的函数
        error_mapper: 异常转换函数（可选）
    
    Returns:
        Right(result) 或 Left(error)
    
    Example:
        >>> from_exception(lambda: int("42"))
        Right(42)
        >>> from_exception(lambda: int("abc"))
        Left(ValueError("invalid literal for int() with base 10: 'abc'"))
        >>> from_exception(lambda: int("abc"), str)
        Left("invalid literal for int() with base 10: 'abc'")
    """
    try:
        return Right(func())
    except Exception as e:
        if error_mapper:
            return Left(error_mapper(e))
        return Left(e)  # type: ignore


def try_catch(func: Callable[..., R]) -> Callable[..., Either[Exception, R]]:
    """
    装饰器，将可能抛出异常的函数转换为返回 Either 的函数
    
    Args:
        func: 可能抛出异常的函数
    
    Returns:
        返回 Either 的函数
    
    Example:
        >>> @try_catch
        ... def safe_divide(a, b):
        ...     return a / b
        >>> safe_divide(10, 2)
        Right(5.0)
        >>> safe_divide(10, 0)
        Left(ZeroDivisionError('division by zero'))
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Either[Exception, R]:
        try:
            return Right(func(*args, **kwargs))
        except Exception as e:
            return Left(e)
    return wrapper


def sequence(eithers: Iterable[Either[L, R]]) -> Either[List[L], List[R]]:
    """
    将 Either 列表转换为 Either 列表
    
    如果所有都是 Right，返回 Right(values)；
    如果有 Left，返回第一个 Left 的错误值列表。
    
    Args:
        eithers: Either 可迭代对象
    
    Returns:
        Either[List[L], List[R]]
    
    Example:
        >>> sequence([Right(1), Right(2), Right(3)])
        Right([1, 2, 3])
        >>> sequence([Right(1), Left("error"), Right(3)])
        Left(['error'])
    """
    lefts: List[L] = []
    rights: List[R] = []
    
    for e in eithers:
        if e.is_left():
            lefts.append(e._value)  # type: ignore
        else:
            rights.append(e._value)  # type: ignore
    
    if lefts:
        return Left(lefts)
    return Right(rights)


def sequence_first_error(eithers: Iterable[Either[L, R]]) -> Either[L, List[R]]:
    """
    将 Either 列表转换为 Either 列表（遇到第一个错误即返回）
    
    Args:
        eithers: Either 可迭代对象
    
    Returns:
        Either[L, List[R]]
    
    Example:
        >>> sequence_first_error([Right(1), Right(2), Right(3)])
        Right([1, 2, 3])
        >>> sequence_first_error([Right(1), Left("error"), Right(3)])
        Left('error')
    """
    rights: List[R] = []
    
    for e in eithers:
        if e.is_left():
            return Left(e._value)  # type: ignore
        rights.append(e._value)  # type: ignore
    
    return Right(rights)


def traverse(func: Callable[[T], Either[L, R]], 
             iterable: Iterable[T]) -> Either[L, List[R]]:
    """
    对每个元素应用函数，收集所有 Right 值或返回第一个 Left
    
    Args:
        func: 返回 Either 的函数
        iterable: 输入可迭代对象
    
    Returns:
        Either[L, List[R]]
    
    Example:
        >>> def safe_int(s):
        ...     try:
        ...         return Right(int(s))
        ...     except ValueError:
        ...         return Left(f"Invalid: {s}")
        >>> traverse(safe_int, ["1", "2", "3"])
        Right([1, 2, 3])
        >>> traverse(safe_int, ["1", "abc", "3"])
        Left('Invalid: abc')
    """
    return sequence_first_error(func(x) for x in iterable)


def partition_eithers(eithers: Iterable[Either[L, R]]) -> Tuple[List[L], List[R]]:
    """
    将 Either 列表分为 Left 和 Right 两部分
    
    Args:
        eithers: Either 可迭代对象
    
    Returns:
        (Left 值列表, Right 值列表)
    
    Example:
        >>> partition_eithers([Right(1), Left("a"), Right(2), Left("b")])
        (['a', 'b'], [1, 2])
    """
    lefts: List[L] = []
    rights: List[R] = []
    
    for e in eithers:
        if e.is_left():
            lefts.append(e._value)  # type: ignore
        else:
            rights.append(e._value)  # type: ignore
    
    return lefts, rights


def cond_either(*clauses: Tuple[Callable[[T], bool], Callable[[T], Either[L, R]]]) -> Callable[[T], Either[L, R]]:
    """
    条件 Either（类似 cond 表达式）
    
    Args:
        *clauses: (条件函数, Either 函数) 元组
    
    Returns:
        条件执行函数
    
    Example:
        >>> classify = cond_either(
        ...     (lambda x: x > 0, lambda x: Right("positive")),
        ...     (lambda x: x < 0, lambda x: Right("negative")),
        ...     (lambda x: True, lambda x: Left("zero is not allowed")),
        ... )
        >>> classify(5)
        Right('positive')
        >>> classify(0)
        Left('zero is not allowed')
    """
    def _cond(x: T) -> Either[L, R]:
        for condition, func in clauses:
            if condition(x):
                return func(x)
        return Left("No matching clause")  # type: ignore
    return _cond


def bimap(func_left: Callable[[L], L2], func_right: Callable[[R], R2]) -> Callable[[Either[L, R]], Either[L2, R2]]:
    """
    双向映射（同时处理 Left 和 Right）
    
    Args:
        func_left: Left 映射函数
        func_right: Right 映射函数
    
    Returns:
        Either 映射函数
    
    Example:
        >>> transform = bimap(str.upper, lambda x: x * 2)
        >>> transform(Right(5))
        Right(10)
        >>> transform(Left("error"))
        Left('ERROR')
    """
    def _bimap(either: Either[L, R]) -> Either[L2, R2]:
        if either.is_left():
            return either.map_left(func_left)  # type: ignore
        return either.map(func_right)  # type: ignore
    return _bimap


def ensure(value: R, condition: bool, error: L) -> Either[L, R]:
    """
    确保值满足条件，否则返回错误
    
    Args:
        value: 值
        condition: 条件
        error: 错误值
    
    Returns:
        Right(value) 或 Left(error)
    
    Example:
        >>> ensure(5, 5 > 0, "Must be positive")
        Right(5)
        >>> ensure(-5, -5 > 0, "Must be positive")
        Left('Must be positive')
    """
    if condition:
        return Right(value)
    return Left(error)


def ensure_pred(value: R, predicate: Callable[[R], bool], error: Union[L, Callable[[R], L]]) -> Either[L, R]:
    """
    使用谓词确保值有效
    
    Args:
        value: 值
        predicate: 谓词函数
        error: 错误值或错误函数
    
    Returns:
        Right(value) 或 Left(error)
    
    Example:
        >>> ensure_pred(5, lambda x: x > 0, "Must be positive")
        Right(5)
        >>> ensure_pred(-5, lambda x: x > 0, lambda x: f"Got {x}, must be positive")
        Left('Got -5, must be positive')
    """
    if predicate(value):
        return Right(value)
    if callable(error):
        return Left(error(value))  # type: ignore
    return Left(error)


# =============================================================================
# 链式操作（Chain of Responsibility）
# =============================================================================

class EitherChain(Generic[L, R]):
    """
    Either 链式操作构建器
    
    提供更流畅的链式操作语法。
    
    Example:
        >>> result = (EitherChain(10)
        ...     .map(lambda x: x * 2)
        ...     .filter(lambda x: x > 15, "Too small")
        ...     .map(lambda x: x + 1)
        ...     .build())
        >>> result
        Right(21)
    """
    
    def __init__(self, value: Either[L, R]):
        self._either = value
    
    @classmethod
    def from_value(cls, value: R) -> 'EitherChain[L, R]':
        """从值创建 Right 链"""
        return cls(Right(value))  # type: ignore
    
    @classmethod
    def from_error(cls, error: L) -> 'EitherChain[L, R]':
        """从错误创建 Left 链"""
        return cls(Left(error))  # type: ignore
    
    def map(self, func: Callable[[R], R2]) -> 'EitherChain[L, R2]':
        """映射 Right 值"""
        return EitherChain(self._either.map(func))  # type: ignore
    
    def map_left(self, func: Callable[[L], L2]) -> 'EitherChain[L2, R]':
        """映射 Left 值"""
        return EitherChain(self._either.map_left(func))  # type: ignore
    
    def flat_map(self, func: Callable[[R], Either[L, R2]]) -> 'EitherChain[L, R2]':
        """扁平映射"""
        return EitherChain(self._either.flat_map(func))  # type: ignore
    
    def filter(self, predicate: Callable[[R], bool], 
               error: Union[L, Callable[[R], L]]) -> 'EitherChain[L, R]':
        """过滤"""
        return EitherChain(self._either.filter(predicate, error))  # type: ignore
    
    def recover(self, other: Either[L, R]) -> 'EitherChain[L, R]':
        """如果是 Left 则恢复"""
        return EitherChain(self._either.or_else(other))
    
    def tap(self, func: Callable[[R], Any]) -> 'EitherChain[L, R]':
        """执行副作用后返回原值"""
        if self._either.is_right():
            func(self._either._value)  # type: ignore
        return self  # type: ignore
    
    def tap_left(self, func: Callable[[L], Any]) -> 'EitherChain[L, R]':
        """如果是 Left 则执行副作用"""
        if self._either.is_left():
            func(self._either._value)  # type: ignore
        return self  # type: ignore
    
    def on_success(self, func: Callable[[R], Any]) -> 'EitherChain[L, R]':
        """成功时执行（tap 的别名）"""
        return self.tap(func)
    
    def on_failure(self, func: Callable[[L], Any]) -> 'EitherChain[L, R]':
        """失败时执行（tap_left 的别名）"""
        return self.tap_left(func)
    
    def build(self) -> Either[L, R]:
        """构建最终的 Either"""
        return self._either
    
    def get_or_else(self, default: Union[R, Callable[[], R]]) -> R:
        """获取值或默认值"""
        return self._either.get_or_else(default)
    
    def get_or_raise(self) -> R:
        """获取值或抛出异常"""
        return self._either.get_or_raise()
    
    def __repr__(self) -> str:
        return f"EitherChain({self._either!r})"


def chain(value: R) -> EitherChain[Any, R]:
    """
    从值创建 Either 链
    
    Example:
        >>> chain(10).map(lambda x: x * 2).build()
        Right(20)
    """
    return EitherChain.from_value(value)


def chain_error(error: L) -> EitherChain[L, Any]:
    """
    从错误创建 Either 链
    
    Example:
        >>> chain_error("oops").map(lambda x: x * 2).build()
        Left('oops')
    """
    return EitherChain.from_error(error)


# =============================================================================
# 实用工具
# =============================================================================

def all_rights(eithers: Iterable[Either[L, R]]) -> List[R]:
    """
    收集所有 Right 值
    
    Args:
        eithers: Either 可迭代对象
    
    Returns:
        Right 值列表
    
    Example:
        >>> all_rights([Right(1), Left("a"), Right(2)])
        [1, 2]
    """
    return [e._value for e in eithers if e.is_right()]  # type: ignore


def all_lefts(eithers: Iterable[Either[L, R]]) -> List[L]:
    """
    收集所有 Left 值
    
    Args:
        eithers: Either 可迭代对象
    
    Returns:
        Left 值列表
    
    Example:
        >>> all_lefts([Right(1), Left("a"), Left("b")])
        ['a', 'b']
    """
    return [e._value for e in eithers if e.is_left()]  # type: ignore


def is_left(either: Either[L, R]) -> bool:
    """检查是否为 Left"""
    return either.is_left()


def is_right(either: Either[L, R]) -> bool:
    """检查是否为 Right"""
    return either.is_right()


def getOrElse(either: Either[L, R], default: R) -> R:
    """获取值或默认值"""
    return either.get_or_else(default)


def get_or_else(either: Either[L, R], default: R) -> R:
    """获取值或默认值（别名）"""
    return either.get_or_else(default)


# =============================================================================
# 模块导出
# =============================================================================

__all__ = [
    # 类
    'Either',
    'Left',
    'Right',
    'EitherChain',
    
    # 构造函数
    'left',
    'right',
    'from_optional',
    'from_exception',
    
    # 装饰器
    'try_catch',
    
    # 组合函数
    'sequence',
    'sequence_first_error',
    'traverse',
    'partition_eithers',
    'cond_either',
    'bimap',
    
    # 验证函数
    'ensure',
    'ensure_pred',
    
    # 链式操作
    'chain',
    'chain_error',
    
    # 实用工具
    'all_rights',
    'all_lefts',
    'is_left',
    'is_right',
    'getOrElse',
    'get_or_else',
]