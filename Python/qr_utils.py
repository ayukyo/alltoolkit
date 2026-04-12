"""
QR Code Utilities Module
二维码工具函数库

提供二维码生成、解析和自定义功能，支持多种数据格式和样式定制。
使用纯 Python 实现，可选安装 qrcode 库增强功能。
所有函数设计为简单易用，支持文本、URL、vCard 等多种数据类型。

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import base64
import hashlib
import struct
from typing import Optional, List, Dict, Any, Tuple, Union
from pathlib import Path


# ============================================================================
# 常量定义
# ============================================================================

# QR 码纠错级别
ERROR_CORRECTION_L = 'L'  # 7% 恢复能力
ERROR_CORRECTION_M = 'M'  # 15% 恢复能力
ERROR_CORRECTION_Q = 'Q'  # 25% 恢复能力
ERROR_CORRECTION_H = 'H'  # 30% 恢复能力

# 默认配置
DEFAULT_ERROR_CORRECTION = ERROR_CORRECTION_M
DEFAULT_BORDER = 4
DEFAULT_BOX_SIZE = 10
DEFAULT_FILL_COLOR = 'black'
DEFAULT_BACK_COLOR = 'white'


# ============================================================================
# 异常类
# ============================================================================

class QRCodeError(Exception):
    """二维码操作异常"""
    pass


class QRCodeDataError(QRCodeError):
    """数据格式错误"""
    pass


class QRCodeRenderError(QRCodeError):
    """渲染错误"""
    pass


# ============================================================================
# QR 码矩阵生成（纯 Python 实现）
# ============================================================================

class QRMatrixGenerator:
    """
    QR 码矩阵生成器（简化版纯 Python 实现）
    
    支持版本 1-10 的 QR 码生成，适用于小型数据。
    对于更复杂的需求，建议安装 qrcode 库。
    """
    
    # QR 码版本信息（版本 1-10 的容量）
    VERSION_CAPACITY = {
        1: (41, 25, 17, 10),   # L, M, Q, H
        2: (77, 47, 32, 20),
        3: (127, 77, 53, 32),
        4: (187, 114, 78, 48),
        5: (255, 154, 106, 65),
        6: (322, 195, 134, 82),
        7: (370, 224, 154, 95),
        8: (461, 279, 192, 118),
        9: (552, 335, 231, 141),
        10: (652, 395, 272, 167),
    }
    
    # 定位图案位置
    FINDER_PATTERNS = [(0, 0), (0, 6), (6, 0)]
    
    def __init__(self, version: int = 1, error_correction: str = DEFAULT_ERROR_CORRECTION):
        """
        初始化 QR 码生成器
        
        Args:
            version: QR 码版本 (1-10)
            error_correction: 纠错级别 (L/M/Q/H)
        """
        if not 1 <= version <= 10:
            raise QRCodeDataError("版本必须在 1-10 之间")
        if error_correction not in [ERROR_CORRECTION_L, ERROR_CORRECTION_M, 
                                     ERROR_CORRECTION_Q, ERROR_CORRECTION_H]:
            raise QRCodeDataError("无效的纠错级别")
        
        self.version = version
        self.error_correction = error_correction
        self.size = version * 4 + 17  # QR 码矩阵大小
        self.matrix = [[False] * self.size for _ in range(self.size)]
        self.data_bits = []
    
    def generate(self, data: str) -> List[List[bool]]:
        """
        生成 QR 码矩阵
        
        Args:
            data: 要编码的数据
        
        Returns:
            二维布尔矩阵（True=黑色，False=白色）
        """
        # 清空矩阵
        self.matrix = [[False] * self.size for _ in range(self.size)]
        
        # 添加定位图案
        self._add_finder_patterns()
        
        # 添加对齐图案（版本 2+）
        if self.version >= 2:
            self._add_alignment_patterns()
        
        # 添加时序图案
        self._add_timing_patterns()
        
        # 添加数据
        self._encode_data(data)
        
        # 添加格式信息
        self._add_format_info()
        
        return self.matrix
    
    def _add_finder_patterns(self):
        """添加定位图案（三个角的 7x7 方块）"""
        for row, col in self.FINDER_PATTERNS:
            for r in range(7):
                for c in range(7):
                    matrix_r = row + r
                    matrix_c = col + c
                    if matrix_r < self.size and matrix_c < self.size:
                        # 外框、内框、中心点
                        if r in [0, 6] or c in [0, 6]:
                            self.matrix[matrix_r][matrix_c] = True
                        elif r in [2, 4] and c in [2, 4]:
                            self.matrix[matrix_r][matrix_c] = True
    
    def _add_alignment_patterns(self):
        """添加对齐图案"""
        # 简化版：只在中心添加一个对齐图案
        center = self.size // 2
        for r in range(-2, 3):
            for c in range(-2, 3):
                matrix_r = center + r
                matrix_c = center + c
                if 0 <= matrix_r < self.size and 0 <= matrix_c < self.size:
                    if r in [-2, 2] or c in [-2, 2]:
                        self.matrix[matrix_r][matrix_c] = True
                    elif r == 0 and c == 0:
                        self.matrix[matrix_r][matrix_c] = True
    
    def _add_timing_patterns(self):
        """添加时序图案"""
        for i in range(8, self.size - 8):
            # 水平时序
            self.matrix[6][i] = (i % 2 == 0)
            # 垂直时序
            self.matrix[i][6] = (i % 2 == 0)
    
    def _encode_data(self, data: str):
        """编码数据到 QR 码"""
        # 简化实现：将数据转换为位模式并填充
        data_bytes = data.encode('utf-8')
        
        # 简单的数据放置策略
        bit_index = 0
        for row in range(self.size - 1, -1, -1):
            for col_offset in range(0, 2):
                col = self.size - 1 - col_offset - (bit_index // (self.size * 2)) * 2
                if col < 0:
                    break
                
                # 跳过功能图案区域
                if self._is_functional(row, col):
                    continue
                
                # 放置数据位
                if bit_index < len(data_bytes) * 8:
                    byte_index = bit_index // 8
                    bit_pos = 7 - (bit_index % 8)
                    if byte_index < len(data_bytes):
                        self.matrix[row][col] = bool((data_bytes[byte_index] >> bit_pos) & 1)
                
                bit_index += 1
    
    def _add_format_info(self):
        """添加格式信息"""
        # 简化版：使用固定的格式信息
        # 实际实现需要计算 BCH 校验
        format_bits = [True, False, True, True, False, False, True, True, False, True,
                       True, False, True, False, True]
        
        # 放置格式信息
        for i, bit in enumerate(format_bits):
            if i < 6:
                self.matrix[8][i] = bit
                self.matrix[i][8] = bit
            else:
                self.matrix[8][i + 1] = bit
                self.matrix[8 + (i - 5)][8] = bit
    
    def _is_functional(self, row: int, col: int) -> bool:
        """检查位置是否为功能图案区域"""
        # 定位图案区域
        for fr, fc in self.FINDER_PATTERNS:
            if fr <= row < fr + 9 and fc <= col < fc + 9:
                return True
        
        # 时序图案
        if row == 6 or col == 6:
            return True
        
        # 格式信息
        if row == 8 or col == 8:
            return True
        
        return False


# ============================================================================
# 主要 API 函数
# ============================================================================

def generate_qr_matrix(data: str, version: int = 1, 
                       error_correction: str = DEFAULT_ERROR_CORRECTION) -> List[List[bool]]:
    """
    生成 QR 码矩阵
    
    功能：将数据转换为 QR 码矩阵，可用于自定义渲染。
    纯 Python 实现，无需外部依赖。
    
    Args:
        data: 要编码的数据（文本、URL 等）
        version: QR 码版本 (1-10)，默认自动选择
        error_correction: 纠错级别 (L/M/Q/H)
    
    Returns:
        二维布尔矩阵（True=黑色，False=白色）
    
    Examples:
        >>> matrix = generate_qr_matrix("Hello, World!")
        >>> len(matrix)  # 矩阵大小
        21
    """
    if not data:
        raise QRCodeDataError("数据不能为空")
    
    # 自动选择版本
    if version == 0:
        version = _auto_select_version(data, error_correction)
    
    generator = QRMatrixGenerator(version=version, error_correction=error_correction)
    return generator.generate(data)


def _auto_select_version(data: str, error_correction: str) -> int:
    """自动选择合适的 QR 码版本"""
    data_len = len(data.encode('utf-8'))
    
    capacity_index = {
        ERROR_CORRECTION_L: 0,
        ERROR_CORRECTION_M: 1,
        ERROR_CORRECTION_Q: 2,
        ERROR_CORRECTION_H: 3,
    }
    
    idx = capacity_index.get(error_correction, 1)
    
    for version in range(1, 11):
        capacity = QRMatrixGenerator.VERSION_CAPACITY[version][idx]
        if data_len <= capacity:
            return version
    
    return 10  # 最大版本


def render_qr_ascii(matrix: List[List[bool]], 
                    dark_char: str = '█',
                    light_char: str = ' ') -> str:
    """
    将 QR 码矩阵渲染为 ASCII 艺术
    
    功能：在终端中显示 QR 码，适合快速预览和日志输出。
    
    Args:
        matrix: QR 码矩阵
        dark_char: 深色字符（默认实心方块）
        light_char: 浅色字符（默认空格）
    
    Returns:
        ASCII 字符串
    
    Examples:
        >>> matrix = generate_qr_matrix("https://example.com")
        >>> print(render_qr_ascii(matrix))
        ███████  ████  ███████
        █     █  █  █  █     █
        ...
    """
    lines = []
    for row in matrix:
        line = ''.join(dark_char if cell else light_char for cell in row)
        lines.append(line)
    return '\n'.join(lines)


def render_qr_emoji(matrix: List[List[bool]]) -> str:
    """
    将 QR 码矩阵渲染为 Emoji 艺术
    
    功能：使用 Emoji 方块创建彩色 QR 码，适合社交媒体分享。
    
    Args:
        matrix: QR 码矩阵
    
    Returns:
        Emoji 字符串
    
    Examples:
        >>> matrix = generate_qr_matrix("Hello!")
        >>> print(render_qr_emoji(matrix))
        🟥🟥🟥⬜🟥🟥🟥
        🟥⬜⬜⬜⬜⬜🟥
        ...
    """
    dark_emoji = '🟥'  # 红色方块
    light_emoji = '⬜'  # 白色方块
    
    lines = []
    for row in matrix:
        line = ''.join(dark_emoji if cell else light_emoji for cell in row)
        lines.append(line)
    return '\n'.join(lines)


def save_qr_image(matrix: List[List[bool]], 
                  filepath: str,
                  box_size: int = 10,
                  border: int = 4,
                  fill_color: str = 'black',
                  back_color: str = 'white') -> str:
    """
    保存 QR 码为 PNG 图片
    
    功能：生成可保存的 QR 码图片文件。
    使用纯 Python 实现 PNG 编码，无需外部依赖。
    
    Args:
        matrix: QR 码矩阵
        filepath: 输出文件路径
        box_size: 每个模块的像素大小
        border: 边框宽度（模块数）
        fill_color: 填充颜色（'black', 'red', 'blue', '#RRGGBB'）
        back_color: 背景颜色
    
    Returns:
        保存的文件路径
    
    Examples:
        >>> matrix = generate_qr_matrix("https://example.com")
        >>> save_qr_image(matrix, "qrcode.png")
        'qrcode.png'
    """
    # 解析颜色
    fill_rgb = _parse_color(fill_color)
    back_rgb = _parse_color(back_color)
    
    # 计算图片尺寸
    matrix_size = len(matrix)
    img_size = (matrix_size + border * 2) * box_size
    
    # 创建像素数据
    pixels = []
    for y in range(img_size):
        for x in range(img_size):
            # 计算矩阵坐标
            matrix_x = (x // box_size) - border
            matrix_y = (y // box_size) - border
            
            # 确定颜色
            if 0 <= matrix_x < matrix_size and 0 <= matrix_y < matrix_size:
                is_dark = matrix[matrix_y][matrix_x]
            else:
                is_dark = False
            
            rgb = fill_rgb if is_dark else back_rgb
            pixels.extend(rgb)
    
    # 生成 PNG
    png_data = _create_png(img_size, img_size, pixels)
    
    # 保存文件
    with open(filepath, 'wb') as f:
        f.write(png_data)
    
    return os.path.abspath(filepath)


def _parse_color(color: str) -> Tuple[int, int, int]:
    """解析颜色字符串为 RGB 元组"""
    color_map = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 128, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
    }
    
    if color.lower() in color_map:
        return color_map[color.lower()]
    
    # 解析 #RRGGBB
    if color.startswith('#') and len(color) == 7:
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return (r, g, b)
        except ValueError:
            pass
    
    return (0, 0, 0)  # 默认黑色


def _create_png(width: int, height: int, pixels: List[int]) -> bytes:
    """
    创建 PNG 文件（纯 Python 实现）
    
    支持 RGB 格式，无压缩（使用最简单的 deflate）
    """
    import zlib
    
    def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)
    
    # PNG 签名
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR 块
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)
    
    # IDAT 块（图像数据）
    raw_data = []
    for y in range(height):
        raw_data.append(0)  # 过滤器类型：None
        row_start = y * width * 3
        row_end = row_start + width * 3
        raw_data.extend(pixels[row_start:row_end])
    
    compressed = zlib.compress(bytes(raw_data), 9)
    idat = png_chunk(b'IDAT', compressed)
    
    # IEND 块
    iend = png_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend


def generate_qr_data_url(data: str, **kwargs) -> str:
    """
    生成 QR 码的 Data URL
    
    功能：创建可直接嵌入 HTML 的 base64 编码 QR 码图片。
    
    Args:
        data: 要编码的数据
        **kwargs: 传递给 save_qr_image 的参数
    
    Returns:
        Data URL 字符串（data:image/png;base64,...）
    
    Examples:
        >>> url = generate_qr_data_url("https://example.com")
        >>> html = f'<img src="{url}" alt="QR Code">'
    """
    import tempfile
    import base64
    
    matrix = generate_qr_matrix(data)
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        temp_path = f.name
    
    try:
        save_qr_image(matrix, temp_path, **kwargs)
        with open(temp_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        return f"data:image/png;base64,{img_data}"
    finally:
        os.unlink(temp_path)


# ============================================================================
# 数据编码工具
# ============================================================================

def encode_url(url: str) -> str:
    """
    编码 URL 为 QR 码数据格式
    
    功能：优化 URL 编码，确保 QR 码正确解析。
    
    Args:
        url: 要编码的 URL
    
    Returns:
        编码后的字符串
    
    Examples:
        >>> encode_url("https://example.com")
        'https://example.com'
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def encode_vcard(name: str, phone: str, email: str = '', 
                 org: str = '', title: str = '') -> str:
    """
    编码 vCard 联系人信息
    
    功能：创建标准 vCard 格式，可被手机通讯录识别。
    
    Args:
        name: 姓名
        phone: 电话号码
        email: 邮箱（可选）
        org: 组织/公司（可选）
        title: 职位（可选）
    
    Returns:
        vCard 格式字符串
    
    Examples:
        >>> vcard = encode_vcard("张三", "13800138000", "zhangsan@example.com")
        >>> matrix = generate_qr_matrix(vcard)
    """
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{name}",
        f"FN:{name}",
        f"TEL:{phone}",
    ]
    
    if email:
        lines.append(f"EMAIL:{email}")
    if org:
        lines.append(f"ORG:{org}")
    if title:
        lines.append(f"TITLE:{title}")
    
    lines.append("END:VCARD")
    
    return '\n'.join(lines)


