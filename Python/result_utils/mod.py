# -*- coding: utf-8 -*-
"""
AllToolkit - Result Type Utilities

零依赖的 Result/Either 类型实现，提供函数式错误处理模式。
类似 Rust 的 Result<T, E> 和 Scala 的 Either[L, R]。
完全使用 Python 标准库实现，无需任何外部依赖。

核心概念：
- Result[T, E]: 表示可能成功(Ok)或失败(Error)的结果
- Ok[T]: 成功结果，包含值
- Error[E]: 失败结果，包含错误信息
- Either[L, R]: 左或右值，可表示成功/失败或其他二元状态

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

from typing import (
    Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar, Union,
    overload, cast, NoReturn
)
from functools import wraps
import traceback


# =============================================================================
# 类型变量
# =============================================================================

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')
F = TypeVar('F')
L = TypeVar('L')
R = TypeVar('R')


# =============================================================================
# Result 类型 - Ok 和 Error
# =============================================================================

class Ok(Generic[T]):
    """
    成功结果类型
    
    表示操作成功完成并包含返回值。
    
    Example:
        >>> result = Ok(42)
        >>> result.is_ok()
        True
        >>> result.unwrap()
        42
    """
    
    def __init__(self, value: T):
        self._value = value
    
    @property
    def value(self) -> T:
        """获取值（属性访问）"""
        return self._value
    
    def is_ok(self) -> bool:
        """检查是否为成功结果"""
        return True
    
    def is_error(self) -> bool:
        """检查是否为失败结果"""
        return False
    
    def unwrap(self) -> T:
        """
        获取成功值，如果是 Error 则抛出异常
        
        Returns:
            成功值
        
        Raises:
            UnwrapError: 如果是 Error 结果
        """
        return self._value
    
    def unwrap_or(self, default: T) -> T:
        """获取值，失败时返回默认值"""
        return self._value
    
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        """获取值，失败时调用函数生成默认值"""
        return self._value
    
    def unwrap_error(self) -> NoReturn:
        """
        获取错误值，如果是 Ok 则抛出异常
        
        Raises:
            UnwrapError: 如果是 Ok 结果
        """
        raise UnwrapError("Called unwrap_error on an Ok value")
    
    def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
        """对成功值应用函数"""
        return Ok(f(self._value))
    
    def map_error(self, f: Callable[[E], F]) -> 'Result[T, F]':
        """对错误值应用函数（Ok 不变）"""
        return cast('Result[T, F]', self)
    
    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """链式操作，对成功值调用函数返回新的 Result"""
        return f(self._value)
    
    def or_else(self, f: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        """链式操作，对错误值调用函数（Ok 不变）"""
        return cast('Result[T, F]', self)
    
    def expect(self, msg: str) -> T:
        """获取值，失败时抛出带消息的异常"""
        return self._value
    
    def expect_error(self, msg: str) -> NoReturn:
        """获取错误值，成功时抛出带消息的异常"""
        raise UnwrapError(f"{msg}: Ok({self._value})")
    
    def ok(self) -> Optional[T]:
        """转换为 Optional，Ok 返回值，Error 返回 None"""
        return self._value
    
    def err(self) -> Optional[E]:
        """获取错误值，Ok 返回 None"""
        return None
    
    def transpose(self) -> 'Optional[Result[T, E]]':
        """如果值为 Optional，转换为 Result Optional"""
        if self._value is None:
            return None
        return Ok(self._value)
    
    def __repr__(self) -> str:
        return f"Ok({self._value!r})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        return False
    
    def __hash__(self) -> int:
        return hash(('Ok', self._value))


class Error(Generic[E]):
    """
    失败结果类型
    
    表示操作失败并包含错误信息。
    
    Example:
        >>> result = Error("something went wrong")
        >>> result.is_error()
        True
        >>> result.unwrap_error()
        'something went wrong'
    """
    
    def __init__(self, error: E):
        self._error = error
    
    @property
    def error_value(self) -> E:
        """获取错误值（属性访问）"""
        return self._error
    
    def is_ok(self) -> bool:
        """检查是否为成功结果"""
        return False
    
    def is_error(self) -> bool:
        """检查是否为失败结果"""
        return True
    
    def unwrap(self) -> NoReturn:
        """
        获取成功值，如果是 Error 则抛出异常
        
        Raises:
            UnwrapError: 如果是 Error 结果
        """
        raise UnwrapError(f"Called unwrap on an Error value: {self._error!r}")
    
    def unwrap_or(self, default: T) -> T:
        """获取值，失败时返回默认值"""
        return default
    
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        """获取值，失败时调用函数生成默认值"""
        return f(self._error)
    
    def unwrap_error(self) -> E:
        """获取错误值"""
        return self._error
    
    def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
        """对成功值应用函数（Error 不变）"""
        return cast('Result[U, E]', self)
    
    def map_error(self, f: Callable[[E], F]) -> 'Result[T, F]':
        """对错误值应用函数"""
        return Error(f(self._error))
    
    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """链式操作，对成功值调用函数（Error 不变）"""
        return cast('Result[U, E]', self)
    
    def or_else(self, f: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        """链式操作，对错误值调用函数"""
        return f(self._error)
    
    def expect(self, msg: str) -> NoReturn:
        """获取值，失败时抛出带消息的异常"""
        raise UnwrapError(f"{msg}: Error({self._error!r})")
    
    def expect_error(self, msg: str) -> E:
        """获取错误值"""
        return self._error
    
    def ok(self) -> Optional[T]:
        """转换为 Optional，Ok 返回值，Error 返回 None"""
        return None
    
    def err(self) -> Optional[E]:
        """获取错误值，Ok 返回 None"""
        return self._error
    
    def transpose(self) -> Optional['Result[T, E]']:
        """如果值为 Optional，转换为 Result Optional"""
        return self
    
    def __repr__(self) -> str:
        return f"Error({self._error!r})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Error):
            return self._error == other._error
        return False
    
    def __hash__(self) -> int:
        return hash(('Error', self._error))


# Result 类型别名
Result = Union[Ok[T], Error[E]]


# =============================================================================
# Either 类型 - Left 和 Right
# =============================================================================

class Left(Generic[L]):
    """
    Either 的左值
    
    通常用于表示失败或异常情况，但也可以表示其他含义。
    
    Example:
        >>> either = Left("error message")
        >>> either.is_left()
        True
    """
    
    def __init__(self, value: L):
        self._value = value
    
    @property
    def value(self) -> L:
        """获取值（属性访问）"""
        return self._value
    
    def is_left(self) -> bool:
        """检查是否为左值"""
        return True
    
    def is_right(self) -> bool:
        """检查是否为右值"""
        return False
    
    def unwrap_left(self) -> L:
        """获取左值"""
        return self._value
    
    def unwrap_right(self) -> NoReturn:
        """获取右值，Left 时抛出异常"""
        raise UnwrapError("Called unwrap_right on a Left value")
    
    def unwrap_left_or(self, default: L) -> L:
        """获取左值（Left 时返回自身值）"""
        return self._value
    
    def unwrap_right_or(self, default: R) -> R:
        """获取右值，Left 时返回默认值"""
        return default
    
    def unwrap_left_or_else(self, f: Callable[[R], L]) -> L:
        """获取左值（Left 时返回自身值）"""
        return self._value
    
    def unwrap_right_or_else(self, f: Callable[[L], R]) -> R:
        """获取右值，Left 时调用函数"""
        return f(self._value)
    
    def map_left(self, f: Callable[[L], U]) -> 'Either[U, R]':
        """对左值应用函数"""
        return Left(f(self._value))
    
    def map_right(self, f: Callable[[R], U]) -> 'Either[L, U]':
        """对右值应用函数（Left 不变）"""
        return cast('Either[L, U]', self)
    
    def fold(self, left_fn: Callable[[L], T], right_fn: Callable[[R], T]) -> T:
        """根据类型应用对应函数"""
        return left_fn(self._value)
    
    def swap(self) -> 'Either[R, L]':
        """交换左右"""
        return Right(self._value)
    
    def left(self) -> Optional[L]:
        """获取左值，Right 时返回 None"""
        return self._value
    
    def right(self) -> Optional[R]:
        """获取右值，Left 时返回 None"""
        return None
    
    def __repr__(self) -> str:
        return f"Left({self._value!r})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Left):
            return self._value == other._value
        return False
    
    def __hash__(self) -> int:
        return hash(('Left', self._value))


class Right(Generic[R]):
    """
    Either 的右值
    
    通常用于表示成功或正常情况。
    
    Example:
        >>> either = Right(42)
        >>> either.is_right()
        True
    """
    
    def __init__(self, value: R):
        self._value = value
    
    @property
    def value(self) -> R:
        """获取值（属性访问）"""
        return self._value
    
    def is_left(self) -> bool:
        """检查是否为左值"""
        return False
    
    def is_right(self) -> bool:
        """检查是否为右值"""
        return True
    
    def unwrap_left(self) -> NoReturn:
        """获取左值，Right 时抛出异常"""
        raise UnwrapError("Called unwrap_left on a Right value")
    
    def unwrap_right(self) -> R:
        """获取右值"""
        return self._value
    
    def unwrap_left_or(self, default: L) -> L:
        """获取左值，Right 时返回默认值"""
        return default
    
    def unwrap_right_or(self, default: R) -> R:
        """获取右值（Right 时返回自身值）"""
        return self._value
    
    def unwrap_left_or_else(self, f: Callable[[R], L]) -> L:
        """获取左值，Right 时调用函数"""
        return f(self._value)
    
    def unwrap_right_or_else(self, f: Callable[[L], R]) -> R:
        """获取右值（Right 时返回自身值）"""
        return self._value
    
    def map_left(self, f: Callable[[L], U]) -> 'Either[U, R]':
        """对左值应用函数（Right 不变）"""
        return cast('Either[U, R]', self)
    
    def map_right(self, f: Callable[[R], U]) -> 'Either[L, U]':
        """对右值应用函数"""
        return Right(f(self._value))
    
    def fold(self, left_fn: Callable[[L], T], right_fn: Callable[[R], T]) -> T:
        """根据类型应用对应函数"""
        return right_fn(self._value)
    
    def swap(self) -> 'Either[R, L]':
        """交换左右"""
        return Left(self._value)
    
    def left(self) -> Optional[L]:
        """获取左值，Right 时返回 None"""
        return None
    
    def right(self) -> Optional[R]:
        """获取右值，Left 时返回 None"""
        return self._value
    
    def __repr__(self) -> str:
        return f"Right({self._value!r})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Right):
            return self._value == other._value
        return False
    
    def __hash__(self) -> int:
        return hash(('Right', self._value))


# Either 类型别名
Either = Union[Left[L], Right[R]]


# =============================================================================
# 异常类
# =============================================================================

class UnwrapError(Exception):
    """
    解包错误异常
    
    在对 Result/Either 类型进行不正确的解包操作时抛出。
    """
    pass


# =============================================================================
# 辅助函数
# =============================================================================

def ok(value: T) -> Ok[T]:
    """
    创建成功结果
    
    Args:
        value: 成功值
    
    Returns:
        Ok 结果
    
    Example:
        >>> result = ok(42)
        >>> result.unwrap()
        42
    """
    return Ok(value)


def error(err: E) -> Error[E]:
    """
    创建失败结果
    
    Args:
        err: 错误值
    
    Returns:
        Error 结果
    
    Example:
        >>> result = error("failed")
        >>> result.unwrap_error()
        'failed'
    """
    return Error(err)


def left(value: L) -> Left[L]:
    """
    创建 Either 左值
    
    Args:
        value: 左值
    
    Returns:
        Left 值
    
    Example:
        >>> either = left("error")
        >>> either.is_left()
        True
    """
    return Left(value)


def right(value: R) -> Right[R]:
    """
    创建 Either 右值
    
    Args:
        value: 右值
    
    Returns:
        Right 值
    
    Example:
        >>> either = right(42)
        >>> either.is_right()
        True
    """
    return Right(value)


def from_optional(value: Optional[T], err: E) -> Result[T, E]:
    """
    从 Optional 创建 Result
    
    Args:
        value: 可选值
        err: None 时的错误值
    
    Returns:
        Ok(value) 或 Error(err)
    
    Example:
        >>> from_optional(42, "not found").unwrap()
        42
        >>> from_optional(None, "not found").unwrap_error()
        'not found'
    """
    if value is None:
        return Error(err)
    return Ok(value)


def from_exception(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    """
    将可能抛出异常的函数转换为返回 Result 的函数
    
    Args:
        func: 可能抛出异常的函数
    
    Returns:
        返回 Result 的包装函数
    
    Example:
        >>> @from_exception
        ... def divide(a, b):
        ...     return a / b
        >>> divide(10, 2).unwrap()
        5.0
        >>> divide(10, 0).is_error()
        True
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Result[T, Exception]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            return Error(e)
    return wrapper


