"""
堆工具集 (Heap Utilities)
==========================

提供全面的堆数据结构和操作功能，包括：
- 最小堆 (MinHeap)
- 最大堆 (MaxHeap)
- 双端堆 (MinMaxHeap)
- 堆排序算法
- 第K大/小元素查找
- 堆合并操作
- 优先队列实现

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-04-17
版本: 1.0.0
"""

from typing import List, Optional, TypeVar, Generic, Callable, Any, Iterator, Tuple
from functools import total_ordering

T = TypeVar('T')


@total_ordering
class HeapItem(Generic[T]):
    """
    堆元素包装类，支持自定义优先级比较
    用于在堆中存储带有优先级的元素
    """
    
    def __init__(self, priority: float, value: T):
        """
        初始化堆元素
        
        Args:
            priority: 优先级（数值越小优先级越高）
            value: 实际存储的值
        """
        self.priority = priority
        self.value = value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HeapItem):
            return NotImplemented
        return self.priority == other.priority
    
    def __lt__(self, other: 'HeapItem[T]') -> bool:
        return self.priority < other.priority
    
    def __repr__(self) -> str:
        return f"HeapItem(priority={self.priority}, value={self.value})"


class MinHeap(Generic[T]):
    """
    最小堆实现
    
    支持动态扩容，提供完整的堆操作接口。
    元素按从小到大排序，堆顶始终是最小元素。
    """
    
    def __init__(self, items: Optional[List[T]] = None, 
                 key: Optional[Callable[[T], float]] = None):
        """
        初始化最小堆
        
        Args:
            items: 初始元素列表
            key: 用于比较的键函数
        """
        self._data: List[T] = []
        self._key = key
        
        if items:
            self._data = list(items)
            self._heapify()
    
    def _compare(self, a: T, b: T) -> bool:
        """比较两个元素，返回 a < b（用于最小堆）"""
        if self._key:
            return self._key(a) < self._key(b)
        if isinstance(a, HeapItem) and isinstance(b, HeapItem):
            return a.priority < b.priority
        # 直接使用 Python 比较运算符
        try:
            return a < b
        except TypeError:
            # 如果无法直接比较，使用 hash 值
            return hash(a) < hash(b)
    
    def _sift_up(self, index: int):
        """向上调整堆"""
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self._data[index], self._data[parent]):
                self._data[index], self._data[parent] = self._data[parent], self._data[index]
                index = parent
            else:
                break
    
    def _sift_down(self, index: int):
        """向下调整堆"""
        size = len(self._data)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            if left < size and self._compare(self._data[left], self._data[smallest]):
                smallest = left
            if right < size and self._compare(self._data[right], self._data[smallest]):
                smallest = right
            
            if smallest != index:
                self._data[index], self._data[smallest] = self._data[smallest], self._data[index]
                index = smallest
            else:
                break
    
    def _heapify(self):
        """将列表转换为堆"""
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)
    
    def push(self, item: T):
        """
        向堆中添加元素
        
        Args:
            item: 要添加的元素
        """
        self._data.append(item)
        self._sift_up(len(self._data) - 1)
    
    def pop(self) -> T:
        """
        弹出堆顶元素（最小元素）
        
        Returns:
            堆顶元素
            
        Raises:
            IndexError: 堆为空时
        """
        if not self._data:
            raise IndexError("pop from empty heap")
        
        result = self._data[0]
        last = self._data.pop()
        
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        
        return result
    
    def peek(self) -> T:
        """
        查看堆顶元素但不弹出
        
        Returns:
            堆顶元素
            
        Raises:
            IndexError: 堆为空时
        """
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]
    
    def replace(self, item: T) -> T:
        """
        弹出堆顶并插入新元素
        
        Args:
            item: 要插入的新元素
            
        Returns:
            原堆顶元素
        """
        if not self._data:
            self._data.append(item)
            raise IndexError("replace on empty heap, item added")
        
        result = self._data[0]
        self._data[0] = item
        self._sift_down(0)
        return result
    
    def pushpop(self, item: T) -> T:
        """
        先插入元素再弹出堆顶
        
        Args:
            item: 要插入的元素
            
        Returns:
            堆顶元素
        """
        self.push(item)
        return self.pop()
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __bool__(self) -> bool:
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        """迭代弹出元素（会消耗堆）"""
        while self._data:
            yield self.pop()
    
    def __repr__(self) -> str:
        return f"MinHeap({self._data})"
    
    def clear(self):
        """清空堆"""
        self._data.clear()
    
    def to_list(self, sorted_: bool = True) -> List[T]:
        """
        转换为列表
        
        Args:
            sorted_: 是否按堆序（从小到大）输出
            
        Returns:
            元素列表
        """
        if sorted_:
            return list(self.__iter__())
        return list(self._data)
    
    def merge(self, other: 'MinHeap[T]') -> 'MinHeap[T]':
        """
        合并另一个堆
        
        Args:
            other: 要合并的堆
            
        Returns:
            新的合并堆
        """
        return MinHeap(self._data + other._data, key=self._key)
    
    def update(self, index: int, new_item: T):
        """
        更新指定位置的元素
        
        Args:
            index: 要更新的位置
            new_item: 新元素
        """
        if not 0 <= index < len(self._data):
            raise IndexError("index out of range")
        
        old_item = self._data[index]
        self._data[index] = new_item
        
        # 比较新旧元素，决定调整方向
        if self._compare(new_item, old_item):
            # 新元素比旧元素"更小"（优先级更高），向上调整
            self._sift_up(index)
        else:
            # 新元素比旧元素"更大"（优先级更低），向下调整
            self._sift_down(index)