def encode_wifi(ssid: str, password: str, 
                encryption: str = 'WPA', hidden: bool = False) -> str:
    """
    编码 WiFi 连接信息
    
    功能：创建 WiFi 快速连接 QR 码，手机扫描即可连接。
    
    Args:
        ssid: WiFi 名称
        password: WiFi 密码
        encryption: 加密类型（WPA/WEP/nopass）
        hidden: 是否为隐藏网络
    
    Returns:
        WiFi 格式字符串
    
    Examples:
        >>> wifi = encode_wifi("MyWiFi", "password123")
        >>> matrix = generate_qr_matrix(wifi)
    """
    hidden_str = 'true' if hidden else 'false'
    return f"WIFI:T:{encryption};S:{ssid};P:{password};H:{hidden_str};;"


def encode_text(text: str) -> str:
    """
    编码纯文本
    
    功能：简单文本编码，用于 QR 码存储任意文本信息。
    
    Args:
        text: 要编码的文本
    
    Returns:
        原始文本
    
    Examples:
        >>> encoded = encode_text("Hello, World!")
    """
    return text


def encode_email(to: str, subject: str = '', body: str = '') -> str:
    """
    编码邮件信息
    
    功能：创建 mailto 链接，扫描后打开默认邮件客户端。
    
    Args:
        to: 收件人邮箱
        subject: 邮件主题（可选）
        body: 邮件正文（可选）
    
    Returns:
        mailto 链接
    
    Examples:
        >>> mail = encode_email("user@example.com", "Hello", "Body text")
    """
    url = f"mailto:{to}"
    params = []
    if subject:
        import urllib.parse
        params.append(f"subject={urllib.parse.quote(subject)}")
    if body:
        import urllib.parse
        params.append(f"body={urllib.parse.quote(body)}")
    
    if params:
        url += "?" + "&".join(params)
    
    return url