def try_call(func: Callable[..., T], *args, **kwargs) -> Result[T, Exception]:
    """
    尝试调用函数，捕获异常并返回 Result
    
    Args:
        func: 要调用的函数
        *args: 函数参数
        **kwargs: 函数关键字参数
    
    Returns:
        Ok(result) 或 Error(exception)
    
    Example:
        >>> try_call(int, "42").unwrap()
        42
        >>> try_call(int, "abc").is_error()
        True
    """
    try:
        return Ok(func(*args, **kwargs))
    except Exception as e:
        return Error(e)


def try_call_with(exc_type: type, func: Callable[..., T], *args, **kwargs) -> Result[T, E]:
    """
    尝试调用函数，捕获特定类型异常
    
    Args:
        exc_type: 要捕获的异常类型
        func: 要调用的函数
        *args: 函数参数
        **kwargs: 函数关键字参数
    
    Returns:
        Ok(result) 或 Error(exception)
    
    Example:
        >>> try_call_with(ValueError, int, "abc").unwrap_error()
        ValueError(...)
    """
    try:
        return Ok(func(*args, **kwargs))
    except exc_type as e:
        return Error(cast(E, e))


def collect_results(results: List[Result[T, E]]) -> Result[List[T], List[E]]:
    """
    收集多个 Result，全成功返回 Ok(列表)，否则返回 Error(错误列表)
    
    Args:
        results: Result 列表
    
    Returns:
        Ok(values) 或 Error(errors)
    
    Example:
        >>> collect_results([Ok(1), Ok(2), Ok(3)].unwrap()
        [1, 2, 3]
        >>> collect_results([Ok(1), Error("e1"), Error("e2")]).unwrap_error()
        ['e1', 'e2']
    """
    values = []
    errors = []
    
    for r in results:
        if r.is_ok():
            values.append(r.unwrap())
        else:
            errors.append(r.unwrap_error())
    
    if errors:
        return Error(errors)
    return Ok(values)


