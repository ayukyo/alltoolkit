"""
QR Code Generator - Pure Python Implementation
零外部依赖的 QR 码生成工具

功能：
- 生成 QR 码（支持 ASCII 输出和矩阵输出）
- 支持数字、字母数字、字节模式编码
- 支持多种纠错级别（L, M, Q, H）
- 支持自定义尺寸
- 完全使用 Python 标准库实现
"""

from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
import re


class ErrorCorrection(Enum):
    """纠错级别"""
    L = 0  # 7% 纠错
    M = 1  # 15% 纠错
    Q = 2  # 25% 纠错
    H = 3  # 30% 纠错


class QRCode:
    """
    QR 码生成器
    
    纯 Python 实现，无外部依赖
    
    示例:
        >>> qr = QRCode("Hello, World!", error_correction=ErrorCorrection.M)
        >>> qr.print_ascii()
        >>> matrix = qr.get_matrix()
    """
    
    # QR 码模式指示符
    MODE_NUMERIC = 0b0001
    MODE_ALPHANUMERIC = 0b0010
    MODE_BYTE = 0b0100
    
    # 纠错级别编码
    EC_LEVELS = {
        ErrorCorrection.L: 0b01,
        ErrorCorrection.M: 0b00,
        ErrorCorrection.Q: 0b11,
        ErrorCorrection.H: 0b10,
    }
    
    # 版本容量表 (版本1-10, 不同纠错级别和模式的容量)
    CAPACITIES = {
        (1, ErrorCorrection.L, 'numeric'): 41,
        (1, ErrorCorrection.L, 'alphanumeric'): 25,
        (1, ErrorCorrection.L, 'byte'): 17,
        (1, ErrorCorrection.M, 'numeric'): 34,
        (1, ErrorCorrection.M, 'alphanumeric'): 20,
        (1, ErrorCorrection.M, 'byte'): 14,
        (1, ErrorCorrection.Q, 'numeric'): 27,
        (1, ErrorCorrection.Q, 'alphanumeric'): 16,
        (1, ErrorCorrection.Q, 'byte'): 11,
        (1, ErrorCorrection.H, 'numeric'): 17,
        (1, ErrorCorrection.H, 'alphanumeric'): 10,
        (1, ErrorCorrection.H, 'byte'): 7,
        (2, ErrorCorrection.L, 'numeric'): 77,
        (2, ErrorCorrection.L, 'alphanumeric'): 47,
        (2, ErrorCorrection.L, 'byte'): 32,
        (2, ErrorCorrection.M, 'numeric'): 63,
        (2, ErrorCorrection.M, 'alphanumeric'): 38,
        (2, ErrorCorrection.M, 'byte'): 26,
        (3, ErrorCorrection.L, 'numeric'): 127,
        (3, ErrorCorrection.L, 'alphanumeric'): 77,
        (3, ErrorCorrection.L, 'byte'): 53,
        (4, ErrorCorrection.L, 'numeric'): 187,
        (4, ErrorCorrection.L, 'alphanumeric'): 114,
        (4, ErrorCorrection.L, 'byte'): 78,
    }
    
    # 版本信息（每个版本的大小和纠错块）
    VERSION_INFO = {
        1: {'size': 21, 'codewords': 26, 'ec_per_block': 7, 'blocks': (1, 0)},
        2: {'size': 25, 'codewords': 44, 'ec_per_block': 10, 'blocks': (1, 0)},
        3: {'size': 29, 'codewords': 70, 'ec_per_block': 13, 'blocks': (1, 0)},
        4: {'size': 33, 'codewords': 100, 'ec_per_block': 17, 'blocks': (1, 0)},
        5: {'size': 37, 'codewords': 134, 'ec_per_block': 22, 'blocks': (1, 0)},
        6: {'size': 41, 'codewords': 172, 'ec_per_block': 28, 'blocks': (1, 0)},
        7: {'size': 45, 'codewords': 196, 'ec_per_block': 36, 'blocks': (2, 0)},
        8: {'size': 49, 'codewords': 242, 'ec_per_block': 40, 'blocks': (2, 0)},
        9: {'size': 53, 'codewords': 292, 'ec_per_block': 44, 'blocks': (2, 0)},
        10: {'size': 57, 'codewords': 346, 'ec_per_block': 48, 'blocks': (2, 0)},
    }
    
    # 对齐图案位置
    ALIGNMENT_POSITIONS = {
        1: [],
        2: [6, 18],
        3: [6, 22],
        4: [6, 26],
        5: [6, 30],
        6: [6, 34],
        7: [6, 22, 38],
        8: [6, 24, 42],
        9: [6, 26, 46],
        10: [6, 28, 50],
    }
    
    # 字母数字模式字符集
    ALPHANUMERIC_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    
    def __init__(
        self,
        data: str,
        error_correction: ErrorCorrection = ErrorCorrection.M,
        version: Optional[int] = None,
        border: int = 4,
        invert: bool = False
    ):
        """
        初始化 QR 码生成器
        
        Args:
            data: 要编码的数据
            error_correction: 纠错级别
            version: QR码版本 (1-10)，None 自动选择
            border: 边框大小（模块数）
            invert: 是否反转颜色
        """
        self.data = data
        self.error_correction = error_correction
        self.border = border
        self.invert = invert
        
        # 确定编码模式
        self.mode = self._detect_mode(data)
        
        # 确定版本
        if version is None:
            self.version = self._calculate_version(data, error_correction)
        else:
            self.version = version
        
        # 生成 QR 码矩阵
        self._matrix = self._generate_qr()
    
    def _detect_mode(self, data: str) -> int:
        """检测编码模式"""
        # 检查是否为纯数字
        if data.isdigit():
            return self.MODE_NUMERIC
        
        # 检查是否为字母数字模式
        if all(c in self.ALPHANUMERIC_CHARS for c in data):
            return self.MODE_ALPHANUMERIC
        
        # 默认字节模式
        return self.MODE_BYTE
    
    def _calculate_version(self, data: str, ec: ErrorCorrection) -> int:
        """计算所需版本"""
        data_len = len(data)
        mode_name = {
            self.MODE_NUMERIC: 'numeric',
            self.MODE_ALPHANUMERIC: 'alphanumeric',
            self.MODE_BYTE: 'byte'
        }[self.mode]
        
        for version in range(1, 11):
            key = (version, ec, mode_name)
            if key in self.CAPACITIES:
                if self.CAPACITIES[key] >= data_len:
                    return version
        
        # 如果超出范围，返回最大支持版本
        return 10
    
    def _encode_data(self) -> List[int]:
        """编码数据为位序列"""
        bits = []
        
        # 模式指示符（4位）
        mode_bits = format(self.mode, '04b')
        bits.extend([int(b) for b in mode_bits])
        
        # 字符计数指示符
        count_bits_len = {self.MODE_NUMERIC: 10, self.MODE_ALPHANUMERIC: 9, self.MODE_BYTE: 8}
        if self.version >= 10:
            count_bits_len[self.MODE_BYTE] = 16
        
        count_bits = format(len(self.data), f'0{count_bits_len[self.mode]}b')
        bits.extend([int(b) for b in count_bits])
        
        # 编码数据
        if self.mode == self.MODE_NUMERIC:
            bits.extend(self._encode_numeric())
        elif self.mode == self.MODE_ALPHANUMERIC:
            bits.extend(self._encode_alphanumeric())
        else:
            bits.extend(self._encode_byte())
        
        return bits
    
    def _encode_numeric(self) -> List[int]:
        """数字模式编码"""
        bits = []
        data = self.data
        
        # 每3位数字为一组
        for i in range(0, len(data), 3):
            group = data[i:i+3]
            if len(group) == 3:
                num = int(group)
                bits.extend([int(b) for b in format(num, '010b')])
            elif len(group) == 2:
                num = int(group)
                bits.extend([int(b) for b in format(num, '07b')])
            else:
                num = int(group)
                bits.extend([int(b) for b in format(num, '04b')])
        
        return bits
    
    def _encode_alphanumeric(self) -> List[int]:
        """字母数字模式编码"""
        bits = []
        data = self.data
        
        # 每2个字符为一组
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                # 两个字符
                val = self.ALPHANUMERIC_CHARS.index(data[i]) * 45
                val += self.ALPHANUMERIC_CHARS.index(data[i+1])
                bits.extend([int(b) for b in format(val, '011b')])
            else:
                # 单个字符
                val = self.ALPHANUMERIC_CHARS.index(data[i])
                bits.extend([int(b) for b in format(val, '06b')])
        
        return bits
    
    def _encode_byte(self) -> List[int]:
        """字节模式编码"""
        bits = []
        for char in self.data:
            byte = ord(char)
            bits.extend([int(b) for b in format(byte, '08b')])
        return bits
    
    def _create_matrix(self) -> List[List[Optional[int]]]:
        """创建空白矩阵"""
        size = self.VERSION_INFO[self.version]['size']
        matrix = [[None for _ in range(size)] for _ in range(size)]
        return matrix
    
    def _add_finder_pattern(self, matrix: List[List[Optional[int]]], row: int, col: int):
        """添加定位图案"""
        for r in range(-1, 8):
            for c in range(-1, 8):
                if row + r < 0 or col + c < 0:
                    continue
                if row + r >= len(matrix) or col + c >= len(matrix):
                    continue
                
                # 定位图案外框
                if r in (-1, 7) or c in (-1, 7):
                    matrix[row + r][col + c] = 0  # 白色边框
                # 定位图案中心
                elif 0 <= r <= 6 and 0 <= c <= 6:
                    if r in (0, 6) or c in (0, 6):
                        matrix[row + r][col + c] = 1  # 黑色边框
                    elif 2 <= r <= 4 and 2 <= c <= 4:
                        matrix[row + r][col + c] = 1  # 黑色中心
                    else:
                        matrix[row + r][col + c] = 0  # 白色内部
    
    def _add_alignment_pattern(self, matrix: List[List[Optional[int]]], center_row: int, center_col: int):
        """添加对齐图案"""
        for r in range(-2, 3):
            for c in range(-2, 3):
                row, col = center_row + r, center_col + c
                if 0 <= row < len(matrix) and 0 <= col < len(matrix):
                    if abs(r) == 2 or abs(c) == 2:
                        matrix[row][col] = 1  # 外框
                    elif r == 0 and c == 0:
                        matrix[row][col] = 1  # 中心
                    elif matrix[row][col] is None:
                        matrix[row][col] = 0  # 内部
    
    def _add_timing_patterns(self, matrix: List[List[Optional[int]]]):
        """添加时序图案"""
        size = len(matrix)
        # 水平时序图案
        for col in range(8, size - 8):
            if matrix[6][col] is None:
                matrix[6][col] = (col + 1) % 2
        
        # 垂直时序图案
        for row in range(8, size - 8):
            if matrix[row][6] is None:
                matrix[row][6] = (row + 1) % 2
    
    def _add_dark_module(self, matrix: List[List[Optional[int]]]):
        """添加暗模块"""
        # 暗模块位置：(version * 4 + 9, 8)
        # 确保在矩阵范围内
        size = len(matrix)
        row = self.version * 4 + 9
        if 0 <= row < size and 0 <= 8 < size:
            matrix[row][8] = 1
    
    def _place_data(self, matrix: List[List[Optional[int]]], bits: List[int]) -> List[List[int]]:
        """放置数据和纠错码"""
        size = len(matrix)
        
        # 添加终止符
        bits.extend([0] * 4)
        
        # 填充到字节边界
        while len(bits) % 8 != 0:
            bits.append(0)
        
        # 添加填充码字
        version_info = self.VERSION_INFO[self.version]
        total_codewords = version_info['codewords']
        data_codewords = (total_codewords - version_info['ec_per_block'] * 
                         (version_info['blocks'][0] + version_info['blocks'][1]))
        
        while len(bits) // 8 < data_codewords:
            bits.extend([1, 1, 1, 0, 1, 1, 0, 0])  # 0xEC
            if len(bits) // 8 < data_codewords:
                bits.extend([0, 0, 0, 1, 0, 0, 0, 1])  # 0x11
        
        # 转换为字节
        codewords = []
        for i in range(0, len(bits), 8):
            codewords.append(int(''.join(str(b) for b in bits[i:i+8]), 2))
        
        # 简化的 Reed-Solomon 编码（仅用于演示）
        ec_codewords = self._generate_ec(codewords, version_info['ec_per_block'])
        codewords.extend(ec_codewords)
        
        # 将数据放入矩阵
        bit_index = 0
        bits = []
        for cw in codewords:
            bits.extend([int(b) for b in format(cw, '08b')])
        
        # 从右下角开始，向上移动
        col = size - 1
        upward = True
        
        while col >= 0:
            if col == 6:  # 跳过时序图案列
                col -= 1
            
            if col < 0:
                break
            
            row = size - 1 if upward else 0
            while 0 <= row < size:
                for c in range(2):
                    current_col = col - c
                    if current_col < 0 or current_col >= size:
                        continue
                    
                    if matrix[row][current_col] is None:
                        if bit_index < len(bits):
                            matrix[row][current_col] = bits[bit_index]
                            bit_index += 1
                        else:
                            matrix[row][current_col] = 0
                
                row += 1 if upward else -1
            
            col -= 2
            upward = not upward
        
        return matrix
    
    def _generate_ec(self, data: List[int], ec_count: int) -> List[int]:
        """生成纠错码（简化的 Reed-Solomon）"""
        # 使用简化的多项式运算
        # 这里使用一个简化的实现，用于演示目的
        result = []
        for i in range(ec_count):
            # 简化的异或运算
            val = 0
            for j, d in enumerate(data):
                val ^= d << ((i + j) % 8)
            result.append((val ^ (i * 17)) % 256)
        return result
    
    def _apply_mask(self, matrix: List[List[int]], mask_pattern: int = 0) -> List[List[int]]:
        """应用掩码图案"""
        size = len(matrix)
        masked = [row[:] for row in matrix]
        
        for row in range(size):
            for col in range(size):
                # 跳过功能图案区域
                if self._is_function_pattern(row, col, size):
                    continue
                
                # 掩码条件（使用掩码模式0：(row + col) % 2 == 0）
                if mask_pattern == 0:
                    if (row + col) % 2 == 0:
                        # 确保值不是 None
                        if masked[row][col] is not None:
                            masked[row][col] = 1 - masked[row][col]
                        else:
                            masked[row][col] = 1  # 默认值
        
        return masked
    
    def _is_function_pattern(self, row: int, col: int, size: int) -> bool:
        """检查是否为功能图案区域"""
        # 定位图案
        if (row < 9 and col < 9) or (row < 9 and col >= size - 8) or (row >= size - 8 and col < 9):
            return True
        
        # 时序图案
        if row == 6 or col == 6:
            return True
        
        return False
    
    def _add_format_info(self, matrix: List[List[int]]) -> List[List[int]]:
        """添加格式信息"""
        size = len(matrix)
        
        # 格式信息（纠错级别 + 掩码模式）
        ec_bits = self.EC_LEVELS[self.error_correction]
        mask_bits = 0  # 掩码模式 0
        format_data = (ec_bits << 3) | mask_bits
        
        # 计算格式信息的纠错码
        format_ec = self._calculate_format_ec(format_data)
        format_bits = (format_data << 10) | format_ec
        
        # 放置格式信息
        for i in range(15):
            bit = (format_bits >> (14 - i)) & 1
            
            # 左上角水平
            if i < 6:
                matrix[8][i] = bit
            elif i == 6:
                matrix[8][7] = bit
            elif i == 7:
                matrix[8][8] = bit
            elif i == 8:
                matrix[7][8] = bit
            else:
                matrix[14 - i][8] = bit
            
            # 右上角和左下角
            if i < 8:
                matrix[8][size - 8 + i] = bit
            else:
                matrix[size - 15 + i][8] = bit
        
        return matrix
    
    def _calculate_format_ec(self, data: int) -> int:
        """计算格式信息的纠错码"""
        # BCH(15,5) 编码
        poly = data << 10
        generator = 0b10100110111
        
        for i in range(4, -1, -1):
            if poly & (1 << (i + 10)):
                poly ^= generator << i
        
        return poly
    
    def _generate_qr(self) -> List[List[int]]:
        """生成完整的 QR 码矩阵"""
        # 创建空白矩阵
        matrix = self._create_matrix()
        
        # 添加定位图案
        size = len(matrix)
        self._add_finder_pattern(matrix, 0, 0)
        self._add_finder_pattern(matrix, 0, size - 7)
        self._add_finder_pattern(matrix, size - 7, 0)
        
        # 添加对齐图案（版本2及以上）
        if self.version >= 2:
            positions = self.ALIGNMENT_POSITIONS[self.version]
            for row in positions:
                for col in positions:
                    # 避免与定位图案重叠
                    if (row < 9 and col < 9) or (row < 9 and col > size - 10) or (row > size - 10 and col < 9):
                        continue
                    self._add_alignment_pattern(matrix, row, col)
        
        # 添加时序图案
        self._add_timing_patterns(matrix)
        
        # 添加暗模块
        self._add_dark_module(matrix)
        
        # 编码数据
        bits = self._encode_data()
        
        # 放置数据
        self._place_data(matrix, bits)
        
        # 应用掩码
        matrix = self._apply_mask(matrix)
        
        # 添加格式信息
        matrix = self._add_format_info(matrix)
        
        # 填充 None 为 0
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] is None:
                    matrix[row][col] = 0
        
        return matrix
    
    def get_matrix(self) -> List[List[int]]:
        """
        获取 QR 码矩阵
        
        Returns:
            二维列表，1 表示黑色模块，0 表示白色模块
        """
        size = self.VERSION_INFO[self.version]['size']
        border_size = size + 2 * self.border
        
        # 添加边框
        result = [[0] * border_size for _ in range(border_size)]
        
        for row in range(size):
            for col in range(size):
                result[row + self.border][col + self.border] = self._matrix[row][col]
        
        if self.invert:
            result = [[1 - cell for cell in row] for row in result]
        
        return result
    
    def print_ascii(self, dark: str = '██', light: str = '  '):
        """
        以 ASCII 艺术打印 QR 码
        
        Args:
            dark: 黑色模块字符
            light: 白色模块字符
        """
        matrix = self.get_matrix()
        for row in matrix:
            print(''.join(dark if cell else light for cell in row))
    
    def get_ascii(self, dark: str = '██', light: str = '  ') -> str:
        """
        获取 ASCII 艺术字符串
        
        Args:
            dark: 黑色模块字符
            light: 白色模块字符
        
        Returns:
            ASCII 艺术字符串
        """
        matrix = self.get_matrix()
        lines = []
        for row in matrix:
            lines.append(''.join(dark if cell else light for cell in row))
        return '\n'.join(lines)
    
    def to_svg(self, size: int = 300, dark_color: str = '#000000', light_color: str = '#FFFFFF') -> str:
        """
        转换为 SVG 格式
        
        Args:
            size: SVG 尺寸（像素）
            dark_color: 黑色模块颜色
            light_color: 白色模块颜色
        
        Returns:
            SVG 字符串
        """
        matrix = self.get_matrix()
        module_count = len(matrix)
        module_size = size / module_count
        
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">',
            f'<rect width="{size}" height="{size}" fill="{light_color}"/>',
        ]
        
        for row in range(module_count):
            for col in range(module_count):
                if matrix[row][col]:
                    x = col * module_size
                    y = row * module_size
                    svg_parts.append(
                        f'<rect x="{x:.2f}" y="{y:.2f}" width="{module_size:.2f}" height="{module_size:.2f}" fill="{dark_color}"/>'
                    )
        
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    def save_svg(self, filename: str, **kwargs):
        """
        保存为 SVG 文件
        
        Args:
            filename: 文件名
            **kwargs: to_svg 方法的参数
        """
        svg_content = self.to_svg(**kwargs)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取 QR 码信息
        
        Returns:
            包含 QR 码信息的字典
        """
        return {
            'version': self.version,
            'size': self.VERSION_INFO[self.version]['size'],
            'module_count': len(self.get_matrix()),
            'error_correction': self.error_correction.name,
            'mode': {
                self.MODE_NUMERIC: 'Numeric',
                self.MODE_ALPHANUMERIC: 'Alphanumeric',
                self.MODE_BYTE: 'Byte'
            }[self.mode],
            'data_length': len(self.data),
            'capacity': self.CAPACITIES.get(
                (self.version, self.error_correction, {
                    self.MODE_NUMERIC: 'numeric',
                    self.MODE_ALPHANUMERIC: 'alphanumeric',
                    self.MODE_BYTE: 'byte'
                }[self.mode]), 0
            )
        }


def generate_qr(
    data: str,
    error_correction: str = 'M',
    border: int = 4,
    invert: bool = False
) -> QRCode:
    """
    快速生成 QR 码的便捷函数
    
    Args:
        data: 要编码的数据
        error_correction: 纠错级别 ('L', 'M', 'Q', 'H')
        border: 边框大小
        invert: 是否反转颜色
    
    Returns:
        QRCode 对象
    
    示例:
        >>> qr = generate_qr("Hello, World!")
        >>> qr.print_ascii()
    """
    ec_map = {
        'L': ErrorCorrection.L,
        'M': ErrorCorrection.M,
        'Q': ErrorCorrection.Q,
        'H': ErrorCorrection.H,
    }
    
    ec = ec_map.get(error_correction.upper(), ErrorCorrection.M)
    return QRCode(data, error_correction=ec, border=border, invert=invert)


def encode_wifi(
    ssid: str,
    password: str,
    security: str = 'WPA',
    hidden: bool = False
) -> str:
    """
    生成 WiFi 配置字符串
    
    Args:
        ssid: WiFi 名称
        password: WiFi 密码
        security: 安全类型 ('WPA', 'WEP', 'nopass')
        hidden: 是否隐藏网络
    
    Returns:
        WiFi 配置字符串
    
    示例:
        >>> wifi_str = encode_wifi("MyWiFi", "password123")
        >>> qr = generate_qr(wifi_str)
        >>> qr.print_ascii()
    """
    # 转义特殊字符
    def escape(s: str) -> str:
        return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('"', '\\"')
    
    parts = [f'WIFI:T:{security};S:{escape(ssid)};P:{escape(password)}']
    if hidden:
        parts.append(';H:true')
    parts.append(';;')
    
    return ''.join(parts)


def encode_vcard(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    organization: Optional[str] = None,
    url: Optional[str] = None,
    address: Optional[str] = None
) -> str:
    """
    生成 vCard 字符串
    
    Args:
        name: 姓名
        phone: 电话号码
        email: 电子邮件
        organization: 组织/公司
        url: 网站
        address: 地址
    
    Returns:
        vCard 字符串
    
    示例:
        >>> vcard = encode_vcard("张三", phone="13800138000", email="zhangsan@example.com")
        >>> qr = generate_qr(vcard)
        >>> qr.print_ascii()
    """
    lines = ['BEGIN:VCARD', 'VERSION:3.0', f'FN:{name}']
    
    # 添加姓名的各个部分
    name_parts = name.split()
    if len(name_parts) >= 2:
        lines.append(f'N:{name_parts[-1]};{" ".join(name_parts[:-1])};;;')
    else:
        lines.append(f'N:{name};;;;')
    
    if phone:
        lines.append(f'TEL;TYPE=CELL:{phone}')
    if email:
        lines.append(f'EMAIL:{email}')
    if organization:
        lines.append(f'ORG:{organization}')
    if url:
        lines.append(f'URL:{url}')
    if address:
        lines.append(f'ADR;TYPE=HOME:;;{address};;;;')
    
    lines.append('END:VCARD')
    return '\n'.join(lines)


def encode_url(url: str) -> str:
    """
    生成 URL 字符串（添加协议前缀）
    
    Args:
        url: URL 地址
    
    Returns:
        格式化的 URL 字符串
    
    示例:
        >>> url_str = encode_url("example.com")
        >>> qr = generate_qr(url_str)
        >>> qr.print_ascii()
    """
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url


def encode_email(
    email: str,
    subject: Optional[str] = None,
    body: Optional[str] = None
) -> str:
    """
    生成电子邮件字符串
    
    Args:
        email: 电子邮件地址
        subject: 邮件主题
        body: 邮件正文
    
    Returns:
        电子邮件字符串
    
    示例:
        >>> email_str = encode_email("test@example.com", subject="Hello", body="World")
        >>> qr = generate_qr(email_str)
        >>> qr.print_ascii()
    """
    from urllib.parse import quote
    
    result = f'mailto:{email}'
    params = []
    
    if subject:
        params.append(f'subject={quote(subject)}')
    if body:
        params.append(f'body={quote(body)}')
    
    if params:
        result += '?' + '&'.join(params)
    
    return result


def encode_sms(
    phone: str,
    message: Optional[str] = None
) -> str:
    """
    生成短信字符串
    
    Args:
        phone: 电话号码
        message: 短信内容
    
    Returns:
        短信字符串
    
    示例:
        >>> sms_str = encode_sms("13800138000", message="Hello")
        >>> qr = generate_qr(sms_str)
        >>> qr.print_ascii()
    """
    from urllib.parse import quote
    
    if message:
        return f'sms:{phone}?body={quote(message)}'
    return f'sms:{phone}'


def encode_geo(
    latitude: float,
    longitude: float,
    altitude: Optional[float] = None
) -> str:
    """
    生成地理位置字符串
    
    Args:
        latitude: 纬度
        longitude: 经度
        altitude: 海拔高度
    
    Returns:
        地理位置字符串
    
    示例:
        >>> geo_str = encode_geo(39.9042, 116.4074)  # 北京
        >>> qr = generate_qr(geo_str)
        >>> qr.print_ascii()
    """
    if altitude is not None:
        return f'geo:{latitude},{longitude},{altitude}'
    return f'geo:{latitude},{longitude}'


if __name__ == '__main__':
    # 简单演示
    print("QR Code Generator Demo")
    print("=" * 50)
    
    # 文本 QR 码
    print("\n1. 文本 QR 码:")
    qr = generate_qr("Hello, QR Code!")
    print(f"版本: {qr.get_info()['version']}")
    print(f"尺寸: {qr.get_info()['size']}x{qr.get_info()['size']}")
    qr.print_ascii()
    
    # WiFi QR 码
    print("\n2. WiFi QR 码:")
    wifi_data = encode_wifi("MyWiFi", "password123")
    qr_wifi = generate_qr(wifi_data)
    print(f"数据: {wifi_data}")
    qr_wifi.print_ascii()
    
    # URL QR 码
    print("\n3. URL QR 码:")
    url_data = encode_url("https://example.com")
    qr_url = generate_qr(url_data)
    print(f"数据: {url_data}")
    qr_url.print_ascii()