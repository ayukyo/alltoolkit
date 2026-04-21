"""
KD树工具模块 (KD-Tree Utilities)
==============================

提供KD树的完整实现，支持多维空间索引和最近邻搜索。
零外部依赖，纯Python实现。

核心功能：
- KD树的构建和插入
- k近邻搜索 (k-NN)
- 范围查询
- 最近邻搜索
- 删除节点
- 树的平衡检查

作者: AllToolkit 自动生成
日期: 2026-04-22
"""

from typing import List, Tuple, Optional, Callable, Any, Generic, TypeVar, Union
from dataclasses import dataclass, field
import math
import heapq

T = TypeVar('T')


class KDNode:
    """KD树节点"""
    
    def __init__(self, point: List[float], data: Any = None, 
                 left: Optional['KDNode'] = None, right: Optional['KDNode'] = None, 
                 axis: int = 0):
        self.point = point
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis
    
    def __repr__(self) -> str:
        return f"KDNode(point={self.point}, data={self.data})"


class KDTree:
    """
    KD树实现
    
    一种用于组织k维空间中点的空间分区数据结构。
    支持高效的最近邻搜索、范围查询和k近邻查询。
    
    时间复杂度：
    - 构建: O(n log n)
    - 插入: O(log n) 平均
    - 搜索: O(log n) 平均
    - 删除: O(log n) 平均
    
    示例：
        >>> tree = KDTree(dimension=2)
        >>> tree.insert([1, 2], data="点A")
        >>> tree.insert([3, 4], data="点B")
        >>> nearest = tree.nearest_neighbor([2, 3])
        >>> print(nearest.point)  # [1, 2]
    """
    
    def __init__(self, dimension: int, distance_metric: str = 'euclidean'):
        """
        初始化KD树
        
        Args:
            dimension: 数据的维度
            distance_metric: 距离度量 ('euclidean', 'manhattan', 'chebyshev')
        """
        if dimension < 1:
            raise ValueError("维度必须大于0")
        
        self.dimension = dimension
        self.distance_metric = distance_metric
        self.root: Optional[KDNode] = None
        self._size = 0
        
    def _distance(self, p1: List[float], p2: List[float]) -> float:
        """计算两点之间的距离"""
        if self.distance_metric == 'euclidean':
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
        elif self.distance_metric == 'manhattan':
            return sum(abs(a - b) for a, b in zip(p1, p2))
        elif self.distance_metric == 'chebyshev':
            return max(abs(a - b) for a, b in zip(p1, p2))
        else:
            raise ValueError(f"未知的距离度量: {self.distance_metric}")
    
    def _validate_point(self, point: List[float]) -> None:
        """验证点的维度"""
        if len(point) != self.dimension:
            raise ValueError(f"点维度不匹配: 期望 {self.dimension}, 得到 {len(point)}")
    
    def insert(self, point: List[float], data: Optional[T] = None) -> None:
        """
        插入一个点到KD树中
        
        Args:
            point: 要插入的点
            data: 与点关联的可选数据
        """
        self._validate_point(point)
        self.root = self._insert_recursive(self.root, point, data, 0)
        self._size += 1
    
    def _insert_recursive(
        self, 
        node: Optional[KDNode], 
        point: List[float], 
        data: Optional[T],
        depth: int
    ) -> KDNode:
        """递归插入节点"""
        if node is None:
            return KDNode(point=point, data=data, axis=depth % self.dimension)
        
        axis = depth % self.dimension
        
        if point[axis] < node.point[axis]:
            node.left = self._insert_recursive(node.left, point, data, depth + 1)
        else:
            node.right = self._insert_recursive(node.right, point, data, depth + 1)
        
        return node
    
    def build(self, points: List[Tuple[List[float], Optional[T]]]) -> None:
        """
        从点列表构建平衡的KD树
        
        Args:
            points: (点, 数据) 元组列表
        """
        if not points:
            return
        
        # 验证所有点
        for point, _ in points:
            self._validate_point(point)
        
        self.root = self._build_balanced(points, 0)
        self._size = len(points)
    
    def _build_balanced(
        self, 
        points: List[Tuple[List[float], Optional[T]]], 
        depth: int
    ) -> Optional[KDNode]:
        """递归构建平衡KD树"""
        if not points:
            return None
        
        axis = depth % self.dimension
        
        # 按当前轴排序找中位数
        points.sort(key=lambda x: x[0][axis])
        median_idx = len(points) // 2
        
        node = KDNode(
            point=points[median_idx][0],
            data=points[median_idx][1],
            axis=axis
        )
        
        node.left = self._build_balanced(points[:median_idx], depth + 1)
        node.right = self._build_balanced(points[median_idx + 1:], depth + 1)
        
        return node
    
    def nearest_neighbor(
        self, 
        query: List[float]
    ) -> Optional[Tuple[List[float], Optional[T], float]]:
        """
        查找最近的邻居
        
        Args:
            query: 查询点
            
        Returns:
            (最近的点, 关联数据, 距离) 或 None
        """
        self._validate_point(query)
        
        if self.root is None:
            return None
        
        best: List[Optional[Tuple[List[float], Optional[T], float]]] = [None]
        
        def search(node: Optional[KDNode], depth: int) -> None:
            if node is None:
                return
            
            dist = self._distance(query, node.point)
            
            if best[0] is None or dist < best[0][2]:
                best[0] = (node.point, node.data, dist)
            
            axis = depth % self.dimension
            diff = query[axis] - node.point[axis]
            
            # 先搜索更可能包含最近点的子树
            first, second = (node.left, node.right) if diff < 0 else (node.right, node.left)
            
            search(first, depth + 1)
            
            # 检查是否需要搜索另一棵子树
            if best[0] is None or abs(diff) < best[0][2]:
                search(second, depth + 1)
        
        search(self.root, 0)
        return best[0]
    
    def k_nearest_neighbors(
        self, 
        query: List[float], 
        k: int
    ) -> List[Tuple[List[float], Optional[T], float]]:
        """
        查找k个最近的邻居
        
        Args:
            query: 查询点
            k: 要查找的邻居数量
            
        Returns:
            [(点, 数据, 距离), ...] 列表，按距离排序
        """
        self._validate_point(query)
        
        if self.root is None or k <= 0:
            return []
        
        # 使用最大堆，堆中保留k个最近的点
        # Python的heapq是最小堆，所以存储负距离来实现最大堆
        heap: List[Tuple[float, int, List[float], Optional[T]]] = []
        counter = 0  # 用于处理相同距离的情况
        
        def search(node: Optional[KDNode], depth: int) -> None:
            nonlocal counter
            
            if node is None:
                return
            
            dist = self._distance(query, node.point)
            
            if len(heap) < k:
                heapq.heappush(heap, (-dist, counter, node.point, node.data))
                counter += 1
            elif dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, counter, node.point, node.data))
                counter += 1
            
            axis = depth % self.dimension
            diff = query[axis] - node.point[axis]
            
            first, second = (node.left, node.right) if diff < 0 else (node.right, node.left)
            
            search(first, depth + 1)
            
            # 检查是否需要搜索另一棵子树
            if len(heap) < k or abs(diff) < -heap[0][0]:
                search(second, depth + 1)
        
        search(self.root, 0)
        
        # 转换为排序的结果列表
        result = [(point, data, -neg_dist) for neg_dist, _, point, data in sorted(heap, reverse=True)]
        return result
    
    def range_query(
        self, 
        query: List[Tuple[float, float]]
    ) -> List[Tuple[List[float], Optional[T]]]:
        """
        范围查询：查找指定矩形范围内的所有点
        
        Args:
            query: 每个维度的范围 [(min1, max1), (min2, max2), ...]
            
        Returns:
            [(点, 数据), ...] 列表
        """
        if len(query) != self.dimension:
            raise ValueError(f"查询范围维度不匹配: 期望 {self.dimension}, 得到 {len(query)}")
        
        if self.root is None:
            return []
        
        result: List[Tuple[List[float], Optional[T]]] = []
        
        def search(node: Optional[KDNode]) -> None:
            if node is None:
                return
            
            # 检查当前点是否在范围内
            in_range = all(
                query[i][0] <= node.point[i] <= query[i][1]
                for i in range(self.dimension)
            )
            
            if in_range:
                result.append((node.point, node.data))
            
            axis = node.axis
            
            # 检查左子树
            if node.left and node.point[axis] >= query[axis][0]:
                search(node.left)
            
            # 检查右子树
            if node.right and node.point[axis] <= query[axis][1]:
                search(node.right)
        
        search(self.root)
        return result
    
    def radius_query(
        self, 
        center: List[float], 
        radius: float
    ) -> List[Tuple[List[float], Optional[T], float]]:
        """
        圆形/球形范围查询：查找距离中心点指定半径内的所有点
        
        Args:
            center: 中心点
            radius: 搜索半径
            
        Returns:
            [(点, 数据, 距离), ...] 列表
        """
        self._validate_point(center)
        
        if self.root is None or radius < 0:
            return []
        
        result: List[Tuple[List[float], Optional[T], float]] = []
        
        def search(node: Optional[KDNode], depth: int) -> None:
            if node is None:
                return
            
            dist = self._distance(center, node.point)
            
            if dist <= radius:
                result.append((node.point, node.data, dist))
            
            axis = depth % self.dimension
            diff = center[axis] - node.point[axis]
            
            # 搜索可能包含范围内点的子树
            if diff <= radius:
                search(node.right, depth + 1)
            if diff >= -radius:
                search(node.left, depth + 1)
        
        search(self.root, 0)
        return result
    
    def find(self, point: List[float]) -> Optional[KDNode]:
        """
        查找特定点
        
        Args:
            point: 要查找的点
            
        Returns:
            找到的节点或None
        """
        self._validate_point(point)
        return self._find_node(self.root, point, 0)
    
    def _find_node(
        self, 
        node: Optional[KDNode], 
        point: List[float], 
        depth: int
    ) -> Optional[KDNode]:
        """递归查找节点"""
        if node is None:
            return None
        
        if node.point == point:
            return node
        
        axis = depth % self.dimension
        
        if point[axis] < node.point[axis]:
            return self._find_node(node.left, point, depth + 1)
        else:
            return self._find_node(node.right, point, depth + 1)
    
    def delete(self, point: List[float]) -> bool:
        """
        从KD树中删除一个点
        
        Args:
            point: 要删除的点
            
        Returns:
            是否成功删除
        """
        self._validate_point(point)
        
        if self.root is None:
            return False
        
        result = [False]
        self.root = self._delete_recursive(self.root, point, 0, result)
        
        if result[0]:
            self._size -= 1
        
        return result[0]
    
    def _delete_recursive(
        self, 
        node: Optional[KDNode], 
        point: List[float], 
        depth: int,
        result: List[bool]
    ) -> Optional[KDNode]:
        """递归删除节点"""
        if node is None:
            return None
        
        axis = depth % self.dimension
        
        if node.point == point:
            result[0] = True
            
            # 如果是叶子节点，直接删除
            if node.left is None and node.right is None:
                return None
            
            # 如果右子树非空，找右子树的最小点
            if node.right is not None:
                min_node = self._find_min(node.right, axis, depth + 1)
                node.point = min_node.point
                node.data = min_node.data
                node.right = self._delete_recursive(node.right, min_node.point, depth + 1, [True])
            else:
                # 左子树非空，找左子树的最小点
                min_node = self._find_min(node.left, axis, depth + 1)
                node.point = min_node.point
                node.data = min_node.data
                node.right = self._delete_recursive(node.left, min_node.point, depth + 1, [True])
                node.left = None
            
            return node
        
        if point[axis] < node.point[axis]:
            node.left = self._delete_recursive(node.left, point, depth + 1, result)
        else:
            node.right = self._delete_recursive(node.right, point, depth + 1, result)
        
        return node
    
    def _find_min(self, node: KDNode, axis: int, depth: int) -> KDNode:
        """在子树中找到指定轴上最小的节点"""
        current_axis = depth % self.dimension
        
        if current_axis == axis:
            if node.left is None:
                return node
            return self._find_min(node.left, axis, depth + 1)
        else:
            min_node = node
            if node.left:
                left_min = self._find_min(node.left, axis, depth + 1)
                if left_min.point[axis] < min_node.point[axis]:
                    min_node = left_min
            if node.right:
                right_min = self._find_min(node.right, axis, depth + 1)
                if right_min.point[axis] < min_node.point[axis]:
                    min_node = right_min
            return min_node
    
    def contains(self, point: List[float]) -> bool:
        """检查树中是否包含指定点"""
        return self.find(point) is not None
    
    def size(self) -> int:
        """返回树中节点的数量"""
        return self._size
    
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self.root is None
    
    def height(self) -> int:
        """计算树的高度"""
        def _height(node: Optional[KDNode]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
        return _height(self.root)
    
    def is_balanced(self) -> bool:
        """检查树是否平衡"""
        def check(node: Optional[KDNode]) -> Tuple[bool, int]:
            if node is None:
                return True, 0
            
            left_balanced, left_height = check(node.left)
            right_balanced, right_height = check(node.right)
            
            balanced = left_balanced and right_balanced and abs(left_height - right_height) <= 1
            return balanced, 1 + max(left_height, right_height)
        
        balanced, _ = check(self.root)
        return balanced
    
    def all_points(self) -> List[Tuple[List[float], Optional[T]]]:
        """返回树中所有点"""
        result: List[Tuple[List[float], Optional[T]]] = []
        
        def traverse(node: Optional[KDNode]) -> None:
            if node is None:
                return
            result.append((node.point, node.data))
            traverse(node.left)
            traverse(node.right)
        
        traverse(self.root)
        return result
    
    def to_dict(self) -> dict:
        """将树转换为字典表示"""
        def node_to_dict(node: Optional[KDNode]) -> Optional[dict]:
            if node is None:
                return None
            return {
                'point': node.point,
                'data': node.data,
                'axis': node.axis,
                'left': node_to_dict(node.left),
                'right': node_to_dict(node.right)
            }
        
        return {
            'dimension': self.dimension,
            'distance_metric': self.distance_metric,
            'size': self._size,
            'height': self.height(),
            'root': node_to_dict(self.root)
        }
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"KDTree(dimension={self.dimension}, size={self._size}, height={self.height()})"


def create_kd_tree(
    points: List[Tuple[List[float], Any]], 
    dimension: Optional[int] = None,
    distance_metric: str = 'euclidean'
) -> KDTree:
    """
    便捷函数：从点列表创建KD树
    
    Args:
        points: [(点, 数据), ...] 列表
        dimension: 维度（None则自动推断）
        distance_metric: 距离度量
        
    Returns:
        构建好的KD树
    """
    if not points:
        raise ValueError("点列表不能为空")
    
    dim = dimension if dimension else len(points[0][0])
    tree = KDTree(dim, distance_metric)
    tree.build(points)
    return tree


def nearest_neighbor_search(
    points: List[List[float]],
    query: List[float],
    k: int = 1,
    distance_metric: str = 'euclidean'
) -> List[Tuple[List[float], float]]:
    """
    便捷函数：在点集合中查找最近邻
    
    Args:
        points: 点集合
        query: 查询点
        k: 近邻数量
        distance_metric: 距离度量
        
    Returns:
        [(点, 距离), ...] 列表
    """
    if not points:
        return []
    
    dimension = len(points[0])
    tree = KDTree(dimension, distance_metric)
    
    for point in points:
        tree.insert(point)
    
    neighbors = tree.k_nearest_neighbors(query, k)
    return [(p, d) for p, _, d in neighbors]


class KDTreeBuilder:
    """
    KD树构建器（流式API）
    
    示例：
        >>> tree = (KDTreeBuilder(2)
        ...     .add([1, 2], "A")
        ...     .add([3, 4], "B")
        ...     .build())
    """
    
    def __init__(self, dimension: int, distance_metric: str = 'euclidean'):
        self.dimension = dimension
        self.distance_metric = distance_metric
        self._points: List[Tuple[List[float], Any]] = []
    
    def add(self, point: List[float], data: Any = None) -> 'KDTreeBuilder':
        """添加一个点"""
        self._points.append((point, data))
        return self
    
    def add_many(self, points: List[Tuple[List[float], Any]]) -> 'KDTreeBuilder':
        """添加多个点"""
        self._points.extend(points)
        return self
    
    def build(self) -> KDTree:
        """构建KD树"""
        tree = KDTree(self.dimension, self.distance_metric)
        tree.build(self._points)
        return tree
    
    def clear(self) -> 'KDTreeBuilder':
        """清空已添加的点"""
        self._points.clear()
        return self


if __name__ == "__main__":
    # 简单示例
    print("=== KD树工具模块示例 ===\n")
    
    # 创建2D KD树
    tree = KDTree(dimension=2)
    
    # 插入点
    points = [
        ([2, 3], "A点"),
        ([5, 4], "B点"),
        ([9, 6], "C点"),
        ([4, 7], "D点"),
        ([8, 1], "E点"),
        ([7, 2], "F点"),
    ]
    
    for point, data in points:
        tree.insert(point, data)
    
    print(f"树的大小: {tree.size()}")
    print(f"树的高度: {tree.height()}")
    print(f"是否平衡: {tree.is_balanced()}")
    
    # 最近邻查询
    query = [6, 3]
    nearest = tree.nearest_neighbor(query)
    if nearest:
        print(f"\n查询点: {query}")
        print(f"最近邻: 点={nearest[0]}, 数据={nearest[1]}, 距离={nearest[2]:.2f}")
    
    # k近邻查询
    print(f"\n3个最近邻:")
    k_nearest = tree.k_nearest_neighbors(query, 3)
    for i, (point, data, dist) in enumerate(k_nearest, 1):
        print(f"  {i}. {point} ({data}) - 距离: {dist:.2f}")
    
    # 范围查询
    print(f"\n范围查询 [(4, 8), (2, 5)]:")
    in_range = tree.range_query([(4, 8), (2, 5)])
    for point, data in in_range:
        print(f"  {point} ({data})")
    
    # 圆形范围查询
    print(f"\n圆形范围查询 (中心=[5, 4], 半径=3):")
    in_radius = tree.radius_query([5, 4], 3)
    for point, data, dist in sorted(in_radius, key=lambda x: x[2]):
        print(f"  {point} ({data}) - 距离: {dist:.2f}")
    
    # 使用构建器
    print("\n=== 使用构建器 ===")
    tree2 = (KDTreeBuilder(2)
        .add([1, 1], "P1")
        .add([2, 2], "P2")
        .add([3, 3], "P3")
        .build())
    
    print(f"构建器创建的树: {tree2}")