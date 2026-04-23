"""
Pipeline Utils - 数据处理管道工具包

提供可组合的数据处理管道，零外部依赖，仅使用 Python 标准库。

功能:
- Pipeline: 链式数据处理管道
- Step: 单个处理步骤（支持 map/filter/reduce/flat_map/group_by 等）
- 条件分支和错误处理
- 惰性求值支持
- 并行处理支持
- 管道组合和复用
- 内置常用步骤工厂

作者: AllToolkit
日期: 2026-04-23
"""

from typing import (
    Any, Callable, Dict, Generic, Iterable, Iterator, List,
    Optional, Sequence, Tuple, TypeVar, Union
)
from functools import reduce
from itertools import islice, chain
import copy
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


# ============================================================================
# 异常定义
# ============================================================================

class PipelineError(Exception):
    """管道处理错误"""
    def __init__(self, message: str, step_name: str = "", data: Any = None):
        super().__init__(message)
        self.step_name = step_name
        self.data = data


class StepError(PipelineError):
    """步骤执行错误"""
    pass


class ValidationError(PipelineError):
    """验证错误"""
    pass


# ============================================================================
# 步骤实现
# ============================================================================

class BaseStep(Generic[T, U]):
    """基础步骤类"""
    
    def __init__(self, name: str = ""):
        self._name = name or self.__class__.__name__
    
    @property
    def name(self) -> str:
        return self._name
    
    def process(self, data: T) -> U:
        raise NotImplementedError("子类必须实现 process 方法")
    
    def __repr__(self) -> str:
        return f"<Step: {self._name}>"


class MapStep(BaseStep[Iterable[T], Iterable[U]]):
    """映射步骤 - 对每个元素应用函数"""
    
    def __init__(self, func: Callable[[T], U], name: str = ""):
        super().__init__(name or f"Map({func.__name__})")
        self.func = func
    
    def process(self, data: Iterable[T]) -> Iterable[U]:
        return map(self.func, data)


class FilterStep(BaseStep[Iterable[T], Iterable[T]]):
    """过滤步骤 - 筛选满足条件的元素"""
    
    def __init__(self, predicate: Callable[[T], bool], name: str = ""):
        super().__init__(name or f"Filter({predicate.__name__})")
        self.predicate = predicate
    
    def process(self, data: Iterable[T]) -> Iterable[T]:
        return filter(self.predicate, data)


class ReduceStep(BaseStep[Iterable[T], U]):
    """归约步骤 - 将序列归约为单个值"""
    
    def __init__(
        self, 
        func: Callable[[U, T], U], 
        initial: Optional[U] = None,
        name: str = ""
    ):
        super().__init__(name or f"Reduce({func.__name__})")
        self.func = func
        self.initial = initial
    
    def process(self, data: Iterable[T]) -> U:
        if self.initial is not None:
            return reduce(self.func, data, self.initial)
        return reduce(self.func, data)


class FlatMapStep(BaseStep[Iterable[T], Iterable[U]]):
    """扁平映射步骤 - 映射后展平"""
    
    def __init__(self, func: Callable[[T], Iterable[U]], name: str = ""):
        super().__init__(name or f"FlatMap({func.__name__})")
        self.func = func
    
    def process(self, data: Iterable[T]) -> Iterable[U]:
        return chain.from_iterable(map(self.func, data))


class TakeStep(BaseStep[Iterable[T], Iterable[T]]):
    """取前N个元素"""
    
    def __init__(self, n: int, name: str = ""):
        super().__init__(name or f"Take({n})")
        self.n = n
    
    def process(self, data: Iterable[T]) -> Iterable[T]:
        return islice(data, self.n)


class SkipStep(BaseStep[Iterable[T], Iterable[T]]):
    """跳过前N个元素"""
    
    def __init__(self, n: int, name: str = ""):
        super().__init__(name or f"Skip({n})")
        self.n = n
    
    def process(self, data: Iterable[T]) -> Iterable[T]:
        return islice(data, self.n, None)


