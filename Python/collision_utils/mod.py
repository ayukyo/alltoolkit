"""
Collision Detection Utilities - 碰撞检测工具模块

提供全面的2D碰撞检测功能，包括矩形、圆形、多边形、射线等碰撞检测。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

import math
from typing import Tuple, List, Optional, Union
from dataclasses import dataclass

# 类型别名
Point = Tuple[float, float]
Vector2 = Tuple[float, float]


@dataclass
class Rectangle:
    """矩形类"""
    x: float
    y: float
    width: float
    height: float
    
    @property
    def left(self) -> float:
        return self.x
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def top(self) -> float:
        return self.y
    
    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    @property
    def center(self) -> Point:
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    @property
    def center_x(self) -> float:
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        return self.y + self.height / 2
    
    def contains_point(self, px: float, py: float) -> bool:
        """检查点是否在矩形内"""
        return self.left <= px <= self.right and self.top <= py <= self.bottom
    
    def get_vertices(self) -> List[Point]:
        """获取矩形的四个顶点"""
        return [
            (self.left, self.top),
            (self.right, self.top),
            (self.right, self.bottom),
            (self.left, self.bottom)
        ]


@dataclass
class Circle:
    """圆形类"""
    x: float
    y: float
    radius: float
    
    @property
    def center(self) -> Point:
        return (self.x, self.y)
    
    def contains_point(self, px: float, py: float) -> bool:
        """检查点是否在圆内"""
        dx = px - self.x
        dy = py - self.y
        return dx * dx + dy * dy <= self.radius * self.radius
    
    def get_bounding_box(self) -> Rectangle:
        """获取外接矩形"""
        return Rectangle(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


@dataclass
class Line:
    """线段类"""
    x1: float
    y1: float
    x2: float
    y2: float
    
    @property
    def start(self) -> Point:
        return (self.x1, self.y1)
    
    @property
    def end(self) -> Point:
        return (self.x2, self.y2)
    
    @property
    def length(self) -> float:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return math.sqrt(dx * dx + dy * dy)
    
    @property
    def length_squared(self) -> float:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return dx * dx + dy * dy
    
    def get_bounding_box(self) -> Rectangle:
        """获取外接矩形"""
        x = min(self.x1, self.x2)
        y = min(self.y1, self.y2)
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)
        return Rectangle(x, y, width, height)


@dataclass
class Polygon:
    """多边形类"""
    vertices: List[Point]
    
    def __post_init__(self):
        if len(self.vertices) < 3:
            raise ValueError("多边形至少需要3个顶点")
    
    @property
    def center(self) -> Point:
        """计算多边形的中心点"""
        cx = sum(v[0] for v in self.vertices) / len(self.vertices)
        cy = sum(v[1] for v in self.vertices) / len(self.vertices)
        return (cx, cy)
    
    def get_edges(self) -> List[Line]:
        """获取所有边"""
        edges = []
        n = len(self.vertices)
        for i in range(n):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % n]
            edges.append(Line(p1[0], p1[1], p2[0], p2[1]))
        return edges
    
    def get_bounding_box(self) -> Rectangle:
        """获取外接矩形"""
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        x = min(xs)
        y = min(ys)
        width = max(xs) - x
        height = max(ys) - y
        return Rectangle(x, y, width, height)


@dataclass
class Ray:
    """射线类"""
    origin_x: float
    origin_y: float
    direction_x: float
    direction_y: float
    
    def __post_init__(self):
        # 归一化方向向量
        length = math.sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        if length > 0:
            self.direction_x /= length
            self.direction_y /= length
    
    @property
    def origin(self) -> Point:
        return (self.origin_x, self.origin_y)
    
    @property
    def direction(self) -> Vector2:
        return (self.direction_x, self.direction_y)
    
    def get_point(self, t: float) -> Point:
        """获取射线上距离原点 t 单位的点"""
        return (
            self.origin_x + self.direction_x * t,
            self.origin_y + self.direction_y * t
        )


@dataclass
class RaycastHit:
    """射线碰撞结果"""
    hit: bool
    point: Optional[Point] = None
    distance: float = float('inf')
    normal: Optional[Vector2] = None
    shape: Optional[object] = None


class CollisionUtils:
    """碰撞检测工具类"""
    
    # ==================== 点碰撞检测 ====================
    
    @staticmethod
    def point_in_circle(px: float, py: float, circle: Circle) -> bool:
        """检查点是否在圆内"""
        return circle.contains_point(px, py)
    
    @staticmethod
    def point_in_rectangle(px: float, py: float, rect: Rectangle) -> bool:
        """检查点是否在矩形内"""
        return rect.contains_point(px, py)
    
    @staticmethod
    def point_in_polygon(px: float, py: float, polygon: Polygon) -> bool:
        """
        检查点是否在多边形内（射线法）
        从点向右发射射线，计算与多边形边的交点数
        """
        vertices = polygon.vertices
        n = len(vertices)
        inside = False
        
        j = n - 1
        for i in range(n):
            xi, yi = vertices[i]
            xj, yj = vertices[j]
            
            if ((yi > py) != (yj > py)) and \
               (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                inside = not inside
            
            j = i
        
        return inside
    
    @staticmethod
    def point_on_line(px: float, py: float, line: Line, threshold: float = 1e-10) -> bool:
        """检查点是否在线段上"""
        # 使用叉积判断点是否在直线上
        cross = (py - line.y1) * (line.x2 - line.x1) - \
                (px - line.x1) * (line.y2 - line.y1)
        
        if abs(cross) > threshold:
            return False
        
        # 检查点是否在线段范围内
        min_x = min(line.x1, line.x2)
        max_x = max(line.x1, line.x2)
        min_y = min(line.y1, line.y2)
        max_y = max(line.y1, line.y2)
        
        return min_x - threshold <= px <= max_x + threshold and \
               min_y - threshold <= py <= max_y + threshold
    
    # ==================== 矩形碰撞检测 ====================
    
    @staticmethod
    def rectangle_rectangle(rect1: Rectangle, rect2: Rectangle) -> bool:
        """检查两个矩形是否碰撞（AABB碰撞检测）"""
        return (rect1.left < rect2.right and
                rect1.right > rect2.left and
                rect1.top < rect2.bottom and
                rect1.bottom > rect2.top)
    
    @staticmethod
    def rectangle_circle(rect: Rectangle, circle: Circle) -> bool:
        """检查矩形和圆是否碰撞"""
        # 找到矩形上距离圆心最近的点
        closest_x = max(rect.left, min(circle.x, rect.right))
        closest_y = max(rect.top, min(circle.y, rect.bottom))
        
        # 计算距离平方
        dx = circle.x - closest_x
        dy = circle.y - closest_y
        
        return dx * dx + dy * dy <= circle.radius * circle.radius
    
    @staticmethod
    def rectangle_line(rect: Rectangle, line: Line) -> bool:
        """检查矩形和线段是否碰撞"""
        # 先检查线段端点是否在矩形内
        if rect.contains_point(line.x1, line.y1):
            return True
        if rect.contains_point(line.x2, line.y2):
            return True
        
        # 检查线段是否与矩形的四条边相交
        edges = [
            Line(rect.left, rect.top, rect.right, rect.top),      # 上边
            Line(rect.right, rect.top, rect.right, rect.bottom),   # 右边
            Line(rect.left, rect.bottom, rect.right, rect.bottom), # 下边
            Line(rect.left, rect.top, rect.left, rect.bottom)      # 左边
        ]
        
        for edge in edges:
            if CollisionUtils.line_line(line, edge):
                return True
        
        return False
    
    @staticmethod
    def rectangle_polygon(rect: Rectangle, polygon: Polygon) -> bool:
        """检查矩形和多边形是否碰撞"""
        # 检查多边形的任意顶点是否在矩形内
        for v in polygon.vertices:
            if rect.contains_point(v[0], v[1]):
                return True
        
        # 检查矩形的任意顶点是否在多边形内
        for v in rect.get_vertices():
            if CollisionUtils.point_in_polygon(v[0], v[1], polygon):
                return True
        
        # 检查边的相交
        for edge in polygon.get_edges():
            if CollisionUtils.rectangle_line(rect, edge):
                return True
        
        return False
    
    # ==================== 圆形碰撞检测 ====================
    
    @staticmethod
    def circle_circle(c1: Circle, c2: Circle) -> bool:
        """检查两个圆是否碰撞"""
        dx = c2.x - c1.x
        dy = c2.y - c1.y
        distance_squared = dx * dx + dy * dy
        radius_sum = c1.radius + c2.radius
        return distance_squared <= radius_sum * radius_sum
    
    @staticmethod
    def circle_line(circle: Circle, line: Line) -> bool:
        """检查圆和线段是否碰撞"""
        # 计算线段向量
        dx = line.x2 - line.x1
        dy = line.y2 - line.y1
        
        # 计算圆心到线段起点的向量
        fx = line.x1 - circle.x
        fy = line.y1 - circle.y
        
        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - circle.radius * circle.radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return False
        
        # 检查交点是否在线段上
        discriminant = math.sqrt(discriminant)
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        
        return (0 <= t1 <= 1) or (0 <= t2 <= 1) or (t1 < 0 and t2 > 1)
    
    @staticmethod
    def circle_polygon(circle: Circle, polygon: Polygon) -> bool:
        """检查圆和多边形是否碰撞"""
        # 检查圆心是否在多边形内
        if CollisionUtils.point_in_polygon(circle.x, circle.y, polygon):
            return True
        
        # 检查多边形的任意边是否与圆相交
        for edge in polygon.get_edges():
            if CollisionUtils.circle_line(circle, edge):
                return True
        
        return False
    
    # ==================== 线段碰撞检测 ====================
    
    @staticmethod
    def line_line(line1: Line, line2: Line) -> bool:
        """检查两条线段是否相交"""
        def ccw(ax, ay, bx, by, cx, cy):
            return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)
        
        return (ccw(line1.x1, line1.y1, line2.x1, line2.y1, line2.x2, line2.y2) != 
                ccw(line1.x2, line1.y2, line2.x1, line2.y1, line2.x2, line2.y2) and
                ccw(line1.x1, line1.y1, line1.x2, line1.y2, line2.x1, line2.y1) != 
                ccw(line1.x1, line1.y1, line1.x2, line1.y2, line2.x2, line2.y2))
    
    @staticmethod
    def line_polygon(line: Line, polygon: Polygon) -> bool:
        """检查线段和多边形是否碰撞"""
        # 检查线段端点是否在多边形内
        if CollisionUtils.point_in_polygon(line.x1, line.y1, polygon):
            return True
        if CollisionUtils.point_in_polygon(line.x2, line.y2, polygon):
            return True
        
        # 检查线段是否与多边形的边相交
        for edge in polygon.get_edges():
            if CollisionUtils.line_line(line, edge):
                return True
        
        return False
    
    # ==================== 多边形碰撞检测 ====================
    
    @staticmethod
    def polygon_polygon(poly1: Polygon, poly2: Polygon) -> bool:
        """检查两个多边形是否碰撞（分离轴定理SAT）"""
        def project_polygon(vertices: List[Point], axis: Vector2):
            dots = [v[0] * axis[0] + v[1] * axis[1] for v in vertices]
            return min(dots), max(dots)
        
        def get_axes(vertices: List[Point]) -> List[Vector2]:
            axes = []
            n = len(vertices)
            for i in range(n):
                p1 = vertices[i]
                p2 = vertices[(i + 1) % n]
                edge = (p2[0] - p1[0], p2[1] - p1[1])
                # 法向量
                normal = (-edge[1], edge[0])
                # 归一化
                length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
                if length > 0:
                    axes.append((normal[0] / length, normal[1] / length))
            return axes
        
        # 获取两个多边形的所有分离轴
        axes = get_axes(poly1.vertices) + get_axes(poly2.vertices)
        
        for axis in axes:
            min1, max1 = project_polygon(poly1.vertices, axis)
            min2, max2 = project_polygon(poly2.vertices, axis)
            
            # 如果存在分离轴，则不碰撞
            if max1 < min2 or max2 < min1:
                return False
        
        return True
    
    # ==================== 射线碰撞检测 ====================
    
    @staticmethod
    def ray_rectangle(ray: Ray, rect: Rectangle) -> RaycastHit:
        """射线与矩形碰撞检测"""
        t_min = 0.0
        t_max = float('inf')
        normal = (0.0, 0.0)
        
        # 检查X轴
        if abs(ray.direction_x) < 1e-10:
            if ray.origin_x < rect.left or ray.origin_x > rect.right:
                return RaycastHit(hit=False)
        else:
            t1 = (rect.left - ray.origin_x) / ray.direction_x
            t2 = (rect.right - ray.origin_x) / ray.direction_x
            
            normal_x = (-1.0, 0.0) if t1 < t2 else (1.0, 0.0)
            
            if t1 > t2:
                t1, t2 = t2, t1
            
            if t1 > t_min:
                t_min = t1
                normal = normal_x
            t_max = min(t_max, t2)
            
            if t_min > t_max:
                return RaycastHit(hit=False)
        
        # 检查Y轴
        if abs(ray.direction_y) < 1e-10:
            if ray.origin_y < rect.top or ray.origin_y > rect.bottom:
                return RaycastHit(hit=False)
        else:
            t1 = (rect.top - ray.origin_y) / ray.direction_y
            t2 = (rect.bottom - ray.origin_y) / ray.direction_y
            
            normal_y = (0.0, -1.0) if t1 < t2 else (0.0, 1.0)
            
            if t1 > t2:
                t1, t2 = t2, t1
            
            if t1 > t_min:
                t_min = t1
                normal = normal_y
            t_max = min(t_max, t2)
            
            if t_min > t_max:
                return RaycastHit(hit=False)
        
        if t_min < 0:
            return RaycastHit(hit=False)
        
        point = ray.get_point(t_min)
        return RaycastHit(
            hit=True,
            point=point,
            distance=t_min,
            normal=normal,
            shape=rect
        )
    
    @staticmethod
    def ray_circle(ray: Ray, circle: Circle) -> RaycastHit:
        """射线与圆碰撞检测"""
        # 射线原点到圆心的向量
        dx = ray.origin_x - circle.x
        dy = ray.origin_y - circle.y
        
        # 二次方程系数
        a = ray.direction_x ** 2 + ray.direction_y ** 2
        b = 2 * (dx * ray.direction_x + dy * ray.direction_y)
        c = dx ** 2 + dy ** 2 - circle.radius ** 2
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return RaycastHit(hit=False)
        
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)
        
        # 选择最近的正交点
        t = t1 if t1 >= 0 else t2
        
        if t < 0:
            return RaycastHit(hit=False)
        
        point = ray.get_point(t)
        
        # 法向量（从圆心指向碰撞点）
        normal = (
            (point[0] - circle.x) / circle.radius,
            (point[1] - circle.y) / circle.radius
        )
        
        return RaycastHit(
            hit=True,
            point=point,
            distance=t,
            normal=normal,
            shape=circle
        )
    
    @staticmethod
    def ray_line(ray: Ray, line: Line) -> RaycastHit:
        """射线与线段碰撞检测"""
        # 射线参数方程: P = O + t * D
        # 线段参数方程: Q = A + s * (B - A)
        
        dx = line.x2 - line.x1
        dy = line.y2 - line.y1
        
        denominator = ray.direction_x * dy - ray.direction_y * dx
        
        if abs(denominator) < 1e-10:
            return RaycastHit(hit=False)
        
        t = ((line.x1 - ray.origin_x) * dy - (line.y1 - ray.origin_y) * dx) / denominator
        s = ((line.x1 - ray.origin_x) * ray.direction_y - (line.y1 - ray.origin_y) * ray.direction_x) / denominator
        
        if t < 0 or s < 0 or s > 1:
            return RaycastHit(hit=False)
        
        point = ray.get_point(t)
        
        # 法向量
        line_length = math.sqrt(dx * dx + dy * dy)
        normal = (-dy / line_length, dx / line_length)
        
        return RaycastHit(
            hit=True,
            point=point,
            distance=t,
            normal=normal,
            shape=line
        )
    
    @staticmethod
    def ray_polygon(ray: Ray, polygon: Polygon) -> RaycastHit:
        """射线与多边形碰撞检测"""
        closest_hit = RaycastHit(hit=False)
        
        for edge in polygon.get_edges():
            hit = CollisionUtils.ray_line(ray, edge)
            if hit.hit and (not closest_hit.hit or hit.distance < closest_hit.distance):
                closest_hit = hit
                closest_hit.shape = polygon
        
        # 也检查射线原点是否在多边形内
        if CollisionUtils.point_in_polygon(ray.origin_x, ray.origin_y, polygon):
            return RaycastHit(
                hit=True,
                point=(ray.origin_x, ray.origin_y),
                distance=0,
                normal=(0, 0),
                shape=polygon
            )
        
        return closest_hit
    
    # ==================== 碰撞响应 ====================
    
    @staticmethod
    def get_collision_normal_rect_rect(rect1: Rectangle, rect2: Rectangle) -> Optional[Vector2]:
        """获取两个矩形碰撞的碰撞法向量"""
        if not CollisionUtils.rectangle_rectangle(rect1, rect2):
            return None
        
        # 计算重叠量
        overlap_x = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
        overlap_y = min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top)
        
        # 返回最小穿透轴的法向量
        if overlap_x < overlap_y:
            return (1.0, 0.0) if rect1.center_x < rect2.center_x else (-1.0, 0.0)
        else:
            return (0.0, 1.0) if rect1.center_y < rect2.center_y else (0.0, -1.0)
    
    @staticmethod
    def resolve_circle_circle(c1: Circle, c2: Circle) -> Optional[Tuple[Vector2, Vector2]]:
        """
        计算两个圆碰撞后的分离向量
        返回 (c1的分离向量, c2的分离向量)
        """
        if not CollisionUtils.circle_circle(c1, c2):
            return None
        
        dx = c2.x - c1.x
        dy = c2.y - c1.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            # 圆心重合，随机选择一个方向
            return ((c1.radius, 0), (-c2.radius, 0))
        
        # 归一化
        nx = dx / distance
        ny = dy / distance
        
        # 计算穿透深度
        overlap = (c1.radius + c2.radius - distance) / 2
        
        return ((-nx * overlap, -ny * overlap), (nx * overlap, ny * overlap))
    
    @staticmethod
    def get_broad_phase_candidates(
        shapes: List[object],
        cell_size: float = 100.0
    ) -> List[Tuple[int, int]]:
        """
        空间分割 - 粗略阶段碰撞检测
        返回可能碰撞的形状对索引
        """
        # 空间哈希
        cells = {}
        
        for i, shape in enumerate(shapes):
            bbox = None
            if isinstance(shape, Rectangle):
                bbox = shape
            elif isinstance(shape, Circle):
                bbox = shape.get_bounding_box()
            elif isinstance(shape, Polygon):
                bbox = shape.get_bounding_box()
            elif isinstance(shape, Line):
                bbox = shape.get_bounding_box()
            
            if bbox is None:
                continue
            
            # 计算形状覆盖的网格单元
            min_cell_x = int(bbox.left // cell_size)
            max_cell_x = int(bbox.right // cell_size)
            min_cell_y = int(bbox.top // cell_size)
            max_cell_y = int(bbox.bottom // cell_size)
            
            for cx in range(min_cell_x, max_cell_x + 1):
                for cy in range(min_cell_y, max_cell_y + 1):
                    key = (cx, cy)
                    if key not in cells:
                        cells[key] = []
                    cells[key].append(i)
        
        # 收集候选对
        candidates = set()
        for cell_shapes in cells.values():
            n = len(cell_shapes)
            for i in range(n):
                for j in range(i + 1, n):
                    pair = (min(cell_shapes[i], cell_shapes[j]), 
                           max(cell_shapes[i], cell_shapes[j]))
                    candidates.add(pair)
        
        return list(candidates)


# 便捷函数
def point_in_circle(px: float, py: float, x: float, y: float, radius: float) -> bool:
    """检查点是否在圆内"""
    return CollisionUtils.point_in_circle(px, py, Circle(x, y, radius))


def point_in_rect(px: float, py: float, x: float, y: float, w: float, h: float) -> bool:
    """检查点是否在矩形内"""
    return CollisionUtils.point_in_rectangle(px, py, Rectangle(x, y, w, h))


def circles_collide(x1: float, y1: float, r1: float, 
                    x2: float, y2: float, r2: float) -> bool:
    """检查两个圆是否碰撞"""
    return CollisionUtils.circle_circle(
        Circle(x1, y1, r1), Circle(x2, y2, r2)
    )


def rects_collide(x1: float, y1: float, w1: float, h1: float,
                   x2: float, y2: float, w2: float, h2: float) -> bool:
    """检查两个矩形是否碰撞"""
    return CollisionUtils.rectangle_rectangle(
        Rectangle(x1, y1, w1, h1), Rectangle(x2, y2, w2, h2)
    )


def rect_circle_collide(rx: float, ry: float, rw: float, rh: float,
                         cx: float, cy: float, cr: float) -> bool:
    """检查矩形和圆是否碰撞"""
    return CollisionUtils.rectangle_circle(
        Rectangle(rx, ry, rw, rh), Circle(cx, cy, cr)
    )


def lines_intersect(x1: float, y1: float, x2: float, y2: float,
                    x3: float, y3: float, x4: float, y4: float) -> bool:
    """检查两条线段是否相交"""
    return CollisionUtils.line_line(
        Line(x1, y1, x2, y2), Line(x3, y3, x4, y4)
    )


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """计算两点之间的距离"""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """计算两点之间距离的平方"""
    dx = x2 - x1
    dy = y2 - y1
    return dx * dx + dy * dy


# 示例用法
if __name__ == "__main__":
    # 点碰撞测试
    print("=== 点碰撞测试 ===")
    circle = Circle(0, 0, 5)
    print(f"点(3,4)在圆内: {CollisionUtils.point_in_circle(3, 4, circle)}")  # True
    print(f"点(6,6)在圆内: {CollisionUtils.point_in_circle(6, 6, circle)}")  # False
    
    # 矩形碰撞测试
    print("\n=== 矩形碰撞测试 ===")
    rect1 = Rectangle(0, 0, 10, 10)
    rect2 = Rectangle(5, 5, 10, 10)
    rect3 = Rectangle(20, 20, 10, 10)
    print(f"矩形1和矩形2碰撞: {CollisionUtils.rectangle_rectangle(rect1, rect2)}")  # True
    print(f"矩形1和矩形3碰撞: {CollisionUtils.rectangle_rectangle(rect1, rect3)}")  # False
    
    # 圆碰撞测试
    print("\n=== 圆碰撞测试 ===")
    c1 = Circle(0, 0, 5)
    c2 = Circle(8, 0, 5)
    c3 = Circle(20, 0, 5)
    print(f"圆1和圆2碰撞: {CollisionUtils.circle_circle(c1, c2)}")  # True
    print(f"圆1和圆3碰撞: {CollisionUtils.circle_circle(c1, c3)}")  # False
    
    # 矩形-圆碰撞测试
    print("\n=== 矩形-圆碰撞测试 ===")
    rect = Rectangle(0, 0, 10, 10)
    circle1 = Circle(5, 5, 3)
    circle2 = Circle(20, 20, 3)
    print(f"矩形和圆1碰撞: {CollisionUtils.rectangle_circle(rect, circle1)}")  # True
    print(f"矩形和圆2碰撞: {CollisionUtils.rectangle_circle(rect, circle2)}")  # False
    
    # 线段相交测试
    print("\n=== 线段相交测试 ===")
    line1 = Line(0, 0, 10, 10)
    line2 = Line(0, 10, 10, 0)
    line3 = Line(20, 20, 30, 30)
    print(f"线段1和线段2相交: {CollisionUtils.line_line(line1, line2)}")  # True
    print(f"线段1和线段3相交: {CollisionUtils.line_line(line1, line3)}")  # False
    
    # 多边形碰撞测试
    print("\n=== 多边形碰撞测试 ===")
    triangle = Polygon([(0, 0), (10, 0), (5, 10)])
    square = Polygon([(3, 3), (13, 3), (13, 13), (3, 13)])
    far_shape = Polygon([(100, 100), (110, 100), (105, 110)])
    print(f"三角形和正方形碰撞: {CollisionUtils.polygon_polygon(triangle, square)}")  # True
    print(f"三角形和远形状碰撞: {CollisionUtils.polygon_polygon(triangle, far_shape)}")  # False
    
    # 射线碰撞测试
    print("\n=== 射线碰撞测试 ===")
    ray = Ray(0, 5, 1, 0)
    rect = Rectangle(10, 0, 10, 10)
    hit = CollisionUtils.ray_rectangle(ray, rect)
    print(f"射线击中矩形: {hit.hit}, 距离: {hit.distance:.2f}, 点: {hit.point}")  # True, 10, (10, 5)
    
    # 便捷函数测试
    print("\n=== 便捷函数测试 ===")
    print(f"点(3,4)在圆(0,0,r=5)内: {point_in_circle(3, 4, 0, 0, 5)}")  # True
    print(f"两个圆碰撞: {circles_collide(0, 0, 5, 8, 0, 5)}")  # True
    print(f"两个矩形碰撞: {rects_collide(0, 0, 10, 10, 5, 5, 10, 10)}")  # True
    print(f"两点距离: {distance(0, 0, 3, 4):.2f}")  # 5.00