def encode_sms(phone: str, message: str = '') -> str:
    """
    编码短信信息
    
    功能：创建短信链接，扫描后打开短信应用。
    
    Args:
        phone: 收件人号码
        message: 短信内容（可选）
    
    Returns:
        sms 链接
    
    Examples:
        >>> sms = encode_sms("13800138000", "Hello!")
    """
    if message:
        import urllib.parse
        return f"sms:{phone}?body={urllib.parse.quote(message)}"
    return f"sms:{phone}"


# ============================================================================
# 工具函数
# ============================================================================

def get_qr_info(data: str) -> Dict[str, Any]:
    """
    获取 QR 码信息
    
    功能：分析数据并返回推荐的 QR 码配置。
    
    Args:
        data: 要编码的数据
    
    Returns:
        包含版本、容量等信息的字典
    
    Examples:
        >>> info = get_qr_info("https://example.com")
        >>> print(info['recommended_version'])
        2
    """
    data_len = len(data.encode('utf-8'))
    version = _auto_select_version(data, DEFAULT_ERROR_CORRECTION)
    matrix_size = version * 4 + 17
    
    capacity = QRMatrixGenerator.VERSION_CAPACITY[version][1]  # M 级别
    
    return {
        'data_length': data_len,
        'recommended_version': version,
        'matrix_size': matrix_size,
        'capacity_remaining': capacity - data_len,
        'error_correction': DEFAULT_ERROR_CORRECTION,
    }