class GroupByStep(BaseStep[Iterable[T], Dict[Any, List[T]]]):
    """分组步骤"""
    
    def __init__(self, key_func: Callable[[T], Any], name: str = ""):
        super().__init__(name or f"GroupBy({key_func.__name__})")
        self.key_func = key_func
    
    def process(self, data: Iterable[T]) -> Dict[Any, List[T]]:
        result: Dict[Any, List[T]] = {}
        for item in data:
            key = self.key_func(item)
            if key not in result:
                result[key] = []
            result[key].append(item)
        return result


class SortStep(BaseStep[Iterable[T], List[T]]):
    """排序步骤"""
    
    def __init__(
        self, 
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
        name: str = ""
    ):
        super().__init__(name or "Sort")
        self.key = key
        self.reverse = reverse
    
    def process(self, data: Iterable[T]) -> List[T]:
        return sorted(data, key=self.key, reverse=self.reverse)


class UniqueStep(BaseStep[Iterable[T], Iterable[T]]):
    """去重步骤"""
    
    def __init__(self, key: Optional[Callable[[T], Any]] = None, name: str = ""):
        super().__init__(name or "Unique")
        self.key = key
    
    def process(self, data: Iterable[T]) -> Iterable[T]:
        seen: set = set()
        for item in data:
            k = self.key(item) if self.key else item
            if k not in seen:
                seen.add(k)
                yield item


class ChunkStep(BaseStep[Iterable[T], Iterable[List[T]]]):
    """分块步骤 - 将序列分成固定大小的块"""
    
    def __init__(self, size: int, name: str = ""):
        super().__init__(name or f"Chunk({size})")
        if size < 1:
            raise ValueError("块大小必须大于0")
        self.size = size
    
    def process(self, data: Iterable[T]) -> Iterable[List[T]]:
        chunk: List[T] = []
        for item in data:
            chunk.append(item)
            if len(chunk) == self.size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


class ZipStep(BaseStep[Iterable[T], Iterable[Tuple[T, U]]]):
    """配对步骤 - 与另一序列配对"""
    
    def __init__(self, other: Iterable[U], name: str = ""):
        super().__init__(name or "Zip")
        self.other = other
    
    def process(self, data: Iterable[T]) -> Iterable[Tuple[T, U]]:
        return zip(data, self.other)


class EnumerateStep(BaseStep[Iterable[T], Iterable[Tuple[int, T]]]):
    """枚举步骤 - 添加索引"""
    
    def __init__(self, start: int = 0, name: str = ""):
        super().__init__(name or f"Enumerate(start={start})")
        self.start = start
    
    def process(self, data: Iterable[T]) -> Iterable[Tuple[int, T]]:
        return enumerate(data, start=self.start)


class TapStep(BaseStep[Iterable[T], Iterable[T]]):
    """旁路步骤 - 对每个元素执行操作但不修改数据"""
    
    def __init__(self, action: Callable[[T], None], name: str = ""):
        super().__init__(name or f"Tap({action.__name__})")
        self.action = action
    
    def process(self, data: Iterable[T]) -> Iterable[T]:
        for item in data:
            self.action(item)
            yield item


class BatchStep(BaseStep[Iterable[T], Iterable[List[T]]]):
    """批量处理步骤 - 累积后批量处理"""
    
    def __init__(
        self, 
        batch_func: Callable[[List[T]], List[U]],
        batch_size: int = 100,
        name: str = ""
    ):
        super().__init__(name or f"Batch(size={batch_size})")
        self.batch_func = batch_func
        self.batch_size = batch_size
    
    def process(self, data: Iterable[T]) -> Iterable[U]:
        batch: List[T] = []
        for item in data:
            batch.append(item)
            if len(batch) >= self.batch_size:
                yield from self.batch_func(batch)
                batch = []
        if batch:
            yield from self.batch_func(batch)