def partition_results(results: List[Result[T, E]]) -> Tuple[List[T], List[E]]:
    """
    分离 Result 列表为成功和失败两部分
    
    Args:
        results: Result 列表
    
    Returns:
        (成功值列表, 错误值列表)
    
    Example:
        >>> partition_results([Ok(1), Error("e1"), Ok(2)])
        ([1, 2], ['e1'])
    """
    values = []
    errors = []
    
    for r in results:
        if r.is_ok():
            values.append(r.unwrap())
        else:
            errors.append(r.unwrap_error())
    
    return (values, errors)


def first_ok(results: List[Result[T, E]]) -> Result[T, List[E]]:
    """
    获取第一个成功结果，全失败返回所有错误
    
    Args:
        results: Result 列表
    
    Returns:
        第一个 Ok 或 Error(所有错误)
    
    Example:
        >>> first_ok([Error("e1"), Ok(42), Ok(3)].unwrap()
        42
    """
    errors = []
    
    for r in results:
        if r.is_ok():
            return r
        errors.append(r.unwrap_error())
    
    return Error(errors)


def flatten_result(result: Result[Result[T, E], E]) -> Result[T, E]:
    """
    嵌套 Result 解压
    
    Args:
        result: 嵌套的 Result
    
    Returns:
        解压后的 Result
    
    Example:
        >>> flatten_result(Ok(Ok(42))).unwrap()
        42
        >>> flatten_result(Ok(Error("e"))).unwrap_error()
        'e'
    """
    if result.is_ok():
        inner = result.unwrap()
        if isinstance(inner, (Ok, Error)):
            return inner
        return Ok(inner)
    return result


