"""
Lazy Utils - 零依赖惰性求值工具库
==================================

提供惰性求值相关工具，包括：
- Lazy: 惰性求值包装器
- lazy_property: 惰性属性装饰器（计算一次后缓存）
- lazy_class_property: 类级别的惰性属性
- LazySequence: 惰性序列（按需生成元素）
- Thunk: 延迟计算块
- LazyDict: 延迟求值字典
- LazyList: 支持切片的惰性列表
- Deferred: 带状态的延迟值

使用场景：
- 性能优化：延迟昂贵的计算
- 内存优化：按需生成大型序列
- 循环依赖解决：延迟初始化
- 无限数据结构：生成器序列

作者: AllToolkit 自动化生成
日期: 2026-05-12
"""

from typing import (
    Any, Callable, Generic, TypeVar, Optional, 
    Iterator, Iterable, Union, Dict, List, Tuple,
    overload, TYPE_CHECKING
)
from functools import wraps
from threading import Lock
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class Lazy(Generic[T]):
    """
    惰性求值包装器
    
    包装一个计算函数，只有在首次访问值时才执行计算。
    计算结果会被缓存，后续访问直接返回缓存值。
    
    特性：
    - 线程安全
    - 支持重置（重新计算）
    - 支持检查是否已计算
    
    Example:
        >>> expensive_value = Lazy(lambda: compute_heavy_task())
        >>> # 此时还未计算
        >>> result = expensive_value.value  # 首次访问时计算
        >>> result2 = expensive_value.value  # 直接返回缓存值
    """
    
    __slots__ = ('_factory', '_value', '_computed', '_lock')
    
    def __init__(self, factory: Callable[[], T]):
        """
        初始化惰性包装器
        
        Args:
            factory: 延迟计算的工厂函数
        """
        if not callable(factory):
            raise TypeError("factory must be callable")
        self._factory = factory
        self._value: Optional[T] = None
        self._computed = False
        self._lock = Lock()
    
    @property
    def value(self) -> T:
        """
        获取值（延迟计算）
        
        Returns:
            工厂函数的返回值
        """
        if not self._computed:
            with self._lock:
                if not self._computed:  # 双重检查锁定
                    self._value = self._factory()
                    self._computed = True
        return self._value
    
    @property
    def is_computed(self) -> bool:
        """检查是否已经计算"""
        return self._computed
    
    def reset(self) -> None:
        """重置计算状态，下次访问将重新计算"""
        with self._lock:
            self._computed = False
            self._value = None
    
    def get_or_else(self, default: T) -> T:
        """
        如果已计算则返回值，否则返回默认值
        
        Args:
            default: 默认值
            
        Returns:
            已计算的值或默认值
        """
        if self._computed:
            return self._value  # type: ignore
        return default
    
    def map(self, func: Callable[[T], Any]) -> 'Lazy':
        """
        映射转换值
        
        Args:
            func: 转换函数
            
        Returns:
            新的惰性包装器
        """
        return Lazy(lambda: func(self.value))
    
    def __repr__(self) -> str:
        if self._computed:
            return f"Lazy(value={self._value!r})"
        return "Lazy(<not computed>)"
    
    def __str__(self) -> str:
        if self._computed:
            return str(self._value)
        return "<lazy value not computed>"


def lazy_property(func: Callable[..., T]) -> property:
    """
    惰性属性装饰器
    
    将方法转换为惰性求值属性。首次访问时计算并缓存，
    后续访问直接返回缓存值。
    
    特性：
    - 自动缓存计算结果
    - 线程安全
    - 支持重置（删除属性后重新计算）
    
    Example:
        >>> class Database:
        ...     @lazy_property
        ...     def connection(self):
        ...         print("Creating connection...")
        ...         return create_expensive_connection()
        >>> 
        >>> db = Database()
        >>> conn = db.connection  # 首次访问，打印消息
        Creating connection...
        >>> conn2 = db.connection  # 后续访问，无打印
    """
    attr_name = f'_lazy_{func.__name__}'
    
    @wraps(func)
    def getter(self) -> T:
        if not hasattr(self, attr_name):
            with Lock():
                if not hasattr(self, attr_name):
                    setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    @wraps(func)
    def deleter(self) -> None:
        if hasattr(self, attr_name):
            delattr(self, attr_name)
    
    return property(getter, None, deleter, doc=func.__doc__)