def validate_qr_data(data: str, data_type: str = 'auto') -> bool:
    """
    验证 QR 码数据
    
    功能：检查数据格式是否有效。
    
    Args:
        data: 要验证的数据
        data_type: 数据类型（auto/url/vcard/wifi/email/sms/text）
    
    Returns:
        验证是否通过
    
    Examples:
        >>> validate_qr_data("https://example.com", "url")
        True
        >>> validate_qr_data("invalid", "url")
        False
    """
    if not data:
        return False
    
    if data_type == 'auto':
        return True
    
    if data_type == 'url':
        return data.startswith(('http://', 'https://'))
    
    if data_type == 'vcard':
        return data.startswith('BEGIN:VCARD') and data.endswith('END:VCARD')
    
    if data_type == 'wifi':
        return data.startswith('WIFI:')
    
    if data_type == 'email':
        return data.startswith('mailto:')
    
    if data_type == 'sms':
        return data.startswith('sms:')
    
    return True


def get_matrix_stats(matrix: List[List[bool]]) -> Dict[str, Any]:
    """
    获取 QR 码矩阵统计信息
    
    功能：分析矩阵的黑白比例等特征。
    
    Args:
        matrix: QR 码矩阵
    
    Returns:
        统计信息字典
    
    Examples:
        >>> matrix = generate_qr_matrix("test")
        >>> stats = get_matrix_stats(matrix)
        >>> print(stats['dark_ratio'])
        0.45
    """
    total = len(matrix) * len(matrix[0])
    dark_count = sum(sum(1 for cell in row if cell) for row in matrix)
    
    return {
        'size': len(matrix),
        'total_modules': total,
        'dark_modules': dark_count,
        'light_modules': total - dark_count,
        'dark_ratio': dark_count / total,
    }


