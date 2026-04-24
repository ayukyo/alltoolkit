"""
四叉树工具模块 (Quadtree Utilities)

四叉树是一种树数据结构，用于高效地分割二维空间。
每个内部节点恰好有四个子节点，常用于空间索引、图像压缩、碰撞检测等场景。

核心功能:
- 点插入与删除
- 范围查询 (矩形区域内的所有点)
- 最近邻查询 (KNN)
- 半径查询 (圆形区域内的所有点)
- 边界矩形查询
- 自动分裂与合并
- 支持自定义数据

时间复杂度:
- 插入: O(log n) 平均情况
- 删除: O(log n) 平均情况
- 范围查询: O(log n + k)，k为结果数量
- 最近邻: O(log n) 平均情况

零外部依赖，纯 Python 实现。
"""

from dataclasses import dataclass, field
from typing import Generic, TypeVar, List, Optional, Tuple, Callable, Iterator, Any
from math import inf, sqrt

T = TypeVar('T')


@dataclass
class Point(Generic[T]):
    """二维点，可携带任意数据"""
    x: float
    y: float
    data: Optional[T] = None
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        if self.data is not None:
            return f"Point({self.x}, {self.y}, data={self.data!r})"
        return f"Point({self.x}, {self.y})"


@dataclass
class Rectangle:
    """
    轴对齐边界矩形 (Axis-Aligned Bounding Box)
    
    Attributes:
        x: 左边界 x 坐标
        y: 上边界 y 坐标
        width: 宽度
        height: 高度
    """
    x: float
    y: float
    width: float
    height: float
    
    @property
    def left(self) -> float:
        """左边界"""
        return self.x
    
    @property
    def right(self) -> float:
        """右边界"""
        return self.x + self.width
    
    @property
    def top(self) -> float:
        """上边界"""
        return self.y
    
    @property
    def bottom(self) -> float:
        """下边界"""
        return self.y + self.height
    
    @property
    def center(self) -> Tuple[float, float]:
        """中心点坐标"""
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    @property
    def area(self) -> float:
        """面积"""
        return self.width * self.height
    
    def contains_point(self, point: Point) -> bool:
        """检查点是否在矩形内"""
        return (self.left <= point.x < self.right and
                self.top <= point.y < self.bottom)
    
    def intersects(self, other: 'Rectangle') -> bool:
        """检查两个矩形是否相交"""
        return not (other.left >= self.right or
                    other.right <= self.left or
                    other.top >= self.bottom or
                    other.bottom <= self.top)
    
    def contains_rect(self, other: 'Rectangle') -> bool:
        """检查另一个矩形是否完全包含在内"""
        return (other.left >= self.left and
                other.right <= self.right and
                other.top >= self.top and
                other.bottom <= self.bottom)
    
    def __repr__(self) -> str:
        return f"Rectangle(x={self.x}, y={self.y}, w={self.width}, h={self.height})"


@dataclass
class Circle:
    """圆形区域"""
    x: float  # 圆心 x
    y: float  # 圆心 y
    radius: float
    
    def contains_point(self, point: Point) -> bool:
        """检查点是否在圆内"""
        dx = point.x - self.x
        dy = point.y - self.y
        return dx * dx + dy * dy <= self.radius * self.radius
    
    def intersects_rect(self, rect: Rectangle) -> bool:
        """检查圆与矩形是否相交"""
        # 找到矩形上离圆心最近的点
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))
        
        dx = self.x - closest_x
        dy = self.y - closest_y
        
        return dx * dx + dy * dy <= self.radius * self.radius