def result_to_either(result: Result[T, E]) -> Either[E, T]:
    """
    将 Result 转换为 Either
    
    Args:
        result: Result 类型
    
    Returns:
        Either 类型（Left=Error, Right=Ok）
    
    Example:
        >>> result_to_either(Ok(42)).is_right()
        True
        >>> result_to_either(Error("e")).is_left()
        True
    """
    if result.is_ok():
        return Right(result.unwrap())
    return Left(result.unwrap_error())


def either_to_result(either: Either[E, T]) -> Result[T, E]:
    """
    将 Either 转换为 Result
    
    Args:
        either: Either 类型
    
    Returns:
        Result 类型（Left=Error, Right=Ok）
    
    Example:
        >>> either_to_result(Right(42)).is_ok()
        True
        >>> either_to_result(Left("e")).is_error()
        True
    """
    if either.is_right():
        return Ok(either.unwrap_right())
    return Error(either.unwrap_left())


def safe_get(d: Dict[Any, T], key: Any, err: E) -> Result[T, E]:
    """
    安全获取字典值
    
    Args:
        d: 字典
        key: 键
        err: 键不存在时的错误值
    
    Returns:
        Ok(value) 或 Error(err)
    
    Example:
        >>> safe_get({'a': 1}, 'a', 'not found').unwrap()
        1
    """
    if key in d:
        return Ok(d[key])
    return Error(err)


