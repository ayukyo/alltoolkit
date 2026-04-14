"""
优先队列工具模块

提供完整的优先队列实现，支持：
- 基于二叉堆的最小/最大堆优先队列
- 自定义优先级比较器
- 动态更新优先级
- 队列合并
- 线程安全版本
- 支持泛型元素类型

零外部依赖，纯 Python 标准库实现。

使用场景：
- 任务调度系统
- 事件驱动模拟
- 图算法（Dijkstra、A*）
- 数据流处理
- 合并K个有序列表
"""

from typing import TypeVar, Generic, Callable, Optional, List, Tuple, Any, Dict
from dataclasses import dataclass
import heapq
import threading
from abc import ABC, abstractmethod

T = TypeVar('T')


@dataclass
class PriorityItem(Generic[T]):
    """带优先级的队列元素"""
    priority: float
    item: T
    sequence: int = 0  # 用于稳定排序
    
    def __lt__(self, other: 'PriorityItem') -> bool:
        if self.priority == other.priority:
            return self.sequence < other.sequence
        return self.priority < other.priority
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PriorityItem):
            return False
        return self.priority == other.priority and self.item == other.item


class PriorityQueue(Generic[T]):
    """
    基于二叉堆的优先队列实现
    
    默认为最小堆（优先级值越小越优先）。
    
    时间复杂度：
    - 插入：O(log n)
    - 取出：O(log n)
    - 查看堆顶：O(1)
    - 更新优先级：O(log n) 需要配合 item_index
    - 合并：O(n + m)
    
    示例:
        >>> pq = PriorityQueue[int]()
        >>> pq.push(5, priority=2)
        >>> pq.push(3, priority=1)
        >>> pq.pop()
        3  # 优先级更高（值更小）
    """
    
    def __init__(self, max_heap: bool = False):
        """
        初始化优先队列
        
        Args:
            max_heap: 是否为最大堆，默认 False（最小堆）
        """
        self._heap: List[PriorityItem[T]] = []
        self._counter: int = 0  # 序列号，保证稳定排序
        self._max_heap: bool = max_heap
        self._item_index: Dict[int, int] = {}  # id(item) -> heap index
    
    def push(self, item: T, priority: float) -> None:
        """
        插入元素
        
        Args:
            item: 要插入的元素
            priority: 优先级值
        """
        actual_priority = -priority if self._max_heap else priority
        pitem = PriorityItem(
            priority=actual_priority,
            item=item,
            sequence=self._counter
        )
        self._counter += 1
        
        self._item_index[id(item)] = len(self._heap)
        heapq.heappush(self._heap, pitem)
    
    def pop(self) -> Optional[T]:
        """
        取出并返回优先级最高的元素
        
        Returns:
            优先级最高的元素，队列为空时返回 None
        """
        if not self._heap:
            return None
        pitem = heapq.heappop(self._heap)
        item_id = id(pitem.item)
        if item_id in self._item_index:
            del self._item_index[item_id]
        return pitem.item
    
    def peek(self) -> Optional[T]:
        """
        查看堆顶元素但不取出
        
        Returns:
            堆顶元素，队列为空时返回 None
        """
        if not self._heap:
            return None
        return self._heap[0].item
    
    def peek_priority(self) -> Optional[float]:
        """
        查看堆顶元素的优先级
        
        Returns:
            堆顶元素的优先级，队列为空时返回 None
        """
        if not self._heap:
            return None
        actual = self._heap[0].priority
        return -actual if self._max_heap else actual
    
    def update_priority(self, item: T, new_priority: float) -> bool:
        """
        更新元素的优先级
        
        注意：此方法的时间复杂度为 O(n)，因为需要遍历查找元素。
        如果需要频繁更新优先级，建议使用 UpdatablePriorityQueue。
        
        Args:
            item: 要更新的元素
            new_priority: 新的优先级值
            
        Returns:
            bool: 是否成功更新
        """
        actual_priority = -new_priority if self._max_heap else new_priority
        
        for i, pitem in enumerate(self._heap):
            if pitem.item == item:
                self._heap[i].priority = actual_priority
                heapq.heapify(self._heap)
                return True
        return False
    
    def remove(self, item: T) -> bool:
        """
        从队列中移除指定元素
        
        Args:
            item: 要移除的元素
            
        Returns:
            bool: 是否成功移除
        """
        for i, pitem in enumerate(self._heap):
            if pitem.item == item:
                self._heap.pop(i)
                heapq.heapify(self._heap)
                item_id = id(item)
                if item_id in self._item_index:
                    del self._item_index[item_id]
                return True
        return False
    
    def merge(self, other: 'PriorityQueue[T]') -> None:
        """
        合并另一个优先队列
        
        Args:
            other: 要合并的优先队列
        """
        while other._heap:
            pitem = heapq.heappop(other._heap)
            actual_priority = -pitem.priority if self._max_heap else pitem.priority
            self.push(pitem.item, actual_priority)
    
    def clear(self) -> None:
        """清空队列"""
        self._heap.clear()
        self._item_index.clear()
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __bool__(self) -> bool:
        return bool(self._heap)
    
    def __contains__(self, item: T) -> bool:
        return any(p.item == item for p in self._heap)
    
    def to_list(self, sorted_: bool = True) -> List[Tuple[T, float]]:
        """
        转换为列表
        
        Args:
            sorted_: 是否按优先级排序
            
        Returns:
            元素和优先级组成的元组列表
        """
        if sorted_:
            items = sorted(self._heap, key=lambda p: p.priority)
        else:
            items = self._heap
        return [(p.item, -p.priority if self._max_heap else p.priority) for p in items]
    
    @classmethod
    def from_list(cls, items: List[Tuple[T, float]], max_heap: bool = False) -> 'PriorityQueue[T]':
        """
        从列表创建优先队列
        
        Args:
            items: 元素和优先级组成的元组列表
            max_heap: 是否为最大堆
            
        Returns:
            新的优先队列实例
        """
        pq = cls(max_heap=max_heap)
        for item, priority in items:
            pq.push(item, priority)
        return pq