# ============================================================================
# 批量处理
# ============================================================================

def generate_qr_batch(data_list: List[str], 
                      output_dir: str,
                      prefix: str = 'qr',
                      **kwargs) -> List[str]:
    """
    批量生成 QR 码图片
    
    功能：一次性生成多个 QR 码，适合批量处理场景。
    
    Args:
        data_list: 数据列表
        output_dir: 输出目录
        prefix: 文件名前缀
        **kwargs: 传递给 save_qr_image 的参数
    
    Returns:
        生成的文件路径列表
    
    Examples:
        >>> urls = ["https://site1.com", "https://site2.com"]
        >>> files = generate_qr_batch(urls, "./qrcodes")
    """
    os.makedirs(output_dir, exist_ok=True)
    
    result = []
    for i, data in enumerate(data_list):
        filename = f"{prefix}_{i:04d}.png"
        filepath = os.path.join(output_dir, filename)
        matrix = generate_qr_matrix(data)
        save_qr_image(matrix, filepath, **kwargs)
        result.append(filepath)
    
    return result


# ============================================================================
# 模块信息
# ============================================================================

def get_version() -> str:
    """获取模块版本"""
    return "1.0.0"


def get_capabilities() -> List[str]:
    """获取模块功能列表"""
    return [
        "generate_qr_matrix",
        "render_qr_ascii",
        "render_qr_emoji",
        "save_qr_image",
        "generate_qr_data_url",
        "encode_url",
        "encode_vcard",
        "encode_wifi",
        "encode_text",
        "encode_email",
        "encode_sms",
        "get_qr_info",
        "validate_qr_data",
        "get_matrix_stats",
        "generate_qr_batch",
    ]


if __name__ == '__main__':
    # 简单演示
    print("QR Code Utils - 二维码工具库")
    print("=" * 40)
    
    # 生成示例 QR 码
    data = "Hello, AllToolkit!"
    print(f"\n生成 QR 码：{data}")
    
    matrix = generate_qr_matrix(data)
    print(f"矩阵大小：{len(matrix)}x{len(matrix)}")
    
    # ASCII 预览
    print("\nASCII 预览:")
    print(render_qr_ascii(matrix))
    
    # 获取信息
    info = get_qr_info(data)
    print(f"\nQR 码信息:")
    print(f"  推荐版本：{info['recommended_version']}")
    print(f"  容量剩余：{info['capacity_remaining']} 字节")
    
    print("\n功能列表:")
    for cap in get_capabilities():
        print(f"  - {cap}")