class ConditionalStep(BaseStep[Iterable[T], Iterable[U]]):
    """条件分支步骤"""
    
    def __init__(
        self,
        condition: Callable[[T], bool],
        true_step: Callable[[T], U],
        false_step: Callable[[T], U],
        name: str = ""
    ):
        super().__init__(name or "Conditional")
        self.condition = condition
        self.true_step = true_step
        self.false_step = false_step
    
    def process(self, data: Iterable[T]) -> Iterable[U]:
        for item in data:
            if self.condition(item):
                yield self.true_step(item)
            else:
                yield self.false_step(item)


class TryCatchStep(BaseStep[Iterable[T], Iterable[U]]):
    """错误捕获步骤"""
    
    def __init__(
        self,
        step: Callable[[T], U],
        on_error: Optional[Callable[[T, Exception], U]] = None,
        name: str = ""
    ):
        super().__init__(name or f"TryCatch({step.__name__})")
        self.step = step
        self.on_error = on_error
    
    def process(self, data: Iterable[T]) -> Iterable[U]:
        for item in data:
            try:
                yield self.step(item)
            except Exception as e:
                if self.on_error:
                    yield self.on_error(item, e)
                else:
                    raise StepError(
                        f"步骤 {self._name} 处理失败: {e}",
                        step_name=self._name,
                        data=item
                    ) from e


class ParallelMapStep(BaseStep[Iterable[T], Iterable[U]]):
    """并行映射步骤 - 使用线程池并行处理"""
    
    def __init__(
        self,
        func: Callable[[T], U],
        max_workers: int = 4,
        name: str = ""
    ):
        super().__init__(name or f"ParallelMap({func.__name__})")
        self.func = func
        self.max_workers = max_workers
    
    def process(self, data: Iterable[T]) -> Iterable[U]:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.func, item) for item in data]
            for future in as_completed(futures):
                yield future.result()


# ============================================================================
# 管道实现
# ============================================================================