class UpdatablePriorityQueue(Generic[T]):
    """
    支持高效优先级更新的优先队列
    
    使用额外的索引字典来跟踪元素位置，
    使得更新优先级的时间复杂度降低到 O(log n)。
    
    要求元素必须是可哈希的。
    
    示例:
        >>> pq = UpdatablePriorityQueue[str]()
        >>> pq.push("task1", 2)
        >>> pq.push("task2", 1)
        >>> pq.update_priority("task1", 0)  # 更新为最高优先级
        >>> pq.pop()
        "task1"
    """
    
    def __init__(self, max_heap: bool = False):
        """
        初始化可更新优先队列
        
        Args:
            max_heap: 是否为最大堆
        """
        self._heap: List[PriorityItem[T]] = []
        self._counter: int = 0
        self._max_heap: bool = max_heap
        self._index: Dict[T, int] = {}  # item -> heap index
        self._entry_finder: Dict[T, PriorityItem[T]] = {}  # item -> PriorityItem
    
    def push(self, item: T, priority: float) -> None:
        """
        插入元素，如果已存在则更新优先级
        
        Args:
            item: 要插入的元素
            priority: 优先级值
        """
        if item in self._entry_finder:
            self.update_priority(item, priority)
            return
        
        actual_priority = -priority if self._max_heap else priority
        pitem = PriorityItem(
            priority=actual_priority,
            item=item,
            sequence=self._counter
        )
        self._counter += 1
        
        self._index[item] = len(self._heap)
        self._entry_finder[item] = pitem
        heapq.heappush(self._heap, pitem)
    
    def pop(self) -> Optional[T]:
        """
        取出并返回优先级最高的元素
        
        Returns:
            优先级最高的元素，队列为空时返回 None
        """
        while self._heap:
            pitem = heapq.heappop(self._heap)
            item = pitem.item
            if item in self._entry_finder:
                del self._entry_finder[item]
                del self._index[item]
                return item
        return None
    
    def peek(self) -> Optional[T]:
        """查看堆顶元素"""
        while self._heap:
            pitem = self._heap[0]
            if pitem.item in self._entry_finder:
                return pitem.item
            heapq.heappop(self._heap)
        return None
    
    def update_priority(self, item: T, new_priority: float) -> bool:
        """
        更新元素的优先级（O(log n)）
        
        Args:
            item: 要更新的元素
            new_priority: 新的优先级值
            
        Returns:
            bool: 是否成功更新
        """
        if item not in self._entry_finder:
            return False
        
        actual_priority = -new_priority if self._max_heap else new_priority
        
        # 标记旧条目为删除
        old_pitem = self._entry_finder[item]
        del self._entry_finder[item]
        
        # 插入新条目
        new_pitem = PriorityItem(
            priority=actual_priority,
            item=item,
            sequence=self._counter
        )
        self._counter += 1
        
        self._entry_finder[item] = new_pitem
        heapq.heappush(self._heap, new_pitem)
        return True
    
    def remove(self, item: T) -> bool:
        """
        从队列中移除指定元素
        
        Args:
            item: 要移除的元素
            
        Returns:
            bool: 是否成功移除
        """
        if item not in self._entry_finder:
            return False
        del self._entry_finder[item]
        if item in self._index:
            del self._index[item]
        return True
    
    def contains(self, item: T) -> bool:
        """检查元素是否在队列中"""
        return item in self._entry_finder
    
    def get_priority(self, item: T) -> Optional[float]:
        """获取元素的优先级"""
        if item not in self._entry_finder:
            return None
        actual = self._entry_finder[item].priority
        return -actual if self._max_heap else actual
    
    def clear(self) -> None:
        """清空队列"""
        self._heap.clear()
        self._index.clear()
        self._entry_finder.clear()
    
    def __len__(self) -> int:
        return len(self._entry_finder)
    
    def __bool__(self) -> bool:
        return bool(self._entry_finder)
    
    def __contains__(self, item: T) -> bool:
        return item in self._entry_finder