def safe_index(lst: List[T], index: int, err: E) -> Result[T, E]:
    """
    安全获取列表元素
    
    Args:
        lst: 列表
        index: 索引
        err: 索引越界时的错误值
    
    Returns:
        Ok(value) 或 Error(err)
    
    Example:
        >>> safe_index([1, 2, 3], 1, 'out of bounds').unwrap()
        2
    """
    try:
        return Ok(lst[index])
    except IndexError:
        return Error(err)


def safe_divide(a: float, b: float, err: E = "division by zero") -> Result[float, E]:
    """
    安全除法
    
    Args:
        a: 被除数
        b: 除数
        err: 除数为 0 时的错误值
    
    Returns:
        Ok(result) 或 Error(err)
    
    Example:
        >>> safe_divide(10, 2).unwrap()
        5.0
    """
    if b == 0:
        return Error(err)
    return Ok(a / b)


def safe_parse_int(s: str, err: E = "invalid integer") -> Result[int, E]:
    """
    安全解析整数
    
    Args:
        s: 字符串
        err: 解析失败时的错误值
    
    Returns:
        Ok(int) 或 Error(err)
    
    Example:
        >>> safe_parse_int("42").unwrap()
        42
    """
    try:
        return Ok(int(s))
    except ValueError:
        return Error(err)


def safe_parse_float(s: str, err: E = "invalid float") -> Result[float, E]:
    """
    安全解析浮点数
    
    Args:
        s: 字符串
        err: 解析失败时的错误值
    
    Returns:
        Ok(float) 或 Error(err)
    
    Example:
        >>> safe_parse_float("3.14").unwrap()
        3.14
    """
    try:
        return Ok(float(s))
    except ValueError:
        return Error(err)


# =============================================================================
# 上下文管理器
# =============================================================================

class ResultContext:
    """
    Result 上下文管理器
    
    用于在上下文中自动捕获异常并转换为 Result。
    
    Example:
        >>> with ResultContext() as result:
        ...     value = int("42")
        ...     result.set_ok(value)
        >>> result.value.is_ok()
        True
    """
    
    def __init__(self):
        self._result: Optional[Result[T, Exception]] = None
    
    def __enter__(self) -> 'ResultContext':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._result = Error(exc_val)
            return True  # 抑制异常
        return False
    
    def set_ok(self, value: T) -> None:
        """设置成功结果"""
        self._result = Ok(value)
    
    def get_result(self, default_error: str = "no result set") -> Result[T, Union[Exception, str]]:
        """获取结果"""
        if self._result is None:
            return Error(default_error)
        return self._result
    
    @property
    def result(self) -> Optional[Result[T, Exception]]:
        """获取结果"""
        return self._result