class MaxHeap(Generic[T]):
    """
    最大堆实现
    
    元素按从大到小排序，堆顶始终是最大元素。
    """
    
    def __init__(self, items: Optional[List[T]] = None,
                 key: Optional[Callable[[T], float]] = None):
        """
        初始化最大堆
        
        Args:
            items: 初始元素列表
            key: 用于比较的键函数
        """
        self._data: List[T] = []
        self._key = key
        
        if items:
            self._data = list(items)
            self._heapify()
    
    def _compare(self, a: T, b: T) -> bool:
        """比较两个元素，返回 a < b（用于最小堆逻辑，但我们要找最大）"""
        if self._key:
            # 对于最大堆，键值越大优先级越高
            return self._key(a) > self._key(b)
        if isinstance(a, HeapItem) and isinstance(b, HeapItem):
            # 对于最大堆，优先级越低（数值小）在堆顶
            return a.priority > b.priority
        # 直接使用 Python 比较运算符（反转）
        try:
            return a > b  # 对于最大堆，较大的值应该更"小"（堆顶）
        except TypeError:
            return hash(a) > hash(b)
    
    def _sift_up(self, index: int):
        """向上调整堆"""
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self._data[index], self._data[parent]):
                self._data[index], self._data[parent] = self._data[parent], self._data[index]
                index = parent
            else:
                break
    
    def _sift_down(self, index: int):
        """向下调整堆"""
        size = len(self._data)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            if left < size and self._compare(self._data[left], self._data[smallest]):
                smallest = left
            if right < size and self._compare(self._data[right], self._data[smallest]):
                smallest = right
            
            if smallest != index:
                self._data[index], self._data[smallest] = self._data[smallest], self._data[index]
                index = smallest
            else:
                break
    
    def _heapify(self):
        """将列表转换为堆"""
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)
    
    def push(self, item: T):
        """向堆中添加元素"""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)
    
    def pop(self) -> T:
        """弹出堆顶元素（最大元素）"""
        if not self._data:
            raise IndexError("pop from empty heap")
        
        result = self._data[0]
        last = self._data.pop()
        
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        
        return result
    
    def peek(self) -> T:
        """查看堆顶元素但不弹出"""
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __bool__(self) -> bool:
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        """迭代弹出元素（会消耗堆）"""
        while self._data:
            yield self.pop()
    
    def __repr__(self) -> str:
        return f"MaxHeap({self._data})"
    
    def clear(self):
        """清空堆"""
        self._data.clear()
    
    def to_list(self, sorted_: bool = True) -> List[T]:
        """转换为列表"""
        if sorted_:
            return list(self.__iter__())
        return list(self._data)