class ThreadSafePriorityQueue(Generic[T]):
    """
    线程安全的优先队列
    
    使用锁来保证多线程环境下的安全性。
    
    示例:
        >>> pq = ThreadSafePriorityQueue[str]()
        >>> pq.push("task", 1)
        >>> with pq.pop_wait(timeout=5) as item:
        ...     print(item)
    """
    
    def __init__(self, max_heap: bool = False):
        """
        初始化线程安全优先队列
        
        Args:
            max_heap: 是否为最大堆
        """
        self._pq = PriorityQueue[T](max_heap=max_heap)
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
    
    def push(self, item: T, priority: float) -> None:
        """
        插入元素（线程安全）
        
        Args:
            item: 要插入的元素
            priority: 优先级值
        """
        with self._lock:
            self._pq.push(item, priority)
            self._not_empty.notify()
    
    def pop(self, timeout: Optional[float] = None) -> Optional[T]:
        """
        取出元素（线程安全，可阻塞）
        
        Args:
            timeout: 超时时间（秒），None 表示无限等待
            
        Returns:
            优先级最高的元素，超时时返回 None
        """
        with self._not_empty:
            if timeout is not None:
                self._not_empty.wait_for(lambda: len(self._pq) > 0, timeout=timeout)
            else:
                while len(self._pq) == 0:
                    self._not_empty.wait()
            return self._pq.pop()
    
    def try_pop(self) -> Optional[T]:
        """
        尝试立即取出元素（非阻塞）
        
        Returns:
            元素或 None（队列为空时）
        """
        with self._lock:
            return self._pq.pop()
    
    def peek(self) -> Optional[T]:
        """查看堆顶元素（线程安全）"""
        with self._lock:
            return self._pq.peek()
    
    def clear(self) -> None:
        """清空队列（线程安全）"""
        with self._lock:
            self._pq.clear()
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._pq)
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._pq)