class Pipeline(Generic[T]):
    """
    数据处理管道 - 支持链式组合多个处理步骤。
    
    特性:
    - 链式调用，声明式构建
    - 惰性求值（默认）
    - 支持并行处理
    - 可组合和复用
    - 支持错误处理
    
    示例:
        >>> # 基础管道
        >>> result = (
        ...     Pipeline([1, 2, 3, 4, 5])
        ...     .map(lambda x: x * 2)
        ...     .filter(lambda x: x > 4)
        ...     .to_list()
        ... )
        >>> print(result)  # [6, 8, 10]
        
        >>> # 链式处理
        >>> pipeline = (
        ...     Pipeline()
        ...     .map(lambda x: x * 2)
        ...     .filter(lambda x: x > 10)
        ...     .take(5)
        ... )
        >>> result = pipeline.run([5, 6, 7, 8, 9, 10, 11])
    """
    
    def __init__(self, source: Optional[Iterable[T]] = None):
        """
        初始化管道。
        
        Args:
            source: 可选的数据源
        """
        self._source = source
        self._steps: List[BaseStep] = []
        self._lazy: bool = True
    
    # ========================================================================
    # 步骤添加方法
    # ========================================================================
    
    def map(self, func: Callable[[T], U], name: str = "") -> "Pipeline[U]":
        """对每个元素应用函数"""
        self._steps.append(MapStep(func, name))
        return self  # type: ignore
    
    def filter(self, predicate: Callable[[T], bool], name: str = "") -> "Pipeline[T]":
        """过滤满足条件的元素"""
        self._steps.append(FilterStep(predicate, name))
        return self
    
    def reduce(
        self, 
        func: Callable[[U, T], U],
        initial: Optional[U] = None,
        name: str = ""
    ) -> "Pipeline[U]":
        """归约为单个值"""
        self._steps.append(ReduceStep(func, initial, name))
        return self  # type: ignore
    
    def flat_map(
        self, 
        func: Callable[[T], Iterable[U]], 
        name: str = ""
    ) -> "Pipeline[U]":
        """映射后展平"""
        self._steps.append(FlatMapStep(func, name))
        return self  # type: ignore
    
    def take(self, n: int, name: str = "") -> "Pipeline[T]":
        """取前N个元素"""
        self._steps.append(TakeStep(n, name))
        return self
    
    def skip(self, n: int, name: str = "") -> "Pipeline[T]":
        """跳过前N个元素"""
        self._steps.append(SkipStep(n, name))
        return self
    
    def group_by(
        self, 
        key_func: Callable[[T], Any], 
        name: str = ""
    ) -> "Pipeline[Dict[Any, List[T]]]":
        """按key分组"""
        self._steps.append(GroupByStep(key_func, name))
        return self  # type: ignore
    
    def sort(
        self,
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
        name: str = ""
    ) -> "Pipeline[List[T]]":
        """排序"""
        self._steps.append(SortStep(key, reverse, name))
        return self  # type: ignore
    
    def unique(
        self,
        key: Optional[Callable[[T], Any]] = None,
        name: str = ""
    ) -> "Pipeline[T]":
        """去重"""
        self._steps.append(UniqueStep(key, name))
        return self
    
    def chunk(self, size: int, name: str = "") -> "Pipeline[List[T]]":
        """分块"""
        self._steps.append(ChunkStep(size, name))
        return self  # type: ignore
    
    def zip_with(
        self, 
        other: Iterable[U], 
        name: str = ""
    ) -> "Pipeline[Tuple[T, U]]":
        """与另一序列配对"""
        self._steps.append(ZipStep(other, name))
        return self  # type: ignore
    
    def enumerate(self, start: int = 0, name: str = "") -> "Pipeline[Tuple[int, T]]":
        """添加索引"""
        self._steps.append(EnumerateStep(start, name))
        return self  # type: ignore
    
    def tap(self, action: Callable[[T], None], name: str = "") -> "Pipeline[T]":
        """旁路操作（不修改数据）"""
        self._steps.append(TapStep(action, name))
        return self
    
    def batch(
        self,
        batch_func: Callable[[List[T]], List[U]],
        batch_size: int = 100,
        name: str = ""
    ) -> "Pipeline[U]":
        """批量处理"""
        self._steps.append(BatchStep(batch_func, batch_size, name))
        return self  # type: ignore
    
    def conditional(
        self,
        condition: Callable[[T], bool],
        true_func: Callable[[T], U],
        false_func: Callable[[T], U],
        name: str = ""
    ) -> "Pipeline[U]":
        """条件分支"""
        self._steps.append(ConditionalStep(condition, true_func, false_func, name))
        return self  # type: ignore
    
    def try_catch(
        self,
        func: Callable[[T], U],
        on_error: Optional[Callable[[T, Exception], U]] = None,
        name: str = ""
    ) -> "Pipeline[U]":
        """错误捕获"""
        self._steps.append(TryCatchStep(func, on_error, name))
        return self  # type: ignore
    
    def parallel_map(
        self,
        func: Callable[[T], U],
        max_workers: int = 4,
        name: str = ""
    ) -> "Pipeline[U]":
        """并行映射"""
        self._steps.append(ParallelMapStep(func, max_workers, name))
        return self  # type: ignore
    
    def add_step(self, step: BaseStep) -> "Pipeline":
        """添加自定义步骤"""
        self._steps.append(step)
        return self
    
    # ========================================================================
    # 配置方法
    # ========================================================================
    
    def eager(self) -> "Pipeline[T]":
        """设置为立即求值模式"""
        self._lazy = False
        return self
    
    def lazy(self) -> "Pipeline[T]":
        """设置为惰性求值模式（默认）"""
        self._lazy = True
        return self
    
    # ========================================================================
    # 执行方法
    # ========================================================================
    
    def run(self, source: Optional[Iterable[T]] = None) -> Any:
        """
        执行管道。
        
        Args:
            source: 可选的数据源（覆盖初始化时的数据源）
        
        Returns:
            处理结果
        """
        data = source if source is not None else self._source
        if data is None:
            raise PipelineError("管道没有数据源")
        
        for step in self._steps:
            data = step.process(data)
        
        if not self._lazy:
            # 立即求值
            if isinstance(data, Iterator):
                data = list(data)
        
        return data
    
    def to_list(self) -> List:
        """执行并返回列表"""
        return list(self.run() if self._source else self.run(self._source))
    
    def to_dict(self, key_func: Callable, value_func: Optional[Callable] = None) -> Dict:
        """执行并返回字典"""
        data = self.run()
        if value_func:
            return {key_func(item): value_func(item) for item in data}
        return {key_func(item): item for item in data}
    
    def first(self, default: Any = None) -> Any:
        """返回第一个元素"""
        data = self.run()
        try:
            return next(iter(data))
        except StopIteration:
            return default
    
    def last(self, default: Any = None) -> Any:
        """返回最后一个元素"""
        data = self.run()
        result = default
        for item in data:
            result = item
        return result
    
    def count(self) -> int:
        """返回元素数量"""
        data = self.run()
        return sum(1 for _ in data)
    
    def sum(self) -> Union[int, float]:
        """返回总和"""
        data = self.run()
        return sum(data)  # type: ignore
    
    def min(self, key: Optional[Callable] = None) -> Any:
        """返回最小值"""
        data = list(self.run())
        if not data:
            raise ValueError("空序列没有最小值")
        if key is not None:
            return min(data, key=key)
        return min(data)
    
    def max(self, key: Optional[Callable] = None) -> Any:
        """返回最大值"""
        data = list(self.run())
        if not data:
            raise ValueError("空序列没有最大值")
        if key is not None:
            return max(data, key=key)
        return max(data)
    
    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """检查是否有任意元素满足条件"""
        data = self.run()
        if predicate:
            return any(predicate(item) for item in data)
        return any(data)  # type: ignore
    
    def all(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """检查是否所有元素都满足条件"""
        data = self.run()
        if predicate:
            return all(predicate(item) for item in data)
        return all(data)  # type: ignore
    
    def for_each(self, action: Callable[[T], None]) -> None:
        """对每个元素执行操作"""
        for item in self.run():
            action(item)
    
    # ========================================================================
    # 组合方法
    # ========================================================================
    
    def compose(self, other: "Pipeline") -> "Pipeline":
        """
        组合两个管道。
        
        Args:
            other: 另一个管道
        
        Returns:
            组合后的新管道
        """
        new_pipeline = Pipeline(self._source)
        new_pipeline._steps = self._steps + other._steps
        new_pipeline._lazy = self._lazy
        return new_pipeline
    
    def clone(self) -> "Pipeline[T]":
        """克隆管道"""
        new_pipeline = Pipeline(self._source)
        new_pipeline._steps = copy.copy(self._steps)
        new_pipeline._lazy = self._lazy
        return new_pipeline
    
    def __or__(self, other: "Pipeline") -> "Pipeline":
        """支持使用 | 操作符组合管道"""
        return self.compose(other)
    
    def __repr__(self) -> str:
        steps_str = " -> ".join(s.name for s in self._steps)
        return f"<Pipeline: {steps_str or 'empty'}>"
    
    def __iter__(self):
        """支持迭代"""
        return iter(self.run())


# ============================================================================
# 管道构建器
# ============================================================================

class PipelineBuilder:
    """
    管道构建器 - 用于创建可复用的管道模板。
    
    示例:
        >>> # 创建管道模板
        >>> builder = PipelineBuilder()
        >>> builder.map(lambda x: x * 2)
        >>> builder.filter(lambda x: x > 10)
        >>> 
        >>> # 使用模板
        >>> pipeline = builder.build()
        >>> result = pipeline.run([5, 6, 7, 8])
    """
    
    def __init__(self):
        self._steps: List[BaseStep] = []
    
    def map(self, func: Callable, name: str = "") -> "PipelineBuilder":
        self._steps.append(MapStep(func, name))
        return self
    
    def filter(self, predicate: Callable, name: str = "") -> "PipelineBuilder":
        self._steps.append(FilterStep(predicate, name))
        return self
    
    def reduce(
        self, 
        func: Callable, 
        initial: Any = None,
        name: str = ""
    ) -> "PipelineBuilder":
        self._steps.append(ReduceStep(func, initial, name))
        return self
    
    def flat_map(self, func: Callable, name: str = "") -> "PipelineBuilder":
        self._steps.append(FlatMapStep(func, name))
        return self
    
    def take(self, n: int, name: str = "") -> "PipelineBuilder":
        self._steps.append(TakeStep(n, name))
        return self
    
    def skip(self, n: int, name: str = "") -> "PipelineBuilder":
        self._steps.append(SkipStep(n, name))
        return self
    
    def group_by(self, key_func: Callable, name: str = "") -> "PipelineBuilder":
        self._steps.append(GroupByStep(key_func, name))
        return self
    
    def sort(
        self, 
        key: Optional[Callable] = None,
        reverse: bool = False,
        name: str = ""
    ) -> "PipelineBuilder":
        self._steps.append(SortStep(key, reverse, name))
        return self
    
    def unique(
        self, 
        key: Optional[Callable] = None,
        name: str = ""
    ) -> "PipelineBuilder":
        self._steps.append(UniqueStep(key, name))
        return self
    
    def chunk(self, size: int, name: str = "") -> "PipelineBuilder":
        self._steps.append(ChunkStep(size, name))
        return self
    
    def add_step(self, step: BaseStep) -> "PipelineBuilder":
        self._steps.append(step)
        return self
    
    def build(self, source: Optional[Iterable] = None) -> Pipeline:
        """构建管道"""
        pipeline = Pipeline(source)
        pipeline._steps = copy.copy(self._steps)
        return pipeline


# ============================================================================
# 常用管道工厂
# ============================================================================

def create_filter_pipeline(predicate: Callable[[T], bool]) -> Pipeline[T]:
    """创建过滤管道"""
    return Pipeline().filter(predicate)


def create_map_pipeline(func: Callable[[T], U]) -> Pipeline[U]:
    """创建映射管道"""
    return Pipeline().map(func)


def create_sort_pipeline(
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> Pipeline[List[T]]:
    """创建排序管道"""
    return Pipeline().sort(key, reverse)


def create_unique_pipeline(
    key: Optional[Callable[[T], Any]] = None
) -> Pipeline[T]:
    """创建去重管道"""
    return Pipeline().unique(key)


def create_batch_pipeline(
    batch_func: Callable[[List[T]], List[U]],
    batch_size: int = 100
) -> Pipeline[U]:
    """创建批量处理管道"""
    return Pipeline().batch(batch_func, batch_size)


# ============================================================================
# 便捷函数
# ============================================================================

def pipe(*funcs: Callable) -> Callable:
    """
    函数管道 - 从左到右依次应用函数。
    
    示例:
        >>> result = pipe(
        ...     lambda x: x + 1,
        ...     lambda x: x * 2,
        ...     lambda x: x - 3
        ... )(5)
        >>> print(result)  # 9
    """
    def composed(x):
        result = x
        for func in funcs:
            result = func(result)
        return result
    return composed


def compose(*funcs: Callable) -> Callable:
    """
    函数组合 - 从右到左依次应用函数。
    
    示例:
        >>> result = compose(
        ...     lambda x: x - 3,
        ...     lambda x: x * 2,
        ...     lambda x: x + 1
        ... )(5)
        >>> print(result)  # 9
    """
    def composed(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 异常
    'PipelineError',
    'StepError',
    'ValidationError',
    
    # 步骤类
    'BaseStep',
    'MapStep',
    'FilterStep',
    'ReduceStep',
    'FlatMapStep',
    'TakeStep',
    'SkipStep',
    'GroupByStep',
    'SortStep',
    'UniqueStep',
    'ChunkStep',
    'ZipStep',
    'EnumerateStep',
    'TapStep',
    'BatchStep',
    'ConditionalStep',
    'TryCatchStep',
    'ParallelMapStep',
    
    # 管道类
    'Pipeline',
    'PipelineBuilder',
    
    # 工厂函数
    'create_filter_pipeline',
    'create_map_pipeline',
    'create_sort_pipeline',
    'create_unique_pipeline',
    'create_batch_pipeline',
    
    # 便捷函数
    'pipe',
    'compose',
]