class MinMaxHeap(Generic[T]):
    """
    双端堆（最小最大堆）
    
    同时支持O(log n)时间获取最小和最大元素。
    适用于需要同时访问最小和最大元素的场景。
    """
    
    def __init__(self, items: Optional[List[T]] = None):
        """初始化双端堆"""
        self._min_heap: List[T] = []
        self._max_heap: List[Tuple[float, int, T]] = []  # (neg_key, index, value)
        self._index = 0
        
        if items:
            for item in items:
                self.push(item)
    
    def push(self, item: T):
        """添加元素"""
        key = self._get_key(item)
        self._min_heap.append(item)
        
        # 使用索引保证相同优先级元素的稳定性
        self._max_heap.append((-key, self._index, item))
        self._index += 1
        
        self._sift_up_min(len(self._min_heap) - 1)
        self._sift_up_max(len(self._max_heap) - 1)
    
    def _get_key(self, item: T) -> float:
        """获取比较键"""
        if isinstance(item, HeapItem):
            return item.priority
        if isinstance(item, (int, float)):
            return item
        return hash(item)
    
    def _sift_up_min(self, i: int):
        """最小堆向上调整"""
        while i > 0:
            parent = (i - 1) // 2
            if self._get_key(self._min_heap[i]) < self._get_key(self._min_heap[parent]):
                self._min_heap[i], self._min_heap[parent] = self._min_heap[parent], self._min_heap[i]
                i = parent
            else:
                break
    
    def _sift_up_max(self, i: int):
        """最大堆向上调整"""
        while i > 0:
            parent = (i - 1) // 2
            if self._max_heap[i][0] < self._max_heap[parent][0]:
                self._max_heap[i], self._max_heap[parent] = self._max_heap[parent], self._max_heap[i]
                i = parent
            else:
                break
    
    def _sift_down_min(self, i: int):
        """最小堆向下调整"""
        size = len(self._min_heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < size and self._get_key(self._min_heap[left]) < self._get_key(self._min_heap[smallest]):
                smallest = left
            if right < size and self._get_key(self._min_heap[right]) < self._get_key(self._min_heap[smallest]):
                smallest = right
            
            if smallest != i:
                self._min_heap[i], self._min_heap[smallest] = self._min_heap[smallest], self._min_heap[i]
                i = smallest
            else:
                break
    
    def _sift_down_max(self, i: int):
        """最大堆向下调整"""
        size = len(self._max_heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < size and self._max_heap[left][0] < self._max_heap[smallest][0]:
                smallest = left
            if right < size and self._max_heap[right][0] < self._max_heap[smallest][0]:
                smallest = right
            
            if smallest != i:
                self._max_heap[i], self._max_heap[smallest] = self._max_heap[smallest], self._max_heap[i]
                i = smallest
            else:
                break
    
    def get_min(self) -> T:
        """获取最小元素"""
        if not self._min_heap:
            raise IndexError("get_min from empty heap")
        return self._min_heap[0]
    
    def get_max(self) -> T:
        """获取最大元素"""
        if not self._max_heap:
            raise IndexError("get_max from empty heap")
        return self._max_heap[0][2]
    
    def pop_min(self) -> T:
        """弹出最小元素"""
        if not self._min_heap:
            raise IndexError("pop_min from empty heap")
        
        result = self._min_heap[0]
        last = self._min_heap.pop()
        
        if self._min_heap:
            self._min_heap[0] = last
            self._sift_down_min(0)
        
        # 从最大堆中移除对应元素（简化处理：重建）
        self._rebuild_max_heap()
        return result
    
    def pop_max(self) -> T:
        """弹出最大元素"""
        if not self._max_heap:
            raise IndexError("pop_max from empty heap")
        
        result = self._max_heap[0][2]
        last = self._max_heap.pop()
        
        if self._max_heap:
            self._max_heap[0] = last
            self._sift_down_max(0)
        
        # 从最小堆中移除对应元素（简化处理：重建）
        self._rebuild_min_heap()
        return result
    
    def _rebuild_max_heap(self):
        """重建最大堆"""
        self._max_heap = [(-self._get_key(x), i, x) for i, x in enumerate(self._min_heap)]
        for i in range(len(self._max_heap) // 2 - 1, -1, -1):
            self._sift_down_max(i)
    
    def _rebuild_min_heap(self):
        """重建最小堆"""
        self._min_heap = [x[2] for x in self._max_heap]
        for i in range(len(self._min_heap) // 2 - 1, -1, -1):
            self._sift_down_min(i)
    
    def __len__(self) -> int:
        return len(self._min_heap)
    
    def __bool__(self) -> bool:
        return bool(self._min_heap)
    
    def __repr__(self) -> str:
        return f"MinMaxHeap({self._min_heap})"


class PriorityQueue(Generic[T]):
    """
    优先队列实现
    
    基于最小堆实现，支持自定义优先级。
    低优先级值的元素先出队。
    相同优先级时遵循 FIFO（先进先出）。
    """
    
    def __init__(self, max_priority: bool = False):
        """
        初始化优先队列
        
        Args:
            max_priority: 是否为最大优先队列（高优先级先出）
        """
        self._heap: MinHeap[Tuple[float, int, T]] = MinHeap()
        self._max_priority = max_priority
        self._counter = 0  # 保证FIFO顺序
    
    def push(self, item: T, priority: float = 0):
        """
        入队
        
        Args:
            item: 元素
            priority: 优先级（数值越小优先级越高）
        """
        if self._max_priority:
            priority = -priority
        # 使用元组 (priority, counter, item)，元组比较先比较 priority，再比较 counter
        self._heap.push((priority, self._counter, item))
        self._counter += 1
    
    def pop(self) -> T:
        """出队（返回优先级最高/最低的元素）"""
        if not self._heap:
            raise IndexError("pop from empty queue")
        priority, counter, item = self._heap.pop()
        return item
    
    def peek(self) -> T:
        """查看队首元素"""
        if not self._heap:
            raise IndexError("peek from empty queue")
        priority, counter, item = self._heap.peek()
        return item
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __bool__(self) -> bool:
        return bool(self._heap)
    
    def __repr__(self) -> str:
        items = [(h[2], h[0]) for h in self._heap._data]
        return f"PriorityQueue({items})"
    
    def clear(self):
        """清空队列"""
        self._heap.clear()
        self._counter = 0


# ==================== 工具函数 ====================

def heap_sort(data: List[T], reverse: bool = False, 
              key: Optional[Callable[[T], float]] = None) -> List[T]:
    """
    堆排序
    
    Args:
        data: 待排序的数据
        reverse: 是否降序排列
        key: 比较键函数
        
    Returns:
        排序后的列表
        
    示例:
        >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
        >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6], reverse=True)
        [9, 6, 5, 4, 3, 2, 1, 1]
    """
    if not data:
        return []
    
    if reverse:
        heap = MaxHeap(data, key=key)
    else:
        heap = MinHeap(data, key=key)
    
    return list(heap)


def nth_smallest(data: List[T], n: int, 
                 key: Optional[Callable[[T], float]] = None) -> T:
    """
    找出第 n 小的元素（从1开始）
    
    Args:
        data: 数据列表
        n: 第n小（从1开始）
        key: 比较键函数
        
    Returns:
        第n小的元素
        
    Raises:
        ValueError: n超出范围
        
    示例:
        >>> nth_smallest([3, 1, 4, 1, 5, 9, 2, 6], 3)
        2
    """
    if not 1 <= n <= len(data):
        raise ValueError(f"n must be between 1 and {len(data)}")
    
    heap = MinHeap(data, key=key)
    for _ in range(n - 1):
        heap.pop()
    return heap.pop()


def nth_largest(data: List[T], n: int,
                key: Optional[Callable[[T], float]] = None) -> T:
    """
    找出第 n 大的元素（从1开始）
    
    Args:
        data: 数据列表
        n: 第n大（从1开始）
        key: 比较键函数
        
    Returns:
        第n大的元素
        
    示例:
        >>> nth_largest([3, 1, 4, 1, 5, 9, 2, 6], 2)
        6
    """
    if not 1 <= n <= len(data):
        raise ValueError(f"n must be between 1 and {len(data)}")
    
    heap = MaxHeap(data, key=key)
    for _ in range(n - 1):
        heap.pop()
    return heap.pop()


def k_smallest(data: List[T], k: int,
               key: Optional[Callable[[T], float]] = None) -> List[T]:
    """
    找出最小的 k 个元素
    
    Args:
        data: 数据列表
        k: 要找的元素个数
        key: 比较键函数
        
    Returns:
        最小的k个元素列表（已排序）
        
    示例:
        >>> k_smallest([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [1, 1, 2]
    """
    if k <= 0:
        return []
    if k >= len(data):
        return heap_sort(data, reverse=False, key=key)
    
    heap = MinHeap(data, key=key)
    return [heap.pop() for _ in range(k)]


def k_largest(data: List[T], k: int,
              key: Optional[Callable[[T], float]] = None) -> List[T]:
    """
    找出最大的 k 个元素
    
    Args:
        data: 数据列表
        k: 要找的元素个数
        key: 比较键函数
        
    Returns:
        最大的k个元素列表（已排序，从大到小）
        
    示例:
        >>> k_largest([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [9, 6, 5]
    """
    if k <= 0:
        return []
    if k >= len(data):
        return heap_sort(data, reverse=True, key=key)
    
    heap = MaxHeap(data, key=key)
    return [heap.pop() for _ in range(k)]


def merge_sorted_lists(*lists: List[T], reverse: bool = False) -> List[T]:
    """
    合并多个已排序列表
    
    Args:
        *lists: 多个已排序列表
        reverse: 输入列表是否为降序
        
    Returns:
        合并后的排序列表
        
    示例:
        >>> merge_sorted_lists([1, 3, 5], [2, 4, 6], [0, 7])
        [0, 1, 2, 3, 4, 5, 6, 7]
    """
    if not lists:
        return []
    
    # 使用堆进行多路归并
    if reverse:
        heap = MaxHeap()
    else:
        heap = MinHeap()
    
    result = []
    for lst in lists:
        for item in lst:
            heap.push(item)
    
    return list(heap)


def is_valid_heap(data: List[T], min_heap: bool = True,
                  key: Optional[Callable[[T], float]] = None) -> bool:
    """
    检查列表是否满足堆性质
    
    Args:
        data: 数据列表
        min_heap: 是否检查最小堆性质
        key: 比较键函数
        
    Returns:
        是否满足堆性质
        
    示例:
        >>> is_valid_heap([1, 2, 3, 4, 5])
        True
        >>> is_valid_heap([5, 4, 3, 2, 1])
        False
    """
    def get_key(item):
        if key:
            return key(item)
        return float(item) if not isinstance(item, (int, float)) else item
    
    n = len(data)
    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            if min_heap:
                if get_key(data[left]) < get_key(data[i]):
                    return False
            else:
                if get_key(data[left]) > get_key(data[i]):
                    return False
        
        if right < n:
            if min_heap:
                if get_key(data[right]) < get_key(data[i]):
                    return False
            else:
                if get_key(data[right]) > get_key(data[i]):
                    return False
    
    return True


def heapify(data: List[T], min_heap: bool = True) -> List[T]:
    """
    将列表原地转换为堆
    
    Args:
        data: 数据列表
        min_heap: 是否为最小堆
        
    Returns:
        堆化后的列表（原地修改）
        
    示例:
        >>> arr = [3, 1, 4, 1, 5]
        >>> heapify(arr)
        >>> is_valid_heap(arr)
        True
    """
    def get_key(item):
        return float(item) if not isinstance(item, (int, float)) else item
    
    def sift_down(arr, start, end):
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            
            if min_heap:
                if child + 1 <= end and get_key(arr[child + 1]) < get_key(arr[child]):
                    child += 1
                if get_key(arr[root]) > get_key(arr[child]):
                    arr[root], arr[child] = arr[child], arr[root]
                    root = child
                else:
                    break
            else:
                if child + 1 <= end and get_key(arr[child + 1]) > get_key(arr[child]):
                    child += 1
                if get_key(arr[root]) < get_key(arr[child]):
                    arr[root], arr[child] = arr[child], arr[root]
                    root = child
                else:
                    break
    
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(data, i, n - 1)
    
    return data


def median_of_data(data: List[T]) -> float:
    """
    使用堆计算中位数
    
    Args:
        data: 数据列表
        
    Returns:
        中位数（偶数个元素时返回中间两个的平均值）
        
    示例:
        >>> median_of_data([1, 2, 3, 4, 5])
        3.0
        >>> median_of_data([1, 2, 3, 4])
        2.5
    """
    if not data:
        raise ValueError("Cannot find median of empty data")
    
    sorted_data = heap_sort(data)
    n = len(sorted_data)
    
    if n % 2 == 1:
        return float(sorted_data[n // 2])
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0


# ==================== 导出 ====================

__all__ = [
    'HeapItem',
    'MinHeap',
    'MaxHeap',
    'MinMaxHeap',
    'PriorityQueue',
    'heap_sort',
    'nth_smallest',
    'nth_largest',
    'k_smallest',
    'k_largest',
    'merge_sorted_lists',
    'is_valid_heap',
    'heapify',
    'median_of_data',
]