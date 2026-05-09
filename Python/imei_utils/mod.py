"""
IMEI 工具模块 - 国际移动设备识别码处理工具

功能:
- IMEI 验证（Luhn算法）
- IMEI 校验位计算
- IMEI 解析（TAC、SNR、校验位）
- 随机有效 IMEI 生成（测试用）
- IMEI 格式化

作者: AllToolkit 自动生成
日期: 2026-05-09
"""

import random
from typing import Optional, Dict, Tuple


def calculate_luhn_checksum(digits: str) -> int:
    """
    使用 Luhn 算法计算校验位
    
    Args:
        digits: 前14位数字字符串
        
    Returns:
        校验位 (0-9)
        
    Raises:
        ValueError: 如果输入不是14位数字
    """
    if not digits.isdigit() or len(digits) != 14:
        raise ValueError("输入必须是14位数字")
    
    # 从右向左遍历，偶数位置乘以2
    total = 0
    digit_list = [int(d) for d in digits]
    
    # 从右向左，偶数位置（从右数第2,4,6...）乘以2
    for i in range(len(digit_list) - 1, -1, -1):
        # 计算从右向左的位置（1开始）
        pos_from_right = len(digit_list) - i
        if pos_from_right % 2 == 0:  # 偶数位置
            digit_list[i] *= 2
            if digit_list[i] > 9:
                digit_list[i] -= 9
        total += digit_list[i]
    
    # 校验位是让总和成为10的倍数的数
    checksum = (10 - (total % 10)) % 10
    return checksum


def validate_imei(imei: str) -> bool:
    """
    验证 IMEI 是否有效
    
    Args:
        imei: IMEI 字符串（15位数字，可包含分隔符）
        
    Returns:
        True 如果有效，False 否则
    """
    # 移除分隔符
    clean_imei = imei.replace('-', '').replace(' ', '')
    
    # 检查格式
    if not clean_imei.isdigit() or len(clean_imei) != 15:
        return False
    
    # 使用 Luhn 算法验证
    digits = clean_imei[:14]
    checksum = clean_imei[14]
    
    try:
        expected = calculate_luhn_checksum(digits)
        return int(checksum) == expected
    except ValueError:
        return False


def parse_imei(imei: str) -> Optional[Dict[str, str]]:
    """
    解析 IMEI，提取各部分信息
    
    IMEI 结构 (15位):
    - TAC (Type Allocation Code): 前8位，设备型号识别
    - SNR (Serial Number): 中间6位，序列号
    - CD (Check Digit): 最后1位，校验位
    
    Args:
        imei: IMEI 字符串
        
    Returns:
        包含解析结果的字典，或 None 如果无效
    """
    clean_imei = imei.replace('-', '').replace(' ', '')
    
    if not validate_imei(clean_imei):
        return None
    
    return {
        'imei': clean_imei,
        'tac': clean_imei[:8],      # Type Allocation Code
        'snr': clean_imei[8:14],    # Serial Number
        'checksum': clean_imei[14], # Check Digit
        'formatted': format_imei(clean_imei)
    }


def format_imei(imei: str, separator: str = '-') -> str:
    """
    格式化 IMEI 显示
    
    标准格式: TAC-SNR-CD (8-6-1)
    例如: 35-209009-176548-3
    
    Args:
        imei: IMEI 字符串
        separator: 分隔符，默认为 '-'
        
    Returns:
        格式化后的 IMEI
    """
    clean_imei = imei.replace('-', '').replace(' ', '')
    
    if not clean_imei.isdigit() or len(clean_imei) != 15:
        raise ValueError("IMEI 必须是15位数字")
    
    return f"{clean_imei[:8]}{separator}{clean_imei[8:14]}{separator}{clean_imei[14]}"


def generate_random_imei(tac: Optional[str] = None) -> str:
    """
    生成随机有效 IMEI（仅用于测试目的）
    
    Args:
        tac: 可选的8位 TAC 码，如果不提供则随机生成
        
    Returns:
        15位有效 IMEI 字符串
        
    Note:
        此函数仅用于测试，生成的 IMEI 不对应真实设备
    """
    # 生成或验证 TAC
    if tac:
        if not tac.isdigit() or len(tac) != 8:
            raise ValueError("TAC 必须是8位数字")
    else:
        # 使用测试范围的 TAC (35xxxxxx 常见用于测试)
        tac = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    
    # 生成6位序列号
    snr = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # 组合前14位
    digits = tac + snr
    
    # 计算校验位
    checksum = calculate_luhn_checksum(digits)
    
    return digits + str(checksum)


