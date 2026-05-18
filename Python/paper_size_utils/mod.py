"""
AllToolkit - Python Paper Size Utilities

纸张尺寸工具模块，提供国际标准纸张尺寸（ISO A/B/C 系列）、北美纸张尺寸、
像素与纸张尺寸转换、DPI 计算等功能。

零外部依赖，仅使用 Python 标准库。

Author: AllToolkit
License: MIT
"""

from typing import Dict, Tuple, Optional, Union, List, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    pass


# =============================================================================
# 数据结构定义
# =============================================================================

class PaperSeries(Enum):
    """纸张系列枚举。"""
    ISO_A = "ISO A"
    ISO_B = "ISO B"
    ISO_C = "ISO C"
    NORTH_AMERICAN = "North American"
    JIS_B = "JIS B"
    CHINESE = "Chinese"
    PHOTO = "Photo"
    BUSINESS_CARD = "Business Card"
    ENVELOPE = "Envelope"


@dataclass
class PaperSize:
    """
    纸张尺寸数据类。
    
    Attributes:
        name: 纸张名称（如 "A4", "Letter"）
        width_mm: 宽度（毫米）
        height_mm: 高度（毫米）
        series: 纸张系列
        description: 描述信息
    """
    name: str
    width_mm: float
    height_mm: float
    series: PaperSeries
    description: str = ""
    
    @property
    def width_cm(self) -> float:
        """宽度（厘米）。"""
        return self.width_mm / 10
    
    @property
    def height_cm(self) -> float:
        """高度（厘米）。"""
        return self.height_mm / 10
    
    @property
    def width_inch(self) -> float:
        """宽度（英寸）。"""
        return self.width_mm / 25.4
    
    @property
    def height_inch(self) -> float:
        """高度（英寸）。"""
        return self.height_mm / 25.4
    
    @property
    def area_mm2(self) -> float:
        """面积（平方毫米）。"""
        return self.width_mm * self.height_mm
    
    @property
    def area_cm2(self) -> float:
        """面积（平方厘米）。"""
        return self.area_mm2 / 100
    
    @property
    def area_inch2(self) -> float:
        """面积（平方英寸）。"""
        return self.width_inch * self.height_inch
    
    @property
    def aspect_ratio(self) -> float:
        """宽高比。"""
        return self.width_mm / self.height_mm
    
    def to_pixels(self, dpi: int = 300) -> Tuple[int, int]:
        """
        转换为像素尺寸。
        
        Args:
            dpi: 每英寸点数（分辨率）
        
        Returns:
            Tuple[int, int]: (宽度像素, 高度像素)
        """
        width_px = int(round(self.width_inch * dpi))
        height_px = int(round(self.height_inch * dpi))
        return (width_px, height_px)
    
    def get_orientation(self) -> str:
        """获取方向（portrait/landscape）。"""
        return "portrait" if self.height_mm >= self.width_mm else "landscape"
    
    def flip(self) -> 'PaperSize':
        """翻转纸张方向。"""
        return PaperSize(
            name=self.name,
            width_mm=self.height_mm,
            height_mm=self.width_mm,
            series=self.series,
            description=f"{self.description} (flipped)"
        )
    
    def __repr__(self) -> str:
        return f"PaperSize({self.name}: {self.width_mm}×{self.height_mm}mm, {self.series.value})"
    
    def to_dict(self) -> Dict:
        """转换为字典。"""
        return {
            "name": self.name,
            "width_mm": self.width_mm,
            "height_mm": self.height_mm,
            "width_cm": self.width_cm,
            "height_cm": self.height_cm,
            "width_inch": self.width_inch,
            "height_inch": self.height_inch,
            "area_mm2": self.area_mm2,
            "area_cm2": self.area_cm2,
            "area_inch2": self.area_inch2,
            "aspect_ratio": self.aspect_ratio,
            "series": self.series.value,
            "description": self.description,
            "orientation": self.get_orientation(),
        }


# =============================================================================
# 纸张尺寸常量
# =============================================================================

# ISO A 系列（国际标准）
# 基于面积递减，每号面积减半，A0 面积为 1m²，宽高比为 √2:1
ISO_A_SERIES: Dict[str, PaperSize] = {
    "A0": PaperSize("A0", 841, 1189, PaperSeries.ISO_A, "ISO A 系列最大尺寸"),
    "A1": PaperSize("A1", 594, 841, PaperSeries.ISO_A, "海报、大型图纸"),
    "A2": PaperSize("A2", 420, 594, PaperSeries.ISO_A, "海报、图表"),
    "A3": PaperSize("A3", 297, 420, PaperSeries.ISO_A, "图表、报纸"),
    "A4": PaperSize("A4", 210, 297, PaperSeries.ISO_A, "标准办公纸张"),
    "A5": PaperSize("A5", 148, 210, PaperSeries.ISO_A, "笔记本、小册子"),
    "A6": PaperSize("A6", 105, 148, PaperSeries.ISO_A, "明信片"),
    "A7": PaperSize("A7", 74, 105, PaperSeries.ISO_A, "小型便签"),
    "A8": PaperSize("A8", 52, 74, PaperSeries.ISO_A, "名片尺寸"),
    "A9": PaperSize("A9", 37, 52, PaperSeries.ISO_A, "极小尺寸"),
    "A10": PaperSize("A10", 26, 37, PaperSeries.ISO_A, "最小 ISO A 尺寸"),
}

