"""
中国身份证工具模块 (Chinese ID Card Utilities)

提供中国大陆居民身份证号码的验证、解析和信息提取功能。

功能:
- 身份证号码格式验证
- 校验码计算与验证
- 地区码解析（省市区）
- 出生日期提取
- 性别判断
- 年龄计算
- 十五位转十八位
- 身份证信息批量解析
- 星座和生肖计算
- 测试数据生成

使用示例:
    from chinese_id_utils import parse_id, is_valid_id
    
    # 验证身份证
    if is_valid_id('11010519491231002X'):
        print("身份证有效")
    
    # 解析身份证获取详细信息
    info = parse_id('11010519491231002X')
    print(f"省份: {info.province}")
    print(f"出生日期: {info.birth_date}")
    print(f"性别: {info.gender}")
    print(f"年龄: {info.age}")
"""

from .mod import (
    # 数据类型
    IDInfo,
    CHECKSUM_WEIGHTS,
    CHECKSUM_CODES,
    PROVINCE_CODES,
    DISTRICT_CODES,
    
    # 核心功能
    validate_format,
    calculate_checksum,
    validate_checksum,
    convert_15_to_18,
    extract_birth_date,
    extract_gender,
    calculate_age,
    
    # 地区解析
    get_province,
    get_city,
    get_district,
    
    # 综合解析
    parse_id,
    is_valid_id,
    batch_parse,
    
    # 附加功能
    get_zodiac,
    get_chinese_zodiac,
    format_id_info,
    
    # 测试数据生成
    generate_random_id,
)

__version__ = '1.0.0'
__author__ = 'AllToolkit'
__all__ = [
    'IDInfo',
    'CHECKSUM_WEIGHTS',
    'CHECKSUM_CODES',
    'PROVINCE_CODES',
    'DISTRICT_CODES',
    'validate_format',
    'calculate_checksum',
    'validate_checksum',
    'convert_15_to_18',
    'extract_birth_date',
    'extract_gender',
    'calculate_age',
    'get_province',
    'get_city',
    'get_district',
    'parse_id',
    'is_valid_id',
    'batch_parse',
    'get_zodiac',
    'get_chinese_zodiac',
    'format_id_info',
    'generate_random_id',
]