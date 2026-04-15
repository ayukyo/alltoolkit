# -*- coding: utf-8 -*-
"""
AllToolkit - Functional Programming Utilities 🧩

零依赖函数式编程工具库，提供柯里化、函数组合、管道、偏函数、记忆化等功能。
完全使用 Python 标准库实现（functools, inspect, typing），无需任何外部依赖。

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import functools
import inspect
from typing import (
    Any, Callable, Dict, List, Optional, Tuple, TypeVar, 
    Union, Iterable, Iterator, Generic, Type
)
from collections.abc import Mapping, Sequence


# =============================================================================
# 类型定义
# =============================================================================

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
R = TypeVar('R')

FuncType = Callable[..., R]


# =============================================================================
# 柯里化 (Currying)
# =============================================================================

def curry(func: Callable) -> Callable:
    """
    将函数转换为柯里化形式
    
    柯里化允许你部分应用函数的参数，返回一个新函数接受剩余参数。
    
    Args:
        func: 要柯里化的函数
    
    Returns:
        柯里化后的函数
    
    Example:
        >>> def add(a, b, c):
        ...     return a + b + c
        >>> curried_add = curry(add)
        >>> curried_add(1)(2)(3)
        6
        >>> curried_add(1)(2, 3)
        6
        >>> curried_add(1, 2)(3)
        6
    """
    sig = inspect.signature(func)
    param_count = len([p for p in sig.parameters.values() 
                       if p.default is p.empty and p.kind not in (inspect.Parameter.VAR_POSITIONAL, 
                                                                   inspect.Parameter.VAR_KEYWORD)])
    
    @functools.wraps(func)
    def _curry(*args, **kwargs):
        # 检查是否所有必需参数都已提供
        try:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            # 所有参数都已提供，调用原函数
            return func(*bound.args, **bound.kwargs)
        except TypeError:
            # 参数不足，返回新函数
            @functools.wraps(func)
            def _next(*more_args, **more_kwargs):
                new_args = args + more_args
                new_kwargs = {**kwargs, **more_kwargs}
                return _curry(*new_args, **new_kwargs)
            return _next
    
    return _curry


def curry_n(func: Callable, n: Optional[int] = None) -> Callable:
    """
    将函数转换为固定元数的柯里化形式
    
    Args:
        func: 要柯里化的函数
        n: 期望的参数数量（None 表示自动检测）
    
    Returns:
        柯里化后的函数
    
    Example:
        >>> def add(a, b, c):
        ...     return a + b + c
        >>> curried = curry_n(add, 3)
        >>> curried(1)(2)(3)
        6
    """
    if n is None:
        sig = inspect.signature(func)
        n = len([p for p in sig.parameters.values() 
                 if p.default is p.empty and p.kind not in (inspect.Parameter.VAR_POSITIONAL, 
                                                             inspect.Parameter.VAR_KEYWORD)])
    
    @functools.wraps(func)
    def _curry(*args):
        if len(args) >= n:
            return func(*args[:n])
        return lambda *more: _curry(*(args + more))
    
    return _curry


# =============================================================================
# 函数组合 (Function Composition)
# =============================================================================

def compose(*functions: Callable) -> Callable:
    """
    从右到左组合多个函数
    
    compose(f, g, h)(x) = f(g(h(x)))
    
    Args:
        *functions: 要组合的函数列表
    
    Returns:
        组合后的函数
    
    Example:
        >>> def double(x): return x * 2
        >>> def add_one(x): return x + 1
        >>> def square(x): return x ** 2
        >>> compose(square, add_one, double)(3)
        49  # square(add_one(double(3))) = square(7) = 49
    """
    if not functions:
        return lambda x: x
    
    def _compose(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    
    return _compose


def compose_left(*functions: Callable) -> Callable:
    """
    从左到右组合多个函数（管道风格）
    
    compose_left(f, g, h)(x) = h(g(f(x)))
    
    Args:
        *functions: 要组合的函数列表
    
    Returns:
        组合后的函数
    
    Example:
        >>> def double(x): return x * 2
        >>> def add_one(x): return x + 1
        >>> compose_left(double, add_one)(3)
        7  # add_one(double(3)) = add_one(6) = 7
    """
    return compose(*reversed(functions))


def pipe(*functions: Callable) -> Callable:
    """
    创建管道（别名，与 compose_left 相同）
    
    pipe(f, g, h)(x) = h(g(f(x)))
    
    Args:
        *functions: 要组合的函数列表
    
    Returns:
        管道函数
    
    Example:
        >>> pipe(
        ...     lambda x: x * 2,
        ...     lambda x: x + 1,
        ...     lambda x: x ** 2
        ... )(3)
        49  # ((3 * 2) + 1) ** 2 = 49
    """
    return compose_left(*functions)


# =============================================================================
# 偏函数 (Partial Application)
# =============================================================================

def partial(func: Callable, *args, **kwargs) -> Callable:
    """
    创建偏函数（functools.partial 的增强版）
    
    固定函数的部分参数，返回一个新函数。
    
    Args:
        func: 原函数
        *args: 位置参数
        **kwargs: 关键字参数
    
    Returns:
        偏函数
    
    Example:
        >>> def multiply(a, b, c):
        ...     return a * b * c
        >>> double = partial(multiply, 2)
        >>> double(3, 4)
        24
    """
    @functools.wraps(func)
    def _partial(*more_args, **more_kwargs):
        new_kwargs = {**kwargs, **more_kwargs}
        return func(*args, *more_args, **new_kwargs)
    return _partial


def partial_right(func: Callable, *args, **kwargs) -> Callable:
    """
    从右侧绑定参数的偏函数
    
    Args:
        func: 原函数
        *args: 要绑定的位置参数（从右侧开始）
        **kwargs: 关键字参数
    
    Returns:
        偏函数
    
    Example:
        >>> def divide(a, b):
        ...     return a / b
        >>> divide_by_2 = partial_right(divide, 2)
        >>> divide_by_2(10)
        5.0
    """
    @functools.wraps(func)
    def _wrapped(*more_args, **more_kwargs):
        new_kwargs = {**kwargs, **more_kwargs}
        return func(*more_args, *args, **new_kwargs)
    return _wrapped


def flip(func: Callable) -> Callable:
    """
    翻转函数的前两个参数
    
    Args:
        func: 原函数
    
    Returns:
        参数翻转后的函数
    
    Example:
        >>> def greet(greeting, name):
        ...     return f"{greeting}, {name}!"
        >>> flipped = flip(greet)
        >>> flipped("Alice", "Hello")
        'Hello, Alice!'
    """
    @functools.wraps(func)
    def _flipped(a, b, *args, **kwargs):
        return func(b, a, *args, **kwargs)
    return _flipped


# =============================================================================
# 记忆化 (Memoization)
# =============================================================================

def memoize(func: Callable) -> Callable:
    """
    为函数添加记忆化缓存
    
    缓存函数的返回值，避免重复计算。
    
    Args:
        func: 要记忆化的函数
    
    Returns:
        带缓存的函数
    
    Example:
        >>> @memoize
        ... def fibonacci(n):
        ...     if n < 2:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        >>> fibonacci(10)
        55
        >>> fibonacci(10)  # 从缓存获取
        55
    """
    cache: Dict[Tuple, Any] = {}
    
    @functools.wraps(func)
    def _memoized(*args, **kwargs):
        # 创建缓存键
        key = (args, tuple(sorted(kwargs.items())))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    _memoized.cache = cache
    _memoized.cache_clear = lambda: cache.clear()
    _memoized.cache_info = lambda: len(cache)
    
    return _memoized


def memoize_with_ttl(ttl_seconds: int) -> Callable:
    """
    带过期时间的记忆化装饰器
    
    Args:
        ttl_seconds: 缓存过期时间（秒）
    
    Returns:
        装饰器
    
    Example:
        >>> @memoize_with_ttl(60)
        ... def get_data(key):
        ...     return expensive_operation(key)
    """
    import time
    
    def decorator(func: Callable) -> Callable:
        cache: Dict[Tuple, Tuple[Any, float]] = {}
        
        @functools.wraps(func)
        def _memoized(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()
            
            if key in cache:
                value, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    return value
                del cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        _memoized.cache = cache
        _memoized.cache_clear = lambda: cache.clear()
        
        return _memoized
    
    return decorator


# =============================================================================
# 惰性求值 (Lazy Evaluation)
# =============================================================================

class Lazy(Generic[T]):
    """
    惰性求值包装器
    
    延迟计算直到首次访问值。
    
    Example:
        >>> lazy_val = Lazy(lambda: expensive_computation())
        >>> # 计算尚未执行
        >>> result = lazy_val.value  # 现在才执行计算
    """
    
    def __init__(self, factory: Callable[[], T]):
        self._factory = factory
        self._computed = False
        self._value: Optional[T] = None
    
    @property
    def value(self) -> T:
        if not self._computed:
            self._value = self._factory()
            self._computed = True
        return self._value
    
    def reset(self):
        """重置缓存，下次访问时重新计算"""
        self._computed = False
        self._value = None
    
    def __repr__(self):
        if self._computed:
            return f"Lazy(computed={self._value!r})"
        return "Lazy(<not computed>)"


def lazy(func: Callable[[], T]) -> Lazy[T]:
    """
    创建惰性求值对象
    
    Args:
        func: 无参工厂函数
    
    Returns:
        Lazy 对象
    """
    return Lazy(func)


# =============================================================================
# 迭代器工具 (Iterator Utilities)
# =============================================================================

def take(n: int, iterable: Iterable[T]) -> List[T]:
    """
    从迭代器中取前 n 个元素
    
    Args:
        n: 要取的元素数量
        iterable: 可迭代对象
    
    Returns:
        元素列表
    
    Example:
        >>> take(3, [1, 2, 3, 4, 5])
        [1, 2, 3]
    """
    result = []
    for i, item in enumerate(iterable):
        if i >= n:
            break
        result.append(item)
    return result


def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> List[T]:
    """
    从迭代器中取元素，直到条件不满足
    
    Args:
        predicate: 条件函数
        iterable: 可迭代对象
    
    Returns:
        元素列表
    
    Example:
        >>> take_while(lambda x: x < 5, [1, 2, 3, 6, 7])
        [1, 2, 3]
    """
    result = []
    for item in iterable:
        if not predicate(item):
            break
        result.append(item)
    return result


def drop(n: int, iterable: Iterable[T]) -> List[T]:
    """
    从迭代器中丢弃前 n 个元素，返回剩余元素
    
    Args:
        n: 要丢弃的元素数量
        iterable: 可迭代对象
    
    Returns:
        剩余元素列表
    
    Example:
        >>> drop(2, [1, 2, 3, 4, 5])
        [3, 4, 5]
    """
    iterator = iter(iterable)
    for _ in range(n):
        next(iterator, None)
    return list(iterator)


def drop_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> List[T]:
    """
    从迭代器中丢弃元素，直到条件不满足，返回剩余元素
    
    Args:
        predicate: 条件函数
        iterable: 可迭代对象
    
    Returns:
        剩余元素列表
    
    Example:
        >>> drop_while(lambda x: x < 3, [1, 2, 3, 4, 5])
        [3, 4, 5]
    """
    iterator = iter(iterable)
    for item in iterator:
        if not predicate(item):
            return [item] + list(iterator)
    return []


def iterate(func: Callable[[T], T], initial: T, count: Optional[int] = None) -> Iterator[T]:
    """
    生成迭代序列：initial, func(initial), func(func(initial)), ...
    
    Args:
        func: 转换函数
        initial: 初始值
        count: 生成数量（None 表示无限）
    
    Yields:
        迭代生成的值
    
    Example:
        >>> list(iterate(lambda x: x * 2, 1, 5))
        [1, 2, 4, 8, 16]
    """
    current = initial
    yielded = 0
    while count is None or yielded < count:
        yield current
        current = func(current)
        yielded += 1


def flatten(nested: Iterable[Iterable[T]]) -> Iterator[T]:
    """
    展平一层嵌套的迭代器
    
    Args:
        nested: 嵌套的可迭代对象
    
    Yields:
        展平后的元素
    
    Example:
        >>> list(flatten([[1, 2], [3, 4], [5]]))
        [1, 2, 3, 4, 5]
    """
    for inner in nested:
        for item in inner:
            yield item


def flatten_deep(nested: Iterable, max_depth: Optional[int] = None) -> Iterator[Any]:
    """
    深度展平嵌套的迭代器
    
    Args:
        nested: 嵌套的可迭代对象
        max_depth: 最大展平深度（None 表示无限）
    
    Yields:
        展平后的元素
    
    Example:
        >>> list(flatten_deep([1, [2, [3, [4]]]], max_depth=2))
        [1, 2, 3, [4]]
    """
    def _flatten(item, depth):
        # 检查是否达到最大深度
        if max_depth is not None and depth >= max_depth:
            yield item
            return
        
        # 尝试迭代
        try:
            # 字符串和字节不展开
            if isinstance(item, (str, bytes)):
                yield item
                return
            for sub_item in item:
                yield from _flatten(sub_item, depth + 1)
        except TypeError:
            # 不是可迭代对象，直接返回
            yield item
    
    yield from _flatten(nested, 0)


def chunk(n: int, iterable: Iterable[T]) -> Iterator[List[T]]:
    """
    将迭代器分块
    
    Args:
        n: 每块的大小
        iterable: 可迭代对象
    
    Yields:
        大小为 n 的块（最后一块可能小于 n）
    
    Example:
        >>> list(chunk(3, [1, 2, 3, 4, 5, 6, 7]))
        [[1, 2, 3], [4, 5, 6], [7]]
    """
    current_chunk = []
    for item in iterable:
        current_chunk.append(item)
        if len(current_chunk) == n:
            yield current_chunk
            current_chunk = []
    if current_chunk:
        yield current_chunk


def sliding_window(n: int, iterable: Iterable[T]) -> Iterator[List[T]]:
    """
    生成滑动窗口
    
    Args:
        n: 窗口大小
        iterable: 可迭代对象
    
    Yields:
        大小为 n 的滑动窗口
    
    Example:
        >>> list(sliding_window(3, [1, 2, 3, 4, 5]))
        [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    """
    window = []
    iterator = iter(iterable)
    
    # 填充初始窗口
    for item in iterator:
        window.append(item)
        if len(window) == n:
            yield window[:]
            break
    
    # 滑动窗口
    for item in iterator:
        window.pop(0)
        window.append(item)
        yield window[:]


# =============================================================================
# 集合操作 (Collection Operations)
# =============================================================================

def mapcat(func: Callable[[T], Iterable[U]], iterable: Iterable[T]) -> List[U]:
    """
    map + flatten 的组合
    
    Args:
        func: 映射函数（返回可迭代对象）
        iterable: 输入可迭代对象
    
    Returns:
        展平后的结果列表
    
    Example:
        >>> mapcat(lambda x: [x, x * 2], [1, 2, 3])
        [1, 2, 2, 4, 3, 6]
    """
    result = []
    for item in iterable:
        result.extend(func(item))
    return result


def filter_map(func: Callable[[T], Optional[U]], iterable: Iterable[T]) -> List[U]:
    """
    filter + map 的组合
    
    应用函数，过滤掉返回 None 的结果。
    
    Args:
        func: 映射函数（返回 None 表示过滤）
        iterable: 输入可迭代对象
    
    Returns:
        过滤后的结果列表
    
    Example:
        >>> def safe_int(x):
        ...     try:
        ...         return int(x)
        ...     except ValueError:
        ...         return None
        >>> filter_map(safe_int, ['1', 'a', '2', 'b'])
        [1, 2]
    """
    result = []
    for item in iterable:
        mapped = func(item)
        if mapped is not None:
            result.append(mapped)
    return result


def reduce(func: Callable[[U, T], U], iterable: Iterable[T], initial: Optional[U] = None) -> U:
    """
    归约/折叠操作
    
    Args:
        func: 归约函数
        iterable: 输入可迭代对象
        initial: 初始值（可选）
    
    Returns:
        归约结果
    
    Example:
        >>> reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])
        15
        >>> reduce(lambda acc, x: acc * 10 + x, [1, 2, 3], 0)
        123
    """
    iterator = iter(iterable)
    
    if initial is None:
        try:
            accumulator = next(iterator)
        except StopIteration:
            raise TypeError("reduce() of empty sequence with no initial value")
    else:
        accumulator = initial
    
    for item in iterator:
        accumulator = func(accumulator, item)
    
    return accumulator


def reduce_right(func: Callable[[T, U], U], iterable: Iterable[T], initial: Optional[U] = None) -> U:
    """
    从右到左归约
    
    Args:
        func: 归约函数
        iterable: 输入可迭代对象
        initial: 初始值（可选）
    
    Returns:
        归约结果
    
    Example:
        >>> reduce_right(lambda x, acc: str(x) + acc, [1, 2, 3], '')
        '123'
    """
    items = list(iterable)
    
    if initial is None:
        if not items:
            raise TypeError("reduce_right() of empty sequence with no initial value")
        accumulator = items.pop()
    else:
        accumulator = initial
    
    for item in reversed(items):
        accumulator = func(item, accumulator)
    
    return accumulator


def scan(func: Callable[[U, T], U], iterable: Iterable[T], initial: Optional[U] = None) -> List[U]:
    """
    扫描/累积操作（返回所有中间结果）
    
    Args:
        func: 累积函数
        iterable: 输入可迭代对象
        initial: 初始值（可选）
    
    Returns:
        累积结果列表
    
    Example:
        >>> scan(lambda acc, x: acc + x, [1, 2, 3, 4])
        [1, 3, 6, 10]
        >>> scan(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
        [0, 1, 3, 6, 10]
    """
    result = []
    iterator = iter(iterable)
    
    if initial is not None:
        result.append(initial)
        accumulator = initial
    else:
        try:
            accumulator = next(iterator)
            result.append(accumulator)
        except StopIteration:
            return result
    
    for item in iterator:
        accumulator = func(accumulator, item)
        result.append(accumulator)
    
    return result


def partition(pred: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[List[T], List[T]]:
    """
    根据条件将集合分为两部分
    
    Args:
        pred: 条件函数
        iterable: 输入可迭代对象
    
    Returns:
        (满足条件的元素，不满足条件的元素)
    
    Example:
        >>> partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])
        ([2, 4, 6], [1, 3, 5])
    """
    truthy = []
    falsy = []
    for item in iterable:
        if pred(item):
            truthy.append(item)
        else:
            falsy.append(item)
    return truthy, falsy


def group_by(key_func: Callable[[T], U], iterable: Iterable[T]) -> Dict[U, List[T]]:
    """
    根据键函数分组
    
    Args:
        key_func: 键函数
        iterable: 输入可迭代对象
    
    Returns:
        分组字典
    
    Example:
        >>> group_by(len, ['a', 'bb', 'ccc', 'dd'])
        {1: ['a'], 2: ['bb', 'dd'], 3: ['ccc']}
    """
    result: Dict[U, List[T]] = {}
    for item in iterable:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def unique(iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
    """
    去重，保持顺序
    
    Args:
        iterable: 输入可迭代对象
        key: 用于比较的键函数（可选）
    
    Returns:
        去重后的列表
    
    Example:
        >>> unique([1, 2, 2, 3, 1, 4])
        [1, 2, 3, 4]
        >>> unique(['a', 'A', 'b'], key=str.lower)
        ['a', 'b']
    
    Note:
        优化版本：使用 key 函数优化避免重复调用，
        对于不可哈希类型自动降级为 O(n²) 算法。
    """
    seen: set = set()
    result: List[T] = []
    
    # 快速路径：无 key 函数时直接处理
    if key is None:
        for item in iterable:
            try:
                # 尝试哈希，如果成功则使用 set
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            except TypeError:
                # 不可哈希类型，降级为线性查找
                if item not in result:
                    result.append(item)
        return result
    
    # 带 key 函数的路径
    for item in iterable:
        try:
            comparison_key = key(item)
            if comparison_key not in seen:
                seen.add(comparison_key)
                result.append(item)
        except TypeError:
            # key 结果不可哈希，降级处理
            comparison_key = key(item)
            is_duplicate = False
            for existing in result:
                if key(existing) == comparison_key:
                    is_duplicate = True
                    break
            if not is_duplicate:
                result.append(item)
    
    return result


# =============================================================================
# 谓词逻辑 (Predicate Logic)
# =============================================================================

def all_pred(*predicates: Callable[[T], bool]) -> Callable[[T], bool]:
    """
    组合多个谓词，全部为真时才返回真
    
    Args:
        *predicates: 谓词函数列表
    
    Returns:
        组合后的谓词
    
    Example:
        >>> is_positive = lambda x: x > 0
        >>> is_even = lambda x: x % 2 == 0
        >>> check = all_pred(is_positive, is_even)
        >>> check(4)
        True
        >>> check(3)
        False
    """
    def _combined(x: T) -> bool:
        return all(pred(x) for pred in predicates)
    return _combined


def any_pred(*predicates: Callable[[T], bool]) -> Callable[[T], bool]:
    """
    组合多个谓词，任一为真就返回真
    
    Args:
        *predicates: 谓词函数列表
    
    Returns:
        组合后的谓词
    
    Example:
        >>> is_zero = lambda x: x == 0
        >>> is_negative = lambda x: x < 0
        >>> check = any_pred(is_zero, is_negative)
        >>> check(-5)
        True
        >>> check(5)
        False
    """
    def _combined(x: T) -> bool:
        return any(pred(x) for pred in predicates)
    return _combined


def not_pred(predicate: Callable[[T], bool]) -> Callable[[T], bool]:
    """
    谓词取反
    
    Args:
        predicate: 谓词函数
    
    Returns:
        取反后的谓词
    
    Example:
        >>> is_even = lambda x: x % 2 == 0
        >>> is_odd = not_pred(is_even)
        >>> is_odd(3)
        True
    """
    return lambda x: not predicate(x)


def eq(value: Any) -> Callable[[Any], bool]:
    """
    创建等于比较的谓词
    
    Args:
        value: 比较值
    
    Returns:
        谓词函数
    
    Example:
        >>> is_five = eq(5)
        >>> is_five(5)
        True
        >>> is_five(3)
        False
    """
    return lambda x: x == value


def gt(value: Any) -> Callable[[Any], bool]:
    """创建大于比较的谓词"""
    return lambda x: x > value


def lt(value: Any) -> Callable[[Any], bool]:
    """创建小于比较的谓词"""
    return lambda x: x < value


def ge(value: Any) -> Callable[[Any], bool]:
    """创建大于等于比较的谓词"""
    return lambda x: x >= value


def le(value: Any) -> Callable[[Any], bool]:
    """创建小于等于比较的谓词"""
    return lambda x: x <= value


# =============================================================================
# 条件执行 (Conditional Execution)
# =============================================================================

def cond(*clauses: Tuple[Callable[[T], bool], Callable[[T], U]]) -> Callable[[T], Optional[U]]:
    """
    条件执行（类似 cond 表达式）
    
    Args:
        *clauses: (条件函数，结果函数) 元组列表
    
    Returns:
        条件执行函数
    
    Example:
        >>> classify = cond(
        ...     (lambda x: x > 0, lambda x: 'positive'),
        ...     (lambda x: x < 0, lambda x: 'negative'),
        ...     (lambda x: True, lambda x: 'zero'),
        ... )
        >>> classify(5)
        'positive'
        >>> classify(-3)
        'negative'
        >>> classify(0)
        'zero'
    """
    def _cond(x: T) -> Optional[U]:
        for condition, result_func in clauses:
            if condition(x):
                return result_func(x)
        return None
    return _cond


def when(predicate: Callable[[T], bool], func: Callable[[T], U]) -> Callable[[T], Optional[U]]:
    """
    当条件满足时执行函数
    
    Args:
        predicate: 条件函数
        func: 执行函数
    
    Returns:
        条件执行函数
    
    Example:
        >>> log_positive = when(lambda x: x > 0, lambda x: f"{x} is positive")
        >>> log_positive(5)
        '5 is positive'
        >>> log_positive(-3)
        None
    """
    def _when(x: T) -> Optional[U]:
        if predicate(x):
            return func(x)
        return None
    return _when


def unless(predicate: Callable[[T], bool], func: Callable[[T], U]) -> Callable[[T], Optional[U]]:
    """
    当条件不满足时执行函数
    
    Args:
        predicate: 条件函数
        func: 执行函数
    
    Returns:
        条件执行函数
    
    Example:
        >>> log_non_positive = unless(lambda x: x > 0, lambda x: f"{x} is not positive")
        >>> log_non_positive(-3)
        '-3 is not positive'
        >>> log_non_positive(5)
        None
    """
    return when(not_pred(predicate), func)


# =============================================================================
# 实用工具 (Utilities)
# =============================================================================

def identity(x: T) -> T:
    """
    恒等函数
    
    Args:
        x: 任意值
    
    Returns:
        原值
    
    Example:
        >>> identity(5)
        5
    """
    return x


def constantly(value: U) -> Callable[..., U]:
    """
    创建常量函数
    
    Args:
        value: 常量值
    
    Returns:
        总是返回该值的函数
    
    Example:
        >>> always_five = constantly(5)
        >>> always_five()
        5
        >>> always_five(1, 2, 3)
        5
    """
    return lambda *args, **kwargs: value


def tap(func: Callable[[T], Any]) -> Callable[[T], T]:
    """
    调试辅助函数，执行副作用后返回原值
    
    Args:
        func: 副作用函数
    
    Returns:
        包装后的函数
    
    Example:
        >>> result = pipe(
        ...     lambda x: x * 2,
        ...     tap(lambda x: print(f"Debug: {x}")),
        ...     lambda x: x + 1,
        ... )(5)
        Debug: 10
        >>> result
        11
    """
    def _tap(x: T) -> T:
        func(x)
        return x
    return _tap


def noop(*args, **kwargs) -> None:
    """
    空操作函数
    
    Example:
        >>> noop()
        >>> noop(1, 2, 3)
        >>> noop(a=1, b=2)
    """
    pass


def call_times(n: int, func: Callable) -> List[Any]:
    """
    调用函数 n 次
    
    Args:
        n: 调用次数
        func: 要调用的函数
    
    Returns:
        结果列表
    
    Example:
        >>> counter = 0
        >>> def increment():
        ...     global counter
        ...     counter += 1
        ...     return counter
        >>> call_times(3, increment)
        [1, 2, 3]
    """
    return [func() for _ in range(n)]


def apply_to(value: T, *funcs: Callable[[T], Any]) -> List[Any]:
    """
    将值应用到多个函数
    
    Args:
        value: 输入值
        *funcs: 函数列表
    
    Returns:
        结果列表
    
    Example:
        >>> apply_to(5, lambda x: x * 2, lambda x: x + 1, lambda x: x ** 2)
        [10, 6, 25]
    """
    return [func(value) for func in funcs]


# =============================================================================
# 模块导出
# =============================================================================

__all__ = [
    # 柯里化
    'curry',
    'curry_n',
    
    # 函数组合
    'compose',
    'compose_left',
    'pipe',
    
    # 偏函数
    'partial',
    'partial_right',
    'flip',
    
    # 记忆化
    'memoize',
    'memoize_with_ttl',
    
    # 惰性求值
    'Lazy',
    'lazy',
    
    # 迭代器工具
    'take',
    'take_while',
    'drop',
    'drop_while',
    'iterate',
    'flatten',
    'flatten_deep',
    'chunk',
    'sliding_window',
    
    # 集合操作
    'mapcat',
    'filter_map',
    'reduce',
    'reduce_right',
    'scan',
    'partition',
    'group_by',
    'unique',
    
    # 谓词逻辑
    'all_pred',
    'any_pred',
    'not_pred',
    'eq',
    'gt',
    'lt',
    'ge',
    'le',
    
    # 条件执行
    'cond',
    'when',
    'unless',
    
    # 实用工具
    'identity',
    'constantly',
    'tap',
    'noop',
    'call_times',
    'apply_to',
]