# ISO B 系列（介于 A 系列之间）
# 用于印刷行业，尺寸介于相邻 A 号之间
ISO_B_SERIES: Dict[str, PaperSize] = {
    "B0": PaperSize("B0", 1000, 1414, PaperSeries.ISO_B, "ISO B 系列最大尺寸"),
    "B1": PaperSize("B1", 707, 1000, PaperSeries.ISO_B, "大型海报"),
    "B2": PaperSize("B2", 500, 707, PaperSeries.ISO_B, "海报"),
    "B3": PaperSize("B3", 353, 500, PaperSeries.ISO_B, "图表"),
    "B4": PaperSize("B4", 250, 353, PaperSeries.ISO_B, "报纸"),
    "B5": PaperSize("B5", 176, 250, PaperSeries.ISO_B, "书籍"),
    "B6": PaperSize("B6", 125, 176, PaperSeries.ISO_B, "小册子"),
    "B7": PaperSize("B7", 88, 125, PaperSeries.ISO_B, "便签"),
    "B8": PaperSize("B8", 62, 88, PaperSeries.ISO_B, "小型打印"),
    "B9": PaperSize("B9", 44, 62, PaperSeries.ISO_B, "极小尺寸"),
    "B10": PaperSize("B10", 31, 44, PaperSeries.ISO_B, "最小 ISO B 尺寸"),
}

# ISO C 系列（信封尺寸）
# 设计用于容纳对应的 A 系列纸张
ISO_C_SERIES: Dict[str, PaperSize] = {
    "C0": PaperSize("C0", 917, 1297, PaperSeries.ISO_C, "信封（容纳 A0）"),
    "C1": PaperSize("C1", 648, 917, PaperSeries.ISO_C, "信封（容纳 A1）"),
    "C2": PaperSize("C2", 458, 648, PaperSeries.ISO_C, "信封（容纳 A2）"),
    "C3": PaperSize("C3", 324, 458, PaperSeries.ISO_C, "信封（容纳 A3）"),
    "C4": PaperSize("C4", 229, 324, PaperSeries.ISO_C, "信封（容纳 A4）"),
    "C5": PaperSize("C5", 162, 229, PaperSeries.ISO_C, "信封（容纳 A5）"),
    "C6": PaperSize("C6", 114, 162, PaperSeries.ISO_C, "信封（容纳 A6）"),
    "C7": PaperSize("C7", 81, 114, PaperSeries.ISO_C, "信封（容纳 A7）"),
    "C8": PaperSize("C8", 57, 81, PaperSeries.ISO_C, "小型信封"),
    "C9": PaperSize("C9", 40, 57, PaperSeries.ISO_C, "极小信封"),
    "C10": PaperSize("C10", 28, 40, PaperSeries.ISO_C, "最小 ISO C 尺寸"),
}

# 北美纸张系列（美国、加拿大常用）
NORTH_AMERICAN_SERIES: Dict[str, PaperSize] = {
    "Letter": PaperSize("Letter", 215.9, 279.4, PaperSeries.NORTH_AMERICAN, "美国标准办公纸张 (8.5×11英寸)"),
    "Legal": PaperSize("Legal", 215.9, 355.6, PaperSeries.NORTH_AMERICAN, "美国法律文件纸张 (8.5×14英寸)"),
    "Tabloid": PaperSize("Tabloid", 279.4, 431.8, PaperSeries.NORTH_AMERICAN, "报纸/大型打印 (11×17英寸)"),
    "Ledger": PaperSize("Ledger", 431.8, 279.4, PaperSeries.NORTH_AMERICAN, "账簿纸张 (17×11英寸)"),
    "Executive": PaperSize("Executive", 184.15, 266.7, PaperSeries.NORTH_AMERICAN, "美国行政纸张 (7.25×10.5英寸)"),
    "Half Letter": PaperSize("Half Letter", 139.7, 215.9, PaperSeries.NORTH_AMERICAN, "半 Letter 尺寸 (5.5×8.5英寸)"),
    "Government Letter": PaperSize("Government Letter", 203.2, 266.7, PaperSeries.NORTH_AMERICAN, "美国政府纸张 (8×10.5英寸)"),
    "Government Legal": PaperSize("Government Legal", 203.2, 330.2, PaperSeries.NORTH_AMERICAN, "美国政府法律纸张 (8×13英寸)"),
    "ANSI A": PaperSize("ANSI A", 215.9, 279.4, PaperSeries.NORTH_AMERICAN, "ANSI A (Letter)"),
    "ANSI B": PaperSize("ANSI B", 279.4, 431.8, PaperSeries.NORTH_AMERICAN, "ANSI B (Tabloid/Ledger)"),
    "ANSI C": PaperSize("ANSI C", 431.8, 558.8, PaperSeries.NORTH_AMERICAN, "ANSI C (17×22英寸)"),
    "ANSI D": PaperSize("ANSI D", 558.8, 863.6, PaperSeries.NORTH_AMERICAN, "ANSI D (22×34英寸)"),
    "ANSI E": PaperSize("ANSI E", 863.6, 1117.6, PaperSeries.NORTH_AMERICAN, "ANSI E (34×44英寸)"),
    "Arch A": PaperSize("Arch A", 228.6, 304.8, PaperSeries.NORTH_AMERICAN, "建筑图纸 A (9×12英寸)"),
    "Arch B": PaperSize("Arch B", 304.8, 457.2, PaperSeries.NORTH_AMERICAN, "建筑图纸 B (12×18英寸)"),
    "Arch C": PaperSize("Arch C", 457.2, 609.6, PaperSeries.NORTH_AMERICAN, "建筑图纸 C (18×24英寸)"),
    "Arch D": PaperSize("Arch D", 609.6, 914.4, PaperSeries.NORTH_AMERICAN, "建筑图纸 D (24×36英寸)"),
    "Arch E": PaperSize("Arch E", 914.4, 1219.2, PaperSeries.NORTH_AMERICAN, "建筑图纸 E (36×48英寸)"),
    "Arch E1": PaperSize("Arch E1", 762, 1066.8, PaperSeries.NORTH_AMERICAN, "建筑图纸 E1 (30×42英寸)"),
    "Arch E2": PaperSize("Arch E2", 660.4, 914.4, PaperSeries.NORTH_AMERICAN, "建筑图纸 E2 (26×36英寸)"),
    "Arch E3": PaperSize("Arch E3", 685.8, 990.6, PaperSeries.NORTH_AMERICAN, "建筑图纸 E3 (27×39英寸)"),
}