class QuadTreeNode(Generic[T]):
    """四叉树节点"""
    
    # 子节点方位常量
    NW = 0  # 西北 (左上)
    NE = 1  # 东北 (右上)
    SW = 2  # 西南 (左下)
    SE = 3  # 东南 (右下)
    
    def __init__(
        self,
        boundary: Rectangle,
        capacity: int = 4,
        max_depth: int = 8,
        depth: int = 0
    ):
        """
        初始化四叉树节点
        
        Args:
            boundary: 节点的边界矩形
            capacity: 节点分裂前最大容量
            max_depth: 最大深度
            depth: 当前深度
        """
        self.boundary = boundary
        self.capacity = capacity
        self.max_depth = max_depth
        self.depth = depth
        self.points: List[Point[T]] = []
        self.children: Optional[List[Any]] = None  # List[QuadTreeNode[T]] or None
        self._total_points = 0  # 该节点及其子树的总点数
    
    @property
    def is_leaf(self) -> bool:
        """是否为叶子节点"""
        return self.children is None
    
    @property
    def is_empty(self) -> bool:
        """是否为空节点"""
        return self._total_points == 0
    
    def _subdivide(self) -> None:
        """将当前节点分裂为四个子节点"""
        if not self.is_leaf:
            return
        
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.width / 2, self.boundary.height / 2
        new_depth = self.depth + 1
        
        self.children = [
            QuadTreeNode(  # 西北 (左上)
                Rectangle(x, y, w, h),
                self.capacity,
                self.max_depth,
                new_depth
            ),
            QuadTreeNode(  # 东北 (右上)
                Rectangle(x + w, y, w, h),
                self.capacity,
                self.max_depth,
                new_depth
            ),
            QuadTreeNode(  # 西南 (左下)
                Rectangle(x, y + h, w, h),
                self.capacity,
                self.max_depth,
                new_depth
            ),
            QuadTreeNode(  # 东南 (右下)
                Rectangle(x + w, y + h, w, h),
                self.capacity,
                self.max_depth,
                new_depth
            ),
        ]
        
        # 将当前节点的点重新分配到子节点（不更新计数，因为总数没变）
        for point in self.points:
            quadrant = self._get_quadrant(point)
            if quadrant is not None:
                child = self.children[quadrant]
                # 直接添加到子节点，不更新父节点计数
                child.points.append(point)
                child._total_points += 1
        self.points.clear()
    
    def _get_quadrant(self, point: Point) -> Optional[int]:
        """确定点应该进入哪个象限"""
        if not self.boundary.contains_point(point):
            return None
        
        mid_x = self.boundary.x + self.boundary.width / 2
        mid_y = self.boundary.y + self.boundary.height / 2
        
        if point.x < mid_x:
            return self.SW if point.y >= mid_y else self.NW
        else:
            return self.SE if point.y >= mid_y else self.NE
    
    def _insert_to_child(self, point: Point) -> bool:
        """将点插入到子节点"""
        quadrant = self._get_quadrant(point)
        if quadrant is None:
            return False
        child = self.children[quadrant]
        if child is None:
            return False
        if child.insert(point):
            self._total_points += 1
            return True
        return False
    
    def insert(self, point: Point) -> bool:
        """
        插入一个点
        
        Args:
            point: 要插入的点
            
        Returns:
            是否插入成功
        """
        if not self.boundary.contains_point(point):
            return False
        
        if self.is_leaf:
            if len(self.points) < self.capacity or self.depth >= self.max_depth:
                self.points.append(point)
                self._total_points += 1
                return True
            
            # 需要分裂
            self._subdivide()
            
            # 现在是内部节点，将新点插入到子节点
            return self._insert_to_child(point)
        else:
            # 内部节点，插入到子节点
            return self._insert_to_child(point)
    
    def remove(self, point: Point) -> bool:
        """
        删除一个点
        
        Args:
            point: 要删除的点
            
        Returns:
            是否删除成功
        """
        if not self.boundary.contains_point(point):
            return False
        
        if self.is_leaf:
            for i, p in enumerate(self.points):
                if p.x == point.x and p.y == point.y:
                    self.points.pop(i)
                    self._total_points -= 1
                    return True
            return False
        else:
            quadrant = self._get_quadrant(point)
            if quadrant is None:
                return False
            
            child = self.children[quadrant]
            if child is None:
                return False
            
            if child.remove(point):
                self._total_points -= 1
                
                # 检查是否可以合并子节点
                if self._total_points <= self.capacity:
                    self._merge()
                
                return True
            return False
    
    def _merge(self) -> None:
        """合并子节点"""
        if self.is_leaf:
            return
        
        self.points = list(self.query(Rectangle(
            self.boundary.x,
            self.boundary.y,
            self.boundary.width,
            self.boundary.height
        )))
        self.children = None
    
    def query(self, region: Rectangle) -> Iterator[Point[T]]:
        """
        查询矩形区域内的所有点
        
        Args:
            region: 查询区域
            
        Yields:
            区域内的点
        """
        if not self.boundary.intersects(region):
            return
        
        if self.is_leaf:
            for point in self.points:
                if region.contains_point(point):
                    yield point
        else:
            for child in self.children:
                if child is not None and not child.is_empty:
                    yield from child.query(region)
    
    def query_circle(self, circle: Circle) -> Iterator[Point[T]]:
        """
        查询圆形区域内的所有点
        
        Args:
            circle: 圆形区域
            
        Yields:
            区域内的点
        """
        if not circle.intersects_rect(self.boundary):
            return
        
        if self.is_leaf:
            for point in self.points:
                if circle.contains_point(point):
                    yield point
        else:
            for child in self.children:
                if child is not None and not child.is_empty:
                    yield from child.query_circle(circle)
    
    def find_nearest(
        self,
        point: Point,
        k: int = 1,
        exclude_self: bool = False
    ) -> List[Tuple[Point[T], float]]:
        """
        查找最近的 k 个点
        
        Args:
            point: 查询点
            k: 返回最近点的数量
            exclude_self: 是否排除与查询点坐标相同的点
            
        Returns:
            (点, 距离) 元组列表，按距离升序排列
        """
        result: List[Tuple[Point[T], float]] = []
        
        def search(node: QuadTreeNode[T]) -> None:
            if node.is_empty:
                return
            
            # 剪枝：如果最小可能的距离都大于当前第 k 远的距离，跳过
            if len(result) >= k:
                min_dist = node._min_distance_to_point(point)
                if min_dist > result[-1][1]:
                    return
            
            if node.is_leaf:
                for p in node.points:
                    if exclude_self and p.x == point.x and p.y == point.y:
                        continue
                    dist = sqrt((p.x - point.x) ** 2 + (p.y - point.y) ** 2)
                    result.append((p, dist))
            else:
                # 按到查询点的距离排序子节点，优先搜索更近的
                child_distances = []
                for i, child in enumerate(node.children):
                    if child is not None and not child.is_empty:
                        dist = child._min_distance_to_point(point)
                        child_distances.append((dist, i, child))
                
                child_distances.sort(key=lambda x: x[0])
                for _, _, child in child_distances:
                    search(child)
        
        search(self)
        
        # 排序并取前 k 个
        result.sort(key=lambda x: x[1])
        return result[:k]
    
    def _min_distance_to_point(self, point: Point) -> float:
        """计算点到边界矩形的最小距离"""
        dx = 0.0
        if point.x < self.boundary.left:
            dx = self.boundary.left - point.x
        elif point.x > self.boundary.right:
            dx = point.x - self.boundary.right
        
        dy = 0.0
        if point.y < self.boundary.top:
            dy = self.boundary.top - point.y
        elif point.y > self.boundary.bottom:
            dy = point.y - self.boundary.bottom
        
        return sqrt(dx * dx + dy * dy)
    
    def find_in_radius(self, point: Point, radius: float) -> List[Tuple[Point[T], float]]:
        """
        查找半径范围内的所有点
        
        Args:
            point: 圆心
            radius: 半径
            
        Returns:
            (点, 距离) 元组列表
        """
        circle = Circle(point.x, point.y, radius)
        result = []
        
        for p in self.query_circle(circle):
            dist = sqrt((p.x - point.x) ** 2 + (p.y - point.y) ** 2)
            if dist <= radius:
                result.append((p, dist))
        
        result.sort(key=lambda x: x[1])
        return result
    
    def for_each(self, callback: Callable[[Point[T]], None]) -> None:
        """
        遍历所有点
        
        Args:
            callback: 对每个点调用的函数
        """
        if self.is_leaf:
            for point in self.points:
                callback(point)
        else:
            for child in self.children:
                if child is not None and not child.is_empty:
                    child.for_each(callback)
    
    def all_points(self) -> List[Point[T]]:
        """返回所有点的列表"""
        result: List[Point[T]] = []
        self.for_each(result.append)
        return result
    
    def __len__(self) -> int:
        """返回点的总数"""
        return self._total_points
    
    def __iter__(self) -> Iterator[Point[T]]:
        """迭代所有点"""
        return self.query(Rectangle(
            self.boundary.x,
            self.boundary.y,
            self.boundary.width,
            self.boundary.height
        ))