class BoundedPriorityQueue(Generic[T]):
    """
    有界优先队列
    
    当队列达到最大容量时，新插入的低优先级元素会被拒绝。
    
    示例:
        >>> pq = BoundedPriorityQueue[int](max_size=3)
        >>> pq.push(1, 1)
        True
        >>> pq.push(4, 4)  # 低优先级，队列已满
        False
    """
    
    def __init__(self, max_size: int, max_heap: bool = False):
        """
        初始化有界优先队列
        
        Args:
            max_size: 最大容量
            max_heap: 是否为最大堆
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._pq = PriorityQueue[T](max_heap=max_heap)
    
    def push(self, item: T, priority: float) -> bool:
        """
        尝试插入元素
        
        如果队列已满且新元素优先级低于当前最低优先级，则拒绝插入。
        
        Args:
            item: 要插入的元素
            priority: 优先级值
            
        Returns:
            bool: 是否成功插入
        """
        if len(self._pq) < self._max_size:
            self._pq.push(item, priority)
            return True
        
        # 队列已满，检查是否可以替换最低优先级元素
        # 获取当前最低优先级（最后一个元素）
        items = self._pq.to_list(sorted_=True)
        if not items:
            self._pq.push(item, priority)
            return True
        
        lowest_item, lowest_priority = items[-1]
        
        # 判断新元素优先级是否高于最低优先级元素
        if self._pq._max_heap:
            # 最大堆：priority越大越优先，lowest_priority是最小的
            if priority <= lowest_priority:
                # 新元素优先级更低或相等，拒绝
                return False
        else:
            # 最小堆：priority越小越优先，lowest_priority是最大的
            if priority >= lowest_priority:
                # 新元素优先级更低或相等，拒绝
                return False
        
        # 移除最低优先级元素，插入新元素
        self._pq.remove(lowest_item)
        self._pq.push(item, priority)
        return True
    
    def pop(self) -> Optional[T]:
        """取出优先级最高的元素"""
        return self._pq.pop()
    
    def peek(self) -> Optional[T]:
        """查看堆顶元素"""
        return self._pq.peek()
    
    def is_full(self) -> bool:
        """队列是否已满"""
        return len(self._pq) >= self._max_size
    
    @property
    def max_size(self) -> int:
        """最大容量"""
        return self._max_size
    
    def __len__(self) -> int:
        return len(self._pq)
    
    def __bool__(self) -> bool:
        return bool(self._pq)


def merge_sorted_lists(lists: List[List[Tuple[T, float]]], 
                       max_heap: bool = False) -> List[Tuple[T, float]]:
    """
    合并多个已排序的列表（每个列表按优先级排序）
    
    使用优先队列高效合并，时间复杂度 O(n * log k)，
    其中 n 是总元素数，k 是列表数。
    
    Args:
        lists: 多个已排序列表的列表
        max_heap: 是否按优先级降序排列
        
    Returns:
        合并后的排序列表
        
    示例:
        >>> lists = [[('a', 1), ('b', 3)], [('c', 2), ('d', 4)]]
        >>> merge_sorted_lists(lists)
        [('a', 1), ('c', 2), ('b', 3), ('d', 4)]
    """
    if not lists:
        return []
    
    pq = PriorityQueue[Tuple[int, int, T]](max_heap=False)  # (priority, list_idx, elem_idx)
    
    # 初始化：每个列表的第一个元素
    for i, lst in enumerate(lists):
        if lst:
            item, priority = lst[0]
            pq.push((priority, i, 0, item), priority)
    
    result: List[Tuple[T, float]] = []
    
    while pq:
        priority, list_idx, elem_idx, item = pq.pop()
        result.append((item, priority))
        
        # 从对应列表取下一个元素
        if elem_idx + 1 < len(lists[list_idx]):
            next_item, next_priority = lists[list_idx][elem_idx + 1]
            pq.push((next_priority, list_idx, elem_idx + 1, next_item), next_priority)
    
    return result


class TaskScheduler:
    """
    基于优先队列的任务调度器
    
    支持任务优先级、延迟执行、周期执行。
    
    示例:
        >>> scheduler = TaskScheduler()
        >>> scheduler.add_task("urgent_task", priority=1)
        >>> scheduler.add_task("normal_task", priority=5)
        >>> scheduler.get_next_task()
        'urgent_task'
    """
    
    def __init__(self, max_heap: bool = False):
        """
        初始化任务调度器
        
        Args:
            max_heap: 是否为最大堆（True 时优先级大的先执行）
        """
        self._pq = UpdatablePriorityQueue[str](max_heap=max_heap)
        self._task_data: Dict[str, Any] = {}
    
    def add_task(self, task_id: str, priority: float, 
                 data: Optional[Any] = None) -> None:
        """
        添加任务
        
        Args:
            task_id: 任务唯一标识
            priority: 优先级（值越小越优先，除非 max_heap=True）
            data: 任务附加数据
        """
        self._pq.push(task_id, priority)
        if data is not None:
            self._task_data[task_id] = data
    
    def get_next_task(self) -> Optional[str]:
        """
        获取下一个要执行的任务
        
        Returns:
            任务ID，队列为空时返回 None
        """
        return self._pq.pop()
    
    def update_task_priority(self, task_id: str, new_priority: float) -> bool:
        """
        更新任务优先级
        
        Args:
            task_id: 任务ID
            new_priority: 新优先级
            
        Returns:
            bool: 是否成功更新
        """
        return self._pq.update_priority(task_id, new_priority)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功取消
        """
        if task_id in self._task_data:
            del self._task_data[task_id]
        return self._pq.remove(task_id)
    
    def get_task_data(self, task_id: str) -> Optional[Any]:
        """
        获取任务附加数据
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务数据，不存在时返回 None
        """
        return self._task_data.get(task_id)
    
    def peek_next_task(self) -> Optional[str]:
        """查看下一个任务（不移除）"""
        return self._pq.peek()
    
    def has_task(self, task_id: str) -> bool:
        """检查任务是否存在"""
        return task_id in self._pq
    
    def clear(self) -> None:
        """清空所有任务"""
        self._pq.clear()
        self._task_data.clear()
    
    def __len__(self) -> int:
        return len(self._pq)
    
    def __bool__(self) -> bool:
        return bool(self._pq)