# JIS B 系列（日本工业标准）
# 与 ISO B 系列略有不同
JIS_B_SERIES: Dict[str, PaperSize] = {
    "JIS B0": PaperSize("JIS B0", 1030, 1456, PaperSeries.JIS_B, "日本标准最大尺寸"),
    "JIS B1": PaperSize("JIS B1", 728, 1030, PaperSeries.JIS_B, "日本大型海报"),
    "JIS B2": PaperSize("JIS B2", 515, 728, PaperSeries.JIS_B, "日本海报"),
    "JIS B3": PaperSize("JIS B3", 364, 515, PaperSeries.JIS_B, "日本图表"),
    "JIS B4": PaperSize("JIS B4", 257, 364, PaperSeries.JIS_B, "日本书籍"),
    "JIS B5": PaperSize("JIS B5", 182, 257, PaperSeries.JIS_B, "日本书籍"),
    "JIS B6": PaperSize("JIS B6", 128, 182, PaperSeries.JIS_B, "日本小册子"),
    "JIS B7": PaperSize("JIS B7", 91, 128, PaperSeries.JIS_B, "日本便签"),
    "JIS B8": PaperSize("JIS B8", 64, 91, PaperSeries.JIS_B, "日本小型打印"),
    "JIS B9": PaperSize("JIS B9", 45, 64, PaperSeries.JIS_B, "日本极小尺寸"),
    "JIS B10": PaperSize("JIS B10", 32, 45, PaperSeries.JIS_B, "日本最小标准尺寸"),
}

# 中国纸张标准
CHINESE_SERIES: Dict[str, PaperSize] = {
    "D0": PaperSize("D0", 764, 1064, PaperSeries.CHINESE, "中国标准最大尺寸"),
    "D1": PaperSize("D1", 532, 760, PaperSeries.CHINESE, "中国大型图纸"),
    "D2": PaperSize("D2", 380, 528, PaperSeries.CHINESE, "中国图纸"),
    "D3": PaperSize("D3", 264, 376, PaperSeries.CHINESE, "中国图纸"),
    "D4": PaperSize("D4", 188, 260, PaperSeries.CHINESE, "中国图纸"),
    "D5": PaperSize("D5", 130, 184, PaperSeries.CHINESE, "中国小型图纸"),
    "D6": PaperSize("D6", 92, 126, PaperSeries.CHINESE, "中国小型图纸"),
}

# 照片尺寸（常用照片打印尺寸）
PHOTO_SIZES: Dict[str, PaperSize] = {
    "2R": PaperSize("2R", 63.5, 88.9, PaperSeries.PHOTO, "照片 2.5×3.5英寸"),
    "3R": PaperSize("3R", 88.9, 127, PaperSeries.PHOTO, "照片 3.5×5英寸"),
    "4R": PaperSize("4R", 101.6, 152.4, PaperSeries.PHOTO, "标准照片 4×6英寸"),
    "5R": PaperSize("5R", 127, 177.8, PaperSeries.PHOTO, "照片 5×7英寸"),
    "6R": PaperSize("6R", 152.4, 203.2, PaperSeries.PHOTO, "照片 6×8英寸"),
    "8R": PaperSize("8R", 203.2, 254, PaperSeries.PHOTO, "照片 8×10英寸"),
    "10R": PaperSize("10R", 254, 304.8, PaperSeries.PHOTO, "照片 10×12英寸"),
    "11R": PaperSize("11R", 279.4, 355.6, PaperSeries.PHOTO, "照片 11×14英寸"),
    "12R": PaperSize("12R", 304.8, 381, PaperSeries.PHOTO, "照片 12×15英寸"),
    "S8R": PaperSize("S8R", 203.2, 304.8, PaperSeries.PHOTO, "照片 8×12英寸"),
    "A4全景": PaperSize("A4全景", 210, 297, PaperSeries.PHOTO, "A4 全景照片"),
    "A3全景": PaperSize("A3全景", 297, 420, PaperSeries.PHOTO, "A3 全景照片"),
}