class QuadTree(Generic[T]):
    """
    四叉树 - 二维空间索引数据结构
    
    四叉树递归地将二维空间划分为四个象限，适合存储和查询空间点数据。
    
    Example:
        >>> tree = QuadTree(Rectangle(0, 0, 100, 100))
        >>> tree.insert(Point(10, 10, "A"))
        >>> tree.insert(Point(50, 50, "B"))
        >>> list(tree.query(Rectangle(0, 0, 20, 20)))
        [Point(10, 10, data='A')]
    """
    
    def __init__(
        self,
        boundary: Rectangle,
        capacity: int = 4,
        max_depth: int = 8
    ):
        """
        创建四叉树
        
        Args:
            boundary: 整个树的边界矩形
            capacity: 每个节点的最大容量（分裂前）
            max_depth: 最大深度
        """
        self._root = QuadTreeNode(boundary, capacity, max_depth)
        self._capacity = capacity
        self._max_depth = max_depth
    
    @property
    def boundary(self) -> Rectangle:
        """边界矩形"""
        return self._root.boundary
    
    @property
    def capacity(self) -> int:
        """节点容量"""
        return self._capacity
    
    @property
    def max_depth(self) -> int:
        """最大深度"""
        return self._max_depth
    
    def insert(self, point: Point[T]) -> bool:
        """
        插入一个点
        
        Args:
            point: 要插入的点
            
        Returns:
            是否插入成功
        """
        return self._root.insert(point)
    
    def insert_many(self, points: List[Point[T]]) -> int:
        """
        批量插入点
        
        Args:
            points: 点列表
            
        Returns:
            成功插入的数量
        """
        count = 0
        for point in points:
            if self.insert(point):
                count += 1
        return count
    
    def remove(self, point: Point[T]) -> bool:
        """
        删除一个点
        
        Args:
            point: 要删除的点（根据坐标匹配）
            
        Returns:
            是否删除成功
        """
        return self._root.remove(point)
    
    def query(self, region: Rectangle) -> List[Point[T]]:
        """
        查询矩形区域内的所有点
        
        Args:
            region: 查询区域
            
        Returns:
            区域内的点列表
        """
        return list(self._root.query(region))
    
    def query_circle(self, circle: Circle) -> List[Point[T]]:
        """
        查询圆形区域内的所有点
        
        Args:
            circle: 圆形区域
            
        Returns:
            区域内的点列表
        """
        return list(self._root.query_circle(circle))
    
    def find_nearest(
        self,
        point: Point,
        k: int = 1,
        exclude_self: bool = False
    ) -> List[Tuple[Point[T], float]]:
        """
        查找最近的 k 个点
        
        Args:
            point: 查询点
            k: 返回最近点的数量
            exclude_self: 是否排除与查询点坐标相同的点
            
        Returns:
            (点, 距离) 元组列表
        """
        return self._root.find_nearest(point, k, exclude_self)
    
    def find_nearest_one(
        self,
        point: Point,
        exclude_self: bool = False
    ) -> Optional[Tuple[Point[T], float]]:
        """
        查找最近的一个点
        
        Args:
            point: 查询点
            exclude_self: 是否排除与查询点坐标相同的点
            
        Returns:
            (点, 距离) 元组，如果没有找到则返回 None
        """
        result = self.find_nearest(point, 1, exclude_self)
        return result[0] if result else None
    
    def find_in_radius(
        self,
        point: Point,
        radius: float
    ) -> List[Tuple[Point[T], float]]:
        """
        查找半径范围内的所有点
        
        Args:
            point: 圆心
            radius: 半径
            
        Returns:
            (点, 距离) 元组列表
        """
        return self._root.find_in_radius(point, radius)
    
    def for_each(self, callback: Callable[[Point[T]], None]) -> None:
        """
        遍历所有点
        
        Args:
            callback: 对每个点调用的函数
        """
        self._root.for_each(callback)
    
    def all_points(self) -> List[Point[T]]:
        """返回所有点的列表"""
        return self._root.all_points()
    
    def clear(self) -> None:
        """清空四叉树"""
        self._root = QuadTreeNode(
            self.boundary,
            self._capacity,
            self._max_depth
        )
    
    def __len__(self) -> int:
        """返回点的总数"""
        return len(self._root)
    
    def __iter__(self) -> Iterator[Point[T]]:
        """迭代所有点"""
        return iter(self._root)
    
    def __contains__(self, point: Point) -> bool:
        """检查点是否存在"""
        for p in self.query(Rectangle(point.x, point.y, 1, 1)):
            if p.x == point.x and p.y == point.y:
                return True
        return False
    
    def __repr__(self) -> str:
        return f"QuadTree(boundary={self.boundary}, points={len(self)})"


