"""
Luhn Algorithm Utilities

Luhn算法工具模块 - 用于验证和生成信用卡号、IMEI等识别号码

主要功能:
- validate(): 验证数字字符串是否符合Luhn算法
- calculate_check_digit(): 计算Luhn校验位
- generate_with_check_digit(): 生成带校验位的完整号码
- format_card_number(): 格式化卡号
- mask_card_number(): 遮蔽卡号中间部分
- identify_card_type(): 识别信用卡类型
- validate_card(): 综合验证信用卡
- generate_test_card(): 生成测试卡号
- validate_imei(): 验证IMEI号码
- generate_imei(): 生成IMEI号码
- extract_luhn_info(): 提取完整信息
"""

from .mod import (
    luhn_checksum,
    calculate_check_digit,
    validate,
    generate_with_check_digit,
    format_card_number,
    mask_card_number,
    identify_card_type,
    validate_card,
    generate_test_card,
    validate_imei,
    generate_imei,
    extract_luhn_info,
)

__all__ = [
    "luhn_checksum",
    "calculate_check_digit",
    "validate",
    "generate_with_check_digit",
    "format_card_number",
    "mask_card_number",
    "identify_card_type",
    "validate_card",
    "generate_test_card",
    "validate_imei",
    "generate_imei",
    "extract_luhn_info",
]

__version__ = "1.0.0"