# 名片尺寸
BUSINESS_CARD_SIZES: Dict[str, PaperSize] = {
    "标准名片": PaperSize("标准名片", 90, 55, PaperSeries.BUSINESS_CARD, "ISO 标准名片"),
    "美国名片": PaperSize("美国名片", 89, 51, PaperSeries.BUSINESS_CARD, "美国标准名片 (3.5×2英寸)"),
    "欧洲名片": PaperSize("欧洲名片", 85, 55, PaperSeries.BUSINESS_CARD, "欧洲标准名片"),
    "中国名片": PaperSize("中国名片", 90, 54, PaperSeries.BUSINESS_CARD, "中国标准名片"),
    "折叠名片": PaperSize("折叠名片", 90, 110, PaperSeries.BUSINESS_CARD, "折叠名片"),
    "方形名片": PaperSize("方形名片", 65, 65, PaperSeries.BUSINESS_CARD, "方形名片"),
}

# 信封尺寸（常用）
ENVELOPE_SIZES: Dict[str, PaperSize] = {
    "DL": PaperSize("DL", 110, 220, PaperSeries.ENVELOPE, "欧洲标准信封（容纳 A4 折叠）"),
    "C6": PaperSize("C6", 114, 162, PaperSeries.ENVELOPE, "信封（容纳 A5 或 A4 折叠）"),
    "C5": PaperSize("C5", 162, 229, PaperSeries.ENVELOPE, "信封（容纳 A5）"),
    "C4": PaperSize("C4", 229, 324, PaperSeries.ENVELOPE, "信封（容纳 A4）"),
    "#10": PaperSize("#10", 104.8, 241.3, PaperSeries.ENVELOPE, "美国标准商务信封 (4.125×9.5英寸)"),
    "#9": PaperSize("#9", 98.4, 225.4, PaperSeries.ENVELOPE, "美国信封 (3.875×8.875英寸)"),
    "#6.75": PaperSize("#6.75", 92.1, 160.6, PaperSeries.ENVELOPE, "美国信封 (3.625×6.375英寸)"),
    "A2": PaperSize("A2", 111.1, 146.1, PaperSeries.ENVELOPE, "美国邀请函信封 (4.375×5.75英寸)"),
    "A7": PaperSize("A7", 133.4, 184.1, PaperSeries.ENVELOPE, "美国邀请函信封 (5.25×7.25英寸)"),
    "A9": PaperSize("A9", 146.1, 222.3, PaperSeries.ENVELOPE, "美国邀请函信封 (5.75×8.75英寸)"),
    "B4": PaperSize("B4", 248, 353, PaperSeries.ENVELOPE, "信封（容纳 B5）"),
    "B5": PaperSize("B5", 176, 250, PaperSeries.ENVELOPE, "信封（容纳 B6）"),
    "B6": PaperSize("B6", 125, 176, PaperSeries.ENVELOPE, "信封"),
}


# =============================================================================
# 合并所有纸张尺寸
# =============================================================================

ALL_PAPER_SIZES: Dict[str, PaperSize] = {}
ALL_PAPER_SIZES.update(ISO_A_SERIES)
ALL_PAPER_SIZES.update(ISO_B_SERIES)
ALL_PAPER_SIZES.update(ISO_C_SERIES)
ALL_PAPER_SIZES.update(NORTH_AMERICAN_SERIES)
ALL_PAPER_SIZES.update(JIS_B_SERIES)
ALL_PAPER_SIZES.update(CHINESE_SERIES)
ALL_PAPER_SIZES.update(PHOTO_SIZES)
ALL_PAPER_SIZES.update(BUSINESS_CARD_SIZES)
ALL_PAPER_SIZES.update(ENVELOPE_SIZES)


# =============================================================================
# 工具函数
# =============================================================================

# 预计算的查找映射（避免重复字符串操作）
_NORMALIZED_PAPER_LOOKUP: Dict[str, PaperSize] = {}

def _init_normalized_lookup():
    """初始化标准化查找映射"""
    global _NORMALIZED_PAPER_LOOKUP
    if _NORMALIZED_PAPER_LOOKUP:
        return
    
    for name, paper in ALL_PAPER_SIZES.items():
        # 标准化名称（去除空格、统一大小写）
        normalized = name.strip().upper()
        _NORMALIZED_PAPER_LOOKUP[normalized] = paper
        # 添加无空格版本
        no_space = normalized.replace(" ", "")
        if no_space != normalized:
            _NORMALIZED_PAPER_LOOKUP[no_space] = paper


def get_paper_size(name: str) -> Optional[PaperSize]:
    """
    获取纸张尺寸信息。
    
    Args:
        name: 纸张名称（如 "A4", "Letter", "B5"）
    
    Returns:
        PaperSize 或 None
    
    Example:
        >>> paper = get_paper_size("A4")
        >>> print(f"{paper.width_mm}×{paper.height_mm}mm")
        210×297mm
    
    Note:
        使用预计算的查找映射，避免重复字符串标准化操作
    """
    # 初始化查找映射（仅首次调用时执行）
    _init_normalized_lookup()
    
    # 标准化输入并直接查找
    normalized = name.strip().upper().replace(" ", "")
    
    return _NORMALIZED_PAPER_LOOKUP.get(normalized)


