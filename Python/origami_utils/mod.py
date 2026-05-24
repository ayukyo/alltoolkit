"""
Origami Utilities - 折纸算法工具

提供折纸相关的计算和工具：
- 折痕展开模式（Crease Pattern）分析
- 折叠步骤序列计算
- 纸张尺寸计算与标准化
- 折叠角度计算
- 几何折叠辅助
- 山折/谷折序列生成
- 经典折纸模型参数

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, Tuple, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum
import math


class FoldType(Enum):
    """折叠类型"""
    MOUNTAIN = "mountain"  # 山折
    VALLEY = "valley"      # 谷折


class PaperSize(Enum):
    """标准纸张尺寸（毫米）"""
    A0 = (841, 1189)
    A1 = (594, 841)
    A2 = (420, 594)
    A3 = (297, 420)
    A4 = (210, 297)
    A5 = (148, 210)
    A6 = (105, 148)
    A7 = (74, 105)
    A8 = (52, 74)
    LETTER = (216, 279)  # US Letter (约)
    LEGAL = (216, 356)   # US Legal (约)
    SQUARE_15 = (150, 150)
    SQUARE_20 = (200, 200)
    SQUARE_25 = (250, 250)


@dataclass
class Crease:
    """折痕定义"""
    start: Tuple[float, float]  # 起点 (x, y)
    end: Tuple[float, float]    # 终点 (x, y)
    fold_type: FoldType          # 折叠类型
    
    @property
    def length(self) -> float:
        """计算折痕长度"""
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        return math.sqrt(dx * dx + dy * dy)
    
    @property
    def midpoint(self) -> Tuple[float, float]:
        """折痕中点"""
        return (
            (self.start[0] + self.end[0]) / 2,
            (self.start[1] + self.end[1]) / 2
        )
    
    @property
    def angle(self) -> float:
        """折痕角度（度）"""
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        return math.degrees(math.atan2(dy, dx))


@dataclass
class CreasePattern:
    """折痕展开模式"""
    width: float
    height: float
    creases: List[Crease]
    
    def get_creases_by_type(self, fold_type: FoldType) -> List[Crease]:
        """按类型获取折痕"""
        return [c for c in self.creases if c.fold_type == fold_type]
    
    def total_crease_length(self) -> float:
        """总折痕长度"""
        return sum(c.length for c in self.creases)
    
    def complexity_score(self) -> int:
        """复杂度评分（基于折痕数量和总长度）"""
        return len(self.creases) + int(self.total_crease_length() / 100)


@dataclass
class FoldStep:
    """折叠步骤"""
    step_number: int
    description: str
    creases: List[Crease]
    notes: Optional[str] = None


class OrigamiUtils:
    """折纸工具类"""
    
    @staticmethod
    def paper_dimensions(size: PaperSize) -> Tuple[float, float]:
        """
        获取纸张尺寸
        
        Args:
            size: 标准纸张大小
            
        Returns:
            (宽度, 高度) 毫米
        """
        return size.value
    
    @staticmethod
    def is_square(width: float, height: float) -> bool:
        """检查是否为正方形"""
        return abs(width - height) < 0.01
    
    @staticmethod
    def make_square(width: float, height: float, 
                    method: str = 'crop') -> Tuple[float, float]:
        """
        将矩形转换为正方形
        
        Args:
            width: 宽度
            height: 高度
            method: 'crop' 裁剪为较小值，'extend' 扩展为较大值
            
        Returns:
            正方形边长
        """
        if method == 'crop':
            return (min(width, height), min(width, height))
        else:
            return (max(width, height), max(width, height))
    
    @staticmethod
    def fold_line_coordinate(paper_width: float, paper_height: float,
                             direction: str,
                             position: float = 0.5) -> Crease:
        """
        计算折叠线坐标
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            direction: 折叠方向
            position: 位置比例 (0-1)，默认 0.5 为中线
            
        Returns:
            Crease 对象
        """
        if direction == 'horizontal':
            y = paper_height * position
            return Crease((0, y), (paper_width, y), FoldType.VALLEY)
        elif direction == 'vertical':
            x = paper_width * position
            return Crease((x, 0), (x, paper_height), FoldType.VALLEY)
        elif direction == 'diagonal':
            return Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY)
        else:  # diagonal2
            return Crease((paper_width, 0), (0, paper_height), FoldType.VALLEY)
    
    @staticmethod
    def divide_paper(paper_width: float, paper_height: float,
                     divisions: int, 
                     direction: str = 'horizontal') -> List[Crease]:
        """
        将纸张等分折痕
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            divisions: 等分数
            direction: 折叠方向
            
        Returns:
            折痕列表
        """
        creases = []
        for i in range(1, divisions):
            position = i / divisions
            crease = OrigamiUtils.fold_line_coordinate(
                paper_width, paper_height, direction, position
            )
            creases.append(crease)
        return creases
    
    @staticmethod
    def grid_creases(paper_width: float, paper_height: float,
                     rows: int, cols: int) -> List[Crease]:
        """
        生成网格折痕
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            rows: 行数
            cols: 列数
            
        Returns:
            折痕列表
        """
        creases = []
        
        # 水平折痕
        for i in range(1, rows):
            y = paper_height * i / rows
            creases.append(Crease((0, y), (paper_width, y), FoldType.VALLEY))
        
        # 垂直折痕
        for i in range(1, cols):
            x = paper_width * i / cols
            creases.append(Crease((x, 0), (x, paper_height), FoldType.VALLEY))
        
        return creases
    
    @staticmethod
    def rabbit_ear_crease(paper_width: float, paper_height: float) -> List[Crease]:
        """
        兔耳折法折痕
        
        将角折叠形成三角形突起的经典折法
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            折痕列表
        """
        creases = []
        # 对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY))
        # 从对角线中点到相邻两边中点的折痕
        mid_x, mid_y = paper_width / 2, paper_height / 2
        creases.append(Crease((mid_x, 0), (mid_x, mid_y), FoldType.MOUNTAIN))
        creases.append(Crease((0, mid_y), (mid_x, mid_y), FoldType.MOUNTAIN))
        return creases
    
    @staticmethod
    def waterbomb_base_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        水弹基础折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        
        # 两条对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.MOUNTAIN))
        creases.append(Crease((paper_width, 0), (0, paper_height), FoldType.MOUNTAIN))
        
        # 水平中线
        mid_y = paper_height / 2
        creases.append(Crease((0, mid_y), (paper_width, mid_y), FoldType.VALLEY))
        
        # 从中点到四个角
        center = (paper_width / 2, paper_height / 2)
        creases.append(Crease(center, (0, 0), FoldType.VALLEY))
        creases.append(Crease(center, (paper_width, 0), FoldType.VALLEY))
        creases.append(Crease(center, (0, paper_height), FoldType.VALLEY))
        creases.append(Crease(center, (paper_width, paper_height), FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def preliminary_base_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        初步基础折痕模式（正方形基础）
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 两条对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY))
        creases.append(Crease((paper_width, 0), (0, paper_height), FoldType.VALLEY))
        
        # 中线
        mid_x, mid_y = center
        creases.append(Crease((0, mid_y), (paper_width, mid_y), FoldType.MOUNTAIN))
        creases.append(Crease((mid_x, 0), (mid_x, paper_height), FoldType.MOUNTAIN))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def blintz_fold_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        Blintz 折法（四角向中心折叠）
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 从四个角到中心的折痕
        corners = [
            (0, 0),
            (paper_width, 0),
            (paper_width, paper_height),
            (0, paper_height)
        ]
        
        for corner in corners:
            creases.append(Crease(corner, center, FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def fish_base_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        鱼基础折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        
        # 对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY))
        
        # 从两角到对角线上
        third_w = paper_width / 3
        third_h = paper_height / 3
        
        creases.append(Crease((0, 0), (third_w, paper_height), FoldType.VALLEY))
        creases.append(Crease((0, 0), (paper_width, third_h), FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def bird_base_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        鸟基础折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        # 先创建初步基础
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY))
        creases.append(Crease((paper_width, 0), (0, paper_height), FoldType.VALLEY))
        
        # 中线
        mid_x, mid_y = center
        creases.append(Crease((0, mid_y), (paper_width, mid_y), FoldType.MOUNTAIN))
        creases.append(Crease((mid_x, 0), (mid_x, paper_height), FoldType.MOUNTAIN))
        
        # 角平分线
        quarter_w = paper_width / 4
        quarter_h = paper_height / 4
        
        creases.append(Crease((quarter_w, 0), (center[0], quarter_h), FoldType.VALLEY))
        creases.append(Crease((paper_width - quarter_w, 0), (center[0], quarter_h), FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def frog_base_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        青蛙基础折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY))
        creases.append(Crease((paper_width, 0), (0, paper_height), FoldType.VALLEY))
        
        # 中线
        mid_x, mid_y = center
        creases.append(Crease((0, mid_y), (paper_width, mid_y), FoldType.MOUNTAIN))
        creases.append(Crease((mid_x, 0), (mid_x, paper_height), FoldType.MOUNTAIN))
        
        # 角到中心的额外折痕
        for i in range(4):
            angle = i * math.pi / 2 + math.pi / 4
            start_x = center[0] + paper_width / 4 * math.cos(angle)
            start_y = center[1] + paper_height / 4 * math.sin(angle)
            creases.append(Crease(center, (start_x, start_y), FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def fold_angle(layers: int = 1) -> float:
        """
        计算折叠角度
        
        Args:
            layers: 纸张层数
            
        Returns:
            折叠角度（度）
        """
        if layers < 1:
            return 0
        return 180 / (layers + 1)
    
    @staticmethod
    def paper_thickness_after_fold(initial_thickness: float, 
                                    folds: int) -> float:
        """
        计算折叠后的纸张厚度
        
        Args:
            initial_thickness: 初始厚度（毫米）
            folds: 折叠次数
            
        Returns:
            折叠后厚度（毫米）
        """
        return initial_thickness * (2 ** folds)
    
    @staticmethod
    def max_folds(paper_thickness: float, paper_length: float) -> int:
        """
        估算最大可折叠次数
        
        基于纸张厚度和长度估算
        
        Args:
            paper_thickness: 纸张厚度（毫米）
            paper_length: 纸张长度（毫米）
            
        Returns:
            预估最大折叠次数
        """
        # Britney Gallivan 公式简化版
        # L = π * t * 2^(n-1) / 6
        # n ≈ log2(6L / (π * t)) + 1
        if paper_thickness <= 0 or paper_length <= 0:
            return 0
        
        import math
        n = math.log2(6 * paper_length / (math.pi * paper_thickness)) + 1
        return max(0, int(n))
    
    @staticmethod
    def mito_creases(paper_width: float, paper_height: float,
                    angle: float) -> List[Crease]:
        """
        生成放射状折痕（类似折纸鹤的展开）
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            angle: 放射角度间隔（度）
            
        Returns:
            折痕列表
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 最大半径（到纸张边缘）
        max_radius = math.sqrt(center[0]**2 + center[1]**2)
        
        num_lines = int(360 / angle)
        for i in range(num_lines):
            theta = math.radians(i * angle)
            end_x = center[0] + max_radius * math.cos(theta)
            end_y = center[1] + max_radius * math.sin(theta)
            
            # 交替山折和谷折
            fold_type = FoldType.MOUNTAIN if i % 2 == 0 else FoldType.VALLEY
            creases.append(Crease(center, (end_x, end_y), fold_type))
        
        return creases
    
    @staticmethod
    def squash_fold_creases(paper_width: float, paper_height: float,
                           corner: str) -> CreasePattern:
        """
        压折折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            corner: 角落位置 (tl=左上, tr=右上, bl=左下, br=右下)
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        corners_map = {
            'tl': (0, 0),
            'tr': (paper_width, 0),
            'bl': (0, paper_height),
            'br': (paper_width, paper_height)
        }
        
        corner_pos = corners_map[corner]
        
        # 从角到中心的折痕
        creases.append(Crease(corner_pos, center, FoldType.VALLEY))
        
        # 从角到相邻边中点的折痕
        if corner in ('tl', 'tr'):
            side_mid = (corner_pos[0], paper_height / 2)
            other_mid = (paper_width / 2, 0)
        else:
            side_mid = (corner_pos[0], paper_height / 2)
            other_mid = (paper_width / 2, paper_height)
        
        creases.append(Crease(corner_pos, side_mid, FoldType.VALLEY))
        creases.append(Crease(corner_pos, other_mid, FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def reverse_fold_creases(paper_width: float, paper_height: float,
                            direction: str) -> CreasePattern:
        """
        翻折折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            direction: 'inside' 内翻折，'outside' 外翻折
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 主折痕
        fold_type = FoldType.MOUNTAIN if direction == 'inside' else FoldType.VALLEY
        
        # 三角形折痕
        creases.append(Crease((0, 0), center, FoldType.VALLEY))
        creases.append(Crease((paper_width, 0), center, FoldType.VALLEY))
        creases.append(Crease((paper_width, paper_height), center, fold_type))
        creases.append(Crease((0, paper_height), center, fold_type))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def petal_fold_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        花瓣折折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 对角线
        creases.append(Crease((0, 0), (paper_width, paper_height), FoldType.VALLEY))
        
        # 中心到边的折痕
        third_h = paper_height / 3
        creases.append(Crease(center, (center[0], third_h), FoldType.MOUNTAIN))
        creases.append(Crease(center, (center[0], paper_height - third_h), FoldType.MOUNTAIN))
        
        # 斜向折痕
        creases.append(Crease((0, paper_height / 3), center, FoldType.VALLEY))
        creases.append(Crease((paper_width, paper_height / 3), center, FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def sink_fold_creases(paper_width: float, paper_height: float) -> CreasePattern:
        """
        沉折折痕模式
        
        Args:
            paper_width: 纸张宽度
            paper_height: 纸张高度
            
        Returns:
            CreasePattern 对象
        """
        creases = []
        center = (paper_width / 2, paper_height / 2)
        
        # 外框
        margin = min(paper_width, paper_height) / 4
        inner_rect = [
            (margin, margin),
            (paper_width - margin, margin),
            (paper_width - margin, paper_height - margin),
            (margin, paper_height - margin)
        ]
        
        # 内框折痕
        for i in range(4):
            start = inner_rect[i]
            end = inner_rect[(i + 1) % 4]
            creases.append(Crease(start, end, FoldType.MOUNTAIN))
        
        # 角到内框角
        corners = [(0, 0), (paper_width, 0), 
                   (paper_width, paper_height), (0, paper_height)]
        for i, corner in enumerate(corners):
            creases.append(Crease(corner, inner_rect[i], FoldType.VALLEY))
        
        return CreasePattern(paper_width, paper_height, creases)
    
    @staticmethod
    def generate_fold_sequence(pattern: CreasePattern) -> List[FoldStep]:
        """
        根据折痕模式生成折叠步骤
        
        Args:
            pattern: 折痕模式
            
        Returns:
            折叠步骤列表
        """
        steps = []
        
        # 按类型分组
        valley_creases = pattern.get_creases_by_type(FoldType.VALLEY)
        mountain_creases = pattern.get_creases_by_type(FoldType.MOUNTAIN)
        
        step_num = 1
        
        # 先处理谷折
        if valley_creases:
            desc = f"执行 {len(valley_creases)} 条谷折"
            steps.append(FoldStep(step_num, desc, valley_creases, "谷折：纸张向上凸起"))
            step_num += 1
        
        # 再处理山折
        if mountain_creases:
            desc = f"执行 {len(mountain_creases)} 条山折"
            steps.append(FoldStep(step_num, desc, mountain_creases, "山折：纸张向下凹陷"))
            step_num += 1
        
        return steps
    
    @staticmethod
    def paper_area(width: float, height: float) -> float:
        """计算纸张面积"""
        return width * height
    
    @staticmethod
    def paper_perimeter(width: float, height: float) -> float:
        """计算纸张周长"""
        return 2 * (width + height)
    
    @staticmethod
    def diagonal_length(width: float, height: float) -> float:
        """计算对角线长度"""
        return math.sqrt(width**2 + height**2)
    
    @staticmethod
    def aspect_ratio(width: float, height: float) -> float:
        """计算宽高比"""
        return width / height if height > 0 else 0
    
    @staticmethod
    def is_a_series(width: float, height: float, tolerance: float = 1.0) -> bool:
        """
        检查是否为 A 系列纸张
        
        A 系列纸张的宽高比为 √2:1
        
        Args:
            width: 宽度（毫米）
            height: 高度（毫米）
            tolerance: 容差（毫米）
            
        Returns:
            是否为 A 系列
        """
        ratio = OrigamiUtils.aspect_ratio(width, height)
        sqrt2 = math.sqrt(2)
        # 检查正反两个方向
        return abs(ratio - sqrt2) < tolerance / 100 or abs(1/ratio - sqrt2) < tolerance / 100


# 便捷函数
def create_square_from_a4() -> Tuple[float, float]:
    """从 A4 纸创建正方形（裁剪方案）"""
    width, height = PaperSize.A4.value
    return OrigamiUtils.make_square(width, height, 'crop')


def classic_crane_creases() -> CreasePattern:
    """经典千纸鹤折痕模式（使用标准 15cm 正方形纸）"""
    size = 150  # 15cm = 150mm
    return OrigamiUtils.bird_base_creases(size, size)


def classic_frog_creases() -> CreasePattern:
    """经典青蛙折痕模式（使用标准 15cm 正方形纸）"""
    size = 150  # 15cm = 150mm
    return OrigamiUtils.frog_base_creases(size, size)


def classic_waterbomb_creases() -> CreasePattern:
    """经典水弹折痕模式（使用标准 15cm 正方形纸）"""
    size = 150  # 15cm = 150mm
    return OrigamiUtils.waterbomb_base_creases(size, size)


# 导出
__all__ = [
    'FoldType',
    'PaperSize',
    'Crease',
    'CreasePattern',
    'FoldStep',
    'OrigamiUtils',
    'create_square_from_a4',
    'classic_crane_creases',
    'classic_frog_creases',
    'classic_waterbomb_creases',
]