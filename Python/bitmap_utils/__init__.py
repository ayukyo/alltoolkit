"""
Bitmap Utils - 位图工具库

高效位图实现，支持大规模位集操作。

核心功能：
- Bitmap: 密集位图（适合密集数据）
- SparseBitmap: 稀疏位图（适合稀疏数据）
- 位图运算（AND, OR, XOR, NOT）
- 序列化与反序列化
- 零外部依赖

使用示例：
    from bitmap_utils import Bitmap
    
    bm = Bitmap(64)
    bm.set(10)
    bm.set(20)
    bm.clear(10)
    
    # 位图运算
    bm1 = Bitmap.from_bit_string("11110000")
    bm2 = Bitmap.from_bit_string("11001100")
    result = bm1 & bm2
"""

from .mod import (
    Bitmap,
    SparseBitmap,
    create_bitmap,
    bitmap_from_string,
    bitmap_union,
    bitmap_intersection,
    bitmap_difference,
)

__version__ = "1.0.0"
__all__ = [
    'Bitmap',
    'SparseBitmap',
    'create_bitmap',
    'bitmap_from_string',
    'bitmap_union',
    'bitmap_intersection',
    'bitmap_difference',
]