def get_all_paper_sizes() -> Dict[str, PaperSize]:
    """
    获取所有纸张尺寸。
    
    Returns:
        Dict[str, PaperSize]: 所有纸张尺寸字典
    
    Example:
        >>> sizes = get_all_paper_sizes()
        >>> print(f"共 {len(sizes)} 种纸张尺寸")
    """
    return ALL_PAPER_SIZES.copy()


def get_paper_sizes_by_series(series: PaperSeries) -> Dict[str, PaperSize]:
    """
    获取指定系列的纸张尺寸。
    
    Args:
        series: 纸张系列
    
    Returns:
        Dict[str, PaperSize]: 该系列的纸张尺寸
    
    Example:
        >>> a_series = get_paper_sizes_by_series(PaperSeries.ISO_A)
        >>> print(list(a_series.keys()))
        ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
    """
    result = {}
    for name, paper in ALL_PAPER_SIZES.items():
        if paper.series == series:
            result[name] = paper
    return result


def search_paper_sizes(query: str) -> List[PaperSize]:
    """
    搜索纸张尺寸。
    
    Args:
        query: 搜索关键词
    
    Returns:
        List[PaperSize]: 匹配的纸张尺寸列表
    
    Example:
        >>> results = search_paper_sizes("信封")
        >>> for paper in results:
        ...     print(f"{paper.name}: {paper.description}")
    """
    results = []
    query_lower = query.lower()
    
    for paper in ALL_PAPER_SIZES.values():
        if (query_lower in paper.name.lower() or 
            query_lower in paper.description.lower() or
            query_lower in paper.series.value.lower()):
            results.append(paper)
    
    return results


def mm_to_pixels(mm: float, dpi: int = 300) -> int:
    """
    毫米转像素。
    
    Args:
        mm: 毫米值
        dpi: 每英寸点数
    
    Returns:
        int: 像素值
    
    Example:
        >>> pixels = mm_to_pixels(210, 300)  # A4 宽度
        >>> print(pixels)
        2481
    """
    inch = mm / 25.4
    return int(round(inch * dpi))


def pixels_to_mm(pixels: int, dpi: int = 300) -> float:
    """
    像素转毫米。
    
    Args:
        pixels: 像素值
        dpi: 每英寸点数
    
    Returns:
        float: 毫米值
    
    Example:
        >>> mm = pixels_to_mm(2481, 300)
        >>> print(f"{mm:.2f}mm")
        210.00mm
    """
    inch = pixels / dpi
    return inch * 25.4


def inch_to_mm(inch: float) -> float:
    """
    英寸转毫米。
    
    Args:
        inch: 英寸值
    
    Returns:
        float: 毫米值
    
    Example:
        >>> mm = inch_to_mm(8.5)  # Letter 宽度
        >>> print(f"{mm:.2f}mm")
        215.90mm
    """
    return inch * 25.4


def mm_to_inch(mm: float) -> float:
    """
    毫米转英寸。
    
    Args:
        mm: 毫米值
    
    Returns:
        float: 英寸值
    
    Example:
        >>> inch = mm_to_inch(210)
        >>> print(f"{inch:.4f}inch")
        8.2677inch
    """
    return mm / 25.4


def calculate_pixels_for_paper(paper_name: str, dpi: int = 300) -> Tuple[int, int]:
    """
    计算纸张在指定 DPI 下的像素尺寸。
    
    Args:
        paper_name: 纸张名称
        dpi: 每英寸点数
    
    Returns:
        Tuple[int, int]: (宽度像素, 高度像素)
    
    Raises:
        ValueError: 未知的纸张名称
    
    Example:
        >>> width, height = calculate_pixels_for_paper("A4", 300)
        >>> print(f"{width}×{height}px")
        2481×3508px
    """
    paper = get_paper_size(paper_name)
    if paper is None:
        raise ValueError(f"未知的纸张名称: {paper_name}")
    return paper.to_pixels(dpi)


def calculate_dpi_for_paper(paper_name: str, target_width_px: int, target_height_px: int) -> float:
    """
    计算达到目标像素尺寸所需的 DPI。
    
    Args:
        paper_name: 纸张名称
        target_width_px: 目标宽度（像素）
        target_height_px: 目标高度（像素）
    
    Returns:
        float: DPI 值
    
    Raises:
        ValueError: 未知的纸张名称
    
    Example:
        >>> dpi = calculate_dpi_for_paper("A4", 1920, 1080)
        >>> print(f"DPI: {dpi:.2f}")
    """
    paper = get_paper_size(paper_name)
    if paper is None:
        raise ValueError(f"未知的纸张名称: {paper_name}")
    
    # 计算两个方向的 DPI，取较小值以确保完全覆盖
    dpi_width = target_width_px / paper.width_inch
    dpi_height = target_height_px / paper.height_inch
    
    # 返回较小的 DPI（确保不超出纸张范围）
    return min(dpi_width, dpi_height)