def generate_batch_imeis(count: int, tac: Optional[str] = None) -> list:
    """
    批量生成随机有效 IMEI（仅用于测试）
    
    Args:
        count: 生成数量
        tac: 可选的8位 TAC 码
        
    Returns:
        IMEI 字符串列表
        
    Raises:
        ValueError: 如果数量不在 1-10000 范围内
    """
    if count < 1 or count > 10000:
        raise ValueError("数量必须在 1-10000 之间")
    
    return [generate_random_imei(tac) for _ in range(count)]


def get_imei_type(tac: str) -> str:
    """
    根据 TAC 获取设备类型描述（简化版）
    
    注意：完整的 TAC 数据库需要外部数据源，
    这里仅提供基本的范围判断
    
    Args:
        tac: 8位 TAC 码
        
    Returns:
        设备类型描述
    """
    if not tac.isdigit() or len(tac) != 8:
        return "无效的 TAC"
    
    # 常见测试 TAC 范围
    tac_int = int(tac[:2])
    
    if tac.startswith('00'):
        return "测试/假设备"
    elif 35 <= tac_int <= 44:
        return "常见移动设备"
    elif 86 <= tac_int <= 99:
        return "测试/保留范围"
    else:
        return "标准分配"


def compare_imeis(imei1: str, imei2: str) -> Dict[str, any]:
    """
    比较两个 IMEI
    
    Args:
        imei1: 第一个 IMEI
        imei2: 第二个 IMEI
        
    Returns:
        包含比较结果的字典
    """
    clean1 = imei1.replace('-', '').replace(' ', '')
    clean2 = imei2.replace('-', '').replace(' ', '')
    
    result = {
        'imei1_valid': validate_imei(clean1),
        'imei2_valid': validate_imei(clean2),
        'are_equal': clean1 == clean2,
        'same_tac': clean1[:8] == clean2[:8] if len(clean1) >= 8 and len(clean2) >= 8 else False,
        'same_manufacturer_batch': clean1[:10] == clean2[:10] if len(clean1) >= 10 and len(clean2) >= 10 else False
    }
    
    return result


def extract_tac_info(tac: str) -> Dict[str, str]:
    """
    从 TAC 提取基本信息
    
    TAC 前2位通常代表报告体标识符（Reporting Body Identifier）
    
    Args:
        tac: 8位 TAC 码
        
    Returns:
        包含 TAC 信息的字典
    """
    if not tac.isdigit() or len(tac) != 8:
        return {'error': 'TAC 必须是8位数字'}
    
    # Reporting Body Identifier (RBI) - 前2位
    rbi = tac[:2]
    
    # 常见 RBI 对应的报告体
    rbi_map = {
        '01': 'CTIA (美国)',
        '35': 'GSMA (全球)',
        '44': 'PTCRB (北美)',
        '50': 'GCF (全球认证论坛)',
        '86': '中国 (TAF)',
    }
    
    reporting_body = rbi_map.get(rbi, '未知报告体')
    
    return {
        'tac': tac,
        'rbi': rbi,
        'reporting_body': reporting_body,
        'device_type': get_imei_type(tac)
    }


class IMEIValidator:
    """
    IMEI 验证器类
    
    提供面向对象的 IMEI 处理接口
    """
    
    def __init__(self, imei: str):
        """
        初始化验证器
        
        Args:
            imei: IMEI 字符串
        """
        self._raw_imei = imei
        self._clean_imei = imei.replace('-', '').replace(' ', '')
        self._parsed = parse_imei(imei)
    
    @property
    def is_valid(self) -> bool:
        """检查 IMEI 是否有效"""
        return self._parsed is not None
    
    @property
    def tac(self) -> Optional[str]:
        """获取 TAC 码"""
        return self._parsed['tac'] if self._parsed else None
    
    @property
    def snr(self) -> Optional[str]:
        """获取序列号"""
        return self._parsed['snr'] if self._parsed else None
    
    @property
    def checksum(self) -> Optional[str]:
        """获取校验位"""
        return self._parsed['checksum'] if self._parsed else None
    
    @property
    def formatted(self) -> Optional[str]:
        """获取格式化的 IMEI"""
        return self._parsed['formatted'] if self._parsed else None
    
    def __str__(self) -> str:
        return self._clean_imei
    
    def __repr__(self) -> str:
        status = "有效" if self.is_valid else "无效"
        return f"IMEIValidator('{self._clean_imei}' - {status})"


# 模块级别的便捷常量
TEST_TAC_SAMPLE = "35905001"  # 示例测试用 TAC


if __name__ == "__main__":
    # 简单测试
    test_imei = "35-209009-176548-3"
    print(f"验证 IMEI {test_imei}: {validate_imei(test_imei)}")
    
    parsed = parse_imei(test_imei)
    if parsed:
        print(f"解析结果: TAC={parsed['tac']}, SNR={parsed['snr']}, 校验位={parsed['checksum']}")
    
    random_imei = generate_random_imei()
    print(f"随机生成 IMEI: {random_imei} (有效: {validate_imei(random_imei)})")