# =============================================================================
# 异步支持
# =============================================================================

async def try_call_async(func: Callable[..., T], *args, **kwargs) -> Result[T, Exception]:
    """
    异步尝试调用函数
    
    Args:
        func: 要调用的函数
        *args: 函数参数
        **kwargs: 函数关键字参数
    
    Returns:
        Ok(result) 或 Error(exception)
    
    Example:
        >>> async def fetch_data():
        ...     return await try_call_async(requests.get, "https://api.example.com")
    """
    try:
        result = func(*args, **kwargs)
        if hasattr(result, '__await__'):
            result = await result
        return Ok(result)
    except Exception as e:
        return Error(e)


def from_exception_async(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    """
    将可能抛出异常的异步函数转换为返回 Result 的函数
    
    Args:
        func: 可能抛出异常的异步函数
    
    Returns:
        返回 Result 的包装函数
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Result[T, Exception]:
        try:
            result = func(*args, **kwargs)
            if hasattr(result, '__await__'):
                result = await result
            return Ok(result)
        except Exception as e:
            return Error(e)
    return wrapper


# =============================================================================
# 调试和日志工具
# =============================================================================

def result_trace(result: Result[T, E], include_stack: bool = False) -> Dict[str, Any]:
    """
    获取 Result 的调试信息
    
    Args:
        result: Result 类型
        include_stack: 是否包含堆栈信息
    
    Returns:
        调试信息字典
    """
    info = {
        "type": "Ok" if result.is_ok() else "Error",
        "value": result.ok() if result.is_ok() else result.err(),
    }
    
    if include_stack and result.is_error():
        err = result.unwrap_error()
        if isinstance(err, Exception):
            info["stack_trace"] = traceback.format_exception(type(err), err, err.__traceback__)
    
    return info


def pretty_result(result: Result[T, E]) -> str:
    """
    格式化 Result 为可读字符串
    
    Args:
        result: Result 类型
    
    Returns:
        格式化字符串
    """
    if result.is_ok():
        return f"✓ Ok: {result.unwrap()!r}"
    return f"✗ Error: {result.unwrap_error()!r}"


# =============================================================================
# 类型检查工具
# =============================================================================

def is_ok(value: Any) -> bool:
    """检查是否为 Ok 类型"""
    return isinstance(value, Ok)


def is_error(value: Any) -> bool:
    """检查是否为 Error 类型"""
    return isinstance(value, Error)


def is_result(value: Any) -> bool:
    """检查是否为 Result 类型"""
    return isinstance(value, (Ok, Error))


def is_left(value: Any) -> bool:
    """检查是否为 Left 类型"""
    return isinstance(value, Left)


def is_right(value: Any) -> bool:
    """检查是否为 Right 类型"""
    return isinstance(value, Right)


def is_either(value: Any) -> bool:
    """检查是否为 Either 类型"""
    return isinstance(value, (Left, Right))


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    # 类型
    'Ok', 'Error', 'Result', 'Left', 'Right', 'Either',
    # 异常
    'UnwrapError',
    # 创建函数
    'ok', 'error', 'left', 'right',
    # 转换函数
    'from_optional', 'from_exception', 'from_exception_async',
    'result_to_either', 'either_to_result', 'flatten_result',
    # 尝试函数
    'try_call', 'try_call_with', 'try_call_async',
    # 收集函数
    'collect_results', 'partition_results', 'first_ok',
    # 安全操作
    'safe_get', 'safe_index', 'safe_divide', 
    'safe_parse_int', 'safe_parse_float',
    # 上下文管理器
    'ResultContext',
    # 调试工具
    'result_trace', 'pretty_result',
    # 类型检查
    'is_ok', 'is_error', 'is_result',
    'is_left', 'is_right', 'is_either',
]