"""
Data Masking Utils - 敏感数据脱敏工具

提供常用敏感数据的脱敏处理功能，支持：
- 手机号脱敏
- 身份证号脱敏
- 银行卡号脱敏
- 邮箱脱敏
- 姓名脱敏
- 地址脱敏
- IP地址脱敏
- 自定义规则脱敏

零外部依赖，纯Python实现。
"""

__version__ = "1.0.0"
__author__ = "AllToolkit"

from .masker import (
    mask_phone,
    mask_id_card,
    mask_bank_card,
    mask_email,
    mask_name,
    mask_address,
    mask_ip,
    mask_custom,
    mask_string,
    DataMasker,
    MaskRule,
    MaskMode,
)

__all__ = [
    "mask_phone",
    "mask_id_card",
    "mask_bank_card",
    "mask_email",
    "mask_name",
    "mask_address",
    "mask_ip",
    "mask_custom",
    "mask_string",
    "DataMasker",
    "MaskRule",
    "MaskMode",
]