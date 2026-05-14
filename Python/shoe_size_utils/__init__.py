"""
鞋码转换工具 (shoe_size_utils)

支持各国鞋码系统之间的转换：
- EU (欧洲码)
- US (美国码) - 男/女/儿童
- UK (英国码)
- JP (日本码/厘米)
- CM (厘米)
- CN (中国码/毫米)
- BR (巴西码)
- AU (澳大利亚码)
- MEX (墨西哥码)
- KR (韩国码/毫米)

主要功能：
1. convert_shoe_size() - 单一鞋码转换
2. get_all_sizes() - 获取所有系统鞋码
3. recommend_shoe_size() - 根据脚长推荐鞋码
4. validate_shoe_size() - 验证鞋码合理性
5. compare_sizes() - 比较两个鞋码

示例：
    from shoe_size_utils import convert_shoe_size, get_all_sizes
    
    # 转换鞋码
    us_size = convert_shoe_size(42, "EU", "US_MEN")  # ≈ 8.5
    
    # 获取所有尺码
    all_sizes = get_all_sizes(42, "EU")
    # {'eu': 42, 'us_men': 8.5, 'uk': 8, 'cm': 26.5, ...}
"""

from .mod import (
    # 类
    ShoeSizeConverter,
    ShoeSize,
    SizeSystem,
    Gender,
    
    # 函数
    convert_shoe_size,
    get_all_sizes,
    get_foot_length_info,
    recommend_shoe_size,
    validate_shoe_size,
    compare_sizes,
    find_closest_size,
    
    # 数据
    COMMON_SIZE_CHART,
)

__all__ = [
    "ShoeSizeConverter",
    "ShoeSize",
    "SizeSystem",
    "Gender",
    "convert_shoe_size",
    "get_all_sizes",
    "get_foot_length_info",
    "recommend_shoe_size",
    "validate_shoe_size",
    "compare_sizes",
    "find_closest_size",
    "COMMON_SIZE_CHART",
]

__version__ = "1.0.0"
__author__ = "AllToolkit"
__description__ = "国际鞋码转换工具，支持EU、US、UK、JP、CN等多系统互转"