def find_paper_by_dimensions(width: float, height: float, 
                              unit: str = "mm",
                              tolerance: float = 2.0) -> List[PaperSize]:
    """
    根据尺寸查找纸张。
    
    Args:
        width: 宽度
        height: 高度
        unit: 单位（"mm", "cm", "inch", "px"）
        tolerance: 允许误差（毫米）
    
    Returns:
        List[PaperSize]: 匹配的纸张列表
    
    Example:
        >>> papers = find_paper_by_dimensions(210, 297, "mm")
        >>> print(papers[0].name)
        A4
    """
    # 转换为毫米
    if unit == "cm":
        width_mm = width * 10
        height_mm = height * 10
    elif unit == "inch":
        width_mm = width * 25.4
        height_mm = height * 25.4
    elif unit == "px":
        # 需要指定 DPI，这里假设 300 DPI
        width_mm = pixels_to_mm(int(width), 300)
        height_mm = pixels_to_mm(int(height), 300)
    else:  # mm
        width_mm = width
        height_mm = height
    
    results = []
    
    for paper in ALL_PAPER_SIZES.values():
        # 检查正向匹配
        if (abs(paper.width_mm - width_mm) <= tolerance and 
            abs(paper.height_mm - height_mm) <= tolerance):
            results.append(paper)
        # 检查反向匹配（landscape）
        elif (abs(paper.height_mm - width_mm) <= tolerance and 
              abs(paper.width_mm - height_mm) <= tolerance):
            results.append(paper)
    
    return results


def find_paper_by_area(area: float, unit: str = "mm2", tolerance: float = 100.0) -> List[PaperSize]:
    """
    根据面积查找纸张。
    
    Args:
        area: 面积
        unit: 单位（"mm2", "cm2", "inch2"）
        tolerance: 允许误差（平方毫米）
    
    Returns:
        List[PaperSize]: 匹配的纸张列表
    
    Example:
        >>> papers = find_paper_by_area(62370, "mm2")  # A4 面积约 62370 mm²
        >>> print(papers[0].name)
        A4
    """
    # 转换为平方毫米
    if unit == "cm2":
        area_mm2 = area * 100
    elif unit == "inch2":
        area_mm2 = area * 645.16  # 25.4²
    else:  # mm2
        area_mm2 = area
    
    results = []
    
    for paper in ALL_PAPER_SIZES.values():
        if abs(paper.area_mm2 - area_mm2) <= tolerance:
            results.append(paper)
    
    return results


def find_paper_by_aspect_ratio(ratio: float, tolerance: float = 0.05) -> List[PaperSize]:
    """
    根据宽高比查找纸张。
    
    Args:
        ratio: 目标宽高比
        tolerance: 允许误差
    
    Returns:
        List[PaperSize]: 匹配的纸张列表
    
    Example:
        >>> # ISO A 系列宽高比为 √2 ≈ 0.707
        >>> papers = find_paper_by_aspect_ratio(0.707, 0.01)
        >>> for paper in papers[:3]:
        ...     print(paper.name)
        A0
        A1
        A2
    """
    results = []
    
    for paper in ALL_PAPER_SIZES.values():
        # 检查正向和反向比例
        if abs(paper.aspect_ratio - ratio) <= tolerance:
            results.append(paper)
        elif abs(1 / paper.aspect_ratio - ratio) <= tolerance:
            results.append(paper)
    
    return results


def calculate_iso_paper_size(series: str, number: int) -> PaperSize:
    """
    计算任意 ISO 纸张尺寸。
    
    ISO 系列基于以下规则：
    - A0 面积为 1m²，宽高比为 √2:1
    - 每号面积减半，尺寸按 √2 缩放
    
    Args:
        series: 系列（"A", "B", "C"）
        number: 号数（如 A4 的 4）
    
    Returns:
        PaperSize: 计算出的纸张尺寸
    
    Raises:
        ValueError: 无效的系列或号数
    
    Example:
        >>> paper = calculate_iso_paper_size("A", 4)
        >>> print(f"{paper.width_mm:.2f}×{paper.height_mm:.2f}mm")
        210.00×297.00mm
        
        >>> # 计算 A15（扩展）
        >>> paper = calculate_iso_paper_size("A", 15)
        >>> print(f"{paper.width_mm:.4f}×{paper.height_mm:.4f}mm")
    """
    if series.upper() not in ("A", "B", "C"):
        raise ValueError(f"无效的 ISO 系列: {series}")
    
    if number < 0:
        raise ValueError(f"号数必须 >= 0: {number}")
    
    # A0 尺寸
    a0_width = 841  # mm
    a0_height = 1189  # mm
    a0_area = a0_width * a0_height
    
    # √2 比例因子
    sqrt2 = 1.41421356237
    
    series_upper = series.upper()
    
    if series_upper == "A":
        # A 系列每号面积减半
        # A(n) = A0 / 2^n
        scale = sqrt2 ** number
        width = a0_width / scale
        height = a0_height / scale
        
        # 对奇数 n，宽高互换
        if number % 2 == 1:
            width, height = height, width
        
        return PaperSize(
            f"A{number}",
            round(width, 2),
            round(height, 2),
            PaperSeries.ISO_A,
            f"ISO A{number} 系列"
        )
    
    elif series_upper == "B":
        # B 系列介于 A 系列之间
        # B(n) = √(A(n) × A(n-1))
        a_n = calculate_iso_paper_size("A", number)
        a_n_minus_1 = calculate_iso_paper_size("A", number - 1) if number > 0 else PaperSize("A-1", a0_width * sqrt2, a0_height * sqrt2, PaperSeries.ISO_A)
        
        # B 系列是相邻 A 号的几何平均
        b_width = (a_n.width_mm + a_n_minus_1.width_mm) / sqrt2
        b_height = (a_n.height_mm + a_n_minus_1.height_mm) / sqrt2
        
        return PaperSize(
            f"B{number}",
            round(b_width, 2),
            round(b_height, 2),
            PaperSeries.ISO_B,
            f"ISO B{number} 系列"
        )
    
    elif series_upper == "C":
        # C 系列是 A 和 B 的几何平均
        # C(n) = √(A(n) × B(n))
        a_n = calculate_iso_paper_size("A", number)
        b_n = calculate_iso_paper_size("B", number)
        
        c_width = sqrt2 * ((a_n.width_mm + b_n.width_mm) / 2)
        c_height = sqrt2 * ((a_n.height_mm + b_n.height_mm) / 2)
        
        return PaperSize(
            f"C{number}",
            round(c_width, 2),
            round(c_height, 2),
            PaperSeries.ISO_C,
            f"ISO C{number} 系列（信封）"
        )