# ============ 便捷工厂函数 ============

def create_quadtree(
    x: float = 0,
    y: float = 0,
    width: float = 100,
    height: float = 100,
    capacity: int = 4,
    max_depth: int = 8
) -> QuadTree:
    """
    创建四叉树的便捷函数
    
    Args:
        x: 左边界 x 坐标
        y: 上边界 y 坐标
        width: 宽度
        height: 高度
        capacity: 节点容量
        max_depth: 最大深度
        
    Returns:
        新的四叉树实例
    """
    return QuadTree(
        Rectangle(x, y, width, height),
        capacity,
        max_depth
    )


def from_points(
    points: List[Point[T]],
    capacity: int = 4,
    max_depth: int = 8,
    padding: float = 1.0
) -> QuadTree[T]:
    """
    从点列表创建四叉树
    
    自动计算边界矩形以包含所有点。
    
    Args:
        points: 点列表
        capacity: 节点容量
        max_depth: 最大深度
        padding: 边界留白
        
    Returns:
        包含所有点的四叉树
    """
    if not points:
        return create_quadtree(capacity=capacity, max_depth=max_depth)
    
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    
    # 确保边界有效
    width = max(max_x - min_x, 1) + padding * 2
    height = max(max_y - min_y, 1) + padding * 2
    
    tree = QuadTree(
        Rectangle(min_x - padding, min_y - padding, width, height),
        capacity,
        max_depth
    )
    
    for point in points:
        tree.insert(point)
    
    return tree