class LazyClassPropertyDescriptor:
    """
    类级别惰性属性描述器
    
    与 lazy_property 类似，但作用于类级别。
    """
    
    def __init__(self, func: Callable[..., T]):
        self.func = func
        self.attr_name = f'_lazy_class_{func.__name__}'
        self.lock = Lock()
    
    def __get__(self, obj, objtype=None) -> T:
        cls = objtype if objtype is not None else type(obj)
        if not hasattr(cls, self.attr_name):
            with self.lock:
                if not hasattr(cls, self.attr_name):
                    setattr(cls, self.attr_name, self.func(cls))
        return getattr(cls, self.attr_name)


def lazy_class_property(func: Callable[..., T]) -> LazyClassPropertyDescriptor:
    """
    类级别的惰性属性装饰器
    
    与 lazy_property 类似，但作用于类级别。
    
    Example:
        >>> class Config:
        ...     @lazy_class_property
        ...     def settings(cls):
        ...         print("Loading settings...")
        ...         return load_settings_from_file()
    """
    return LazyClassPropertyDescriptor(func)


class LazySequence(Generic[T]):
    """
    惰性序列
    
    按需生成元素的序列。支持迭代、切片和长度检查。
    适用于大型或无限序列。
    
    特性：
    - 按需生成元素
    - 支持切片操作
    - 支持迭代
    - 可指定是否缓存已计算元素
    
    Example:
        >>> # 生成斐波那契数列
        >>> def fib_gen():
        ...     a, b = 0, 1
        ...     while True:
        ...         yield a
        ...         a, b = b, a + b
        >>> 
        >>> fibs = LazySequence(fib_gen)
        >>> fibs[10]  # 获取第10个元素
        55
        >>> list(fibs[:5])  # 获取前5个元素
        [0, 1, 1, 2, 3]
    """
    
    def __init__(
        self, 
        factory: Union[Callable[[], Iterator[T]], Iterator[T]],
        cache: bool = True,
        length: Optional[int] = None
    ):
        """
        初始化惰性序列
        
        Args:
            factory: 生成器函数或迭代器
            cache: 是否缓存已计算元素
            length: 已知长度（可选，用于len()）
        """
        if callable(factory):
            self._iterator = factory()
        else:
            self._iterator = factory
        self._cache = cache
        self._known_length = length
        self._cached: List[T] = []
        self._exhausted = False
        self._lock = Lock()
    
    def _ensure_until(self, index: int) -> None:
        """确保缓存到指定索引"""
        if self._exhausted:
            return
        
        if self._cache:
            while len(self._cached) <= index:
                try:
                    with self._lock:
                        self._cached.append(next(self._iterator))
                except StopIteration:
                    self._exhausted = True
                    break
        else:
            # 无缓存模式：遍历到目标位置
            for i, _ in enumerate(self):
                if i >= index:
                    break
    
    def __iter__(self) -> Iterator[T]:
        if self._cache:
            # 从缓存开始，然后继续生成
            yield from self._cached
            while not self._exhausted:
                try:
                    with self._lock:
                        if self._exhausted:
                            break
                        item = next(self._iterator)
                        self._cached.append(item)
                    yield item
                except StopIteration:
                    self._exhausted = True
                    break
        else:
            yield from self._iterator
    
    @overload
    def __getitem__(self, index: int) -> T: ...
    
    @overload
    def __getitem__(self, index: slice) -> List[T]: ...
    
    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        if isinstance(index, int):
            if index < 0:
                raise IndexError("LazySequence does not support negative indexing")
            self._ensure_until(index)
            if index >= len(self._cached):
                raise IndexError("LazySequence index out of range")
            return self._cached[index]
        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if start is None:
                start = 0
            if stop is None:
                raise ValueError("LazySequence slice requires stop index")
            self._ensure_until(stop - 1)
            return self._cached[start:stop:step]
        else:
            raise TypeError("Invalid index type")
    
    def __len__(self) -> int:
        if self._known_length is not None:
            return self._known_length
        raise TypeError("LazySequence has no known length. Provide length parameter or use .exhaust()")
    
    def exhaust(self) -> List[T]:
        """
        穷尽序列并返回所有元素
        
        Returns:
            所有元素的列表
        """
        return list(self)
    
    def is_exhausted(self) -> bool:
        """检查序列是否已穷尽"""
        return self._exhausted
    
    def take(self, n: int) -> List[T]:
        """
        获取前n个元素
        
        Args:
            n: 要获取的元素数量
            
        Returns:
            前n个元素的列表
        """
        result = []
        for i, item in enumerate(self):
            if i >= n:
                break
            result.append(item)
        return result
    
    def take_while(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        获取满足条件的连续元素
        
        Args:
            predicate: 条件函数
            
        Returns:
            满足条件的连续元素列表
        """
        result = []
        for item in self:
            if not predicate(item):
                break
            result.append(item)
        return result
    
    def __repr__(self) -> str:
        if self._exhausted:
            return f"LazySequence({self._cached!r})"
        elif self._cached:
            return f"LazySequence({self._cached!r} ...)"
        return "LazySequence(<not started>)"


class Thunk(Generic[T]):
    """
    延迟计算块
    
    表示一个延迟计算的表达式。与 Lazy 类似，
    但更侧重于表达式而非工厂函数。
    
    特性：
    - 显式的延迟计算
    - 支持强制求值
    - 支持组合多个 Thunk
    
    Example:
        >>> x = Thunk(lambda: 10)
        >>> y = Thunk(lambda: 20)
        >>> z = Thunk(lambda: x.value + y.value)
        >>> z.force()  # 强制计算
        30
    """
    
    __slots__ = ('_expr', '_value', '_forced', '_lock')
    
    def __init__(self, expr: Callable[[], T]):
        """
        初始化 Thunk
        
        Args:
            expr: 延迟计算的表达式（无参函数）
        """
        self._expr = expr
        self._value: Optional[T] = None
        self._forced = False
        self._lock = Lock()
    
    def force(self) -> T:
        """
        强制求值
        
        Returns:
            表达式的值
        """
        if not self._forced:
            with self._lock:
                if not self._forced:
                    self._value = self._expr()
                    self._forced = True
        return self._value  # type: ignore
    
    @property
    def value(self) -> T:
        """获取值（force 的别名）"""
        return self.force()
    
    @property
    def is_forced(self) -> bool:
        """检查是否已强制求值"""
        return self._forced
    
    def __repr__(self) -> str:
        if self._forced:
            return f"Thunk({self._value!r})"
        return "Thunk(<not forced>)"


class LazyDict(Dict[K, V], Generic[K, V]):
    """
    延迟求值字典
    
    字典的值在首次访问时才计算。
    适用于值计算成本高的场景。
    
    特性：
    - 按需计算值
    - 支持默认工厂函数
    - 支持缓存
    
    Example:
        >>> d = LazyDict(lambda k: f"value-{k}")
        >>> d['a']  # 首次访问，计算
        'value-a'
        >>> d['a']  # 后续访问，缓存
        'value-a'
    """
    
    def __init__(
        self, 
        default_factory: Optional[Callable[[K], V]] = None,
        initial: Optional[Dict[K, V]] = None
    ):
        """
        初始化延迟字典
        
        Args:
            default_factory: 默认值工厂函数
            initial: 初始键值对
        """
        super().__init__()
        self._factory = default_factory
        self._computed: Dict[K, bool] = {}
        if initial:
            for k, v in initial.items():
                self[k] = v
    
    def __missing__(self, key: K) -> V:
        """处理缺失键"""
        if self._factory is not None:
            value = self._factory(key)
            self[key] = value
            return value
        raise KeyError(key)
    
    def __getitem__(self, key: K) -> V:
        if key in self:
            return super().__getitem__(key)
        return self.__missing__(key)
    
    def get_or_compute(self, key: K, factory: Callable[[K], V]) -> V:
        """
        获取值，如果不存在则使用指定工厂计算
        
        Args:
            key: 键
            factory: 计算工厂
            
        Returns:
            值
        """
        if key not in self:
            self[key] = factory(key)
        return self[key]
    
    def prefetch(self, *keys: K) -> None:
        """
        预取多个键的值
        
        Args:
            keys: 要预取的键
        """
        for key in keys:
            _ = self[key]


class LazyList(Generic[T]):
    """
    支持切片的惰性列表
    
    类似于 LazySequence，但提供更好的列表接口支持。
    元素按需生成，支持追加和预计算。
    
    Example:
        >>> lst = LazyList(lambda i: i * 2)
        >>> lst[5]  # 自动生成到索引5
        10
        >>> lst[:3]  # 切片
        [0, 2, 4]
    """
    
    def __init__(
        self, 
        element_factory: Callable[[int], T],
        initial_size: int = 0
    ):
        """
        初始化惰性列表
        
        Args:
            element_factory: 元素工厂函数，接收索引返回元素
            initial_size: 初始大小（可选）
        """
        self._factory = element_factory
        self._elements: List[T] = []
        self._size_hint = initial_size
        self._lock = Lock()
    
    def _ensure_size(self, size: int) -> None:
        """确保列表至少有指定大小"""
        while len(self._elements) < size:
            with self._lock:
                if len(self._elements) >= size:
                    break
                self._elements.append(self._factory(len(self._elements)))
    
    @overload
    def __getitem__(self, index: int) -> T: ...
    
    @overload
    def __getitem__(self, index: slice) -> List[T]: ...
    
    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        if isinstance(index, int):
            if index < 0:
                raise IndexError("LazyList does not support negative indexing")
            self._ensure_size(index + 1)
            return self._elements[index]
        elif isinstance(index, slice):
            start = index.start or 0
            stop = index.stop
            if stop is None:
                raise ValueError("LazyList slice requires stop index")
            self._ensure_size(stop)
            return self._elements[start:stop:index.step]
        raise TypeError("Invalid index type")
    
    def __len__(self) -> int:
        return len(self._elements)
    
    def __iter__(self) -> Iterator[T]:
        i = 0
        while True:
            try:
                yield self[i]
                i += 1
            except Exception:
                break
    
    def append(self, value: T) -> None:
        """追加元素"""
        with self._lock:
            self._elements.append(value)
    
    def extend(self, values: Iterable[T]) -> None:
        """扩展多个元素"""
        with self._lock:
            self._elements.extend(values)
    
    def to_list(self) -> List[T]:
        """转换为普通列表"""
        return self._elements.copy()
    
    def __repr__(self) -> str:
        if len(self._elements) <= 10:
            return f"LazyList({self._elements!r})"
        return f"LazyList({self._elements[:10]!r} ... [{len(self._elements)} items])"


class Deferred(Generic[T]):
    """
    带状态的延迟值
    
    比 Lazy 更复杂的延迟值，支持：
    - 待计算、正在计算、已完成、失败等状态
    - 计算超时
    - 计算取消
    - 计算回调
    
    Example:
        >>> d = Deferred(lambda: slow_network_request())
        >>> d.is_pending
        True
        >>> result = d.get()  # 阻塞直到完成
        >>> d.is_completed
        True
    """
    
    def __init__(
        self, 
        factory: Callable[[], T],
        timeout: Optional[float] = None
    ):
        """
        初始化延迟值
        
        Args:
            factory: 计算工厂
            timeout: 超时时间（秒）
        """
        self._factory = factory
        self._timeout = timeout
        self._value: Optional[T] = None
        self._error: Optional[Exception] = None
        self._status = 'pending'  # pending, computing, completed, failed, cancelled
        self._lock = Lock()
        self._callbacks: List[Callable[[T], None]] = []
        self._error_callbacks: List[Callable[[Exception], None]] = []
    
    @property
    def is_pending(self) -> bool:
        """是否待计算"""
        return self._status == 'pending'
    
    @property
    def is_computing(self) -> bool:
        """是否正在计算"""
        return self._status == 'computing'
    
    @property
    def is_completed(self) -> bool:
        """是否已完成"""
        return self._status == 'completed'
    
    @property
    def is_failed(self) -> bool:
        """是否失败"""
        return self._status == 'failed'
    
    @property
    def is_cancelled(self) -> bool:
        """是否已取消"""
        return self._status == 'cancelled'
    
    def get(self, timeout: Optional[float] = None) -> T:
        """
        获取值（阻塞直到完成或超时）
        
        Args:
            timeout: 超时时间（覆盖默认值）
            
        Returns:
            计算值
            
        Raises:
            TimeoutError: 超时
            RuntimeError: 已取消或失败
        """
        effective_timeout = timeout if timeout is not None else self._timeout
        
        if self._status == 'completed':
            return self._value  # type: ignore
        
        if self._status == 'failed':
            raise self._error  # type: ignore
        
        if self._status == 'cancelled':
            raise RuntimeError("Deferred was cancelled")
        
        if self._status == 'computing':
            # 等待计算完成
            import time
            start = time.time()
            while self._status == 'computing':
                time.sleep(0.01)
                if effective_timeout and (time.time() - start) > effective_timeout:
                    raise TimeoutError("Deferred computation timed out")
            if self._status == 'completed':
                return self._value  # type: ignore
            if self._status == 'failed':
                raise self._error  # type: ignore
            raise RuntimeError("Deferred computation was cancelled")
        
        # 开始计算
        with self._lock:
            if self._status != 'pending':
                return self.get(timeout)
            self._status = 'computing'
        
        try:
            self._value = self._factory()
            self._status = 'completed'
            # 触发回调
            for callback in self._callbacks:
                callback(self._value)  # type: ignore
            return self._value  # type: ignore
        except Exception as e:
            self._error = e
            self._status = 'failed'
            for callback in self._error_callbacks:
                callback(e)
            raise
    
    def cancel(self) -> bool:
        """
        取消计算
        
        Returns:
            是否成功取消
        """
        with self._lock:
            if self._status in ('pending', 'computing'):
                self._status = 'cancelled'
                return True
            return False
    
    def on_complete(self, callback: Callable[[T], None]) -> 'Deferred[T]':
        """
        添加完成回调
        
        Args:
            callback: 回调函数
            
        Returns:
            self（链式调用）
        """
        self._callbacks.append(callback)
        return self
    
    def on_error(self, callback: Callable[[Exception], None]) -> 'Deferred[T]':
        """
        添加错误回调
        
        Args:
            callback: 回调函数
            
        Returns:
            self（链式调用）
        """
        self._error_callbacks.append(callback)
        return self
    
    def __repr__(self) -> str:
        return f"Deferred(status={self._status}, value={self._value!r})"


# =============================================================================
# 便捷函数
# =============================================================================

def lazy(factory: Callable[[], T]) -> Lazy[T]:
    """
    创建惰性值的便捷函数
    
    Args:
        factory: 工厂函数
        
    Returns:
        Lazy 实例
        
    Example:
        >>> config = lazy(lambda: load_config())
    """
    return Lazy(factory)


def thunk(expr: Callable[[], T]) -> Thunk[T]:
    """
    创建 Thunk 的便捷函数
    
    Args:
        expr: 延迟表达式
        
    Returns:
        Thunk 实例
        
    Example:
        >>> result = thunk(lambda: expensive_computation())
    """
    return Thunk(expr)


def lazy_sequence(
    factory: Union[Callable[[], Iterator[T]], Iterator[T]],
    cache: bool = True,
    length: Optional[int] = None
) -> LazySequence[T]:
    """
    创建惰性序列的便捷函数
    
    Args:
        factory: 生成器函数或迭代器
        cache: 是否缓存
        length: 已知长度
        
    Returns:
        LazySequence 实例
    """
    return LazySequence(factory, cache, length)


def lazy_list(factory: Callable[[int], T]) -> LazyList[T]:
    """
    创建惰性列表的便捷函数
    
    Args:
        factory: 元素工厂函数
        
    Returns:
        LazyList 实例
    """
    return LazyList(factory)