def scale_paper_to_fit(paper_name: str, target_width: float, target_height: float,
                       unit: str = "mm") -> Tuple[float, float]:
    """
    计算纸张缩放到目标尺寸的缩放比例。
    
    Args:
        paper_name: 纸张名称
        target_width: 目标宽度
        target_height: 目标高度
        unit: 单位（"mm", "cm", "inch", "px"）
    
    Returns:
        Tuple[float, float]: (宽度缩放比例, 高度缩放比例)
    
    Raises:
        ValueError: 未知的纸张名称
    
    Example:
        >>> scale_w, scale_h = scale_paper_to_fit("A4", 400, 400, "mm")
        >>> print(f"宽度缩放: {scale_w:.2f}, 高度缩放: {scale_h:.2f}")
    """
    paper = get_paper_size(paper_name)
    if paper is None:
        raise ValueError(f"未知的纸张名称: {paper_name}")
    
    # 转换目标尺寸为毫米
    if unit == "cm":
        target_width_mm = target_width * 10
        target_height_mm = target_height * 10
    elif unit == "inch":
        target_width_mm = target_width * 25.4
        target_height_mm = target_height * 25.4
    elif unit == "px":
        target_width_mm = pixels_to_mm(int(target_width), 300)
        target_height_mm = pixels_to_mm(int(target_height), 300)
    else:
        target_width_mm = target_width
        target_height_mm = target_height
    
    scale_width = target_width_mm / paper.width_mm
    scale_height = target_height_mm / paper.height_mm
    
    return (scale_width, scale_height)


def get_best_fit_paper(width: float, height: float, 
                       unit: str = "mm",
                       prefer_smaller: bool = False) -> Optional[PaperSize]:
    """
    找到最适合容纳目标尺寸的纸张。
    
    Args:
        width: 目标宽度
        height: 目标高度
        unit: 单位
        prefer_smaller: 是否优先选择较小的纸张
    
    Returns:
        PaperSize: 最佳匹配纸张
    
    Example:
        >>> paper = get_best_fit_paper(200, 280, "mm")
        >>> print(paper.name)
        A4
    """
    # 转换为毫米
    if unit == "cm":
        width_mm = width * 10
        height_mm = height * 10
    elif unit == "inch":
        width_mm = width * 25.4
        height_mm = height * 25.4
    else:
        width_mm = width
        height_mm = height
    
    candidates = []
    
    for paper in ALL_PAPER_SIZES.values():
        # 检查正向
        if paper.width_mm >= width_mm and paper.height_mm >= height_mm:
            waste = (paper.area_mm2 - width_mm * height_mm)
            candidates.append((paper, waste, True))
        # 检查反向（landscape）
        if paper.height_mm >= width_mm and paper.width_mm >= height_mm:
            waste = (paper.area_mm2 - width_mm * height_mm)
            candidates.append((paper, waste, False))
    
    if not candidates:
        return None
    
    # 按浪费面积排序
    if prefer_smaller:
        candidates.sort(key=lambda x: x[1])
    else:
        # 优先选择浪费最小但足够大的
        candidates.sort(key=lambda x: (-1 if x[2] else 1, x[1]))
    
    return candidates[0][0]


def compare_paper_sizes(paper1: str, paper2: str) -> Dict:
    """
    比较两个纸张尺寸。
    
    Args:
        paper1: 第一个纸张名称
        paper2: 第二个纸张名称
    
    Returns:
        Dict: 比较结果
    
    Raises:
        ValueError: 未知的纸张名称
    
    Example:
        >>> result = compare_paper_sizes("A4", "Letter")
        >>> print(f"A4 比 Letter 小 {result['area_ratio']:.2%}")
    """
    p1 = get_paper_size(paper1)
    p2 = get_paper_size(paper2)
    
    if p1 is None:
        raise ValueError(f"未知的纸张名称: {paper1}")
    if p2 is None:
        raise ValueError(f"未知的纸张名称: {paper2}")
    
    return {
        "paper1": p1.to_dict(),
        "paper2": p2.to_dict(),
        "width_difference_mm": p1.width_mm - p2.width_mm,
        "height_difference_mm": p1.height_mm - p2.height_mm,
        "area_difference_mm2": p1.area_mm2 - p2.area_mm2,
        "area_ratio": p1.area_mm2 / p2.area_mm2,
        "is_same_series": p1.series == p2.series,
        "width_ratio": p1.width_mm / p2.width_mm,
        "height_ratio": p1.height_mm / p2.height_mm,
        "larger": p1.name if p1.area_mm2 > p2.area_mm2 else p2.name if p2.area_mm2 > p1.area_mm2 else "相同",
    }