# 便捷函数

def create_min_heap() -> PriorityQueue:
    """创建最小堆优先队列"""
    return PriorityQueue(max_heap=False)


def create_max_heap() -> PriorityQueue:
    """创建最大堆优先队列"""
    return PriorityQueue(max_heap=True)


def top_k(items: List[Tuple[T, float]], k: int, largest: bool = True) -> List[Tuple[T, float]]:
    """
    获取前 K 个元素
    
    使用 heapq 模块高效获取前 K 个元素，
    时间复杂度 O(n log k)。
    
    Args:
        items: 元素和优先级组成的元组列表
        k: 返回元素数量
        largest: True 返回优先级最大的 K 个，False 返回优先级最小的 K 个
        
    Returns:
        前 K 个元素列表（按优先级排序）
        
    示例:
        >>> items = [('a', 3), ('b', 1), ('c', 2)]
        >>> top_k(items, 2, largest=True)
        [('a', 3), ('c', 2)]
    """
    if k <= 0 or not items:
        return []
    
    # 使用内置 heapq 模块
    import heapq as hp
    
    # 转换为带优先级的元组
    if largest:
        # 获取最大的 K 个，使用 nlargest
        # heapq.nlargest 返回按优先级降序排列
        result = hp.nlargest(k, items, key=lambda x: x[1])
    else:
        # 获取最小的 K 个，使用 nsmallest
        # heapq.nsmallest 返回按优先级升序排列
        result = hp.nsmallest(k, items, key=lambda x: x[1])
    
    return result


if __name__ == "__main__":
    # 基本使用示例
    print("=== PriorityQueue 基本使用 ===")
    pq = PriorityQueue[str]()
    pq.push("low priority", 10)
    pq.push("high priority", 1)
    pq.push("medium priority", 5)
    
    print("按优先级弹出:")
    while pq:
        print(f"  {pq.pop()}")
    
    print("\n=== 最大堆 ===")
    max_pq = PriorityQueue[int](max_heap=True)
    max_pq.push(1, 1)
    max_pq.push(5, 5)
    max_pq.push(3, 3)
    
    print("按优先级降序弹出:")
    while max_pq:
        print(f"  {max_pq.pop()}")
    
    print("\n=== UpdatablePriorityQueue ===")
    upq = UpdatablePriorityQueue[str]()
    upq.push("task1", 3)
    upq.push("task2", 1)
    upq.push("task3", 2)
    
    print("更新 task1 优先级为 0")
    upq.update_priority("task1", 0)
    
    print("按优先级弹出:")
    while upq:
        print(f"  {upq.pop()}")
    
    print("\n=== TaskScheduler ===")
    scheduler = TaskScheduler()
    scheduler.add_task("urgent", priority=1, data={"type": "critical"})
    scheduler.add_task("normal", priority=5, data={"type": "regular"})
    scheduler.add_task("important", priority=2, data={"type": "important"})
    
    print("任务执行顺序:")
    while scheduler:
        task = scheduler.get_next_task()
        data = scheduler.get_task_data(task) if task in scheduler._task_data else None
        print(f"  {task}: {data}")