def print_paper_info(paper_name: str) -> str:
    """
    打印纸张详细信息（用于调试/显示）。
    
    Args:
        paper_name: 纸张名称
    
    Returns:
        str: 格式化的信息字符串
    
    Example:
        >>> info = print_paper_info("A4")
        >>> print(info)
    """
    paper = get_paper_size(paper_name)
    if paper is None:
        return f"未知的纸张: {paper_name}"
    
    lines = [
        f"纸张名称: {paper.name}",
        f"系列: {paper.series.value}",
        f"尺寸: {paper.width_mm}×{paper.height_mm} mm",
        f"尺寸: {paper.width_cm:.2f}×{paper.height_cm:.2f} cm",
        f"尺寸: {paper.width_inch:.4f}×{paper.height_inch:.4f} inch",
        f"面积: {paper.area_mm2:.2f} mm²",
        f"面积: {paper.area_cm2:.2f} cm²",
        f"面积: {paper.area_inch2:.4f} inch²",
        f"宽高比: {paper.aspect_ratio:.4f}",
        f"方向: {paper.get_orientation()}",
        f"像素尺寸 (72 DPI): {paper.to_pixels(72)[0]}×{paper.to_pixels(72)[1]} px",
        f"像素尺寸 (150 DPI): {paper.to_pixels(150)[0]}×{paper.to_pixels(150)[1]} px",
        f"像素尺寸 (300 DPI): {paper.to_pixels(300)[0]}×{paper.to_pixels(300)[1]} px",
        f"像素尺寸 (600 DPI): {paper.to_pixels(600)[0]}×{paper.to_pixels(600)[1]} px",
        f"描述: {paper.description}",
    ]
    
    return "\n".join(lines)


def list_available_papers() -> List[str]:
    """
    列出所有可用纸张名称。
    
    Returns:
        List[str]: 纸张名称列表
    
    Example:
        >>> papers = list_available_papers()
        >>> print(f"共 {len(papers)} 种纸张")
    """
    return sorted(ALL_PAPER_SIZES.keys())


def get_series_names() -> List[str]:
    """
    获取所有系列名称。
    
    Returns:
        List[str]: 系列名称列表
    """
    return [series.value for series in PaperSeries]


# =============================================================================
# 模块信息
# =============================================================================

def get_version() -> str:
    """获取模块版本。"""
    return "1.0.0"


def get_module_info() -> Dict:
    """获取模块信息。"""
    return {
        "name": "paper_size_utils",
        "version": get_version(),
        "description": "纸张尺寸工具模块",
        "total_paper_sizes": len(ALL_PAPER_SIZES),
        "series_count": len(PaperSeries),
        "series": get_series_names(),
    }


# =============================================================================
# 主程序入口（用于测试）
# =============================================================================

if __name__ == '__main__':
    print(f"Paper Size Utils v{get_version()}")
    print(f"共收录 {len(ALL_PAPER_SIZES)} 种纸张尺寸")
    print()
    
    # 测试基本功能
    print("=== 基本测试 ===")
    
    # 获取 A4 信息
    a4 = get_paper_size("A4")
    print(f"A4 尺寸: {a4.width_mm}×{a4.height_mm}mm")
    print(f"A4 像素尺寸 (300 DPI): {a4.to_pixels(300)}")
    
    # 获取 Letter 信息
    letter = get_paper_size("Letter")
    print(f"Letter 尺寸: {letter.width_mm:.2f}×{letter.height_mm:.2f}mm")
    
    # 比较纸张
    comparison = compare_paper_sizes("A4", "Letter")
    print(f"A4 与 Letter 比较:")
    print(f"  - 面积比例: {comparison['area_ratio']:.4f}")
    print(f"  - 较大者: {comparison['larger']}")
    
    # 搜索纸张
    print("\n=== 搜索测试 ===")
    envelopes = search_paper_sizes("信封")
    print(f"搜索 '信封' 结果: {len(envelopes)} 个")
    for e in envelopes[:3]:
        print(f"  - {e.name}: {e.description}")
    
    # 根据尺寸查找
    print("\n=== 尺寸查找测试 ===")
    papers = find_paper_by_dimensions(210, 297, "mm")
    print(f"查找 210×297mm: {[p.name for p in papers]}")
    
    # 计算任意 ISO 尺寸
    print("\n=== ISO 计算测试 ===")
    a15 = calculate_iso_paper_size("A", 15)
    print(f"A15: {a15.width_mm:.4f}×{a15.height_mm:.4f}mm")
    
    a_minus_1 = calculate_iso_paper_size("A", -1)
    print(f"A(-1): {a_minus_1.width_mm:.2f}×{a_minus_1.height_mm:.2f}mm")
    
    # 打印详细信息
    print("\n=== 详细信息 ===")
    print(print_paper_info("A4"))
    
    print("\n模块加载成功！")